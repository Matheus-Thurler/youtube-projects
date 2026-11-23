"""Time SRE de exemplo: especialistas em paralelo, depois um relatório.

As tools são falsas (dados fixos). O cenário SRE é exemplo do projeto, não da doc do ADK.
"""
from google.adk.agents import Agent, ParallelAgent, SequentialAgent

MODEL = "gemini-flash-latest"


def query_metrics(service: str) -> dict:
    """Returns latency and error metrics for a service."""
    return {"service": service, "p95_seconds": 4.8, "error_rate": 0.12}


def search_logs(service: str) -> dict:
    """Returns recent error logs for a service."""
    return {"service": service, "errors": ["HTTP 500 upstream timeout", "DB connection pool exhausted"]}


metrics_agent = Agent(
    model=MODEL, name="metrics_agent", tools=[query_metrics],
    instruction="Check the metrics of the service in the alert and summarize in 2 lines.",
    output_key="metrics_summary",
)
logs_agent = Agent(
    model=MODEL, name="logs_agent", tools=[search_logs],
    instruction="Check the logs of the service in the alert and summarize in 2 lines.",
    output_key="logs_summary",
)
report_agent = Agent(
    model=MODEL, name="report_agent",
    instruction=(
        "Write a short incident report with probable cause and next step.\n"
        "Metrics: {metrics_summary}\nLogs: {logs_summary}"
    ),
)

root_agent = SequentialAgent(
    name="sre_team",
    sub_agents=[ParallelAgent(name="investigate", sub_agents=[metrics_agent, logs_agent]), report_agent],
)
