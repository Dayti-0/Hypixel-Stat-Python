"""Hypixel progression formulas: network level, Bed Wars stars, SkyWars level and ranks."""

from __future__ import annotations

import math
import re
from typing import Any

_COLOR_CODE = re.compile(r"§[0-9a-fk-or]", re.IGNORECASE)

# Minecraft chat colors, used for ranks and "+" colors.
MC_COLORS = {
    "BLACK": "#000000", "DARK_BLUE": "#0000AA", "DARK_GREEN": "#00AA00",
    "DARK_AQUA": "#00AAAA", "DARK_RED": "#AA0000", "DARK_PURPLE": "#AA00AA",
    "GOLD": "#FFAA00", "GRAY": "#AAAAAA", "DARK_GRAY": "#555555", "BLUE": "#5555FF",
    "GREEN": "#55FF55", "AQUA": "#55FFFF", "RED": "#FF5555", "LIGHT_PURPLE": "#FF55FF",
    "YELLOW": "#FFFF55", "WHITE": "#FFFFFF",
}


def strip_color_codes(text: str) -> str:
    return _COLOR_CODE.sub("", text or "")


# --------------------------------------------------------------------------- Network

def network_level(experience: float | int | None) -> float:
    """Exact (fractional) network level from `networkExp`."""
    exp = max(float(experience or 0), 0.0)
    return math.sqrt(2 * exp + 30625) / 50 - 2.5


# --------------------------------------------------------------------------- Bed Wars

_BW_EASY_LEVELS = (500, 1000, 2000, 3500)
_BW_LEVEL_COST = 5000
_BW_PRESTIGE_COST = sum(_BW_EASY_LEVELS) + (100 - len(_BW_EASY_LEVELS)) * _BW_LEVEL_COST  # 487 000


def bedwars_star(experience: int | None) -> int:
    """Bed Wars star from the `Experience` field of the Bedwars stats."""
    prestiges, remaining = divmod(max(int(experience or 0), 0), _BW_PRESTIGE_COST)
    level = prestiges * 100
    for cost in _BW_EASY_LEVELS:
        if remaining < cost:
            return level
        remaining -= cost
        level += 1
    return level + remaining // _BW_LEVEL_COST


# --------------------------------------------------------------------------- SkyWars

_SW_LEVEL_XP = (0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000)


def skywars_level_from_xp(experience: int | None) -> int:
    exp = max(int(experience or 0), 0)
    if exp >= _SW_LEVEL_XP[-1]:
        return (exp - _SW_LEVEL_XP[-1]) // 10000 + len(_SW_LEVEL_XP)
    return sum(1 for threshold in _SW_LEVEL_XP if exp >= threshold)


def skywars_level(stats: dict[str, Any]) -> str | None:
    """Displayable SkyWars level, e.g. "15⋆"."""
    formatted = strip_color_codes(str(stats.get("levelFormatted") or "")).strip()
    if formatted:
        formatted = formatted.strip("[]")
        return f"{formatted}⋆" if formatted.isdigit() else formatted
    if "skywars_experience" in stats:
        return f"{skywars_level_from_xp(stats['skywars_experience'])}⋆"
    return None


# --------------------------------------------------------------------------- Ranks

_STAFF_RANKS = {
    "ADMIN": ("ADMIN", "RED"),
    "OWNER": ("OWNER", "RED"),
    "GAME_MASTER": ("GM", "DARK_GREEN"),
    "MODERATOR": ("MOD", "DARK_GREEN"),
    "HELPER": ("HELPER", "BLUE"),
    "YOUTUBER": ("YOUTUBE", "RED"),
}
_PACKAGE_RANKS = {
    "VIP": ("VIP", "GREEN"),
    "VIP_PLUS": ("VIP+", "GREEN"),
    "MVP": ("MVP", "AQUA"),
    "MVP_PLUS": ("MVP+", "AQUA"),
}


def player_rank(player: dict[str, Any]) -> tuple[str | None, str]:
    """Return (rank label or None, hex color) for a raw player object."""
    prefix = player.get("prefix")
    if prefix:
        label = strip_color_codes(prefix).strip().strip("[]")
        return label or None, MC_COLORS["RED"]

    staff = player.get("rank")
    if staff in _STAFF_RANKS:
        label, color = _STAFF_RANKS[staff]
        return label, MC_COLORS[color]

    if player.get("monthlyPackageRank") == "SUPERSTAR":
        color = player.get("monthlyRankColor") or "GOLD"
        return "MVP++", MC_COLORS.get(color, MC_COLORS["GOLD"])

    package = player.get("newPackageRank") or player.get("packageRank")
    if package in _PACKAGE_RANKS:
        label, color = _PACKAGE_RANKS[package]
        return label, MC_COLORS[color]

    return None, MC_COLORS["GRAY"]
