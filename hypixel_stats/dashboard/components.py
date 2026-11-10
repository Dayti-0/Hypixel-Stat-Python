"""Dash component builders (pure functions: data in, component tree out)."""

from __future__ import annotations

from dash import dcc, html

from hypixel_stats.games import (GAMES, METRICS, OVERVIEW_ID, RATIOS, Game, Mode,
                                 mode_metrics, mode_ratios)
from hypixel_stats.models import ModeStats, PlayerProfile, active_metrics, active_ratios

from . import charts, theme
from .formatting import fmt_date, fmt_int, fmt_percent, fmt_ratio, fmt_relative

GRAPH_CONFIG = {"displayModeBar": False, "responsive": True}


def avatar_url(profile: PlayerProfile, size: int = 64) -> str:
    return f"https://mc-heads.net/avatar/{profile.uuid or profile.name}/{size}"


# --------------------------------------------------------------------------- Feedback

def notice(message: str, kind: str = "error") -> html.Div:
    return html.Div(message, className=f"notice notice-{kind}", role="status")


def feedback(loaded: int, errors: dict[str, str]) -> list[html.Div]:
    items = [notice(f"{name} — {error}", "error") for name, error in errors.items()]
    if loaded:
        items.insert(0, notice(f"{loaded} joueur{'s' if loaded > 1 else ''} chargé{'s' if loaded > 1 else ''}.",
                               "success"))
    return items


# --------------------------------------------------------------------------- Empty state

def empty_state(has_env_key: bool) -> html.Div:
    steps = ["Entrez un ou plusieurs pseudos Minecraft.", "Cliquez sur « Comparer » ou appuyez sur Entrée."]
    if not has_env_key:
        steps.insert(0, "Collez votre clé API Hypixel (developer.hypixel.net).")
    return html.Div(
        [
            html.Div("⚔", className="empty-glyph", **{"aria-hidden": "true"}),
            html.H2("Comparez des joueurs Hypixel", className="empty-title"),
            html.P("Bed Wars, SkyWars et Duels : volumes, ratios et winstreaks, mode par mode.",
                   className="empty-text"),
            html.Ol([html.Li(step) for step in steps], className="empty-steps"),
        ],
        className="empty-state",
    )


# --------------------------------------------------------------------------- Profiles

def _fact(label: str, value: str) -> html.Div:
    return html.Div([html.Dt(label), html.Dd(value)], className="fact")


def profile_card(profile: PlayerProfile, index: int) -> html.Article:
    color = theme.player_color(index)
    level = profile.network_level
    progress = (level - int(level)) * 100
    badges = [
        html.Span([html.Span(GAMES[game_id].name, className="badge-game"), value],
                  className="level-badge", style={"--badge-color": GAMES[game_id].color})
        for game_id, value in profile.levels.items() if game_id in GAMES
    ]
    return html.Article(
        [
            html.Div(
                [
                    html.Img(src=avatar_url(profile), alt="", className="profile-avatar"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(f"[{profile.rank}]", className="profile-rank",
                                              style={"color": profile.rank_color}) if profile.rank else None,
                                    html.H3(profile.name, className="profile-name",
                                            style={"color": profile.rank_color if profile.rank else theme.TEXT}),
                                ],
                                className="profile-title",
                            ),
                            html.Div(badges, className="profile-badges"),
                        ],
                        className="profile-heading",
                    ),
                ],
                className="profile-top",
            ),
            html.Div(
                [
                    html.Div([html.Span("Niveau réseau"), html.Strong(f"{int(level)}")],
                             className="level-row"),
                    html.Div(html.Div(className="level-fill", style={"width": f"{progress:.0f}%"}),
                             className="level-track", title=f"{progress:.0f} % vers le niveau {int(level) + 1}"),
                ],
                className="profile-level",
            ),
            html.Dl(
                [
                    _fact("Karma", fmt_int(profile.karma)),
                    _fact("Succès", fmt_int(profile.achievement_points)),
                    _fact("Première connexion", fmt_date(profile.first_login)),
                    _fact("Dernière connexion", fmt_relative(profile.last_login)),
                ],
                className="profile-facts",
            ),
        ],
        className="profile-card",
        style={"--player-color": color},
    )


def profile_grid(players: list[PlayerProfile]) -> html.Div:
    return html.Div([profile_card(p, i) for i, p in enumerate(players)], className="profile-grid")


# --------------------------------------------------------------------------- Navigation

def game_tabs() -> html.Nav:
    tabs = [(OVERVIEW_ID, "Vue d'ensemble", "#818cf8")] + [(g.id, g.name, g.color) for g in GAMES.values()]
    return html.Nav(
        [
            html.Button(name, id={"type": "game-tab", "index": game_id}, n_clicks=0,
                        className="game-tab", style={"--tab-color": color})
            for game_id, name, color in tabs
        ],
        className="game-tabs",
        **{"aria-label": "Jeux"},
    )


