# 07-rag

Fonte: só a doc oficial do ADK. A teoria geral de RAG (chunking, rerank, etc.) **não** está na doc do ADK; ela fica em `../variacoes-rag.md`, que foi escrito fora da doc.

## 1. Grounding: onde o RAG entra no ADK
Doc: https://adk.dev/grounding/

Grounding conecta o agente a fontes externas para respostas mais corretas, atuais e verificáveis, reduzindo alucinação. A doc lista:
- **Google Search Grounding**: informação em tempo real da web.
- **Grounding with Search**: documentos privados da organização (datastores do Agent Search).
- **Agentic RAG**: o agente decide como buscar, montando consultas e filtros dinamicamente (Agent Retrieval, Knowledge Engine ou outros sistemas).
- Exemplos citados: artigo "10-minute Agentic RAG with Vector Search 2.0 and ADK" e o agente `deep-search` do `adk-samples`.

## 2. Opção local mais simples: `FilesRetrieval`
Doc: https://adk.dev/integrations/filesretrieval/

- Indexa uma pasta local (texto, Markdown, código) com um `VectorStoreIndex` do LlamaIndex, usando embedding do Gemini.
- Instalação: `pip install "google-adk[extensions]"`; credencial do Google AI Studio (chave de API) ou do Agent Platform.
- O agente enxerga uma função, `search_documents(query)`, que devolve o trecho mais relevante.
- Parâmetros: `name`, `description`, `input_dir` (obrigatórios) e `embedding_model` (opcional; padrão `GoogleGenAIEmbedding(model_name="gemini-embedding-2-preview", embed_batch_size=1)`).
- A pasta precisa existir ao construir a tool, e é reindexada toda vez que o módulo do agente é importado.
- A doc avisa: o conteúdo é enviado ao modelo de embedding; revise os termos antes de indexar dado sensível.

```python
files_retrieval = FilesRetrieval(
    name="search_documents",
    description="Search through local documentation files ...",
    input_dir=DATA_DIR,
)
root_agent = Agent(model="gemini-flash-latest", name="files_retrieval_agent",
                   instruction="...", tools=[files_retrieval])
```

## 3. Vector DB via MCP: Qdrant
Doc: https://adk.dev/integrations/qdrant/

- O MCP Server do Qdrant dá ao agente busca semântica (memória, índice de código, base de conhecimento/RAG).
- Pré-requisito: Qdrant rodando (Qdrant Cloud ou `docker run -p 6333:6333 qdrant/qdrant`).
- Tools expostas: `qdrant-store` (guarda informação com metadados) e `qdrant-find` (busca em linguagem natural).
- Configuração por variáveis: `QDRANT_URL`, `QDRANT_API_KEY`, `COLLECTION_NAME`, `QDRANT_LOCAL_PATH`, `EMBEDDING_MODEL` (padrão `sentence-transformers/all-MiniLM-L6-v2`), `EMBEDDING_PROVIDER` (`fastembed` ou `ollama`), `TOOL_STORE_DESCRIPTION`, `TOOL_FIND_DESCRIPTION`.
- Conexão do exemplo da doc: `McpToolset` com `StdioConnectionParams` e `StdioServerParameters(command="uvx", args=["mcp-server-qdrant"], env={...})`.

## 4. Como o MCP se encaixa
Ver `../08-mcp-tools/`.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example rag_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run adk web
```
`FilesRetrieval` gera embeddings ao carregar o agente, então a chave precisa estar válida já na abertura. Docs indexados: `rag_agent/docs/`.

## Sugestão de roteiro do vídeo
1. O que é grounding e os três caminhos da doc.
2. `FilesRetrieval` com uma pasta de `.md` (o mais curto para demonstrar).
3. Qdrant em Docker + MCP (`qdrant-store` / `qdrant-find`).
