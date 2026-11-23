import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator


@pytest.mark.asyncio
async def test_light_agent():
    await AgentEvaluator.evaluate(
        agent_module="light_agent",
        eval_dataset_file_path_or_dir="tests/light.test.json",
    )
