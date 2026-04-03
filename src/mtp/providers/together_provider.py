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


class TogetherAIToolCallingProvider(ProviderAdapter):
    """
    Provider adapter for Together AI.

    Together AI hosts 200+ open-source models with OpenAI-compatible API.
    Great for running large open models (Llama, Qwen, DeepSeek, Mixtral)
    without vendor lock-in.

    Recommended models for tool calling:
        - meta-llama/Llama-4-Scout-17B-16E-Instruct   (default, best tool use)
        - meta-llama/Llama-3.3-70B-Instruct-Turbo     (fast, reliable)
        - Qwen/Qwen2.5-72B-Instruct-Turbo             (excellent reasoning)
        - deepseek-ai/DeepSeek-V3                      (top-tier reasoning)
        - mistralai/Mixtral-8x22B-Instruct-v0.1        (strong + fast)
        - microsoft/WizardLM-2-8x22B                   (complex instruction following)

    Strengths:
        - Widest model selection of any provider
        - Run DeepSeek/Qwen/Llama at scale
        - Competitive pricing (~$0.18/1M tokens for 70B)
        - Good for comparing model performance on same task

    Free tier : $1 credit on signup — https://api.together.ai
    Env var   : TOGETHER_API_KEY
    Docs      : https://docs.together.ai
    Install   : pip install together   OR   pip install openai (uses OpenAI compat)
    """

    def __init__(
        self,
        *,
        model: str = "meta-llama/Llama-4-Scout-17B-16E-Instruct",
        api_key: str | None = None,
        temperature: float = 0.0,
        tool_choice: str | dict[str, Any] = "auto",
        parallel_tool_calls: bool = True,
        max_tokens: int = 4096,
        client: Any | None = None,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.tool_choice = tool_choice
        self.parallel_tool_calls = parallel_tool_calls
        self.max_tokens = max_tokens
        self._last_finalize_usage: dict[str, int] | None = None
        self._client = client or self._make_client(api_key=api_key)

    # ------------------------------------------------------------------
    # Client construction
    # ------------------------------------------------------------------

    def _make_client(self, api_key: str | None) -> Any:
        # Together AI has its own SDK but also supports the OpenAI client.
        # We prefer the Together SDK when available, fall back to openai.
        key = api_key or require_env("TOGETHER_API_KEY")
        try:
            from together import Together
            return Together(api_key=key)
        except ImportError:
            pass

        try:
            from openai import OpenAI
            return OpenAI(
                base_url="https://api.together.xyz/v1",
                api_key=key,
            )
        except ImportError as exc:
            raise ImportError(
                "Neither `together` nor `openai` is installed. "
                "Install with: pip install together  OR  pip install openai"
            ) from exc

    # ------------------------------------------------------------------
    # Message / tool formatting
    # ------------------------------------------------------------------

    def _to_together_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        formatted: list[dict[str, Any]] = []
        for msg in messages:
            converted = format_openai_like_message(
                msg,
                allow_images=True,    # Llama 4 / vision models support images
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

    def _to_together_tools(self, tools: list[ToolSpec]) -> list[dict[str, Any]]:
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
        together_messages = self._to_together_messages(messages)
        together_tools = self._to_together_tools(tools)

        request_args: dict[str, Any] = {
            "model": self.model,
            "messages": together_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if together_tools:
            request_args["tools"] = together_tools
            request_args["tool_choice"] = self.tool_choice

        try:
            if together_tools:
                request_args["parallel_tool_calls"] = self.parallel_tool_calls
            response = self._client.chat.completions.create(**request_args)
        except Exception:
            request_args.pop("parallel_tool_calls", None)
            response = self._client.chat.completions.create(**request_args)

        message = response.choices[0].message
        tool_calls = getattr(message, "tool_calls", None)
        usage = extract_usage_metrics(response)
        action_meta: dict[str, Any] = {"provider": "together", "model": self.model}
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
                metadata={"provider": "together", "model": self.model},
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
        together_messages = self._to_together_messages(messages)
        response = self._client.chat.completions.create(
            model=self.model,
            messages=together_messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
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