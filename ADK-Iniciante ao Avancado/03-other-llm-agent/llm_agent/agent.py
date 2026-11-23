import os
import random

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


def roll_die(sides: int) -> dict:
    """Rolls a die with the given number of sides."""
    return {"status": "success", "result": random.randint(1, sides)}


root_agent = LlmAgent(
    model=LiteLlm(model=os.getenv("LLM_MODEL", "lm_studio/google/gemma-4-e4b")),
    name="dice_agent",
    description="Rolls dice.",
    instruction="You roll dice and answer questions about the outcome of the dice rolls.",
    tools=[roll_die],
)
