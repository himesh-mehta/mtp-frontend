from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from collections.abc import AsyncIterator, Iterator
from typing import Any, Callable, Protocol
from uuid import uuid4

from .events import EventStreamContext
from .prompts import DEFAULT_MTP_SYSTEM_INSTRUCTIONS
from .protocol import ExecutionPlan, ToolResult, ToolSpec
from .runtime import ExecutionCancelledError, ToolRegistry
from .schema import ToolArgumentsValidationError, validate_tool_arguments
from .strict import validate_strict_dependencies


@dataclass(slots=True)
class AgentAction:
    response_text: str | None = None
    plan: ExecutionPlan | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RunOutput:
    run_id: str
    input: str
    final_text: str
    messages: list[dict[str, Any]]
    tool_results: list[ToolResult]
    user_id: str | None = None
    session_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    cancelled: bool = False
    total_tool_calls: int = 0
    output: Any | None = None
    output_validation_error: str | None = None


class ProviderAdapter(Protocol):
    def next_action(self, messages: list[dict[str, Any]], tools: list[ToolSpec]) -> AgentAction:
        ...

    def finalize(
        self,
        messages: list[dict[str, Any]],
        tool_results: list[ToolResult],
    ) -> str:
        ...

    def finalize_stream(
        self,
        messages: list[dict[str, Any]],
        tool_results: list[ToolResult],
    ) -> Iterator[str]:
        ...


