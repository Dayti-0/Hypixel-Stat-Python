import plotly.graph_objects as go


# Fonction pour obtenir les statistiques détaillées des duels

def get_duel_stats(player_data, duel_type):
    if not player_data or "stats" not in player_data or "Duels" not in player_data["stats"]:
        return {}

    duels = player_data["stats"]["Duels"]

    # Clés pour chaque type de duel spécifique
    duel_keys = {
        "SUMO": "sumo_duel",
        "CLASSIC": "classic_duel"
    }

    # Extraire les statistiques du type de duel spécifique
    key = duel_keys.get(duel_type.upper())
    if key:
        stats = {
            'wins': duels.get(f'{key}_wins', 0),
            'games_played': duels.get(f'{key}_rounds_played', 0),
            'kills': duels.get(f'{key}_kills', 0),
            'deaths': duels.get(f'{key}_deaths', 0)
        }
        return stats
    return {}


# Fonction pour créer les figures

def create_figures(players_data, historical_data):
    fig_bedwars = go.Figure()
    fig_bedwars_4v4 = go.Figure()
    fig_duels = go.Figure()
    fig_sumo_duel = go.Figure()
    fig_classic_duel = go.Figure()
    fig_skywars = go.Figure()
    fig_combined = go.Figure()

    colors = ['#4e73df', '#1cc88a', '#e74a3b', '#f6c23e', '#36b9cc', '#6610f2', '#fd7e14', '#6f42c1', '#20c9a6', '#e83e8c']

    winstreaks_text = {}  # Dictionnaire pour stocker les meilleurs winstreaks par joueur

    for i, (username, player) in enumerate(players_data.items()):
        color = colors[i % len(colors)]

        # Statistiques Bedwars
        if "stats" in player and "Bedwars" in player["stats"]:
            bedwars = player["stats"]["Bedwars"]

            fig_bedwars.add_trace(go.Bar(
                x=['Victoires', 'Parties jouées', 'Éliminations', 'Morts', 'Lits détruits'],
                y=[bedwars.get('wins_bedwars', 0),
                   bedwars.get('games_played_bedwars', 0),
                   bedwars.get('kills_bedwars', 0),
                   bedwars.get('deaths_bedwars', 0),
                   bedwars.get('beds_broken_bedwars', 0)],
                name=f'{username} - Bedwars',
                marker_color=color
            ))

            fig_bedwars_4v4.add_trace(go.Bar(
                x=['Victoires 4v4', 'Parties jouées 4v4', 'Éliminations 4v4', 'Morts 4v4', 'Lits détruits 4v4'],
                y=[bedwars.get('two_four_wins_bedwars', 0),
                   bedwars.get('two_four_games_played_bedwars', 0),
                   bedwars.get('two_four_kills_bedwars', 0),
                   bedwars.get('two_four_deaths_bedwars', 0),
                   bedwars.get('two_four_beds_broken_bedwars', 0)],
                name=f'{username} - Bedwars 4v4',
                marker_color=color
            ))

        # Statistiques Duels
        if "stats" in player and "Duels" in player["stats"]:
            duels = player["stats"]["Duels"]
            fig_duels.add_trace(go.Bar(
                x=['Victoires', 'Parties jouées', 'Éliminations', 'Morts'],
                y=[duels.get('wins', 0),
                   duels.get('rounds_played', 0),  # Mise à jour de la clé pour les parties jouées
                   duels.get('kills', 0),
                   duels.get('deaths', 0)],
                name=f'{username} - Duels',
                marker_color=color
            ))

            # Ajouter Meilleur Winstreak Classic et Sumo sous forme de texte
            best_classic_winstreak = duels.get('best_classic_winstreak', 0)
            best_sumo_winstreak = duels.get('best_sumo_winstreak', 0)
            winstreaks_text[username] = {
                'classic': best_classic_winstreak,
                'sumo': best_sumo_winstreak
            }

            # Statistiques spécifiques pour "Sumo Duel"
            sumo_stats = get_duel_stats(player, "SUMO")
            if sumo_stats:
                fig_sumo_duel.add_trace(go.Bar(
                    x=['Victoires', 'Parties jouées', 'Éliminations', 'Morts'],
                    y=[sumo_stats.get('wins', 0),
                       sumo_stats.get('games_played', 0),
                       sumo_stats.get('kills', 0),
                       sumo_stats.get('deaths', 0)],
                    name=f'{username} - Sumo Duel',
                    marker_color=color
                ))

            # Statistiques spécifiques pour "Classic Duel"
            classic_stats = get_duel_stats(player, "CLASSIC")
            if classic_stats:
                fig_classic_duel.add_trace(go.Bar(
                    x=['Victoires', 'Parties jouées', 'Éliminations', 'Morts'],
                    y=[classic_stats.get('wins', 0),
                       classic_stats.get('games_played', 0),
                       classic_stats.get('kills', 0),
                       classic_stats.get('deaths', 0)],
                    name=f'{username} - Classic Duel',
                    marker_color=color
                ))

        # Statistiques Skywars
        if "stats" in player and "SkyWars" in player["stats"]:
            skywars = player["stats"]["SkyWars"]
            fig_skywars.add_trace(go.Bar(
                x=['Victoires', 'Parties jouées', 'Éliminations', 'Morts'],
                y=[skywars.get('wins', 0),
                   skywars.get('games_played_skywars', 0),
                   skywars.get('kills', 0),
                   skywars.get('deaths', 0)],
                name=f'{username} - Skywars',
                marker_color=color
            ))

        # Statistiques combinées (exclure Sumo, Classic Duels, et Bedwars 4v4)
        combined_wins = bedwars.get('wins_bedwars', 0) + duels.get('wins', 0) + skywars.get('wins', 0)
        combined_games = (
            bedwars.get('games_played_bedwars', 0) +  # Parties jouées Bedwars
            duels.get('rounds_played', 0) +  # Parties jouées Duels
            skywars.get('games_played_skywars', 0)  # Parties jouées Skywars
        )
        combined_kills = bedwars.get('kills_bedwars', 0) + duels.get('kills', 0) + skywars.get('kills', 0)
        combined_deaths = bedwars.get('deaths_bedwars', 0) + duels.get('deaths', 0) + skywars.get('deaths', 0)

        fig_combined.add_trace(go.Bar(
            x=['Victoires', 'Parties jouées', 'Éliminations', 'Morts'],
            y=[combined_wins, combined_games, combined_kills, combined_deaths],
            name=f'{username} - Combiné',
            marker_color=color
        ))

    # Mise en page des graphiques
    for fig in [fig_bedwars, fig_bedwars_4v4, fig_duels, fig_skywars, fig_combined, fig_sumo_duel, fig_classic_duel]:
        fig.update_layout(barmode='group')

    fig_bedwars.update_layout(title="Statistiques Bedwars")
    fig_bedwars_4v4.update_layout(title="Statistiques Bedwars 4v4")
    fig_duels.update_layout(title="Statistiques Duels")
    fig_sumo_duel.update_layout(title="Statistiques Sumo Duel")
    fig_classic_duel.update_layout(title="Statistiques Classic Duel")
    fig_skywars.update_layout(title="Statistiques Skywars")
    fig_combined.update_layout(title="Statistiques Combinées (Sans Bedwars 4v4)")

    return fig_bedwars, fig_bedwars_4v4, fig_duels, fig_sumo_duel, fig_classic_duel, fig_skywars, fig_combined, winstreaks_text
