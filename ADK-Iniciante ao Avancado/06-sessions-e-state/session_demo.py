"""Session, State e Memory sem LLM."""
import asyncio

from google.adk.events import Event, EventActions
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.genai import types

APP, USER = "demo", "u1"


async def main():
    svc = InMemorySessionService()

    # state inicial com os 4 escopos (sem prefixo, user:, app:, temp:)
    s1 = await svc.create_session(
        app_name=APP, user_id=USER, session_id="s1",
        state={"cart": 1, "user:name": "Ana", "app:theme": "dark"},
    )
    # atualizar state da forma recomendada: Event com state_delta
    await svc.append_event(s1, Event(author="agent", actions=EventActions(state_delta={"cart": 2, "user:visits": 1})))
    s1 = await svc.get_session(app_name=APP, user_id=USER, session_id="s1")
    print("s1:", s1.state)

    # nova sessão do mesmo usuário: user:/app: aparecem, state de sessão não
    s2 = await svc.create_session(app_name=APP, user_id=USER, session_id="s2")
    print("s2:", s2.state)

    # Memory: guardar a sessão e buscar depois
    s1.events.append(Event(author="user", content=types.Content(role="user", parts=[types.Part(text="Meu gato se chama Tom")])))
    mem = InMemoryMemoryService()
    await mem.add_session_to_memory(s1)
    res = await mem.search_memory(app_name=APP, user_id=USER, query="gato")
    print("memória:", [m.content.parts[0].text for m in res.memories])


asyncio.run(main())