class Agent:
    def __init__(
        self,
        provider: ProviderAdapter,
        registry: ToolRegistry | None = None,
        *,
        tools: ToolRegistry | None = None,
        debug_mode: bool = False,
        debug_logger: Callable[[str], None] | None = None,
        debug_max_chars: int = 600,
        strict_dependency_mode: bool = False,
        instructions: str | None = None,
        system_instructions: str | None = None,
        stream_chunk_size: int = 40,
        max_history_messages: int = 200,
    ) -> None:
        if registry is not None and tools is not None and registry is not tools:
            raise ValueError("Pass only one of `tools` or `registry`.")
        resolved_tools = tools or registry
        if resolved_tools is None:
            raise ValueError("Missing tools registry. Pass `tools=` (or legacy `registry=`).")

        self.provider = provider
        self.registry = resolved_tools
        self.tools = resolved_tools
        self.debug_mode = debug_mode
        self.debug_logger = debug_logger or print
        self.debug_max_chars = debug_max_chars
        self.strict_dependency_mode = strict_dependency_mode
        self.instructions = instructions
        self.system_instructions = system_instructions or DEFAULT_MTP_SYSTEM_INSTRUCTIONS
        self.stream_chunk_size = stream_chunk_size
        self.max_history_messages = max_history_messages
        self._system_seeded = False
        self.messages: list[dict[str, Any]] = []
        self._active_runs: set[str] = set()
        self._cancelled_runs: set[str] = set()

    def _debug(self, text: str) -> None:
        if self.debug_mode:
            self.debug_logger(f"[MTP DEBUG] {text}")

    def cancel_run(self, run_id: str) -> bool:
        if run_id not in self._active_runs:
            return False
        self._cancelled_runs.add(run_id)
        return True

    def _register_run(self, run_id: str) -> None:
        self._active_runs.add(run_id)
        self._cancelled_runs.discard(run_id)

    def _complete_run(self, run_id: str) -> None:
        self._active_runs.discard(run_id)

    def _is_cancelled(self, run_id: str) -> bool:
        return run_id in self._cancelled_runs

    def _short(self, value: Any) -> str:
        try:
            if isinstance(value, str):
                text = value
            else:
                text = json.dumps(value, default=str)
        except Exception:
            text = repr(value)
        if len(text) <= self.debug_max_chars:
            return text
        return text[: self.debug_max_chars] + "...<truncated>"

    def _parse_and_validate_output(
        self,
        final_text: str,
        output_schema: dict[str, Any] | None,
    ) -> tuple[Any | None, str | None]:
        if output_schema is None:
            return None, None
        try:
            parsed = json.loads(final_text)
        except json.JSONDecodeError as exc:
            return None, f"Output is not valid JSON: {exc}"
        try:
            validate_tool_arguments(parsed, output_schema)
        except ToolArgumentsValidationError as exc:
            return parsed, f"Output does not match schema: {exc}"
        return parsed, None

    def run(self, user_text: str) -> str:
        return self.run_loop(user_text=user_text, max_rounds=1)

    async def arun(self, user_text: str) -> str:
        return await self.arun_loop(user_text=user_text, max_rounds=1)

    def _run_coro_sync(self, coro: Any) -> Any:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)
        close_fn = getattr(coro, "close", None)
        if callable(close_fn):
            close_fn()
        raise RuntimeError(
            "Agent sync APIs cannot run inside an active asyncio event loop. "
            "Use arun()/arun_loop() instead."
        )

    def _trim_messages(self) -> None:
        if self.max_history_messages <= 0 or len(self.messages) <= self.max_history_messages:
            return
        system_messages = [msg for msg in self.messages if msg.get("role") == "system"]
        non_system = [msg for msg in self.messages if msg.get("role") != "system"]
        keep_non_system = max(self.max_history_messages - len(system_messages), 0)
        self.messages = system_messages + non_system[-keep_non_system:]

    def _append_message(self, message: dict[str, Any]) -> None:
        self.messages.append(message)
        self._trim_messages()

    def _extend_messages(self, messages: list[dict[str, Any]]) -> None:
        self.messages.extend(messages)
        self._trim_messages()

    def _chunk_text(self, text: str) -> Iterator[str]:
        if self.stream_chunk_size <= 0:
            yield text
            return
        for i in range(0, len(text), self.stream_chunk_size):
            yield text[i : i + self.stream_chunk_size]

    def _seed_system_messages_if_needed(self) -> None:
        if self._system_seeded:
            return
        if self.system_instructions:
            self._append_message({"role": "system", "content": self.system_instructions})
            self._debug(f"mtp_system_instructions={self._short(self.system_instructions)}")
        if self.instructions:
            self._append_message({"role": "system", "content": self.instructions})
            self._debug(f"user_instructions={self._short(self.instructions)}")
        self._system_seeded = True

    def _run_tool_rounds(
        self,
        user_text: str,
        max_rounds: int,
        *,
        run_id: str,
        tool_call_limit: int | None = None,
    ) -> tuple[list[ToolResult], str | None, bool, int]:
        self._seed_system_messages_if_needed()

        self._append_message({"role": "user", "content": user_text})
        self._debug(f"user_message={user_text!r}")
        tools = self.registry.list_tools()
        self._debug(f"tools_available={len(tools)}")
        self._debug(f"tool_names={[tool.name for tool in tools]}")
        last_results: list[ToolResult] = []
        cancelled = False
        total_tool_calls = 0

        for round_idx in range(1, max_rounds + 1):
            if self._is_cancelled(run_id):
                cancelled = True
                break
            self._debug(f"round={round_idx} start")
            self._debug(
                "llm_request_messages="
                + self._short(
                    [
                        {
                            "role": msg.get("role"),
                            "content": msg.get("content"),
                            "tool_calls": msg.get("tool_calls"),
                            "tool_call_id": msg.get("tool_call_id"),
                            "tool_name": msg.get("tool_name"),
                        }
                        for msg in self.messages
                    ]
                )
            )
            action = self.provider.next_action(self.messages, tools)

            if action.response_text and action.plan is None:
                self._debug("provider returned direct response (no tool plan)")
                self._debug(f"assistant_response={self._short(action.response_text)}")
                self._append_message({"role": "assistant", "content": action.response_text})
                return last_results, action.response_text, cancelled, total_tool_calls

            if action.plan is None:
                self._debug("provider returned no plan; breaking loop")
                break

            call_count = sum(len(batch.calls) for batch in action.plan.batches)
            if tool_call_limit is not None and total_tool_calls + call_count > tool_call_limit:
                self._append_message(
                    {
                        "role": "system",
                        "content": (
                            "Tool call limit reached. Do not call tools again; provide the best final answer "
                            "from available context."
                        ),
                    }
                )
                break
            total_tool_calls += call_count
            self._debug(f"plan_received batches={len(action.plan.batches)} calls={call_count}")
            for batch_idx, batch in enumerate(action.plan.batches, start=1):
                call_names = [call.name for call in batch.calls]
                self._debug(f"batch#{batch_idx} mode={batch.mode} calls={call_names}")

            if self.strict_dependency_mode:
                violations = validate_strict_dependencies(action.plan)
                if violations:
                    self._debug(f"strict_dependency_violations={len(violations)}")
                    for violation in violations:
                        self._debug(
                            f"strict_violation call_id={violation.call_id} "
                            f"tool={violation.tool_name} message={violation.message}"
                        )
                    self._append_message(
                        {
                            "role": "system",
                            "content": (
                                "Strict dependency mode is enabled. "
                                "Replan tool calls with explicit depends_on and/or $ref "
                                "for multi-call same-toolkit batches."
                            ),
                        }
                    )
                    continue

            assistant_tool_message = action.metadata.get("assistant_tool_message")
            if isinstance(assistant_tool_message, dict):
                self._debug("assistant tool-call message appended")
                self._debug(f"assistant_tool_message={self._short(assistant_tool_message)}")
                self._append_message(assistant_tool_message)

            try:
                last_results = self._run_coro_sync(
                    self.registry.execute_plan(action.plan, cancel_checker=lambda: self._is_cancelled(run_id))
                )
            except ExecutionCancelledError:
                cancelled = True
                break
            self._debug(f"executed_calls={len(last_results)}")
            for result in last_results:
                self._debug(
                    "tool_result "
                    f"id={result.call_id} tool={result.tool_name} "
                    f"success={result.success} cached={result.cached} "
                    f"approval={result.approval}"
                )
                self._debug(
                    f"tool_result_payload id={result.call_id} data={self._short(result.output if result.success else result.error)}"
                )
            tool_messages = [
                {
                    "role": "tool",
                    "tool_call_id": result.call_id,
                    "tool_name": result.tool_name,
                    "content": result.output if result.success else result.error,
                    "success": result.success,
                    "cached": result.cached,
                }
                for result in last_results
            ]
            self._extend_messages(tool_messages)

        return last_results, None, cancelled, total_tool_calls

    def run_output(
        self,
        user_text: str,
        *,
        max_rounds: int = 5,
        run_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tool_call_limit: int | None = None,
        output_schema: dict[str, Any] | None = None,
    ) -> RunOutput:
        if max_rounds < 1:
            raise ValueError("max_rounds must be >= 1")

        resolved_run_id = run_id or str(uuid4())
        self._register_run(resolved_run_id)
        try:
            last_results, direct_response, cancelled, total_tool_calls = self._run_tool_rounds(
                user_text=user_text,
                max_rounds=max_rounds,
                run_id=resolved_run_id,
                tool_call_limit=tool_call_limit,
            )
            if cancelled:
                final_text = "Run cancelled."
                self._append_message({"role": "assistant", "content": final_text})
            elif direct_response is not None:
                final_text = direct_response
            else:
                self._debug("calling provider.finalize")
                final_text = self.provider.finalize(self.messages, last_results)
                self._append_message({"role": "assistant", "content": final_text})
                self._debug(f"final response generated text={self._short(final_text)}")

            parsed_output, output_validation_error = self._parse_and_validate_output(final_text, output_schema)
            return RunOutput(
                run_id=resolved_run_id,
                input=user_text,
                final_text=final_text,
                messages=list(self.messages),
                tool_results=list(last_results),
                user_id=user_id,
                session_id=session_id,
                metadata=dict(metadata or {}),
                cancelled=cancelled,
                total_tool_calls=total_tool_calls,
                output=parsed_output,
                output_validation_error=output_validation_error,
            )
        finally:
            self._complete_run(resolved_run_id)

    def run_loop(
        self,
        user_text: str,
        max_rounds: int = 5,
        *,
        tool_call_limit: int | None = None,
    ) -> str:
        run = self.run_output(
            user_text=user_text,
            max_rounds=max_rounds,
            tool_call_limit=tool_call_limit,
        )
        return run.final_text

    async def _arun_tool_rounds(
        self,
        user_text: str,
        max_rounds: int,
        *,
        run_id: str,
        tool_call_limit: int | None = None,
    ) -> tuple[list[ToolResult], str | None, bool, int]:
        self._seed_system_messages_if_needed()
        self._append_message({"role": "user", "content": user_text})
        tools = self.registry.list_tools()
        last_results: list[ToolResult] = []
        cancelled = False
        total_tool_calls = 0

        for _round_idx in range(1, max_rounds + 1):
            if self._is_cancelled(run_id):
                cancelled = True
                break
            action = self.provider.next_action(self.messages, tools)
            if action.response_text and action.plan is None:
                self._append_message({"role": "assistant", "content": action.response_text})
                return last_results, action.response_text, cancelled, total_tool_calls
            if action.plan is None:
                break
            call_count = sum(len(batch.calls) for batch in action.plan.batches)
            if tool_call_limit is not None and total_tool_calls + call_count > tool_call_limit:
                self._append_message(
                    {
                        "role": "system",
                        "content": (
                            "Tool call limit reached. Do not call tools again; provide the best final answer "
                            "from available context."
                        ),
                    }
                )
                break
            total_tool_calls += call_count

            if self.strict_dependency_mode:
                violations = validate_strict_dependencies(action.plan)
                if violations:
                    self._append_message(
                        {
                            "role": "system",
                            "content": (
                                "Strict dependency mode is enabled. "
                                "Replan tool calls with explicit depends_on and/or $ref "
                                "for multi-call same-toolkit batches."
                            ),
                        }
                    )
                    continue

            assistant_tool_message = action.metadata.get("assistant_tool_message")
            if isinstance(assistant_tool_message, dict):
                self._append_message(assistant_tool_message)

            try:
                last_results = await self.registry.execute_plan(
                    action.plan,
                    cancel_checker=lambda: self._is_cancelled(run_id),
                )
            except ExecutionCancelledError:
                cancelled = True
                break
            tool_messages = [
                {
                    "role": "tool",
                    "tool_call_id": result.call_id,
                    "tool_name": result.tool_name,
                    "content": result.output if result.success else result.error,
                    "success": result.success,
                    "cached": result.cached,
                }
                for result in last_results
            ]
            self._extend_messages(tool_messages)

        return last_results, None, cancelled, total_tool_calls

    async def arun_output(
        self,
        user_text: str,
        *,
        max_rounds: int = 5,
        run_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tool_call_limit: int | None = None,
        output_schema: dict[str, Any] | None = None,
    ) -> RunOutput:
        if max_rounds < 1:
            raise ValueError("max_rounds must be >= 1")

        resolved_run_id = run_id or str(uuid4())
        self._register_run(resolved_run_id)
        try:
            last_results, direct_response, cancelled, total_tool_calls = await self._arun_tool_rounds(
                user_text=user_text,
                max_rounds=max_rounds,
                run_id=resolved_run_id,
                tool_call_limit=tool_call_limit,
            )
            if cancelled:
                final_text = "Run cancelled."
                self._append_message({"role": "assistant", "content": final_text})
            elif direct_response is not None:
                final_text = direct_response
            else:
                final_text = self.provider.finalize(self.messages, last_results)
                self._append_message({"role": "assistant", "content": final_text})

            parsed_output, output_validation_error = self._parse_and_validate_output(final_text, output_schema)
            return RunOutput(
                run_id=resolved_run_id,
                input=user_text,
                final_text=final_text,
                messages=list(self.messages),
                tool_results=list(last_results),
                user_id=user_id,
                session_id=session_id,
                metadata=dict(metadata or {}),
                cancelled=cancelled,
                total_tool_calls=total_tool_calls,
                output=parsed_output,
                output_validation_error=output_validation_error,
            )
        finally:
            self._complete_run(resolved_run_id)

    async def arun_loop(
        self,
        user_text: str,
        max_rounds: int = 5,
        *,
        tool_call_limit: int | None = None,
    ) -> str:
        run = await self.arun_output(
            user_text=user_text,
            max_rounds=max_rounds,
            tool_call_limit=tool_call_limit,
        )
        return run.final_text

    def run_loop_stream(
        self,
        user_text: str,
        max_rounds: int = 5,
        *,
        tool_call_limit: int | None = None,
        run_id: str | None = None,
    ) -> Iterator[str]:
        if max_rounds < 1:
            raise ValueError("max_rounds must be >= 1")
        resolved_run_id = run_id or str(uuid4())
        self._register_run(resolved_run_id)
        try:
            last_results, direct_response, cancelled, _tool_calls = self._run_tool_rounds(
                user_text=user_text,
                max_rounds=max_rounds,
                run_id=resolved_run_id,
                tool_call_limit=tool_call_limit,
            )
            if cancelled:
                final_text = "Run cancelled."
                self._append_message({"role": "assistant", "content": final_text})
                yield final_text
                return
            if direct_response is not None:
                for chunk in self._chunk_text(direct_response):
                    yield chunk
                return

            self._debug("calling provider.finalize_stream")
            finalize_stream = getattr(self.provider, "finalize_stream", None)
            if not callable(finalize_stream):
                final_text = self.provider.finalize(self.messages, last_results)
                self._append_message({"role": "assistant", "content": final_text})
                self._debug(f"final response generated text={self._short(final_text)}")
                yield final_text
                return

            chunks: list[str] = []
            for chunk in finalize_stream(self.messages, last_results):
                if self._is_cancelled(resolved_run_id):
                    final_text = "Run cancelled."
                    self._append_message({"role": "assistant", "content": final_text})
                    yield final_text
                    return
                if chunk:
                    chunks.append(chunk)
                    yield chunk
            final_text = "".join(chunks)
            self._append_message({"role": "assistant", "content": final_text})
            self._debug(f"final streamed response generated text={self._short(final_text)}")
        finally:
            self._complete_run(resolved_run_id)

    def run_loop_events(
        self,
        user_text: str,
        max_rounds: int = 5,
        *,
        stream_final: bool = True,
        run_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tool_call_limit: int | None = None,
    ) -> Iterator[dict[str, Any]]:
        if max_rounds < 1:
            raise ValueError("max_rounds must be >= 1")

        resolved_run_id = run_id or str(uuid4())
        self._register_run(resolved_run_id)
        events = EventStreamContext(run_id=resolved_run_id)
        self._seed_system_messages_if_needed()
        self._append_message({"role": "user", "content": user_text})
        tools = self.registry.list_tools()
        yield events.emit(
            "run_started",
            user_message=user_text,
            max_rounds=max_rounds,
            tools_available=len(tools),
            tool_names=[tool.name for tool in tools],
            user_id=user_id,
            session_id=session_id,
            metadata=metadata or {},
        )

        last_results: list[ToolResult] = []
        total_tool_calls = 0
        try:
            for round_idx in range(1, max_rounds + 1):
                if self._is_cancelled(resolved_run_id):
                    yield events.emit("run_cancelled", round=round_idx)
                    self._append_message({"role": "assistant", "content": "Run cancelled."})
                    return
                yield events.emit("round_started", round=round_idx)
                action = self.provider.next_action(self.messages, tools)

                if action.response_text and action.plan is None:
                    self._append_message({"role": "assistant", "content": action.response_text})
                    if stream_final:
                        for chunk in self._chunk_text(action.response_text):
                            yield events.emit("text_chunk", chunk=chunk, source="direct")
                    yield events.emit(
                        "run_completed",
                        final_text=action.response_text,
                        rounds=round_idx,
                        total_tool_calls=total_tool_calls,
                    )
                    return

                if action.plan is None:
                    break

                round_call_count = sum(len(batch.calls) for batch in action.plan.batches)
                if tool_call_limit is not None and total_tool_calls + round_call_count > tool_call_limit:
                    self._append_message(
                        {
                            "role": "system",
                            "content": (
                                "Tool call limit reached. Do not call tools again; provide the best final answer "
                                "from available context."
                            ),
                        }
                    )
                    break
                total_tool_calls += round_call_count

                yield events.emit(
                    "plan_received",
                    round=round_idx,
                    batches=[
                        {
                            "mode": batch.mode,
                            "calls": [call.name for call in batch.calls],
                            "call_ids": [call.id for call in batch.calls],
                        }
                        for batch in action.plan.batches
                    ],
                )

                if self.strict_dependency_mode:
                    violations = validate_strict_dependencies(action.plan)
                    if violations:
                        yield events.emit(
                            "strict_violations",
                            round=round_idx,
                            violations=[
                                {
                                    "call_id": violation.call_id,
                                    "tool_name": violation.tool_name,
                                    "message": violation.message,
                                }
                                for violation in violations
                            ],
                        )
                        self._append_message(
                            {
                                "role": "system",
                                "content": (
                                    "Strict dependency mode is enabled. "
                                    "Replan tool calls with explicit depends_on and/or $ref "
                                    "for multi-call same-toolkit batches."
                                ),
                            }
                        )
                        continue

                assistant_tool_message = action.metadata.get("assistant_tool_message")
                if isinstance(assistant_tool_message, dict):
                    self._append_message(assistant_tool_message)
                    yield events.emit("assistant_tool_message", round=round_idx, message=assistant_tool_message)

                for batch_idx, batch in enumerate(action.plan.batches, start=1):
                    yield events.emit(
                        "batch_started",
                        round=round_idx,
                        batch_index=batch_idx,
                        mode=batch.mode,
                        call_ids=[call.id for call in batch.calls],
                    )
                    for call in batch.calls:
                        yield events.emit(
                            "tool_started",
                            round=round_idx,
                            batch_index=batch_idx,
                            call_id=call.id,
                            tool_name=call.name,
                            arguments=call.arguments,
                            depends_on=call.depends_on,
                        )

                try:
                    last_results = self._run_coro_sync(
                        self.registry.execute_plan(
                            action.plan,
                            cancel_checker=lambda: self._is_cancelled(resolved_run_id),
                        )
                    )
                except ExecutionCancelledError:
                    yield events.emit("run_cancelled", round=round_idx)
                    self._append_message({"role": "assistant", "content": "Run cancelled."})
                    return
                for result in last_results:
                    yield events.emit(
                        "tool_finished",
                        round=round_idx,
                        call_id=result.call_id,
                        tool_name=result.tool_name,
                        success=result.success,
                        cached=result.cached,
                        approval=result.approval,
                        output=result.output if result.success else None,
                        error=result.error if not result.success else None,
                    )

                tool_messages = [
                    {
                        "role": "tool",
                        "tool_call_id": result.call_id,
                        "tool_name": result.tool_name,
                        "content": result.output if result.success else result.error,
                        "success": result.success,
                        "cached": result.cached,
                    }
                    for result in last_results
                ]
                self._extend_messages(tool_messages)

            finalize_stream = getattr(self.provider, "finalize_stream", None)
            if stream_final and callable(finalize_stream):
                chunks: list[str] = []
                for chunk in finalize_stream(self.messages, last_results):
                    if self._is_cancelled(resolved_run_id):
                        yield events.emit("run_cancelled", round=max_rounds)
                        self._append_message({"role": "assistant", "content": "Run cancelled."})
                        return
                    if chunk:
                        chunks.append(chunk)
                        yield events.emit("text_chunk", chunk=chunk, source="finalize_stream")
                final_text = "".join(chunks)
            else:
                final_text = self.provider.finalize(self.messages, last_results)
                if stream_final:
                    for chunk in self._chunk_text(final_text):
                        yield events.emit("text_chunk", chunk=chunk, source="finalize_fallback")

            self._append_message({"role": "assistant", "content": final_text})
            yield events.emit("run_completed", final_text=final_text, rounds=max_rounds, total_tool_calls=total_tool_calls)
        finally:
            self._complete_run(resolved_run_id)

    async def arun_loop_events(
        self,
        user_text: str,
        max_rounds: int = 5,
        *,
        stream_final: bool = True,
        run_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tool_call_limit: int | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        if max_rounds < 1:
            raise ValueError("max_rounds must be >= 1")

        resolved_run_id = run_id or str(uuid4())
        self._register_run(resolved_run_id)
        events = EventStreamContext(run_id=resolved_run_id)
        self._seed_system_messages_if_needed()
        self._append_message({"role": "user", "content": user_text})
        tools = self.registry.list_tools()
        yield events.emit(
            "run_started",
            user_message=user_text,
            max_rounds=max_rounds,
            tools_available=len(tools),
            tool_names=[tool.name for tool in tools],
            user_id=user_id,
            session_id=session_id,
            metadata=metadata or {},
        )

        last_results: list[ToolResult] = []
        total_tool_calls = 0
        try:
            for round_idx in range(1, max_rounds + 1):
                if self._is_cancelled(resolved_run_id):
                    yield events.emit("run_cancelled", round=round_idx)
                    self._append_message({"role": "assistant", "content": "Run cancelled."})
                    return
                yield events.emit("round_started", round=round_idx)
                action = self.provider.next_action(self.messages, tools)

                if action.response_text and action.plan is None:
                    self._append_message({"role": "assistant", "content": action.response_text})
                    if stream_final:
                        for chunk in self._chunk_text(action.response_text):
                            yield events.emit("text_chunk", chunk=chunk, source="direct")
                    yield events.emit(
                        "run_completed",
                        final_text=action.response_text,
                        rounds=round_idx,
                        total_tool_calls=total_tool_calls,
                    )
                    return

                if action.plan is None:
                    break

                round_call_count = sum(len(batch.calls) for batch in action.plan.batches)
                if tool_call_limit is not None and total_tool_calls + round_call_count > tool_call_limit:
                    self._append_message(
                        {
                            "role": "system",
                            "content": (
                                "Tool call limit reached. Do not call tools again; provide the best final answer "
                                "from available context."
                            ),
                        }
                    )
                    break
                total_tool_calls += round_call_count

                yield events.emit(
                    "plan_received",
                    round=round_idx,
                    batches=[
                        {
                            "mode": batch.mode,
                            "calls": [call.name for call in batch.calls],
                            "call_ids": [call.id for call in batch.calls],
                        }
                        for batch in action.plan.batches
                    ],
                )

                if self.strict_dependency_mode:
                    violations = validate_strict_dependencies(action.plan)
                    if violations:
                        yield events.emit(
                            "strict_violations",
                            round=round_idx,
                            violations=[
                                {
                                    "call_id": violation.call_id,
                                    "tool_name": violation.tool_name,
                                    "message": violation.message,
                                }
                                for violation in violations
                            ],
                        )
                        self._append_message(
                            {
                                "role": "system",
                                "content": (
                                    "Strict dependency mode is enabled. "
                                    "Replan tool calls with explicit depends_on and/or $ref "
                                    "for multi-call same-toolkit batches."
                                ),
                            }
                        )
                        continue

                assistant_tool_message = action.metadata.get("assistant_tool_message")
                if isinstance(assistant_tool_message, dict):
                    self._append_message(assistant_tool_message)
                    yield events.emit("assistant_tool_message", round=round_idx, message=assistant_tool_message)

                for batch_idx, batch in enumerate(action.plan.batches, start=1):
                    yield events.emit(
                        "batch_started",
                        round=round_idx,
                        batch_index=batch_idx,
                        mode=batch.mode,
                        call_ids=[call.id for call in batch.calls],
                    )
                    for call in batch.calls:
                        yield events.emit(
                            "tool_started",
                            round=round_idx,
                            batch_index=batch_idx,
                            call_id=call.id,
                            tool_name=call.name,
                            arguments=call.arguments,
                            depends_on=call.depends_on,
                        )

                try:
                    last_results = await self.registry.execute_plan(
                        action.plan,
                        cancel_checker=lambda: self._is_cancelled(resolved_run_id),
                    )
                except ExecutionCancelledError:
                    yield events.emit("run_cancelled", round=round_idx)
                    self._append_message({"role": "assistant", "content": "Run cancelled."})
                    return
                for result in last_results:
                    yield events.emit(
                        "tool_finished",
                        round=round_idx,
                        call_id=result.call_id,
                        tool_name=result.tool_name,
                        success=result.success,
                        cached=result.cached,
                        approval=result.approval,
                        output=result.output if result.success else None,
                        error=result.error if not result.success else None,
                    )

                tool_messages = [
                    {
                        "role": "tool",
                        "tool_call_id": result.call_id,
                        "tool_name": result.tool_name,
                        "content": result.output if result.success else result.error,
                        "success": result.success,
                        "cached": result.cached,
                    }
                    for result in last_results
                ]
                self._extend_messages(tool_messages)

            finalize_stream = getattr(self.provider, "finalize_stream", None)
            if stream_final and callable(finalize_stream):
                chunks: list[str] = []
                for chunk in finalize_stream(self.messages, last_results):
                    if self._is_cancelled(resolved_run_id):
                        yield events.emit("run_cancelled", round=max_rounds)
                        self._append_message({"role": "assistant", "content": "Run cancelled."})
                        return
                    if chunk:
                        chunks.append(chunk)
                        yield events.emit("text_chunk", chunk=chunk, source="finalize_stream")
                final_text = "".join(chunks)
            else:
                final_text = self.provider.finalize(self.messages, last_results)
                if stream_final:
                    for chunk in self._chunk_text(final_text):
                        yield events.emit("text_chunk", chunk=chunk, source="finalize_fallback")

            self._append_message({"role": "assistant", "content": final_text})
            yield events.emit("run_completed", final_text=final_text, rounds=max_rounds, total_tool_calls=total_tool_calls)
        finally:
            self._complete_run(resolved_run_id)
