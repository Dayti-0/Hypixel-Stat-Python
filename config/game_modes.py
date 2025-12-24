# Game modes configuration - Organized by game type with sub-modes

def safe_divide(a, b):
    """Safely divide two numbers, returning 0 if divisor is 0."""
    return round(a / b, 2) if b > 0 else 0


# Organized game modes structure
GAME_CATEGORIES = {
    'bedwars': {
        'name': 'Bedwars',
        'icon': '⚔️',
        'color': '#e74c3c',
        'modes': {
            'bedwars_overall': {
                'id': 'bedwars_overall',
                'name': 'Overall',
                'parent': 'bedwars',
            },
            'bedwars_solo': {
                'id': 'bedwars_solo',
                'name': 'Solo',
                'parent': 'bedwars',
            },
            'bedwars_doubles': {
                'id': 'bedwars_doubles',
                'name': 'Doubles',
                'parent': 'bedwars',
            },
            'bedwars_threes': {
                'id': 'bedwars_threes',
                'name': '3v3v3v3',
                'parent': 'bedwars',
            },
            'bedwars_fours': {
                'id': 'bedwars_fours',
                'name': '4v4v4v4',
                'parent': 'bedwars',
            },
            'bedwars_4v4': {
                'id': 'bedwars_4v4',
                'name': '4v4',
                'parent': 'bedwars',
            },
        }
    },
    'skywars': {
        'name': 'Skywars',
        'icon': '☁️',
        'color': '#00bcd4',
        'modes': {
            'skywars_overall': {
                'id': 'skywars_overall',
                'name': 'Overall',
                'parent': 'skywars',
            },
            'skywars_ranked': {
                'id': 'skywars_ranked',
                'name': 'Ranked',
                'parent': 'skywars',
            },
            'skywars_solo_normal': {
                'id': 'skywars_solo_normal',
                'name': 'Solo Normal',
                'parent': 'skywars',
            },
            'skywars_solo_insane': {
                'id': 'skywars_solo_insane',
                'name': 'Solo Insane',
                'parent': 'skywars',
            },
            'skywars_team_normal': {
                'id': 'skywars_team_normal',
                'name': 'Team Normal',
                'parent': 'skywars',
            },
            'skywars_team_insane': {
                'id': 'skywars_team_insane',
                'name': 'Team Insane',
                'parent': 'skywars',
            },
            'skywars_mega': {
                'id': 'skywars_mega',
                'name': 'Mega',
                'parent': 'skywars',
            },
        }
    },
    'duels': {
        'name': 'Duels',
        'icon': '🤺',
        'color': '#ff9800',
        'modes': {
            'duels_overall': {
                'id': 'duels_overall',
                'name': 'Overall',
                'parent': 'duels',
            },
            'duel_classic': {
                'id': 'duel_classic',
                'name': 'Classic',
                'parent': 'duels',
            },
            'duel_sumo': {
                'id': 'duel_sumo',
                'name': 'Sumo',
                'parent': 'duels',
            },
            'duel_bridge': {
                'id': 'duel_bridge',
                'name': 'Bridge',
                'parent': 'duels',
            },
            'duel_uhc': {
                'id': 'duel_uhc',
                'name': 'UHC',
                'parent': 'duels',
            },
            'duel_skywars': {
                'id': 'duel_skywars',
                'name': 'Skywars',
                'parent': 'duels',
            },
            'duel_combo': {
                'id': 'duel_combo',
                'name': 'Combo',
                'parent': 'duels',
            },
            'duel_bow': {
                'id': 'duel_bow',
                'name': 'Bow',
                'parent': 'duels',
            },
            'duel_bowspleef': {
                'id': 'duel_bowspleef',
                'name': 'Bowspleef',
                'parent': 'duels',
            },
            'duel_boxing': {
                'id': 'duel_boxing',
                'name': 'Boxing',
                'parent': 'duels',
            },
            'duel_mega_walls': {
                'id': 'duel_mega_walls',
                'name': 'Mega Walls',
                'parent': 'duels',
            },
            'duel_nodebuff': {
                'id': 'duel_nodebuff',
                'name': 'NoDebuff',
                'parent': 'duels',
            },
            'duel_op': {
                'id': 'duel_op',
                'name': 'OP',
                'parent': 'duels',
            },
            'duel_potion': {
                'id': 'duel_potion',
                'name': 'Potion',
                'parent': 'duels',
            },
        }
    },
}

