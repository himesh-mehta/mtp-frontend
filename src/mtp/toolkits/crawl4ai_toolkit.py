from __future__ import annotations

from typing import Any

from ..protocol import ToolRiskLevel, ToolSpec
from ..runtime import RegisteredTool, ToolkitLoader
from .common import allow_ref


class Crawl4aiToolkit(ToolkitLoader):
    def __init__(
        self,
        *,
        default_max_length: int = 1000,
        timeout_seconds: int = 60,
        headless: bool = True,
        wait_until: str = "domcontentloaded",
        use_pruning: bool = False,
        pruning_threshold: float = 0.48,
        bm25_threshold: float = 1.0,
        proxy_config: dict[str, Any] | None = None,
    ) -> None:
        self.default_max_length = default_max_length
        self.timeout_seconds = timeout_seconds
        self.headless = headless
        self.wait_until = wait_until
        self.use_pruning = use_pruning
        self.pruning_threshold = pruning_threshold
        self.bm25_threshold = bm25_threshold
        self.proxy_config = proxy_config or {}

    def _build_run_config(self, search_query: str | None) -> dict[str, Any]:
        config: dict[str, Any] = {
            "page_timeout": self.timeout_seconds * 1000,
            "wait_until": self.wait_until,
            "cache_mode": "bypass",
            "verbose": False,
        }

        if self.use_pruning or search_query:
            try:
                from crawl4ai.content_filter_strategy import BM25ContentFilter, PruningContentFilter
                from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
            except ImportError:
                return config

            if search_query:
                content_filter = BM25ContentFilter(user_query=search_query, bm25_threshold=self.bm25_threshold)
            else:
                content_filter = PruningContentFilter(
                    threshold=self.pruning_threshold,
                    threshold_type="fixed",
                    min_word_threshold=2,
                )
            config["markdown_generator"] = DefaultMarkdownGenerator(content_filter=content_filter)
        return config

    async def _crawl_url(self, url: str, search_query: str | None, max_length: int) -> str:
        try:
            from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
        except ImportError as exc:
            raise ImportError("Crawl4aiToolkit requires `crawl4ai`. Install with: pip install crawl4ai") from exc

        browser_config = BrowserConfig(headless=self.headless, verbose=False, **self.proxy_config)
        async with AsyncWebCrawler(config=browser_config) as crawler:
            config = CrawlerRunConfig(**self._build_run_config(search_query))
            result = await crawler.arun(url=url, config=config)

            if not result:
                return ""

            content = ""
            if hasattr(result, "fit_markdown") and result.fit_markdown:
                content = str(result.fit_markdown)
            elif hasattr(result, "markdown") and result.markdown:
                if hasattr(result.markdown, "raw_markdown"):
                    content = str(result.markdown.raw_markdown)
                else:
                    content = str(result.markdown)
            elif hasattr(result, "text") and result.text:
                content = str(result.text)

            if max_length > 0 and len(content) > max_length:
                content = content[:max_length]
            return content

    def list_tool_specs(self) -> list[ToolSpec]:
        return [
            ToolSpec(
                name="crawl4ai.web_crawler",
                description="Crawl a webpage with crawl4ai and return extracted text.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "url": allow_ref({"type": "string"}),
                        "search_query": allow_ref({"type": "string"}),
                        "max_length": allow_ref({"type": "integer"}),
                    },
                    "required": ["url"],
                    "additionalProperties": False,
                },
                risk_level=ToolRiskLevel.READ_ONLY,
            )
        ]

    def load_tools(self) -> list[RegisteredTool]:
        async def web_crawler(
            url: str,
            search_query: str | None = None,
            max_length: int | None = None,
        ) -> str:
            resolved_max_length = self.default_max_length if max_length is None else max_length
            return await self._crawl_url(url=url, search_query=search_query, max_length=resolved_max_length)

        return [RegisteredTool(spec=self.list_tool_specs()[0], handler=web_crawler)]
