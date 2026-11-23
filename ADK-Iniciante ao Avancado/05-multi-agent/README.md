# 05 - Multi-agent

Fonte: só a doc oficial do ADK: [Agent team (tutorial)](https://adk.dev/tutorials/agent-team/), [Collaborative agent teams](https://adk.dev/workflows/collaboration/), [LlmAgent](https://adk.dev/agents/llm-agents/), [Overview](https://adk.dev/get-started/about/).

## Por que um time de agentes (doc, tutorial Step 3)
Em vez de um agente único com tools e instruções cada vez maiores:
1. Vários agentes **especializados**.
2. Um **root agent** (orquestrador) que recebe o pedido.
3. O root **delega** ao sub-agente certo conforme a intenção do usuário.

Vantagens citadas: modularidade, especialização (instruções e modelo por tarefa), escalabilidade e eficiência (modelos mais simples/baratos para tarefas simples).

## Como o root escolhe (doc)
- `name` é usado internamente para um agente referenciar/delegar a outro.
- `description` é usada principalmente por *outros* agentes LLM para decidir se devem rotear a tarefa. A doc pede que seja específica o bastante para diferenciar dos pares ("Handles inquiries about current billing statements", não só "Billing agent").

## Time com modos (doc, ADK Python 2.0 / Go 2.0)
```python
from google.adk import Agent

weather_agent = Agent(
    name="weather_checker",
    mode="single_turn",         # no user interaction
    tools=[get_weather, user_info, geocode_address],
)
flight_agent = Agent(
    name="flight_booker",
    mode="task",                # can ask user questions
    input_schema=FlightInput,
    output_schema=FlightResult,
    tools=[search_flights, book_flight],
)
root = Agent(
    name="travel_planner",      # coordinator agent
    sub_agents=[weather_agent, flight_agent],
    # Auto-injects delegation tools named after each subagent
)
```

| | `chat` (default) | `task` | `single_turn` |
|---|---|---|---|
| Interação com usuário | Livre | Só para esclarecimento | Nenhuma |
| Controle | Até handoff manual | Até a tarefa terminar | Retorna após a tarefa |
| Execução paralela | Não | Não | Sim |
| Retorno ao pai | Manual (`transfer`) | Automático (`finish_task`) | Automático (com resultado) |

Regras da doc:
- `mode` é só para sub-agentes; **não** configure o root com `mode`.
- Agentes `task` e `single_turn` rodam em branch de sessão isolado; em paralelo não enxergam os eventos dos pares.
- Agentes `task` devem ser folhas (sem sub-agentes).
- Modo `task` está desativado em workflows baseados em grafo no ADK Python 2.0.0.

## Agente como tool (doc)
`AgentTool` embrulha outro agente para delegação. A doc do `LlmAgent` diz que, em Python, é preferível `mode='single_turn'` + `sub_agents`, evitando `AgentTool(agent=...)` direto.

## Configuração de transferência e regras globais (doc)
`disallow_transfer_to_parent`, `disallow_transfer_to_peers`; regras comuns a todos os agentes com `GlobalInstructionPlugin`: https://adk.dev/workflows/collaboration/

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`. A chave fica em `team_agent/.env` (modelo em `.env.example`).

```shell
uv run adk web
```
Escolha `team_agent`. Diga *Hi!* ou *Bye!* e veja, nos eventos, o `coordinator` delegando ao sub-agente. `team_agent/agent.py`: root + dois especialistas, cada um com `description` clara.

## Roteiro do vídeo
1. Limite do agente único e por que dividir.
2. Criar 2 sub-agentes com `name` e `description` claros.
3. Root com `sub_agents=[...]` e ver a delegação no `adk web` (eventos).
4. Modos `chat`, `task`, `single_turn` (tabela).
5. Ligação com o episódio 09 (workflow agents) para fluxos fixos.
