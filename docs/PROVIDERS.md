# Providers

MTP supports both:
- short ergonomic aliases (Agno-style), for example `Groq`
- explicit provider class names, for example `GroqToolCallingProvider`

Both styles are equivalent.

## Capability contract (enforceable)

Each provider adapter exposes:

```python
def capabilities(self) -> ProviderCapabilities
```

`ProviderCapabilities` includes:
- `supports_tool_calling`
- `supports_parallel_tool_calls`
- `input_modalities` (subset of `text`, `image`, `audio`, `video`, `file`)
- `supports_tool_media_output`
- `supports_finalize_streaming`
- `usage_metrics_quality` (`none`, `basic`, `rich`)
- `supports_reasoning_metadata`
- `structured_output_support` (`none`, `client_validated`, `native_json_object`, `native_json_schema`)
- `supports_native_async`
- `allow_finalize_stream_fallback`

Runtime guardrails in `Agent`/`MTPAgent` enforce this contract:
- Unsupported requested input modality => fail fast with clear error.
- Unsupported native finalize streaming => fail fast, unless fallback is explicitly allowed.

This prevents providers from silently over-promising features in production.

## Built-in usage (alias style)

```python
from mtp.providers import Groq

provider = Groq(model="llama-3.3-70b-versatile")
```

## Built-in usage (explicit style)

```python
from mtp.providers import GroqToolCallingProvider

provider = GroqToolCallingProvider(model="llama-3.3-70b-versatile")
```

## Add a new provider

## 1) Create provider file

Example: `src/mtp/providers/anthropic_provider.py`

```python
from mtp.agent import AgentAction, ProviderAdapter

class AnthropicToolCallingProvider(ProviderAdapter):
    def next_action(self, messages, tools) -> AgentAction:
        ...

    def finalize(self, messages, tool_results) -> str:
        ...

    async def anext_action(self, messages, tools) -> AgentAction:
        ...

    async def afinalize(self, messages, tool_results) -> str:
        ...
```

## 2) Export provider class

In `src/mtp/providers/__init__.py`:

```python
from .anthropic_provider import AnthropicToolCallingProvider
```

## 3) Use provider directly

```python
from mtp import Agent
from mtp.providers import AnthropicToolCallingProvider

provider = AnthropicToolCallingProvider(model="claude-...")
registry = Agent.ToolRegistry()
agent = Agent.MTPAgent(provider=provider, tools=registry)
```

## Notes

- Alias names available (when matching optional SDKs are installed):
  - `Groq`, `OpenRouter`, `OpenAI`, `Gemini`, `Anthropic`, `SambaNova`
  - `Cerebras`, `DeepSeek`, `Mistral`, `Cohere`, `TogetherAI`, `FireworksAI`
- Local deterministic planner provider is also available as `MockPlannerProvider` (class alias for `SimplePlannerProvider`).
- Provider exports are dependency-optional: missing SDKs no longer block importing other providers.
- Provider symbols are lazily loaded to avoid import-time circular dependencies.
- Explicit class names remain fully supported and unchanged.
- No provider is defaulted by core `Agent` / `MTPAgent`.
- Different providers can expose different constructor parameters safely.
- Async provider hooks are optional. If omitted, async agent APIs fall back to running sync provider methods in threads.

Related:
- [Storage and Sessions](C:\Users\prajw\Downloads\MTP\docs\STORAGE.md)
