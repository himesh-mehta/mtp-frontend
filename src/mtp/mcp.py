from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Callable

from .protocol import ToolCall, ToolRiskLevel, ToolSpec
from .runtime import ToolRegistry

JsonDict = dict[str, Any]
AuthValidator = Callable[[str | None, JsonDict], bool]


@dataclass(slots=True)
class MCPServerInfo:
    name: str = "mtp-mcp-adapter"
    version: str = "0.1.0"


class MCPJsonRpcServer:
    """
    Thin MCP-compatible JSON-RPC adapter around MTP ToolRegistry.

    Scope:
    - lifecycle: initialize + notifications/initialized
    - capability negotiation: tools capability
    - methods: ping, tools/list, tools/call
    - optional request-level auth token validation
    """

    def __init__(
        self,
        *,
        tools: ToolRegistry,
        server_info: MCPServerInfo | None = None,
        instructions: str | None = None,
        require_auth: bool = False,
        auth_token: str | None = None,
        auth_validator: AuthValidator | None = None,
        protocol_version: str = "2026-03-26",
    ) -> None:
        self.tools = tools
        self.server_info = server_info or MCPServerInfo()
        self.instructions = instructions or (
            "This MCP compatibility server exposes MTP tools through JSON-RPC methods."
        )
        self.require_auth = require_auth
        self.auth_token = auth_token
        self.auth_validator = auth_validator
        self.protocol_version = protocol_version

        self._initialized = False
        self._client_initialized = False
        self._client_info: JsonDict = {}
        self._client_capabilities: JsonDict = {}
        self._initialized_at: datetime | None = None

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def client_initialized(self) -> bool:
        return self._client_initialized

    @property
    def client_info(self) -> JsonDict:
        return dict(self._client_info)

    def handle_json(self, raw: str) -> str | None:
        """
        Handle one JSON-RPC request payload (single request object only).
        Returns serialized response JSON, or None for notifications.
        """
        try:
            data = json.loads(raw)
        except Exception as exc:  # noqa: BLE001
            return json.dumps(self._error_response(None, -32700, f"Parse error: {exc}"))

        if not isinstance(data, dict):
            return json.dumps(self._error_response(None, -32600, "Invalid Request: expected object"))

        response = self.handle_request(data)
        if response is None:
            return None
        return json.dumps(response, default=str)

    def handle_request(self, request: JsonDict) -> JsonDict | None:
        request_id = request.get("id")
        is_notification = "id" not in request

        validation_error = self._validate_request(request)
        if validation_error is not None:
            if is_notification:
                return None
            return self._error_response(request_id, -32600, validation_error)

        method = str(request["method"])
        params = request.get("params") if isinstance(request.get("params"), dict) else {}

        if self._requires_auth(method):
            if not self._authorized(request):
                if is_notification:
                    return None
                return self._error_response(request_id, -32001, "Unauthorized")

        if method not in {"initialize", "ping", "notifications/initialized"} and not self._initialized:
            if is_notification:
                return None
            return self._error_response(request_id, -32002, "Server not initialized")

        try:
            result = self._dispatch(method, params)
        except ValueError as exc:
            if is_notification:
                return None
            return self._error_response(request_id, -32602, str(exc))
        except Exception as exc:  # noqa: BLE001
            if is_notification:
                return None
            return self._error_response(request_id, -32000, str(exc))

        if is_notification:
            return None
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    def _validate_request(self, request: JsonDict) -> str | None:
        if request.get("jsonrpc") != "2.0":
            return "Invalid Request: jsonrpc must be '2.0'"
        method = request.get("method")
        if not isinstance(method, str) or not method:
            return "Invalid Request: missing method"
        params = request.get("params")
        if params is not None and not isinstance(params, dict):
            return "Invalid params: expected object"
        return None

    def _requires_auth(self, method: str) -> bool:
        return self.require_auth or self.auth_validator is not None or self.auth_token is not None

    def _authorized(self, request: JsonDict) -> bool:
        token: str | None = None
        meta = request.get("meta")
        if isinstance(meta, dict):
            candidate = meta.get("authToken")
            if isinstance(candidate, str):
                token = candidate
        if token is None:
            params = request.get("params")
            if isinstance(params, dict):
                candidate = params.get("auth_token")
                if isinstance(candidate, str):
                    token = candidate

        if self.auth_validator is not None:
            return bool(self.auth_validator(token, request))
        if self.auth_token is not None:
            return token == self.auth_token
        return token is not None

    def _dispatch(self, method: str, params: JsonDict) -> JsonDict:
        if method == "ping":
            return {"ok": True, "timestamp": datetime.now(UTC).isoformat()}
        if method == "initialize":
            return self._initialize(params)
        if method == "notifications/initialized":
            self._client_initialized = True
            return {}
        if method == "tools/list":
            return {"tools": [self._tool_spec_to_mcp(spec) for spec in self.tools.list_tools()]}
        if method == "tools/call":
            return self._tools_call(params)
        raise ValueError(f"Method not found: {method}")

    def _initialize(self, params: JsonDict) -> JsonDict:
        requested_version = params.get("protocolVersion")
        if isinstance(requested_version, str) and requested_version.strip():
            negotiated_version = requested_version
        else:
            negotiated_version = self.protocol_version

        client_info = params.get("clientInfo")
        if isinstance(client_info, dict):
            self._client_info = dict(client_info)
        else:
            self._client_info = {}

        capabilities = params.get("capabilities")
        if isinstance(capabilities, dict):
            self._client_capabilities = dict(capabilities)
        else:
            self._client_capabilities = {}

        self._initialized = True
        self._initialized_at = datetime.now(UTC)
        return {
            "protocolVersion": negotiated_version,
            "serverInfo": {
                "name": self.server_info.name,
                "version": self.server_info.version,
            },
            "capabilities": {
                "tools": {"listChanged": False},
            },
            "instructions": self.instructions,
        }

    def _tool_spec_to_mcp(self, spec: ToolSpec) -> JsonDict:
        annotations = {
            "title": spec.name,
            "riskLevel": spec.risk_level.value if isinstance(spec.risk_level, ToolRiskLevel) else str(spec.risk_level),
            "costHint": spec.cost_hint,
            "sideEffects": spec.side_effects,
        }
        return {
            "name": spec.name,
            "description": spec.description,
            "inputSchema": spec.input_schema or {"type": "object", "additionalProperties": True},
            "annotations": annotations,
        }

    def _tools_call(self, params: JsonDict) -> JsonDict:
        name = params.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("tools/call requires string param `name`")
        arguments = params.get("arguments", {})
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, dict):
            raise ValueError("tools/call param `arguments` must be an object")
        call_id = params.get("callId")
        if not isinstance(call_id, str) or not call_id:
            call_id = f"mcp-{datetime.now(UTC).timestamp()}"

        call = ToolCall(id=call_id, name=name, arguments=arguments)
        result = self._run_coro_sync(self.tools.execute_call(call, prior_results={}))

        is_error = (not result.success) or bool(result.error)
        rendered_text = self._render_tool_output_text(result.output if result.success else result.error)
        response: JsonDict = {
            "isError": is_error,
            "content": [{"type": "text", "text": rendered_text}],
            "result": {
                "callId": result.call_id,
                "toolName": result.tool_name,
                "success": result.success,
                "error": result.error,
                "cached": result.cached,
                "approval": result.approval,
                "skipped": result.skipped,
                "output": result.output,
            },
        }
        return response

    def _run_coro_sync(self, coro: Any) -> Any:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)
        close_fn = getattr(coro, "close", None)
        if callable(close_fn):
            close_fn()
        raise RuntimeError(
            "MCPJsonRpcServer sync methods cannot run inside an active asyncio event loop. "
            "Call from non-async context or add an async wrapper."
        )

    def _render_tool_output_text(self, payload: Any) -> str:
        if payload is None:
            return ""
        if isinstance(payload, str):
            return payload
        try:
            return json.dumps(payload, ensure_ascii=True, sort_keys=True, default=str)
        except Exception:
            return str(payload)

    def _error_response(self, request_id: Any, code: int, message: str) -> JsonDict:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }


def run_mcp_stdio(server: MCPJsonRpcServer) -> None:
    """
    Line-delimited stdio JSON-RPC loop.

    Reads one JSON request object per line and writes one JSON response object per line
    for request messages. Notifications do not emit responses.
    """
    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue
        response = server.handle_json(raw)
        if response is None:
            continue
        sys.stdout.write(response + "\n")
        sys.stdout.flush()

