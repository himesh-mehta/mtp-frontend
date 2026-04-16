from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent
from mtp.providers import LMStudio
from mtp.toolkits import CalculatorToolkit, FileToolkit


def main() -> None:
    tools = Agent.ToolRegistry()
    tools.register_toolkit_loader("calculator", CalculatorToolkit())
    tools.register_toolkit_loader("file", FileToolkit(base_dir=pathlib.Path.cwd()))

    provider = LMStudio(
        # Change this if your loaded LM Studio model uses a different id.
        model="qwen3-4b-thinking-2507",
        base_url="http://127.0.0.1:1234/v1",
        temperature=0.0,
        parallel_tool_calls=True,
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
