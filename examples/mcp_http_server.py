import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import MCPHTTPTransportServer, MCPJsonRpcServer, ToolRegistry, ToolSpec


def main() -> None:
    tools = ToolRegistry()
    tools.register_tool(ToolSpec(name="calc.add", description="Add two numbers"), lambda a, b: a + b)
    tools.register_tool(ToolSpec(name="calc.mul", description="Multiply two numbers"), lambda a, b: a * b)

    server = MCPJsonRpcServer(
        tools=tools,
        instructions="MCP HTTP demo server. POST JSON-RPC to /rpc and poll /events for progress.",
    )
    transport = MCPHTTPTransportServer("127.0.0.1", 8081, server)
    transport.start()


if __name__ == "__main__":
    main()
