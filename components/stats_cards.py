from dash import html
from config.game_modes import GAME_MODES, get_mode_stats, compute_stats
from config.theme import THEME


def create_stats_cards(players_data, mode_id):
    """Create stat cards for the selected game mode."""
    if not players_data or mode_id not in GAME_MODES:
        return create_empty_state()

    config = GAME_MODES[mode_id]

    # For combined stats, show aggregated view
    if config.get('is_combined'):
        return create_combined_cards(players_data)

    cards = []

    for username, player in players_data.items():
        raw_stats = get_mode_stats(player, mode_id)
        computed = compute_stats(raw_stats, mode_id)

        # Create individual stat items
        stat_items = []

        # Main stats - dynamically create from available raw_stats
        stat_keys = [
            ('wins', 'Victoires', '🏆'),
            ('games', 'Parties', '🎮'),
            ('kills', 'Éliminations', '🗡️'),
            ('deaths', 'Morts', '💀'),
            ('beds_broken', 'Lits détruits', '🛏️'),
            ('final_kills', 'Final Kills', '⚡'),
        ]

        for key, label, icon in stat_keys[:4]:  # Show first 4 available stats
            if key in raw_stats:
                value = raw_stats[key]
                stat_items.append(
                    html.Div(
                        [
                            html.Span(icon, className='stat-icon'),
                            html.Div(
                                [
                                    html.Span(f'{value:,}', className='stat-value'),
                                    html.Span(label, className='stat-label'),
                                ],
                                className='stat-text',
                            ),
                        ],
                        className='stat-item',
                    )
                )

        # Computed stats (KDR, Win Rate)
        computed_items = []
        for stat_id, stat_data in computed.items():
            computed_items.append(
                html.Div(
                    [
                        html.Span(stat_data['display'], className='computed-value'),
                        html.Span(stat_data['label'], className='computed-label'),
                    ],
                    className='computed-item',
                )
            )

        cards.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=f'https://mc-heads.net/avatar/{username}/48',
                                className='card-avatar',
                            ),
                            html.Div(
                                [
                                    html.H3(username, className='card-username'),
                                    html.Span(config['name'], className='card-mode'),
                                ],
                                className='card-header-text',
                            ),
                        ],
                        className='card-header',
                    ),
                    html.Div(stat_items, className='stats-grid'),
                    html.Div(computed_items, className='computed-stats'),
                ],
                className='stat-card',
                style={'borderTopColor': config.get('color', '#6366f1')},
            )
        )

    return html.Div(cards, className='stats-cards-container')


def create_combined_cards(players_data):
    """Create cards for combined stats view."""
    cards = []

    for username, player in players_data.items():
        total_wins = 0
        total_games = 0
        total_kills = 0
        total_deaths = 0

        # Aggregate from Bedwars
        if 'Bedwars' in player.get('stats', {}):
            bw = player['stats']['Bedwars']
            total_wins += bw.get('wins_bedwars', 0)
            total_games += bw.get('games_played_bedwars', 0)
            total_kills += bw.get('kills_bedwars', 0)
            total_deaths += bw.get('deaths_bedwars', 0)

        # Aggregate from Duels
        if 'Duels' in player.get('stats', {}):
            duels = player['stats']['Duels']
            total_wins += duels.get('wins', 0)
            total_games += duels.get('rounds_played', 0)
            total_kills += duels.get('kills', 0)
            total_deaths += duels.get('deaths', 0)

        # Aggregate from Skywars
        if 'SkyWars' in player.get('stats', {}):
            sw = player['stats']['SkyWars']
            total_wins += sw.get('wins', 0)
            total_games += sw.get('games_played_skywars', 0)
            total_kills += sw.get('kills', 0)
            total_deaths += sw.get('deaths', 0)

        kdr = round(total_kills / total_deaths, 2) if total_deaths > 0 else 0
        win_rate = round((total_wins / total_games) * 100, 1) if total_games > 0 else 0

        cards.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=f'https://mc-heads.net/avatar/{username}/48',
                                className='card-avatar',
                            ),
                            html.Div(
                                [
                                    html.H3(username, className='card-username'),
                                    html.Span('Stats Combin\u00e9es', className='card-mode'),
                                ],
                                className='card-header-text',
                            ),
                        ],
                        className='card-header',
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span('\U0001f3c6', className='stat-icon'),
                                    html.Div(
                                        [
                                            html.Span(f'{total_wins:,}', className='stat-value'),
                                            html.Span('Victoires', className='stat-label'),
                                        ],
                                        className='stat-text',
                                    ),
                                ],
                                className='stat-item',
                            ),
                            html.Div(
                                [
                                    html.Span('\U0001f3ae', className='stat-icon'),
                                    html.Div(
                                        [
                                            html.Span(f'{total_games:,}', className='stat-value'),
                                            html.Span('Parties', className='stat-label'),
                                        ],
                                        className='stat-text',
                                    ),
                                ],
                                className='stat-item',
                            ),
                            html.Div(
                                [
                                    html.Span('\U0001f5e1\ufe0f', className='stat-icon'),
                                    html.Div(
                                        [
                                            html.Span(f'{total_kills:,}', className='stat-value'),
                                            html.Span('\u00c9liminations', className='stat-label'),
                                        ],
                                        className='stat-text',
                                    ),
                                ],
                                className='stat-item',
                            ),
                            html.Div(
                                [
                                    html.Span('\U0001f480', className='stat-icon'),
                                    html.Div(
                                        [
                                            html.Span(f'{total_deaths:,}', className='stat-value'),
                                            html.Span('Morts', className='stat-label'),
                                        ],
                                        className='stat-text',
                                    ),
                                ],
                                className='stat-item',
                            ),
                        ],
                        className='stats-grid',
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(f'{kdr}', className='computed-value'),
                                    html.Span('K/D Ratio', className='computed-label'),
                                ],
                                className='computed-item',
                            ),
                            html.Div(
                                [
                                    html.Span(f'{win_rate}%', className='computed-value'),
                                    html.Span('Win Rate', className='computed-label'),
                                ],
                                className='computed-item',
                            ),
                        ],
                        className='computed-stats',
                    ),
                ],
                className='stat-card',
                style={'borderTopColor': '#4caf50'},
            )
        )

    return html.Div(cards, className='stats-cards-container')


def create_empty_state():
    """Create an empty state placeholder when no data is available."""
    return html.Div(
        [
            html.Div('\U0001f50d', className='empty-icon'),
            html.H2('Aucune donn\u00e9e', className='empty-title'),
            html.P(
                'Entrez des noms de joueurs et votre cl\u00e9 API pour voir les statistiques.',
                className='empty-description',
            ),
            html.Div(
                [
                    html.Span('1', className='step-number'),
                    html.Span('Cliquez sur Param\u00e8tres', className='step-text'),
                ],
                className='empty-step',
            ),
            html.Div(
                [
                    html.Span('2', className='step-number'),
                    html.Span('Entrez les noms de joueurs', className='step-text'),
                ],
                className='empty-step',
            ),
            html.Div(
                [
                    html.Span('3', className='step-number'),
                    html.Span('Ajoutez votre cl\u00e9 API Hypixel', className='step-text'),
                ],
                className='empty-step',
            ),
        ],
        className='empty-state',
    )
