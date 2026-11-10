import pytest

from hypixel_stats import levels
from hypixel_stats.games import GAMES, METRICS, RATIOS, mode_metrics, mode_ratios
from hypixel_stats.models import ModeStats, PlayerProfile
from hypixel_stats.parser import parse_player


# --------------------------------------------------------------------------- levels

@pytest.mark.parametrize("exp, expected", [(0, 1.0), (None, 1.0), (10_000, 2.0), (1_000_000, 26.0)])
def test_network_level(exp, expected):
    assert levels.network_level(exp) == pytest.approx(expected, abs=0.05)


@pytest.mark.parametrize("exp, star", [
    (0, 0), (499, 0), (500, 1), (1500, 2), (3500, 3), (7000, 4), (12_000, 5),
    (487_000, 100), (487_000 * 3 + 7000 + 5000 * 10, 314),
])
def test_bedwars_star(exp, star):
    assert levels.bedwars_star(exp) == star


@pytest.mark.parametrize("exp, level", [(0, 1), (20, 2), (14_999, 11), (15_000, 12), (35_000, 14)])
def test_skywars_level_from_xp(exp, level):
    assert levels.skywars_level_from_xp(exp) == level


def test_skywars_level_prefers_formatted():
    assert levels.skywars_level({"levelFormatted": "§b25⋆", "skywars_experience": 0}) == "25⋆"
    assert levels.skywars_level({"skywars_experience": 15_000}) == "12⋆"
    assert levels.skywars_level({"levelFormatted": "§78"}) == "8⋆"
    assert levels.skywars_level({"levelFormatted": "§f6✙"}) == "6✙"
    assert levels.skywars_level({}) is None


@pytest.mark.parametrize("player, label", [
    ({"rank": "ADMIN", "newPackageRank": "MVP_PLUS"}, "ADMIN"),
    ({"monthlyPackageRank": "SUPERSTAR", "newPackageRank": "MVP_PLUS"}, "MVP++"),
    ({"newPackageRank": "VIP_PLUS"}, "VIP+"),
    ({"packageRank": "MVP"}, "MVP"),
    ({"prefix": "§c[OWNER]"}, "OWNER"),
    ({"rank": "NORMAL"}, None),
    ({}, None),
])
def test_player_rank(player, label):
    assert levels.player_rank(player)[0] == label


# --------------------------------------------------------------------------- registry

def test_registry_is_consistent():
    mode_ids = [m.id for g in GAMES.values() for m in g.modes]
    assert len(mode_ids) == len(set(mode_ids)), "mode ids must be unique"
    for game in GAMES.values():
        assert game.modes[0].id == f"{game.id}.overall"
        assert set(game.metrics) <= set(METRICS)
        assert set(game.ratios) <= set(RATIOS)
        for mode in game.modes:
            assert set(mode.keys) <= set(METRICS), mode.id
            assert mode_metrics(game, mode)
            assert mode_ratios(game, mode)


def test_game_mode_falls_back_to_overall():
    assert GAMES["duels"].mode("nope").id == "duels.overall"
    assert GAMES["duels"].mode(None).id == "duels.overall"


# --------------------------------------------------------------------------- ratios

def test_ratios_and_derived_games():
    stats = ModeStats({"wins": 30, "losses": 10, "kills": 50, "deaths": 0})
    assert stats.get("games_played") == 40
    assert stats.ratio("wlr") == 3
    assert stats.ratio("kdr") == 50  # no deaths: ratio == kills
    assert stats.ratio("win_rate") == 75
    assert ModeStats().ratio("win_rate") == 0
    assert ModeStats().is_empty


# --------------------------------------------------------------------------- parser

def test_parse_player_profile(raw_player):
    profile = parse_player(raw_player)
    assert profile.name == "hypixel"
    assert profile.rank == "ADMIN"
    assert profile.levels == {"bedwars": "412✫", "skywars": "25⋆"}
    assert profile.karma == 123456
    assert int(profile.network_level) == 26


def test_parse_bedwars(raw_player):
    profile = parse_player(raw_player)
    overall = profile.mode("bedwars.overall")
    assert overall.get("games_played") == 1210  # explicit value wins over wins+losses
    assert overall.ratio("fkdr") == 7.5
    assert overall.ratio("bblr") == 5
    assert overall.get("winstreak") == 12
    solo = profile.mode("bedwars.solo")
    assert solo.ratio("fkdr") == 400
    assert not solo.has("winstreak")


def test_parse_skywars_sums_submodes(raw_player):
    profile = parse_player(raw_player)
    assert profile.mode("skywars.overall").get("winstreak") == 3
    mega = profile.mode("skywars.mega")
    assert mega.get("wins") == 12 and mega.get("kills") == 30


def test_parse_duels_uses_real_api_keys(raw_player):
    profile = parse_player(raw_player)
    uhc = profile.mode("duels.uhc")
    assert uhc.get("wins") == 125
    assert uhc.get("best_winstreak") == 15  # max, not sum
    bridge = profile.mode("duels.bridge")
    assert bridge.get("kills") == 900 and bridge.get("goals") == 600
    assert profile.mode("duels.megawalls").get("wins") == 11
    assert profile.mode("duels.nodebuff").get("wins") == 22
    assert profile.mode("duels.skywars").get("wins") == 33
    assert profile.mode("duels.overall").get("best_winstreak") == 40


def test_parse_player_without_stats():
    profile = parse_player({"uuid": "abc", "displayname": "Newbie"})
    assert profile.levels == {}
    assert all(profile.mode(m.id).is_empty for g in GAMES.values() for m in g.modes)


def test_profile_roundtrip(raw_player):
    profile = parse_player(raw_player)
    assert PlayerProfile.from_dict(profile.to_dict()) == profile
