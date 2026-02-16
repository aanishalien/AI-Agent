import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def create_plan(user_query: str, context: str, facts: str) -> list:
    """
    Generates a list of steps the agent should perform. 
    """
    prompt = f""" 
You are an AI planning module.

Your job is to break the user's request into a clear sequence of steps.

Avilable tools:
- calculator -> for math or percentages
- file_reader -> for reading files or documents
- web_search -> for current or factual information from the internet

Conversation context:
{context}

Facts about user:
{facts}

User question:
{user_query}

Respond ONLY as a numbered list of steps.

Example:
1.  Search GDP of India
2.  Search GDP of Sri Lanka
3.  Calculate difference
"""
    
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    steps = response.content[0].text.strip().split("\n")
    steps = [step.split(".",1)[1].strip() for step in steps if "." in step]

    return steps

    