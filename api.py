import asyncio
import sys

try:
    import hypixel
except ImportError:
    print("=" * 60)
    print("ERREUR: Le module 'hypixel' n'est pas installé.")
    print()
    print("Pour installer la bibliothèque requise, exécutez:")
    print("    pip install hypixel.py")
    print()
    print("Si vous avez plusieurs versions de Python, utilisez:")
    print("    python -m pip install hypixel.py")
    print()
    print("Ou avec Python 3 explicitement:")
    print("    python3 -m pip install hypixel.py")
    print("=" * 60)
    sys.exit(1)


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


def _extract_bedwars_stats(player):
    """Extract all Bedwars stats including all game modes."""
    bedwars = player.bedwars

    return {
        # Overall stats
        'wins_bedwars': bedwars.wins,
        'games_played_bedwars': bedwars.games,
        'kills_bedwars': bedwars.kills,
        'deaths_bedwars': bedwars.deaths,
        'beds_broken_bedwars': bedwars.beds_broken,
        'final_kills_bedwars': bedwars.final_kills,
        'final_deaths_bedwars': bedwars.final_deaths,
        'winstreak': bedwars.winstreak if bedwars.winstreak is not None else 0,

        # Solo (8v8 -> 1v1v1v1v1v1v1v1)
        'eight_one_wins_bedwars': bedwars.solo.wins,
        'eight_one_games_played_bedwars': bedwars.solo.games,
        'eight_one_kills_bedwars': bedwars.solo.kills,
        'eight_one_deaths_bedwars': bedwars.solo.deaths,
        'eight_one_beds_broken_bedwars': bedwars.solo.beds_broken,

        # Doubles (8v8 -> 2v2v2v2)
        'eight_two_wins_bedwars': bedwars.doubles.wins,
        'eight_two_games_played_bedwars': bedwars.doubles.games,
        'eight_two_kills_bedwars': bedwars.doubles.kills,
        'eight_two_deaths_bedwars': bedwars.doubles.deaths,
        'eight_two_beds_broken_bedwars': bedwars.doubles.beds_broken,

        # 3v3v3v3 (4 teams of 3)
        'four_three_wins_bedwars': bedwars.threes.wins,
        'four_three_games_played_bedwars': bedwars.threes.games,
        'four_three_kills_bedwars': bedwars.threes.kills,
        'four_three_deaths_bedwars': bedwars.threes.deaths,
        'four_three_beds_broken_bedwars': bedwars.threes.beds_broken,

        # 4v4v4v4 (4 teams of 4)
        'four_four_wins_bedwars': bedwars.fours.wins,
        'four_four_games_played_bedwars': bedwars.fours.games,
        'four_four_kills_bedwars': bedwars.fours.kills,
        'four_four_deaths_bedwars': bedwars.fours.deaths,
        'four_four_beds_broken_bedwars': bedwars.fours.beds_broken,

        # 4v4 (2 teams of 4)
        'two_four_wins_bedwars': bedwars.teams.wins,
        'two_four_games_played_bedwars': bedwars.teams.games,
        'two_four_kills_bedwars': bedwars.teams.kills,
        'two_four_deaths_bedwars': bedwars.teams.deaths,
        'two_four_beds_broken_bedwars': bedwars.teams.beds_broken,
    }


def _extract_skywars_stats(player):
    """Extract all Skywars stats including all game modes."""
    skywars = player.skywars

    return {
        # Overall stats
        'wins': skywars.wins,
        'games_played_skywars': skywars.games,
        'kills': skywars.kills,
        'deaths': skywars.deaths,
        'winstreak': skywars.winstreak if skywars.winstreak is not None else 0,

        # Ranked
        'ranked_wins': skywars.ranked.wins,
        'ranked_games': skywars.ranked.games,
        'ranked_kills': skywars.ranked.kills,
        'ranked_deaths': skywars.ranked.deaths,

        # Solo Normal
        'solo_normal_wins': skywars.solo_normal.wins,
        'solo_normal_games': skywars.solo_normal.games,
        'solo_normal_kills': skywars.solo_normal.kills,
        'solo_normal_deaths': skywars.solo_normal.deaths,

        # Solo Insane
        'solo_insane_wins': skywars.solo_insane.wins,
        'solo_insane_games': skywars.solo_insane.games,
        'solo_insane_kills': skywars.solo_insane.kills,
        'solo_insane_deaths': skywars.solo_insane.deaths,

        # Team Normal
        'team_normal_wins': skywars.team_normal.wins,
        'team_normal_games': skywars.team_normal.games,
        'team_normal_kills': skywars.team_normal.kills,
        'team_normal_deaths': skywars.team_normal.deaths,

        # Team Insane
        'team_insane_wins': skywars.team_insane.wins,
        'team_insane_games': skywars.team_insane.games,
        'team_insane_kills': skywars.team_insane.kills,
        'team_insane_deaths': skywars.team_insane.deaths,

        # Mega (combining mega_normal and mega_doubles)
        'mega_wins': skywars.mega_normal.wins + skywars.mega_doubles.wins,
        'mega_games': skywars.mega_normal.games + skywars.mega_doubles.games,
        'mega_kills': skywars.mega_normal.kills + skywars.mega_doubles.kills,
        'mega_deaths': skywars.mega_normal.deaths + skywars.mega_doubles.deaths,
    }


def _extract_duels_stats(player):
    """Extract all Duels stats including all duel types."""
    duels = player.duels

    # List of all duel types to extract
    duel_types = [
        'classic', 'bow', 'bowspleef', 'boxing', 'bridge', 'combo',
        'mega_walls', 'nodebuff', 'op', 'potion', 'skywars', 'sumo', 'uhc'
    ]

    stats = {
        # Overall stats
        'wins': duels.wins,
        'rounds_played': duels.wins + duels.losses,
        'kills': duels.kills,
        'deaths': duels.deaths,
    }

    # Extract stats for each duel type
    for duel_type in duel_types:
        prefix = f'{duel_type}_duel'
        stats[f'{prefix}_wins'] = duels._data.get(f'{prefix}_wins', 0)
        stats[f'{prefix}_losses'] = duels._data.get(f'{prefix}_losses', 0)
        stats[f'{prefix}_rounds_played'] = (
            duels._data.get(f'{prefix}_wins', 0) +
            duels._data.get(f'{prefix}_losses', 0)
        )
        stats[f'{prefix}_kills'] = duels._data.get(f'{prefix}_kills', 0)
        stats[f'{prefix}_deaths'] = duels._data.get(f'{prefix}_deaths', 0)
        stats[f'best_{duel_type}_winstreak'] = duels._data.get(f'best_{duel_type}_winstreak', 0)

    return stats


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
            'Bedwars': _extract_bedwars_stats(player),
            'SkyWars': _extract_skywars_stats(player),
            'Duels': _extract_duels_stats(player),
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
