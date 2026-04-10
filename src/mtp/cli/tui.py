from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import tempfile

from mtp import Agent
from mtp.providers import OpenAI
from mtp.toolkits.local import register_local_toolkits


_BACKENDS = {"codex", "mtp-openai"}


@dataclass
class TUIState:
    backend: str
    codex_model: str | None
    openai_model: str
    max_rounds: int
    cwd: Path
    autoresearch: bool
    research_instructions: str | None
    agent: Agent.MTPAgent | None = None
    codex_bin: str | None = None


def _print_banner(state: TUIState) -> None:
    print("=" * 72)
    print("MTP TUI")
    print("Minimal terminal UI for MTP SDK + Codex CLI bridge")
    print("=" * 72)
    print("Commands: /help  /backend  /model  /rounds  /status  /exit")
    print("Extra: /codex-login  /autoresearch on|off  /research <text>  /cd <dir>")
    print("Tip: leading '/' is optional for commands (for example `codex-login` also works).")
    print(f"Current backend: {state.backend} | cwd: {state.cwd}")
    print("-" * 72)


def _print_help() -> None:
    print("Available commands:")
    print("  /help                         Show command help")
    print("  /exit                         Exit TUI")
    print("  /status                       Show current TUI/session state")
    print("  /backend codex|mtp-openai     Switch backend")
    print("  /model <name>                 Set model for active backend")
    print("  /rounds <n>                   Set max_rounds for mtp-openai backend")
    print("  /autoresearch on|off          Toggle autoresearch for mtp-openai backend")
    print("  /research <text>              Set research_instructions for mtp-openai backend")
    print("  /codex-login                  Run official `codex login`")
    print("  /cd <dir>                     Change working directory for both backends")


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


def _run_codex_prompt(state: TUIState, prompt: str) -> str:
    codex_bin = state.codex_bin or _detect_codex_bin()
    state.codex_bin = codex_bin
    if not codex_bin:
        return (
            "Codex CLI not found on PATH.\n"
            "Install with: npm install -g @openai/codex\n"
            "Then login with: codex login"
        )

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as tmp:
        output_path = Path(tmp.name)

    cmd = [
        codex_bin,
        "exec",
        "--skip-git-repo-check",
        "-C",
        str(state.cwd),
        "--output-last-message",
        str(output_path),
    ]
    if state.codex_model:
        cmd.extend(["-m", state.codex_model])
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

    if proc.returncode != 0:
        details = (proc.stderr or proc.stdout or "").strip()
        hint = "Try: codex login"
        if details:
            return f"Codex exec failed (exit {proc.returncode}).\n{details}\n{hint}"
        return f"Codex exec failed (exit {proc.returncode}).\n{hint}"

    if text:
        return text
    if proc.stdout.strip():
        return proc.stdout.strip()
    return "(Codex returned no final text.)"


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
    ]


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
    if cmd == "/backend":
        if arg not in _BACKENDS:
            return "Usage: /backend codex|mtp-openai"
        state.backend = arg
        return f"Switched backend to {arg}."
    if cmd == "/model":
        if not arg:
            return "Usage: /model <name>"
        if state.backend == "codex":
            if arg.lower() in {"default", "auto"}:
                state.codex_model = None
                return "Codex model reset to CLI default."
            state.codex_model = arg
            return f"Codex model set to {arg}."
        state.openai_model = arg
        state.agent = None
        return f"OpenAI model set to {arg}. Agent reloaded."
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
        "model",
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


def run_tui(args) -> int:
    state = TUIState(
        backend=args.backend,
        codex_model=args.codex_model,
        openai_model=args.openai_model,
        max_rounds=int(args.max_rounds),
        cwd=Path(args.cwd).expanduser().resolve(),
        autoresearch=bool(args.autoresearch),
        research_instructions=args.research_instructions,
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

        print(f"[{state.backend}] running...")
        try:
            if state.backend == "codex":
                result = _run_codex_prompt(state, raw)
            else:
                agent = _ensure_openai_agent(state)
                result = agent.run(raw, max_rounds=state.max_rounds)
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}")
            continue
        print("\n" + result + "\n")
