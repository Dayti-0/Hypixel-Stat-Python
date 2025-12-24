import asyncio
import hypixel


# Global client instance (will be initialized with API key)
_client = None


def init_client(api_key):
    """Initialize the hypixel.py client with the API key."""
    global _client
    _client = hypixel.Client(api_key)


async def _get_player_async(username):
    """Internal async function to get player data."""
    if _client is None:
        raise ValueError("Client not initialized. Call init_client() first.")

    async with _client:
        try:
            player = await _client.player(username)
            return player, None
        except Exception as e:
            return None, str(e)


def get_hypixel_stats(api_key, username):
    """
    Fetch Hypixel stats for the given username using the provided API key.

    This is a synchronous wrapper around the async hypixel.py library.
    Returns (player_data_dict, error_message).
    """
    # Initialize client with API key
    init_client(api_key)

    # Run async function
    player, error = asyncio.run(_get_player_async(username))

    if error:
        return None, f"Erreur API: {error}"

    if not player:
        return None, f"Joueur non trouvé: {username}"

    # Convert player object to a dictionary format compatible with existing code
    player_data = {
        'uuid': player.uuid,
        'displayname': player.name,
        'stats': {
            'Bedwars': {
                # Overall stats
                'wins_bedwars': player.bedwars.wins,
                'games_played_bedwars': player.bedwars.games,
                'kills_bedwars': player.bedwars.kills,
                'deaths_bedwars': player.bedwars.deaths,
                'beds_broken_bedwars': player.bedwars.beds_broken,
                'final_kills_bedwars': player.bedwars.final_kills,
                'final_deaths_bedwars': player.bedwars.final_deaths,
                'winstreak': player.bedwars.winstreak if player.bedwars.winstreak is not None else 0,

                # 4v4 specific stats
                'two_four_wins_bedwars': player.bedwars.fours.wins,
                'two_four_games_played_bedwars': player.bedwars.fours.games,
                'two_four_kills_bedwars': player.bedwars.fours.kills,
                'two_four_deaths_bedwars': player.bedwars.fours.deaths,
                'two_four_beds_broken_bedwars': player.bedwars.fours.beds_broken,
            },
            'SkyWars': {
                'wins': player.skywars.wins,
                'games_played_skywars': player.skywars.games,
                'kills': player.skywars.kills,
                'deaths': player.skywars.deaths,
                'winstreak': player.skywars.winstreak if player.skywars.winstreak is not None else 0,
            },
            'Duels': {
                'wins': player.duels.wins,
                'rounds_played': player.duels.wins + player.duels.losses,  # Approximation
                'kills': player.duels.kills,
                'deaths': player.duels.deaths,

                # Access mode-specific stats from raw data
                'sumo_duel_wins': player.duels._data.get('sumo_duel_wins', 0),
                'sumo_duel_rounds_played': (
                    player.duels._data.get('sumo_duel_wins', 0) +
                    player.duels._data.get('sumo_duel_losses', 0)
                ),
                'sumo_duel_kills': player.duels._data.get('sumo_duel_kills', 0),
                'sumo_duel_deaths': player.duels._data.get('sumo_duel_deaths', 0),
                'best_sumo_winstreak': player.duels._data.get('best_sumo_winstreak', 0),

                'classic_duel_wins': player.duels._data.get('classic_duel_wins', 0),
                'classic_duel_rounds_played': (
                    player.duels._data.get('classic_duel_wins', 0) +
                    player.duels._data.get('classic_duel_losses', 0)
                ),
                'classic_duel_kills': player.duels._data.get('classic_duel_kills', 0),
                'classic_duel_deaths': player.duels._data.get('classic_duel_deaths', 0),
                'best_classic_winstreak': player.duels._data.get('best_classic_winstreak', 0),
            }
        },
        # Store the raw player object for future use
        '_raw_player': player,
    }

    return player_data, None


def get_player_history(api_key, uuid, stat_type, time_period):
    """
    Retrieve historical statistics for a player over a given time period.

    Note: hypixel.py doesn't provide historical data endpoint.
    This function is kept for compatibility but returns None.
    Historical data would need to be tracked separately.
    """
    # The Hypixel API doesn't actually have a historical endpoint like this
    # This was likely placeholder code in the original implementation
    return None


if __name__ == "__main__":
    # Test the API
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv('HYPIXEL_API_KEY')

    if api_key:
        test_username = "Technoblade"
        print(f"Fetching stats for {test_username}...")
        player_data, error = get_hypixel_stats(api_key, test_username)

        if error:
            print(f"Error: {error}")
        else:
            print(f"Player: {player_data['displayname']}")
            print(f"Bedwars wins: {player_data['stats']['Bedwars']['wins_bedwars']}")
            print(f"Skywars wins: {player_data['stats']['SkyWars']['wins']}")
            print(f"Duels wins: {player_data['stats']['Duels']['wins']}")
    else:
        print("No API key found. Set HYPIXEL_API_KEY in .env file")
