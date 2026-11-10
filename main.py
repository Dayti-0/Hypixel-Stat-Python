"""Point d'entrée : `python main.py [--host HOST] [--port PORT] [--debug] [--no-browser]`."""

from __future__ import annotations

import argparse
import threading
import webbrowser

from hypixel_stats.dashboard import create_app
from hypixel_stats.settings import Settings


def main() -> None:
    settings = Settings.from_env()
    parser = argparse.ArgumentParser(description="Tableau de bord des statistiques Hypixel.")
    parser.add_argument("--host", default=settings.host, help=f"adresse d'écoute (défaut : {settings.host})")
    parser.add_argument("--port", type=int, default=settings.port, help=f"port (défaut : {settings.port})")
    parser.add_argument("--debug", action="store_true", help="mode debug Dash (rechargement, outils dev)")
    parser.add_argument("--no-browser", action="store_true", help="ne pas ouvrir le navigateur")
    args = parser.parse_args()

    app = create_app(settings)
    url = f"http://{'127.0.0.1' if args.host in ('0.0.0.0', '::') else args.host}:{args.port}/"
    if not args.no_browser:
        threading.Timer(1.0, webbrowser.open, args=(url,)).start()
    print(f"Hypixel Stats disponible sur {url}")
    app.run(host=args.host, port=args.port, debug=args.debug, use_reloader=False)


if __name__ == "__main__":
    main()
