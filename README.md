# Hypixel Stats

Tableau de bord local pour **comparer des joueurs Hypixel** en Bed Wars, SkyWars et Duels :
ratios (FK/D, W/L, K/D, BB/L…), volumes, winstreaks, mode par mode, avec le meilleur
joueur surligné sur chaque ligne.

- Profils : rang, niveau réseau, étoiles Bed Wars, niveau SkyWars, karma, dernière connexion
- Bed Wars : Global, Solo, Doubles, 3v3v3v3, 4v4v4v4, 4v4
- SkyWars : Global, Solo, Équipe, Mini, Mega, Laboratoire, Ranked, Insane
- Duels : Global, Classic, UHC, SkyWars, Bridge, Sumo, OP, Combo, Bow, Bow Spleef, Boxing,
  NoDebuff, Mega Walls, Blitz, Bed Wars, Parkour
- Jusqu'à 8 joueurs à la fois, récupérés en parallèle et mis en cache 2 minutes

## Démarrage rapide

**Windows** : double-cliquez sur `run.bat` (il crée l'environnement virtuel, installe les
dépendances puis lance l'application).

**Ailleurs** (Python 3.10+) :

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

L'application s'ouvre sur <http://127.0.0.1:8050/>. Entrez un ou plusieurs pseudos
(séparés par des virgules ou des espaces), votre clé API, puis **Comparer**.

## Clé API Hypixel

Créez une clé sur <https://developer.hypixel.net/dashboard>. Deux façons de la fournir :

1. la coller dans le champ de l'interface (elle reste uniquement dans votre navigateur) ;
2. ou la mettre dans un fichier `.env` (copiez `.env.example`) — le champ peut alors rester vide :

```
HYPIXEL_API_KEY=votre-cle
```

## Options

```bash
python main.py --port 8080 --no-browser
```

| Option / variable | Rôle | Défaut |
| --- | --- | --- |
| `--host` / `HOST` | adresse d'écoute | `127.0.0.1` |
| `--port` / `PORT` | port | `8050` |
| `--debug` | mode debug Dash | désactivé |
| `--no-browser` | ne pas ouvrir le navigateur | — |
| `CACHE_TTL` | durée du cache par joueur (s) | `120` |
| `REQUEST_TIMEOUT` | délai max d'une requête (s) | `10` |
| `MAX_PLAYERS` | joueurs max par comparaison | `8` |

## Structure

```
main.py                     point d'entrée (CLI)
hypixel_stats/
  api.py                    client HTTP Hypixel v2 + Mojang, cache, erreurs
  games.py                  registre déclaratif des jeux, modes et métriques
  parser.py                 JSON brut Hypixel -> PlayerProfile
  models.py                 modèles de données et calcul des ratios
  levels.py                 niveau réseau, étoiles Bed Wars, niveau SkyWars, rangs
  settings.py               configuration (variables d'environnement / .env)
  dashboard/
    app.py                  fabrique de l'application Dash
    layout.py               squelette de la page
    callbacks.py            interactions
    components.py           cartes, tableaux, vues
    charts.py               graphiques Plotly
    assets/style.css        thème
tests/                      tests pytest (API simulée, aucune clé nécessaire)
```

### Ajouter un mode

Chaque mode associe une métrique aux clés brutes de l'API. Par exemple, dans `games.py` :

```python
_duels_mode("classic", "Classic", ("classic_duel",), "classic"),
```

lit `classic_duel_wins`, `classic_duel_losses`, `classic_duel_kills`… et les winstreaks
`best_winstreak_mode_classic_duel` / `best_classic_winstreak`. Les comptes de plusieurs
sous-modes sont additionnés, les winstreaks prennent le maximum.

## Tests

```bash
pip install -r requirements-dev.txt
```

```bash
pytest
```

---

Projet non affilié à Hypixel Inc. Avatars fournis par mc-heads.net.
