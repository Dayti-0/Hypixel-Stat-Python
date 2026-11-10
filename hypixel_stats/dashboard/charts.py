"""Plotly figures. Built on demand for the selected mode only."""

from __future__ import annotations

import plotly.graph_objects as go

from hypixel_stats.games import GAMES, METRICS, RATIOS, Game, Mode, mode_metrics, mode_ratios
from hypixel_stats.models import PlayerProfile, active_metrics, active_ratios

from . import theme


def _base_layout(fig: go.Figure, title: str, y_title: str | None = None) -> go.Figure:
    fig.update_layout(
        title={"text": title, "x": 0, "xanchor": "left", "font": {"size": 15, "color": theme.TEXT}},
        barmode="group",
        bargap=0.25,
        bargroupgap=0.08,
        separators=", ",  # French: decimal comma, space as thousands separator
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": theme.FONT_FAMILY, "color": theme.TEXT_MUTED, "size": 12},
        margin={"l": 8, "r": 8, "t": 44, "b": 8},
        legend={"orientation": "h", "y": -0.12, "yanchor": "top", "x": 0, "xanchor": "left",
                "bgcolor": "rgba(0,0,0,0)"},
        hoverlabel={"bgcolor": theme.SURFACE, "bordercolor": "rgba(255,255,255,0.15)",
                    "font": {"color": theme.TEXT, "family": theme.FONT_FAMILY}},
        xaxis={"showgrid": False, "linecolor": theme.GRID, "tickfont": {"color": theme.TEXT}},
        yaxis={"gridcolor": theme.GRID, "zeroline": False, "title": y_title, "automargin": True},
    )
    return fig


def _empty(title: str, message: str = "Aucune donnée pour ce mode") -> go.Figure:
    fig = _base_layout(go.Figure(), title)
    fig.update_layout(
        xaxis={"visible": False}, yaxis={"visible": False},
        annotations=[{"text": message, "showarrow": False, "xref": "paper", "yref": "paper",
                      "font": {"size": 14, "color": theme.TEXT_MUTED}}],
    )
    return fig


def _grouped_bars(title: str, categories: list[str], series: list[tuple[str, list[float]]],
                  value_format: str) -> go.Figure:
    if not any(any(values) for _, values in series):
        return _empty(title)
    fig = go.Figure()
    for index, (name, values) in enumerate(series):
        fig.add_bar(
            x=categories, y=values, name=name,
            marker={"color": theme.player_color(index), "cornerradius": 4},
            hovertemplate=f"<b>{name}</b><br>%{{x}} : %{{y:{value_format}}}<extra></extra>",
        )
    return _base_layout(fig, title)


def counts_figure(players: list[PlayerProfile], game: Game, mode: Mode) -> go.Figure:
    stats = [p.mode(mode.id) for p in players]
    metrics = active_metrics(stats, [m for m in mode_metrics(game, mode) if not METRICS[m].is_streak])
    series = [(p.name, [p.mode(mode.id).get(m) for m in metrics]) for p in players]
    return _grouped_bars(f"{game.name} · {mode.name} — volumes",
                         [METRICS[m].label for m in metrics], series, ",d")


def ratios_figure(players: list[PlayerProfile], game: Game, mode: Mode) -> go.Figure:
    stats = [p.mode(mode.id) for p in players]
    ratios = active_ratios(stats, [r for r in mode_ratios(game, mode) if not RATIOS[r].percent])
    series = [(p.name, [round(p.mode(mode.id).ratio(r), 2) for r in ratios]) for p in players]
    return _grouped_bars(f"{game.name} · {mode.name} — ratios",
                         [RATIOS[r].label for r in ratios], series, ".2f")


def overview_figure(players: list[PlayerProfile]) -> go.Figure:
    games = list(GAMES.values())
    series = [(p.name, [p.mode(f"{g.id}.overall").get("wins") for g in games]) for p in players]
    return _grouped_bars("Victoires par jeu", [g.name for g in games], series, ",d")
