"""Static page skeleton. Dynamic parts are filled by callbacks."""

from __future__ import annotations

from dash import dcc, html

from hypixel_stats.games import OVERVIEW_ID

from . import components


def build_layout(has_env_key: bool) -> html.Div:
    key_hint = ("Clé chargée depuis le fichier .env — laissez vide pour l'utiliser."
                if has_env_key else "Stockée uniquement dans ce navigateur.")
    return html.Div(
        [
            dcc.Store(id="players-store", storage_type="session"),
            dcc.Store(id="view-store", data={"game": OVERVIEW_ID, "mode": None}, storage_type="session"),

            html.Header(
                [
                    html.Div(
                        [
                            html.Div("H", className="brand-mark", **{"aria-hidden": "true"}),
                            html.Div([html.Span("Hypixel Stats", className="brand-name"),
                                      html.Span("Comparateur de joueurs", className="brand-sub")]),
                        ],
                        className="brand",
                    ),
                    html.A("Obtenir une clé API ↗", href="https://developer.hypixel.net/dashboard",
                           target="_blank", rel="noopener noreferrer", className="topbar-link"),
                ],
                className="topbar",
            ),

            html.Main(
                [
                    html.Section(
                        [
                            html.Div(
                                [
                                    html.Label("Joueurs", htmlFor="usernames-input", className="field-label"),
                                    dcc.Input(id="usernames-input", type="text", debounce=False,
                                              placeholder="Pseudos séparés par des virgules ou des espaces",
                                              autoComplete="off", className="field-input",
                                              persistence=True, persistence_type="local"),
                                ],
                                className="field field-players",
                            ),
                            html.Div(
                                [
                                    html.Label("Clé API Hypixel", htmlFor="api-key-input", className="field-label"),
                                    dcc.Input(id="api-key-input", type="password", autoComplete="off",
                                              placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                                              className="field-input",
                                              persistence=True, persistence_type="local"),
                                    html.Span(key_hint, className="field-hint"),
                                ],
                                className="field field-key",
                            ),
                            html.Button("Comparer", id="fetch-button", n_clicks=0, className="primary-button"),
                        ],
                        className="search-card",
                    ),
                    html.Div(id="feedback", className="feedback", **{"aria-live": "polite"}),

                    dcc.Loading(
                        html.Div(
                            [
                                html.Div(components.empty_state(has_env_key), id="empty-state"),
                                html.Div(
                                    [
                                        html.Div(id="profiles"),
                                        components.game_tabs(),
                                        html.Div(id="mode-pills", className="mode-pills"),
                                        html.Div(id="view-content"),
                                    ],
                                    id="results",
                                    style={"display": "none"},
                                ),
                            ]
                        ),
                        type="dot",
                        color="#818cf8",
                        delay_show=150,
                    ),
                ],
                className="page",
            ),

            html.Footer(
                "Données : API publique Hypixel et Mojang. Projet non affilié à Hypixel Inc.",
                className="footer",
            ),
        ],
        className="app",
    )
