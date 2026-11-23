# 11-observability

Fonte: doc oficial do ADK. A parte de Prometheus/Grafana **não** é do ADK: use a doc de cada ferramenta (marcado abaixo).
Docs: https://adk.dev/observability/ · /metrics/ · /traces/ · /logging/

## 1. Visão geral
O ADK traz observabilidade embutida em três sinais: **logging**, **metrics** e **traces**, todos via OpenTelemetry. Para análise mais avançada, a doc aponta as integrações de observabilidade em https://adk.dev/integrations/?topic=observability (AgentOps, Arize, Phoenix, MLflow, Langfuse, Datadog...).

## 2. Metrics (Python v1.32.0+)
Doc: https://adk.dev/observability/metrics/
- Seguem as *OpenTelemetry Semantic Conventions for GenAI* e saem em formato OTLP, sem acoplar a um backend (Prometheus, Datadog, SigNoz, Google Cloud Monitoring...).
- Métricas mais baratas e leves que logs e traces para análise agregada.

| Métrica | Tipo | O que mede |
|---|---|---|
| `gen_ai.invoke_agent.duration` | histograma (s) | tempo total do agente para processar um prompt |
| `gen_ai.invoke_workflow.duration` | histograma (s) | tempo de um workflow |
| `gen_ai.execute_tool.duration` | histograma (s) | latência de cada tool |
| `gen_ai.invoke_agent.inference_calls` | histograma (contagem) | chamadas ao modelo por invocação |
| `gen_ai.invoke_agent.tool_calls` | histograma (contagem) | chamadas de tool por invocação |
| `gen_ai.client.operation.duration` | histograma (s) | latência de uma chamada `generate_content` |
| `gen_ai.client.token.usage` | histograma (tokens) | tokens por chamada, separados por `gen_ai.token.type` (input/output) |

- Existem também métricas `adk.experimental.*` (tokens por invocação/workflow, cache, reasoning); desligadas por padrão e ainda sujeitas a mudar.
- **Export via `adk web`/`adk api_server`:**
```bash
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT="http://your-collector:4318/v1/metrics"
adk web path/to/your/agents_dir
```
  A doc cita também a variável genérica `OTEL_EXPORTER_OTLP_ENDPOINT`, que envia metrics, traces e logs ao mesmo endpoint.
- **Google Cloud Monitoring:** `adk web --otel_to_cloud path/to/your/agents_dir`.
- **Programático:**
```python
from google.adk.telemetry.setup import maybe_set_otel_providers
import os
os.environ["OTEL_EXPORTER_OTLP_METRICS_ENDPOINT"] = "http://your-collector:4318/v1/metrics"
os.environ["OTEL_SERVICE_NAME"] = "your-adk-agent"
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "key1=value1,key2=value2"
maybe_set_otel_providers()
```

## 3. Traces (Python v1.17.0+)
Doc: https://adk.dev/observability/traces/
- Spans hierárquicos: `invoke_agent {agent.name}` → `invoke_workflow {workflow.name}` → `execute_tool {tool.name}` e `generate_content {model.name}` (a chamada ao modelo).
- Backends citados: Google Cloud Trace, Jaeger, Grafana Tempo, Datadog. O contexto de trace é propagado para serviços externos chamados por tools.
- Export OTLP por variáveis de ambiente (como em metrics) ou `--otel_to_cloud`.

## 4. Logging
Doc: https://adk.dev/observability/logging/
- Usa o `logging` padrão do Python e eventos estruturados GenAI via OpenTelemetry.
- Níveis: `DEBUG` (prompts completos do LLM), `INFO` (ciclo de vida, execução de tool com nome e argumentos), `WARNING`, `ERROR`. Recomendação da doc: `INFO` ou `WARNING` em produção; `DEBUG` só ao investigar (pode conter dado sensível).
- `adk web --log_level DEBUG` (padrão `INFO`).
- Conteúdo de prompt vem **omitido por padrão**. Para registrar: `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` com `NO_CONTENT`, `EVENT_ONLY`, `SPAN_ONLY` ou `SPAN_AND_EVENT` (`true`/`1` = `EVENT_ONLY`). Aviso da doc: captura PII; em produção, desligue ou tenha política de dados.

## 5. Fora da doc do ADK (pesquisar na doc de cada ferramenta)
- Receber OTLP no Prometheus (receiver OTLP) e criar painéis no Grafana: docs do Prometheus e do Grafana.

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example obs_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run adk web --log_level DEBUG
```
Variáveis OTEL comentadas em `.env.example`. Para exportar métricas: defina `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` antes do `adk web`.

## Sugestão de roteiro do vídeo
1. Os três sinais e a tabela de métricas.
2. Exportar métricas: variável `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` + `adk web`.
3. Ver traces (`invoke_agent` → `generate_content` / `execute_tool`).
4. Logging: níveis e captura de conteúdo de prompt.
