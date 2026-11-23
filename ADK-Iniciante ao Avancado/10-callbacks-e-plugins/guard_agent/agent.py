from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import LlmRequest, LlmResponse
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types


# Callback de agente: retornar LlmResponse pula o LLM; retornar None segue o fluxo
def block_keyword(callback_context: CallbackContext, llm_request: LlmRequest):
    last = llm_request.contents[-1] if llm_request.contents else None
    text = last.parts[0].text if last and last.parts and last.parts[0].text else ""
    if "BLOQUEAR" in text.upper():
        return LlmResponse(content=types.Content(role="model", parts=[types.Part(text="Pedido bloqueado pelo guardrail.")]))
    return None


def get_status(service: str) -> dict:
    """Returns the status of a service."""
    return {"status": "success", "service": service, "state": "ok"}


# Plugin: registrado uma vez no App, vale para todos os agentes e tools
class CountToolsPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="count_tools")
        self.calls = 0

    async def after_tool_callback(self, *, tool: BaseTool, tool_args: dict, tool_context: ToolContext, result: dict):
        self.calls += 1
        print(f"[plugin] tool={tool.name} chamadas={self.calls}")
        return None  # None = apenas observa


root_agent = Agent(
    model="gemini-flash-latest",
    name="guard_agent",
    instruction="Use get_status para responder sobre serviços.",
    tools=[get_status],
    before_model_callback=block_keyword,
)

app = App(name="guard_agent", root_agent=root_agent, plugins=[CountToolsPlugin()])
