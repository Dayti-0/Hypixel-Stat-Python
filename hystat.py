import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import requests
import json
import os
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import webbrowser  # Importez le module webbrowser

# Charger les variables d'environnement
load_dotenv()

# Utiliser la variable d'environnement pour la clé API
DEFAULT_API_KEY = os.getenv('HYPIXEL_API_KEY', '')

# Fonction pour obtenir l'UUID Minecraft
def get_uuid(username):
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if response.status_code == 200:
        return json.loads(response.text).get("id")
    return None

# Fonction pour obtenir les statistiques Hypixel
def get_hypixel_stats(api_key, username):
    uuid = get_uuid(username)
    if not uuid:
        return None, f"Joueur Minecraft non trouvé : {username}"
    
    response = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}")
    data = json.loads(response.text)
    
    if not data["success"]:
        return None, data.get("cause", "Erreur inconnue")
    
    player_data = data.get("player")
    if player_data:
        player_data['uuid'] = uuid  # Ajouter l'UUID aux données du joueur
    return player_data, None

# Nouvelle fonction pour récupérer l'historique des statistiques
def get_player_history(api_key, uuid, stat_type, time_period):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=time_period)
    
    url = f"https://api.hypixel.net/player/statistics?key={api_key}&uuid={uuid}&type={stat_type}&startDate={start_date.isoformat()}&endDate={end_date.isoformat()}"
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return None

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

# Créer l'application Dash avec le thème Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Tableau de bord des statistiques Hypixel", className="text-center mb-4")
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Tabs(id='tabs', children=[
                dcc.Tab(label='Bedwars Stats', children=[
                    dcc.Graph(id='bedwars-graph')
                ]),
                dcc.Tab(label='Bedwars 4v4 Stats', children=[
                    dcc.Graph(id='bedwars-4v4-graph')
                ]),
                dcc.Tab(label='Skywars Stats', children=[
                    dcc.Graph(id='skywars-graph')
                ]),
                dcc.Tab(label='Duels Stats', children=[
                    dcc.Graph(id='duels-graph')
                ]),
                dcc.Tab(label='Sumo Duel Stats', children=[
                    dcc.Graph(id='sumo-duel-graph'),
                    html.Div(id='sumo-winstreak', className='mt-4')
                ]),
                dcc.Tab(label='Classic Duel Stats', children=[
                    dcc.Graph(id='classic-duel-graph'),
                    html.Div(id='classic-winstreak', className='mt-4')
                ]),
                dcc.Tab(label='Statistiques Combinées', children=[
                    dcc.Graph(id='combined-graph')
                ])
            ], className="custom-tabs-container")
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Button(
                "Paramètres", id="collapse-button", color="primary", n_clicks=0, className="mb-3"
            ),
            dbc.Collapse(
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Noms d'utilisateurs Minecraft (séparés par des virgules):"),
                        dcc.Input(id='usernames-input', value='', type='text', className="form-control", style={'marginBottom': '10px'}),
                        html.Label("Clé API Hypixel:"),
                        dcc.Input(id='api-key-input', value=DEFAULT_API_KEY, type='text', className="form-control", style={'marginBottom': '10px'}),
                        dbc.Button('Obtenir les statistiques', id='fetch-button', color="primary", className="btn-block"),
                        html.Div(id='result', className="alert alert-info mt-4", style={'display': 'none'}),
                        dcc.Loading(
                            id="loading",
                            type="default",
                            children=html.Div(id="loading-output")
                        )
                    ])
                ]),
                id="collapse",
                is_open=False,
            )
        ], width=12)
    ])
], fluid=True)

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output('bedwars-graph', 'figure'),
     Output('bedwars-4v4-graph', 'figure'),
     Output('duels-graph', 'figure'),
     Output('sumo-duel-graph', 'figure'),
     Output('classic-duel-graph', 'figure'),
     Output('skywars-graph', 'figure'),
     Output('combined-graph', 'figure'),
     Output('sumo-winstreak', 'children'),
     Output('classic-winstreak', 'children'),
     Output('result', 'children'),
     Output('result', 'style'),
     Output('loading-output', 'children')],
    [Input('fetch-button', 'n_clicks')],
    [State('usernames-input', 'value'),
     State('api-key-input', 'value')]
)
def update_graphs(n_clicks, usernames, api_key):
    if not n_clicks:
        raise PreventUpdate

    usernames_list = [username.strip() for username in usernames.split(',') if username.strip()]
    
    players_data = {}
    errors = []

    for username in usernames_list:
        player, error = get_hypixel_stats(api_key, username)
        if error:
            errors.append(f"{username}: {error}")
        elif not player:
            errors.append(f"{username}: Aucune donnée trouvée")
        else:
            players_data[player.get('displayname', username)] = player
    
    if errors:
        return [dash.no_update] * 10 + ["\n".join(errors), {'display': 'block'}, None]

    if not players_data:
        return [dash.no_update] * 10 + ["Aucune donnée valide trouvée pour les joueurs spécifiés.", {'display': 'block'}, None]

    historical_data = {}
    for username, player in players_data.items():
        uuid = player['uuid']
        history = get_player_history(api_key, uuid, 'BEDWARS', 30)  # Example period for historical data
        if history:
            historical_data[username] = history['data']

    fig_bedwars, fig_bedwars_4v4, fig_duels, fig_sumo_duel, fig_classic_duel, fig_skywars, fig_combined, winstreaks_text = create_figures(players_data, historical_data)
    
    # Mise à jour du texte des winstreaks avec le format désiré
    sumo_winstreak_text = "Meilleur Winstreak Sumo : " + " --- ".join([f"{user} : {winstreaks_text[user]['sumo']}" for user in winstreaks_text])
    classic_winstreak_text = "Meilleur Winstreak Classic : " + " --- ".join([f"{user} : {winstreaks_text[user]['classic']}" for user in winstreaks_text])
    
    return fig_bedwars, fig_bedwars_4v4, fig_duels, fig_sumo_duel, fig_classic_duel, fig_skywars, fig_combined, sumo_winstreak_text, classic_winstreak_text, "Données récupérées et graphiques mis à jour.", {'display': 'block'}, None

if __name__ == '__main__':
    # Ouvrir le lien dans le navigateur une seule fois
    webbrowser.open("http://127.0.0.1:8050/")
    
    # Démarrer le serveur Dash sans recharger automatiquement
    app.run_server(debug=True, use_reloader=False)

