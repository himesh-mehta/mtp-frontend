# MTP Roadmap (Python)

## Phase 0 (current)
- Protocol objects for tools, calls, results, and plans.
- Runtime for lazy loading, parallel/sequential batches, call dependencies.
- TTL caching for repeat calls.
- Provider adapter interface and local planner.
- Basic tests and quickstart.

## Phase 1 (next)
- Versioned wire schema (`mtp_version`, message envelope, JSON schema files).
- Deterministic plan validator:
  - no duplicate call IDs
  - cycle detection
  - dependency edge validation
- Approval policy hooks:
  - allow / ask / deny by risk level and tool tags
  - per-tool override and audit record

## Phase 2
- Real provider adapters:
  - OpenAI Responses API
  - Anthropic Messages API
  - Gemini function calling
  - Groq-compatible OpenAI schema mode
- Planner modes:
  - direct model-native tool calls
  - model-generated MTP plan mode

## Phase 3
- Transport and remote execution:
  - stdio and HTTP transports
  - remote tool servers
  - streamable partial results for long-running tools
- Unified tracing events for all tool calls.

## Phase 4
- Developer experience:
  - `mtp new` project template
  - tool decorator package (`@mtp_tool`)
  - docs site with runnable examples
  - integration test matrix across providers
