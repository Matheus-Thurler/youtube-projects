# 20-time-sre

Projeto final: junta as peças dos episódios anteriores. **O cenário SRE é um exemplo escolhido por você, não vem da doc do ADK**; cada peça de ADK abaixo aponta para a página que a explica.

## Arquitetura (o que foi feito antes)
Alerta → métricas, logs e runbook em paralelo → dashboard → relatório.

| Peça | Episódio | Doc |
|---|---|---|
| Agentes em sequência e em paralelo; passar resultado pelo state com `output_key` | `09-workflow-agents`, `06-sessions-e-state` | https://adk.dev/agents/workflow-agents/ |
| Tools do Grafana via MCP, `tool_filter` por agente | `08-mcp-tools` | https://adk.dev/tools-custom/mcp-tools/ · https://adk.dev/integrations/grafana-cloud/ |
| Base de conhecimento (runbooks e livro) | `07-rag` | https://adk.dev/grounding/ · https://adk.dev/integrations/qdrant/ |
| Bloquear conteúdo suspeito vindo de tools | `10-callbacks-e-plugins` | https://adk.dev/plugins/ · https://adk.dev/safety/ |
| Confirmação humana antes de ação de risco | `10-callbacks-e-plugins` | https://adk.dev/tools-custom/confirmation/ |
| Medir o agente | `11-observability` | https://adk.dev/observability/ |
| Avaliar com casos de incidente | `12-avaliacao-eval` | https://adk.dev/evaluate/ |
| Servidor FastAPI e deploy | `16-api-server-e-fastapi`, `19-deploy` | https://adk.dev/runtime/api-server/ |
| Estrutura de projeto | `18-agents-cli` | https://adk.dev/get-started/agents-cli/ |

## Pontos de atenção segundo a doc
- Template workflows (Sequential/Parallel/Loop) estão marcados como deprecated em favor de workflows de grafo (`JoinNode` para juntar ramos paralelos): https://adk.dev/graphs/routes/
- `McpToolset`: use `tool_filter`; em produção defina de forma síncrona em `agent.py`.
- Saída de tool pode carregar prompt injection indireta (https://adk.dev/safety/).
- Doc do Grafana MCP **hospedado** (Grafana Cloud): `https://mcp.grafana.com/mcp`, OAuth 2.1, acesso de leitura sempre disponível e escrita opcional. O servidor local em Docker (`grafana/mcp-grafana`) é do repositório da Grafana, não da doc do ADK.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example sre_team/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run adk web
```
Tools falsas (dados fixos). Alerta de exemplo: *Alerta: pagamentos-api com latência alta*.

## Sugestão de roteiro do vídeo
1. Desenho do time (alerta → especialistas → relatório).
2. Montar com as peças já vistas, uma a uma.
3. Rodar com um alerta e acompanhar no `adk web`/playground (state, eventos).
4. Medir e avaliar.
