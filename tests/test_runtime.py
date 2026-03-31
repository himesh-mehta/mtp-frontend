from __future__ import annotations

import asyncio
import pathlib
import sys
import time
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp.protocol import ExecutionPlan, ToolBatch, ToolCall, ToolRiskLevel, ToolSpec
from mtp.runtime import RegisteredTool, ToolRegistry, ToolkitLoader


class DemoToolkit(ToolkitLoader):
    def __init__(self) -> None:
        self.loaded = False

    def load_tools(self) -> list[RegisteredTool]:
        self.loaded = True

        def ping() -> str:
            return "pong"

        return [
            RegisteredTool(
                spec=ToolSpec(
                    name="github.ping",
                    description="Ping tool",
                    risk_level=ToolRiskLevel.READ_ONLY,
                ),
                handler=ping,
            )
        ]


class RuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_lazy_loading(self) -> None:
        reg = ToolRegistry()
        toolkit = DemoToolkit()
        reg.register_toolkit_loader("github", toolkit)
        result = await reg.execute_call(ToolCall(id="1", name="github.ping"), {})
        self.assertTrue(toolkit.loaded)
        self.assertTrue(result.success)
        self.assertEqual(result.output, "pong")

    async def test_dependency_reference(self) -> None:
        reg = ToolRegistry()

        def base() -> dict:
            return {"x": 41}

        def plus_one(payload: dict) -> int:
            return payload["x"] + 1

        reg.register_tool(
            ToolSpec(name="math.base", description="Base value"),
            base,
        )
        reg.register_tool(
            ToolSpec(name="math.plus_one", description="Increment"),
            plus_one,
        )

        plan = ExecutionPlan(
            batches=[
                ToolBatch(
                    mode="sequential",
                    calls=[
                        ToolCall(id="c1", name="math.base"),
                        ToolCall(
                            id="c2",
                            name="math.plus_one",
                            arguments={"payload": {"$ref": "c1"}},
                            depends_on=["c1"],
                        ),
                    ],
                )
            ]
        )

        results = await reg.execute_plan(plan)
        self.assertEqual(results[-1].output, 42)

    async def test_parallel_batch(self) -> None:
        reg = ToolRegistry()

        async def slow_one() -> int:
            await asyncio.sleep(0.2)
            return 1

        async def slow_two() -> int:
            await asyncio.sleep(0.2)
            return 2

        reg.register_tool(ToolSpec(name="t.one", description=""), slow_one)
        reg.register_tool(ToolSpec(name="t.two", description=""), slow_two)

        plan = ExecutionPlan(
            batches=[
                ToolBatch(
                    mode="parallel",
                    calls=[
                        ToolCall(id="a", name="t.one"),
                        ToolCall(id="b", name="t.two"),
                    ],
                )
            ]
        )
        start = time.perf_counter()
        results = await reg.execute_plan(plan)
        elapsed = time.perf_counter() - start
        self.assertEqual(len(results), 2)
        self.assertLess(elapsed, 0.35)

    async def test_cache_ttl(self) -> None:
        reg = ToolRegistry()
        calls = {"count": 0}

        def expensive(x: int) -> int:
            calls["count"] += 1
            return x * 10

        reg.register_tool(
            ToolSpec(
                name="math.expensive",
                description="",
                cache_ttl_seconds=60,
            ),
            expensive,
        )

        first = await reg.execute_call(
            ToolCall(id="1", name="math.expensive", arguments={"x": 3}),
            {},
        )
        second = await reg.execute_call(
            ToolCall(id="2", name="math.expensive", arguments={"x": 3}),
            {},
        )

        self.assertEqual(first.output, 30)
        self.assertEqual(second.output, 30)
        self.assertFalse(first.cached)
        self.assertTrue(second.cached)
        self.assertEqual(calls["count"], 1)


if __name__ == "__main__":
    unittest.main()
