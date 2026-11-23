# 14 - App e contexto

Fonte: só a doc oficial do ADK: [App](https://adk.dev/apps/), [Agent context](https://adk.dev/context/), [Context caching](https://adk.dev/context/caching/), [Context compression](https://adk.dev/context/compaction/), [Resume](https://adk.dev/runtime/resume/), [Plugins](https://adk.dev/plugins/).

## A classe `App` (doc)
Contêiner de nível mais alto do workflow de agentes, agrupados por um `root agent`. Opcional. Separa a infraestrutura operacional do raciocínio de cada agente. Serve para configurar:
- Context caching
- Context compression
- Agent resume
- Plugins

Problemas que resolve (doc): configuração centralizada, hooks de startup/shutdown (pools de conexão, caches), escopo explícito do state `app:*`, e uma **unidade formal de deploy**.

```python
from google.adk.agents.llm_agent import Agent
from google.adk.apps import App

root_agent = Agent(
    model='gemini-flash-latest',
    name='greeter_agent',
    description='An agent that provides a friendly greeting.',
    instruction='Reply with Hello, World!',
)

app = App(
    name="agents",
    root_agent=root_agent,
    # Optionally include App-level features:
    # plugins, context_cache_config, events_compaction_config,
    # resumability_config
)
```
Dica da doc: nomeie a variável `app` para ser compatível com as ferramentas de linha de comando do ADK.

Rodando com `InMemoryRunner`:
```python
from google.adk.runners import InMemoryRunner
from agent import app

runner = InMemoryRunner(app=app)
response = await runner.run_debug("Hello there!")  # run_debug: ADK Python 1.18+
```

## Contexto (doc)
Contexto é o pacote de informação disponível ao agente e às tools. Permite: manter state, passar dados entre passos, acessar serviços (artifacts, memory, authentication), identidade e tracking (`agent.name`, `invocation_id`), e ações específicas de tools.

A peça central é o `InvocationContext` (uma invocação completa, da pergunta à resposta final). Você normalmente **não** o cria: o framework o cria em `runner.run_async` e o passa de forma implícita para agentes, callbacks e tools.

| Tipo | Onde aparece |
|---|---|
| `InvocationContext` | Dentro de agentes (`_run_async_impl`) |
| `ReadonlyContext` | Onde só leitura é permitida (ex.: `InstructionProvider`) |
| `CallbackContext` / `Context` | Callbacks |
| `ToolContext` | Tools |

Em Python e TypeScript, `CallbackContext` e `ToolContext` são unificados em um único `Context` (aliases continuam válidos). Tarefas comuns com o contexto (doc): ler informação, gerenciar state, trabalhar com artifacts (episódio 15), autenticação de tools, memory.

## Context caching (doc, Python 1.15+, **experimental**)
Reaproveita instruções longas ou grandes conjuntos de dados entre requisições, com modelos que suportam (Gemini 2.0+). Configurado no `App`:
```python
from google.adk.agents.context_cache_config import ContextCacheConfig

app = App(
    name='my-caching-agent-app',
    root_agent=root_agent,
    context_cache_config=ContextCacheConfig(
        min_tokens=2048,    # Minimum tokens to trigger caching
        ttl_seconds=600,    # Store for up to 10 minutes
        cache_intervals=5,  # Refresh after 5 uses
    ),
)
```

## Context compression / compaction (doc, Python 1.16+)
Reduz o contexto que cresce durante a sessão. Duas estratégias em `EventsCompactionConfig`:
- **Token-based (primária):** dispara por volume de tokens. Se as duas estiverem configuradas, a por token tem prioridade.
- **Sliding window (por turnos):** dispara após um número fixo de turnos.

```python
from google.adk.apps.app import App, EventsCompactionConfig

compaction_config = EventsCompactionConfig(
    token_threshold=4000,     # Triggers compaction when actual token count exceeds this
    event_retention_size=5    # Number of recent raw events to keep intact when token limit is hit
)

app = App(
    name="my_compacting_agent_app",
    root_agent=root_agent,
    events_compaction_config=compaction_config
)
```

## Plugins e resume no `App`
`plugins=[...]` (episódio 10) e `resumability_config` (episódio 13) também são configurados aqui.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example app_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run python main.py   # InMemoryRunner(app=app)
uv run adk web
```
`ContextCacheConfig` é experimental (doc).

## Roteiro do vídeo
1. Por que um `App` (as 4 razões da doc) e o que ele agrega.
2. Montar `App(name, root_agent, ...)` e rodar com `InMemoryRunner`.
3. Os tipos de contexto e quem recebe qual.
4. Caching e compaction: o problema (contexto crescendo) e as configs.
