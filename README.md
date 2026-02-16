# AI-Agent
Autonomous AI research agent that plans tasks, executes searches, and synthesizes answers via a REST API.


User → FastAPI → Agent → Tools/Search → Response

docker build -t ai-agent .
docker run -p 8000:80 ai-agent

