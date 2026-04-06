from __future__ import annotations

import asyncio
import json
from pathlib import Path
import shlex
import socket
import subprocess
import threading
import time
from typing import Any, Protocol
from urllib import request

from mtp import MCPHTTPTransportServer, MCPJsonRpcServer


class ConformanceClient(Protocol):
    client_id: str
    client_name: str
    client_version: str
    transport: str

    def initialize(self) -> dict[str, Any]:
        ...

    def initialized_notification(self) -> None:
        ...

    def tools_list(self) -> dict[str, Any]:
        ...

    def tools_call(self, *, request_id: str, name: str, arguments: dict[str, Any], progress_token: str | None = None) -> dict[str, Any]:
        ...

    def resources_list(self) -> dict[str, Any]:
        ...

    def resources_read(self, *, uri: str) -> dict[str, Any]:
        ...

    def prompts_list(self) -> dict[str, Any]:
        ...

    def prompts_get(self, *, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        ...

    def cancel_request(self, *, request_id: str) -> None:
        ...

    def progress_events(self) -> list[dict[str, Any]]:
        ...

    def auth_initialize(self, *, token: str | None) -> tuple[int, dict[str, Any], dict[str, str]]:
        ...


class DirectJsonRpcClient:
    client_id = "direct-jsonrpc-v1"
    client_name = "direct-jsonrpc"
    client_version = "v1"
    transport = "direct"

    def __init__(self, server: MCPJsonRpcServer, auth_server: MCPJsonRpcServer) -> None:
        self.server = server
        self.auth_server = auth_server

    def _request(self, method: str, *, request_id: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}}
        response = self.server.handle_request(payload)
        return response or {}

    def initialize(self) -> dict[str, Any]:
        return self._request(
            "initialize",
            request_id="init-1",
            params={"protocolVersion": "2026-03-26", "clientInfo": {"name": self.client_name}},
        )

    def initialized_notification(self) -> None:
        self.server.handle_request({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})

    def tools_list(self) -> dict[str, Any]:
        return self._request("tools/list", request_id="tools-list")

    def tools_call(self, *, request_id: str, name: str, arguments: dict[str, Any], progress_token: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"name": name, "arguments": arguments}
        if progress_token:
            params["progressToken"] = progress_token
        return self._request("tools/call", request_id=request_id, params=params)

    def resources_list(self) -> dict[str, Any]:
        return self._request("resources/list", request_id="resources-list")

    def resources_read(self, *, uri: str) -> dict[str, Any]:
        return self._request("resources/read", request_id="resources-read", params={"uri": uri})

    def prompts_list(self) -> dict[str, Any]:
        return self._request("prompts/list", request_id="prompts-list")

    def prompts_get(self, *, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        return self._request("prompts/get", request_id="prompts-get", params={"name": name, "arguments": arguments})

    def cancel_request(self, *, request_id: str) -> None:
        self.server.handle_request({"jsonrpc": "2.0", "method": "$/cancelRequest", "params": {"id": request_id}})

    def progress_events(self) -> list[dict[str, Any]]:
        return list(self.server.progress_events)

    def auth_initialize(self, *, token: str | None) -> tuple[int, dict[str, Any], dict[str, str]]:
        params: dict[str, Any] = {}
        if token is not None:
            params["auth_token"] = token
        payload = {"jsonrpc": "2.0", "id": "auth-init", "method": "initialize", "params": params}
        response = self.auth_server.handle_request(payload) or {}
        return 200, response, {}


class HttpJsonRpcClient:
    client_id = "http-jsonrpc-v1"
    client_name = "http-jsonrpc"
    client_version = "v1"
    transport = "http"

    def __init__(self, *, server: MCPJsonRpcServer, auth_server: MCPJsonRpcServer) -> None:
        self._port = self._free_port()
        self._auth_port = self._free_port()
        self._transport = MCPHTTPTransportServer("127.0.0.1", self._port, server)
        self._auth_transport = MCPHTTPTransportServer("127.0.0.1", self._auth_port, auth_server)
        self._thread = threading.Thread(target=self._transport.start, daemon=True)
        self._auth_thread = threading.Thread(target=self._auth_transport.start, daemon=True)
        self._thread.start()
        self._auth_thread.start()
        time.sleep(0.1)

    def close(self) -> None:
        self._transport.shutdown()
        self._auth_transport.shutdown()
        self._thread.join(timeout=1)
        self._auth_thread.join(timeout=1)

    def _free_port(self) -> int:
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        _, port = sock.getsockname()
        sock.close()
        return int(port)

    def _post(self, *, base_port: int, payload: dict[str, Any], headers: dict[str, str] | None = None) -> tuple[int, dict[str, Any], dict[str, str]]:
        req = request.Request(
            f"http://127.0.0.1:{base_port}/rpc",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json", **(headers or {})},
        )
        with request.urlopen(req, timeout=5) as resp:
            raw = resp.read().decode("utf-8")
            body = json.loads(raw) if raw else {}
            return int(resp.status), body, dict(resp.headers)

    def _get_events(self) -> list[dict[str, Any]]:
        req = request.Request(f"http://127.0.0.1:{self._port}/events?since_id=0&limit=200", method="GET")
        with request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return list(payload.get("events", []))

    def initialize(self) -> dict[str, Any]:
        _status, body, _headers = self._post(
            base_port=self._port,
            payload={
                "jsonrpc": "2.0",
                "id": "init-1",
                "method": "initialize",
                "params": {"protocolVersion": "2026-03-26", "clientInfo": {"name": self.client_name}},
            },
        )
        return body

    def initialized_notification(self) -> None:
        self._post(
            base_port=self._port,
            payload={"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        )

    def tools_list(self) -> dict[str, Any]:
        _status, body, _headers = self._post(
            base_port=self._port,
            payload={"jsonrpc": "2.0", "id": "tools-list", "method": "tools/list", "params": {}},
        )
        return body

    def tools_call(self, *, request_id: str, name: str, arguments: dict[str, Any], progress_token: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"name": name, "arguments": arguments}
        if progress_token:
            params["progressToken"] = progress_token
        _status, body, _headers = self._post(
            base_port=self._port,
            payload={"jsonrpc": "2.0", "id": request_id, "method": "tools/call", "params": params},
        )
        return body

    def resources_list(self) -> dict[str, Any]:
        _status, body, _headers = self._post(
            base_port=self._port,
            payload={"jsonrpc": "2.0", "id": "resources-list", "method": "resources/list", "params": {}},
        )
        return body

    def resources_read(self, *, uri: str) -> dict[str, Any]:
        _status, body, _headers = self._post(
            base_port=self._port,
            payload={"jsonrpc": "2.0", "id": "resources-read", "method": "resources/read", "params": {"uri": uri}},
        )
        return body

    def prompts_list(self) -> dict[str, Any]:
        _status, body, _headers = self._post(
            base_port=self._port,
            payload={"jsonrpc": "2.0", "id": "prompts-list", "method": "prompts/list", "params": {}},
        )
        return body

    def prompts_get(self, *, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        _status, body, _headers = self._post(
            base_port=self._port,
            payload={"jsonrpc": "2.0", "id": "prompts-get", "method": "prompts/get", "params": {"name": name, "arguments": arguments}},
        )
        return body

    def cancel_request(self, *, request_id: str) -> None:
        self._post(
            base_port=self._port,
            payload={"jsonrpc": "2.0", "method": "$/cancelRequest", "params": {"id": request_id}},
        )

    def progress_events(self) -> list[dict[str, Any]]:
        return self._get_events()

    def auth_initialize(self, *, token: str | None) -> tuple[int, dict[str, Any], dict[str, str]]:
        params: dict[str, Any] = {}
        if token is not None:
            params["auth_token"] = token
        return self._post(
            base_port=self._auth_port,
            payload={"jsonrpc": "2.0", "id": "auth-init", "method": "initialize", "params": params},
        )


class SubprocessExternalClient:
    """
    Optional wrapper for external client conformance adapters.

    Contract:
    - command must accept JSON payload on stdin
    - command must emit JSON payload on stdout
    - payload shape:
      {"action":"run","server":{"rpc_url": "...", "events_url":"..."}, "scenario":"..."}
    """

    def __init__(self, *, command: str, rpc_url: str, events_url: str) -> None:
        self.command = shlex.split(command)
        self.rpc_url = rpc_url
        self.events_url = events_url

    def run(self, *, scenario: str, timeout: float = 30.0) -> dict[str, Any]:
        proc = subprocess.run(  # noqa: S603
            self.command,
            input=json.dumps(
                {
                    "action": "run",
                    "scenario": scenario,
                    "server": {"rpc_url": self.rpc_url, "events_url": self.events_url},
                }
            ),
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        if proc.returncode != 0:
            return {"ok": False, "error": f"external client exited {proc.returncode}", "stderr": proc.stderr}
        try:
            payload = json.loads(proc.stdout or "{}")
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": f"invalid json from external client: {exc}", "stdout": proc.stdout}
        if not isinstance(payload, dict):
            return {"ok": False, "error": "external client returned non-object payload"}
        return payload

