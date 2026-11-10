import json

import plotly

from hypixel_stats.dashboard import components, create_app
from hypixel_stats.dashboard.formatting import fmt_int, fmt_percent, fmt_ratio
from hypixel_stats.games import GAMES
from hypixel_stats.parser import parse_player
from hypixel_stats.settings import Settings


def _players(raw_player):
    other = dict(raw_player, uuid="0" * 32, displayname="Other", stats={})
    return [parse_player(raw_player), parse_player(other)]


def _serializable(component):
    json.dumps(component, cls=plotly.utils.PlotlyJSONEncoder)


def test_formatting():
    assert fmt_int(1234567) == "1 234 567"
    assert fmt_ratio(7.5) == "7,50"
    assert fmt_percent(75) == "75,0 %"


def test_every_mode_renders(raw_player):
    players = _players(raw_player)
    for game in GAMES.values():
        for mode in game.modes:
            _serializable(components.mode_view(players, game, mode))
    _serializable(components.overview_view(players))
    _serializable(components.profile_grid(players))


def test_best_value_is_highlighted(raw_player):
    players = _players(raw_player)
    table = json.dumps(components.comparison_table(players, GAMES["bedwars"], GAMES["bedwars"].modes[0]),
                       cls=plotly.utils.PlotlyJSONEncoder)
    assert "is-best" in table


def test_create_app_layout():
    app = create_app(Settings(api_key=""), client_factory=lambda key: None)
    assert app.title == "Hypixel Stats"
    layout = json.dumps(app.layout, cls=plotly.utils.PlotlyJSONEncoder)
    for component_id in ("usernames-input", "api-key-input", "fetch-button", "view-content"):
        assert component_id in layout


def test_rows_nobody_has_are_hidden(raw_player):
    players = _players(raw_player)
    duels = GAMES["duels"]
    table = json.dumps(components.comparison_table(players, duels, duels.mode("duels.uhc")),
                       cls=plotly.utils.PlotlyJSONEncoder)
    assert "Victoires" in table
    assert "K/D" not in table and "Éliminations" not in table  # fixture has no UHC kills
