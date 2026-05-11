from fastapi import FastAPI
from datetime import date
import requests

app = FastAPI()

SOFASCORE = "https://api.sofascore.com/api/v1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

@app.get("/get_matches")
def get_matches(match_date: date):
    """Returns all football matches scheduled on a given date with scores and team IDs.

    Args:
        match_date: Date in YYYY-MM-DD format.

    Returns:
        dict with date, match_count, and a list of matches (event_id, slug, home/away team,
        home/away score, status, tournament).
    """
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

@app.get("/get_match_detail/{eventID}")
def get_match_detail(eventID: str):
    """Returns the full match summary for a given event: score by period, venue, referee, and teams.

    Args:
        eventID: Sofascore event ID.

    Returns:
        dict with home/away team names, scores (current, period1, period2), status, venue, and referee.
        Returns an error dict if the event is not found.
    """
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

@app.get("/get_incidents/{eventID}")
def get_incidents(eventID: int):
    """Returns a cleaned timeline of goals, cards, and substitutions with their minute for a match.

    Args:
        eventID: Sofascore event ID.

    Returns:
        dict with three lists — goals (minute, added_time, side, scorer, assist),
        cards (minute, side, player, card type), and substitutions (minute, side,
        player_off, player_on, injury flag).
        Returns an error dict if the event is not found.
    """
    url = f"{SOFASCORE}/event/{eventID}/incidents"
    r = requests.get(url, headers=HEADERS)

    incidents = r.json().get("incidents", {})
    if not incidents:
        return {"error": f"Event {eventID} not found"}
    
    goals = []
    cards = []
    subs  = []
    incident:dict

    for incident in incidents:
        side = "home" if incident.get("isHome") else "away"

        if incident.get("incidentType") == "goal":
            goals.append({
                "minute": incident.get("time"),
                "added_time": incident.get("addedTime"),
                "side":   side,
                "scorer": incident.get("player", {}).get("name"),
                "assist": incident.get("assist1", {}).get("name")  # None if no assist
            })

        elif incident.get("incidentType") == "card":
            cards.append({
                "minute": incident.get("time"),
                "side":   side,
                "player": incident.get("player", {}).get("name"),
                "card":   incident.get("incidentClass")  # "yellow" or "red"
            })

        elif incident.get("incidentType") == "substitution":
            subs.append({
                "minute":     incident.get("time"),
                "side":       side,
                "player_off": incident.get("playerOut", {}).get("name"),
                "player_on":  incident.get("playerIn",  {}).get("name"),
                "injury":     incident.get("injury", False)
            })

    return {"goals": goals, "cards": cards, "substitutions": subs}





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