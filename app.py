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
    dcc.Store(id='figures-store'),
    dcc.Store(id='mode-store', data='bedwars'),
    html.Div(
        id='side-menu',
        children=[
            html.Div('Bedwars Stats', id='bedwars-item', className='menu-item', n_clicks=0),
            html.Div('Bedwars 4v4 Stats', id='bedwars_4v4-item', className='menu-item', n_clicks=0),
            html.Div('Skywars Stats', id='skywars-item', className='menu-item', n_clicks=0),
            html.Div('Duels Stats', id='duels-item', className='menu-item', n_clicks=0),
            html.Div('Sumo Duel Stats', id='sumo_duel-item', className='menu-item', n_clicks=0),
            html.Div('Classic Duel Stats', id='classic_duel-item', className='menu-item', n_clicks=0),
            html.Div('Statistiques Combinées', id='combined-item', className='menu-item', n_clicks=0),
        ],
    ),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H1("Tableau de bord des statistiques Hypixel", className="text-center mb-4")
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='stats-graph'),
                html.Div(id='winstreak-info', className='mt-4')
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                html.Div(
                    [
                        dbc.Button(
                            "Paramètres",
                            id="collapse-button",
                            color="primary",
                            n_clicks=0,
                            className="mb-3",
                        ),
                        dbc.Button(
                            "Obtenir une clé",
                            id="api-link-button",
                            href="https://developer.hypixel.net/dashboard",
                            target="_blank",
                            color="secondary",
                            className="mb-3 ms-2",
                            style={"display": "none"},
                        ),
                    ],
                    className="d-flex",
                ),
                dbc.Collapse(
                    dbc.Card([
                        dbc.CardBody([
                            html.Label("Noms d'utilisateurs Minecraft (séparés par des virgules):"),
                            dcc.Input(id='usernames-input', value='', type='text', className="form-control", style={'marginBottom': '10px'}),
                            html.Label("Clé API Hypixel:"),
                            dcc.Input(
                                id="api-key-input",
                                value=DEFAULT_API_KEY,
                                type="text",
                                className="form-control mb-3",
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
    ], className='content')
], fluid=True)

@app.callback(
    [Output("collapse", "is_open"), Output("api-link-button", "style")],
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")]
)
def toggle_collapse(n, is_open):
    if n:
        new_is_open = not is_open
        style = {"display": "inline-block"} if new_is_open else {"display": "none"}
        return new_is_open, style
    return is_open, {"display": "none"}

@app.callback(
    [Output('figures-store', 'data'),
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
        return dash.no_update, "\n".join(errors), {'display': 'block'}, None

    if not players_data:
        return dash.no_update, "Aucune donnée valide trouvée pour les joueurs spécifiés.", {'display': 'block'}, None

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

    figures_data = {
        'bedwars': fig_bedwars,
        'bedwars_4v4': fig_bedwars_4v4,
        'duels': fig_duels,
        'sumo_duel': fig_sumo_duel,
        'classic_duel': fig_classic_duel,
        'skywars': fig_skywars,
        'combined': fig_combined,
        'sumo_winstreak': sumo_winstreak_text,
        'classic_winstreak': classic_winstreak_text,
    }

    return figures_data, "Données récupérées et graphiques mis à jour.", {'display': 'block'}, None


@app.callback(
    Output('mode-store', 'data'),
    [
        Input('bedwars-item', 'n_clicks'),
        Input('bedwars_4v4-item', 'n_clicks'),
        Input('skywars-item', 'n_clicks'),
        Input('duels-item', 'n_clicks'),
        Input('sumo_duel-item', 'n_clicks'),
        Input('classic_duel-item', 'n_clicks'),
        Input('combined-item', 'n_clicks'),
    ],
    prevent_initial_call=True
)
def update_mode(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    mapping = {
        'bedwars-item': 'bedwars',
        'bedwars_4v4-item': 'bedwars_4v4',
        'skywars-item': 'skywars',
        'duels-item': 'duels',
        'sumo_duel-item': 'sumo_duel',
        'classic_duel-item': 'classic_duel',
        'combined-item': 'combined',
    }
    return mapping.get(triggered_id, dash.no_update)


@app.callback(
    [Output('stats-graph', 'figure'), Output('winstreak-info', 'children')],
    [Input('mode-store', 'data')],
    [State('figures-store', 'data')]
)
def display_selected_graph(mode, data):
    if not data or mode not in data:
        raise PreventUpdate

    figure = data.get(mode)
    winstreak = None
    if mode == 'sumo_duel':
        winstreak = data.get('sumo_winstreak')
    elif mode == 'classic_duel':
        winstreak = data.get('classic_winstreak')

    return figure, winstreak
