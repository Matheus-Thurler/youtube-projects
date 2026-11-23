from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import Agent


def check_prime(nums: list[int]) -> str:
    """Check if the given numbers are prime."""
    def is_prime(n):
        return n > 1 and all(n % i for i in range(2, int(n**0.5) + 1))
    return ", ".join(f"{n}: {'prime' if is_prime(n) else 'not prime'}" for n in nums)


root_agent = Agent(
    model="gemini-flash-latest",
    name="prime_agent",
    description="Checks whether numbers are prime.",
    instruction="Use the check_prime tool to answer whether numbers are prime.",
    tools=[check_prime],
)

# Expõe via A2A; a porta precisa bater com a do uvicorn
a2a_app = to_a2a(root_agent, port=8001)
