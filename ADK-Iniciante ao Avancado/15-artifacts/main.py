"""Artifacts sem LLM: salvar, versionar e carregar com InMemoryArtifactService."""
import asyncio

from google.adk.artifacts import InMemoryArtifactService
from google.genai import types

APP, USER, SESSION = "demo", "u1", "s1"


async def main():
    svc = InMemoryArtifactService()

    def part(text):
        return types.Part.from_bytes(data=text.encode(), mime_type="text/plain")

    # sessão: nome simples; cada save cria uma versão nova
    v0 = await svc.save_artifact(app_name=APP, user_id=USER, session_id=SESSION, filename="report.txt", artifact=part("v0"))
    v1 = await svc.save_artifact(app_name=APP, user_id=USER, session_id=SESSION, filename="report.txt", artifact=part("v1"))
    print("versões salvas:", v0, v1)
    print("lista de versões:", await svc.list_versions(app_name=APP, user_id=USER, session_id=SESSION, filename="report.txt"))

    latest = await svc.load_artifact(app_name=APP, user_id=USER, session_id=SESSION, filename="report.txt")
    first = await svc.load_artifact(app_name=APP, user_id=USER, session_id=SESSION, filename="report.txt", version=0)
    print("mais recente:", latest.inline_data.data, "| versão 0:", first.inline_data.data)

    # escopo de usuário: prefixo "user:" vale para qualquer sessão
    await svc.save_artifact(app_name=APP, user_id=USER, session_id=SESSION, filename="user:profile.txt", artifact=part("perfil"))
    other = await svc.load_artifact(app_name=APP, user_id=USER, session_id="OUTRA", filename="user:profile.txt")
    print("user: visto em outra sessão:", other.inline_data.data)
    print("plain visto em outra sessão:", await svc.load_artifact(app_name=APP, user_id=USER, session_id="OUTRA", filename="report.txt"))


asyncio.run(main())
