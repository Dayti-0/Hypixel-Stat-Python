from dash import html, dcc
from config.game_modes import GAME_MODES, MENU_SECTIONS


def create_sidebar():
    """Create the navigation sidebar with collapsible sections and submodes."""
    sections_list = []

    for section_id, section in MENU_SECTIONS.items():
        # Create submodes list for this section
        submodes_items = []
        for mode_id in section['submodes']:
            if mode_id in GAME_MODES:
                mode_config = GAME_MODES[mode_id]
                submodes_items.append(
                    html.Div(
                        [
                            html.Span(mode_config['icon'], className='submode-icon'),
                            html.Span(mode_config['name'], className='submode-label'),
                        ],
                        id=f'{mode_id}-item',
                        className='submode-item',
                        n_clicks=0,
                        **{'data-mode': mode_id, 'data-section': section_id},
                    )
                )

        # Create the section with header and collapsible content
        section_element = html.Div(
            [
                # Section header (clickable to expand/collapse)
                html.Div(
                    [
                        html.Span(section['icon'], className='section-icon'),
                        html.Span(section['name'], className='section-label'),
                        html.Span('▼', className='section-arrow'),
                    ],
                    id=f'{section_id}-header',
                    className='section-header',
                    n_clicks=0,
                    style={'borderLeftColor': section['color']},
                ),
                # Submodes container (collapsible)
                html.Div(
                    submodes_items,
                    id=f'{section_id}-submodes',
                    className='submodes-container',
                    style={'display': 'none'},  # Initially collapsed
                ),
            ],
            className='menu-section',
            id=f'{section_id}-section',
        )
        sections_list.append(section_element)

    # Add "Combined Stats" as a special item at the bottom
    sections_list.append(
        html.Div(
            [
                html.Span('📊', className='section-icon'),
                html.Span('Stats Combinées', className='section-label'),
            ],
            id='combined-item',
            className='section-header combined-item',
            n_clicks=0,
            style={'borderLeftColor': '#6366f1', 'marginTop': '10px'},
        )
    )

    return html.Div(
        [
            # Logo
            html.Div(
                [
                    html.Div('H', className='logo-letter'),
                    html.Span('Hypixel Stats', className='logo-text'),
                ],
                className='sidebar-logo',
            ),
            # Menu sections
            html.Div(sections_list, className='menu-sections'),
            # Store for tracking expanded sections
            dcc.Store(id='expanded-sections-store', data=[]),
        ],
        id='sidebar',
        className='sidebar',
    )


def get_all_mode_ids():
    """Return all mode IDs including combined."""
    return list(GAME_MODES.keys()) + ['combined']


def get_section_ids():
    """Return all section IDs."""
    return list(MENU_SECTIONS.keys())


def get_sidebar_callbacks_inputs():
    """Return the list of Input objects for sidebar menu items."""
    from dash.dependencies import Input
    inputs = [Input(f'{mode_id}-item', 'n_clicks') for mode_id in GAME_MODES.keys()]
    inputs.append(Input('combined-item', 'n_clicks'))
    return inputs


def get_section_header_inputs():
    """Return the list of Input objects for section headers."""
    from dash.dependencies import Input
    return [Input(f'{section_id}-header', 'n_clicks') for section_id in MENU_SECTIONS.keys()]


def get_mode_from_trigger(triggered_id):
    """Extract mode ID from the triggered element ID."""
    if triggered_id and '-item' in triggered_id:
        return triggered_id.replace('-item', '')
    return None
