from google.adk.agents import Agent


def set_light(location: str, status: str) -> dict:
    """Turns a light ON or OFF in a location.

    Args:
        location: Room name, for example Bedroom.
        status: Either ON or OFF.
    """
    return {"status": "success", "location": location, "light": status}


root_agent = Agent(
    model="gemini-flash-latest",
    name="light_agent",
    description="Controls lights in a house.",
    instruction="Use set_light to turn lights ON or OFF when asked. Confirm briefly.",
    tools=[set_light],
)
