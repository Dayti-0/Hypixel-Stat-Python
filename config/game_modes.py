# Game modes configuration with sections and subsections

def safe_divide(a, b):
    """Safely divide two numbers, returning 0 if divisor is 0."""
    return round(a / b, 2) if b > 0 else 0


# Menu structure with sections and subsections
MENU_SECTIONS = {
    'duels': {
        'name': 'Duels',
        'icon': '🤺',
        'color': '#ff9800',
        'submodes': ['duels_general', 'classic_duel', 'op_duel', 'bow_duel', 'sumo_duel', 'boxing_duel',
                     'uhc_duel', 'uhc_doubles', 'skywars_duel', 'skywars_doubles', 'blitz_duel',
                     'bridge_duel', 'bridge_doubles', 'combo_duel', 'nodebuff_duel', 'megawalls_duel',
                     'bowspleef_duel', 'arena_duel', 'bedwars_duel']
    },
    'bedwars': {
        'name': 'Bedwars',
        'icon': '🛏️',
        'color': '#e74c3c',
        'submodes': ['bedwars_general', 'bedwars_solo', 'bedwars_doubles', 'bedwars_3v3', 'bedwars_4v4', 'bedwars_4v4v4v4']
    },
    'skywars': {
        'name': 'SkyWars',
        'icon': '☁️',
        'color': '#00bcd4',
        'submodes': ['skywars_general', 'skywars_solo_normal', 'skywars_solo_insane', 'skywars_teams_normal', 'skywars_teams_insane']
    },
    'arcade': {
        'name': 'Arcade',
        'icon': '🎮',
        'color': '#9c27b0',
        'submodes': ['arcade_general', 'party_games', 'pixel_party', 'zombies', 'dropper', 'simon_says',
                     'hide_and_seek', 'farm_hunt', 'hole_in_the_wall', 'mini_walls', 'bounty_hunters', 'dragon_wars']
    },
    'murder_mystery': {
        'name': 'Murder Mystery',
        'icon': '🔪',
        'color': '#f44336',
        'submodes': ['murder_classic', 'murder_assassins', 'murder_double_up', 'murder_infection']
    },
    'tnt_games': {
        'name': 'TNT Games',
        'icon': '💣',
        'color': '#ff5722',
        'submodes': ['tnt_tag', 'tnt_run', 'tnt_bowspleef', 'tnt_wizards']
    },
    'build_battle': {
        'name': 'Build Battle',
        'icon': '🏗️',
        'color': '#4caf50',
        'submodes': ['build_battle_solo', 'build_battle_teams', 'guess_the_build']
    },
    'other_games': {
        'name': 'Autres Jeux',
        'icon': '🎯',
        'color': '#607d8b',
        'submodes': ['mega_walls', 'blitz_sg', 'uhc_champions', 'wool_wars', 'capture_the_wool',
                     'speed_uhc', 'the_pit', 'quake', 'arena_brawl', 'turbo_kart', 'paintball',
                     'vampirez', 'the_walls', 'warlords', 'smash_heroes', 'cops_and_crims']
    },
}


