from google.adk.agents import LlmAgent

# {user:name?} é lido do state; "?" evita erro se a chave não existir
root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="chat_agent",
    instruction="Você é um assistente. O nome do usuário é {user:name?}. Responda em uma frase.",
    output_key="last_reply",  # a resposta final fica em state["last_reply"]
)
