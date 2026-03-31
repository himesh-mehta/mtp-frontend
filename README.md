# MTP Python

MTP is a protocol-first Python library for agent tool orchestration, built to support:
- Lazy tool loading by toolkit/category.
- Dependency-aware batch tool execution.
- Policy-aware execution based on tool risk.
- Provider adapters (now including Groq).

## Repository structure

- `src/mtp/protocol.py`: Core protocol entities (`ToolSpec`, `ToolCall`, `ExecutionPlan`, etc.).
- `src/mtp/schema.py`: Versioned envelope + execution plan validation.
- `src/mtp/policy.py`: Risk policy (`allow` / `ask` / `deny`).
- `src/mtp/runtime.py`: Tool registry, lazy loading, caching, batch execution.
- `src/mtp/agent.py`: Agent loop around provider + runtime.
- `src/mtp/providers/`: Provider adapters (`MockPlannerProvider`, `GroqToolCallingProvider`).
- `docs/`: Architecture, roadmap, protocol details, Groq integration guide.

## Install

### Base install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

### Provider SDKs and dotenv (install separately)

```bash
pip install groq
pip install python-dotenv
```

Copy `.env.example` to `.env` and set your key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Quickstart

### Local mock planner

```bash
python examples/quickstart.py
```

### Groq provider (real API)

```bash
python examples/groq_agent.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```
