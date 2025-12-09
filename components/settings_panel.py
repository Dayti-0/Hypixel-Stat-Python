from dash import dcc, html
import dash_bootstrap_components as dbc


def create_settings_panel(default_api_key=''):
    """Create the settings panel with inputs for usernames and API key."""
    return html.Div(
        [
            # Settings toggle button
            html.Div(
                [
                    html.Button(
                        [
                            html.Span('\u2699\ufe0f', className='btn-icon'),
                            html.Span('Param\u00e8tres', className='btn-text'),
                        ],
                        id='settings-toggle',
                        className='settings-btn',
                    ),
                    html.A(
                        [
                            html.Span('\U0001f511', className='btn-icon'),
                            html.Span('Obtenir une cl\u00e9 API', className='btn-text'),
                        ],
                        id='api-link',
                        href='https://developer.hypixel.net/dashboard',
                        target='_blank',
                        className='api-link-btn',
                    ),
                ],
                className='settings-buttons',
            ),

            # Collapsible settings panel
            dbc.Collapse(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    [
                                        html.Span('\U0001f464', className='input-icon'),
                                        'Joueurs',
                                    ],
                                    className='input-label',
                                ),
                                dcc.Input(
                                    id='usernames-input',
                                    type='text',
                                    placeholder='Entrez les pseudos (s\u00e9par\u00e9s par des virgules)',
                                    className='input-field',
                                ),
                                html.Span(
                                    'Ex: Technoblade, Dream, Gamerboy80',
                                    className='input-hint',
                                ),
                            ],
                            className='input-group',
                        ),
                        html.Div(
                            [
                                html.Label(
                                    [
                                        html.Span('\U0001f511', className='input-icon'),
                                        'Cl\u00e9 API Hypixel',
                                    ],
                                    className='input-label',
                                ),
                                dcc.Input(
                                    id='api-key-input',
                                    type='password',
                                    placeholder='Votre cl\u00e9 API',
                                    value=default_api_key,
                                    className='input-field',
                                ),
                            ],
                            className='input-group',
                        ),
                        html.Button(
                            [
                                html.Span('\U0001f50d', className='btn-icon'),
                                html.Span('Charger les stats', className='btn-text'),
                            ],
                            id='fetch-button',
                            className='fetch-btn',
                        ),
                        html.Div(id='result-message', className='result-message'),
                        dcc.Loading(
                            id='loading',
                            type='circle',
                            children=html.Div(id='loading-output'),
                            color='#6366f1',
                        ),
                    ],
                    className='settings-content',
                ),
                id='settings-collapse',
                is_open=False,
            ),
        ],
        className='settings-panel',
    )


def create_error_message(message):
    """Create an error message component."""
    return html.Div(
        [
            html.Span('\u274c', className='message-icon'),
            html.Span(message, className='message-text'),
        ],
        className='error-message',
    )


def create_success_message(message):
    """Create a success message component."""
    return html.Div(
        [
            html.Span('\u2705', className='message-icon'),
            html.Span(message, className='message-text'),
        ],
        className='success-message',
    )
