"""Plain data models. Everything here round-trips through JSON (needed for dcc.Store)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from hypixel_stats.games import RATIOS


@dataclass(frozen=True)
class ModeStats:
    """Metrics of one player in one mode. Missing metrics read as 0."""

    values: dict[str, int] = field(default_factory=dict)

    def has(self, metric: str) -> bool:
        return metric in self.values

    def get(self, metric: str) -> int:
        if metric == "games_played" and not self.values.get("games_played"):
            return self.values.get("wins", 0) + self.values.get("losses", 0)
        return self.values.get(metric, 0)

    def ratio(self, ratio_id: str) -> float:
        ratio = RATIOS[ratio_id]
        num, den = self.get(ratio.numerator), self.get(ratio.denominator)
        if ratio.percent:
            return 100 * num / den if den else 0.0
        # Community convention: with no deaths/losses the ratio equals the numerator.
        return num / den if den else float(num)

    @property
    def is_empty(self) -> bool:
        return not any(self.values.values())


@dataclass
class PlayerProfile:
    uuid: str
    name: str
    rank: str | None = None
    rank_color: str = "#AAAAAA"
    network_level: float = 1.0
    karma: int = 0
    achievement_points: int = 0
    first_login: int | None = None  # epoch milliseconds
    last_login: int | None = None
    levels: dict[str, str] = field(default_factory=dict)  # game id -> "412✫"
    stats: dict[str, dict[str, int]] = field(default_factory=dict)  # mode id -> metrics

    def mode(self, mode_id: str) -> ModeStats:
        return ModeStats(self.stats.get(mode_id, {}))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PlayerProfile":
        return cls(**data)


def active_metrics(stats: list[ModeStats], metrics: list[str]) -> list[str]:
    """Keep metrics that at least one player has a non-zero value for."""
    return [m for m in metrics if any(s.get(m) for s in stats)]


def active_ratios(stats: list[ModeStats], ratios: list[str]) -> list[str]:
    """Keep ratios whose numerator or denominator is non-zero for at least one player."""
    return [r for r in ratios
            if any(s.get(RATIOS[r].numerator) or s.get(RATIOS[r].denominator) for s in stats)]
