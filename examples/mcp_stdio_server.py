import pathlib
import sys

# Add src to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import MCPJsonRpcServer, ToolRegistry, ToolSpec, run_mcp_stdio


def main() -> None:
    tools = ToolRegistry()
    tools.register_tool(ToolSpec(name="calc.add", description="Add two numbers"), lambda a, b: a + b)
    tools.register_tool(ToolSpec(name="calc.mul", description="Multiply two numbers"), lambda a, b: a * b)

    server = MCPJsonRpcServer(
        tools=tools,
        instructions="MTP MCP adapter demo. Call initialize first, then tools/list or tools/call.",
    )
    run_mcp_stdio(server)


if __name__ == "__main__":
    main()

