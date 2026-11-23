from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools.retrieval.files_retrieval import FilesRetrieval

DOCS = Path(__file__).parent / "docs"

# Indexa os arquivos da pasta e expõe a tool search_documents(query)
runbooks = FilesRetrieval(
    name="search_documents",
    description="Busca nos runbooks da equipe.",
    input_dir=str(DOCS),
)

root_agent = Agent(
    model="gemini-flash-latest",
    name="rag_agent",
    instruction="Responda usando a tool de busca nos runbooks. Se não achar, diga que não sabe.",
    tools=[runbooks],
)
