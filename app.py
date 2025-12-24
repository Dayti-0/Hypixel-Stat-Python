import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

from api import get_hypixel_stats, get_player_history
from stats import create_figures
from config.game_modes import GAME_MODES
from config.theme import CHART_LAYOUT
from components import (
    create_sidebar,
    create_header,
    create_stats_cards,
    create_empty_state,
    create_settings_panel,
)
from components.header import create_player_info, create_mode_indicator
from components.settings_panel import create_error_message, create_success_message

# Load environment variables
load_dotenv()
DEFAULT_API_KEY = os.getenv('HYPIXEL_API_KEY', '')

# Create Dash application
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Application layout
app.layout = html.Div(
    [
        # Data stores
        dcc.Store(id='figures-store'),
        dcc.Store(id='players-store'),
        dcc.Store(id='mode-store', data='bedwars_overall'),

        # Sidebar navigation
        create_sidebar(),

        # Main content area
        html.Div(
            [
                create_header(),
                create_settings_panel(DEFAULT_API_KEY),
                html.Div(id='mode-indicator'),
                html.Div(id='stats-cards', children=create_empty_state()),
                html.Div(
                    [
                        dcc.Graph(
                            id='stats-graph',
                            config={'displayModeBar': False},
                            style={'height': '600px'},
                        ),
                    ],
                    id='chart-container',
                    className='chart-container',
                    style={'display': 'none'},
                ),
                html.Div(id='winstreak-info', className='winstreak-info'),
            ],
            className='main-content',
        ),
    ],
)


