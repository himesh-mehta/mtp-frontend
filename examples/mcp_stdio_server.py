import pathlib
import sys

# Add src to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import MCPJsonRpcServer, ToolRegistry, ToolSpec, run_mcp_stdio
from mtp import MCPPrompt, MCPPromptArgument, MCPResource


def main() -> None:
    tools = ToolRegistry()
    tools.register_tool(ToolSpec(name="calc.add", description="Add two numbers"), lambda a, b: a + b)
    tools.register_tool(ToolSpec(name="calc.mul", description="Multiply two numbers"), lambda a, b: a * b)

    resources = [
        MCPResource(
            uri="memory://docs/quickstart",
            name="Quickstart",
            description="In-memory quickstart guide",
            mime_type="text/markdown",
        )
    ]
    prompts = [
        MCPPrompt(
            name="explain_math",
            description="Explain a simple arithmetic expression",
            arguments=[MCPPromptArgument(name="expression", required=True)],
            template="Explain this expression in one short paragraph: {expression}",
        )
    ]

    def read_resource(uri: str) -> str:
        if uri == "memory://docs/quickstart":
            return "# Quickstart\nUse tools/list, then tools/call to execute calc tools."
        return ""

    server = MCPJsonRpcServer(
        tools=tools,
        resources=resources,
        resource_reader=read_resource,
        prompts=prompts,
        instructions=(
            "MTP MCP adapter demo. Call initialize first, then try tools/list, tools/call, "
            "resources/list, resources/read, prompts/list, prompts/get."
        ),
    )
    run_mcp_stdio(server)


if __name__ == "__main__":
    main()
