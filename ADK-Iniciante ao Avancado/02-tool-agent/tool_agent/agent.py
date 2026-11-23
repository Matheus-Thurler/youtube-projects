import json
from datetime import datetime
from urllib.request import urlopen
from zoneinfo import ZoneInfo

from google.adk.agents.llm_agent import Agent

GEO = "https://geocoding-api.open-meteo.com/v1/search?count=1&name="
WEATHER = (
    "https://api.open-meteo.com/v1/forecast?current=temperature_2m,weather_code"
    "&latitude={latitude}&longitude={longitude}"
)


def get_current_time(city: str) -> dict:
    """Returns the current real-time date and time in a specified city.

    Args:
        city: Name of the city.
    """
    places = json.load(urlopen(GEO + city)).get("results")
    if not places:
        return {"status": "error", "message": f"City '{city}' not found."}
    now = datetime.now(ZoneInfo(places[0]["timezone"]))
    return {"status": "success", "city": city, "time": now.strftime("%H:%M:%S")}


def get_current_weather(city: str) -> dict:
    """Returns the current real-time weather in a specified city.

    Args:
        city: Name of the city.
    """
    places = json.load(urlopen(GEO + city)).get("results")
    if not places:
        return {"status": "error", "message": f"City '{city}' not found."}
    current = json.load(urlopen(WEATHER.format(**places[0])))["current"]
    return {
        "status": "success",
        "city": city,
        "temperature_c": current["temperature_2m"],
        "weather_code": current["weather_code"],  # WMO code, 0 = clear sky
    }


root_agent = Agent(
    model="gemini-flash-latest",
    name="root_agent",
    description="Tells the current time and weather in a specified city.",
    instruction=(
        "You are a helpful assistant that tells the current time and weather in cities. "
        "Use 'get_current_time' for time and 'get_current_weather' for weather. "
        "Translate the WMO weather_code into plain words."
    ),
    tools=[get_current_time, get_current_weather],
)
