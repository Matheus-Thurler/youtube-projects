# 13 - Runner, Event Loop e Events

Fonte: só a doc oficial do ADK: [Event Loop](https://adk.dev/runtime/event-loop/), [Events](https://adk.dev/events/), [Runtime Config](https://adk.dev/runtime/runconfig/), [Resume](https://adk.dev/runtime/resume/), [Agent Runtime](https://adk.dev/runtime/).

Este é o "motor" por baixo de `adk run`, `adk web` e do servidor FastAPI dos próximos episódios.

## Formas de rodar um agente (doc)
| Forma | Comando |
|---|---|
| Dev UI | `adk web` |
| Linha de comando | `adk run` |
| API Server (REST) | `adk api_server` (episódio 16) |
| Ambient agents | agentes autônomos que processam eventos |

## Event Loop (doc)
O Runtime é o "motor" da aplicação. No centro há um **Event Loop** entre o `Runner` e a sua *Execution Logic* (agents, chamadas ao LLM, callbacks e tools):
1. O `Runner` recebe a query do usuário e pede ao agente principal para começar.
2. O agente roda até ter algo a reportar (resposta, pedido de tool, mudança de state) e **emite (yield)** um `Event`.
3. O `Runner` processa o evento (grava `state_delta`/`artifact_delta` via Services) e o repassa adiante (UI).
4. O agente **retoma** de onde parou só depois que o `Runner` terminou de processar.
5. Repete até não haver mais eventos para aquela query.

## Componentes do Runtime (doc)
| Componente | Papel |
|---|---|
| `Runner` | Ponto de entrada e orquestrador de uma query (`run_async`) |
| Execution Logic | Agents (`BaseAgent`, `LlmAgent`), Tools, Callbacks |
| `Event` | Mensagem entre `Runner` e a lógica; carrega conteúdo e efeitos (`actions`) |
| Services | `SessionService`, `ArtifactService`, `MemoryService` (opcional) |
| `Session` | Estado e histórico de *uma* conversa |
| `Invocation` | Tudo que acontece em resposta a *uma* query do usuário (`invocation_id`); `temp:` vale só aqui |

## Passo a passo de uma invocação (doc)
Usuário pergunta → `Runner` carrega a `Session` e adiciona a pergunta como `Event` → chama `agent.run_async(ctx)` → LLM decide chamar tool → evento `FunctionCall` → `Runner` grava e repassa → agente executa a tool → evento `FunctionResponse` (pode ter `state_delta`/`artifact_delta`) → `Runner` aplica → LLM gera o texto final → evento final (`is_final_response()`).

## Comportamentos importantes (doc)
- **Commit do state:** a mudança só é gravada depois que o evento com o `state_delta` é emitido e processado pelo `Runner`.
- **"Dirty reads":** código executado depois, na mesma invocação e antes do evento ser processado, *pode* ver a mudança local ainda não gravada.
- **Streaming (`partial=True`):** o `Runner` repassa eventos parciais na hora (para a UI) mas **não processa as `actions`** deles; só processa o evento final, não parcial.
- **Async é o padrão:** `Runner.run_async` é o ponto principal; `Runner.run` (síncrono) é conveniência. No Python, uma tool síncrona roda inline no event loop do asyncio: I/O bloqueante trava o loop.

## Events (doc)
`google.adk.events.Event` estende `LlmResponse` e adiciona: `author` (`'user'` ou nome do agente), `invocation_id`, `id`, `timestamp`, `actions` (`EventActions`), `branch`.
- Identificar o tipo: `event.get_function_calls()`, `event.get_function_responses()`, `event.partial`, texto em `event.content.parts`.
- **Resposta final de um turno:** `event.is_final_response()`.
- **Sinais de controle em `event.actions`:** `state_delta`, `artifact_delta`, `transfer_to_agent` (passar o controle), `escalate` (encerrar um loop), `skip_summarization` (não resumir o resultado da tool).

## Usando o Runner (doc: exemplo do Agent Context)
```python
from google.adk import Runner

runner = Runner(
    app_name="my_app",
    agent=my_root_agent,
    session_service=my_session_service,
    artifact_service=my_artifact_service,
)

async for event in runner.run_async(
    user_id="user123",
    session_id="session456",
    new_message=user_message
):
    ...
```

## RunConfig (doc)
Passado a `runner.run_async()` / `run_live()`:
```python
from google.adk.agents.run_config import RunConfig, StreamingMode

config = RunConfig(
    streaming_mode=StreamingMode.SSE,
    max_llm_calls=200,
)
```
- `StreamingMode.NONE` (padrão): uma resposta completa por turno. `StreamingMode.SSE`: eventos parciais enquanto o LLM gera.
- Python: `get_session_config` (`num_recent_events` / `after_timestamp`) limita os eventos carregados; `context_window_compression`; `model_input_context` (contexto só daquela invocação, não persistido).

## Resume (doc, Python 1.16+)
Retomar um workflow interrompido, via `App`:
```python
app = App(
    name='my_resumable_agent',
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)
```
Retoma-se com o `invocation_id` (que aparece no histórico de Events). Custom Agents não suportam resume por padrão. Atenção: muda o comportamento de Long Running Functions, Confirmations e Authentication.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

```shell
uv run python main.py
```
Sem LLM: um agente próprio emite `Event`s e o `Runner` grava o `state_delta`.

## Roteiro do vídeo
1. As formas de rodar (`adk web`, `adk run`, `adk api_server`) e o que todas têm em comum: o `Runner`.
2. Desenhar o Event Loop: yield → pausa → `Runner` processa → retoma.
3. Mostrar os eventos no `adk web` (aba de eventos) e ler `author`, `actions`.
4. `partial` e streaming; `RunConfig`.
5. Resume (ponte para o episódio 14, `App`).
