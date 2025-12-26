# Hypixel Stat Python

Cette application Dash permet de consulter les statistiques des joueurs sur Hypixel via un tableau de bord interactif.

## Installation

```bash
pip install -r requirements.txt
```

Ou installez les dépendances manuellement :

```bash
pip install dash dash-bootstrap-components plotly python-dotenv hypixel.py
```

**Note importante:** Si vous avez plusieurs versions de Python installées, utilisez `python -m pip` pour vous assurer d'installer dans le bon environnement :

```bash
python -m pip install -r requirements.txt
```

## Exécution

1. Installez les dépendances ci-dessus.
2. Lancez l'application :

```bash
python main.py
```

3. Lorsque l'interface s'ouvre, saisissez votre clé API Hypixel.

Le serveur démarrera sur [http://127.0.0.1:8050/](http://127.0.0.1:8050/) et s'ouvrira automatiquement dans votre navigateur.
