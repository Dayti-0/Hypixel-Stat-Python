"""Turn a raw Hypixel `player` object into a PlayerProfile."""

from __future__ import annotations

from typing import Any

from hypixel_stats import levels
from hypixel_stats.games import GAMES, METRICS
from hypixel_stats.models import PlayerProfile


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    return None


def extract_mode(section: dict[str, Any], keys: dict[str, tuple[str, ...]]) -> dict[str, int]:
    """Read each metric from its raw keys. Absent metrics are left out entirely."""
    result: dict[str, int] = {}
    for metric, raw_keys in keys.items():
        found = [v for v in (_as_int(section.get(k)) for k in raw_keys) if v is not None]
        if found:
            result[metric] = max(found) if METRICS[metric].is_streak else sum(found)
    return result


def parse_player(player: dict[str, Any], fallback_name: str = "") -> PlayerProfile:
    stats_root = player.get("stats") or {}
    rank, rank_color = levels.player_rank(player)

    stats: dict[str, dict[str, int]] = {}
    for game in GAMES.values():
        section = stats_root.get(game.api_section) or {}
        for mode in game.modes:
            stats[mode.id] = extract_mode(section, mode.keys)

    game_levels: dict[str, str] = {}
    bedwars = stats_root.get("Bedwars") or {}
    star = (player.get("achievements") or {}).get("bedwars_level")
    if star is None and "Experience" in bedwars:
        star = levels.bedwars_star(bedwars["Experience"])
    if star is not None:
        game_levels["bedwars"] = f"{int(star)}✫"

    skywars_level = levels.skywars_level(stats_root.get("SkyWars") or {})
    if skywars_level:
        game_levels["skywars"] = skywars_level

    return PlayerProfile(
        uuid=str(player.get("uuid") or ""),
        name=str(player.get("displayname") or fallback_name),
        rank=rank,
        rank_color=rank_color,
        network_level=levels.network_level(player.get("networkExp")),
        karma=_as_int(player.get("karma")) or 0,
        achievement_points=_as_int(player.get("achievementPoints")) or 0,
        first_login=_as_int(player.get("firstLogin")),
        last_login=_as_int(player.get("lastLogin")),
        levels=game_levels,
        stats=stats,
    )
