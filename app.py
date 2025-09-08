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

app.layout = html.Div([
    html.Div(
        dbc.Nav(
            [
                dbc.NavLink("Bedwars", id="nav-bedwars", active=True),
                dbc.NavLink("Bedwars 4v4", id="nav-bedwars4v4"),
                dbc.NavLink("Duels", id="nav-duels"),
                dbc.NavLink("Sumo Duel", id="nav-sumo"),
                dbc.NavLink("Classic Duel", id="nav-classic"),
                dbc.NavLink("Skywars", id="nav-skywars"),
                dbc.NavLink("Combinées", id="nav-combined"),
            ],
            vertical=True,
            pills=True,
        ),
        className="sidebar",
    ),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Tableau de bord des statistiques Hypixel", className="text-center mb-4")
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                html.Div(dcc.Graph(id='bedwars-graph'), id='content-bedwars'),
                html.Div(dcc.Graph(id='bedwars-4v4-graph'), id='content-bedwars4v4', style={'display': 'none'}),
                html.Div(dcc.Graph(id='duels-graph'), id='content-duels', style={'display': 'none'}),
                html.Div([
                    dcc.Graph(id='sumo-duel-graph'),
                    html.Div(id='sumo-winstreak', className='mt-4')
                ], id='content-sumo', style={'display': 'none'}),
                html.Div([
                    dcc.Graph(id='classic-duel-graph'),
                    html.Div(id='classic-winstreak', className='mt-4')
                ], id='content-classic', style={'display': 'none'}),
                html.Div(dcc.Graph(id='skywars-graph'), id='content-skywars', style={'display': 'none'}),
                html.Div(dcc.Graph(id='combined-graph'), id='content-combined', style={'display': 'none'}),
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
    ], fluid=True, className="content")
])

@app.callback(
    [Output('content-bedwars', 'style'),
     Output('content-bedwars4v4', 'style'),
     Output('content-duels', 'style'),
     Output('content-sumo', 'style'),
     Output('content-classic', 'style'),
     Output('content-skywars', 'style'),
     Output('content-combined', 'style'),
     Output('nav-bedwars', 'active'),
     Output('nav-bedwars4v4', 'active'),
     Output('nav-duels', 'active'),
     Output('nav-sumo', 'active'),
     Output('nav-classic', 'active'),
     Output('nav-skywars', 'active'),
     Output('nav-combined', 'active')],
    [Input('nav-bedwars', 'n_clicks'),
     Input('nav-bedwars4v4', 'n_clicks'),
     Input('nav-duels', 'n_clicks'),
     Input('nav-sumo', 'n_clicks'),
     Input('nav-classic', 'n_clicks'),
     Input('nav-skywars', 'n_clicks'),
     Input('nav-combined', 'n_clicks')]
)
def display_content(n1, n2, n3, n4, n5, n6, n7):
    ctx = dash.callback_context
    if not ctx.triggered:
        selected = 'nav-bedwars'
    else:
        selected = ctx.triggered[0]['prop_id'].split('.')[0]

    style_show = {'display': 'block'}
    style_hide = {'display': 'none'}

    styles = [
        style_show if selected == 'nav-bedwars' else style_hide,
        style_show if selected == 'nav-bedwars4v4' else style_hide,
        style_show if selected == 'nav-duels' else style_hide,
        style_show if selected == 'nav-sumo' else style_hide,
        style_show if selected == 'nav-classic' else style_hide,
        style_show if selected == 'nav-skywars' else style_hide,
        style_show if selected == 'nav-combined' else style_hide,
    ]

    actives = [
        selected == 'nav-bedwars',
        selected == 'nav-bedwars4v4',
        selected == 'nav-duels',
        selected == 'nav-sumo',
        selected == 'nav-classic',
        selected == 'nav-skywars',
        selected == 'nav-combined',
    ]

    return styles + actives

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

