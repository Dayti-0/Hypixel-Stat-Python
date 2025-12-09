from dash import html
from config.game_modes import GAME_MODES


def create_header():
    """Create the main header with title and player info area."""
    return html.Div(
        [
            html.Div(
                [
                    html.H1('Hypixel Stats', className='header-title'),
                    html.P('Tableau de bord des statistiques', className='header-subtitle'),
                ],
                className='header-text',
            ),
            html.Div(
                id='player-info',
                className='player-info',
            ),
        ],
        className='header',
    )


def create_player_info(players_data):
    """Create player info badges for the header."""
    if not players_data:
        return None

    badges = []
    for username in players_data.keys():
        badges.append(
            html.Div(
                [
                    html.Img(
                        src=f'https://mc-heads.net/avatar/{username}/32',
                        className='player-avatar',
                    ),
                    html.Span(username, className='player-name'),
                ],
                className='player-badge',
            )
        )

    return html.Div(badges, className='player-badges')


def create_mode_indicator(mode_id):
    """Create an indicator showing the current game mode."""
    config = GAME_MODES.get(mode_id, {})

    return html.Div(
        [
            html.Span(config.get('icon', ''), className='mode-icon'),
            html.Span(config.get('name', 'Unknown'), className='mode-name'),
        ],
        className='current-mode',
        style={'borderColor': config.get('color', '#6366f1')},
    )
