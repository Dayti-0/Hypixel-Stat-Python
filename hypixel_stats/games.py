"""Declarative registry of supported games, their modes and how to read them from the API.

Adding a mode is a single entry in one of the builders below: each mode maps a metric
name to the raw Hypixel keys it is read from. Counts are summed across keys (useful to
merge sub-modes, e.g. UHC 1v1 + 2v2 + 4v4), winstreaks take the maximum.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class Metric:
    id: str
    label: str
    higher_is_better: bool | None = True  # None: not ranked (e.g. deaths)
    is_streak: bool = False


@dataclass(frozen=True)
class Ratio:
    id: str
    label: str
    numerator: str
    denominator: str
    percent: bool = False


METRICS: dict[str, Metric] = {
    m.id: m
    for m in (
        Metric("wins", "Victoires"),
        Metric("losses", "Défaites", None),
        Metric("games_played", "Parties"),
        Metric("kills", "Éliminations"),
        Metric("deaths", "Morts", None),
        Metric("final_kills", "Final kills"),
        Metric("final_deaths", "Final deaths", None),
        Metric("beds_broken", "Lits détruits"),
        Metric("beds_lost", "Lits perdus", None),
        Metric("goals", "Buts"),
        Metric("winstreak", "Winstreak actuel", is_streak=True),
        Metric("best_winstreak", "Meilleur winstreak", is_streak=True),
    )
}

RATIOS: dict[str, Ratio] = {
    r.id: r
    for r in (
        Ratio("win_rate", "Taux de victoire", "wins", "games_played", percent=True),
        Ratio("wlr", "W/L", "wins", "losses"),
        Ratio("kdr", "K/D", "kills", "deaths"),
        Ratio("fkdr", "FK/D", "final_kills", "final_deaths"),
        Ratio("bblr", "BB/L", "beds_broken", "beds_lost"),
    )
}


@dataclass(frozen=True)
class Mode:
    id: str
    name: str
    keys: Mapping[str, tuple[str, ...]]


@dataclass(frozen=True)
class Game:
    id: str
    name: str
    api_section: str  # key under player["stats"]
    color: str
    metrics: tuple[str, ...]
    ratios: tuple[str, ...]
    modes: tuple[Mode, ...] = field(default_factory=tuple)

    def mode(self, mode_id: str | None) -> Mode:
        for mode in self.modes:
            if mode.id == mode_id:
                return mode
        return self.modes[0]


# --------------------------------------------------------------------------- Bed Wars

def _bedwars_mode(mode_id: str, name: str, prefix: str) -> Mode:
    keys = {
        metric: (f"{prefix}{metric}_bedwars",)
        for metric in (
            "wins", "losses", "games_played", "kills", "deaths",
            "final_kills", "final_deaths", "beds_broken", "beds_lost",
        )
    }
    keys["winstreak"] = (f"{prefix}winstreak",)
    return Mode(f"bedwars.{mode_id}", name, keys)


BEDWARS = Game(
    id="bedwars",
    name="Bed Wars",
    api_section="Bedwars",
    color="#ef4444",
    metrics=("wins", "losses", "final_kills", "final_deaths", "beds_broken",
             "beds_lost", "kills", "deaths", "games_played", "winstreak"),
    ratios=("fkdr", "wlr", "bblr", "kdr", "win_rate"),
    modes=(
        _bedwars_mode("overall", "Global", ""),
        _bedwars_mode("solo", "Solo", "eight_one_"),
        _bedwars_mode("doubles", "Doubles", "eight_two_"),
        _bedwars_mode("threes", "3v3v3v3", "four_three_"),
        _bedwars_mode("fours", "4v4v4v4", "four_four_"),
        _bedwars_mode("4v4", "4v4", "two_four_"),
    ),
)


# --------------------------------------------------------------------------- SkyWars

def _skywars_mode(mode_id: str, name: str, *suffixes: str) -> Mode:
    keys = {
        metric: tuple(f"{metric}{suffix}" for suffix in suffixes)
        for metric in ("wins", "losses", "kills", "deaths")
    }
    if suffixes == ("",):
        keys["games_played"] = ("games_played_skywars",)
        keys["winstreak"] = ("win_streak", "winstreak")
    return Mode(f"skywars.{mode_id}", name, keys)


SKYWARS = Game(
    id="skywars",
    name="SkyWars",
    api_section="SkyWars",
    color="#06b6d4",
    metrics=("wins", "losses", "kills", "deaths", "games_played", "winstreak"),
    ratios=("kdr", "wlr", "win_rate"),
    modes=(
        _skywars_mode("overall", "Global", ""),
        _skywars_mode("solo", "Solo", "_solo"),
        _skywars_mode("team", "Équipe", "_team"),
        _skywars_mode("mini", "Mini", "_mini"),
        _skywars_mode("mega", "Mega", "_mega", "_mega_doubles"),
        _skywars_mode("lab", "Laboratoire", "_lab"),
        _skywars_mode("ranked", "Ranked", "_ranked"),
        _skywars_mode("solo_insane", "Solo Insane", "_solo_insane"),
        _skywars_mode("team_insane", "Équipe Insane", "_team_insane"),
    ),
)


# --------------------------------------------------------------------------- Duels

def _duels_mode(mode_id: str, name: str, submodes: tuple[str, ...],
                category: str | None = None, bridge: bool = False) -> Mode:
    kills_key, deaths_key = ("bridge_kills", "bridge_deaths") if bridge else ("kills", "deaths")
    keys: dict[str, tuple[str, ...]] = {
        "wins": tuple(f"{m}_wins" for m in submodes),
        "losses": tuple(f"{m}_losses" for m in submodes),
        "games_played": tuple(f"{m}_rounds_played" for m in submodes),
        "kills": tuple(f"{m}_{kills_key}" for m in submodes),
        "deaths": tuple(f"{m}_{deaths_key}" for m in submodes),
        "winstreak": tuple(f"current_winstreak_mode_{m}" for m in submodes),
        "best_winstreak": tuple(f"best_winstreak_mode_{m}" for m in submodes),
    }
    if bridge:
        keys["goals"] = tuple(f"{m}_goals" for m in submodes)
    if category:
        keys["winstreak"] += (f"current_{category}_winstreak",)
        keys["best_winstreak"] += (f"best_{category}_winstreak",)
    return Mode(f"duels.{mode_id}", name, keys)


DUELS = Game(
    id="duels",
    name="Duels",
    api_section="Duels",
    color="#f59e0b",
    metrics=("wins", "losses", "kills", "deaths", "games_played", "goals",
             "winstreak", "best_winstreak"),
    ratios=("wlr", "kdr", "win_rate"),
    modes=(
        Mode("duels.overall", "Global", {
            "wins": ("wins",),
            "losses": ("losses",),
            "games_played": ("games_played_duels",),
            "kills": ("kills",),
            "deaths": ("deaths",),
            "winstreak": ("current_winstreak",),
            "best_winstreak": ("best_overall_winstreak",),
        }),
        _duels_mode("classic", "Classic", ("classic_duel",), "classic"),
        _duels_mode("uhc", "UHC", ("uhc_duel", "uhc_doubles", "uhc_four", "uhc_meetup"), "uhc"),
        _duels_mode("skywars", "SkyWars", ("sw_duel", "sw_doubles"), "skywars"),
        _duels_mode("bridge", "Bridge", (
            "bridge_duel", "bridge_doubles", "bridge_threes", "bridge_four",
            "bridge_2v2v2v2", "bridge_3v3v3v3", "capture_threes",
        ), "bridge", bridge=True),
        _duels_mode("sumo", "Sumo", ("sumo_duel",), "sumo"),
        _duels_mode("op", "OP", ("op_duel", "op_doubles"), "op"),
        _duels_mode("combo", "Combo", ("combo_duel",), "combo"),
        _duels_mode("bow", "Bow", ("bow_duel",), "bow"),
        _duels_mode("bowspleef", "Bow Spleef", ("bowspleef_duel",), "tnt_games"),
        _duels_mode("boxing", "Boxing", ("boxing_duel",), "boxing"),
        _duels_mode("nodebuff", "NoDebuff", ("potion_duel",), "no_debuff"),
        _duels_mode("megawalls", "Mega Walls", ("mw_duel", "mw_doubles"), "mega_walls"),
        _duels_mode("blitz", "Blitz", ("blitz_duel",), "blitz"),
        _duels_mode("bedwars", "Bed Wars", ("bedwars_two_one_duels", "bedwars_two_one_duels_rush")),
        _duels_mode("parkour", "Parkour", ("parkour_eight",), "parkour"),
    ),
)


GAMES: dict[str, Game] = {g.id: g for g in (BEDWARS, SKYWARS, DUELS)}
OVERVIEW_ID = "overview"


def all_modes() -> list[tuple[Game, Mode]]:
    return [(game, mode) for game in GAMES.values() for mode in game.modes]


def mode_metrics(game: Game, mode: Mode) -> list[str]:
    """Metrics of `game` that `mode` actually provides (games played can always be derived)."""
    return [m for m in game.metrics if m in mode.keys or m == "games_played"]


def mode_ratios(game: Game, mode: Mode) -> list[str]:
    available = set(mode_metrics(game, mode))
    return [r for r in game.ratios
            if RATIOS[r].numerator in available and RATIOS[r].denominator in available]
