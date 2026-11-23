# Variações de RAG

Todas resolvem o mesmo problema: dar ao LLM a informação certa na hora de responder. Comece pelo RAG simples (`06-rag`) e só adicione uma variação quando a avaliação mostrar um problema que ela resolve.

## RAG simples (base)

1. **Indexar**: docs → chunks → embeddings.
2. **Recuperar**: embedding da pergunta + similaridade, pega os top-k.
3. **Gerar**: o LLM responde só com os chunks no prompt.

## Comparação

| Variação | Ideia | Quando usar | Contra |
|---|---|---|---|
| **CAG** (Cache-Augmented Generation) | Coloca **todos os docs no prompt** e reusa via prompt caching. Sem embedding nem vector DB | Base pequena e estável, que cabe na janela de contexto | Custo e latência crescem com o tamanho; o modelo pode se perder em contexto enorme |
| **Agentic RAG** | A busca vira uma tool; o agente decide quando buscar, o que buscar e se busca de novo | Perguntas que exigem várias buscas ou combinar tools | Mais chamadas ao LLM, mais custo e latência |
| **GraphRAG** | Docs viram um **grafo de entidades e relações**; a busca navega pelo grafo | Perguntas que juntam vários docs ("quem aprovou os contratos da empresa X?") | Construir o grafo é caro e complexo |
| **HyDE** | O LLM escreve uma resposta hipotética e você embeda **ela**, não a pergunta | Quando pergunta e chunk são muito diferentes em forma | Uma chamada extra ao LLM por busca |
| **Query rewriting / multi-query** | O LLM reformula ou divide a pergunta antes de buscar | Perguntas vagas, longas ou com várias partes | Uma chamada extra ao LLM |
| **Self-RAG / Corrective RAG** | O sistema avalia o que recuperou; se for ruim, busca de novo, reformula ou vai à web | Quando recuperação ruim gera resposta errada | Mais etapas e mais custo |
| **Multimodal RAG** | Indexa imagens, tabelas e PDFs escaneados, não só texto | Docs com conteúdo visual relevante | Modelos de embedding multimodais, índice maior |
| **Fine-tuning** (não é RAG) | Ensina o modelo com os seus dados | Estilo, formato e vocabulário | Ruim para fatos: esquece, não cita fonte e fica velho |

**Regra comum:** RAG para conhecimento, fine-tuning para comportamento.

## Melhorias na recuperação (combinam com qualquer variação)

- **Chunking**: 200–500 tokens, 10–20% de sobreposição, quebrar por estrutura (títulos) antes de tamanho. É o que mais pesa na qualidade.
- **Metadados**: guardar fonte, página e data no `payload`; serve para citar e filtrar.
- **Busca híbrida**: embedding (significado) + BM25 (termo exato). Resolve códigos, siglas e nomes próprios.
- **Rerank**: modelo cross-encoder reordena os top 20–50 candidatos e fica com os top 3–5. Só vale com muitos chunks.
- **Corte de nota**: se o melhor chunk é fraco, responder "não sei" sem chamar o LLM.

## Como escolher

```
Base pequena (< ~500 páginas) e estável  →  CAG
Base média/grande                        →  RAG simples
RAG simples falha em perguntas ligadas   →  GraphRAG
Perguntas complexas, várias etapas       →  Agentic RAG
Qualidade da busca fraca                 →  rerank, híbrida, query rewriting
```

## Limites do RAG

- Pergunta de agregação ("quantos reembolsos tivemos?") não é problema de RAG; use SQL.
- Se o conjunto de docs cabe inteiro no contexto, talvez nem precise de RAG.

## Avaliação

Sem medir, não dá para saber se uma mudança ajudou. Monte 20–50 perguntas com resposta esperada e o chunk que deveria ser recuperado. Meça separado: (1) a recuperação trouxe o chunk certo; (2) o LLM respondeu certo com ele. A maioria dos erros está em (1).

## Embeddings

A Anthropic não tem modelo de embedding próprio. Opções: Gemini (`gemini-embedding-001`), Voyage AI (`voyage-4`, `voyage-4-lite`, `voyage-4-large`), OpenAI, ou modelos open source locais. O mesmo modelo deve indexar os chunks e embedar as perguntas; trocou de modelo, reindexa tudo.

Fonte: [Embeddings - Claude Docs](https://platform.claude.com/docs/en/build-with-claude/embeddings)
