"""Checagem sem LLM: o guardrail bloqueia e o plugin conta."""
import asyncio
from types import SimpleNamespace

from google.genai import types
from google.adk.models import LlmRequest

from guard_agent.agent import CountToolsPlugin, block_keyword


def req(text):
    return LlmRequest(contents=[types.Content(role="user", parts=[types.Part(text=text)])])


assert block_keyword(None, req("por favor BLOQUEAR isso")) is not None
assert block_keyword(None, req("olá")) is None

plugin = CountToolsPlugin()
asyncio.run(plugin.after_tool_callback(tool=SimpleNamespace(name="get_status"), tool_args={}, tool_context=None, result={}))
assert plugin.calls == 1
print("ok")
