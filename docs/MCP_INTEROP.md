# MCP Interoperability Adapter (Experimental)

This document explains how MCP is wrapped inside MTP today, what is implemented now, and what still needs to be added for broader interoperability.

## Why this exists

MTP is the runtime/orchestration core.  
MCP is a protocol boundary for interoperability.

The adapter in `src/mtp/mcp.py` keeps this split:

1. `MTP runtime` remains the source of truth for tool registry, policy, and execution.
2. `MCP adapter` translates JSON-RPC messages into MTP tool operations.
3. Results and errors are translated back into JSON-RPC responses.

This avoids rewriting existing runtime logic while enabling protocol-level integration.

## Implemented now

`MCPJsonRpcServer` (in `src/mtp/mcp.py`) currently supports:

1. JSON-RPC 2.0 request validation and error envelopes.
2. Lifecycle gates:
- `initialize`
- `notifications/initialized` (notification-only)
3. Basic capability negotiation payload returned from `initialize`:
- `tools` capability with `listChanged=false`
4. Methods:
- `ping`
- `tools/list`
- `tools/call`
5. Optional request-level auth:
- static token (`auth_token`)
- or custom validator callback (`auth_validator`)
6. Stdio loop utility:
- `run_mcp_stdio(server)` for one-line JSON request/response operation.

## Not implemented yet

This adapter is intentionally thin. The following are not yet implemented:

1. MCP resources/prompts APIs.
2. Streaming chunks/progress/cancellation semantics.
3. HTTP transport adapter specialized for MCP headers/session semantics.
4. Rich capability matrix negotiation beyond the minimal tools capability.
5. Production-grade auth stacks (OAuth discovery, scope negotiation, refresh lifecycle).
6. Cross-session resumability model standardized to MCP expectations.

## Step-by-step request flow

### 1) Lifecycle setup

Client sends `initialize`.

Server stores:
- `clientInfo`
- `capabilities`
- initialization timestamp

Server responds with:
- `protocolVersion` (echoed from client when provided, else server default)
- `serverInfo`
- supported capabilities
- human instructions text

### 2) Client ready notification

Client sends `notifications/initialized` as a JSON-RPC notification (no `id`).

Server marks client as ready and returns no response body.

### 3) Tool discovery

Client sends `tools/list`.

Server maps each `ToolSpec` from `ToolRegistry.list_tools()` into MCP-facing fields:
- `name`
- `description`
- `inputSchema`
- `annotations` (risk/cost/side-effect hints derived from MTP metadata)

### 4) Tool invocation

Client sends `tools/call` with:
- `name`
- optional `arguments`
- optional `callId`

Server converts to MTP `ToolCall`, executes via `ToolRegistry.execute_call(...)`, and returns:
- `content` text block for model-facing usage
- `isError` flag
- detailed result metadata under `result`

## Method contracts (current adapter)

## `initialize`

Request params:
- `protocolVersion` (optional string)
- `clientInfo` (optional object)
- `capabilities` (optional object)

Response result:
- `protocolVersion`
- `serverInfo` (`name`, `version`)
- `capabilities` (`tools.listChanged`)
- `instructions`

## `notifications/initialized`

Request:
- notification (no `id`)

Response:
- none

## `ping`

Response result:
- `ok: true`
- `timestamp` (ISO datetime)

## `tools/list`

Response result:
- `tools: [...]`

Each tool contains:
- `name`
- `description`
- `inputSchema`
- `annotations` (`title`, `riskLevel`, `costHint`, `sideEffects`)

## `tools/call`

Request params:
- `name` (required)
- `arguments` (optional object, defaults to `{}`)
- `callId` (optional)

Response result:
- `isError`
- `content: [{type: "text", text: "..."}]`
- `result`:
  - `callId`
  - `toolName`
  - `success`
  - `error`
  - `cached`
  - `approval`
  - `skipped`
  - `output`

## Error handling model

Adapter emits JSON-RPC shaped errors:

- `-32700`: parse error
- `-32600`: invalid request
- `-32602`: invalid params / method usage issues
- `-32000`: internal server error
- `-32001`: unauthorized
- `-32002`: server not initialized

## Auth model (current)

Auth is request-level and transport-agnostic.

Token sources accepted:
1. `request.meta.authToken`
2. `request.params.auth_token`

Validation options:
1. Static token check via `auth_token`.
2. Custom logic via `auth_validator(token, request)`.

Important:
- This is a practical local/integration guard, not a complete production auth stack.
- For internet-facing deployments, add transport-specific auth hardening before use.

## Usage example

Minimal stdio server:

```python
from mtp import MCPJsonRpcServer, ToolRegistry, ToolSpec, run_mcp_stdio

tools = ToolRegistry()
tools.register_tool(ToolSpec(name="calc.add", description="Add"), lambda a, b: a + b)

server = MCPJsonRpcServer(tools=tools)
run_mcp_stdio(server)
```

Repository example:
- [mcp_stdio_server.py](/c:/Users/prajw/Downloads/MTP/examples/mcp_stdio_server.py)

## Testing coverage

Current test coverage in:
- [test_mcp_adapter.py](/c:/Users/prajw/Downloads/MTP/tests/test_mcp_adapter.py)

Covered behaviors:
- lifecycle enforcement before/after initialize
- tool listing and invocation mapping
- auth denial path
- notification no-response behavior
- success/error shape validation for tool calls

## Practical roadmap for full interoperability

1. Add MCP resources/prompts endpoints mapped to MTP abstractions.
2. Add structured progress notifications and cancellation.
3. Add HTTP MCP transport adapter with hardened auth and session handling.
4. Add compatibility tests against external MCP clients.
5. Publish explicit version support matrix in docs.

