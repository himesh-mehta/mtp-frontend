from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent
from mtp.providers import Groq


@Agent.mtp_tool(description="Add two integers and return the sum.")
def add(a: int, b: int) -> int:
    return a + b


@Agent.mtp_tool(description="Reverse a string.")
def reverse_text(text: str) -> str:
    return text[::-1]


def main() -> None:
    Agent.load_dotenv_if_available()
    provider = Groq(model="moonshotai/kimi-k2-instruct")

    tools = Agent.ToolRegistry()
    tools.register_toolkit_loader("custom", Agent.toolkit_from_functions("custom", add, reverse_text))

    agent = Agent.MTPAgent(
        provider=provider,
        tools=tools,
        instructions="Use tools when useful and keep responses concise.",
    )
    print(agent.run("Add 40 and 2, then reverse 'MTP'."))


if __name__ == "__main__":
    main()

