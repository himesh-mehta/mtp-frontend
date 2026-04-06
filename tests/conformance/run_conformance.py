from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

from mtp import (  # noqa: E402
    MCPAuthDecision,
    MCPJsonRpcServer,
    MCPPrompt,
    MCPPromptArgument,
    MCPResource,
    ToolRegistry,
    ToolSpec,
)

from tests.conformance.clients import DirectJsonRpcClient, HttpJsonRpcClient  # noqa: E402
from tests.conformance.harness import (  # noqa: E402
    ClientReport,
    make_report,
    write_json_report,
    write_markdown_matrix,
)
from tests.conformance.scenarios import ALL_SCENARIOS, ScenarioContext  # noqa: E402


def _build_registry() -> ToolRegistry:
    reg = ToolRegistry()
    reg.register_tool(ToolSpec(name="calc.add", description="Add two numbers"), lambda a, b: a + b)
    reg.register_tool(ToolSpec(name="ops.fail", description="Always fails"), lambda: 1 / 0)
    return reg


def _build_server(*, support_progress: bool = True, support_cancellation: bool = True) -> MCPJsonRpcServer:
    resources = [
        MCPResource(
            uri="memory://readme",
            name="README",
            description="MCP in-memory readme",
            mime_type="text/markdown",
        )
    ]
    prompts = [
        MCPPrompt(
            name="summarize",
            description="Summarize topic",
            arguments=[MCPPromptArgument(name="topic", required=True)],
            template="Summarize this topic: {topic}",
        )
    ]
    return MCPJsonRpcServer(
        tools=_build_registry(),
        resources=resources,
        resource_reader=lambda uri: "# hello" if uri == "memory://readme" else "",
        prompts=prompts,
        support_progress=support_progress,
        support_cancellation=support_cancellation,
    )


def _build_auth_server() -> MCPJsonRpcServer:
    class _OAuthProvider:
        def authorize(self, token: str | None, request: dict[str, Any], context: Any) -> MCPAuthDecision:
            _ = request
            _ = context
            if token == "ok-token":
                return MCPAuthDecision(allowed=True)
            return MCPAuthDecision(
                allowed=False,
                message="Missing OAuth bearer token",
                www_authenticate='Bearer realm="mtp", error="invalid_token"',
            )

    return MCPJsonRpcServer(
        tools=_build_registry(),
        auth_provider=_OAuthProvider(),
    )


def _make_clients(profile: str, server_feature_set: str) -> tuple[list[Any], list[Any]]:
    support_progress = True
    support_cancellation = True
    if server_feature_set == "core":
        support_progress = False
        support_cancellation = False
    server = _build_server(support_progress=support_progress, support_cancellation=support_cancellation)
    auth_server = _build_auth_server()

    closers: list[Any] = []
    clients: list[Any] = []

    if profile in {"all", "direct"}:
        clients.append(DirectJsonRpcClient(server=server, auth_server=auth_server))
    if profile in {"all", "http"}:
        http_client = HttpJsonRpcClient(server=server, auth_server=auth_server)
        clients.append(http_client)
        closers.append(http_client)
    return clients, closers


def run_suite(*, profile: str, server_feature_set: str) -> list[ClientReport]:
    clients, closers = _make_clients(profile, server_feature_set)
    reports: list[ClientReport] = []
    try:
        for client in clients:
            client_report = ClientReport(
                client_id=client.client_id,
                client_name=client.client_name,
                client_version=client.client_version,
                transport=client.transport,
                server_feature_set=server_feature_set,
            )
            ctx = ScenarioContext(client=client)
            for scenario in ALL_SCENARIOS:
                result = scenario(ctx)
                client_report.scenarios.append(result)
            reports.append(client_report)
    finally:
        for closer in closers:
            close_fn = getattr(closer, "close", None)
            if callable(close_fn):
                close_fn()
    return reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run MCP conformance automation suite.")
    parser.add_argument("--profile", default="all", choices=["all", "direct", "http"], help="Client profile")
    parser.add_argument(
        "--server-feature-set",
        default="resumable",
        choices=["core", "resumable"],
        help="Server feature set under test",
    )
    parser.add_argument("--report-json", default="tmp/conformance/report.json", help="Output path for JSON report")
    parser.add_argument(
        "--matrix-doc",
        default="docs/MCP_COMPATIBILITY_MATRIX.md",
        help="Output path for Markdown matrix report",
    )
    parser.add_argument("--fail-on-critical", action="store_true", help="Exit non-zero on critical failures")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    reports = run_suite(profile=args.profile, server_feature_set=args.server_feature_set)
    report = make_report(profile=args.profile, server_feature_set=args.server_feature_set, clients=reports)

    write_json_report(report, Path(args.report_json))
    write_markdown_matrix(report, Path(args.matrix_doc))

    print(f"Wrote JSON report: {args.report_json}")
    print(f"Wrote matrix doc: {args.matrix_doc}")

    for client in report.clients:
        failed = [scenario for scenario in client.scenarios if not scenario.passed]
        print(
            f"{client.client_name} ({client.transport}) => "
            f"{len(client.scenarios) - len(failed)}/{len(client.scenarios)} passed"
        )
        for item in failed:
            print(f"  - FAIL {item.scenario_id} [{item.severity}] tag={item.triage_tag}: {item.details}")

    if args.fail_on_critical and report.has_critical_failure():
        print("Critical MCP compatibility failure detected.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
