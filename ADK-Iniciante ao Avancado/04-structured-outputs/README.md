# 04 - Structured outputs

Fonte: só a doc oficial do ADK: [LlmAgent, "Structure data input and output"](https://adk.dev/agents/llm-agents/).

## Parâmetros (doc)
- **`output_schema`:** estrutura desejada da saída. Se definido, a resposta final do agente **deve** ser uma string JSON conforme o schema.
- **`output_key`:** se definido, a resposta final é salva no `state` da sessão sob essa chave (`session.state[output_key]`). Útil para passar resultado entre agentes ou etapas de um workflow.
- **`input_schema`:** estrutura de entrada esperada quando o agente é invocado **como tool**. No Python, o `AgentTool` valida os argumentos do agente chamador. Não vale para mensagens do usuário enviadas direto ao agente.

## Tipos de schema aceitos em Python (doc)
- Classe Pydantic (`BaseModel`)
- Listas de primitivos: `list[str]`, `list[int]`, `list[bool]`, `list[float]`
- `dict`
- `google.genai.types.Schema`

## Exemplo da doc
```python
from pydantic import BaseModel, Field

class CapitalOutput(BaseModel):
    capital: str = Field(description="The capital of the country.")

structured_capital_agent = LlmAgent(
    # ... name, model, description
    instruction="""You are a Capital Information Agent. Given a country, respond ONLY with a JSON object containing the capital. Format: {"capital": "capital_name"}""",
    output_schema=CapitalOutput, # Enforce JSON output
    output_key="found_capital"  # Store result in state['found_capital']
)
```

## O que acontece com `output_key` + `output_schema` (doc)
- Python: o ADK valida a resposta contra o schema e guarda o valor **já parseado** (um `BaseModel` vira `dict`; `list[BaseModel]` vira `list[dict]`).
- Se a validação falhar, o ADK registra o erro e guarda a string crua sob `output_key` (descrito na doc para Java/Kotlin).
- Python valida contra um modelo Pydantic, que **aplica** as constraints declaradas nele.

## `output_schema` junto com `tools` (doc)
Em Python é suportado: as tools continuam disponíveis e o schema vale só para a resposta final. Alguns modelos aceitam os dois na mesma requisição (ex.: Gemini no Google Cloud, `LiteLlm` cujo provedor suporta response schema). Para os outros, o ADK adiciona uma tool `set_model_response` e instrui o modelo a responder por ela, o que "may not work reliably". Nesse caso a doc sugere sub-agentes que cuidam só da formatação.

## `generate_content_config` (doc)
Em Python, o ADK levanta `ValueError` se `generate_content_config` definir `tools`, `system_instruction`, `response_schema` ou `http_options.base_url`. Use os campos `tools`, `instruction` e `output_schema` do agente.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example capital_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run adk web
```
Pergunte um país; a resposta é JSON e o state ganha `found_capital`.

## Roteiro do vídeo
1. Resposta em texto livre vs JSON previsível.
2. Pydantic `BaseModel` + `output_schema`.
3. `output_key` e ver o valor no state no `adk web`.
4. `output_schema` com `tools` e a ressalva da doc.
5. `input_schema` quando o agente é usado como tool (ponte para o episódio 05).
