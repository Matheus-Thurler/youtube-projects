from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


class CapitalOutput(BaseModel):
    capital: str = Field(description="The capital of the country.")


root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="capital_agent",
    description="Returns the capital of a country as JSON.",
    instruction='You are a Capital Information Agent. Given a country, respond ONLY with a JSON object containing the capital. Format: {"capital": "capital_name"}',
    output_schema=CapitalOutput,
    output_key="found_capital",  # resultado fica em state["found_capital"]
)
