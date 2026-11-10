"""Application settings, read from environment variables (and an optional .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    try:
        return int(raw) if raw else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    api_key: str = ""
    host: str = "127.0.0.1"
    port: int = 8050
    cache_ttl: int = 120  # seconds a player's stats are kept before re-fetching
    request_timeout: int = 10
    max_players: int = 8

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            api_key=os.getenv("HYPIXEL_API_KEY", "").strip(),
            host=os.getenv("HOST", cls.host),
            port=_int_env("PORT", cls.port),
            cache_ttl=_int_env("CACHE_TTL", cls.cache_ttl),
            request_timeout=_int_env("REQUEST_TIMEOUT", cls.request_timeout),
            max_players=_int_env("MAX_PLAYERS", cls.max_players),
        )
