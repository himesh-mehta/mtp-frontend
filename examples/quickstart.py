from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent, ToolRegistry, ToolRiskLevel, ToolSpec, ToolkitLoader
from mtp.providers import MockPlannerProvider
from mtp.runtime import RegisteredTool


class GitHubToolkit(ToolkitLoader):
    def __init__(self) -> None:
        self._counter = 0

    def load_tools(self) -> list[RegisteredTool]:
        def get_user() -> dict:
            return {"login": "demo-user", "id": 123}

        def create_issue(title: str, body: dict) -> str:
            self._counter += 1
            return f"https://example.com/issues/{self._counter}?title={title}&by={body['login']}"

        return [
            RegisteredTool(
                spec=ToolSpec(
                    name="github.get_user",
                    description="Fetch authenticated GitHub user profile.",
                    input_schema={"type": "object", "properties": {}, "additionalProperties": False},
                    risk_level=ToolRiskLevel.READ_ONLY,
                    cache_ttl_seconds=60,
                ),
                handler=get_user,
            ),
            RegisteredTool(
                spec=ToolSpec(
                    name="github.create_issue",
                    description="Create a GitHub issue.",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "body": {"type": "object"},
                        },
                        "required": ["title", "body"],
                        "additionalProperties": False,
                    },
                    risk_level=ToolRiskLevel.WRITE,
                    side_effects="remote_state_change",
                ),
                handler=create_issue,
            ),
        ]


def main() -> None:
    registry = ToolRegistry()
    registry.register_toolkit_loader("github", GitHubToolkit())

    provider = MockPlannerProvider()
    agent = Agent(provider=provider, registry=registry)
    response = agent.run("Please use my profile and open an issue.")
    print(response)

    print("\nMessages:")
    for msg in agent.messages:
        print(msg)


if __name__ == "__main__":
    main()
