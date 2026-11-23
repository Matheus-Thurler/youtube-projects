"""Event loop sem LLM: um agente próprio emite Events; o Runner os grava."""
import asyncio

from google.adk.agents import BaseAgent
from google.adk.events import Event, EventActions
from google.adk.runners import InMemoryRunner
from google.genai import types


class CounterAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        # 1. emite um evento com state_delta e PAUSA até o Runner processar
        yield Event(
            author=self.name,
            actions=EventActions(state_delta={"status": "processing"}),
        )
        # 2. aqui o state já foi gravado pelo Runner
        print("  [agente] state após o yield:", ctx.session.state.get("status"))
        yield Event(
            author=self.name,
            content=types.Content(role="model", parts=[types.Part(text="pronto")]),
        )


async def main():
    runner = InMemoryRunner(agent=CounterAgent(name="counter"), app_name="demo")
    session = await runner.session_service.create_session(app_name="demo", user_id="u1")
    msg = types.Content(role="user", parts=[types.Part(text="oi")])
    async for event in runner.run_async(user_id="u1", session_id=session.id, new_message=msg):
        print(f"evento de {event.author}: final={event.is_final_response()} delta={event.actions.state_delta}")
    s = await runner.session_service.get_session(app_name="demo", user_id="u1", session_id=session.id)
    print("state final:", s.state)
    print("eventos na sessão:", [e.author for e in s.events])


asyncio.run(main())
