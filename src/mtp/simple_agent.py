from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from datetime import datetime
import json
import textwrap
from typing import Any

from .agent import Agent, RunOutput
from .protocol import ToolResult
from .runtime import ToolRegistry
from .agent import ProviderAdapter


class MTPAgent:
    """
    Provider-agnostic convenience wrapper around Agent.
    Requires explicit provider + tool registry from the user.
    """

    def __init__(
        self,
        *,
        provider: ProviderAdapter,
        tools: ToolRegistry | None = None,
        registry: ToolRegistry | None = None,
        debug_mode: bool = False,
        strict_dependency_mode: bool = False,
        instructions: str | None = None,
        system_instructions: str | None = None,
        stream_chunk_size: int = 40,
        max_history_messages: int = 200,
        mode: str = "standalone",
        members: dict[str, Agent] | None = None,
    ) -> None:
        if registry is not None and tools is not None and registry is not tools:
            raise ValueError("Pass only one of `tools` or `registry`.")
        resolved_tools = tools or registry
        if resolved_tools is None:
            raise ValueError("Missing tools registry. Pass `tools=` (or legacy `registry=`).")

        self._agent = Agent(
            provider=provider,
            tools=resolved_tools,
            debug_mode=debug_mode,
            strict_dependency_mode=strict_dependency_mode,
            instructions=instructions,
            system_instructions=system_instructions,
            stream_chunk_size=stream_chunk_size,
            max_history_messages=max_history_messages,
            mode=mode,
            members=members,
        )

    def run(self, prompt: str, *, max_rounds: int = 5, tool_call_limit: int | None = None) -> str:
        return self._agent.run_loop(user_input=prompt, max_rounds=max_rounds, tool_call_limit=tool_call_limit)

    def run_output(
        self,
        prompt: str,
        *,
        max_rounds: int = 5,
        run_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tool_call_limit: int | None = None,
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        output_model: ProviderAdapter | None = None,
        output_model_prompt: str | None = None,
        parser_model: ProviderAdapter | None = None,
        parser_model_prompt: str | None = None,
    ) -> RunOutput:
        return self._agent.run_output(
            user_input=prompt,
            max_rounds=max_rounds,
            run_id=run_id,
            user_id=user_id,
            session_id=session_id,
            metadata=metadata,
            tool_call_limit=tool_call_limit,
            input_schema=input_schema,
            output_schema=output_schema,
            output_model=output_model,
            output_model_prompt=output_model_prompt,
            parser_model=parser_model,
            parser_model_prompt=parser_model_prompt,
        )

    def run_stream(
        self,
        prompt: str,
        *,
        max_rounds: int = 5,
        tool_call_limit: int | None = None,
        run_id: str | None = None,
        input_schema: dict[str, Any] | None = None,
    ) -> Iterator[str]:
        return self._agent.run_loop_stream(
            user_input=prompt,
            max_rounds=max_rounds,
            tool_call_limit=tool_call_limit,
            run_id=run_id,
            input_schema=input_schema,
        )

    async def arun(self, prompt: str, *, max_rounds: int = 5, tool_call_limit: int | None = None) -> str:
        return await self._agent.arun_loop(user_input=prompt, max_rounds=max_rounds, tool_call_limit=tool_call_limit)

    async def arun_output(
        self,
        prompt: str,
        *,
        max_rounds: int = 5,
        run_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tool_call_limit: int | None = None,
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        output_model: ProviderAdapter | None = None,
        output_model_prompt: str | None = None,
        parser_model: ProviderAdapter | None = None,
        parser_model_prompt: str | None = None,
    ) -> RunOutput:
        return await self._agent.arun_output(
            user_input=prompt,
            max_rounds=max_rounds,
            run_id=run_id,
            user_id=user_id,
            session_id=session_id,
            metadata=metadata,
            tool_call_limit=tool_call_limit,
            input_schema=input_schema,
            output_schema=output_schema,
            output_model=output_model,
            output_model_prompt=output_model_prompt,
            parser_model=parser_model,
            parser_model_prompt=parser_model_prompt,
        )

    def run_events(
        self,
        prompt: str,
        *,
        max_rounds: int = 5,
        stream_final: bool = True,
        run_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tool_call_limit: int | None = None,
        input_schema: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        return self._agent.run_loop_events(
            user_input=prompt,
            max_rounds=max_rounds,
            stream_final=stream_final,
            run_id=run_id,
            user_id=user_id,
            session_id=session_id,
            metadata=metadata,
            tool_call_limit=tool_call_limit,
            input_schema=input_schema,
        )

    def arun_events(
        self,
        prompt: str,
        *,
        max_rounds: int = 5,
        stream_final: bool = True,
        run_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tool_call_limit: int | None = None,
        input_schema: dict[str, Any] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        return self._agent.arun_loop_events(
            user_input=prompt,
            max_rounds=max_rounds,
            stream_final=stream_final,
            run_id=run_id,
            user_id=user_id,
            session_id=session_id,
            metadata=metadata,
            tool_call_limit=tool_call_limit,
            input_schema=input_schema,
        )

    def cancel_run(self, run_id: str) -> bool:
        return self._agent.cancel_run(run_id)

    def continue_run(
        self,
        *,
        run_output: RunOutput | None = None,
        run_id: str | None = None,
        max_rounds: int = 5,
        updated_tools: list[ToolResult] | None = None,
        tool_call_limit: int | None = None,
    ) -> RunOutput:
        return self._agent.continue_run(
            run_output=run_output,
            run_id=run_id,
            max_rounds=max_rounds,
            updated_tools=updated_tools,
            tool_call_limit=tool_call_limit,
        )

    async def acontinue_run(
        self,
        *,
        run_output: RunOutput | None = None,
        run_id: str | None = None,
        max_rounds: int = 5,
        updated_tools: list[ToolResult] | None = None,
        tool_call_limit: int | None = None,
    ) -> RunOutput:
        return await self._agent.acontinue_run(
            run_output=run_output,
            run_id=run_id,
            max_rounds=max_rounds,
            updated_tools=updated_tools,
            tool_call_limit=tool_call_limit,
        )

    def print_response(
        self,
        prompt: str,
        *,
        max_rounds: int = 5,
        stream: bool = False,
        stream_events: bool = False,
        run_id: str | None = None,
        tool_call_limit: int | None = None,
        event_format: str = "pretty",
    ) -> None:
        if stream_events:
            if event_format not in {"pretty", "json"}:
                raise ValueError("event_format must be 'pretty' or 'json'")
            printed_chunk = False
            pretty_context: dict[str, Any] = {
                "member_map": {},
                "delegated_calls": {},
                "tool_starts": {},
                "run_started_at": None,
                "tools_ok": 0,
                "tools_failed": 0,
                "tools_cached": 0,
            }
            for event in self.run_events(
                prompt,
                max_rounds=max_rounds,
                stream_final=stream,
                run_id=run_id,
                tool_call_limit=tool_call_limit,
            ):
                if event_format == "json":
                    print(json.dumps(event, default=str))
                    continue
                printed_chunk = self._print_pretty_event(event, printed_chunk=printed_chunk, context=pretty_context)
            return
        if not stream:
            print(self.run(prompt, max_rounds=max_rounds, tool_call_limit=tool_call_limit))
            return
        for chunk in self.run_stream(
            prompt,
            max_rounds=max_rounds,
            tool_call_limit=tool_call_limit,
            run_id=run_id,
        ):
            print(chunk, end="", flush=True)
        print()

    def _parse_iso_datetime(self, value: Any) -> datetime | None:
        if not isinstance(value, str) or "T" not in value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None

    def _format_timestamp(self, stamp: Any) -> str:
        parsed = self._parse_iso_datetime(stamp)
        if parsed is None:
            return str(stamp) if stamp is not None else "-"
        return parsed.strftime("%H:%M:%S.%f")[:-3]

    def _format_meta(self, *, event_type: str, sequence: Any, stamp: Any) -> str:
        return f"[seq={sequence} t={self._format_timestamp(stamp)}] {event_type}"

    def _duration_seconds(self, start: Any, end: Any) -> str | None:
        start_dt = self._parse_iso_datetime(start)
        end_dt = self._parse_iso_datetime(end)
        if start_dt is None or end_dt is None:
            return None
        return f"{(end_dt - start_dt).total_seconds():.3f}s"

    def _short(self, value: Any, *, width: int = 180) -> str:
        if isinstance(value, str):
            text = value
        else:
            try:
                text = json.dumps(value, ensure_ascii=True, sort_keys=True, default=str)
            except Exception:
                text = repr(value)
        if len(text) <= width:
            return text
        return text[:width] + "...<truncated>"

    def _hr(self, char: str = "-", width: int = 88) -> str:
        return char * width

    def _print_wrapped_block(self, title: str, text: Any, *, indent: str = "  ", width: int = 100) -> None:
        print(f"{title}:")
        raw = str(text or "")
        if not raw.strip():
            print(f"{indent}(none)")
            return
        for paragraph in raw.splitlines() or [""]:
            wrapped = textwrap.wrap(paragraph, width=width - len(indent)) or [""]
            for line in wrapped:
                print(f"{indent}{line}")

    def _print_json_block(self, title: str, value: Any, *, indent: str = "  ", max_chars: int = 1200) -> None:
        try:
            rendered = json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True, default=str)
        except Exception:
            rendered = str(value)
        if len(rendered) > max_chars:
            rendered = rendered[:max_chars] + "...<truncated>"
        self._print_wrapped_block(title, rendered, indent=indent)

    def _print_bullet(self, text: Any, *, indent: str = "  ", width: int = 100) -> None:
        raw = str(text or "")
        lines = raw.splitlines() or [""]
        first = True
        for line in lines:
            wrapped = textwrap.wrap(line, width=width - len(indent) - 2) or [""]
            for chunk in wrapped:
                prefix = "- " if first else "  "
                print(f"{indent}{prefix}{chunk}")
                first = False

    def _print_pretty_event(
        self,
        event: dict[str, Any],
        *,
        printed_chunk: bool,
        context: dict[str, Any],
    ) -> bool:
        event_type = str(event.get("type", ""))
        stamp = str(event.get("timestamp", ""))
        sequence = event.get("sequence")
        meta = self._format_meta(event_type=event_type, sequence=sequence, stamp=stamp)

        if event_type == "run_started":
            context["run_started_at"] = stamp
            print(f"\n{self._hr('=')}")
            print(f"[MTP RUN START] {meta}")
            print(self._hr("="))
            print(f"Run ID          : {event.get('run_id')}")
            print(f"Max Rounds      : {event.get('max_rounds')}")
            print(f"Tools Available : {event.get('tools_available')}")
            direct_tools = [str(tool) for tool in list(event.get("direct_tool_names", []))]
            if not direct_tools:
                all_tools = [str(tool) for tool in list(event.get("tool_names", []))]
                member_delegation_tools = {str(member.get("delegation_tool")) for member in list(event.get("member_agents", []))}
                direct_tools = [tool for tool in all_tools if tool not in member_delegation_tools and not tool.startswith("agent.member.")]
            print("Tools:")
            if direct_tools:
                for tool in direct_tools:
                    print(f"  - {tool}")
            else:
                print("  - (none)")
            member_agents = list(event.get("member_agents", []))
            context["member_map"] = {str(member.get("id")): member for member in member_agents}
            if member_agents:
                print("Sub Agents:")
                for member in member_agents:
                    member_id = member.get("id")
                    role = member.get("role")
                    member_tools = [str(tool) for tool in list(member.get("tools", []))]
                    print(f"  - id={member_id}")
                    print(f"    mode={member.get('mode')}")
                    print(f"    delegation_tool={member.get('delegation_tool')}")
                    print("    tools:")
                    if member_tools:
                        for tool in member_tools:
                            print(f"      - {tool}")
                    else:
                        print("      - (none)")
                    if role:
                        self._print_wrapped_block("    role", role, indent="      ", width=100)
            else:
                print("Sub Agents: (none)")
            system_instructions = list(event.get("system_instructions", []))
            user_instructions = list(event.get("user_instructions", []))
            orchestration_instructions = list(event.get("orchestration_instructions", []))
            print("System Instructions:")
            if system_instructions:
                for item in system_instructions:
                    self._print_bullet(item, indent="  ", width=100)
            else:
                print("  - (none)")
            print("User Instructions:")
            if user_instructions:
                for item in user_instructions:
                    self._print_bullet(item, indent="  ", width=100)
            else:
                print("  - (none)")
            print("Orchestration Instructions:")
            if orchestration_instructions:
                for item in orchestration_instructions:
                    self._print_bullet(item, indent="  ", width=100)
            else:
                print("  - (none)")
            input_validation_error = event.get("input_validation_error")
            if input_validation_error:
                self._print_wrapped_block("Input Validation Error", input_validation_error, indent="  ", width=100)
            self._print_wrapped_block("User Message", event.get("user_message"), indent="  ", width=100)
            return False

        if event_type == "round_started":
            round_idx = event.get("round")
            print(f"\n{self._hr('-')}")
            print(f"[MTP ROUND START] round={round_idx}  {meta}")
            print(self._hr("-"))
            return False

        if event_type == "plan_received":
            round_idx = event.get("round")
            batches = event.get("batches", [])
            total_calls = sum(len(list(batch.get("calls", []))) for batch in batches)
            print(f"[MTP PLAN] round={round_idx} batches={len(batches)} calls={total_calls}  {meta}")
            for idx, batch in enumerate(batches, start=1):
                print(f"  Batch #{idx} ({batch.get('mode')})")
                calls = list(batch.get("calls", []))
                call_ids = list(batch.get("call_ids", []))
                for call_name, call_id in zip(calls, call_ids, strict=False):
                    print(f"    - tool={call_name}")
                    print(f"      id={call_id}")
            return False

        if event_type == "tool_started":
            call_id = str(event.get("call_id"))
            context.setdefault("tool_starts", {})[call_id] = stamp
            print(f"[MTP TOOL START] round={event.get('round')} tool={event.get('tool_name')} id={event.get('call_id')}  {meta}")
            self._print_json_block("  Arguments", event.get("arguments"), indent="    ", max_chars=600)
            tool_name = str(event.get("tool_name", ""))
            if tool_name.startswith("agent.member."):
                member_id = tool_name.removeprefix("agent.member.")
                context.setdefault("delegated_calls", {})[call_id] = member_id
                print(f"  Delegation: started member={member_id} parent_call_id={call_id}")
                member = context.get("member_map", {}).get(member_id, {})
                role = member.get("role")
                if role:
                    self._print_wrapped_block("  Member Role", role, indent="    ", width=100)
                member_tools = list(member.get("tools", []))
                print("  Member Tools:")
                if member_tools:
                    for tool in member_tools:
                        print(f"    - {tool}")
                else:
                    print("    - (none)")
            return False

        if event_type == "tool_finished":
            success = bool(event.get("success"))
            success_text = "SUCCESS" if success else "FAILED"
            call_id = str(event.get("call_id"))
            if success:
                context["tools_ok"] = int(context.get("tools_ok", 0)) + 1
            else:
                context["tools_failed"] = int(context.get("tools_failed", 0)) + 1
            if event.get("cached"):
                context["tools_cached"] = int(context.get("tools_cached", 0)) + 1
            duration_text = self._duration_seconds(context.get("tool_starts", {}).pop(call_id, None), stamp)
            duration_segment = f" duration={duration_text}" if duration_text else ""
            payload = event.get("output") if success else event.get("error")
            print(
                f"[MTP TOOL END] status={success_text} tool={event.get('tool_name')} "
                f"id={event.get('call_id')} cached={event.get('cached')}{duration_segment}  {meta}"
            )
            self._print_json_block("  Result", payload, indent="    ", max_chars=900)
            member_id = context.get("delegated_calls", {}).pop(call_id, None)
            if member_id:
                print(
                    f"  Delegation: completed member={member_id} parent_call_id={call_id} "
                    f"status={success_text}"
                )
            return False

        if event_type == "batch_started":
            print(
                f"[MTP BATCH] round={event.get('round')} idx={event.get('batch_index')} "
                f"mode={event.get('mode')} call_ids={event.get('call_ids')}  {meta}"
            )
            return False

        if event_type == "assistant_tool_message":
            message = event.get("message", {})
            tool_calls = message.get("tool_calls", []) if isinstance(message, dict) else []
            print(f"[MTP ASSISTANT TOOL MSG] round={event.get('round')} tool_calls={len(tool_calls)}  {meta}")
            for call in tool_calls:
                function = call.get("function", {})
                args = function.get("arguments")
                if isinstance(args, str):
                    try:
                        parsed = json.loads(args)
                        args = json.dumps(parsed, ensure_ascii=True, sort_keys=True)
                    except Exception:
                        pass
                print(f"  - name={function.get('name')} id={call.get('id')}")
                self._print_wrapped_block("    args", self._short(args), indent="      ", width=100)
            return False

        if event_type == "strict_violations":
            violations = list(event.get("violations", []))
            print(f"[MTP STRICT VIOLATIONS] round={event.get('round')} count={len(violations)}  {meta}")
            for violation in violations:
                print(
                    "  - "
                    f"call_id={violation.get('call_id')} tool={violation.get('tool_name')} "
                    f"message={violation.get('message')}"
                )
            return False

        if event_type == "text_chunk":
            chunk = str(event.get("chunk", ""))
            if chunk:
                print(chunk, end="", flush=True)
                return True
            return printed_chunk

        if event_type == "run_completed":
            if printed_chunk:
                print()
            elapsed = self._duration_seconds(context.get("run_started_at"), stamp)
            elapsed_segment = f" elapsed={elapsed}" if elapsed else ""
            print(f"\n{self._hr('=')}")
            print(f"[MTP RUN END] {meta}")
            print(self._hr("="))
            print(f"Rounds          : {event.get('rounds')}")
            print(f"Total Tool Calls: {event.get('total_tool_calls')}")
            print(f"Tools Succeeded : {context.get('tools_ok', 0)}")
            print(f"Tools Failed    : {context.get('tools_failed', 0)}")
            print(f"Tools Cached    : {context.get('tools_cached', 0)}")
            if elapsed_segment:
                print(f"Elapsed         : {elapsed_segment.removeprefix(' elapsed=')}")
            final_text = str(event.get("final_text", ""))
            self._print_wrapped_block("Final Text", final_text, indent="  ", width=100)
            return False

        if event_type == "run_cancelled":
            elapsed = self._duration_seconds(context.get("run_started_at"), stamp)
            elapsed_segment = f" elapsed={elapsed}" if elapsed else ""
            print(f"\n[MTP RUN CANCELLED] round={event.get('round')}{elapsed_segment}  {meta}")
            return False

        if event_type == "run_paused":
            print(f"\n[MTP RUN PAUSED] round={event.get('round')} tool_name={event.get('tool_name')}  {meta}")
            self._print_wrapped_block("Reason", event.get("reason"), indent="  ", width=100)
            return False

        if event_type == "tool_retry_requested":
            print(f"[MTP TOOL RETRY] round={event.get('round')} tool_name={event.get('tool_name')}  {meta}")
            self._print_wrapped_block("Feedback", event.get("feedback"), indent="  ", width=100)
            return False

        print(json.dumps(event, default=str))
        return False
