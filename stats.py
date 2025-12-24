import plotly.graph_objects as go
from config.theme import CHART_COLORS, CHART_LAYOUT
from config.game_modes import get_mode_stats


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


def create_mode_figure(players_data, mode_id, mode_name):
    """Create a figure for a specific game mode."""
    fig = go.Figure()

    for i, (username, player) in enumerate(players_data.items()):
        color = CHART_COLORS[i % len(CHART_COLORS)]

        # Get stats for this mode using the new get_mode_stats function
        stats = get_mode_stats(player, mode_id)

        if not stats:
            continue

        # Determine which stats to display based on available data
        x_labels = []
        y_values = []

        if 'wins' in stats:
            x_labels.append('Victoires')
            y_values.append(stats['wins'])

        if 'games' in stats:
            x_labels.append('Parties')
            y_values.append(stats['games'])

        if 'kills' in stats:
            x_labels.append('Éliminations')
            y_values.append(stats['kills'])

        if 'deaths' in stats:
            x_labels.append('Morts')
            y_values.append(stats['deaths'])

        if 'beds_broken' in stats:
            x_labels.append('Lits détruits')
            y_values.append(stats['beds_broken'])

        if 'final_kills' in stats:
            x_labels.append('Final Kills')
            y_values.append(stats['final_kills'])

        if x_labels and y_values:
            fig.add_trace(go.Bar(
                x=x_labels,
                y=y_values,
                name=username,
                marker_color=color,
                marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
            ))

    apply_dark_theme(fig, f"Statistiques {mode_name}")
    return fig


def create_figures(players_data, historical_data):
    """
    Create all chart figures for the dashboard.
    Returns a dictionary with mode_id as keys and figures as values.
    """
    from config.game_modes import GAME_MODES

    figures = {}

    # Create a figure for each game mode
    for mode_id, mode_config in GAME_MODES.items():
        if mode_config.get('is_combined'):
            # Handle combined view separately
            figures[mode_id] = create_combined_figure(players_data)
        else:
            mode_name = mode_config.get('name', mode_id)
            figures[mode_id] = create_mode_figure(players_data, mode_id, mode_name)

    # Extract winstreaks for display
    winstreaks = extract_winstreaks(players_data)
    figures['winstreaks'] = winstreaks

    return figures


def create_combined_figure(players_data):
    """Create a combined figure showing overall stats from all games."""
    fig = go.Figure()

    for i, (username, player) in enumerate(players_data.items()):
        color = CHART_COLORS[i % len(CHART_COLORS)]

        # Get stats from each game type
        bedwars_stats = get_mode_stats(player, 'bedwars_overall')
        skywars_stats = get_mode_stats(player, 'skywars_overall')
        duels_stats = get_mode_stats(player, 'duels_overall')

        # Combine wins, games, kills, deaths
        combined_wins = (
            bedwars_stats.get('wins', 0) +
            skywars_stats.get('wins', 0) +
            duels_stats.get('wins', 0)
        )
        combined_games = (
            bedwars_stats.get('games', 0) +
            skywars_stats.get('games', 0) +
            duels_stats.get('games', 0)
        )
        combined_kills = (
            bedwars_stats.get('kills', 0) +
            skywars_stats.get('kills', 0) +
            duels_stats.get('kills', 0)
        )
        combined_deaths = (
            bedwars_stats.get('deaths', 0) +
            skywars_stats.get('deaths', 0) +
            duels_stats.get('deaths', 0)
        )

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
    """Extract winstreak data from all players."""
    winstreaks = {}

    for username, player in players_data.items():
        player_winstreaks = {}

        # Get duels data for winstreaks
        if 'stats' in player and 'Duels' in player['stats']:
            duels = player['stats']['Duels']
            player_winstreaks['sumo'] = duels.get('best_sumo_winstreak', 0)
            player_winstreaks['classic'] = duels.get('best_classic_winstreak', 0)
            player_winstreaks['bridge'] = duels.get('best_bridge_winstreak', 0)
            player_winstreaks['uhc'] = duels.get('best_uhc_winstreak', 0)

        winstreaks[username] = player_winstreaks

    return winstreaks
