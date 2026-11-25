"""French-style number and date formatting."""

from __future__ import annotations

from datetime import datetime, timezone

NARROW_NBSP = " "


def fmt_int(value: float | int) -> str:
    return f"{round(value):,}".replace(",", NARROW_NBSP)


def fmt_ratio(value: float) -> str:
    return f"{value:,.2f}".replace(",", NARROW_NBSP).replace(".", ",")


def fmt_percent(value: float) -> str:
    return f"{value:.1f}".replace(".", ",") + NARROW_NBSP + "%"


def fmt_date(epoch_ms: int | None) -> str:
    if not epoch_ms:
        return "—"
    return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc).astimezone().strftime("%d/%m/%Y")


def fmt_relative(epoch_ms: int | None, now: datetime | None = None) -> str:
    if not epoch_ms:
        return "masqué"
    now = now or datetime.now(timezone.utc)
    seconds = max((now - datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc)).total_seconds(), 0)
    for unit_seconds, singular, plural in (
        (365 * 86400, "an", "ans"),
        (30 * 86400, "mois", "mois"),
        (86400, "jour", "jours"),
        (3600, "heure", "heures"),
        (60, "minute", "minutes"),
    ):
        if seconds >= unit_seconds:
            count = int(seconds // unit_seconds)
            return f"il y a {count} {singular if count == 1 else plural}"
    return "à l'instant"
