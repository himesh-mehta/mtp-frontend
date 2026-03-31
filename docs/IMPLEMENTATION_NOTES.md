# Implementation Notes

## Why policy hooks were added now

Your MTP direction includes operational safety and practical adoption. A protocol that only routes tool calls but has no execution-policy layer is hard to ship in production.

Current behavior:
- `read_only` tools: default `allow`
- `write` tools: default `allow`
- `destructive` tools: default `ask` (blocked until approval flow is added)

This is configurable via `RiskPolicy`.

## Why plan validation is strict

If a provider emits invalid plan graphs, runtime errors become hard to debug. We validate before execution to fail fast and clearly.

## Why Groq adapter currently does one tool round

The current `Agent` contract has one planning phase and one finalization phase. That is enough for:
- direct response
- one model tool-call burst + final response

It does not yet support unlimited model-tool-model loops. This is planned as an `Agent.run_loop(max_rounds=N)` evolution.

## Compatibility with your MTP vision

Implemented now:
- lazy loading support in runtime
- batch execution semantics
- plan format with dependencies
- safety policy hook
- provider adapter with real external model (Groq)

Still needed to reach full ecosystem/library maturity:
- transports
- CLI scaffolding
- toolkit packages (GitHub, Slack, Email, Drive, etc.)
- docs site and benchmark suite
