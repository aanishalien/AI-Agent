import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def decide_action(user_query: str) -> dict:
    prompt = f"""
You are an AI decision engine.

Available tools:
1. calculator -> for math, percentages, numbers
2. file_reader -> for reading files or documents
3. web_search -> for current or factual information from the internet

User question: "{user_query}"

Respond ONLY in valid JSON.

If a tool is needed:
{{
    "use_tool": true,
    "tool_name": "<tool>",
    "tool_input": "<input>"
}}

If no tool is needed:
{{
    "use_tool": false
}}
"""

    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=300,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_text = response.content[0].text.strip()

    with open("prompts/system_prompt.txt", "r") as f:
        SYSTEM_PROMPT = f.read()

    # 🔥 Convert LLM JSON text → Python dict
    try:
        decision = json.loads(raw_text)
        return decision
    except json.JSONDecodeError:
        print("⚠️ JSON parsing failed. Raw output:", raw_text)
        return {"use_tool": False}
