from fastapi import FastAPI
from datetime import date
import requests

SOFASCORE = "https://api.sofascore.com/api/v1"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}




# -- TEST SCRIPTS --
# r = requests.get('https://api.sofascore.com/api/v1/sport/football/scheduled-events/2024-04-10',
#                  headers={"User-Agent": "Mozilla/5.0"})

# print(r.status_code)
# print(type(r.text))
# print(r.text[:500])

# data:dict = r.json()
# print(data.keys())

# events = data.get("events",[])
# print(f"Found {len(events)} matches")
# print(events[0])