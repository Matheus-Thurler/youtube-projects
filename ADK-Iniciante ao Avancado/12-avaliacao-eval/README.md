# 12-avaliacao-eval

Fonte: só a doc oficial do ADK.
Docs: https://adk.dev/evaluate/ · https://adk.dev/evaluate/criteria/ · https://adk.dev/evaluate/custom_metrics/ · https://adk.dev/evaluate/user-sim/

> Observação: `agents-cli eval run` (usado nos projetos scaffoldados) é outra ferramenta, com métricas próprias (`custom_response_quality`). Esta página cobre só o que a doc do **ADK** descreve (`adk eval`, `adk web`, `pytest`, `adk conformance`).

## 1. Por que avaliar agentes
- Testes tradicionais dão "passa/falha"; modelos são probabilísticos, então asserts determinísticos muitas vezes não servem.
- A doc separa dois focos: **trajetória e uso de tools** (a sequência de passos até a solução) e **resposta final** (qualidade, relevância, correção).
- Antes de automatizar: defina sucesso, tarefas críticas e métricas.

## 2. Dois formatos de dataset
- **Test file** (`*.test.json`, o sufixo é a única regra): uma sessão simples; usado como teste unitário durante o desenvolvimento. Campos: User Content, Expected Intermediate Tool Use Trajectory, Expected Intermediate Agent Responses, Final Response. Pode haver `test_config.json` na pasta com os critérios.
- **Evalset** (`*.evalset.json`): vários "evals" (sessões), cada um com um ou mais turnos; serve para conversas longas e multi-turno. Dá para criar pela UI do `adk web` (aba **Eval**, "Add current session").
- Ambos têm modelo Pydantic (`EvalSet`).

## 3. Critérios embutidos
Doc: https://adk.dev/evaluate/criteria/

| Critério | O que faz |
|---|---|
| `tool_trajectory_avg_score` | match exato da trajetória de tools |
| `response_match_score` | similaridade ROUGE-1 com a resposta de referência |
| `final_response_match_v2` | match semântico com a referência, julgado por LLM |
| `rubric_based_final_response_quality_v1` | qualidade da resposta final por rubricas customizadas (LLM) |
| `rubric_based_tool_use_quality_v1` | qualidade do uso de tools por rubricas (LLM) |
| `hallucinations_v1` | resposta ancorada no contexto (sem afirmações sem suporte) |
| `safety_v1` | segurança/inocuidade da resposta |
| `multi_turn_task_success_v1`, `multi_turn_trajectory_quality_v1`, `multi_turn_tool_use_quality_v1` | avaliação de conversas multi-turno |
| eficiência: `tool_call_count_v1`, `inference_call_count_v1`, `token_usage_v1`, `invocation_duration_v1` | só reportam valor, nunca reprovam; saem sem configurar |

- Padrão sem configuração: `tool_trajectory_avg_score` = 1.0 e `response_match_score` = 0.8.
- Recomendações da doc: CI/regressão → trajetória + `response_match_score`; sem referência confiável → rubricas; verificar fundamentação → `hallucinations_v1`; conteúdo nocivo → `safety_v1`.
- Alguns critérios (qualidade de resposta, segurança, multi-turno) exigem o Vertex Gen AI Evaluation Service (autenticação por `GOOGLE_API_KEY` ou credenciais do Google Cloud).
- Config:
```json
{ "criteria": { "tool_trajectory_avg_score": 1.0, "response_match_score": 0.8 } }
```

## 4. Como rodar
- **UI** (`adk web <pasta_dos_agentes>`): aba Eval, criar/escolher evalset, "Run Evaluation", ajustar thresholds nos sliders.
- **`pytest`:**
```python
await AgentEvaluator.evaluate(
    agent_module="home_automation_agent",
    eval_dataset_file_path_or_dir="tests/integration/fixture/home_automation_agent/simple_test.test.json",
)
```
- **CLI:**
```bash
adk eval <AGENT_MODULE_FILE_PATH> <EVAL_SET_FILE_PATH_OR_ID>... \
    [--config_file_path=<PATH>] [--print_detailed_results]
```
  Para rodar só alguns evals: `arquivo.json:eval_1,eval_2`.
- **Conformance:** `adk conformance test` compara o comportamento atual com gravações-base (baseline) para detectar regressões; modo Replay por padrão (modo Live ainda em desenvolvimento).
- **User simulation:** para conversas imprevisíveis; critérios que dependem de trajetória/resposta esperada não funcionam junto com ela (https://adk.dev/evaluate/user-sim/).

## Exemplo (uv)
Pasta criada com `uv init` + `uv add google-adk`. Instalar: `uv sync`.

Copie a chave: `cp .env.example light_agent/.env` e edite `GOOGLE_API_KEY`.

```shell
uv run pytest tests/test_agent.py
uv run adk eval light_agent tests/light.test.json --config_file_path=tests/test_config.json --print_detailed_results
```
O dataset em `tests/light.test.json` valida contra o `EvalSet`; a avaliação chama o LLM (precisa de chave).

## Sugestão de roteiro do vídeo
1. Por que `assert` em texto não basta: trajetória vs. resposta final.
2. Criar um evalset pela UI (`adk web` → Eval → Add current session).
3. Rodar com `adk eval` e ler a nota por critério.
4. Escolher critérios (tabela) e fixar threshold no `test_config.json`.
