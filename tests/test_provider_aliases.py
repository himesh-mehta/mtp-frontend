from __future__ import annotations

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp.providers import (  # noqa: E402
    Anthropic,
    AnthropicToolCallingProvider,
    Gemini,
    GeminiToolCallingProvider,
    Groq,
    GroqToolCallingProvider,
    OpenAI,
    OpenAIToolCallingProvider,
    OpenRouter,
    OpenRouterToolCallingProvider,
    SambaNova,
    SambaNovaToolCallingProvider,
)


class ProviderAliasTests(unittest.TestCase):
    def test_aliases_point_to_provider_classes(self) -> None:
        self.assertIs(Groq, GroqToolCallingProvider)
        self.assertIs(OpenRouter, OpenRouterToolCallingProvider)
        self.assertIs(OpenAI, OpenAIToolCallingProvider)
        self.assertIs(Gemini, GeminiToolCallingProvider)
        self.assertIs(Anthropic, AnthropicToolCallingProvider)
        self.assertIs(SambaNova, SambaNovaToolCallingProvider)


if __name__ == "__main__":
    unittest.main()
