from __future__ import annotations

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import MCPJsonRpcServer, MCPServerInfo, ToolRegistry, ToolSpec


class MCPAdapterTests(unittest.TestCase):
    def _new_registry(self) -> ToolRegistry:
        reg = ToolRegistry()
        reg.register_tool(ToolSpec(name="calc.add", description="add"), lambda a, b: a + b)
        reg.register_tool(ToolSpec(name="ops.fail", description="fail"), lambda: 1 / 0)
        return reg

    def test_rejects_non_initialized_tool_methods(self) -> None:
        server = MCPJsonRpcServer(tools=self._new_registry())
        response = server.handle_request(
            {"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
        )
        assert response is not None
        self.assertEqual(response["error"]["code"], -32002)
        self.assertIn("not initialized", response["error"]["message"].lower())

    def test_initialize_then_list_tools(self) -> None:
        server = MCPJsonRpcServer(
            tools=self._new_registry(),
            server_info=MCPServerInfo(name="mtp-test", version="0.0.1"),
        )
        init = server.handle_request(
            {
                "jsonrpc": "2.0",
                "id": "init-1",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2026-03-26",
                    "clientInfo": {"name": "tester"},
                    "capabilities": {"roots": {}},
                },
            }
        )
        assert init is not None
        self.assertEqual(init["result"]["serverInfo"]["name"], "mtp-test")
        self.assertTrue(server.initialized)
        self.assertEqual(server.client_info.get("name"), "tester")

        listed = server.handle_request(
            {"jsonrpc": "2.0", "id": "tools-1", "method": "tools/list", "params": {}}
        )
        assert listed is not None
        tools = listed["result"]["tools"]
        names = [tool["name"] for tool in tools]
        self.assertIn("calc.add", names)
        self.assertIn("ops.fail", names)

    def test_tools_call_success_and_error_shapes(self) -> None:
        server = MCPJsonRpcServer(tools=self._new_registry())
        server.handle_request({"jsonrpc": "2.0", "id": "init", "method": "initialize", "params": {}})

        ok = server.handle_request(
            {
                "jsonrpc": "2.0",
                "id": "call-1",
                "method": "tools/call",
                "params": {"name": "calc.add", "arguments": {"a": 2, "b": 3}},
            }
        )
        assert ok is not None
        self.assertFalse(ok["result"]["isError"])
        self.assertEqual(ok["result"]["result"]["output"], 5)

        bad = server.handle_request(
            {
                "jsonrpc": "2.0",
                "id": "call-2",
                "method": "tools/call",
                "params": {"name": "ops.fail", "arguments": {}},
            }
        )
        assert bad is not None
        self.assertTrue(bad["result"]["isError"])
        self.assertIn("division by zero", bad["result"]["content"][0]["text"])

    def test_authentication_denies_without_token(self) -> None:
        server = MCPJsonRpcServer(tools=self._new_registry(), auth_token="secret", require_auth=True)

        denied = server.handle_request(
            {"jsonrpc": "2.0", "id": "init", "method": "initialize", "params": {}}
        )
        assert denied is not None
        self.assertEqual(denied["error"]["code"], -32001)

        allowed = server.handle_request(
            {
                "jsonrpc": "2.0",
                "id": "init-2",
                "method": "initialize",
                "params": {"auth_token": "secret"},
            }
        )
        assert allowed is not None
        self.assertIn("result", allowed)

    def test_notifications_return_none(self) -> None:
        server = MCPJsonRpcServer(tools=self._new_registry())
        server.handle_request({"jsonrpc": "2.0", "id": "init", "method": "initialize", "params": {}})
        response = server.handle_request(
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
        )
        self.assertIsNone(response)
        self.assertTrue(server.client_initialized)


if __name__ == "__main__":
    unittest.main()

