from __future__ import annotations

import inspect
import pathlib
import sys
import unittest
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent, ToolRegistry
import mtp.providers as providers
from mtp.agent import AgentAction
from mtp.media import Image
from mtp.providers.common import (
    ProviderCapabilities,
    STRUCTURED_OUTPUT_CLIENT_VALIDATED,
    STRUCTURED_OUTPUT_NATIVE_JSON_OBJECT,
    STRUCTURED_OUTPUT_NATIVE_JSON_SCHEMA,
    STRUCTURED_OUTPUT_NONE,
    USAGE_METRICS_BASIC,
    USAGE_METRICS_NONE,
    USAGE_METRICS_RICH,
    capabilities_from_any,
)


_STRUCTURED_LEVELS = {
    STRUCTURED_OUTPUT_NONE,
    STRUCTURED_OUTPUT_CLIENT_VALIDATED,
    STRUCTURED_OUTPUT_NATIVE_JSON_OBJECT,
    STRUCTURED_OUTPUT_NATIVE_JSON_SCHEMA,
}

_USAGE_LEVELS = {
    USAGE_METRICS_NONE,
    USAGE_METRICS_BASIC,
    USAGE_METRICS_RICH,
}


class _DummyClient:
    pass


class _NoStreamProvider:
    def next_action(self, messages: list[dict[str, Any]], tools: list[Any]) -> AgentAction:
        return AgentAction(response_text="hello")

    def finalize(self, messages: list[dict[str, Any]], tool_results: list[Any]) -> str:
        return "done"

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            provider="no_stream",
            supports_tool_calling=False,
            supports_parallel_tool_calls=False,
            input_modalities=["text"],
            supports_tool_media_output=False,
            supports_finalize_streaming=False,
            usage_metrics_quality=USAGE_METRICS_NONE,
            supports_reasoning_metadata=False,
            structured_output_support=STRUCTURED_OUTPUT_NONE,
            supports_native_async=False,
            allow_finalize_stream_fallback=False,
        )


class ProviderCapabilitiesTests(unittest.TestCase):
    def _iter_provider_classes(self) -> list[type]:
        classes: list[type] = []
        for name in providers.__all__:
            if not (name.endswith("ToolCallingProvider") or name == "MockPlannerProvider"):
                continue
            try:
                obj = getattr(providers, name)
            except Exception:
                continue
            if inspect.isclass(obj):
                classes.append(obj)
        unique: dict[str, type] = {cls.__name__: cls for cls in classes}
        return list(unique.values())

    def _build_provider(self, cls: type) -> Any:
        signature = inspect.signature(cls)
        kwargs: dict[str, Any] = {}
        if "client" in signature.parameters:
            kwargs["client"] = _DummyClient()
        return cls(**kwargs)

    def test_provider_classes_expose_capabilities(self) -> None:
        classes = self._iter_provider_classes()
        self.assertTrue(classes, "No provider classes found for capability checks.")
        for cls in classes:
            provider = self._build_provider(cls)
            self.assertTrue(callable(getattr(provider, "capabilities", None)), f"{cls.__name__} missing capabilities()")
            caps = capabilities_from_any(provider.capabilities())
            self.assertIsInstance(caps, ProviderCapabilities, f"{cls.__name__} returned invalid capabilities payload")
            assert caps is not None
            self.assertIn("text", caps.input_modalities, f"{cls.__name__} must include 'text' input modality")
            self.assertIn(caps.structured_output_support, _STRUCTURED_LEVELS)
            self.assertIn(caps.usage_metrics_quality, _USAGE_LEVELS)
            self.assertEqual(caps.provider, caps.provider.strip())

            if caps.supports_finalize_streaming:
                self.assertTrue(callable(getattr(provider, "finalize_stream", None)))
            if caps.supports_parallel_tool_calls:
                self.assertTrue(caps.supports_tool_calling)

    def test_media_guardrail_fails_fast_for_unsupported_modality(self) -> None:
        provider = providers.MockPlannerProvider()
        registry = ToolRegistry()
        agent = Agent(provider=provider, tools=registry)
        with self.assertRaisesRegex(ValueError, "does not support requested input modalities"):
            agent.run_loop("hello", max_rounds=1, images=[Image(url="https://example.com/image.png")])

    def test_stream_guardrail_can_fail_fast_when_fallback_disabled(self) -> None:
        registry = ToolRegistry()
        agent = Agent(
            provider=_NoStreamProvider(),  # type: ignore[arg-type]
            tools=registry,
            allow_stream_fallback=False,
        )
        with self.assertRaisesRegex(ValueError, "does not support native finalize streaming"):
            list(agent.run_loop_stream("hello", max_rounds=1))

    def test_stream_guardrail_degrades_safely_when_fallback_enabled(self) -> None:
        provider = providers.MockPlannerProvider()
        registry = ToolRegistry()
        agent = Agent(
            provider=provider,
            tools=registry,
            allow_stream_fallback=True,
        )
        chunks = list(agent.run_loop_stream("hello", max_rounds=1))
        self.assertTrue(chunks)


if __name__ == "__main__":
    unittest.main()

