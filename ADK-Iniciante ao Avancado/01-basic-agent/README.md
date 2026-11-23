# 01-basic-agent

Primeiro agente com ADK em Python.

Fonte: https://adk.dev/get-started/python/ e https://adk.dev/get-started/installation/.
A doc usa `pip` + `venv`. Os passos com **uv** abaixo são a versão equivalente (uv não está na doc do ADK).

## Pré-requisitos (doc)
- Python 3.10 ou superior
- Chave do Gemini: https://aistudio.google.com/app/apikey

## 1. Criar o projeto com uv

```shell
uv init
uv add google-adk
```

- `uv init` cria `pyproject.toml`, `.python-version` e `main.py`.
- `uv add google-adk` cria `.venv` e `uv.lock` e instala o ADK.

Doc (equivalente com pip): `python3 -m venv .venv` → ativar → `pip install google-adk`.
Verificar a instalação (doc): `pip show google-adk` (com uv: `uv pip show google-adk`).

## 2. Criar o agente

```shell
uv run adk create my_agent
```

Estrutura gerada (doc):

```text
my_agent/
    agent.py      # main agent code
    .env          # API keys or project IDs
    __init__.py
```

`root_agent` em `agent.py` é o único elemento obrigatório de um agente ADK.

## 3. Editar o `agent.py` (código da doc)

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

## 4. Chave da API

Dentro de `my_agent/`, no `.env`:

```bash
echo 'GOOGLE_API_KEY="YOUR_API_KEY"' > .env
```

Outros modelos: https://adk.dev/agents/models

## 5. Rodar

Terminal:

```shell
uv run adk run my_agent
```

Interface web (rodar da pasta **pai** de `my_agent/`):

```shell
uv run adk web --port 8000
```

Abre em http://localhost:8000; escolha o agente no canto superior esquerdo.
A doc avisa: ADK Web é só para desenvolvimento e depuração, nunca produção.

## Roteiro do vídeo
1. `uv init` + `uv add google-adk` (mostrar `.venv`, `pyproject.toml`, `uv.lock`).
2. `adk create` e a estrutura gerada.
3. `root_agent` e os campos `model`, `name`, `description`, `instruction`, `tools`.
4. `.env` com a chave.
5. `adk run` e `adk web`.
