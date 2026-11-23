from google.adk.agents import Agent

root_agent = Agent(
    model="gemini-flash-latest",
    name="hello_agent",
    description="Says hello.",
    instruction="Reply with a short friendly greeting.",
)
