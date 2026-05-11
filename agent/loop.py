import os
from dotenv import load_dotenv
from groq import Groq
import json
import requests

load_dotenv()

client = Groq()

BACKEND = "http://localhost:8000"

# Tools whose eventID is a path param, not a query param
PATH_PARAM_TOOLS = {
    "get_match_detail": "eventID",
    "get_incidents":    "eventID",
}

tools: list = [
    {
        "type": "function",
        "function": {
            "name": "get_matches",
            "description": "Returns all football matches scheduled on a given date with scores and team IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "match_date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format"
                    }
                },
                "required": ["match_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_match_detail",
            "description": "Returns the full match summary for a given event: score by period, venue, referee, and teams.",
            "parameters": {
                "type": "object",
                "properties": {
                    "eventID": {
                        "type": "string",
                        "description": "Sofascore event ID of the match"
                    }
                },
                "required": ["eventID"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_incidents",
            "description": "Returns a cleaned timeline of goals, cards, and substitutions with their minute for a match.",
            "parameters": {
                "type": "object",
                "properties": {
                    "eventID": {
                        "type": "string",
                        "description": "Sofascore event ID of the match"
                    }
                },
                "required": ["eventID"]
            }
        }
    },
]


def call_backend(tool_name: str, args: dict) -> str:
    if tool_name in PATH_PARAM_TOOLS:
        path_value = args[PATH_PARAM_TOOLS[tool_name]]
        r = requests.get(f"{BACKEND}/{tool_name}/{path_value}")
    else:
        r = requests.get(f"{BACKEND}/{tool_name}", params=args)
    return json.dumps(r.json())


def run_conversation(user_prompt: str):
    messages: list = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps find information about football matches. Use the available functions to look up matches on a date, match details, and match incidents."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls is None:
            print(message.content)
            break

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = call_backend(tool_name, args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


user_prompt = input("Ask about football: ")
run_conversation(user_prompt)
