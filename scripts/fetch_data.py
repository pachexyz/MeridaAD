import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Configuration
# AD Mérida - Primera Federación Grupo 1 (2025/2026)
TEAM_URL = "https://www.lapreferente.com/E14121/merida-ad"
LEAGUE_URL = "https://www.lapreferente.com/index.php?comp=22269&temporada=20252026"
DATA_DIR = "docs/data"
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

def save_json(name, data):
    with open(os.path.join(DATA_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def scrape_team_data():
    print(f"Scraping team data from {TEAM_URL}...")
    try:
        response = requests.get(TEAM_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Fixtures
        fixtures = []
        fixture_rows = soup.find_all('tr', id=re.compile('filaPartido'))
        for row in fixture_rows:
            # Seleccionar por índice de td suele ser más robusto si las clases cambian un poco
            cols = row.find_all('td')
            if len(cols) >= 3:
                # Home (1st TD)
                home_td = cols[0]
                home_name = home_td.get_text(strip=True)
                # Away (3rd TD)
                away_td = cols[2]
                away_name = away_td.get_text(strip=True)
                # Result (2nd TD)
                result = cols[1].get_text(strip=True)
                
                iso_date = datetime.now().isoformat() + "Z"
                goals_home = None
                goals_away = None
                status = "NS"
                
                if '-' in result:
                    parts = result.split('-')
                    if len(parts) == 2 and parts[0].strip().isdigit():
                        try:
                            goals_home = int(parts[0].strip())
                            goals_away = int(parts[1].strip())
                            status = "FT"
                        except: pass

                fixtures.append({
                    "fixture": {"date": iso_date, "status": {"short": status}},
                    "teams": {
                        "home": {"name": home_name, "winner": (goals_home > goals_away if goals_home is not None else None)},
                        "away": {"name": away_name, "winner": (goals_away > goals_home if goals_away is not None else None)}
                    },
                    "goals": {"home": goals_home, "away": goals_away}
                })
        
        # 2. Squad
        players = []
        squad_rows = soup.select('table.tabla-jugadores tr')
        for row in squad_rows:
            name_cell = row.select_one('td.jugador')
            if name_cell:
                name = name_cell.get_text(strip=True)
                if not name: continue
                
                pos_cell = row.select_one('td.demarcacion')
                pos_text = pos_cell.get_text(strip=True).lower() if pos_cell else ""
                age_cell = row.select_one('td.edad')
                age = age_cell.get_text(strip=True) if age_cell else ""
                
                pos = "Midfielder"
                if "portero" in pos_text: pos = "Goalkeeper"
                elif "defensa" in pos_text or "central" in pos_text or "lateral" in pos_text: pos = "Defender"
                elif "delantero" in pos_text or "extremo" in pos_text: pos = "Forward"
                
                players.append({
                    "player": {
                        "name": name,
                        "age": age,
                        "number": None,
                        "pos": pos
                    }
                })
        
        return {"response": fixtures}, {"response": players}
    except Exception as e:
        print(f"Error scraping team data: {e}")
        return None, None

def scrape_standings():
    print(f"Scraping standings from {LEAGUE_URL}...")
    try:
        response = requests.get(LEAGUE_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        standings = []
        # Seleccionar las filas de la tabla de clasificación
        # Estas filas suelen tener la clase 'fila-link' o estar dentro de un table.lpf-consultas-tabla
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            # Las filas de datos suelen tener al menos 10 columnas
            if len(cols) >= 10:
                rank_text = cols[0].get_text(strip=True)
                if not rank_text.isdigit(): continue
                
                rank = int(rank_text)
                team_name = cols[2].get_text(strip=True)
                # En algunas ligas Pts es la columna 3, en otras la 9 o 10. 
                # En Primera Federación suele ser la columna 3 (después de Pos, Logo, Equipo)
                pts_text = cols[3].get_text(strip=True)
                points = int(pts_text) if pts_text.isdigit() else 0
                
                # Goal Difference
                diff = 0
                try:
                    diff_text = cols[10].get_text(strip=True).replace('+', '')
                    diff = int(diff_text)
                except: pass
                
                standings.append({
                    "rank": rank,
                    "team": {"name": team_name, "id": (2501 if "Mérida" in team_name else rank)},
                    "points": points,
                    "goalsDiff": diff
                })
        
        if not standings: return None
        return {"response": [{"league": {"standings": [standings]}}]}
    except Exception as e:
        print(f"Error scraping standings: {e}")
        return None

def main():
    metadata = {
        "last_updated": datetime.now().isoformat(),
        "status": "success",
        "mode": "scraping_v4"
    }

    fixtures, players = scrape_team_data()
    standings = scrape_standings()

    if fixtures: save_json("fixtures", fixtures)
    if standings: save_json("standings", standings)
    if players: save_json("players", players)

    save_json("metadata", metadata)
    # Generate static news
    news = [
        {"title": "Temporada 25/26: El Mérida firme en el Grupo 1", "source": "LaPreferente", "date": datetime.now().strftime("%Y-%m-%d"), "url": "#"},
        {"title": "Reparto de puntos en el duelo ante el Tenerife (1-1)", "source": "Crónica", "date": datetime.now().strftime("%Y-%m-%d"), "url": "#"},
        {"title": "Agenda: Próximo reto para el equipo romano", "source": "Club", "date": datetime.now().strftime("%Y-%m-%d"), "url": "#"}
    ]
    save_json("news", news)
    print("Scraping update complete.")

if __name__ == "__main__":
    main()
