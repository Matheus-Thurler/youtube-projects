# 09-workflow-agents

Fonte: só a doc oficial do ADK.
Docs: https://adk.dev/agents/workflow-agents/ · https://adk.dev/graphs/ · https://adk.dev/graphs/routes/

> **Aviso da doc:** em ADK Python, TypeScript, Go e Kotlin, os *template workflows* (Sequential, Parallel, Loop) estão marcados como **deprecated**: foram superados pelos **workflows baseados em grafo** e pelos **workflows dinâmicos**. A doc ainda lista os três estilos como complementares (grafo, dinâmico, agentes prontos). Vale mostrar os dois no vídeo, deixando claro isso.

## Parte A. Template workflows (agentes prontos)
Orquestram sub-agentes **sem consultar um modelo** para decidir o fluxo: execução determinística.

### SequentialAgent
Doc: https://adk.dev/agents/workflow-agents/sequential-agents/
- Executa os sub-agentes na ordem da lista, passando o **mesmo `InvocationContext`** (mesmo state, inclusive `temp:`).
- A saída de cada um passa ao próximo gravando no state via `output_key`, lida na instrução com `{chave}`.
- Exemplo da doc: Code Writer → Code Reviewer → Code Refactorer.

### ParallelAgent
Doc: https://adk.dev/agents/workflow-agents/parallel-agents/
- Inicia o `run_async()` de todos os sub-agentes ao mesmo tempo.
- Cada um roda em **branch própria**: não há compartilhamento automático do histórico da conversa; mas o **session state é compartilhado** (o que um grava via `output_key` é visível para os outros e para agentes posteriores).
- O `ParallelAgent` não junta os resultados numa lista; ele emite os eventos conforme chegam (ordem não determinística). Para usar o resultado, leia do state (`output_key`).
- A doc recomenda não depender de uma branch ler uma chave que outra ainda está escrevendo.
- Exemplo da doc: três pesquisadores (energia renovável, veículos elétricos, captura de carbono).

### LoopAgent
Doc: https://adk.dev/agents/workflow-agents/loop-agents/
- Repete os sub-agentes até `max_iterations` ou até um sub-agente sinalizar `escalate`. Em Python, `max_iterations` é `None` por padrão: sem `escalate`, o loop não para.
- `escalate`: evento com `actions=EventActions(escalate=True)`, ou `callback_context.actions.escalate = True` / `tool_context.actions.escalate = True`.
- Exemplo da doc: Writer + Critic com tool `exit_loop`, no máximo 5 iterações.

## Parte B. Workflows baseados em grafo (ADK 2.0)
Doc: https://adk.dev/graphs/ · rotas: https://adk.dev/graphs/routes/

- O processo vira um grafo de **nós** (agente, tool, função sua, entrada humana, outro `Workflow`) e **arestas** (`edges`). Combina raciocínio de IA com código determinístico.
- Vantagens segundo a doc: lógica precisa de transição, ramificação e estado, cadeias de funções sem IA, mais previsibilidade que prompts longos.
- Exemplo sequencial da doc (Python):

```python
from google.adk import Agent, Workflow, Event

root_agent = Workflow(
    name="root_agent",
    edges=[("START", city_generator_agent, lookup_time_function,
            city_report_agent, completed_message_function)],
)
```
- **Rotas condicionais:** uma função devolve `Event(route=...)` e a aresta mapeia cada valor ao nó:

```python
def router(node_input: str):
    return Event(route=[r.strip() for r in node_input.split(",")])

Workflow(name="routing_workflow", edges=[
    ("START", process_message, router),
    (router, {"BUG": response_1_bug, "CUSTOMER_SUPPORT": response_2_support,
              "LOGISTICS": response_3_logistics}),
])
```
  Valores de rota podem ser string, número ou booleano; `DEFAULT_ROUTE` pega o que não casou; lista de rotas dispara todas as ramificações.
- **Fan-out e join:** várias linhas começando em `"START"` criam caminhos paralelos; `JoinNode` espera todos os predecessores e passa ao sucessor um dicionário indexado pelo nome do nó. Todo nó que alimenta um join precisa produzir saída.

```python
from google.adk.workflow import JoinNode
my_join_node = JoinNode(name="my_join_node")
edges=[("START", parallel_task_A, my_join_node),
       ("START", parallel_task_B, my_join_node),
       ("START", parallel_task_C, my_join_node),
       (my_join_node, final_task_D)]
```
- **Workflows aninhados:** um `Workflow` é um nó; no máximo um nó terminal com saída (senão `ValueError`; una os ramos com `JoinNode`).
- **Loop no grafo:** uma aresta de volta (back-edge) a um nó anterior; todo ciclo precisa de ao menos uma aresta condicional.
- Agente como nó roda em modo `single_turn` por padrão; modo `chat` só logo após `START`.
- Limitação: algumas integrações de terceiros podem não funcionar com grafos.
- Outras páginas: https://adk.dev/graphs/data-handling/ · https://adk.dev/graphs/dynamic/ · https://adk.dev/graphs/human-input/ · https://adk.dev/graphs/retry/

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example workflow_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run adk web   # escolha workflow_agent (template) ou graph_agent (grafo)
```
`graph_agent` usa só funções (sem LLM): *deu erro no checkout* vai para a rota BUG.

## Sugestão de roteiro do vídeo
1. Template workflows: um exemplo de cada (Sequential, Parallel, Loop) e o aviso de deprecação.
2. Mesmo problema como `Workflow` de grafo: sequência, depois rota condicional.
3. Fan-out + `JoinNode`.
