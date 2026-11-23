# 00 - O que é o ADK

Fonte: só a doc oficial do ADK: [Technical Overview](https://adk.dev/get-started/about/).

## O que é
"Build, Evaluate and Deploy agents, seamlessly!" Ambiente para criar, gerenciar, avaliar e fazer deploy de agentes de IA, conversacionais ou não, capazes de lidar com tarefas e workflows complexos.

## Conceitos centrais (doc)
| Conceito | O que é |
|---|---|
| **Agent** | Unidade de trabalho para uma tarefa. `LlmAgent` raciocina com LLM; "workflow agents" (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) controlam a execução de forma determinística |
| **Tool** | Dá ao agente habilidades além da conversa: APIs, busca, executar código, chamar serviços |
| **Callbacks** | Código seu que roda em pontos específicos do processo (checagens, log, mudar comportamento) |
| **Session & State** | `Session` é o contexto de uma conversa (histórico de `Events`); `State` é a memória de trabalho dela |
| **Memory** | Lembrar informação do usuário entre *várias* sessões |
| **Artifact** | Salvar, carregar e gerenciar arquivos e dados binários (imagens, PDFs) |
| **Code Execution** | Agente gerar e executar código (normalmente via Tools) |
| **Planning** | Quebrar um objetivo em passos, como um planner ReAct |
| **Models** | O LLM que alimenta os `LlmAgent` |
| **Event** | Unidade de comunicação: mensagem do usuário, resposta do agente, uso de tool |
| **Runner** | Motor que gerencia a execução e coordena com os serviços de backend |

## Capacidades principais (doc)
1. Sistemas multi-agente (hierarquia, `transfer` por LLM ou `AgentTool`)
2. Ecossistema de tools (`FunctionTool`, `AgentTool`, code execution, long-running)
3. Orquestração flexível (workflow agents + roteamento dirigido por LLM)
4. Ferramentas de desenvolvimento (CLI e Developer UI)
5. Streaming nativo (agentes live e de voz)
6. Avaliação embutida
7. Suporte amplo a LLMs (otimizado para Gemini; outros via `BaseLlm`)
8. Gerenciamento de artifacts
9. Extensibilidade e interoperabilidade
10. State e Memory

## Mapa da série
| Episódio | Peça do ADK |
|---|---|
| 01 | Agent, instalação, `adk run`/`adk web` |
| 02 | Tool (function tools) |
| 03 | Models (outros LLMs) |
| 04 | `output_schema` / `output_key` |
| 05 | Multi-agent |
| 06 | Session, State, Memory |
| 07 | Grounding / RAG |
| 08 | MCP |
| 09 | Workflow agents e graph `Workflow` |
| 10 | Callbacks, plugins, safety |
| 11 | Observability |
| 12 | Evaluation |
| 13 | Runner, Event Loop, Events, RunConfig, Resume |
| 14 | App, contexto, context caching e compaction |
| 15 | Artifacts |
| 16 | API Server e FastAPI (`get_fast_api_app`) |
| 17 | A2A (agent2agent) |
| 18 | agents-cli |
| 19 | Deploy (Cloud Run, GKE, Agent Runtime) |
| 20 | Projeto final |

## Roteiro do vídeo
1. O que o ADK resolve (construir, avaliar, fazer deploy).
2. Passar pelos conceitos da tabela, um por um, sem código.
3. Apresentar o mapa da série.
