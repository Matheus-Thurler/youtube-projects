import os

import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
# sqlite+aiosqlite: o DatabaseSessionService exige driver assíncrono
SESSION_SERVICE_URI = "sqlite+aiosqlite:///./sessions.db"

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_SERVICE_URI,
    allow_origins=["http://localhost:8080"],
    web=True,  # só desenvolvimento
)


@app.get("/hello")
async def hello():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8080)))
