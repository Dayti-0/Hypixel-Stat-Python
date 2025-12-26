from dash import html
import dash_bootstrap_components as dbc
from config.game_modes import GAME_CATEGORIES, GAME_MODES


def create_sidebar():
    """Create the navigation sidebar with game mode items organized by category."""
    accordion_items = []

    # Create accordion items for each game category
    for category_id, category in GAME_CATEGORIES.items():
        # Create sub-menu items for each mode in the category
        mode_items = []
        for mode_id, mode_config in category['modes'].items():
            mode_items.append(
                html.Div(
                    mode_config['name'],
                    id=f'{mode_id}-item',
                    className='submenu-item',
                    n_clicks=0,
                    **{'data-mode': mode_id},
                )
            )

        # Create accordion item for this category
        accordion_items.append(
            dbc.AccordionItem(
                html.Div(mode_items, className='submenu-items'),
                title=html.Div([
                    html.Span(category['icon'], className='accordion-icon'),
                    html.Span(category['name'], className='accordion-label'),
                ], className='accordion-title'),
                item_id=category_id,
            )
        )

    # Add Combined view as a separate menu item (not in accordion)
    combined_item = html.Div(
        [
            html.Span('📊', className='menu-icon'),
            html.Span('Combiné', className='menu-label'),
        ],
        id='combined-item',
        className='menu-item combined-menu-item',
        n_clicks=0,
        **{'data-mode': 'combined'},
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
            html.Div(
                [
                    dbc.Accordion(
                        accordion_items,
                        id='game-modes-accordion',
                        start_collapsed=False,
                        always_open=True,
                        className='game-modes-accordion',
                    ),
                    combined_item,
                ],
                className='menu-items',
            ),
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
