from groq import Groq
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

client = Groq(api_key=env_vars.get("GroqAPIKey"))

def get_ai_response(messages):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stream=False
    )

    return completion.choices[0].message.content
