import os
from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def format_context(context):
    """Convert memory into readable chat format"""
    formatted = ""
    for msg in context:
        formatted += f"{msg['role'].upper()}: {msg['content']}\n"
    return formatted


def generate_final_answer(user_query: str, tool_result, context: list,facts: list) -> str:

    if tool_result is None:
        tool_text = "No tool used. Use conversation history and facts if relevant."
    if isinstance(tool_result, dict):
        tool_text = json.dumps(tool_result, indent=2)
    else:
        tool_result = str(tool_result)

    prompt = f"""
You are an AI assistant.

IMPORTANT RULES:
- If a tool result is provided → use it as the primary source.
- If no tool was used → answer using conversation history and facts.
- If the answer is not in tool result or memory → say you don't know.
- Do NOT invent facts.


Conversation history:
{format_context(context)}

Facts:
{facts}

User question:
{user_query}

Tool result:
{tool_text}

Now give the final helpful answer.
"""

    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()