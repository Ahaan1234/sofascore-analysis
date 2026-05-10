from fastapi import FastAPI
from datetime import date
import requests

app = FastAPI()

SOFASCORE = "https://api.sofascore.com/api/v1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# get_matches — takes a date (YYYY-MM-DD), returns all football matches on that day with scores and team IDs. 
# Calls /sport/football/scheduled-events/{date}
@app.get("/get_matches")
def get_matches(match_date: date, league: str | None = None):
    url = f"{SOFASCORE}/sport/football/scheduled-events/{match_date}"
    r = requests.get(url, headers=HEADERS)
    events = r.json().get("events",[])

    matches = []
    for event in events:
        matches.append({
            "event_id"  : event["id"],
            "slug"      : event["slug"],
            "home_team" : event["homeTeam"]["name"],
            "away_team" : event["awayTeam"]["name"],
            "home_score": event.get("homeScore",{}).get("current"),
            "away_score": event.get("awayScore",{}).get("current"),
            "status"    : event.get("status", {}).get("description"),
            "tournament": event.get("tournament", {}).get("name")
        })
    
    return {"date": match_date, "match_count": len(matches), "matches": matches}

# get_match_detail — takes an eventId, returns the full match summary: score by period, venue, referee, home/away teams. 
# Calls /event/{eventId}
@app.get("/get_match_detail/{eventID}")
def get_match_detail(eventID: str):
    url = f"{SOFASCORE}/event/{eventID}"
    r = requests.get(url, headers=HEADERS)

    event = r.json().get("event", {})
    if not event:
        return {"error": f"event {eventID} not found"}
    
    return {
        "home_team" : event["homeTeam"]["name"],
        "away_team" : event["awayTeam"]["name"],
        "home_score": {
            "current": event.get("homeScore",{}).get("current"),
            "period1": event.get("homeScore",{}).get("period1"),
            "period2": event.get("homeScore",{}).get("period2")
        },
        "away_score": {
            "current": event.get("awayScore",{}).get("current"),
            "period1": event.get("awayScore",{}).get("period1"),
            "period2": event.get("awayScore",{}).get("period2")
        },
        "status"  : event.get("status",{}).get("description"),
        "venue"   : event.get("venue",{}).get("stadium",{}).get("name"),
        "referee" : event.get("referee",{}).get("name")
    }

# get_incidents — takes an eventId, returns a cleaned timeline of goals, cards, and substitutions with minutes. 
# Calls /event/{eventId}/incidents
@app.get("/get_incidents/{eventID}")
def get_incidents(eventID: str):
    url = f"{SOFASCORE}/event/{eventID}/incidents"
    r = requests.get(url, headers=HEADERS)


# get_momentum — takes an eventId, returns the per-minute dominance summary (home vs away controlled minutes, momentum swings). 
# Calls /event/{eventId}/graph
    



# -- TEST SCRIPTS --
# r = requests.get('https://api.sofascore.com/api/v1/sport/football/scheduled-events/2024-04-10',
#                  headers=)

# print(r.status_code)
# print(type(r.text))
# print(r.text[:500])

# data:dict = r.json()
# print(data.keys())

# events = data.get("events",[])
# print(f"Found {len(events)} matches")
# print(events[0])