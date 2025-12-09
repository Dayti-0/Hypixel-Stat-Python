from dash import html
from config.game_modes import GAME_MODES
from config.theme import THEME


def create_sidebar():
    """Create the navigation sidebar with game mode items."""
    menu_items = []

    for mode_id, config in GAME_MODES.items():
        menu_items.append(
            html.Div(
                [
                    html.Span(config['icon'], className='menu-icon'),
                    html.Span(config['name'], className='menu-label'),
                ],
                id=f'{mode_id}-item',
                className='menu-item',
                n_clicks=0,
                **{'data-mode': mode_id},
            )
        )

    return html.Div(
        [
            html.Div(
                [
                    html.Div('H', className='logo-letter'),
                    html.Span('Hypixel Stats', className='logo-text'),
                ],
                className='sidebar-logo',
            ),
            html.Div(menu_items, className='menu-items'),
        ],
        id='sidebar',
        className='sidebar',
    )


def get_sidebar_callbacks_inputs():
    """Return the list of Input objects for sidebar menu items."""
    from dash.dependencies import Input
    return [Input(f'{mode_id}-item', 'n_clicks') for mode_id in GAME_MODES.keys()]


def get_mode_from_trigger(triggered_id):
    """Extract mode ID from the triggered element ID."""
    if triggered_id and '-item' in triggered_id:
        return triggered_id.replace('-item', '')
    return None
