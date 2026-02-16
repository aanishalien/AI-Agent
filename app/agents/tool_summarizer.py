import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def summarize_tool_output(user_query: str, tool_result: str) -> str:
    """
    Extract only useful facts from tool output. 
    """

    prompt = f""" 
You are a data extraction assistant.

User question:
{user_query}

Tool output:
{tool_result}

Extract ONLY key facts relevant to answering the question.
Return short bullet points.
Ignore ads, noise , unrelated info.
"""
    
    
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=300,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()