# 15 - Artifacts

Fonte: só a doc oficial do ADK: [Artifacts](https://adk.dev/artifacts/), [Agent context](https://adk.dev/context/).

## O que são (doc)
Dados binários **nomeados e versionados**, associados a uma sessão ou, de forma persistente, a um usuário em várias sessões. Permitem lidar com arquivos, imagens, áudio e outros formatos, não só texto.

- Identificados por um `filename` único dentro do escopo (sessão ou usuário).
- Cada `save` com o mesmo nome cria uma **nova versão**.
- Representados por `google.genai.types.Part`, normalmente com `inline_data` (`data` em bytes + `mime_type`).

```python
import google.genai.types as types

image_artifact = types.Part(
    inline_data=types.Blob(
        mime_type="image/png",
        data=image_bytes
    )
)
# convenience constructor:
# types.Part.from_bytes(data=image_bytes, mime_type="image/png")
```

## Artifact Service (doc)
`BaseArtifactService` define *como e onde* persistir. Operações: salvar (retorna a versão), carregar (versão específica ou a mais recente), listar nomes, apagar, listar versões.

Implementações citadas: `InMemoryArtifactService` (teste/temporário), `GcsArtifactService` (Google Cloud Storage, persistente) e, em Kotlin, `FileArtifactService`.

Configura-se no `Runner`:
```python
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService  # Or GcsArtifactService
from google.adk.sessions import InMemorySessionService

runner = Runner(
    agent=agent,
    app_name="artifact_app",
    session_service=InMemorySessionService(),
    artifact_service=InMemoryArtifactService()  # Service must be provided here
)
```

## Versionamento e escopo (doc)
- `save_artifact` devolve o número da versão (começa em 0).
- `load_artifact(..., version=None)` traz a mais recente; `version=N` traz a versão N.
- **Escopo de sessão:** nome simples (`"report.pdf"`) fica preso a `app_name` + `user_id` + `session_id`.
- **Escopo de usuário:** prefixo `"user:"` (`"user:profile.png"`) vale para qualquer sessão do usuário naquele app.

## Usando no código (doc)
Pelos objetos de contexto, em callbacks e tools (`CallbackContext` / `ToolContext`): `save_artifact`, `load_artifact`. É **obrigatório** configurar o `ArtifactService` no `Runner`.

O `artifact_delta` no evento confirma a ação para o `Runner`/`SessionService` (episódio 13).

## Usos comuns (doc)
Compartilhar saídas (PDF, imagem) geradas por tools; persistir arquivos entre sessões com `user:`; guardar dados grandes fora do state.

## Deploy
Sem `--artifact_service_uri`, o container no Cloud Run usa artifacts em memória e **perde** tudo quando a instância é reciclada (doc de deploy; episódio 19).

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

```shell
uv run python main.py
```
Sem LLM: versões, `load_artifact(version=...)` e o escopo `user:`.

## Roteiro do vídeo
1. Por que não colocar binário no state.
2. `types.Part` com `inline_data`.
3. `InMemoryArtifactService` no `Runner`; salvar e carregar numa tool.
4. Versões e o prefixo `user:`.
5. Ver o `artifact_delta` no evento (ponte para o 13).
