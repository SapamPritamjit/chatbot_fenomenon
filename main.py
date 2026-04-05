from json import load, dump
from search import search_web
from ai import get_ai_response
from utils import clean_text
import os

CHATLOG_PATH = "Data/ChatLog.json"

# Ensure file exists
if not os.path.exists("Data"):
    os.mkdir("Data")

if not os.path.exists(CHATLOG_PATH):
    with open(CHATLOG_PATH, "w") as f:
        dump([], f)

# System prompt
preamble = """
You are a decision-making AI that classifies user queries.

DO NOT answer the question.
ONLY classify it.

Categories:

1. general:
- General knowledge
- Definitions
- Explanations
Example:
general: what is python

2. realtime:
- Latest news
- Current prices
- Current positions (CM, PM, CEO now)
Example:
realtime: current gold price

3. task:
- Commands like open apps, play music, etc
Example:
task: open youtube

Rules:
- Always return in format: category: query
- Do NOT return anything else
- If unsure → return general: query
"""

def classify_query(prompt):
    prompt_lower = prompt.lower()

    # 🔥 REALTIME KEYWORDS
    realtime_keywords = [
        "current", "latest", "today", "now",
        "price", "news", "who won", "cm", "pm", "president"
    ]

    # 🔥 GENERAL OVERRIDE
    general_keywords = [
        "who is", "what is", "define", "explain"
    ]

    # If it's basic definition → general
    if any(k in prompt_lower for k in general_keywords):
        if any(x in prompt_lower for x in ["current", "latest", "now", "today"]):
            return "realtime"
        return "general"

    # If contains realtime keywords
    if any(k in prompt_lower for k in realtime_keywords):
        return "realtime"

    return "general"
 
def chatbot(prompt):

    # 🧠 classify
    classification = classify_query(prompt)
    print("DEBUG:", classification)

    # -------------------------
    # 🟢 GENERAL QUERY
    # -------------------------
    if classification == "general":
        messages = [
            {"role": "system", "content": "You are a precise and accurate AI assistant."},
            {"role": "user", "content": prompt}
        ]

        return get_ai_response(messages)

    # -------------------------
    # 🔴 REALTIME QUERY
    # -------------------------
    elif classification == "realtime":

        if "world cup" in prompt.lower():
            search_prompt = "latest ICC cricket world cup winner official 2023 2024"
        else:
            search_prompt = f"{prompt} latest news 2026 official data"

        search_data = search_web(search_prompt)

        if not search_data.strip() or len(search_data) < 50:
            return "Information is unclear."

        enhanced_prompt = f"""
    You are a highly accurate real-time AI.

    STRICT RULES:
    - Answer using the provided data as PRIMARY source
    - If the answer is clearly a well-known factual answer, you may answer
    - If the answer is NOT present and not obvious → say "Information is unclear"
    - Do NOT guess
    - Prefer the most recent information

    Data:
    {search_data}

    Question:
    {prompt}

    Answer in ONE clear sentence:
    Do NOT include exact numbers unless clearly present in the data.
    """

        messages = [
            {"role": "system", "content": "You are a real-time AI assistant."},
            {"role": "user", "content": enhanced_prompt}
        ]

        return clean_text(get_ai_response(messages))
    
    # else:
    #     return "Information is unclear."

# 🔥 CLI test
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print("AI:", chatbot(user_input))