import os
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel, Field


load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class ReflectionResult(BaseModel):
    is_correct: bool = Field(description="Is the answer correct and fully addresses the question?")
    issue: str = Field(description="If incorrect or incomplete, explain what is wrong.")
    retry_needed: bool = Field(description="Should the agent try again using tools?")

def reflect_answer(answer: str, tool_result,user_query: str) -> ReflectionResult:
    prompt = f"""
You are a critical AI assistant.

User question: {user_query}

Agent answer: {answer}

Tool result (if any): {tool_result}

Evaluate the answer.

Return ONLY a **single valid JSON object**, no extra text, with these fields:
- is_correct (true/false)
- issue (string)
- retry_needed (true/false)
"""


    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    try:
        data = json.loads(response.content[0].text.strip())
        return ReflectionResult(**data)
    except Exception as e:
        # If parsing fails, assume not correct
        return ReflectionResult(is_correct=False, issue="Could not parse LLM output", retry_needed=True)