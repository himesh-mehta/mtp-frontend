from __future__ import annotations

import pathlib
import sys
from typing import Any
from uuid import uuid4

import streamlit as st

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent
from mtp.providers import Groq
from mtp.toolkits import CalculatorToolkit, FileToolkit, PythonToolkit, ShellToolkit


def _build_agent(*, model: str, cwd: pathlib.Path) -> Agent.MTPAgent:
    calculator_tools = Agent.ToolRegistry()
    calculator_tools.register_toolkit_loader("calculator", CalculatorToolkit())

    tools = Agent.ToolRegistry()
    tools.register_toolkit_loader("file", FileToolkit(base_dir=cwd))
    tools.register_toolkit_loader("python", PythonToolkit(base_dir=cwd))
    tools.register_toolkit_loader("shell", ShellToolkit(base_dir=cwd))

    provider = Groq(model=model, strict_dependency_mode=True)
    calculator_agent = Agent(
        provider=provider,
        tools=calculator_tools,
        mode="member",
        instructions="You are the calculator member agent. Solve math tasks precisely and return concise results.",
        debug_mode=False,
        strict_dependency_mode=True,
    )

    return Agent.MTPAgent(
        provider=provider,
        tools=tools,
        mode="orchestration",
        members={"calculator": calculator_agent},
        instructions=(
            "You are the orchestrator agent. Delegate math to agent.member.calculator, "
            "use tools for file/system operations, and be concise."
        ),
        autoresearch=False,
        research_instructions=(
            "Stay in persistent work mode until the request is fully complete. "
            "Do not stop after a plausible answer. Verify results with tools when useful, "
            "and call agent.terminate only after you have finished the task."
        ),
        debug_mode=True,
        stream_tool_events=True,
        stream_tool_results=False,
        strict_dependency_mode=True,
    )


