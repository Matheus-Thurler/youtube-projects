# 17 - A2A (Agent2Agent)

Fonte: só a doc oficial do ADK: [A2A](https://adk.dev/a2a/), [Introdução](https://adk.dev/a2a/intro/), [Expor um agente](https://adk.dev/a2a/quickstart-exposing/), [Consumir um agente](https://adk.dev/a2a/quickstart-consuming/), [A2A Extension](https://adk.dev/a2a/a2a-extension/). Protocolo: https://a2a-protocol.org/

Suporte: Python, Go e Java (experimental em Go, Java e Kotlin).

## O que é (doc)
O **Agent2Agent (A2A) Protocol** é o padrão para agentes se comunicarem entre si.

## A2A vs sub-agentes locais (doc)
| Sub-agente local | Agente remoto (A2A) |
|---|---|
| Roda no mesmo processo; comunicação em memória | Serviço independente, comunicação pela rede |
| Organiza o código | Outro time/organização, outra linguagem ou framework |

Use A2A quando: serviço separado, mantido por outro time, linguagens/frameworks diferentes, ou contrato formal.
Prefira sub-agentes locais para: organização interna de código, operações internas críticas em performance, memória/contexto compartilhado, funções auxiliares simples.

## Como funciona no ADK (doc)
1. **Expor:** transformar um agente ADK em um **A2AServer**.
2. **Consumir:** em outro agente, usar `RemoteA2aAgent`, um cliente que conversa com o A2AServer. Para o desenvolvedor, usar o agente remoto fica parecido com usar uma tool ou sub-agente local.

Capacidades suportadas: preservar traços de raciocínio, rastrear tools de longa duração e passar artifacts entre agentes.

## Expor com `to_a2a` (doc)
```shell
pip install google-adk[a2a]
```
```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a

a2a_app = to_a2a(root_agent, port=8001)
```
Serve-se com `uvicorn` (a porta do `to_a2a` precisa bater com a do `uvicorn`):
```shell
uvicorn contributing.samples.a2a.a2a_root.remote_a2a.hello_world.agent:a2a_app --host localhost --port 8001
```
O **agent card** é gerado automaticamente a partir do agente e fica em:
`http://localhost:8001/.well-known/agent-card.json`

Parâmetros de `to_a2a` (doc): `agent` (obrigatório), `host`, `protocol`, `port`, `push_config_store`, `agent_card` (objeto `AgentCard` ou caminho de JSON), `runner` (se omitido, usa serviços em memória), `lifespan`.

## Expor com `adk api_server --a2a` (doc)
Alternativa: escrever o agent card (`agent.json`) e hospedar com:
```shell
adk api_server --a2a --port 8001 contributing/samples/a2a/a2a_basic/remote_a2a
```
Só as pastas de agentes que têm um arquivo chamado exatamente `agent.json` são expostas por A2A. Funciona junto com `adk web`.

Exemplo de agent card (doc):
```json
{
  "capabilities": {},
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["application/json"],
  "description": "An agent specialized in checking whether numbers are prime.",
  "name": "check_prime_agent",
  "skills": [
    {
      "id": "prime_checking",
      "name": "Prime Number Checking",
      "description": "Check if numbers in a list are prime using efficient mathematical algorithms",
      "tags": ["mathematical", "computation", "prime", "numbers"]
    }
  ],
  "url": "http://localhost:8001/a2a/check_prime_agent",
  "version": "1.0.0"
}
```

## Consumir com `RemoteA2aAgent` (doc)
```python
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

prime_agent = RemoteA2aAgent(
    name="prime_agent",
    description="Agent that handles checking if numbers are prime.",
    agent_card=(
        f"http://localhost:8001/a2a/check_prime_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

root_agent = Agent(
    model="gemini-flash-latest",
    name="root_agent",
    sub_agents=[roll_agent, prime_agent],  # local + remoto
    ...
)
```
`agent_card` aceita objeto `AgentCard`, URL ou caminho de arquivo. `description` é opcional.

Rodar o agente consumidor (porta diferente do remoto, que usa 8001):
```shell
adk web contributing/samples/a2a/
```

## Avançado (doc)
- `A2aRemoteAgentConfig` (parâmetro `config`) permite conversores customizados (`a2a_message_converter`, `a2a_task_converter`, `a2a_status_update_converter`, `a2a_artifact_update_converter`, `a2a_part_converter`) e interceptors.
- `use_legacy` é `True` por padrão; `use_legacy=False` usa a nova integração com a [A2A extension](https://adk.dev/a2a/a2a-extension/).
- Versão do `a2a-sdk`: funciona com 0.3.x (modo compatibilidade) e 1.x.x; novas integrações devem usar 1.x.x.

## Relação com o episódio 05
Mesmo desenho de time (root + sub-agentes), mas o sub-agente passa a ser um serviço remoto.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example a2a_root/.env` e edite `GOOGLE_API_KEY`.

```shell
# terminal 1: agente remoto via A2A
uv run uvicorn remote_a2a.prime_agent.agent:a2a_app --host localhost --port 8001
# agent card: http://localhost:8001/.well-known/agent-card.json
# terminal 2: agente consumidor
uv run adk web --port 8000
```
No `adk web`, escolha `a2a_root`. `remote_a2a/prime_agent/` é o agente exposto.

## Roteiro do vídeo
1. Quando A2A vale a pena e quando não (as listas da doc).
2. Expor um agente com `to_a2a` e abrir o agent card no navegador.
3. `RemoteA2aAgent` como sub-agente do root.
4. Ver no `adk web` o root delegando ao agente remoto.
