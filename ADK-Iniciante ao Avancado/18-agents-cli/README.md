# 18-agents-cli

Fonte: só a doc oficial do ADK.
Docs: https://adk.dev/get-started/agents-cli/ · https://adk.dev/runtime/web-interface/ · https://adk.dev/runtime/command-line/

## 1. O que é
Conjunto de CLI + skills para **construir, avaliar e fazer deploy** de agentes ADK com coding agents (Antigravity, Claude Code, Codex). A doc recomenda usar quando você planeja testar, avaliar e fazer deploy; para um agente de arquivo único, só para aprender ADK, use `adk create`.

## 2. Pré-requisitos (doc)
- Python 3.11+, `uv`, Node.js (para instalar as skills), um coding agent.
- Para deploy no Google Cloud: Google Cloud CLI e Terraform.

## 3. Instalação
```shell
uvx google-agents-cli setup
```
Alternativas: `pipx install google-agents-cli && agents-cli setup`, `pip install google-agents-cli && agents-cli setup`, ou só as skills: `npx skills add google/agents-cli`.

## 4. Autenticação
- Mais simples: chave do Google AI Studio no `.env`: `GEMINI_API_KEY=YOUR_API_KEY`, e comentar as três linhas `GOOGLE_CLOUD_*`.
- Alternativa: Application Default Credentials (`gcloud auth application-default login`) com as linhas `GOOGLE_CLOUD_*` preenchidas.

## 5. Construir
Peça ao coding agent (exemplo da doc): "Use agents-cli to build an agent that turns long text into short bullet-point summaries". As skills `google-agents-cli-workflow` e `google-agents-cli-scaffold` fazem perguntas e criam o projeto; a skill `google-agents-cli-adk-code` escreve `app/agent.py`.

Estrutura gerada (doc):
```text
my-agent/
    app/agent.py            # código do agente
    app/fast_api_app.py     # servidor, telemetria e rotas
    app/app_utils/          # serviços de sessão e artifacts
    tests/eval/             # datasets e métricas de avaliação
    tests/integration/
    tests/unit/
    pyproject.toml
    agents-cli-manifest.yaml
    Dockerfile
    GEMINI.md               # guia para coding agents
    .env
```

## 6. Rodar
(`app/fast_api_app.py` é o servidor FastAPI visto no episódio 16.)

```console
agents-cli playground
```
Sobe a interface web do ADK com hot reload (doc: http://localhost:8080).

## 7. Interface web e CLI do ADK
- `adk web` (https://adk.dev/runtime/web-interface/): chat, gerenciamento de sessões, **inspeção e edição do state**, histórico de eventos, Visual Builder (só Python). **Só para desenvolvimento, nunca produção.** Opções: `--port` (8000), `--host` (127.0.0.1), `--session_service_uri`, `--artifact_service_uri`, `--reload`.
- `adk run` (https://adk.dev/runtime/command-line/): terminal interativo; `--save_session`, `--resume`, `--replay`, `--state`, `--timeout`, `--in_memory`, `--jsonl`, `--memory_service_uri` etc.

## 8. Próximos passos (doc)
- "Write evals for this agent and run them" → avaliação.
- "Deploy this to Cloud Run" → Agent Runtime, Cloud Run ou GKE (https://adk.dev/deploy/agent-runtime/agents-cli/).
- "Set up observability infrastructure for my agent" → logging de prompt/resposta.

## Sugestão de roteiro do vídeo
1. `agents-cli` vs `adk create`: quando usar cada um.
2. Instalar, autenticar com a chave do AI Studio.
3. Pedir o agente ao coding agent; ver a estrutura gerada.
4. `agents-cli playground` e o que a UI mostra (state, eventos).
