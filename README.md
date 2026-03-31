# MTP Python

MTP is a protocol-first Python library for agent tool orchestration.

This repository starts with:
- A protocol layer (`mtp.protocol`) for tool calls, results, and dependency-aware execution plans.
- A runtime (`mtp.runtime`) for lazy tool loading, caching, and sequential/parallel batch execution.
- A lightweight agent loop (`mtp.agent`) with a provider adapter interface.
- A mock provider and runnable example.

## Why this exists

Most ecosystems already support tool calling. What is still fragmented is:
- A shared execution-plan format for dependency-aware parallel batches.
- Standardized lazy tool loading and toolkit discovery in one runtime.
- Reusable cache semantics for tool results across turns.

MTP targets those gaps with a practical SDK and a protocol model.

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
python examples/quickstart.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```
