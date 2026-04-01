from __future__ import annotations

import pathlib
import sys
import textwrap
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent, MTPAgent, ToolRegistry, load_dotenv_if_available
from mtp.providers import Groq
from mtp.toolkits import CalculatorToolkit, FileToolkit, PythonToolkit, ShellToolkit


def _print_section(title: str) -> None:
    print(f"\n------{title}------")


def _print_list(title: str, items: list[str]) -> None:
    print(f"{title}:")
    if not items:
        print("  - (none)")
        return
    for item in items:
        print(f"  - {item}")


def _print_wrapped_block(title: str, content: str, width: int = 100) -> None:
    print(f"{title}:")
    wrapped = textwrap.wrap(content, width=width) or [""]
    for line in wrapped:
        print(f"  {line}")


def _print_run_started(event: dict[str, Any], system_messages: list[str]) -> None:
    _print_section("agent-run-started")
    print(f"run_id: {event.get('run_id')}")
    print(f"max_rounds: {event.get('max_rounds')}")
    print(f"user_message: {event.get('user_message')}")
    print(f"tools_available: {event.get('tools_available')}")
    _print_list("tools", list(event.get("tool_names", [])))
    _print_list("system_instructions", system_messages)


def _print_plan(event: dict[str, Any]) -> None:
    _print_section("plan-received")
    print(f"round: {event.get('round')}")
    batches = event.get("batches", [])
    for idx, batch in enumerate(batches, start=1):
        print(f"batch#{idx}: mode={batch.get('mode')} calls={batch.get('calls')} call_ids={batch.get('call_ids')}")


def _print_tool_started(event: dict[str, Any]) -> None:
    print(
        f"[tool-started] round={event.get('round')} "
        f"tool={event.get('tool_name')} id={event.get('call_id')} "
        f"args={event.get('arguments')}"
    )


def _print_tool_finished(event: dict[str, Any]) -> None:
    success = event.get("success")
    status = "success" if success else "failed"
    print(
        f"[tool-finished] {status} tool={event.get('tool_name')} "
        f"id={event.get('call_id')} cached={event.get('cached')} output={event.get('output')}"
    )


def _print_text_chunk(event: dict[str, Any]) -> None:
    chunk = event.get("chunk", "")
    if chunk:
        print(chunk, end="", flush=True)


def _print_run_completed(event: dict[str, Any]) -> None:
    print()
    _print_section("agent-run-completed")
    print(f"rounds: {event.get('rounds')}")
    print(f"total_tool_calls: {event.get('total_tool_calls')}")
    _print_wrapped_block("final_text", str(event.get("final_text", "")))


def main() -> None:
    load_dotenv_if_available()

    calculator_tools = ToolRegistry()
    calculator_tools.register_toolkit_loader("calculator", CalculatorToolkit())

    tools = ToolRegistry()
    tools.register_toolkit_loader("file", FileToolkit(base_dir=pathlib.Path.cwd()))
    tools.register_toolkit_loader("python", PythonToolkit(base_dir=pathlib.Path.cwd()))
    tools.register_toolkit_loader("shell", ShellToolkit(base_dir=pathlib.Path.cwd()))

    provider = Groq(
        model="moonshotai/kimi-k2-instruct",
        strict_dependency_mode=True,
    )
    calculator_agent = Agent(
        provider=provider,
        tools=calculator_tools,
        mode="member",
        instructions="You are the calculator member agent. Solve math tasks precisely and return concise results.",
        debug_mode=False,
        strict_dependency_mode=True,
    )

    agent = MTPAgent(
        provider=provider,
        tools=tools,
        mode="orchestration",
        members={"calculator": calculator_agent},
        instructions=(
            "You are the orchestrator agent. Delegate math to agent.member.calculator, "
            "use tools for file/system operations, and be concise."
        ),
        debug_mode=False,
        strict_dependency_mode=True,
    )

    prompt = (
        "Calculate (25 * 4) + 10 and then list files in the current directory. "
        "Give a short summary."
    )

    events = agent.run_events(prompt, max_rounds=4, stream_final=True)
    for event in events:
        event_type = event.get("type")
        if event_type == "run_started":
            system_messages = [
                str(message.get("content", ""))
                for message in agent._agent.messages
                if message.get("role") == "system"
            ]
            _print_run_started(event, system_messages)
            continue
        if event_type == "round_started":
            _print_section(f"round-{event.get('round')}-started")
            continue
        if event_type == "plan_received":
            _print_plan(event)
            continue
        if event_type == "tool_started":
            _print_tool_started(event)
            continue
        if event_type == "tool_finished":
            _print_tool_finished(event)
            continue
        if event_type == "text_chunk":
            _print_text_chunk(event)
            continue
        if event_type == "run_completed":
            _print_run_completed(event)
            continue


if __name__ == "__main__":
    main()
