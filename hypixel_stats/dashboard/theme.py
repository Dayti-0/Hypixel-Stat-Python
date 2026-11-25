"""Visual constants shared by the Python side (charts, inline colors)."""

# One color per compared player, in order. Chosen to stay distinct on a dark background.
PLAYER_COLORS = (
    "#818cf8",  # indigo
    "#34d399",  # emerald
    "#fbbf24",  # amber
    "#f472b6",  # pink
    "#38bdf8",  # sky
    "#fb923c",  # orange
    "#a78bfa",  # violet
    "#a3e635",  # lime
)

TEXT = "#e5e7eb"
TEXT_MUTED = "#9ca3af"
GRID = "rgba(255, 255, 255, 0.07)"
SURFACE = "#151a2b"
FONT_FAMILY = "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"


def player_color(index: int) -> str:
    return PLAYER_COLORS[index % len(PLAYER_COLORS)]
