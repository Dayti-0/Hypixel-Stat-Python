"""Dash application factory."""

from __future__ import annotations

from pathlib import Path

import dash
import requests

from hypixel_stats.api import HypixelClient, TTLCache
from hypixel_stats.settings import Settings

from .callbacks import ClientFactory, register_callbacks
from .layout import build_layout

ASSETS = Path(__file__).parent / "assets"


def default_client_factory(settings: Settings) -> ClientFactory:
    """Clients share one HTTP session and one cache, whatever API key they use."""
    session = requests.Session()
    player_cache: TTLCache = TTLCache(settings.cache_ttl)
    uuid_cache: TTLCache = TTLCache(3600)

    def factory(api_key: str) -> HypixelClient:
        return HypixelClient(api_key, session=session, timeout=settings.request_timeout,
                             player_cache=player_cache, uuid_cache=uuid_cache)

    return factory


def create_app(settings: Settings | None = None, client_factory: ClientFactory | None = None) -> dash.Dash:
    settings = settings or Settings.from_env()
    app = dash.Dash(
        __name__,
        title="Hypixel Stats",
        assets_folder=str(ASSETS),
        update_title=None,
        external_stylesheets=[
            "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        ],
    )
    app.layout = build_layout(has_env_key=bool(settings.api_key))
    register_callbacks(app, settings, client_factory or default_client_factory(settings))
    return app
