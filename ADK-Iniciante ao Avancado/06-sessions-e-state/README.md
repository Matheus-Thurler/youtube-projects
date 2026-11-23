# 06-sessions-e-state

Fonte: só a doc oficial do ADK. Cada bloco aponta a página. Nada aqui vem de experiência própria.

## 1. Visão geral: Session, State e Memory
Doc: https://adk.dev/sessions/

| Conceito | O que é (segundo a doc) |
|---|---|
| `Session` | A conversa atual: sequência cronológica de `Events` (mensagens e ações) daquela interação. |
| `State` (`session.state`) | Dados dentro da sessão, relevantes só para a conversa em andamento (ex.: itens do carrinho neste chat). |
| `Memory` | Base pesquisável que pode atravessar várias sessões passadas ou fontes externas. |

Serviços: `SessionService` (ciclo de vida das sessões) e `MemoryService` (ingere e busca conhecimento de longo prazo). As implementações **in-memory** são para teste local e perdem tudo ao reiniciar.

## 2. Session
Doc: https://adk.dev/sessions/session/

- Propriedades: `id`, `app_name`, `user_id`, `events` (histórico), `state`, `last_update_time`.
- Ciclo de vida (doc): criar/retomar → o `Runner` entrega a sessão ao agente → agente responde → `Runner` empacota um `Event` → `append_event(session, event)` grava o evento e atualiza o state → sessão pronta para o próximo turno → `delete_session` ao terminar.
- Você não cria `Session` direto; usa um `SessionService` (criar, retomar, salvar progresso, listar, apagar).
- Implementações:
  - `InMemorySessionService`: sem persistência, para desenvolvimento e testes.
  - `VertexAiSessionService`: persistente, via Agent Runtime; precisa do extra `google-adk[gcp]`.
  - `DatabaseSessionService`: persistente em banco relacional; extra `google-adk[db]`; em Python exige driver assíncrono (SQLite: `sqlite+aiosqlite`).
- Erro `SessionNotFoundError`: sessão inexistente. Resolver com `create_session(...)` antes, ou `Runner(..., auto_create_session=True)`.

## 3. State
Doc: https://adk.dev/sessions/state/

- Pares chave/valor; chaves são strings; valores precisam ser serializáveis (nada de objetos de classe, funções, conexões).
- Prefixos definem escopo:
  - sem prefixo: só a sessão atual;
  - `user:`: ligado ao `user_id`, compartilhado entre as sessões do usuário no mesmo `app_name`;
  - `app:`: compartilhado entre todos os usuários e sessões do app;
  - `temp:`: só a invocação atual, não persiste (sub-agentes compartilham o mesmo `temp:`).
- Ler no prompt: `{chave}` na `instruction` injeta o valor do state; se a chave não existir dá erro, a menos que use `{chave?}`. Para chaves literais (ex.: JSON na instrução) use um `InstructionProvider` (função no lugar da string).
- Como atualizar (ordem recomendada pela doc):
  1. `output_key` no agente: grava a resposta final no state;
  2. `EventActions.state_delta` ao montar um `Event` manualmente;
  3. `callback_context.state[...]` / `tool_context.state[...]` dentro de callbacks e tools.
- Aviso da doc: não altere `session.state` de uma sessão obtida do `SessionService` fora de uma invocação; a mudança não vira `Event` e pode não ser salva. Use esse acesso só para leitura.

## 4. Memory
Doc: https://adk.dev/sessions/memory/

- Operações do `BaseMemoryService`: `add_session_to_memory`, `add_events_to_memory` e `add_memory` (as duas últimas são opcionais), e `search_memory`.
- Três implementações em Python:
  - `InMemoryMemoryService`: sem persistência, busca por palavra-chave;
  - `VertexAiMemoryBankService`: gerenciado, extrai memórias das conversas, busca semântica;
  - `VertexAiRagMemoryService`: guarda a conversa no Knowledge Engine, busca por similaridade vetorial.
- Usar no agente: ferramentas prontas **preload memory** (busca no início de cada turno) e **load memory** (o agente decide quando buscar). Para gravar, chame `add_session_to_memory`, por exemplo num callback.
- Via `adk web`/`adk api_server`, um só serviço de memória por flag `--memory_service_uri`; dentro do código dá para consultar um segundo serviço numa tool.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example chat_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run python session_demo.py   # sem LLM: escopos de state e Memory
uv run adk web                    # agente com {user:name?} e output_key
```
O `session_demo.py` roda sem chave.

## Sugestão de roteiro do vídeo
1. Os três conceitos (tabela da seção 1).
2. Session + SessionService in-memory e o ciclo de vida.
3. State: prefixos, `{chave}` na instrução, `output_key`.
4. Memory: add/search com `InMemoryMemoryService`.