# All game modes configurations
GAME_MODES = {
    # ==================== DUELS ====================
    'duels_general': {
        'id': 'duels_general',
        'name': 'Général',
        'icon': '🤺',
        'color': '#ff9800',
        'api_key': 'Duels',
        'section': 'duels',
        'stats': [
            {'key': 'wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'melee_hits', 'label': 'Coups', 'icon': '👊'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills', 0), s.get('deaths', 0))},
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('wins', 0), s.get('rounds_played', 0)) * 100, 'suffix': '%'},
        ],
    },
    'classic_duel': {
        'id': 'classic_duel',
        'name': 'Classic',
        'icon': '🗡️',
        'color': '#607d8b',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'classic_duel_',
        'stats': [
            {'key': 'classic_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'classic_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'classic_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'classic_duel_deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'classic_duel_melee_hits', 'label': 'Coups', 'icon': '👊'},
        ],
        'winstreak_key': 'best_classic_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('classic_duel_kills', 0), s.get('classic_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_classic_winstreak', 0)},
        ],
    },
    'op_duel': {
        'id': 'op_duel',
        'name': 'OP',
        'icon': '💎',
        'color': '#00bcd4',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'op_duel_',
        'stats': [
            {'key': 'op_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'op_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'op_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'op_duel_deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'op_duel_health_regenerated', 'label': 'Vie régénérée', 'icon': '❤️'},
        ],
        'winstreak_key': 'best_op_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('op_duel_kills', 0), s.get('op_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_op_winstreak', 0)},
        ],
    },
    'bow_duel': {
        'id': 'bow_duel',
        'name': 'Bow',
        'icon': '🏹',
        'color': '#8bc34a',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'bow_duel_',
        'stats': [
            {'key': 'bow_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'bow_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'bow_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'bow_duel_deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'bow_duel_bow_hits', 'label': 'Flèches touchées', 'icon': '🎯'},
        ],
        'winstreak_key': 'best_bow_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('bow_duel_kills', 0), s.get('bow_duel_deaths', 0))},
            {'id': 'accuracy', 'label': 'Précision', 'formula': lambda s: safe_divide(s.get('bow_duel_bow_hits', 0), s.get('bow_duel_bow_shots', 0)) * 100, 'suffix': '%'},
        ],
    },
    'sumo_duel': {
        'id': 'sumo_duel',
        'name': 'Sumo',
        'icon': '🥋',
        'color': '#9c27b0',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'sumo_duel_',
        'stats': [
            {'key': 'sumo_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'sumo_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'sumo_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'sumo_duel_deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'sumo_duel_melee_hits', 'label': 'Coups', 'icon': '👊'},
        ],
        'winstreak_key': 'best_sumo_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('sumo_duel_kills', 0), s.get('sumo_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_sumo_winstreak', 0)},
        ],
    },
    'boxing_duel': {
        'id': 'boxing_duel',
        'name': 'Boxing',
        'icon': '🥊',
        'color': '#f44336',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'boxing_duel_',
        'stats': [
            {'key': 'boxing_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'boxing_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'boxing_duel_losses', 'label': 'Défaites', 'icon': '💀'},
            {'key': 'boxing_duel_melee_hits', 'label': 'Coups donnés', 'icon': '👊'},
            {'key': 'boxing_duel_melee_swings', 'label': 'Coups tentés', 'icon': '🎯'},
        ],
        'winstreak_key': 'best_boxing_winstreak',
        'computed_stats': [
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('boxing_duel_wins', 0), s.get('boxing_duel_rounds_played', 0)) * 100, 'suffix': '%'},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_boxing_winstreak', 0)},
        ],
    },
    'uhc_duel': {
        'id': 'uhc_duel',
        'name': 'UHC',
        'icon': '❤️',
        'color': '#e91e63',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'uhc_duel_',
        'stats': [
            {'key': 'uhc_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'uhc_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'uhc_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'uhc_duel_deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'uhc_duel_health_regenerated', 'label': 'Vie régénérée', 'icon': '❤️'},
        ],
        'winstreak_key': 'best_uhc_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('uhc_duel_kills', 0), s.get('uhc_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_uhc_winstreak', 0)},
        ],
    },
    'uhc_doubles': {
        'id': 'uhc_doubles',
        'name': 'UHC Doubles',
        'icon': '❤️',
        'color': '#e91e63',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'uhc_doubles_',
        'stats': [
            {'key': 'uhc_doubles_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'uhc_doubles_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'uhc_doubles_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'uhc_doubles_deaths', 'label': 'Morts', 'icon': '💀'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('uhc_doubles_kills', 0), s.get('uhc_doubles_deaths', 0))},
        ],
    },
    'skywars_duel': {
        'id': 'skywars_duel',
        'name': 'SkyWars',
        'icon': '☁️',
        'color': '#00bcd4',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'sw_duel_',
        'stats': [
            {'key': 'sw_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'sw_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'sw_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'sw_duel_deaths', 'label': 'Morts', 'icon': '💀'},
        ],
        'winstreak_key': 'best_skywars_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('sw_duel_kills', 0), s.get('sw_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_skywars_winstreak', 0)},
        ],
    },
    'skywars_doubles': {
        'id': 'skywars_doubles',
        'name': 'SkyWars Doubles',
        'icon': '☁️',
        'color': '#00bcd4',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'sw_doubles_',
        'stats': [
            {'key': 'sw_doubles_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'sw_doubles_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'sw_doubles_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'sw_doubles_deaths', 'label': 'Morts', 'icon': '💀'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('sw_doubles_kills', 0), s.get('sw_doubles_deaths', 0))},
        ],
    },
    'blitz_duel': {
        'id': 'blitz_duel',
        'name': 'Blitz',
        'icon': '⚡',
        'color': '#ffc107',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'blitz_duel_',
        'stats': [
            {'key': 'blitz_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'blitz_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'blitz_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'blitz_duel_deaths', 'label': 'Morts', 'icon': '💀'},
        ],
        'winstreak_key': 'best_blitz_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('blitz_duel_kills', 0), s.get('blitz_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_blitz_winstreak', 0)},
        ],
    },
    'bridge_duel': {
        'id': 'bridge_duel',
        'name': 'Bridge',
        'icon': '🌉',
        'color': '#03a9f4',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'bridge_duel_',
        'stats': [
            {'key': 'bridge_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'bridge_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'bridge_duel_goals', 'label': 'Buts', 'icon': '⚽'},
            {'key': 'bridge_duel_bridge_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'bridge_duel_bridge_deaths', 'label': 'Morts', 'icon': '💀'},
        ],
        'winstreak_key': 'best_bridge_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('bridge_duel_bridge_kills', 0), s.get('bridge_duel_bridge_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_bridge_winstreak', 0)},
        ],
    },
    'bridge_doubles': {
        'id': 'bridge_doubles',
        'name': 'Bridge Doubles',
        'icon': '🌉',
        'color': '#03a9f4',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'bridge_doubles_',
        'stats': [
            {'key': 'bridge_doubles_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'bridge_doubles_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'bridge_doubles_goals', 'label': 'Buts', 'icon': '⚽'},
            {'key': 'bridge_doubles_bridge_kills', 'label': 'Éliminations', 'icon': '🗡️'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('bridge_doubles_bridge_kills', 0), s.get('bridge_doubles_bridge_deaths', 0))},
        ],
    },
    'combo_duel': {
        'id': 'combo_duel',
        'name': 'Combo',
        'icon': '🔥',
        'color': '#ff5722',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'combo_duel_',
        'stats': [
            {'key': 'combo_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'combo_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'combo_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'combo_duel_deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'combo_duel_melee_hits', 'label': 'Coups', 'icon': '👊'},
        ],
        'winstreak_key': 'best_combo_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('combo_duel_kills', 0), s.get('combo_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_combo_winstreak', 0)},
        ],
    },
    'nodebuff_duel': {
        'id': 'nodebuff_duel',
        'name': 'No Debuff',
        'icon': '🧪',
        'color': '#e91e63',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'potion_duel_',
        'stats': [
            {'key': 'potion_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'potion_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'potion_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'potion_duel_deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'potion_duel_heal_pots_used', 'label': 'Potions utilisées', 'icon': '🧪'},
        ],
        'winstreak_key': 'best_no_debuff_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('potion_duel_kills', 0), s.get('potion_duel_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_no_debuff_winstreak', 0)},
        ],
    },
    'megawalls_duel': {
        'id': 'megawalls_duel',
        'name': 'Mega Walls',
        'icon': '🧱',
        'color': '#795548',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'mw_duel_',
        'stats': [
            {'key': 'mw_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'mw_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'mw_duel_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'mw_duel_deaths', 'label': 'Morts', 'icon': '💀'},
        ],
        'winstreak_key': 'best_mega_walls_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('mw_duel_kills', 0), s.get('mw_duel_deaths', 0))},
        ],
    },
    'bowspleef_duel': {
        'id': 'bowspleef_duel',
        'name': 'Bow Spleef',
        'icon': '🏹',
        'color': '#ff9800',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'bowspleef_duel_',
        'stats': [
            {'key': 'bowspleef_duel_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'bowspleef_duel_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'bowspleef_duel_deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'bowspleef_duel_bow_shots', 'label': 'Flèches tirées', 'icon': '🏹'},
        ],
        'computed_stats': [
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('bowspleef_duel_wins', 0), s.get('bowspleef_duel_rounds_played', 0)) * 100, 'suffix': '%'},
        ],
    },
    'arena_duel': {
        'id': 'arena_duel',
        'name': 'Arena',
        'icon': '🏟️',
        'color': '#673ab7',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'duel_arena_',
        'stats': [
            {'key': 'duel_arena_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'duel_arena_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'duel_arena_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'duel_arena_deaths', 'label': 'Morts', 'icon': '💀'},
        ],
        'winstreak_key': 'best_arena_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('duel_arena_kills', 0), s.get('duel_arena_deaths', 0))},
        ],
    },
    'bedwars_duel': {
        'id': 'bedwars_duel',
        'name': 'Bedwars Rush',
        'icon': '🛏️',
        'color': '#e74c3c',
        'api_key': 'Duels',
        'section': 'duels',
        'prefix': 'bedwars_two_one_duels_rush_',
        'stats': [
            {'key': 'bedwars_two_one_duels_rush_wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'bedwars_two_one_duels_rush_rounds_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'bedwars_two_one_duels_rush_kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'bedwars_two_one_duels_rush_deaths', 'label': 'Morts', 'icon': '💀'},
        ],
        'winstreak_key': 'best_bedwars_winstreak',
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('bedwars_two_one_duels_rush_kills', 0), s.get('bedwars_two_one_duels_rush_deaths', 0))},
            {'id': 'winstreak', 'label': 'Best Winstreak', 'formula': lambda s: s.get('best_bedwars_winstreak', 0)},
        ],
    },

    # ==================== BEDWARS ====================
    'bedwars_general': {
        'id': 'bedwars_general',
        'name': 'Général',
        'icon': '🛏️',
        'color': '#e74c3c',
        'api_key': 'Bedwars',
        'section': 'bedwars',
        'stats': [
            {'key': 'wins_bedwars', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_played_bedwars', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills_bedwars', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_bedwars', 'label': 'Morts', 'icon': '💀'},
            {'key': 'beds_broken_bedwars', 'label': 'Lits détruits', 'icon': '🛏️'},
            {'key': 'final_kills_bedwars', 'label': 'Kills finaux', 'icon': '⚔️'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills_bedwars', 0), s.get('deaths_bedwars', 0))},
            {'id': 'fkdr', 'label': 'FKDR', 'formula': lambda s: safe_divide(s.get('final_kills_bedwars', 0), s.get('final_deaths_bedwars', 0))},
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('wins_bedwars', 0), s.get('games_played_bedwars', 0)) * 100, 'suffix': '%'},
        ],
    },
    'bedwars_solo': {
        'id': 'bedwars_solo',
        'name': 'Solo',
        'icon': '👤',
        'color': '#e74c3c',
        'api_key': 'Bedwars',
        'section': 'bedwars',
        'prefix': 'eight_one_',
        'stats': [
            {'key': 'eight_one_wins_bedwars', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'eight_one_games_played_bedwars', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'eight_one_kills_bedwars', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'eight_one_deaths_bedwars', 'label': 'Morts', 'icon': '💀'},
            {'key': 'eight_one_beds_broken_bedwars', 'label': 'Lits détruits', 'icon': '🛏️'},
            {'key': 'eight_one_final_kills_bedwars', 'label': 'Kills finaux', 'icon': '⚔️'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('eight_one_kills_bedwars', 0), s.get('eight_one_deaths_bedwars', 0))},
            {'id': 'fkdr', 'label': 'FKDR', 'formula': lambda s: safe_divide(s.get('eight_one_final_kills_bedwars', 0), s.get('eight_one_final_deaths_bedwars', 0))},
        ],
    },
    'bedwars_doubles': {
        'id': 'bedwars_doubles',
        'name': 'Doubles',
        'icon': '👥',
        'color': '#e74c3c',
        'api_key': 'Bedwars',
        'section': 'bedwars',
        'prefix': 'eight_two_',
        'stats': [
            {'key': 'eight_two_wins_bedwars', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'eight_two_games_played_bedwars', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'eight_two_kills_bedwars', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'eight_two_deaths_bedwars', 'label': 'Morts', 'icon': '💀'},
            {'key': 'eight_two_beds_broken_bedwars', 'label': 'Lits détruits', 'icon': '🛏️'},
            {'key': 'eight_two_final_kills_bedwars', 'label': 'Kills finaux', 'icon': '⚔️'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('eight_two_kills_bedwars', 0), s.get('eight_two_deaths_bedwars', 0))},
            {'id': 'fkdr', 'label': 'FKDR', 'formula': lambda s: safe_divide(s.get('eight_two_final_kills_bedwars', 0), s.get('eight_two_final_deaths_bedwars', 0))},
        ],
    },
    'bedwars_3v3': {
        'id': 'bedwars_3v3',
        'name': '3v3v3v3',
        'icon': '👥',
        'color': '#e74c3c',
        'api_key': 'Bedwars',
        'section': 'bedwars',
        'prefix': 'four_three_',
        'stats': [
            {'key': 'four_three_wins_bedwars', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'four_three_games_played_bedwars', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'four_three_kills_bedwars', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'four_three_deaths_bedwars', 'label': 'Morts', 'icon': '💀'},
            {'key': 'four_three_beds_broken_bedwars', 'label': 'Lits détruits', 'icon': '🛏️'},
            {'key': 'four_three_final_kills_bedwars', 'label': 'Kills finaux', 'icon': '⚔️'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('four_three_kills_bedwars', 0), s.get('four_three_deaths_bedwars', 0))},
            {'id': 'fkdr', 'label': 'FKDR', 'formula': lambda s: safe_divide(s.get('four_three_final_kills_bedwars', 0), s.get('four_three_final_deaths_bedwars', 0))},
        ],
    },
    'bedwars_4v4': {
        'id': 'bedwars_4v4',
        'name': '4v4v4v4',
        'icon': '👥',
        'color': '#e74c3c',
        'api_key': 'Bedwars',
        'section': 'bedwars',
        'prefix': 'four_four_',
        'stats': [
            {'key': 'four_four_wins_bedwars', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'four_four_games_played_bedwars', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'four_four_kills_bedwars', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'four_four_deaths_bedwars', 'label': 'Morts', 'icon': '💀'},
            {'key': 'four_four_beds_broken_bedwars', 'label': 'Lits détruits', 'icon': '🛏️'},
            {'key': 'four_four_final_kills_bedwars', 'label': 'Kills finaux', 'icon': '⚔️'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('four_four_kills_bedwars', 0), s.get('four_four_deaths_bedwars', 0))},
            {'id': 'fkdr', 'label': 'FKDR', 'formula': lambda s: safe_divide(s.get('four_four_final_kills_bedwars', 0), s.get('four_four_final_deaths_bedwars', 0))},
        ],
    },
    'bedwars_4v4v4v4': {
        'id': 'bedwars_4v4v4v4',
        'name': '4v4',
        'icon': '👥',
        'color': '#e91e63',
        'api_key': 'Bedwars',
        'section': 'bedwars',
        'prefix': 'two_four_',
        'stats': [
            {'key': 'two_four_wins_bedwars', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'two_four_games_played_bedwars', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'two_four_kills_bedwars', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'two_four_deaths_bedwars', 'label': 'Morts', 'icon': '💀'},
            {'key': 'two_four_beds_broken_bedwars', 'label': 'Lits détruits', 'icon': '🛏️'},
            {'key': 'two_four_final_kills_bedwars', 'label': 'Kills finaux', 'icon': '⚔️'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('two_four_kills_bedwars', 0), s.get('two_four_deaths_bedwars', 0))},
            {'id': 'fkdr', 'label': 'FKDR', 'formula': lambda s: safe_divide(s.get('two_four_final_kills_bedwars', 0), s.get('two_four_final_deaths_bedwars', 0))},
        ],
    },

    # ==================== SKYWARS ====================
    'skywars_general': {
        'id': 'skywars_general',
        'name': 'Général',
        'icon': '☁️',
        'color': '#00bcd4',
        'api_key': 'SkyWars',
        'section': 'skywars',
        'stats': [
            {'key': 'wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_played_skywars', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'souls', 'label': 'Âmes', 'icon': '👻'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills', 0), s.get('deaths', 0))},
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('wins', 0), s.get('games_played_skywars', 0)) * 100, 'suffix': '%'},
        ],
    },
    'skywars_solo_normal': {
        'id': 'skywars_solo_normal',
        'name': 'Solo Normal',
        'icon': '👤',
        'color': '#00bcd4',
        'api_key': 'SkyWars',
        'section': 'skywars',
        'stats': [
            {'key': 'wins_solo_normal', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_solo', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills_solo_normal', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_solo_normal', 'label': 'Morts', 'icon': '💀'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills_solo_normal', 0), s.get('deaths_solo_normal', 0))},
        ],
    },
    'skywars_solo_insane': {
        'id': 'skywars_solo_insane',
        'name': 'Solo Insane',
        'icon': '👤',
        'color': '#ff5722',
        'api_key': 'SkyWars',
        'section': 'skywars',
        'stats': [
            {'key': 'wins_solo_insane', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_solo', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills_solo_insane', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_solo_insane', 'label': 'Morts', 'icon': '💀'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills_solo_insane', 0), s.get('deaths_solo_insane', 0))},
        ],
    },
    'skywars_teams_normal': {
        'id': 'skywars_teams_normal',
        'name': 'Teams Normal',
        'icon': '👥',
        'color': '#00bcd4',
        'api_key': 'SkyWars',
        'section': 'skywars',
        'stats': [
            {'key': 'wins_team_normal', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_team', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills_team_normal', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_team_normal', 'label': 'Morts', 'icon': '💀'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills_team_normal', 0), s.get('deaths_team_normal', 0))},
        ],
    },
    'skywars_teams_insane': {
        'id': 'skywars_teams_insane',
        'name': 'Teams Insane',
        'icon': '👥',
        'color': '#ff5722',
        'api_key': 'SkyWars',
        'section': 'skywars',
        'stats': [
            {'key': 'wins_team_insane', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_team', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills_team_insane', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_team_insane', 'label': 'Morts', 'icon': '💀'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills_team_insane', 0), s.get('deaths_team_insane', 0))},
        ],
    },

    # ==================== ARCADE ====================
    'arcade_general': {
        'id': 'arcade_general',
        'name': 'Général',
        'icon': '🎮',
        'color': '#9c27b0',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'coins', 'label': 'Pièces', 'icon': '🪙'},
        ],
        'computed_stats': [],
    },
    'party_games': {
        'id': 'party_games',
        'name': 'Party Games',
        'icon': '🎉',
        'color': '#e91e63',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'wins_party', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'round_wins_party', 'label': 'Manches gagnées', 'icon': '✅'},
            {'key': 'total_stars_party', 'label': 'Étoiles totales', 'icon': '⭐'},
        ],
        'computed_stats': [],
    },
    'pixel_party': {
        'id': 'pixel_party',
        'name': 'Pixel Party',
        'icon': '🎨',
        'color': '#ff9800',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'pixel_party.wins', 'label': 'Victoires', 'icon': '🏆', 'nested': True},
            {'key': 'pixel_party.games_played', 'label': 'Parties', 'icon': '🎮', 'nested': True},
            {'key': 'pixel_party.rounds_completed', 'label': 'Manches complétées', 'icon': '✅', 'nested': True},
            {'key': 'pixel_party.highest_round', 'label': 'Meilleure manche', 'icon': '📈', 'nested': True},
        ],
        'computed_stats': [],
    },
    'zombies': {
        'id': 'zombies',
        'name': 'Zombies',
        'icon': '🧟',
        'color': '#4caf50',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'best_round_zombies', 'label': 'Meilleure manche', 'icon': '📈'},
            {'key': 'zombie_kills_zombies', 'label': 'Zombies tués', 'icon': '🧟'},
            {'key': 'deaths_zombies', 'label': 'Morts', 'icon': '💀'},
            {'key': 'players_revived_zombies', 'label': 'Joueurs réanimés', 'icon': '💚'},
            {'key': 'headshots_zombies', 'label': 'Headshots', 'icon': '🎯'},
        ],
        'computed_stats': [],
    },
    'dropper': {
        'id': 'dropper',
        'name': 'Dropper',
        'icon': '⬇️',
        'color': '#03a9f4',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'dropper.games_played', 'label': 'Parties', 'icon': '🎮', 'nested': True},
            {'key': 'dropper.maps_completed', 'label': 'Maps complétées', 'icon': '🗺️', 'nested': True},
            {'key': 'dropper.fails', 'label': 'Échecs', 'icon': '❌', 'nested': True},
        ],
        'computed_stats': [],
    },
    'simon_says': {
        'id': 'simon_says',
        'name': 'Simon Says',
        'icon': '🔴',
        'color': '#f44336',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'wins_simon_says', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'rounds_simon_says', 'label': 'Manches jouées', 'icon': '🔄'},
            {'key': 'round_wins_simon_says', 'label': 'Manches gagnées', 'icon': '✅'},
            {'key': 'top_score_simon_says', 'label': 'Meilleur score', 'icon': '📈'},
        ],
        'computed_stats': [],
    },
    'hide_and_seek': {
        'id': 'hide_and_seek',
        'name': 'Hide and Seek',
        'icon': '👀',
        'color': '#795548',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'hider_wins_hide_and_seek', 'label': 'Victoires Hider', 'icon': '🏆'},
            {'key': 'seeker_wins_hide_and_seek', 'label': 'Victoires Seeker', 'icon': '🏆'},
        ],
        'computed_stats': [],
    },
    'farm_hunt': {
        'id': 'farm_hunt',
        'name': 'Farm Hunt',
        'icon': '🐄',
        'color': '#8bc34a',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'kills_farm_hunt', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'hunter_kills_farm_hunt', 'label': 'Hunter Kills', 'icon': '🎯'},
            {'key': 'poop_collected_farm_hunt', 'label': 'Caca collecté', 'icon': '💩'},
        ],
        'computed_stats': [],
    },
    'hole_in_the_wall': {
        'id': 'hole_in_the_wall',
        'name': 'Hole in the Wall',
        'icon': '🧱',
        'color': '#607d8b',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'rounds_hole_in_the_wall', 'label': 'Manches jouées', 'icon': '🔄'},
            {'key': 'hitw_record_q', 'label': 'Record Qualif', 'icon': '📈'},
            {'key': 'hitw_record_f', 'label': 'Record Final', 'icon': '🏆'},
        ],
        'computed_stats': [],
    },
    'mini_walls': {
        'id': 'mini_walls',
        'name': 'Mini Walls',
        'icon': '🧱',
        'color': '#795548',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'miniwalls_activeKit', 'label': 'Kit actif', 'icon': '🎒'},
        ],
        'computed_stats': [],
    },
    'bounty_hunters': {
        'id': 'bounty_hunters',
        'name': 'Bounty Hunters',
        'icon': '🎯',
        'color': '#ff5722',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'kills_oneinthequiver', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_oneinthequiver', 'label': 'Morts', 'icon': '💀'},
            {'key': 'bow_kills_oneinthequiver', 'label': 'Arc Kills', 'icon': '🏹'},
            {'key': 'bounty_kills_oneinthequiver', 'label': 'Bounty Kills', 'icon': '🎯'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills_oneinthequiver', 0), s.get('deaths_oneinthequiver', 0))},
        ],
    },
    'dragon_wars': {
        'id': 'dragon_wars',
        'name': 'Dragon Wars',
        'icon': '🐉',
        'color': '#673ab7',
        'api_key': 'Arcade',
        'section': 'arcade',
        'stats': [
            {'key': 'wins_dragonwars2', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'kills_dragonwars2', 'label': 'Éliminations', 'icon': '🗡️'},
        ],
        'computed_stats': [],
    },

    # ==================== MURDER MYSTERY ====================
    'murder_classic': {
        'id': 'murder_classic',
        'name': 'Classic',
        'icon': '🔪',
        'color': '#f44336',
        'api_key': 'MurderMystery',
        'section': 'murder_mystery',
        'stats': [
            {'key': 'wins_MURDER_CLASSIC', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_MURDER_CLASSIC', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills_MURDER_CLASSIC', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_MURDER_CLASSIC', 'label': 'Morts', 'icon': '💀'},
            {'key': 'murderer_wins_MURDER_CLASSIC', 'label': 'Wins Murderer', 'icon': '🔪'},
            {'key': 'detective_wins_MURDER_CLASSIC', 'label': 'Wins Detective', 'icon': '🔍'},
        ],
        'computed_stats': [
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('wins_MURDER_CLASSIC', 0), s.get('games_MURDER_CLASSIC', 0)) * 100, 'suffix': '%'},
        ],
    },
    'murder_assassins': {
        'id': 'murder_assassins',
        'name': 'Assassins',
        'icon': '🗡️',
        'color': '#9c27b0',
        'api_key': 'MurderMystery',
        'section': 'murder_mystery',
        'stats': [
            {'key': 'wins_MURDER_ASSASSINS', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_MURDER_ASSASSINS', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills_MURDER_ASSASSINS', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_MURDER_ASSASSINS', 'label': 'Morts', 'icon': '💀'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills_MURDER_ASSASSINS', 0), s.get('deaths_MURDER_ASSASSINS', 0))},
        ],
    },
    'murder_double_up': {
        'id': 'murder_double_up',
        'name': 'Double Up',
        'icon': '👥',
        'color': '#ff9800',
        'api_key': 'MurderMystery',
        'section': 'murder_mystery',
        'stats': [
            {'key': 'wins_MURDER_DOUBLE_UP', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_MURDER_DOUBLE_UP', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills_MURDER_DOUBLE_UP', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_MURDER_DOUBLE_UP', 'label': 'Morts', 'icon': '💀'},
        ],
        'computed_stats': [
            {'id': 'win_rate', 'label': 'Win Rate', 'formula': lambda s: safe_divide(s.get('wins_MURDER_DOUBLE_UP', 0), s.get('games_MURDER_DOUBLE_UP', 0)) * 100, 'suffix': '%'},
        ],
    },
    'murder_infection': {
        'id': 'murder_infection',
        'name': 'Infection',
        'icon': '🦠',
        'color': '#4caf50',
        'api_key': 'MurderMystery',
        'section': 'murder_mystery',
        'stats': [
            {'key': 'wins_MURDER_INFECTION', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_MURDER_INFECTION', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'kills_MURDER_INFECTION', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'survivor_wins_MURDER_INFECTION', 'label': 'Survivor Wins', 'icon': '🏃'},
            {'key': 'alpha_wins_MURDER_INFECTION', 'label': 'Alpha Wins', 'icon': '🦠'},
        ],
        'computed_stats': [],
    },

    # ==================== TNT GAMES ====================
    'tnt_tag': {
        'id': 'tnt_tag',
        'name': 'TNT Tag',
        'icon': '🏃',
        'color': '#ff5722',
        'api_key': 'TNTGames',
        'section': 'tnt_games',
        'stats': [
            {'key': 'wins_tntag', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'kills_tntag', 'label': 'Tags', 'icon': '👆'},
            {'key': 'deaths_tntag', 'label': 'Explosions', 'icon': '💥'},
        ],
        'computed_stats': [],
    },
    'tnt_run': {
        'id': 'tnt_run',
        'name': 'TNT Run',
        'icon': '🏃',
        'color': '#f44336',
        'api_key': 'TNTGames',
        'section': 'tnt_games',
        'stats': [
            {'key': 'wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'deaths_tntrun', 'label': 'Morts', 'icon': '💀'},
            {'key': 'record_tntrun', 'label': 'Record (sec)', 'icon': '⏱️'},
        ],
        'computed_stats': [],
    },
    'tnt_bowspleef': {
        'id': 'tnt_bowspleef',
        'name': 'Bow Spleef',
        'icon': '🏹',
        'color': '#ff9800',
        'api_key': 'TNTGames',
        'section': 'tnt_games',
        'stats': [
            {'key': 'wins', 'label': 'Victoires', 'icon': '🏆'},
        ],
        'computed_stats': [],
    },
    'tnt_wizards': {
        'id': 'tnt_wizards',
        'name': 'Wizards',
        'icon': '🧙',
        'color': '#9c27b0',
        'api_key': 'TNTGames',
        'section': 'tnt_games',
        'stats': [
            {'key': 'wins_capture', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'kills_capture', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths_capture', 'label': 'Morts', 'icon': '💀'},
            {'key': 'assists_capture', 'label': 'Assistances', 'icon': '🤝'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills_capture', 0), s.get('deaths_capture', 0))},
        ],
    },

    # ==================== BUILD BATTLE ====================
    'build_battle_solo': {
        'id': 'build_battle_solo',
        'name': 'Solo',
        'icon': '🏗️',
        'color': '#4caf50',
        'api_key': 'BuildBattle',
        'section': 'build_battle',
        'stats': [
            {'key': 'wins_solo_normal', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'games_played', 'label': 'Parties', 'icon': '🎮'},
            {'key': 'score', 'label': 'Score', 'icon': '📊'},
            {'key': 'total_votes', 'label': 'Votes totaux', 'icon': '👍'},
        ],
        'computed_stats': [],
    },
    'build_battle_teams': {
        'id': 'build_battle_teams',
        'name': 'Teams',
        'icon': '👥',
        'color': '#2196f3',
        'api_key': 'BuildBattle',
        'section': 'build_battle',
        'stats': [
            {'key': 'wins_teams_normal', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'teams_most_points', 'label': 'Record points', 'icon': '📈'},
        ],
        'computed_stats': [],
    },
    'guess_the_build': {
        'id': 'guess_the_build',
        'name': 'Guess The Build',
        'icon': '❓',
        'color': '#ff9800',
        'api_key': 'BuildBattle',
        'section': 'build_battle',
        'stats': [
            {'key': 'wins_guess_the_build', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'correct_guesses', 'label': 'Bonnes réponses', 'icon': '✅'},
        ],
        'computed_stats': [],
    },

    # ==================== OTHER GAMES ====================
    'mega_walls': {
        'id': 'mega_walls',
        'name': 'Mega Walls',
        'icon': '🧱',
        'color': '#795548',
        'api_key': 'Walls3',
        'section': 'other_games',
        'stats': [
            {'key': 'wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'assists', 'label': 'Assistances', 'icon': '🤝'},
            {'key': 'final_deaths', 'label': 'Morts finales', 'icon': '☠️'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills', 0), s.get('deaths', 0))},
        ],
    },
    'blitz_sg': {
        'id': 'blitz_sg',
        'name': 'Blitz SG',
        'icon': '⚡',
        'color': '#ffc107',
        'api_key': 'HungerGames',
        'section': 'other_games',
        'stats': [
            {'key': 'wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'games_played', 'label': 'Parties', 'icon': '🎮'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills', 0), s.get('deaths', 0))},
        ],
    },
    'uhc_champions': {
        'id': 'uhc_champions',
        'name': 'UHC Champions',
        'icon': '❤️',
        'color': '#e91e63',
        'api_key': 'UHC',
        'section': 'other_games',
        'stats': [
            {'key': 'coins', 'label': 'Pièces', 'icon': '🪙'},
        ],
        'computed_stats': [],
    },
    'wool_wars': {
        'id': 'wool_wars',
        'name': 'Wool Wars',
        'icon': '🧶',
        'color': '#e91e63',
        'api_key': 'WoolGames',
        'section': 'other_games',
        'stats': [
            {'key': 'wool_wars.stats.wins', 'label': 'Victoires', 'icon': '🏆', 'nested': True},
            {'key': 'wool_wars.stats.games_played', 'label': 'Parties', 'icon': '🎮', 'nested': True},
            {'key': 'wool_wars.stats.kills', 'label': 'Éliminations', 'icon': '🗡️', 'nested': True},
            {'key': 'wool_wars.stats.deaths', 'label': 'Morts', 'icon': '💀', 'nested': True},
            {'key': 'wool_wars.stats.wool_placed', 'label': 'Laine placée', 'icon': '🧶', 'nested': True},
        ],
        'computed_stats': [],
    },
    'capture_the_wool': {
        'id': 'capture_the_wool',
        'name': 'Capture the Wool',
        'icon': '🚩',
        'color': '#f44336',
        'api_key': 'WoolGames',
        'section': 'other_games',
        'stats': [
            {'key': 'capture_the_wool.stats.kills', 'label': 'Éliminations', 'icon': '🗡️', 'nested': True},
            {'key': 'capture_the_wool.stats.deaths', 'label': 'Morts', 'icon': '💀', 'nested': True},
            {'key': 'capture_the_wool.stats.wools_stolen', 'label': 'Laines volées', 'icon': '🧶', 'nested': True},
            {'key': 'capture_the_wool.stats.gold_earned', 'label': 'Or gagné', 'icon': '🪙', 'nested': True},
        ],
        'computed_stats': [],
    },
    'speed_uhc': {
        'id': 'speed_uhc',
        'name': 'Speed UHC',
        'icon': '⚡',
        'color': '#ff5722',
        'api_key': 'SpeedUHC',
        'section': 'other_games',
        'stats': [],
        'computed_stats': [],
    },
    'the_pit': {
        'id': 'the_pit',
        'name': 'The Pit',
        'icon': '🕳️',
        'color': '#607d8b',
        'api_key': 'Pit',
        'section': 'other_games',
        'stats': [
            {'key': 'pit_stats_ptl.kills', 'label': 'Éliminations', 'icon': '🗡️', 'nested': True},
            {'key': 'pit_stats_ptl.deaths', 'label': 'Morts', 'icon': '💀', 'nested': True},
            {'key': 'pit_stats_ptl.assists', 'label': 'Assistances', 'icon': '🤝', 'nested': True},
            {'key': 'pit_stats_ptl.max_streak', 'label': 'Meilleur streak', 'icon': '🔥', 'nested': True},
        ],
        'computed_stats': [],
    },
    'quake': {
        'id': 'quake',
        'name': 'Quake',
        'icon': '🔫',
        'color': '#9c27b0',
        'api_key': 'Quake',
        'section': 'other_games',
        'stats': [
            {'key': 'wins', 'label': 'Victoires', 'icon': '🏆'},
            {'key': 'kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'deaths', 'label': 'Morts', 'icon': '💀'},
            {'key': 'headshots', 'label': 'Headshots', 'icon': '🎯'},
            {'key': 'highest_killstreak', 'label': 'Meilleur streak', 'icon': '🔥'},
        ],
        'computed_stats': [
            {'id': 'kdr', 'label': 'K/D Ratio', 'formula': lambda s: safe_divide(s.get('kills', 0), s.get('deaths', 0))},
        ],
    },
    'arena_brawl': {
        'id': 'arena_brawl',
        'name': 'Arena Brawl',
        'icon': '🏟️',
        'color': '#673ab7',
        'api_key': 'Arena',
        'section': 'other_games',
        'stats': [
            {'key': 'coins', 'label': 'Pièces', 'icon': '🪙'},
        ],
        'computed_stats': [],
    },
    'turbo_kart': {
        'id': 'turbo_kart',
        'name': 'Turbo Kart Racers',
        'icon': '🏎️',
        'color': '#ff9800',
        'api_key': 'GingerBread',
        'section': 'other_games',
        'stats': [
            {'key': 'coins', 'label': 'Pièces', 'icon': '🪙'},
        ],
        'computed_stats': [],
    },
    'paintball': {
        'id': 'paintball',
        'name': 'Paintball',
        'icon': '🎨',
        'color': '#2196f3',
        'api_key': 'Paintball',
        'section': 'other_games',
        'stats': [
            {'key': 'coins', 'label': 'Pièces', 'icon': '🪙'},
        ],
        'computed_stats': [],
    },
    'vampirez': {
        'id': 'vampirez',
        'name': 'VampireZ',
        'icon': '🧛',
        'color': '#b71c1c',
        'api_key': 'VampireZ',
        'section': 'other_games',
        'stats': [],
        'computed_stats': [],
    },
    'the_walls': {
        'id': 'the_walls',
        'name': 'The Walls',
        'icon': '🧱',
        'color': '#795548',
        'api_key': 'Walls',
        'section': 'other_games',
        'stats': [
            {'key': 'coins', 'label': 'Pièces', 'icon': '🪙'},
        ],
        'computed_stats': [],
    },
    'warlords': {
        'id': 'warlords',
        'name': 'Warlords',
        'icon': '⚔️',
        'color': '#ff5722',
        'api_key': 'Battleground',
        'section': 'other_games',
        'stats': [
            {'key': 'coins', 'label': 'Pièces', 'icon': '🪙'},
        ],
        'computed_stats': [],
    },
    'smash_heroes': {
        'id': 'smash_heroes',
        'name': 'Smash Heroes',
        'icon': '💥',
        'color': '#e91e63',
        'api_key': 'SuperSmash',
        'section': 'other_games',
        'stats': [
            {'key': 'coins', 'label': 'Pièces', 'icon': '🪙'},
        ],
        'computed_stats': [],
    },
    'cops_and_crims': {
        'id': 'cops_and_crims',
        'name': 'Cops and Crims',
        'icon': '👮',
        'color': '#3f51b5',
        'api_key': 'MCGO',
        'section': 'other_games',
        'stats': [
            {'key': 'coins', 'label': 'Pièces', 'icon': '🪙'},
            {'key': 'kills', 'label': 'Éliminations', 'icon': '🗡️'},
            {'key': 'headshot_kills', 'label': 'Headshots', 'icon': '🎯'},
            {'key': 'game_wins', 'label': 'Victoires', 'icon': '🏆'},
        ],
        'computed_stats': [],
    },
}


def get_mode_config(mode_id):
    """Get configuration for a specific game mode."""
    return GAME_MODES.get(mode_id)


def get_all_modes():
    """Get list of all available game modes."""
    return list(GAME_MODES.keys())


def get_nested_value(data, key_path):
    """Get a nested value from a dictionary using dot notation."""
    keys = key_path.split('.')
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, 0)
        else:
            return 0
    return value if value is not None else 0


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
        if stat.get('nested'):
            # Handle nested keys like 'pixel_party.wins'
            result[key] = get_nested_value(game_stats, key)
        else:
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
        try:
            value = stat['formula'](raw_stats)
            suffix = stat.get('suffix', '')
            computed[stat['id']] = {
                'label': stat['label'],
                'value': value,
                'display': f"{value:.2f}{suffix}" if isinstance(value, float) else f"{value}{suffix}",
            }
        except Exception:
            computed[stat['id']] = {
                'label': stat['label'],
                'value': 0,
                'display': "0",
            }

    return computed
