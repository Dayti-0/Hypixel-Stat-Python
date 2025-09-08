import requests
import json
from datetime import datetime, timedelta


def get_uuid(username):
    """Retrieve the Minecraft UUID for a given username."""
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if response.status_code == 200:
        return json.loads(response.text).get("id")
    return None


def get_hypixel_stats(api_key, username):
    """Fetch Hypixel stats for the given username using the provided API key."""
    uuid = get_uuid(username)
    if not uuid:
        return None, f"Joueur Minecraft non trouvé : {username}"

    response = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}")
    data = json.loads(response.text)

    if not data["success"]:
        return None, data.get("cause", "Erreur inconnue")

    player_data = data.get("player")
    if player_data:
        player_data['uuid'] = uuid  # Ajouter l'UUID aux données du joueur
    return player_data, None


def get_player_history(api_key, uuid, stat_type, time_period):
    """Retrieve historical statistics for a player over a given time period."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=time_period)

    url = (
        f"https://api.hypixel.net/player/statistics?key={api_key}&uuid={uuid}"
        f"&type={stat_type}&startDate={start_date.isoformat()}&endDate={end_date.isoformat()}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return None


if __name__ == "__main__":
    # Minimal test when running this module directly
    test_username = "Notch"
    print("UUID for", test_username, ":", get_uuid(test_username))
