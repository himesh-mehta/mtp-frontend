from __future__ import annotations

import asyncio
from typing import Any
from ..agent import AgentAction, ProviderAdapter
from ..config import require_env
from ..protocol import ExecutionPlan, ToolCall, ToolResult, ToolSpec
from .common import (
    calls_to_dependency_batches,
    extract_refs,
    extract_usage_metrics,
    format_openai_like_message,
    normalize_refs,
    safe_load_arguments,
)


class CerebrasToolCallingProvider(ProviderAdapter):
    """
    Provider adapter for Cerebras Cloud.

    Cerebras runs Llama models on wafer-scale chips, delivering the fastest
    inference available (~2000 tokens/sec). Uses an OpenAI-compatible API,
    so message formatting is identical to the OpenAI adapter.

    Supported models (as of 2025):
        - llama-4-scout-17b-16e-instruct  (default, best tool calling)
        - llama-3.3-70b
        - llama3.1-8b

    Free tier: https://cloud.cerebras.ai  (no credit card required)
    Env var:   CEREBRAS_API_KEY
    """

    def __init__(
        self,
        *,
        model: str = "llama-4-scout-17b-16e-instruct",
        api_key: str | None = None,
        temperature: float = 0.0,
        tool_choice: str | dict[str, Any] = "auto",
        parallel_tool_calls: bool = True,
        client: Any | None = None,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.tool_choice = tool_choice
        self.parallel_tool_calls = parallel_tool_calls
        self._last_finalize_usage: dict[str, int] | None = None
        self._client = client or self._make_client(api_key=api_key)

    # ------------------------------------------------------------------
    # Client construction
    # ------------------------------------------------------------------

    def _make_client(self, api_key: str | None) -> Any:
        try:
            from cerebras.cloud.sdk import Cerebras
        except ImportError as exc:
            raise ImportError(
                "`cerebras-cloud-sdk` not installed. "
                "Install with: pip install cerebras-cloud-sdk"
            ) from exc

        key = api_key or require_env("CEREBRAS_API_KEY")
        return Cerebras(api_key=key)

    # ------------------------------------------------------------------
    # Message / tool formatting
    # ------------------------------------------------------------------

    def _to_cerebras_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        formatted: list[dict[str, Any]] = []
        for msg in messages:
            converted = format_openai_like_message(
                msg,
                allow_images=False,   # Cerebras text-only as of mid-2025
                allow_audio=False,
                allow_video=False,
                allow_files=False,
            )
            if converted is None:
                continue
            if converted.get("role") == "tool":
                converted["name"] = msg.get("tool_name") or msg.get("name")
            formatted.append(converted)
        return formatted

    def _to_cerebras_tools(self, tools: list[ToolSpec]) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema or {"type": "object", "properties": {}},
                },
            }
            for tool in tools
        ]

    # ------------------------------------------------------------------
    # Core protocol methods
    # ------------------------------------------------------------------

    def next_action(self, messages: list[dict[str, Any]], tools: list[ToolSpec]) -> AgentAction:
        cerebras_messages = self._to_cerebras_messages(messages)
        cerebras_tools = self._to_cerebras_tools(tools)

        request_args: dict[str, Any] = {
            "model": self.model,
            "messages": cerebras_messages,
            "temperature": self.temperature,
        }
        if cerebras_tools:
            request_args["tools"] = cerebras_tools
            request_args["tool_choice"] = self.tool_choice
            # parallel_tool_calls supported by Cerebras SDK
            request_args["parallel_tool_calls"] = self.parallel_tool_calls

        try:
            response = self._client.chat.completions.create(**request_args)
        except TypeError:
            # Older SDK versions may not support parallel_tool_calls.
            request_args.pop("parallel_tool_calls", None)
            response = self._client.chat.completions.create(**request_args)

        message = response.choices[0].message
        tool_calls = getattr(message, "tool_calls", None)
        usage = extract_usage_metrics(response)
        action_meta: dict[str, Any] = {"provider": "cerebras", "model": self.model}
        if usage:
            action_meta["usage"] = usage

        if tool_calls:
            mtp_calls: list[ToolCall] = []
            id_by_index: dict[int, str] = {}
            serialized_tool_calls: list[dict[str, Any]] = []

            for idx, tc in enumerate(tool_calls):
                call_id = tc.id or f"call_{idx}"
                id_by_index[idx] = call_id
                parsed_args = safe_load_arguments(tc.function.arguments)
                normalized_args = normalize_refs(parsed_args, id_by_index, current_idx=idx)
                depends_on = list(dict.fromkeys(extract_refs(normalized_args)))
                mtp_calls.append(
                    ToolCall(
                        id=call_id,
                        name=tc.function.name,
                        arguments=normalized_args,
                        depends_on=depends_on,
                    )
                )
                serialized_tool_calls.append(
                    {
                        "id": call_id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments or "{}",
                        },
                    }
                )

            plan = ExecutionPlan(
                batches=calls_to_dependency_batches(mtp_calls),
                metadata={"provider": "cerebras", "model": self.model},
            )
            return AgentAction(
                plan=plan,
                metadata={
                    **action_meta,
                    "assistant_tool_message": {
                        "role": "assistant",
                        "content": message.content or "",
                        "tool_calls": serialized_tool_calls,
                    },
                },
            )

        return AgentAction(response_text=message.content or "", metadata=action_meta)

    def finalize(self, messages: list[dict[str, Any]], tool_results: list[ToolResult]) -> str:
        cerebras_messages = self._to_cerebras_messages(messages)
        response = self._client.chat.completions.create(
            model=self.model,
            messages=cerebras_messages,
            temperature=self.temperature,
        )
        self._last_finalize_usage = extract_usage_metrics(response) or None
        message = response.choices[0].message
        if getattr(message, "tool_calls", None):
            return "Model requested an additional tool round; rerun with a larger max_rounds."
        return message.content or "Done."

    async def anext_action(self, messages: list[dict[str, Any]], tools: list[ToolSpec]) -> AgentAction:
        return await asyncio.to_thread(self.next_action, messages, tools)

    async def afinalize(self, messages: list[dict[str, Any]], tool_results: list[ToolResult]) -> str:
        return await asyncio.to_thread(self.finalize, messages, tool_results)