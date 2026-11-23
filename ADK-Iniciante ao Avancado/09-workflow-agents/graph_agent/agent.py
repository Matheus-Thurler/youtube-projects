"""Workflow baseado em grafo (ADK 2.0): rota condicional, só com funções (sem LLM)."""
from google.adk import Event, Workflow


def classify(node_input):
    # devolve a rota; a aresta abaixo mapeia cada valor ao nó
    text = node_input.parts[0].text if hasattr(node_input, "parts") else str(node_input)
    # output repassa o texto ao próximo nó; route escolhe a aresta
    return Event(output=text, route="BUG" if "erro" in text.lower() else "OTHER")


def handle_bug(node_input: str) -> str:
    return "Abrir incidente."


def handle_other(node_input: str) -> str:
    return "Responder normalmente."


root_agent = Workflow(
    name="graph_agent",
    edges=[
        ("START", classify),
        (classify, {"BUG": handle_bug, "OTHER": handle_other}),
    ],
)
