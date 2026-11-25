"""Synchronous HTTP client for the Hypixel API v2 and the Mojang profile API."""

from __future__ import annotations

import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Generic, Iterable, TypeVar

import requests

from hypixel_stats.models import PlayerProfile
from hypixel_stats.parser import parse_player

HYPIXEL_API = "https://api.hypixel.net/v2"
MOJANG_LOOKUPS = (
    "https://api.mojang.com/users/profiles/minecraft/{name}",
    "https://api.minecraftservices.com/minecraft/profile/lookup/name/{name}",
)
USER_AGENT = "hypixel-stats-dashboard/2.0"

_USERNAME = re.compile(r"^[A-Za-z0-9_]{1,16}$")
_UUID = re.compile(r"^[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}$")


# --------------------------------------------------------------------------- Errors

class HypixelError(Exception):
    """Base error. The message is meant to be shown to the user (in French)."""


class InvalidApiKey(HypixelError):
    pass


class PlayerNotFound(HypixelError):
    pass


class RateLimited(HypixelError):
    pass


# --------------------------------------------------------------------------- Cache

T = TypeVar("T")


class TTLCache(Generic[T]):
    """Tiny thread-safe cache with per-entry expiry."""

    def __init__(self, ttl: float, clock: Callable[[], float] = time.monotonic):
        self.ttl = ttl
        self._clock = clock
        self._data: dict[str, tuple[float, T]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> T | None:
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return None
            expires, value = entry
            if expires < self._clock():
                del self._data[key]
                return None
            return value

    def set(self, key: str, value: T) -> None:
        with self._lock:
            self._data[key] = (self._clock() + self.ttl, value)

    def clear(self) -> None:
        with self._lock:
            self._data.clear()


# --------------------------------------------------------------------------- Client

def parse_player_names(raw: str | None) -> list[str]:
    """Split user input on commas/whitespace, dropping blanks and duplicates."""
    seen: dict[str, str] = {}
    for part in re.split(r"[\s,;]+", raw or ""):
        part = part.strip()
        if part and part.lower() not in seen:
            seen[part.lower()] = part
    return list(seen.values())


class HypixelClient:
    def __init__(
        self,
        api_key: str,
        *,
        session: requests.Session | None = None,
        timeout: float = 10,
        player_cache: TTLCache[dict[str, Any]] | None = None,
        uuid_cache: TTLCache[tuple[str, str]] | None = None,
    ):
        self.api_key = (api_key or "").strip()
        self.session = session or requests.Session()
        self.session.headers.setdefault("User-Agent", USER_AGENT)
        self.timeout = timeout
        self.player_cache = player_cache if player_cache is not None else TTLCache(120)
        self.uuid_cache = uuid_cache if uuid_cache is not None else TTLCache(3600)

    # ---- Mojang

    def resolve(self, name_or_uuid: str) -> tuple[str, str]:
        """Return (uuid without dashes, display name) for a username or UUID."""
        query = name_or_uuid.strip()
        if _UUID.match(query):
            return query.replace("-", "").lower(), query
        if not _USERNAME.match(query):
            raise PlayerNotFound(f"« {query} » n'est pas un pseudo Minecraft valide.")

        cached = self.uuid_cache.get(query.lower())
        if cached:
            return cached

        last_error: Exception | None = None
        for url in MOJANG_LOOKUPS:
            try:
                response = self.session.get(url.format(name=query), timeout=self.timeout)
            except requests.RequestException as exc:
                last_error = exc
                continue
            if response.status_code in (204, 404):
                raise PlayerNotFound(f"Le compte Minecraft « {query} » n'existe pas.")
            if response.ok:
                data = response.json()
                result = (str(data["id"]).replace("-", "").lower(), str(data.get("name") or query))
                self.uuid_cache.set(query.lower(), result)
                return result
            last_error = HypixelError(f"HTTP {response.status_code}")
        raise HypixelError(f"Impossible de résoudre « {query} » auprès de Mojang ({last_error}).")

    # ---- Hypixel

    def _get(self, endpoint: str, **params: str) -> dict[str, Any]:
        if not self.api_key:
            raise InvalidApiKey("Aucune clé API Hypixel fournie.")
        try:
            response = self.session.get(
                f"{HYPIXEL_API}/{endpoint}",
                params=params,
                headers={"API-Key": self.api_key},
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise HypixelError(f"Impossible de joindre l'API Hypixel ({exc.__class__.__name__}).") from exc

        try:
            payload = response.json()
        except ValueError:
            payload = {}
        cause = payload.get("cause") if isinstance(payload, dict) else None

        if response.status_code == 403:
            raise InvalidApiKey("Clé API Hypixel invalide ou expirée.")
        if response.status_code == 429:
            retry = response.headers.get("Retry-After") or response.headers.get("RateLimit-Reset")
            hint = f" Réessayez dans {retry} s." if retry else ""
            raise RateLimited(f"Limite de requêtes Hypixel atteinte.{hint}")
        if not response.ok or not payload.get("success", False):
            raise HypixelError(f"Erreur de l'API Hypixel : {cause or f'HTTP {response.status_code}'}.")
        return payload

    def raw_player(self, uuid: str) -> dict[str, Any] | None:
        cached = self.player_cache.get(uuid)
        if cached is not None:
            return cached or None
        player = self._get("player", uuid=uuid).get("player")
        self.player_cache.set(uuid, player or {})
        return player

    def profile(self, name_or_uuid: str) -> PlayerProfile:
        uuid, name = self.resolve(name_or_uuid)
        player = self.raw_player(uuid)
        if not player:
            raise PlayerNotFound(f"{name} ne s'est jamais connecté à Hypixel.")
        return parse_player(player, fallback_name=name)

    def profiles(self, names: Iterable[str], max_workers: int = 4
                 ) -> tuple[list[PlayerProfile], dict[str, str]]:
        """Fetch several players in parallel. Returns (profiles in input order, errors by name)."""
        names = list(names)
        profiles: list[PlayerProfile] = []
        errors: dict[str, str] = {}
        if not names:
            return profiles, errors

        def fetch(name: str) -> PlayerProfile | HypixelError:
            try:
                return self.profile(name)
            except HypixelError as exc:
                return exc

        with ThreadPoolExecutor(max_workers=min(max_workers, len(names))) as pool:
            for name, result in zip(names, pool.map(fetch, names)):
                if isinstance(result, InvalidApiKey):
                    raise result  # same for every player: report once
                if isinstance(result, HypixelError):
                    errors[name] = str(result)
                elif all(p.uuid != result.uuid for p in profiles):
                    profiles.append(result)
        return profiles, errors
