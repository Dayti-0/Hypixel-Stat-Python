import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

from api import get_hypixel_stats, get_player_history
from stats import create_figures
from config.game_modes import GAME_MODES, MENU_SECTIONS
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
from components.sidebar import get_all_mode_ids, get_section_ids

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
        dcc.Store(id='mode-store', data='duels_general'),
        dcc.Store(id='expanded-sections-store', data=[]),

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
                            style={'height': '400px'},
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


# Callback: Toggle section expand/collapse
@app.callback(
    [Output(f'{section_id}-submodes', 'style') for section_id in MENU_SECTIONS.keys()] +
    [Output(f'{section_id}-header', 'className') for section_id in MENU_SECTIONS.keys()],
    [Input(f'{section_id}-header', 'n_clicks') for section_id in MENU_SECTIONS.keys()],
    [State(f'{section_id}-submodes', 'style') for section_id in MENU_SECTIONS.keys()],
    prevent_initial_call=True,
)
def toggle_sections(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    n_sections = len(MENU_SECTIONS)
    clicks = args[:n_sections]
    current_styles = args[n_sections:]

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Create output lists
    new_styles = []
    new_classes = []

    for i, section_id in enumerate(MENU_SECTIONS.keys()):
        header_id = f'{section_id}-header'
        current_style = current_styles[i] or {}
        is_visible = current_style.get('display') != 'none'

        if header_id == triggered_id:
            # Toggle this section
            if is_visible:
                new_styles.append({'display': 'none'})
                new_classes.append('section-header')
            else:
                new_styles.append({'display': 'block'})
                new_classes.append('section-header expanded')
        else:
            # Keep current state
            new_styles.append(current_style)
            new_classes.append('section-header expanded' if is_visible else 'section-header')

    return new_styles + new_classes


# Callback: Update mode from sidebar submodes or combined
@app.callback(
    Output('mode-store', 'data'),
    [Input(f'{mode_id}-item', 'n_clicks') for mode_id in GAME_MODES.keys()] +
    [Input('combined-item', 'n_clicks')],
    prevent_initial_call=True,
)
def update_mode(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    mode_id = triggered_id.replace('-item', '')

    if mode_id in GAME_MODES or mode_id == 'combined':
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

    # Create figures
    figures = create_figures(players_data, historical_data)

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

    return figures, players_store, message, None


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

    # Handle winstreak display for duel modes
    winstreak_content = None
    winstreaks = figures_data.get('winstreaks', {})

    # Map mode IDs to winstreak keys
    winstreak_mode_map = {
        'sumo_duel': 'sumo',
        'classic_duel': 'classic',
        'op_duel': 'op',
        'uhc_duel': 'uhc',
        'bridge_duel': 'bridge',
        'skywars_duel': 'skywars',
        'blitz_duel': 'blitz',
        'bow_duel': 'bow',
        'boxing_duel': 'boxing',
        'combo_duel': 'combo',
        'nodebuff_duel': 'nodebuff',
    }

    if mode in winstreak_mode_map and winstreaks:
        ws_key = winstreak_mode_map[mode]
        winstreak_items = []
        for username, ws_data in winstreaks.items():
            ws_value = ws_data.get(ws_key, 0)
            if ws_value > 0:
                winstreak_items.append(
                    html.Div(
                        [
                            html.Span('🔥', className='winstreak-icon'),
                            html.Span(f'{username}:', className='winstreak-label'),
                            html.Span(str(ws_value), className='winstreak-value'),
                        ],
                        className='winstreak-badge',
                    )
                )
        if winstreak_items:
            mode_name = GAME_MODES.get(mode, {}).get('name', mode)
            winstreak_content = html.Div(
                [html.Span(f'Meilleur Winstreak {mode_name}', style={'marginRight': '15px', 'color': '#718096'})] + winstreak_items,
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


# Callback: Highlight active submode item
@app.callback(
    [Output(f'{mode_id}-item', 'className') for mode_id in GAME_MODES.keys()] +
    [Output('combined-item', 'className')],
    Input('mode-store', 'data'),
)
def update_active_menu(current_mode):
    classes = []
    for mode_id in GAME_MODES.keys():
        if mode_id == current_mode:
            classes.append('submode-item active')
        else:
            classes.append('submode-item')

    # Combined item
    if current_mode == 'combined':
        classes.append('section-header combined-item active')
    else:
        classes.append('section-header combined-item')

    return classes


if __name__ == '__main__':
    app.run_server(debug=True)
