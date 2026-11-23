# 10-callbacks-e-plugins

Fonte: só a doc oficial do ADK.
Docs: https://adk.dev/callbacks/ · https://adk.dev/callbacks/types-of-callbacks/ · https://adk.dev/plugins/ · https://adk.dev/safety/ · https://adk.dev/tools-custom/confirmation/

## 1. Callbacks
- Funções suas, associadas ao agente na criação; o ADK as chama em pontos definidos. Servem para observar/depurar, customizar/controlar, guardrails, gerenciar state e integrar ações externas.
- Recebem um objeto de contexto (`CallbackContext` ou `ToolContext`) com invocação, state e acesso a serviços (artifacts, memory).
- **O valor de retorno controla o fluxo:**
  - `None`: segue o comportamento padrão.
  - objeto específico: substitui/pula a etapa.

| Callback | Quando | Retorno que altera o fluxo |
|---|---|---|
| `before_agent_callback` | antes do trabalho do agente | `Content`: pula o agente e vira a saída final |
| `after_agent_callback` | depois do agente | `Content`: é **anexado** como evento extra (não substitui) |
| `before_model_callback` | antes de chamar o LLM | `LlmResponse`: pula o LLM (guardrail de entrada, cache) |
| `after_model_callback` | depois da resposta do LLM | `LlmResponse`: **substitui** a resposta |
| `before_tool_callback` | antes da tool | `dict`: pula a tool e vira o resultado |
| `after_tool_callback` | depois da tool | `dict`: **substitui** o resultado |
| `on_model_error_callback` / `on_tool_error_callback` | exceção no modelo/tool | `LlmResponse` / `dict`: suprime a exceção |

- Em Python os parâmetros têm nomes obrigatórios (chamada por palavra-chave): `callback_context`, `llm_request`, `llm_response`, `tool`, `args`, `tool_context`, `tool_response`, `error`. Renomear dá `TypeError`.
- Só `before_agent` e `after_agent` existem em todo `BaseAgent`; os de modelo e tool são do `LlmAgent`.
- Em `before_tool_callback`, retornar `{}` conta como override (a tool não roda): para deixar rodar, retorne `None`.
- Dica da doc: para guardrails de segurança, prefira **Plugins** a callbacks.

## 2. Plugins
Doc: https://adk.dev/plugins/

- Um Plugin estende `BasePlugin`, com um ou mais métodos de callback; é registrado **uma vez** (no `Runner` ou, em Python, no `App`) e vale para todos os agentes, modelos e tools.
- Em Python use `App(plugins=...)`; `Runner(plugins=...)` está deprecated e passar os dois dá `ValueError`. Também dá para carregar com `--extra_plugins` no `adk web` / `adk api_server`.
- Usos listados: logging e tracing, policy enforcement, métricas, cache de respostas, modificação de requisição/resposta.
- Três modos pelo retorno do hook: **observar** (`None`), **intervir** (retornar valor interrompe e usa o retorno como resultado), **ajustar** (modificar o contexto).
- Plugins rodam **antes** dos callbacks do agente; se o plugin retornar algo diferente de `None`, o callback do agente não executa.
- Vários plugins: executam na ordem da lista e param no primeiro que retornar valor; cada um precisa de `name` único.
- Hooks: `on_user_message_callback`, `before_run_callback`/`after_run_callback`, `before_agent`/`after_agent`, `before_model`/`after_model`/`on_model_error`, `before_tool`/`after_tool`/`on_tool_error`, `on_event_callback`.
- Plugins prontos citados: Reflect and Retry Tools, BigQuery Analytics, Model Armor, Context Filter, Global Instruction, Save Files as Artifacts, Auto Tracing, Multimodal Tool Results, Logging, Debug Logging, Reflect and Retry Model, Tool Call Integrity.

| | Plugins | Callbacks de agente |
|---|---|---|
| Escopo | global (todo o Runner/App) | local (a instância do agente) |
| Uso | logging, política, monitoramento, cache | lógica específica do agente |
| Ordem | rodam antes | rodam depois |

## 3. Segurança
Doc: https://adk.dev/safety/

- Fontes de risco: instruções ambíguas, prompt injection e jailbreak de usuários adversários, **prompt injection indireta via uso de tools**.
- Camadas: identidade e autorização (auth do agente vs. auth do usuário/OAuth), guardrails de entrada/saída, execução de código em sandbox, avaliação e tracing, VPC-SC e controles de rede.
- Guardrails: **in-tool** (a tool lê a política do `ToolContext`, definida pelo desenvolvedor, não pelo modelo), filtros do Gemini, `before_tool_callback`, plugins, e Gemini Flash Lite como juiz.
- Exemplos de plugins de segurança na doc: *Gemini as a Judge*, **Model Armor** (acompanha o ADK, https://adk.dev/integrations/model-armor/), redação de PII.
- Sempre escapar conteúdo gerado pelo modelo em UIs (risco de execução de HTML/JS).

## 4. Confirmação humana de tool
Doc: https://adk.dev/tools-custom/confirmation/

- Confirmação booleana: embrulhar a tool com `FunctionTool(..., require_confirmation=True)`.
- `require_confirmation` também aceita uma função que decide com base nos argumentos.
- Confirmação avançada: `tool_context.request_confirmation(hint=..., payload=...)`; a execução pausa até a resposta.
- Sem UI: responder via REST com um `FunctionResponse` de nome `adk_request_confirmation`, `id` igual ao `function_call_id`, e `response` com `confirmed`.
- Limitação listada: `DatabaseSessionService` não é suportado.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example guard_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run python check.py   # sem LLM
uv run adk web
```
Digite uma frase com BLOQUEAR para ver o guardrail; o plugin imprime a contagem de tools no terminal.

## Sugestão de roteiro do vídeo
1. Os seis callbacks e a regra `None` vs objeto.
2. Guardrail com `before_model_callback` e `before_tool_callback`.
3. Mesmo guardrail como Plugin no `App`; diferença de escopo e ordem.
4. Seção de segurança: injeção indireta via tools; Model Armor como opção pronta.
5. `require_confirmation` antes de uma tool de risco.
