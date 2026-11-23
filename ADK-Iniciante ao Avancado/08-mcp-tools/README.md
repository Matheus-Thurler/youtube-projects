# 08-mcp-tools

Fonte: só a doc oficial do ADK.
Docs: https://adk.dev/tools-custom/mcp-tools/ · https://adk.dev/tools-custom/mcp-tools/advanced/

## 1. O que é MCP
Padrão aberto para conectar modelos generativos a fontes de dados, tools e sistemas (cliente-servidor). No ADK, a classe `McpToolset` é a interface entre servidores MCP e agentes. Também é possível expor um agente ADK como servidor MCP.

## 2. Pré-requisitos (doc)
- `pip install "google-adk[mcp]"` (extra de MCP).
- Python 3.10+; Node.js e `npx` para servidores MCP da comunidade empacotados em npm.
- **Regra de deploy:** em produção, defina o `McpToolset` de forma síncrona em `agent.py`.

## 3. Três padrões de integração (tabela da doc)
| Padrão | O que é | Observação da doc |
|---|---|---|
| `McpToolset` (integração direta) | O agente é cliente MCP | Definições e saídas das tools entram no histórico do agente principal (mais contexto); custo e latência previsíveis |
| `to_mcp_server` | Seu agente ADK vira servidor MCP | Quem chama recebe só a resposta final |
| `AgentTool` (sub-agente) | Agente pai chama um sub-agente | Sem inchar o contexto do pai; permite modelos diferentes por camada; mais chamadas ao LLM |

Detalhe: construir o toolset não conecta; a sessão MCP abre no primeiro uso (quando o agente pede as tools). O ADK não restabelece conexões MCP ao restaurar uma sessão; o agente reconecta quando precisa.

## 4. Exemplo local (stdio): servidor de filesystem
```python
McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", TARGET_FOLDER],
        ),
    ),
    tool_filter=["list_directory", "read_file"],   # opcional
)
```
Passos da doc: criar `__init__.py` ao lado do `agent.py`, rodar `adk web`, escolher `filesystem_assistant` e pedir "List files in the current directory".

## 5. Exemplo remoto (HTTP/SSE): Google Maps Grounding Lite
```python
McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mapstools.googleapis.com/mcp",
        headers={"X-Goog-Api-Key": API_KEY, "Content-Type": "application/json",
                 "Accept": "application/json, text/event-stream"},
        timeout=5, sse_read_timeout=300,
    )
)
```

## 6. Autenticação e recursos
- Para servidores remotos (SSE ou Streamable HTTP) com auth: parâmetros `auth_scheme` e `auth_credential` (Bearer, Basic, APIKey, OAuth2); o ADK monta o header `Authorization` e renova tokens OAuth 2.0. A doc também mostra `headers={"Authorization": f"Bearer ..."}` com `SseConnectionParams`.
- Recursos MCP (dados, não só tools): `list_resources()`, `read_resource(name)` e `use_mcp_resources=True` (dá ao agente a `LoadMcpResourceTool`).

## 7. Checklist de boas práticas (doc)
- **Escopo:** sempre `tool_filter=[...]` para expor só o necessário ao LLM.
- **Timeouts:** `StdioConnectionParams(timeout=5)` evita subprocessos pendurados.
- **Limpeza:** fora do `adk web`, `await toolset.close()` ou context manager.
- **Ambiente:** escolher a conexão por variável de ambiente (ex.: `K_SERVICE` = Cloud Run → HTTP; local → stdio).

## 8. Configuração avançada
Tabela da doc (página "advanced"):
| Necessidade | Parâmetro |
|---|---|
| Credencial por usuário / token dinâmico | `header_provider=...` |
| Aprovação antes de tool perigosa | `require_confirmation=...` |
| Progresso de operações longas | `progress_callback=...` |
| Rodar fora do `adk web` | `Runner` + `await toolset.close()` |
| Colisão de nomes entre servidores | `tool_name_prefix`, `tool_filter` |
| Sampling / elicitation do servidor | `sampling_callback`, `elicitation_callback` |
| STDERR do subprocesso | `errlog=sys.stderr` |

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example filesystem_assistant/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run adk web
```
Precisa de Node.js (`npx`). Peça: *List files in the current directory*. Pasta exposta: `filesystem_assistant/files/`.

## Sugestão de roteiro do vídeo
1. O que é MCP e a tabela dos 3 padrões.
2. Exemplo stdio (filesystem) no `adk web`.
3. Exemplo remoto (HTTP) com header de chave de API.
4. Boas práticas: `tool_filter`, timeout, `close()`.
