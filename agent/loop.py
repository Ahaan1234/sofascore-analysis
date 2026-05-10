import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

from groq import Groq

client = Groq()

chat_completion = client.chat.completions.create(
    #
    # Required parameters
    #
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": "Whats the weather like in North Carolina?",
        }
    ],
    tools=[{
        "type": "function",
        "function": {
        "name": "get_current_weather",
        "description":"Get the current weather in a given location",
        "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
            }
        },
        "required": ["location"]
        }
        }
    }
    ],
    tool_choice="auto",
    # The language model which will generate the completion.
    model="llama-3.3-70b-versatile",
)


print(chat_completion.choices[0].message.content)