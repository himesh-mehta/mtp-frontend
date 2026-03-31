from __future__ import annotations

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp.agent import AgentAction, ProviderAdapter
from mtp.protocol import ExecutionPlan, ToolBatch, ToolCall, ToolResult, ToolSpec
from mtp.runtime import ToolRegistry
from mtp import Agent


class _LoopProvider(ProviderAdapter):
    def __init__(self) -> None:
        self.round = 0

    def next_action(self, messages: list[dict], tools: list[ToolSpec]) -> AgentAction:
        self.round += 1
        if self.round == 1:
            return AgentAction(
                plan=ExecutionPlan(
                    batches=[ToolBatch(mode="parallel", calls=[ToolCall(id="a", name="calc.add", arguments={"a": 2, "b": 3})])]
                )
            )
        if self.round == 2:
            return AgentAction(
                plan=ExecutionPlan(
                    batches=[
                        ToolBatch(
                            mode="parallel",
                            calls=[ToolCall(id="b", name="calc.add", arguments={"a": 10, "b": 5})],
                        )
                    ]
                )
            )
        return AgentAction(response_text="final response")

    def finalize(self, messages: list[dict], tool_results: list[ToolResult]) -> str:
        return "fallback finalize"


class AgentLoopTests(unittest.TestCase):
    def test_run_loop_multi_round(self) -> None:
        reg = ToolRegistry()
        reg.register_tool(
            ToolSpec(name="calc.add", description="add"),
            lambda a, b: a + b,
        )
        agent = Agent(provider=_LoopProvider(), registry=reg)
        response = agent.run_loop("run tools", max_rounds=4)
        self.assertEqual(response, "final response")
        tool_messages = [m for m in agent.messages if m.get("role") == "tool"]
        self.assertEqual(len(tool_messages), 2)


class AgentAsyncLoopTests(unittest.IsolatedAsyncioTestCase):
    async def test_arun_loop_multi_round(self) -> None:
        reg = ToolRegistry()
        reg.register_tool(
            ToolSpec(name="calc.add", description="add"),
            lambda a, b: a + b,
        )
        agent = Agent(provider=_LoopProvider(), registry=reg)
        response = await agent.arun_loop("run tools", max_rounds=4)
        self.assertEqual(response, "final response")

    async def test_sync_run_raises_in_async_context(self) -> None:
        reg = ToolRegistry()
        reg.register_tool(
            ToolSpec(name="calc.add", description="add"),
            lambda a, b: a + b,
        )
        agent = Agent(provider=_LoopProvider(), registry=reg)
        with self.assertRaises(RuntimeError):
            agent.run_loop("run tools", max_rounds=1)


if __name__ == "__main__":
    unittest.main()
