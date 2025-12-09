import plotly.graph_objects as go
from config.theme import CHART_COLORS, CHART_LAYOUT


def get_duel_stats(player_data, duel_type):
    """Extract statistics for a specific duel type from player data."""
    if not player_data or "stats" not in player_data or "Duels" not in player_data["stats"]:
        return {}

    duels = player_data["stats"]["Duels"]

    duel_keys = {
        "SUMO": "sumo_duel",
        "CLASSIC": "classic_duel"
    }

    key = duel_keys.get(duel_type.upper())
    if key:
        return {
            'wins': duels.get(f'{key}_wins', 0),
            'games_played': duels.get(f'{key}_rounds_played', 0),
            'kills': duels.get(f'{key}_kills', 0),
            'deaths': duels.get(f'{key}_deaths', 0)
        }
    return {}


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


def create_figures(players_data, historical_data):
    """Create all chart figures for the dashboard."""
    fig_bedwars = go.Figure()
    fig_bedwars_4v4 = go.Figure()
    fig_duels = go.Figure()
    fig_sumo_duel = go.Figure()
    fig_classic_duel = go.Figure()
    fig_skywars = go.Figure()
    fig_combined = go.Figure()

    winstreaks_text = {}

    for i, (username, player) in enumerate(players_data.items()):
        color = CHART_COLORS[i % len(CHART_COLORS)]

        # Initialize default stats
        bedwars = {}
        duels = {}
        skywars = {}

        # Bedwars stats
        if "stats" in player and "Bedwars" in player["stats"]:
            bedwars = player["stats"]["Bedwars"]

            fig_bedwars.add_trace(go.Bar(
                x=['Victoires', 'Parties', 'Éliminations', 'Morts', 'Lits'],
                y=[
                    bedwars.get('wins_bedwars', 0),
                    bedwars.get('games_played_bedwars', 0),
                    bedwars.get('kills_bedwars', 0),
                    bedwars.get('deaths_bedwars', 0),
                    bedwars.get('beds_broken_bedwars', 0)
                ],
                name=username,
                marker_color=color,
                marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
            ))

            fig_bedwars_4v4.add_trace(go.Bar(
                x=['Victoires', 'Parties', 'Éliminations', 'Morts', 'Lits'],
                y=[
                    bedwars.get('two_four_wins_bedwars', 0),
                    bedwars.get('two_four_games_played_bedwars', 0),
                    bedwars.get('two_four_kills_bedwars', 0),
                    bedwars.get('two_four_deaths_bedwars', 0),
                    bedwars.get('two_four_beds_broken_bedwars', 0)
                ],
                name=username,
                marker_color=color,
                marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
            ))

        # Duels stats
        if "stats" in player and "Duels" in player["stats"]:
            duels = player["stats"]["Duels"]

            fig_duels.add_trace(go.Bar(
                x=['Victoires', 'Parties', 'Éliminations', 'Morts'],
                y=[
                    duels.get('wins', 0),
                    duels.get('rounds_played', 0),
                    duels.get('kills', 0),
                    duels.get('deaths', 0)
                ],
                name=username,
                marker_color=color,
                marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
            ))

            # Store winstreaks
            winstreaks_text[username] = {
                'classic': duels.get('best_classic_winstreak', 0),
                'sumo': duels.get('best_sumo_winstreak', 0)
            }

            # Sumo Duel stats
            sumo_stats = get_duel_stats(player, "SUMO")
            if sumo_stats:
                fig_sumo_duel.add_trace(go.Bar(
                    x=['Victoires', 'Parties', 'Éliminations', 'Morts'],
                    y=[
                        sumo_stats.get('wins', 0),
                        sumo_stats.get('games_played', 0),
                        sumo_stats.get('kills', 0),
                        sumo_stats.get('deaths', 0)
                    ],
                    name=username,
                    marker_color=color,
                    marker_line_width=0,
                    hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
                ))

            # Classic Duel stats
            classic_stats = get_duel_stats(player, "CLASSIC")
            if classic_stats:
                fig_classic_duel.add_trace(go.Bar(
                    x=['Victoires', 'Parties', 'Éliminations', 'Morts'],
                    y=[
                        classic_stats.get('wins', 0),
                        classic_stats.get('games_played', 0),
                        classic_stats.get('kills', 0),
                        classic_stats.get('deaths', 0)
                    ],
                    name=username,
                    marker_color=color,
                    marker_line_width=0,
                    hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
                ))

        # Skywars stats
        if "stats" in player and "SkyWars" in player["stats"]:
            skywars = player["stats"]["SkyWars"]

            fig_skywars.add_trace(go.Bar(
                x=['Victoires', 'Parties', 'Éliminations', 'Morts'],
                y=[
                    skywars.get('wins', 0),
                    skywars.get('games_played_skywars', 0),
                    skywars.get('kills', 0),
                    skywars.get('deaths', 0)
                ],
                name=username,
                marker_color=color,
                marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
            ))

        # Combined stats
        combined_wins = (
            bedwars.get('wins_bedwars', 0) +
            duels.get('wins', 0) +
            skywars.get('wins', 0)
        )
        combined_games = (
            bedwars.get('games_played_bedwars', 0) +
            duels.get('rounds_played', 0) +
            skywars.get('games_played_skywars', 0)
        )
        combined_kills = (
            bedwars.get('kills_bedwars', 0) +
            duels.get('kills', 0) +
            skywars.get('kills', 0)
        )
        combined_deaths = (
            bedwars.get('deaths_bedwars', 0) +
            duels.get('deaths', 0) +
            skywars.get('deaths', 0)
        )

        fig_combined.add_trace(go.Bar(
            x=['Victoires', 'Parties', 'Éliminations', 'Morts'],
            y=[combined_wins, combined_games, combined_kills, combined_deaths],
            name=username,
            marker_color=color,
            marker_line_width=0,
            hovertemplate='<b>%{x}</b><br>%{y:,}<extra></extra>',
        ))

    # Apply dark theme to all figures
    apply_dark_theme(fig_bedwars, "Statistiques Bedwars")
    apply_dark_theme(fig_bedwars_4v4, "Statistiques Bedwars 4v4")
    apply_dark_theme(fig_duels, "Statistiques Duels")
    apply_dark_theme(fig_sumo_duel, "Statistiques Sumo Duel")
    apply_dark_theme(fig_classic_duel, "Statistiques Classic Duel")
    apply_dark_theme(fig_skywars, "Statistiques Skywars")
    apply_dark_theme(fig_combined, "Statistiques Combinées")

    return (
        fig_bedwars,
        fig_bedwars_4v4,
        fig_duels,
        fig_sumo_duel,
        fig_classic_duel,
        fig_skywars,
        fig_combined,
        winstreaks_text
    )