def mode_pills(game: Game | None, active_mode_id: str | None) -> list[html.Button]:
    if game is None:
        return []
    active = game.mode(active_mode_id).id
    return [
        html.Button(mode.name, id={"type": "mode-pill", "index": mode.id}, n_clicks=0,
                    className="mode-pill is-active" if mode.id == active else "mode-pill")
        for mode in game.modes
    ]


# --------------------------------------------------------------------------- Comparison table

def _best_index(values: list[float], higher_is_better: bool | None) -> int | None:
    if higher_is_better is None or len(values) < 2 or len(set(values)) == 1:
        return None
    target = max(values) if higher_is_better else min(values)
    return values.index(target)


def _row(label: str, cells: list[str], values: list[float], higher_is_better: bool | None,
         kind: str = "") -> html.Tr:
    best = _best_index(values, higher_is_better)
    return html.Tr(
        [html.Th(label, scope="row")]
        + [html.Td(cell, className="is-best" if i == best else None) for i, cell in enumerate(cells)],
        className=kind or None,
    )


def _table_head(players: list[PlayerProfile]) -> html.Thead:
    return html.Thead(html.Tr(
        [html.Th("")]
        + [
            html.Th(
                html.Span(
                    [html.Img(src=avatar_url(p, 24), alt="", className="th-avatar"), p.name],
                    className="th-player",
                ),
                scope="col", style={"--player-color": theme.player_color(i)},
            )
            for i, p in enumerate(players)
        ]
    ))


def _ratio_cell(stats: ModeStats, ratio_id: str) -> tuple[str, float]:
    # Rounded like the display, so visually equal values are never ranked.
    if RATIOS[ratio_id].percent:
        value = round(stats.ratio(ratio_id), 1)
        return fmt_percent(value), value
    value = round(stats.ratio(ratio_id), 2)
    return fmt_ratio(value), value


def comparison_table(players: list[PlayerProfile], game: Game, mode: Mode) -> html.Div:
    stats = [p.mode(mode.id) for p in players]
    rows = []
    for ratio_id in active_ratios(stats, mode_ratios(game, mode)):
        cells, values = zip(*(_ratio_cell(s, ratio_id) for s in stats))
        rows.append(_row(RATIOS[ratio_id].label, list(cells), list(values), True, "row-ratio"))
    for metric_id in active_metrics(stats, mode_metrics(game, mode)):
        metric = METRICS[metric_id]
        values = [s.get(metric_id) for s in stats]
        cells = [fmt_int(v) if (s.has(metric_id) or not metric.is_streak) else "—"
                 for s, v in zip(stats, values)]
        rows.append(_row(metric.label, cells, values, metric.higher_is_better))
    return html.Div(
        html.Table([_table_head(players), html.Tbody(rows)], className="stats-table"),
        className="table-scroll",
    )


def overview_table(players: list[PlayerProfile]) -> html.Div:
    rows = []
    for game in GAMES.values():
        overall = [p.mode(f"{game.id}.overall") for p in players]
        rows.append(html.Tr(html.Th(game.name, colSpan=len(players) + 1),
                            className="row-section", style={"--section-color": game.color}))
        if any(game.id in p.levels for p in players):
            rows.append(_row("Niveau", [p.levels.get(game.id, "—") for p in players], [], None))
        main_ratio = game.ratios[0]
        cells, values = zip(*(_ratio_cell(s, main_ratio) for s in overall))
        rows.append(_row(RATIOS[main_ratio].label, list(cells), list(values), True, "row-ratio"))
        for metric_id in ("wins", "games_played"):
            values = [s.get(metric_id) for s in overall]
            rows.append(_row(METRICS[metric_id].label, [fmt_int(v) for v in values], values, True))
    return html.Div(
        html.Table([_table_head(players), html.Tbody(rows)], className="stats-table"),
        className="table-scroll",
    )


# --------------------------------------------------------------------------- Panels

def _panel(title: str, body, extra_class: str = "") -> html.Section:
    return html.Section([html.H2(title, className="panel-title"), body],
                        className=f"panel {extra_class}".strip())


def _graph(figure, height: int) -> dcc.Graph:
    return dcc.Graph(figure=figure, config=GRAPH_CONFIG, style={"height": f"{height}px"})


def mode_view(players: list[PlayerProfile], game: Game, mode: Mode) -> html.Div:
    if all(p.mode(mode.id).is_empty for p in players):
        return html.Div(notice(f"Aucun joueur n'a de statistiques en {game.name} · {mode.name}.", "info"),
                        className="view")
    return html.Div(
        [
            _panel("Comparaison", comparison_table(players, game, mode), "panel-table"),
            html.Div(
                [
                    html.Section(_graph(charts.ratios_figure(players, game, mode), 340), className="panel"),
                    html.Section(_graph(charts.counts_figure(players, game, mode), 340), className="panel"),
                ],
                className="chart-grid",
            ),
        ],
        className="view",
    )


def overview_view(players: list[PlayerProfile]) -> html.Div:
    return html.Div(
        [
            _panel("Résumé par jeu", overview_table(players), "panel-table"),
            html.Section(_graph(charts.overview_figure(players), 360), className="panel"),
        ],
        className="view view-overview",
    )
