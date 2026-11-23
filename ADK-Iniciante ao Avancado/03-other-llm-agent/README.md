# 03 - Agente com outro LLM

Fonte: só a doc oficial do ADK: [Models](https://adk.dev/agents/models/), [LiteLLM](https://adk.dev/agents/models/litellm/), [Ollama](https://adk.dev/agents/models/ollama/).

## Três formas de integrar um modelo (doc)
1. **String / registry:** nome do modelo ou endpoint resolvido pelo registry do ADK. Gemini, Claude, modelos hospedados na Agent Platform.
2. **Model connectors:** classe wrapper passada em `model=`. Apigee (`ApigeeLlm`), LiteLLM (`LiteLlm`), Ollama, vLLM, LiteRT-LM.
3. **Model routing:** escolher entre vários modelos em runtime com uma função router, com failover automático em erro: https://adk.dev/agents/models/routing/

## LiteLLM (doc)
Camada de tradução com interface compatível com OpenAI para 100+ LLMs (OpenAI, Anthropic, Ollama, Mistral, DeepSeek, Cohere...).

Instalar (o ADK exige `litellm>=1.84`):
```shell
pip install "litellm>=1.84"
```
Chaves por variável de ambiente, por exemplo:
```shell
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY"
```
Nomes das variáveis de outros provedores: https://docs.litellm.ai/docs/providers

```python
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

agent_openai = LlmAgent(
    model=LiteLlm(model="openai/gpt-4o"),  # LiteLLM model string format
    name="openai_agent",
    instruction="You are a helpful assistant powered by GPT-4o.",
)

agent_claude_direct = LlmAgent(
    model=LiteLlm(model="anthropic/claude-3-haiku-20240307"),
    name="claude_direct_agent",
    instruction="You are an assistant powered by Claude Haiku.",
)
```

> **Aviso na doc:** houve um comprometimento de supply chain no LiteLLM (versões 1.82.7 e 1.82.8 no PyPI, 24/03/2026). Leia o aviso antes de instalar: https://adk.dev/agents/models/litellm/

## Modelo local com Ollama (doc)
O ADK integra o Ollama pelo conector LiteLLM:
```python
root_agent = Agent(
    model=LiteLlm(model="ollama_chat/gemma3:latest"),
    name="dice_agent",
    description="hello world agent that can roll a dice of 8 sides and check prime numbers.",
    instruction="You roll dice and answer questions about the outcome of the dice rolls.",
    tools=[roll_die, check_prime],
)
```
- Use o provider `ollama_chat`, **não** `ollama` (a doc diz que `ollama` pode causar loops infinitos de tool call e ignorar o contexto anterior).
- Defina `OLLAMA_API_BASE` (ex.: `http://localhost:11434`) para todas as requisições irem ao servidor certo.
- Para usar tools, escolha um modelo com suporte a tools (`ollama show <modelo>` lista "Capabilities").

## Tutorial da doc
O Step 2 do tutorial Agent Team usa LiteLLM para trocar de modelo (motivos citados: desempenho, custo, capacidades, disponibilidade/redundância): https://adk.dev/tutorials/agent-team/

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example llm_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run adk web
```
Troque o modelo com `LLM_MODEL` no `.env` (padrão: Ollama local; precisa do Ollama rodando).

## Roteiro do vídeo
1. Por que trocar de modelo (os 4 motivos da doc).
2. Registry vs connectors vs routing.
3. `LiteLlm(model="openai/...")` com a chave no ambiente.
4. Modelo local com Ollama (`ollama_chat/...` + `OLLAMA_API_BASE`).
5. Comparar a resposta do mesmo agente com modelos diferentes no `adk web`.
