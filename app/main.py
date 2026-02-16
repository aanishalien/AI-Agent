from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.agent import run_agent
from app.logger import logger
from tenacity import retry, stop_after_attempt, wait_fixed
import asyncio
from collections import defaultdict

app = FastAPI(title="AI Research Agent" , version="1.0")

memory_store = defaultdict(list)

class Query(BaseModel):
    query: str

@app.get("/health")
async def health():
    return {"status": "ok"}


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@app.post("/research")
async def research(q: Query, user_id: str = "default"):
    try:
        logger.info(f"Received query: {q.query}")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_agent, q.query)
        return {"result": result, "history": memory_store[user_id]}
    except Exception as e:
        logger.error("Agent failed: %s", str(e))
        return {"error": "Agent failed, see logs"}

