from google.adk.agents import Agent

MODEL = "gemini-flash-latest"


def say_hello(name: str = "there") -> str:
    """Provides a simple greeting."""
    return f"Hello, {name}!"


def say_goodbye() -> str:
    """Provides a simple farewell."""
    return "Goodbye! Have a great day."


# description é o que o root lê para decidir a quem delegar
greeting_agent = Agent(
    model=MODEL,
    name="greeting_agent",
    description="Handles simple greetings and hellos using the say_hello tool.",
    instruction="You only greet the user. Use say_hello.",
    tools=[say_hello],
)

farewell_agent = Agent(
    model=MODEL,
    name="farewell_agent",
    description="Handles simple farewells and goodbyes using the say_goodbye tool.",
    instruction="You only say goodbye. Use say_goodbye.",
    tools=[say_goodbye],
)

root_agent = Agent(
    model=MODEL,
    name="coordinator",
    description="Coordinator that delegates greetings and farewells to specialists.",
    instruction="Delegate greetings to greeting_agent and farewells to farewell_agent. Answer anything else yourself.",
    sub_agents=[greeting_agent, farewell_agent],
)