def _short_text(text: str, limit: int = 200) -> str:
    compact = " ".join(text.strip().split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _prefer_reasoning(existing: str | None, incoming: str | None) -> str | None:
    existing_text = existing.strip() if isinstance(existing, str) and existing.strip() else None
    incoming_text = incoming.strip() if isinstance(incoming, str) and incoming.strip() else None
    if incoming_text is None:
        return existing_text
    if existing_text is None:
        return incoming_text
    if len(incoming_text) > len(existing_text):
        return incoming_text
    return existing_text


def _format_tool_lines(tool_events: list[dict[str, str | None]]) -> str:
    lines: list[str] = []
    for item in tool_events:
        name = str(item.get("name") or "tool")
        reasoning = item.get("reasoning")
        if isinstance(reasoning, str) and reasoning.strip():
            lines.append(f"- `{name}`: {reasoning.strip()}")
        else:
            lines.append(f"- `{name}`")
    return "\n".join(lines) if lines else "_No tool events yet._"


def _init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "agent_key" not in st.session_state:
        st.session_state.agent_key = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"streamlit-{uuid4()}"


def _ensure_agent(model: str, cwd: pathlib.Path) -> Agent.MTPAgent:
    key = f"{model}|{cwd}"
    if st.session_state.agent is None or st.session_state.agent_key != key:
        st.session_state.agent = _build_agent(model=model, cwd=cwd)
        st.session_state.agent_key = key
    return st.session_state.agent


def _render_history() -> None:
    for msg in st.session_state.messages:
        role = msg["role"]
        with st.chat_message(role):
            st.markdown(msg["content"])
            tools = msg.get("tool_events")
            if isinstance(tools, list) and tools:
                with st.expander("Tool Activity", expanded=False):
                    st.markdown(_format_tool_lines(tools))
            usage_lines = msg.get("usage_lines")
            if isinstance(usage_lines, list) and usage_lines:
                st.caption(" | ".join(str(line) for line in usage_lines))


def _run_turn(
    *,
    agent: Agent.MTPAgent,
    prompt: str,
    max_rounds: int,
    session_id: str,
) -> tuple[str, list[dict[str, str | None]], list[str]]:
    response_chunks: list[str] = []
    tool_map: dict[str, dict[str, str | None]] = {}
    tool_order: list[str] = []
    usage_totals = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "reasoning_tokens": 0}

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        tools_placeholder = st.empty()
        response_placeholder = st.empty()
        status_placeholder.info("Running agent...")
        tools_placeholder.markdown("_No tool events yet._")

        for event in agent.run_events(
            prompt,
            max_rounds=max_rounds,
            stream_final=True,
            session_id=session_id,
            stream_tool_events=True,
            stream_tool_results=False,
        ):
            event_type = str(event.get("type") or "")
            if event_type == "text_chunk":
                chunk = str(event.get("chunk") or "")
                if chunk:
                    response_chunks.append(chunk)
                    response_placeholder.markdown("".join(response_chunks))
                continue

            if event_type == "tool_started":
                call_id = str(event.get("call_id") or "")
                tool_name = str(event.get("tool_name") or "tool")
                reasoning = event.get("reasoning")
                reasoning_text = str(reasoning).strip() if isinstance(reasoning, str) and reasoning.strip() else None
                key = call_id or f"{tool_name}:{len(tool_order)}"
                if key not in tool_map:
                    tool_map[key] = {"name": tool_name, "reasoning": reasoning_text}
                    tool_order.append(key)
                else:
                    existing = tool_map[key]
                    existing["reasoning"] = _prefer_reasoning(
                        existing.get("reasoning"),
                        reasoning_text,
                    )
                tools_placeholder.markdown(_format_tool_lines([tool_map[k] for k in tool_order]))
                continue

            if event_type == "llm_response":
                usage = event.get("usage")
                if isinstance(usage, dict):
                    for metric_key in usage_totals:
                        value = usage.get(metric_key)
                        if isinstance(value, int):
                            usage_totals[metric_key] += value
                stage = str(event.get("stage") or "next_action")
                status_placeholder.info(f"Model responded ({stage})")
                continue

            if event_type == "run_completed":
                status_placeholder.success("Run completed")
                final_text = str(event.get("final_text") or "")
                if final_text.strip():
                    response_chunks = [final_text]
                    response_placeholder.markdown(final_text)
                continue

            if event_type == "run_failed":
                err = str(event.get("error") or "Unknown error")
                status_placeholder.error(f"Run failed: {err}")

    final_text = "".join(response_chunks).strip()
    tool_events = [tool_map[k] for k in tool_order]
    usage_lines = [
        "tokens(in/out/total/reasoning)="
        f"{usage_totals['input_tokens']}/"
        f"{usage_totals['output_tokens']}/"
        f"{usage_totals['total_tokens']}/"
        f"{usage_totals['reasoning_tokens']}"
    ]
    if not final_text:
        final_text = "_No final text returned._"
    for item in tool_events:
        if isinstance(item.get("reasoning"), str):
            item["reasoning"] = _short_text(str(item["reasoning"]), 200)
    return final_text, tool_events, usage_lines


def main() -> None:
    Agent.load_dotenv_if_available()
    st.set_page_config(page_title="MTP Groq Agent Chat", page_icon="MTP", layout="wide")
    _init_state()

    st.title("MTP Streamlit Chat")
    st.caption("Groq-backed orchestration agent with live tool activity (name + reasoning).")

    with st.sidebar:
        st.header("Settings")
        model = st.text_input("Groq model", value="moonshotai/kimi-k2-instruct")
        max_rounds = st.slider("Max rounds", min_value=1, max_value=24, value=12, step=1)
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = f"streamlit-{uuid4()}"
            st.rerun()
        st.caption("Set `GROQ_API_KEY` in your environment or `.env`.")

    cwd = pathlib.Path.cwd()
    agent = _ensure_agent(model=model, cwd=cwd)
    _render_history()

    prompt = st.chat_input("Ask a complex task that needs tools...")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    final_text, tool_events, usage_lines = _run_turn(
        agent=agent,
        prompt=prompt,
        max_rounds=max_rounds,
        session_id=st.session_state.session_id,
    )
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_text,
            "tool_events": tool_events,
            "usage_lines": usage_lines,
        }
    )


if __name__ == "__main__":
    main()
