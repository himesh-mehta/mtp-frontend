from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Protocol

from .protocol import ExecutionPlan, ToolResult, ToolSpec
from .runtime import ToolRegistry


@dataclass(slots=True)
class AgentAction:
    response_text: str | None = None
    plan: ExecutionPlan | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ProviderAdapter(Protocol):
    def next_action(self, messages: list[dict[str, Any]], tools: list[ToolSpec]) -> AgentAction:
        ...

    def finalize(
        self,
        messages: list[dict[str, Any]],
        tool_results: list[ToolResult],
    ) -> str:
        ...


class Agent:
    def __init__(self, provider: ProviderAdapter, registry: ToolRegistry) -> None:
        self.provider = provider
        self.registry = registry
        self.messages: list[dict[str, Any]] = []

    def run(self, user_text: str) -> str:
        self.messages.append({"role": "user", "content": user_text})
        tools = self.registry.list_tools()
        action = self.provider.next_action(self.messages, tools)

        if action.response_text and action.plan is None:
            self.messages.append({"role": "assistant", "content": action.response_text})
            return action.response_text

        if action.plan is None:
            text = "No plan and no direct response from provider."
            self.messages.append({"role": "assistant", "content": text})
            return text

        results = asyncio.run(self.registry.execute_plan(action.plan))
        tool_messages = [
            {
                "role": "tool",
                "tool_call_id": result.call_id,
                "tool_name": result.tool_name,
                "content": result.output if result.success else result.error,
                "success": result.success,
                "cached": result.cached,
            }
            for result in results
        ]
        self.messages.extend(tool_messages)
        final_text = self.provider.finalize(self.messages, results)
        self.messages.append({"role": "assistant", "content": final_text})
        return final_text

