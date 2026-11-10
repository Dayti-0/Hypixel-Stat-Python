import pytest
import requests

from hypixel_stats.api import (HypixelClient, HypixelError, InvalidApiKey, PlayerNotFound,
                               RateLimited, TTLCache, parse_player_names)

UUID = "f7c77d999f154a66a87dc4a51ef30d19"


class FakeResponse:
    def __init__(self, status=200, payload=None, headers=None):
        self.status_code = status
        self.ok = 200 <= status < 400
        self.headers = headers or {}
        self._payload = payload

    def json(self):
        if self._payload is None:
            raise ValueError("no body")
        return self._payload


response = FakeResponse


class FakeSession:
    """Routes GET requests to canned responses by URL substring."""

    def __init__(self, routes):
        self.routes = routes
        self.headers = {}
        self.calls = []

    def get(self, url, params=None, headers=None, timeout=None):
        self.calls.append((url, params, headers))
        for fragment, result in self.routes.items():
            if fragment in url:
                if isinstance(result, Exception):
                    raise result
                return result(url, params) if callable(result) else result
        raise AssertionError(f"unexpected URL {url}")


def mojang(name="Hypixel"):
    return response(200, {"id": UUID, "name": name})


def hypixel_player(player):
    return response(200, {"success": True, "player": player})


def test_parse_player_names():
    assert parse_player_names(" Foo, bar  baz;foo\nQux ") == ["Foo", "bar", "baz", "Qux"]
    assert parse_player_names(None) == []


def test_ttl_cache_expires():
    now = [0.0]
    cache = TTLCache(10, clock=lambda: now[0])
    cache.set("a", 1)
    assert cache.get("a") == 1
    now[0] = 11
    assert cache.get("a") is None


def test_profile_happy_path_and_cache(raw_player):
    session = FakeSession({"mojang.com": mojang(), "hypixel.net": hypixel_player(raw_player)})
    client = HypixelClient("key", session=session)
    assert client.profile("Hypixel").name == "hypixel"
    client.profile("hypixel")  # cached: no new requests
    assert len(session.calls) == 2
    url, params, headers = session.calls[1]
    assert url.endswith("/v2/player") and params == {"uuid": UUID} and headers == {"API-Key": "key"}


def test_uuid_input_skips_mojang(raw_player):
    session = FakeSession({"hypixel.net": hypixel_player(raw_player)})
    HypixelClient("key", session=session).profile("f7c77d99-9f15-4a66-a87d-c4a51ef30d19")
    assert len(session.calls) == 1


def test_mojang_fallback_endpoint(raw_player):
    session = FakeSession({
        "api.mojang.com": requests.ConnectionError("down"),
        "minecraftservices.com": mojang(),
        "hypixel.net": hypixel_player(raw_player),
    })
    assert HypixelClient("key", session=session).profile("Hypixel").uuid == UUID


@pytest.mark.parametrize("name", ["bad name!", "x" * 17, ""])
def test_invalid_username(name):
    with pytest.raises(PlayerNotFound):
        HypixelClient("key", session=FakeSession({})).resolve(name or " ")


def test_unknown_minecraft_account():
    session = FakeSession({"mojang.com": response(404)})
    with pytest.raises(PlayerNotFound, match="n'existe pas"):
        HypixelClient("key", session=session).profile("Nobody")


def test_never_joined_hypixel():
    session = FakeSession({"mojang.com": mojang(), "hypixel.net": hypixel_player(None)})
    with pytest.raises(PlayerNotFound, match="jamais connecté"):
        HypixelClient("key", session=session).profile("Hypixel")


@pytest.mark.parametrize("status, payload, error", [
    (403, {"success": False, "cause": "Invalid API key"}, InvalidApiKey),
    (429, {"success": False, "cause": "Key throttle"}, RateLimited),
    (500, None, HypixelError),
    (200, {"success": False, "cause": "Malformed UUID"}, HypixelError),
])
def test_hypixel_errors(status, payload, error):
    session = FakeSession({"mojang.com": mojang(), "hypixel.net": response(status, payload)})
    with pytest.raises(error):
        HypixelClient("key", session=session).profile("Hypixel")


def test_missing_api_key():
    with pytest.raises(InvalidApiKey):
        HypixelClient("", session=FakeSession({"mojang.com": mojang()})).profile("Hypixel")


def test_profiles_collects_errors_and_dedupes(raw_player):
    def lookup(url, _params):
        name = url.rsplit("/", 1)[-1]
        return response(404) if name == "Ghost" else mojang(name)

    session = FakeSession({"mojang.com": lookup, "hypixel.net": hypixel_player(raw_player)})
    profiles, errors = HypixelClient("key", session=session).profiles(["Hypixel", "Ghost", "HYPIXEL2"])
    assert len(profiles) == 1  # both names resolve to the same UUID
    assert list(errors) == ["Ghost"]


def test_profiles_invalid_key_is_raised_once():
    session = FakeSession({"mojang.com": mojang(), "hypixel.net": response(403, {"success": False})})
    with pytest.raises(InvalidApiKey):
        HypixelClient("key", session=session).profiles(["A", "B"])
