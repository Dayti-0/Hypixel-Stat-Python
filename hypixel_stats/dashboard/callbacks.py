"""Dash callbacks."""

from __future__ import annotations

from typing import Callable

import dash
from dash import ALL, Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate

from hypixel_stats.api import HypixelClient, HypixelError, parse_player_names
from hypixel_stats.games import GAMES, OVERVIEW_ID
from hypixel_stats.models import PlayerProfile
from hypixel_stats.settings import Settings

from . import components

ClientFactory = Callable[[str], HypixelClient]


def register_callbacks(app: dash.Dash, settings: Settings, client_factory: ClientFactory) -> None:

    @app.callback(
        Output("players-store", "data"),
        Output("feedback", "children"),
        Input("fetch-button", "n_clicks"),
        Input("usernames-input", "n_submit"),
        Input("api-key-input", "n_submit"),
        State("usernames-input", "value"),
        State("api-key-input", "value"),
        prevent_initial_call=True,
        running=[(Output("fetch-button", "disabled"), True, False)],
    )
    def load_players(_clicks, _submit_names, _submit_key, raw_names, api_key):
        names = parse_player_names(raw_names)
        if not names:
            return no_update, components.notice("Entrez au moins un pseudo.")
        if len(names) > settings.max_players:
            return no_update, components.notice(
                f"{settings.max_players} joueurs maximum à la fois ({len(names)} saisis).")

        key = (api_key or "").strip() or settings.api_key
        if not key:
            return no_update, components.notice("Entrez votre clé API Hypixel.")

        try:
            profiles, errors = client_factory(key).profiles(names)
        except HypixelError as exc:
            return no_update, components.notice(str(exc))

        if not profiles:
            return no_update, components.feedback(0, errors)
        return [p.to_dict() for p in profiles], components.feedback(len(profiles), errors)

    @app.callback(
        Output("view-store", "data"),
        Input({"type": "game-tab", "index": ALL}, "n_clicks"),
        Input({"type": "mode-pill", "index": ALL}, "n_clicks"),
        State("view-store", "data"),
        prevent_initial_call=True,
    )
    def select_view(_tabs, _pills, view):
        # Fires too when pills are re-rendered: only react to real clicks.
        if not ctx.triggered_id or not any(t["value"] for t in ctx.triggered):
            raise PreventUpdate
        view = dict(view or {})
        target = ctx.triggered_id
        if target["type"] == "game-tab":
            if target["index"] == view.get("game"):
                raise PreventUpdate
            view = {"game": target["index"], "mode": None}
        else:
            view["mode"] = target["index"]
        return view

    @app.callback(
        Output({"type": "game-tab", "index": ALL}, "className"),
        Output("mode-pills", "children"),
        Input("view-store", "data"),
        State({"type": "game-tab", "index": ALL}, "id"),
    )
    def render_navigation(view, tab_ids):
        game_id = (view or {}).get("game", OVERVIEW_ID)
        classes = ["game-tab is-active" if t["index"] == game_id else "game-tab" for t in tab_ids]
        return classes, components.mode_pills(GAMES.get(game_id), (view or {}).get("mode"))

    @app.callback(
        Output("profiles", "children"),
        Output("results", "style"),
        Output("empty-state", "style"),
        Input("players-store", "data"),
    )
    def render_profiles(data):
        if not data:
            return None, {"display": "none"}, None
        players = [PlayerProfile.from_dict(d) for d in data]
        return components.profile_grid(players), None, {"display": "none"}

    @app.callback(
        Output("view-content", "children"),
        Input("view-store", "data"),
        Input("players-store", "data"),
    )
    def render_view(view, data):
        if not data:
            return None
        players = [PlayerProfile.from_dict(d) for d in data]
        game = GAMES.get((view or {}).get("game"))
        if game is None:
            return components.overview_view(players)
        return components.mode_view(players, game, game.mode((view or {}).get("mode")))
