import os
from dotenv import load_dotenv
from groq import Groq
import asyncio

load_dotenv()

async def main():
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )



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
            "content": "Count to 10.  Your response must begin with \"1; \".  example: 1; 2; 3; ...",
        }
    ],
    stop = "6",
    # The language model which will generate the completion.
    model="llama-3.3-70b-versatile",
)


print(chat_completion.choices[0].message.content)