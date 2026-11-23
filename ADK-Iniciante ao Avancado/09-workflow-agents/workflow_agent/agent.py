"""Template workflows: dois pesquisadores em paralelo, depois um sintetizador em sequência."""
from google.adk.agents import Agent, ParallelAgent, SequentialAgent

MODEL = "gemini-flash-latest"

energy = Agent(
    model=MODEL, name="energy_researcher",
    instruction="Resuma em 2 linhas as novidades em energia renovável.",
    output_key="energy_result",
)
ev = Agent(
    model=MODEL, name="ev_researcher",
    instruction="Resuma em 2 linhas as novidades em veículos elétricos.",
    output_key="ev_result",
)
synthesizer = Agent(
    model=MODEL, name="synthesizer",
    instruction="Combine os resultados em um parágrafo.\nEnergia: {energy_result}\nEVs: {ev_result}",
)

root_agent = SequentialAgent(
    name="research_pipeline",
    sub_agents=[ParallelAgent(name="parallel_research", sub_agents=[energy, ev]), synthesizer],
)
