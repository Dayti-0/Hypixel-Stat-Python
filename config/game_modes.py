# Game modes configuration - Easy to extend with new modes

GAME_MODES = {
    'bedwars': {
        'id': 'bedwars',
        'name': 'Bedwars',
        'icon': '\u2694\ufe0f',  # Crossed swords
        'color': '#e74c3c',
        'api_key': 'Bedwars',
        'stats': [
            {'key': 'wins_bedwars', 'label': 'Victoires', 'icon': '\U0001f3c6'},
            {'key': 'games_played_bedwars', 'label': 'Parties', 'icon': '\U0001f3ae'},
            {'key': 'kills_bedwars', 'label': '\u00c9liminations', 'icon': '\U0001f5e1\ufe0f'},
            {'key': 'deaths_bedwars', 'label': 'Morts', 'icon': '\U0001f480'},
            {'key': 'beds_broken_bedwars', 'label': 'Lits d\u00e9truits', 'icon': '\U0001f6cf\ufe0f'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills_bedwars', 0), s.get('deaths_bedwars', 0))},
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('wins_bedwars', 0), s.get('games_played_bedwars', 0)) * 100, 'suffix': '%'},
        ],
    },
    'bedwars_4v4': {
        'id': 'bedwars_4v4',
        'name': 'Bedwars 4v4',
        'icon': '\U0001f46b',  # People
        'color': '#e91e63',
        'api_key': 'Bedwars',
        'stats': [
            {'key': 'two_four_wins_bedwars', 'label': 'Victoires', 'icon': '\U0001f3c6'},
            {'key': 'two_four_games_played_bedwars', 'label': 'Parties', 'icon': '\U0001f3ae'},
            {'key': 'two_four_kills_bedwars', 'label': '\u00c9liminations', 'icon': '\U0001f5e1\ufe0f'},
            {'key': 'two_four_deaths_bedwars', 'label': 'Morts', 'icon': '\U0001f480'},
            {'key': 'two_four_beds_broken_bedwars', 'label': 'Lits d\u00e9truits', 'icon': '\U0001f6cf\ufe0f'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('two_four_kills_bedwars', 0), s.get('two_four_deaths_bedwars', 0))},
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('two_four_wins_bedwars', 0), s.get('two_four_games_played_bedwars', 0)) * 100, 'suffix': '%'},
        ],
    },
    'skywars': {
        'id': 'skywars',
        'name': 'Skywars',
        'icon': '\u2601\ufe0f',  # Cloud
        'color': '#00bcd4',
        'api_key': 'SkyWars',
        'stats': [
            {'key': 'wins', 'label': 'Victoires', 'icon': '\U0001f3c6'},
            {'key': 'games_played_skywars', 'label': 'Parties', 'icon': '\U0001f3ae'},
            {'key': 'kills', 'label': '\u00c9liminations', 'icon': '\U0001f5e1\ufe0f'},
            {'key': 'deaths', 'label': 'Morts', 'icon': '\U0001f480'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills', 0), s.get('deaths', 0))},
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('wins', 0), s.get('games_played_skywars', 0)) * 100, 'suffix': '%'},
        ],
    },
    'duels': {
        'id': 'duels',
        'name': 'Duels',
        'icon': '\U0001f93a',  # Fencing
        'color': '#ff9800',
        'api_key': 'Duels',
        'stats': [
            {'key': 'wins', 'label': 'Victoires', 'icon': '\U0001f3c6'},
            {'key': 'rounds_played', 'label': 'Parties', 'icon': '\U0001f3ae'},
            {'key': 'kills', 'label': '\u00c9liminations', 'icon': '\U0001f5e1\ufe0f'},
            {'key': 'deaths', 'label': 'Morts', 'icon': '\U0001f480'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills', 0), s.get('deaths', 0))},
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('wins', 0), s.get('rounds_played', 0)) * 100, 'suffix': '%'},
        ],
    },
    'sumo_duel': {
        'id': 'sumo_duel',
        'name': 'Sumo Duel',
        'icon': '\U0001f94b',  # Martial arts
        'color': '#9c27b0',
        'api_key': 'Duels',
        'prefix': 'sumo_duel_',
        'stats': [
            {'key': 'sumo_duel_wins', 'label': 'Victoires', 'icon': '\U0001f3c6'},
            {'key': 'sumo_duel_rounds_played', 'label': 'Parties', 'icon': '\U0001f3ae'},
            {'key': 'sumo_duel_kills', 'label': '\u00c9liminations', 'icon': '\U0001f5e1\ufe0f'},
            {'key': 'sumo_duel_deaths', 'label': 'Morts', 'icon': '\U0001f480'},
        ],
        'winstreak_key': 'best_sumo_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('sumo_duel_kills', 0), s.get('sumo_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_sumo_winstreak', 0)},
        ],
    },
    'classic_duel': {
        'id': 'classic_duel',
        'name': 'Classic Duel',
        'icon': '\U0001f5e1\ufe0f',  # Dagger
        'color': '#607d8b',
        'api_key': 'Duels',
        'prefix': 'classic_duel_',
        'stats': [
            {'key': 'classic_duel_wins', 'label': 'Victoires', 'icon': '\U0001f3c6'},
            {'key': 'classic_duel_rounds_played', 'label': 'Parties', 'icon': '\U0001f3ae'},
            {'key': 'classic_duel_kills', 'label': '\u00c9liminations', 'icon': '\U0001f5e1\ufe0f'},
            {'key': 'classic_duel_deaths', 'label': 'Morts', 'icon': '\U0001f480'},
        ],
        'winstreak_key': 'best_classic_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('classic_duel_kills', 0), s.get('classic_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_classic_winstreak', 0)},
        ],
    },
    'combined': {
        'id': 'combined',
        'name': 'Combin\u00e9',
        'icon': '\U0001f4ca',  # Chart
        'color': '#4caf50',
        'is_combined': True,
        'sources': ['bedwars', 'skywars', 'duels'],
    },
}


def safe_divide(a, b):
    """Safely divide two numbers, returning 0 if divisor is 0."""
    return round(a / b, 2) if b > 0 else 0


def get_mode_config(mode_id):
    """Get configuration for a specific game mode."""
    return GAME_MODES.get(mode_id)


def get_all_modes():
    """Get list of all available game modes."""
    return list(GAME_MODES.keys())


def get_mode_stats(player_data, mode_id):
    """Extract stats for a specific mode from player data."""
    config = get_mode_config(mode_id)
    if not config or not player_data:
        return {}

    api_key = config.get('api_key')
    if not api_key or 'stats' not in player_data:
        return {}

    game_stats = player_data['stats'].get(api_key, {})

    result = {}
    for stat in config.get('stats', []):
        key = stat['key']
        result[key] = game_stats.get(key, 0)

    # Add winstreak if available
    if 'winstreak_key' in config:
        result[config['winstreak_key']] = game_stats.get(config['winstreak_key'], 0)

    return result


def compute_stats(raw_stats, mode_id):
    """Compute derived statistics (KDR, Win Rate, etc.)."""
    config = get_mode_config(mode_id)
    if not config:
        return {}

    computed = {}
    for stat in config.get('computed_stats', []):
        value = stat['formula'](raw_stats)
        suffix = stat.get('suffix', '')
        computed[stat['id']] = {
            'label': stat['label'],
            'value': value,
            'display': f"{value:.2f}{suffix}" if isinstance(value, float) else f"{value}{suffix}",
        }

    return computed
