import json
import os
import requests
from datetime import datetime

# Configuration
API_URL = "https://v3.football.api-sports.io"
API_KEY = os.getenv("API_FOOTBALL_KEY")
TEAM_ID = 2501  # AD Mérida
LEAGUE_ID = 431 # Primera Federación - Group 2 (Typical for Merida)
SEASON = 2025

DATA_DIR = "docs/data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_data(endpoint, params):
    if not API_KEY:
        return None
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": API_KEY
    }
    try:
        response = requests.get(f"{API_URL}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return None

def save_json(name, data):
    with open(os.path.join(DATA_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_mock_data():
    print("Generating realistic mock data...")
    
    # Mock Fixtures
    fixtures = {
        "response": [
            {
                "fixture": {"date": "2026-04-05T18:00:00+00:00", "status": {"short": "FT"}},
                "teams": {"home": {"name": "AD Mérida", "winner": True}, "away": {"name": "Alcoyano", "winner": False}},
                "goals": {"home": 2, "away": 1}
            },
            {
                "fixture": {"date": "2026-04-12T12:00:00+00:00", "status": {"short": "FT"}},
                "teams": {"home": {"name": "Ibiza", "winner": False}, "away": {"name": "AD Mérida", "winner": True}},
                "goals": {"home": 0, "away": 1}
            },
            {
                "fixture": {"date": "2026-04-19T17:00:00+00:00", "status": {"short": "NS"}},
                "teams": {"home": {"name": "AD Mérida"}, "away": {"name": "Castellón"}},
                "goals": {"home": None, "away": None}
            }
        ]
    }
    
    # Mock Standings
    standings = {
        "response": [{
            "league": {
                "standings": [[
                    {"rank": 1, "team": {"name": "Castellón", "id": 1}, "points": 65, "goalsDiff": 20, "group": "Group 2"},
                    {"rank": 2, "team": {"name": "Ibiza", "id": 2}, "points": 62, "goalsDiff": 15},
                    {"rank": 6, "team": {"name": "AD Mérida", "id": 2501}, "points": 48, "goalsDiff": 5},
                    {"rank": 18, "team": {"name": "At. Baleares", "id": 4}, "points": 25, "goalsDiff": -15}
                ]]
            }
        }]
    }
    
    # Mock Players
    players = {
        "response": [
            {"player": {"name": "Cacharrón", "age": 27, "number": 1, "pos": "Goalkeeper"}},
            {"player": {"name": "Lancho", "age": 23, "number": 4, "pos": "Defender"}},
            {"player": {"name": "Martín Solar", "age": 24, "number": 10, "pos": "Midfielder"}},
            {"player": {"name": "Chiqui", "age": 26, "number": 7, "pos": "Forward"}}
        ]
    }
    
    save_json("fixtures", fixtures)
    save_json("standings", standings)
    save_json("players", players)

def get_news():
    # News is not in API-Football, using hardcoded latest relevant news
    news = [
        {
            "title": "El Romano se prepara para el partidazo ante el Castellón",
            "source": "Mérida AD",
            "date": "2026-04-12",
            "url": "#"
        },
        {
            "title": "Victoria clave en Ibiza para soñar con el Play-off",
            "source": "Hoy.es",
            "date": "2026-04-10",
            "url": "#"
        },
        {
            "title": "El equipo entrena a puerta cerrada antes de la jornada 32",
            "source": "Canal Extremadura",
            "date": "2026-04-09",
            "url": "#"
        }
    ]
    save_json("news", news)

def main():
    metadata = {
        "last_updated": datetime.now().isoformat(),
        "status": "success"
    }

    if not API_KEY:
        generate_mock_data()
        metadata["mode"] = "mock"
    else:
        print("Fetching real data from API-Football...")
        # Fixtures
        fixtures = fetch_data("fixtures", {"team": TEAM_ID, "season": SEASON, "last": 10})
        if fixtures: save_json("fixtures", fixtures)
        
        # Standings
        standings = fetch_data("standings", {"league": LEAGUE_ID, "season": SEASON})
        if standings: save_json("standings", standings)
        
        # Players
        players = fetch_data("players", {"team": TEAM_ID, "season": SEASON})
        if players: save_json("players", players)
        
        metadata["mode"] = "real"

    get_news()
    save_json("metadata", metadata)
    print(f"Data update complete. Mode: {metadata['mode']}")

if __name__ == "__main__":
    main()