# Flatten all modes into a single dictionary for easy access
GAME_MODES = {}
for category_id, category in GAME_CATEGORIES.items():
    for mode_id, mode_config in category['modes'].items():
        mode_config['category_name'] = category['name']
        mode_config['category_icon'] = category['icon']
        mode_config['color'] = category['color']
        GAME_MODES[mode_id] = mode_config

# Add Combined view
GAME_MODES['combined'] = {
    'id': 'combined',
    'name': 'Combiné',
    'icon': '📊',
    'color': '#4caf50',
    'is_combined': True,
}


def get_mode_config(mode_id):
    """Get configuration for a specific game mode."""
    return GAME_MODES.get(mode_id)


def get_all_modes():
    """Get list of all available game modes."""
    return list(GAME_MODES.keys())


def get_categories():
    """Get all game categories."""
    return GAME_CATEGORIES


def get_mode_stats(player_data, mode_id):
    """Extract stats for a specific mode from player data."""
    if not player_data or 'stats' not in player_data:
        return {}

    # Parse mode_id to determine game type and specific mode
    if mode_id.startswith('bedwars_'):
        return _get_bedwars_stats(player_data, mode_id)
    elif mode_id.startswith('skywars_'):
        return _get_skywars_stats(player_data, mode_id)
    elif mode_id.startswith('duel_') or mode_id == 'duels_overall':
        return _get_duels_stats(player_data, mode_id)

    return {}


def _get_bedwars_stats(player_data, mode_id):
    """Extract Bedwars stats for a specific mode."""
    if 'Bedwars' not in player_data.get('stats', {}):
        return {}

    bedwars = player_data['stats']['Bedwars']

    if mode_id == 'bedwars_overall':
        return {
            'wins': bedwars.get('wins_bedwars', 0),
            'games': bedwars.get('games_played_bedwars', 0),
            'kills': bedwars.get('kills_bedwars', 0),
            'deaths': bedwars.get('deaths_bedwars', 0),
            'beds_broken': bedwars.get('beds_broken_bedwars', 0),
            'final_kills': bedwars.get('final_kills_bedwars', 0),
            'final_deaths': bedwars.get('final_deaths_bedwars', 0),
        }
    elif mode_id == 'bedwars_solo':
        return {
            'wins': bedwars.get('eight_one_wins_bedwars', 0),
            'games': bedwars.get('eight_one_games_played_bedwars', 0),
            'kills': bedwars.get('eight_one_kills_bedwars', 0),
            'deaths': bedwars.get('eight_one_deaths_bedwars', 0),
            'beds_broken': bedwars.get('eight_one_beds_broken_bedwars', 0),
        }
    elif mode_id == 'bedwars_doubles':
        return {
            'wins': bedwars.get('eight_two_wins_bedwars', 0),
            'games': bedwars.get('eight_two_games_played_bedwars', 0),
            'kills': bedwars.get('eight_two_kills_bedwars', 0),
            'deaths': bedwars.get('eight_two_deaths_bedwars', 0),
            'beds_broken': bedwars.get('eight_two_beds_broken_bedwars', 0),
        }
    elif mode_id == 'bedwars_threes':
        return {
            'wins': bedwars.get('four_three_wins_bedwars', 0),
            'games': bedwars.get('four_three_games_played_bedwars', 0),
            'kills': bedwars.get('four_three_kills_bedwars', 0),
            'deaths': bedwars.get('four_three_deaths_bedwars', 0),
            'beds_broken': bedwars.get('four_three_beds_broken_bedwars', 0),
        }
    elif mode_id == 'bedwars_fours':
        return {
            'wins': bedwars.get('four_four_wins_bedwars', 0),
            'games': bedwars.get('four_four_games_played_bedwars', 0),
            'kills': bedwars.get('four_four_kills_bedwars', 0),
            'deaths': bedwars.get('four_four_deaths_bedwars', 0),
            'beds_broken': bedwars.get('four_four_beds_broken_bedwars', 0),
        }
    elif mode_id == 'bedwars_4v4':
        return {
            'wins': bedwars.get('two_four_wins_bedwars', 0),
            'games': bedwars.get('two_four_games_played_bedwars', 0),
            'kills': bedwars.get('two_four_kills_bedwars', 0),
            'deaths': bedwars.get('two_four_deaths_bedwars', 0),
            'beds_broken': bedwars.get('two_four_beds_broken_bedwars', 0),
        }

    return {}


