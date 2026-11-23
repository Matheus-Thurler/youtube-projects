# 16 - API Server e FastAPI

Fonte: só a doc oficial do ADK: [API Server](https://adk.dev/runtime/api-server/) e [Cloud Run](https://adk.dev/deploy/cloud-run/) (exemplo `get_fast_api_app`).

Esta é a camada que o `agents-cli` (episódio 18) gera pronta em `app/fast_api_app.py`; aqui você vê o que ela é.

## `adk api_server` (doc)
Expõe seus agentes por uma API REST para testes e integração programática.
```shell
adk api_server
```
Roda por padrão em `http://localhost:8000` (Go usa 8080 e prefixo `/api`). Rode do diretório **pai** da pasta do agente. Swagger interativo em `http://localhost:8000/docs` (Python e TypeScript).

Nomes de campos em request e response usam `camelCase` (`appName`, `userId`, `sessionId`).

## Fluxo de teste (doc)
1. Listar agentes descobertos:
```shell
curl -X GET http://localhost:8000/list-apps
```
2. Criar sessão (o JSON do corpo é opcional e define o state inicial):
```shell
curl -X POST http://localhost:8000/apps/my_sample_agent/users/u_123/sessions/s_123 \
  -H "Content-Type: application/json" \
  -d '{"key1": "value1", "key2": 42}'
```
Resposta: `{"id":"s_123","appName":"my_sample_agent","userId":"u_123","state":{...},"events":[],"lastUpdateTime":...}`. Repetir user/session id dá `Session already exists`.

3. Enviar a pergunta:
- `POST /run`: devolve a lista de eventos de uma vez (recomendado se estiver em dúvida).
- `POST /run_sse`: devolve Server-Sent Events; com `"streaming": true`, streaming por token.
```shell
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{
"appName": "my_sample_agent",
"userId": "u_123",
"sessionId": "s_123",
"newMessage": {
    "role": "user",
    "parts": [{ "text": "Hey whats the weather in new york today" }]
}
}'
```
Dá para mandar arquivo em base64 com `inlineData` (`displayName`, `data`, `mimeType`) nas `parts`.

A resposta é a lista de `Event` do episódio 13 (`functionCall`, `functionResponse`, texto, `actions.stateDelta`, `actions.artifactDelta`).

## FastAPI com `get_fast_api_app` (doc, página do Cloud Run)
```python
import os

import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: Use 'sqlite+aiosqlite' instead of 'sqlite' because DatabaseSessionService requires an async driver
SESSION_SERVICE_URI = "sqlite+aiosqlite:///./sessions.db"
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]
SERVE_WEB_INTERFACE = True

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_SERVICE_URI,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

# You can add more FastAPI routes or configurations below if needed
# @app.get("/hello")
# async def read_root():
#     return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
```
- `session_service_uri` troca o `SessionService` (episódio 06): a doc cita SQLite e `memory://`.
- `web=True` serve também a interface web (é só para desenvolvimento).
- Você pode adicionar suas próprias rotas FastAPI.

## Retomar uma execução (doc)
Com resume ativado no `App`, `/run_sse` aceita o `invocation_id` para retomar (episódio 13).

## Próximos passos (doc)
Deploy em Agent Runtime ou Cloud Run (episódio 19).

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example hello_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run python main.py     # FastAPI próprio em :8080
uv run adk api_server     # servidor padrão em :8000
```
O `sqlite+aiosqlite` exige o extra `google-adk[db]` e `aiosqlite` (já no `pyproject.toml`). Teste: `curl localhost:8080/list-apps`.

## Roteiro do vídeo
1. `adk api_server` e o `/docs` (Swagger).
2. `curl`: `list-apps`, criar sessão, `/run`.
3. `/run_sse` com `streaming: true`.
4. `get_fast_api_app` num `main.py` seu, com `session_service_uri`.
5. Mostrar que o `agents-cli` gera esse arquivo (episódio 18).
