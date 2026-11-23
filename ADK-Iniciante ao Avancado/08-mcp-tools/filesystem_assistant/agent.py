import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

# Pasta que o servidor MCP de filesystem pode acessar (requer Node.js/npx)
TARGET_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "files"))
os.makedirs(TARGET_FOLDER, exist_ok=True)

root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="filesystem_assistant",
    instruction="Ajude o usuário a consultar arquivos. Use as tools disponíveis.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-filesystem", TARGET_FOLDER],
                ),
                timeout=30,
            ),
            tool_filter=["list_directory", "read_file"],  # expõe só o necessário
        )
    ],
)
