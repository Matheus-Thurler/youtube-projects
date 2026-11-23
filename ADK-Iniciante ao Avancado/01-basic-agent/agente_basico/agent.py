from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='Voce é um agente de boas vindas.',
    instruction='Voce é um agente de boas vindas. Seu objetivo é receber o usuário e fornecer informações sobre o sistema.',
)
