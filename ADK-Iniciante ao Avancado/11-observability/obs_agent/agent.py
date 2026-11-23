from google.adk.agents import Agent


def get_status(service: str) -> dict:
    """Returns the status of a service."""
    return {"status": "success", "service": service, "state": "ok"}


root_agent = Agent(
    model="gemini-flash-latest",
    name="obs_agent",
    instruction="Use get_status para responder sobre serviços.",
    tools=[get_status],
)