def _get_skywars_stats(player_data, mode_id):
    """Extract Skywars stats for a specific mode."""
    if 'SkyWars' not in player_data.get('stats', {}):
        return {}

    skywars = player_data['stats']['SkyWars']

    if mode_id == 'skywars_overall':
        return {
            'wins': skywars.get('wins', 0),
            'games': skywars.get('games_played_skywars', 0),
            'kills': skywars.get('kills', 0),
            'deaths': skywars.get('deaths', 0),
        }
    elif mode_id == 'skywars_ranked':
        return {
            'wins': skywars.get('ranked_wins', 0),
            'games': skywars.get('ranked_games', 0),
            'kills': skywars.get('ranked_kills', 0),
            'deaths': skywars.get('ranked_deaths', 0),
        }
    elif mode_id == 'skywars_solo_normal':
        return {
            'wins': skywars.get('solo_normal_wins', 0),
            'games': skywars.get('solo_normal_games', 0),
            'kills': skywars.get('solo_normal_kills', 0),
            'deaths': skywars.get('solo_normal_deaths', 0),
        }
    elif mode_id == 'skywars_solo_insane':
        return {
            'wins': skywars.get('solo_insane_wins', 0),
            'games': skywars.get('solo_insane_games', 0),
            'kills': skywars.get('solo_insane_kills', 0),
            'deaths': skywars.get('solo_insane_deaths', 0),
        }
    elif mode_id == 'skywars_team_normal':
        return {
            'wins': skywars.get('team_normal_wins', 0),
            'games': skywars.get('team_normal_games', 0),
            'kills': skywars.get('team_normal_kills', 0),
            'deaths': skywars.get('team_normal_deaths', 0),
        }
    elif mode_id == 'skywars_team_insane':
        return {
            'wins': skywars.get('team_insane_wins', 0),
            'games': skywars.get('team_insane_games', 0),
            'kills': skywars.get('team_insane_kills', 0),
            'deaths': skywars.get('team_insane_deaths', 0),
        }
    elif mode_id == 'skywars_mega':
        return {
            'wins': skywars.get('mega_wins', 0),
            'games': skywars.get('mega_games', 0),
            'kills': skywars.get('mega_kills', 0),
            'deaths': skywars.get('mega_deaths', 0),
        }

    return {}


def _get_duels_stats(player_data, mode_id):
    """Extract Duels stats for a specific mode."""
    if 'Duels' not in player_data.get('stats', {}):
        return {}

    duels = player_data['stats']['Duels']

    if mode_id == 'duels_overall':
        return {
            'wins': duels.get('wins', 0),
            'games': duels.get('rounds_played', 0),
            'kills': duels.get('kills', 0),
            'deaths': duels.get('deaths', 0),
        }

    # Extract the duel type from mode_id (e.g., 'duel_sumo' -> 'sumo')
    duel_type = mode_id.replace('duel_', '')

    return {
        'wins': duels.get(f'{duel_type}_duel_wins', 0),
        'games': duels.get(f'{duel_type}_duel_rounds_played', 0),
        'kills': duels.get(f'{duel_type}_duel_kills', 0),
        'deaths': duels.get(f'{duel_type}_duel_deaths', 0),
        'winstreak': duels.get(f'best_{duel_type}_winstreak', 0),
    }


def compute_stats(raw_stats, mode_id):
    """Compute derived statistics (KDR, Win Rate, etc.)."""
    computed = {}

    # Calculate KDR
    kdr = safe_divide(raw_stats.get('kills', 0), raw_stats.get('deaths', 0))
    computed['kdr'] = {
        'label': 'K/D Ratio',
        'value': kdr,
        'display': f"{kdr:.2f}",
    }

    # Calculate Win Rate
    games = raw_stats.get('games', 0)
    wins = raw_stats.get('wins', 0)
    win_rate = safe_divide(wins, games) * 100 if games > 0 else 0
    computed['win_rate'] = {
        'label': 'Win Rate',
        'value': win_rate,
        'display': f"{win_rate:.2f}%",
    }

    # Add winstreak if available
    if 'winstreak' in raw_stats and raw_stats['winstreak'] > 0:
        computed['winstreak'] = {
            'label': 'Best Winstreak',
            'value': raw_stats['winstreak'],
            'display': str(raw_stats['winstreak']),
        }

    return computed
