import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def web_search(query: str, max_results: int = 3) -> dict:
    """
    Agent Tool: Searched the web and returns summarized results.

    Args:
        query (str): Search Query
        max_results (int): Number of search results

    Returns:
        dict: {
            "status": "success" | "error",
            "results" : [{ title, url, content}]
        }
    """
    if not TAVILY_API_KEY:
        return {"status": "error", "message": "TAVILY_API_KEY not set"}
    
    url = "https://api.tavily.com/search"

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": "basic"
    }

    try: 
        response = requests.post(url, json=payload)
        data = response.json()

        results = []
        for item in data.get("results", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content")
            })
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