# Callback: Toggle settings panel
@app.callback(
    Output('settings-collapse', 'is_open'),
    Input('settings-toggle', 'n_clicks'),
    State('settings-collapse', 'is_open'),
    prevent_initial_call=True,
)
def toggle_settings(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


# Callback: Update mode from sidebar
@app.callback(
    Output('mode-store', 'data'),
    [Input(f'{mode_id}-item', 'n_clicks') for mode_id in GAME_MODES.keys()],
    prevent_initial_call=True,
)
def update_mode(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    mode_id = triggered_id.replace('-item', '')

    if mode_id in GAME_MODES:
        return mode_id

    raise PreventUpdate


# Callback: Fetch player data
@app.callback(
    [
        Output('figures-store', 'data'),
        Output('players-store', 'data'),
        Output('result-message', 'children'),
        Output('loading-output', 'children'),
    ],
    Input('fetch-button', 'n_clicks'),
    [
        State('usernames-input', 'value'),
        State('api-key-input', 'value'),
    ],
    prevent_initial_call=True,
)
def fetch_player_data(n_clicks, usernames, api_key):
    if not n_clicks:
        raise PreventUpdate

    if not usernames or not usernames.strip():
        return dash.no_update, dash.no_update, create_error_message('Veuillez entrer au moins un nom de joueur.'), None

    if not api_key or not api_key.strip():
        return dash.no_update, dash.no_update, create_error_message('Veuillez entrer votre clé API Hypixel.'), None

    usernames_list = [u.strip() for u in usernames.split(',') if u.strip()]
    players_data = {}
    errors = []

    for username in usernames_list:
        player, error = get_hypixel_stats(api_key, username)
        if error:
            errors.append(f'{username}: {error}')
        elif not player:
            errors.append(f'{username}: Aucune donnée trouvée')
        else:
            players_data[player.get('displayname', username)] = player

    if errors and not players_data:
        return dash.no_update, dash.no_update, create_error_message(' | '.join(errors)), None

    if not players_data:
        return dash.no_update, dash.no_update, create_error_message('Aucune donnée valide trouvée.'), None

    # Fetch historical data
    historical_data = {}
    for username, player in players_data.items():
        uuid = player.get('uuid')
        if uuid:
            history = get_player_history(api_key, uuid, 'BEDWARS', 30)
            if history:
                historical_data[username] = history.get('data')

    # Create figures - now returns a dictionary
    figures_data = create_figures(players_data, historical_data)

    # Prepare players data for storage (simplified)
    players_store = {
        username: {
            'displayname': player.get('displayname', username),
            'uuid': player.get('uuid'),
            'stats': player.get('stats', {}),
        }
        for username, player in players_data.items()
    }

    message = create_success_message(f'Données chargées pour {len(players_data)} joueur(s).')
    if errors:
        message = html.Div([
            create_success_message(f'Données chargées pour {len(players_data)} joueur(s).'),
            create_error_message(' | '.join(errors)),
        ])

    return figures_data, players_store, message, None


# Callback: Update display based on mode and data
@app.callback(
    [
        Output('stats-cards', 'children'),
        Output('stats-graph', 'figure'),
        Output('chart-container', 'style'),
        Output('mode-indicator', 'children'),
        Output('winstreak-info', 'children'),
        Output('player-info', 'children'),
    ],
    [
        Input('mode-store', 'data'),
        Input('players-store', 'data'),
    ],
    State('figures-store', 'data'),
)
def update_display(mode, players_data, figures_data):
    # Default empty figure
    empty_figure = {
        'data': [],
        'layout': {
            **CHART_LAYOUT,
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'Aucune donnée disponible',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#718096'},
            }],
        },
    }

    # If no data, show empty state
    if not players_data or not figures_data:
        return (
            create_empty_state(),
            empty_figure,
            {'display': 'none'},
            None,
            None,
            None,
        )

    # Create stats cards
    stats_cards = create_stats_cards(players_data, mode)

    # Get figure for current mode
    figure = figures_data.get(mode, empty_figure)
    if figure:
        # Apply dark theme to figure
        if isinstance(figure, dict) and 'layout' in figure:
            figure['layout'].update(CHART_LAYOUT)

    # Create mode indicator
    mode_indicator = create_mode_indicator(mode)

    # Create player info badges
    player_info = create_player_info(players_data)

    # Handle winstreak display
    winstreak_content = None
    winstreaks = figures_data.get('winstreaks', {})

    if mode == 'duel_sumo' and winstreaks:
        winstreak_items = []
        for username, ws_data in winstreaks.items():
            sumo_ws = ws_data.get('sumo', 0)
            winstreak_items.append(
                html.Div(
                    [
                        html.Span('🔥', className='winstreak-icon'),
                        html.Span(f'{username}:', className='winstreak-label'),
                        html.Span(str(sumo_ws), className='winstreak-value'),
                    ],
                    className='winstreak-badge',
                )
            )
        if winstreak_items:
            winstreak_content = html.Div(
                [html.Span('Meilleur Winstreak Sumo', style={'marginRight': '15px', 'color': '#718096'})] + winstreak_items,
                style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '10px'},
            )

    elif mode == 'duel_classic' and winstreaks:
        winstreak_items = []
        for username, ws_data in winstreaks.items():
            classic_ws = ws_data.get('classic', 0)
            winstreak_items.append(
                html.Div(
                    [
                        html.Span('🔥', className='winstreak-icon'),
                        html.Span(f'{username}:', className='winstreak-label'),
                        html.Span(str(classic_ws), className='winstreak-value'),
                    ],
                    className='winstreak-badge',
                )
            )
        if winstreak_items:
            winstreak_content = html.Div(
                [html.Span('Meilleur Winstreak Classic', style={'marginRight': '15px', 'color': '#718096'})] + winstreak_items,
                style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '10px'},
            )

    return (
        stats_cards,
        figure if figure else empty_figure,
        {'display': 'block'},
        mode_indicator,
        winstreak_content,
        player_info,
    )


# Callback: Highlight active menu item
@app.callback(
    [Output(f'{mode_id}-item', 'className') for mode_id in GAME_MODES.keys()],
    Input('mode-store', 'data'),
)
def update_active_menu(current_mode):
    classes = []
    for mode_id in GAME_MODES.keys():
        config = GAME_MODES[mode_id]
        if config.get('is_combined'):
            # Combined is a top-level menu item
            base_class = 'menu-item combined-menu-item'
            classes.append(f'{base_class} active' if mode_id == current_mode else base_class)
        else:
            # All other modes are submenu items
            base_class = 'submenu-item'
            classes.append(f'{base_class} active' if mode_id == current_mode else base_class)
    return classes


if __name__ == '__main__':
    app.run_server(debug=True)
