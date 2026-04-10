from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any

from mtp import Agent
from mtp.providers import OpenAI
from mtp.toolkits.local import register_local_toolkits


_BACKENDS = {"codex", "mtp-openai"}
_REASONING_EFFORTS = ("none", "low", "medium", "high", "xhigh")
_MAX_ATTACHMENTS = 8
_MAX_ATTACHMENT_CHARS = 16000

_MODEL_PRESETS: list[tuple[str, str]] = [
    ("gpt-5.4", "Frontier general coding model"),
    ("gpt-5.4-mini", "Faster/cheaper coding model"),
    ("gpt-5.3-codex", "Codex-optimized coding model"),
    ("gpt-5.2", "Previous frontier model"),
]

_MODEL_SHORTCUTS = {
    "1": "gpt-5.4",
    "2": "gpt-5.4-mini",
    "3": "gpt-5.3-codex",
    "4": "gpt-5.2",
}

_REASONING_SHORTCUTS = {
    "0": "none",
    "1": "low",
    "2": "medium",
    "3": "high",
    "4": "xhigh",
}

_REASONING_NOTES = {
    "gpt-5.4": "none, low, medium, high, xhigh",
    "gpt-5.3-codex": "low, medium, high, xhigh",
}


@dataclass
class ChatResult:
    text: str
    tool_events: list[str]
    attachments: list[str]
    warnings: list[str]


@dataclass
class TUIState:
    backend: str
    codex_model: str | None
    openai_model: str
    max_rounds: int
    cwd: Path
    autoresearch: bool
    research_instructions: str | None
    reasoning_effort: str
    agent: Agent.MTPAgent | None = None
    codex_bin: str | None = None


def _print_banner(state: TUIState) -> None:
    active_model = state.codex_model if state.backend == "codex" else state.openai_model
    print("=" * 72)
    print("MTP TUI")
    print("Interactive terminal UI for MTP SDK + Codex CLI bridge")
    print("=" * 72)
    print(
        "Models: [1] GPT-5.4  [2] GPT-5.4-mini  [3] GPT-5.3-codex  [4] GPT-5.2"
    )
    print("Reasoning: [0] none  [1] low  [2] medium  [3] high  [4] xhigh")
    print("Commands: /help /backend /model /reasoning /rounds /status /exit")
    print("Extra: /models /codex-login /autoresearch on|off /research <text> /cd <dir>")
    print("Tip: leading '/' is optional for commands (for example `codex-login` also works).")
    print(
        f"Current backend: {state.backend} | model: {active_model or '(codex-default)'} | reasoning: {state.reasoning_effort}"
    )
    print(f"cwd: {state.cwd}")
    print("Tip: include @relative/path.py in your prompt to attach file contents.")
    print("-" * 72)


def _print_help() -> None:
    print("Available commands:")
    print("  /help                         Show command help")
    print("  /exit                         Exit TUI")
    print("  /status                       Show current TUI/session state")
    print("  /backend codex|mtp-openai     Switch backend")
    print("  /models                       Show model + reasoning presets")
    print("  /model <name|1..4|default>    Set model for active backend")
    print("  /reasoning <none|low|...>     Set reasoning effort for codex backend")
    print("  /rounds <n>                   Set max_rounds for mtp-openai backend")
    print("  /autoresearch on|off          Toggle autoresearch for mtp-openai backend")
    print("  /research <text>              Set research_instructions for mtp-openai backend")
    print("  /codex-login                  Run official `codex login`")
    print("  /cd <dir>                     Change working directory for both backends")
    print("Prompt UX:")
    print("  Type @path/to/file.py in a prompt to attach file context to the request.")
    print("  Example: explain bug in @src/mtp/cli/tui.py and propose patch")


def _print_model_matrix(state: TUIState) -> None:
    print("Model presets:")
    for idx, (model, note) in enumerate(_MODEL_PRESETS, start=1):
        marker = " (selected)" if model in {state.codex_model, state.openai_model} else ""
        print(f"  {idx}. {model}{marker} - {note}")
    print("Reasoning presets:")
    print("  0. none  1. low  2. medium  3. high  4. xhigh")
    print("Model-specific notes (from current OpenAI docs):")
    print(f"  gpt-5.4 -> {_REASONING_NOTES['gpt-5.4']}")
    print(f"  gpt-5.3-codex -> {_REASONING_NOTES['gpt-5.3-codex']}")
    print(
        "Use `/model 3` and `/reasoning high`, or `/model gpt-5.4-mini`."
    )


