# MTP Python Architecture (v0.1)

## Layered design

1. `mtp.protocol`
- Defines tool metadata, call objects, results, and execution plans.
- Adds fields needed for practical orchestration: risk hints, cache TTL, dependencies.

2. `mtp.runtime`
- Maintains tool registry and toolkit loaders.
- Supports lazy toolkit loading by tool prefix (example: `github.*`).
- Executes `ExecutionPlan` batches in sequential or parallel mode.
- Resolves inter-call references via `{ "$ref": "<call_id>" }`.
- Applies result caching with TTL.

3. `mtp.agent`
- Generic agent loop:
  - gather tools
  - request plan from provider adapter
  - execute plan
  - return tool results to provider for final response

4. `mtp.providers`
- Provider adapter interface for OpenAI/Anthropic/Gemini/Groq/etc.
- Current repo includes a deterministic local planner (`SimplePlannerProvider`) for demo/testing.

## Protocol direction

Short-term (implemented):
- Standardized plan format for dependency-aware batches.
- Cache TTL semantics in tool specs.
- Lazy toolkit loading and execution in one runtime.

Next steps:
- JSON schema + versioned wire format for MTP messages.
- Transport abstraction (stdio/http/ws).
- Approval policy hooks based on risk level.
- Streaming result chunks for long-running tools.
- Cross-provider adapters.
