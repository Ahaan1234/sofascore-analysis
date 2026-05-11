import os
from dotenv import load_dotenv
from groq import Groq
import json
import requests

load_dotenv()

from groq import Groq

client = Groq()

def calculate(expression:str) -> str:
    """Execute the calculation"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

available_functions = {
    "calculate": calculate,
}

def execute_tool_call(tool_call):
    """Parse and execute a single tool call"""
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)

    return function_to_call(**function_args)

tools=[{
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
            "description": "Returns the full match summary for a given event: score by period, venue, referee, and teams",
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

client_messages = [
    {
        "role": "system",
        "content": "You are an AI assisstant that helps me find out about football matches and their details. Use appropriate functions to share matches on a date, incidents in a match, and match details"
    },
    {
        "role": "user",
        "content": user_prompt,
    }
]

def run_conversation(user_prompt):
    """Run a conversation with tool calling"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=client_messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    client_messages.append(response.choices[0].message)

    if tool_calls:
        for tool_call in tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    expression=function_args.get("expression")
                )
                
                # Add tool response to conversation
                client_messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
        
        second_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=client_messages
        )
        return second_response.choices[0].message.content
    
    return response_message.content


user_prompt = "What is 25 * 4 + 10?"
print(run_conversation(user_prompt))