def _detect_codex_bin() -> str | None:
    for candidate in ("codex.cmd", "codex"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None


def _ensure_openai_agent(state: TUIState) -> Agent.MTPAgent:
    if state.agent is not None:
        return state.agent
    Agent.load_dotenv_if_available()
    tools = Agent.ToolRegistry()
    register_local_toolkits(tools, base_dir=state.cwd)
    provider = OpenAI(model=state.openai_model)
    state.agent = Agent.MTPAgent(
        provider=provider,
        tools=tools,
        strict_dependency_mode=True,
        autoresearch=state.autoresearch,
        research_instructions=state.research_instructions,
    )
    return state.agent


def _parse_codex_json_events(stdout_text: str) -> tuple[str, list[str], list[str]]:
    tool_events: list[str] = []
    warnings: list[str] = []
    final_text = ""
    assistant_chunks: list[str] = []
    for raw_line in stdout_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("ERROR:"):
            warnings.append(line)
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            warnings.append(line)
            continue
        event_type = str(event.get("type", "")).strip().lower()
        if event_type in {"response.output_text.delta", "response.output_text"}:
            delta = event.get("delta") or event.get("text") or ""
            if isinstance(delta, str) and delta:
                assistant_chunks.append(delta)
            continue
        if event_type in {"assistant_message", "message"}:
            text = event.get("text") or event.get("content") or ""
            if isinstance(text, str) and text.strip():
                final_text = text.strip()
            continue
        if "tool" in event_type or "exec_command" in event_type:
            name = event.get("name") or event.get("tool_name") or event_type
            detail = event.get("summary") or event.get("command") or ""
            if detail:
                tool_events.append(f"{name}: {detail}")
            else:
                tool_events.append(str(name))
            continue
    if assistant_chunks:
        final_text = "".join(assistant_chunks).strip() or final_text
    return final_text, tool_events, warnings


def _run_codex_prompt(state: TUIState, prompt: str) -> ChatResult:
    codex_bin = state.codex_bin or _detect_codex_bin()
    state.codex_bin = codex_bin
    if not codex_bin:
        return ChatResult(
            text=(
                "Codex CLI not found on PATH.\n"
                "Install with: npm install -g @openai/codex\n"
                "Then login with: codex login"
            ),
            tool_events=[],
            attachments=[],
            warnings=[],
        )

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as tmp:
        output_path = Path(tmp.name)

    cmd = [
        codex_bin,
        "exec",
        "--skip-git-repo-check",
        "-C",
        str(state.cwd),
        "--json",
        "--output-last-message",
        str(output_path),
    ]
    if state.codex_model:
        cmd.extend(["-m", state.codex_model])
    if state.reasoning_effort in _REASONING_EFFORTS and state.reasoning_effort != "none":
        cmd.extend(["-c", f'reasoning_effort="{state.reasoning_effort}"'])
    cmd.append(prompt)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    text = ""
    try:
        if output_path.exists():
            text = output_path.read_text(encoding="utf-8", errors="replace").strip()
    finally:
        try:
            output_path.unlink(missing_ok=True)
        except Exception:
            pass

    parsed_text, tool_events, parse_warnings = _parse_codex_json_events(proc.stdout or "")

    if proc.returncode != 0:
        details = (proc.stderr or proc.stdout or "").strip()
        hint = "Try: codex login"
        if details:
            return ChatResult(
                text=f"Codex exec failed (exit {proc.returncode}).\n{details}\n{hint}",
                tool_events=tool_events,
                attachments=[],
                warnings=parse_warnings,
            )
        return ChatResult(
            text=f"Codex exec failed (exit {proc.returncode}).\n{hint}",
            tool_events=tool_events,
            attachments=[],
            warnings=parse_warnings,
        )

    if text:
        final_text = text
    elif parsed_text:
        final_text = parsed_text
    elif proc.stdout.strip():
        final_text = proc.stdout.strip()
    else:
        final_text = "(Codex returned no final text.)"
    return ChatResult(
        text=final_text,
        tool_events=tool_events,
        attachments=[],
        warnings=parse_warnings,
    )


def _run_codex_login(state: TUIState) -> str:
    codex_bin = state.codex_bin or _detect_codex_bin()
    state.codex_bin = codex_bin
    if not codex_bin:
        return "Codex CLI not found on PATH. Install: npm install -g @openai/codex"
    proc = subprocess.run([codex_bin, "login"], text=True)
    if proc.returncode == 0:
        return "Codex login completed."
    return f"Codex login exited with code {proc.returncode}."


def _status_lines(state: TUIState) -> list[str]:
    return [
        f"backend={state.backend}",
        f"cwd={state.cwd}",
        f"codex_model={state.codex_model or '(codex-default)'}",
        f"openai_model={state.openai_model}",
        f"max_rounds={state.max_rounds}",
        f"autoresearch={state.autoresearch}",
        f"research_instructions={state.research_instructions or '(none)'}",
        f"reasoning_effort={state.reasoning_effort}",
    ]


def _resolve_model(arg: str) -> str:
    normalized = arg.strip().lower()
    if normalized in _MODEL_SHORTCUTS:
        return _MODEL_SHORTCUTS[normalized]
    return arg.strip()


def _resolve_reasoning(arg: str) -> str | None:
    normalized = arg.strip().lower()
    if normalized in _REASONING_SHORTCUTS:
        return _REASONING_SHORTCUTS[normalized]
    if normalized in _REASONING_EFFORTS:
        return normalized
    if normalized in {"extra-high", "extra_high"}:
        return "xhigh"
    return None


def _handle_command(state: TUIState, raw: str) -> str | None:
    parts = raw.strip().split(" ", 1)
    cmd = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else ""

    if cmd == "/help":
        _print_help()
        return None
    if cmd == "/exit":
        return "__exit__"
    if cmd == "/status":
        return "\n".join(_status_lines(state))
    if cmd == "/models":
        _print_model_matrix(state)
        return None
    if cmd == "/backend":
        if arg not in _BACKENDS:
            return "Usage: /backend codex|mtp-openai"
        state.backend = arg
        return f"Switched backend to {arg}."
    if cmd == "/model":
        if not arg:
            _print_model_matrix(state)
            return "Usage: /model <name|1..4|default>"
        resolved = _resolve_model(arg)
        if state.backend == "codex":
            if resolved.lower() in {"default", "auto"}:
                state.codex_model = None
                return "Codex model reset to CLI default."
            state.codex_model = resolved
            return f"Codex model set to {resolved}."
        state.openai_model = resolved
        state.agent = None
        return f"OpenAI model set to {resolved}. Agent reloaded."
    if cmd == "/reasoning":
        if not arg:
            return "Usage: /reasoning <none|low|medium|high|xhigh>"
        resolved_reasoning = _resolve_reasoning(arg)
        if resolved_reasoning is None:
            return "Usage: /reasoning <none|low|medium|high|xhigh>"
        state.reasoning_effort = resolved_reasoning
        return (
            f"reasoning_effort set to {resolved_reasoning}. "
            "For now this is forwarded to codex backend."
        )
    if cmd == "/rounds":
        if not arg.isdigit():
            return "Usage: /rounds <positive-int>"
        rounds = int(arg)
        if rounds < 1:
            return "max_rounds must be >= 1"
        state.max_rounds = rounds
        return f"max_rounds set to {rounds}."
    if cmd == "/autoresearch":
        lowered = arg.lower()
        if lowered not in {"on", "off"}:
            return "Usage: /autoresearch on|off"
        state.autoresearch = lowered == "on"
        state.agent = None
        return f"autoresearch={state.autoresearch}. Agent reloaded."
    if cmd == "/research":
        state.research_instructions = arg or None
        state.agent = None
        return "research_instructions updated. Agent reloaded."
    if cmd == "/codex-login":
        return _run_codex_login(state)
    if cmd == "/cd":
        if not arg:
            return "Usage: /cd <dir>"
        target = Path(arg).expanduser().resolve()
        if not target.exists() or not target.is_dir():
            return f"Directory not found: {target}"
        state.cwd = target
        state.agent = None
        return f"cwd set to {target}. Agent reloaded."
    return "Unknown command. Use /help."


def _normalize_input(raw: str) -> str:
    # Support command entry without leading slash, e.g. `codex-login`.
    command_heads = {
        "help",
        "exit",
        "status",
        "backend",
        "models",
        "model",
        "reasoning",
        "rounds",
        "codex-login",
        "autoresearch",
        "research",
        "cd",
    }
    if raw.startswith("/"):
        return raw
    head = raw.split(" ", 1)[0].strip().lower()
    if head in command_heads:
        return "/" + raw
    return raw


def _token_looks_like_file_ref(token: str) -> bool:
    if token.startswith("@/"):
        return True
    path_token = token[1:]
    return any(ch in path_token for ch in ("/", "\\", ".")) and "@" not in path_token


def _collect_prompt_attachments(prompt: str, cwd: Path) -> tuple[str, list[str], list[str]]:
    attachments: list[str] = []
    warnings: list[str] = []
    appended_blocks: list[str] = []
    for token in re.findall(r"(?<!\S)@[^\s]+", prompt):
        if not _token_looks_like_file_ref(token):
            continue
        if len(attachments) >= _MAX_ATTACHMENTS:
            warnings.append(
                f"Attachment limit reached ({_MAX_ATTACHMENTS}); skipping additional @file tokens."
            )
            break
        raw_path = token[1:]
        path = Path(raw_path)
        resolved = (cwd / path).resolve() if not path.is_absolute() else path.resolve()
        if not resolved.exists():
            warnings.append(f"Attachment not found: {raw_path}")
            continue
        if not resolved.is_file():
            warnings.append(f"Attachment is not a file: {raw_path}")
            continue
        try:
            text = resolved.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Could not read attachment {raw_path}: {exc}")
            continue
        if len(text) > _MAX_ATTACHMENT_CHARS:
            text = text[:_MAX_ATTACHMENT_CHARS]
            warnings.append(
                f"Attachment truncated to {_MAX_ATTACHMENT_CHARS} chars: {raw_path}"
            )
        display_path = str(resolved.relative_to(cwd)) if resolved.is_relative_to(cwd) else str(resolved)
        attachments.append(display_path)
        appended_blocks.append(
            "\n".join(
                [
                    f"[Attached file: {display_path}]",
                    "```text",
                    text,
                    "```",
                ]
            )
        )
    if not appended_blocks:
        return prompt, attachments, warnings
    expanded = f"{prompt}\n\n" + "\n\n".join(appended_blocks)
    return expanded, attachments, warnings


def _render_prompt_and_response(result: ChatResult) -> None:
    if result.attachments:
        print("attachments>")
        for item in result.attachments:
            print(f"  - {item}")
    if result.tool_events:
        print("tools>")
        for event in result.tool_events:
            print(f"  - {event}")
    if result.warnings:
        print("notes>")
        for warning in result.warnings:
            print(f"  - {warning}")
    print("assistant>")
    print(result.text)
    print()


def run_tui(args) -> int:
    state = TUIState(
        backend=args.backend,
        codex_model=args.codex_model,
        openai_model=args.openai_model,
        max_rounds=int(args.max_rounds),
        cwd=Path(args.cwd).expanduser().resolve(),
        autoresearch=bool(args.autoresearch),
        research_instructions=args.research_instructions,
        reasoning_effort=str(getattr(args, "reasoning_effort", "medium")),
    )
    _print_banner(state)

    while True:
        try:
            raw = input("mtp> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting TUI.")
            return 0
        if not raw:
            continue
        raw = _normalize_input(raw)
        if raw.startswith("/"):
            out = _handle_command(state, raw)
            if out == "__exit__":
                print("Bye.")
                return 0
            if out:
                print(out)
            continue

        expanded_prompt, attachments, attachment_warnings = _collect_prompt_attachments(raw, state.cwd)
        active_model = (
            state.codex_model or "(codex-default)"
            if state.backend == "codex"
            else state.openai_model
        )
        print(f"[{state.backend}] model={active_model} reasoning={state.reasoning_effort} running...")
        try:
            if state.backend == "codex":
                result = _run_codex_prompt(state, expanded_prompt)
                result.attachments = attachments
                result.warnings = [*attachment_warnings, *result.warnings]
            else:
                agent = _ensure_openai_agent(state)
                response = agent.run(expanded_prompt, max_rounds=state.max_rounds)
                result = ChatResult(
                    text=response,
                    tool_events=[],
                    attachments=attachments,
                    warnings=attachment_warnings,
                )
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}")
            continue
        _render_prompt_and_response(result)
