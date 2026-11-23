import asyncio

from app_agent.agent import app
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner

load_dotenv()  # lê GOOGLE_API_KEY do .env


async def main():
    runner = InMemoryRunner(app=app)
    await runner.run_debug("Hello there!")


if __name__ == "__main__":
    asyncio.run(main())
