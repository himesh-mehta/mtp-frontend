from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent
from mtp.providers import Ollama
from mtp.toolkits import CalculatorToolkit, FileToolkit


def main() -> None:
    tools = Agent.ToolRegistry()
    tools.register_toolkit_loader("calculator", CalculatorToolkit())
    tools.register_toolkit_loader("file", FileToolkit(base_dir=pathlib.Path.cwd()))

    provider = Ollama(
        # Change this if you pulled a different Ollama model.
        model="qwen3:1.7b",
        host="http://localhost:11434",
        think=True,
        options={"temperature": 0},
    )

    agent = Agent(
        provider=provider,
        tools=tools,
        instructions=(
            "Use tools when useful. For calculations, prefer the calculator tool. "
            "When asked to inspect the workspace, use the file toolkit."
        ),
        debug_mode=True,
        strict_dependency_mode=True,
    )

    response = agent.run_loop(
        "Use tools to calculate (25 * 4) + 10, then list a few files in the current directory and summarize both results.",
        max_rounds=4,
    )
    print("\nFinal Answer:\n")
    print(response)


if __name__ == "__main__":
    main()
