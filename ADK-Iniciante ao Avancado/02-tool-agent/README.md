# 02 - Agente com tool

Fonte: só a doc oficial do ADK: [Function tools](https://adk.dev/tools-custom/function-tools/) e [LlmAgent](https://adk.dev/agents/llm-agents/).

## O que é
Quando as tools prontas não servem, você cria *function tools*. Ao colocar uma função Python na lista `tools` do agente, o framework a embrulha automaticamente como `FunctionTool`.

## Como funciona (doc)
O ADK inspeciona a assinatura da função (nome, docstring, parâmetros, type hints, valores default) e gera um schema. É esse schema que o LLM usa para entender o propósito da tool, quando usá-la e quais argumentos ela exige.

## Exemplo da doc (quickstart)
```python
from google.adk.agents.llm_agent import Agent

# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-flash-latest',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)
```

## Regras da assinatura (doc)
- **Parâmetro obrigatório:** tem type hint e **não** tem valor default.
- A docstring inteira vira a `description` da tool; descreva cada parâmetro nela (o ADK não envia descrição por parâmetro).
- `*args` e `**kwargs` são **ignorados** no schema; o LLM não sabe deles.
- **Retorno:** o preferido é um dicionário. Se retornar outro tipo, o framework embrulha em `{"result": ...}`. Recomendação da doc: incluir uma chave `"status"` ("success", "error", "pending") e mensagens de erro legíveis, porque quem entende o resultado é o LLM.

## Context injection (doc)
Parâmetro tipado como `ToolContext` é injetado pelo ADK e fica invisível ao LLM (detectado pelo tipo, não pelo nome):
```python
from google.adk.tools import ToolContext

def my_tool(arg1: str, tool_context: ToolContext):
    user_id = tool_context.state.get("user_id")
```
`ToolContext` dá acesso a `state`, `actions` (ex.: `transfer_to_agent`) e métodos de artifacts (`load_artifact`, `save_artifact`).

## Passar dados entre tools (doc)
Recomendado: prefixo `temp:` no state. Vale só para a invocação atual; todas as chamadas de tool de um mesmo turno compartilham o `InvocationContext`.

## Boas práticas (doc)
- Menos parâmetros é melhor.
- Tipos simples (`str`, `int`) em vez de classes.
- Nomes significativos (evitar `do_stuff()`).
- Construir pensando em execução paralela/assíncrona: https://adk.dev/tools-custom/performance/

## Outros tipos de tool na mesma página
Long running function tools (`LongRunningFunctionTool`) e Agent-as-a-Tool. Veja também MCP no episódio 08.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example tool_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run adk web
```
Pergunte: *What time is it in Tokyo?* e veja a chamada da tool nos eventos.

## Roteiro do vídeo
1. O que é uma tool e como o ADK gera o schema da função.
2. Escrever `get_current_time` e ligar em `tools=[...]`.
3. Rodar com `adk web` e ver no painel de eventos a chamada da tool.
4. Docstring, type hints e retorno com `status`.
5. `ToolContext` e `temp:` (rápido, aprofunda no 06).
