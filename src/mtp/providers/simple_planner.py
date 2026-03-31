from __future__ import annotations

from typing import Any

from ..agent import AgentAction, ProviderAdapter
from ..protocol import ExecutionPlan, ToolBatch, ToolCall, ToolResult, ToolSpec


class SimplePlannerProvider(ProviderAdapter):
    """
    Tiny deterministic planner for local demos.

    Rules:
    - If user message contains "profile", execute `github.get_user` then `github.create_issue`.
    - Otherwise return a direct text response.
    """

    def next_action(self, messages: list[dict[str, Any]], tools: list[ToolSpec]) -> AgentAction:
        latest = messages[-1]["content"].lower()

        if "profile" in latest:
            plan = ExecutionPlan(
                batches=[
                    ToolBatch(
                        mode="sequential",
                        calls=[
                            ToolCall(id="c1", name="github.get_user", arguments={}),
                            ToolCall(
                                id="c2",
                                name="github.create_issue",
                                arguments={
                                    "title": "Auto-created issue",
                                    "body": {
                                        "$ref": "c1",
                                    },
                                },
                                depends_on=["c1"],
                            ),
                        ],
                    )
                ],
                metadata={"planner": "simple"},
            )
            return AgentAction(plan=plan)

        return AgentAction(response_text="Planner has no tool plan for this prompt yet.")

    def finalize(self, messages: list[dict[str, Any]], tool_results: list[ToolResult]) -> str:
        failures = [r for r in tool_results if not r.success]
        if failures:
            return f"Execution failed for {len(failures)} tool calls."
        created = [r for r in tool_results if r.tool_name == "github.create_issue"]
        if created:
            return f"Done. Issue created: {created[-1].output}"
        return f"Done. Ran {len(tool_results)} tool calls."
