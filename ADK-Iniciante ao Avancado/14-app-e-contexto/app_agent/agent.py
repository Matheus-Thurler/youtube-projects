from google.adk.agents import Agent
from google.adk.agents.context_cache_config import ContextCacheConfig
from google.adk.apps import App
from google.adk.apps.app import EventsCompactionConfig

root_agent = Agent(
    model="gemini-flash-latest",
    name="greeter_agent",
    description="An agent that provides a friendly greeting.",
    instruction="Reply with Hello, World!",
)

# A variável deve se chamar `app` para funcionar com as ferramentas do ADK
app = App(
    name="app_agent",
    root_agent=root_agent,
    context_cache_config=ContextCacheConfig(min_tokens=2048, ttl_seconds=600, cache_intervals=5),  # experimental
    events_compaction_config=EventsCompactionConfig(token_threshold=4000, event_retention_size=5),
)
