import plotly.graph_objects as go
from config.theme import CHART_COLORS, CHART_LAYOUT
from config.game_modes import GAME_MODES, safe_divide


def get_nested_value(data, key_path, default=0):
    """Get a value from nested dictionary using dot notation."""
    if not data:
        return default
    keys = key_path.split('.')
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, default)
        else:
            return default
    return value if value is not None else default


def get_stat_value(game_stats, stat_config):
    """Get a stat value from game stats based on configuration."""
    key = stat_config.get('key', '')
    if '.' in key:
        return get_nested_value(game_stats, key, 0)
    return game_stats.get(key, 0)


def apply_dark_theme(fig, title):
    """Apply dark theme styling to a figure."""
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 18, 'color': '#ffffff'},
            'x': 0.5,
            'xanchor': 'center',
        },
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#a0aec0', 'family': 'Inter, system-ui, sans-serif'},
        xaxis={
            'gridcolor': 'rgba(255,255,255,0.1)',
            'zerolinecolor': 'rgba(255,255,255,0.1)',
            'tickfont': {'color': '#a0aec0'},
        },
        yaxis={
            'gridcolor': 'rgba(255,255,255,0.1)',
            'zerolinecolor': 'rgba(255,255,255,0.1)',
            'tickfont': {'color': '#a0aec0'},
        },
        legend={
            'bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': '#a0aec0'},
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': -0.2,
            'xanchor': 'center',
            'x': 0.5,
        },
        margin={'l': 50, 'r': 30, 't': 60, 'b': 80},
        hoverlabel={
            'bgcolor': '#1a1a2e',
            'bordercolor': '#6366f1',
            'font': {'color': '#ffffff'},
        },
    )
    return fig


def create_figure_for_mode(mode_id, mode_config, players_data):
    """Create a figure for a specific game mode."""
    fig = go.Figure()
    api_key = mode_config.get('api_key', '')
    stats_config = mode_config.get('stats', [])

    for i, (username, player) in enumerate(players_data.items()):
        color = CHART_COLORS[i % len(CHART_COLORS)]

        # Get game stats from player data
        game_stats = {}
        if 'stats' in player and api_key in player['stats']:
            game_stats = player['stats'][api_key]

        # Check if we have any stats
        if not game_stats and not stats_config:
            continue

        # Build x and y values from stats config
        x_values = []
        y_values = []

        for stat in stats_config:
            label = stat.get('label', stat.get('key', ''))
            value = get_stat_value(game_stats, stat)
            x_values.append(label)
            y_values.append(value)

        if x_values:
            fig.add_trace(go.Bar(
                x=x_values,
                y=y_values,
                name=username,
                marker_color=color,
                marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
            ))

    title = f"Statistiques {mode_config.get('name', mode_id)}"
    apply_dark_theme(fig, title)
    return fig


def create_combined_figure(players_data):
    """Create a combined stats figure."""
    fig = go.Figure()

    for i, (username, player) in enumerate(players_data.items()):
        color = CHART_COLORS[i % len(CHART_COLORS)]

        # Collect wins from all game types
        combined_wins = 0
        combined_games = 0
        combined_kills = 0
        combined_deaths = 0

        stats = player.get('stats', {})

        # Bedwars
        if 'Bedwars' in stats:
            bedwars = stats['Bedwars']
            combined_wins += bedwars.get('wins_bedwars', 0)
            combined_games += bedwars.get('games_played_bedwars', 0)
            combined_kills += bedwars.get('kills_bedwars', 0)
            combined_deaths += bedwars.get('deaths_bedwars', 0)

        # Duels
        if 'Duels' in stats:
            duels = stats['Duels']
            combined_wins += duels.get('wins', 0)
            combined_games += duels.get('rounds_played', 0)
            combined_kills += duels.get('kills', 0)
            combined_deaths += duels.get('deaths', 0)

        # SkyWars
        if 'SkyWars' in stats:
            skywars = stats['SkyWars']
            combined_wins += skywars.get('wins', 0)
            combined_games += skywars.get('games_played_skywars', 0)
            combined_kills += skywars.get('kills', 0)
            combined_deaths += skywars.get('deaths', 0)

        # Arcade
        if 'Arcade' in stats:
            arcade = stats['Arcade']
            combined_wins += arcade.get('wins', 0)

        # Murder Mystery
        if 'MurderMystery' in stats:
            mm = stats['MurderMystery']
            combined_wins += mm.get('wins', 0)
            combined_games += mm.get('games', 0)
            combined_kills += mm.get('kills', 0)
            combined_deaths += mm.get('deaths', 0)

        # TNT Games
        if 'TNTGames' in stats:
            tnt = stats['TNTGames']
            combined_wins += tnt.get('wins', 0)

        fig.add_trace(go.Bar(
            x=['Victoires', 'Parties', 'Éliminations', 'Morts'],
            y=[combined_wins, combined_games, combined_kills, combined_deaths],
            name=username,
            marker_color=color,
            marker_line_width=0,
            hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
        ))

    apply_dark_theme(fig, "Statistiques Combinées")
    return fig


def extract_winstreaks(players_data):
    """Extract winstreak data for all players."""
    winstreaks = {}

    for username, player in players_data.items():
        stats = player.get('stats', {})
        duels = stats.get('Duels', {})

        if duels:
            winstreaks[username] = {
                'classic': duels.get('best_classic_winstreak', 0),
                'sumo': duels.get('best_sumo_winstreak', 0),
                'op': duels.get('best_op_winstreak', 0),
                'uhc': duels.get('best_uhc_winstreak', 0),
                'bridge': duels.get('best_bridge_winstreak', 0),
                'skywars': duels.get('best_skywars_winstreak', 0),
                'blitz': duels.get('best_blitz_winstreak', 0),
                'bow': duels.get('best_bow_winstreak', 0),
                'boxing': duels.get('current_boxing_winstreak', 0),
                'combo': duels.get('best_combo_winstreak', 0),
                'nodebuff': duels.get('best_nodebuff_winstreak', 0),
            }

    return winstreaks


def create_figures(players_data, historical_data=None):
    """Create all chart figures for the dashboard."""
    figures_data = {}

    # Generate figures for all game modes
    for mode_id, mode_config in GAME_MODES.items():
        figures_data[mode_id] = create_figure_for_mode(mode_id, mode_config, players_data)

    # Add combined figure
    figures_data['combined'] = create_combined_figure(players_data)

    # Extract winstreaks
    figures_data['winstreaks'] = extract_winstreaks(players_data)

    return figures_data
