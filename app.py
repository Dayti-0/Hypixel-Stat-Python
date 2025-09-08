import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import os
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
from dotenv import load_dotenv

from api import get_uuid, get_hypixel_stats, get_player_history
from stats import get_duel_stats, create_figures

# Charger les variables d'environnement
load_dotenv()

# Utiliser la variable d'environnement pour la clé API
DEFAULT_API_KEY = os.getenv('HYPIXEL_API_KEY', '')

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
            html.Div(
                dbc.Button(
                    "Paramètres",
                    id="collapse-button",
                    color="primary",
                    n_clicks=0,
                    className="mb-3"
                )
            ),
            dbc.Collapse(
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Noms d'utilisateurs Minecraft (séparés par des virgules):"),
                        dcc.Input(id='usernames-input', value='', type='text', className="form-control", style={'marginBottom': '10px'}),
                        html.Label("Clé API Hypixel:"),
                        html.Div(
                            [
                                dcc.Input(
                                    id="api-key-input",
                                    value=DEFAULT_API_KEY,
                                    type="text",
                                    className="form-control me-2"
                                ),
                                dbc.Button(
                                    "Obtenir une clé",
                                    href="https://developer.hypixel.net/dashboard",
                                    target="_blank",
                                    color="secondary"
                                ),
                            ],
                            className="d-flex mb-3"
                        ),
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
    [State("collapse", "is_open")]
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
        return [dash.no_update] * 9 + ["\n".join(errors), {'display': 'block'}, None]

    if not players_data:
        return [dash.no_update] * 9 + ["Aucune donnée valide trouvée pour les joueurs spécifiés.", {'display': 'block'}, None]

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
