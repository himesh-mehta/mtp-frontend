from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


TRIAGE_PROTOCOL = "protocol_mismatch"
TRIAGE_TRANSPORT = "transport_mismatch"
TRIAGE_AUTH = "auth_mismatch"

SEVERITY_CRITICAL = "critical"
SEVERITY_MAJOR = "major"
SEVERITY_MINOR = "minor"


@dataclass(slots=True)
class ScenarioResult:
    scenario_id: str
    title: str
    passed: bool
    severity: str
    triage_tag: str | None = None
    details: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ClientReport:
    client_id: str
    client_name: str
    client_version: str
    transport: str
    server_feature_set: str
    scenarios: list[ScenarioResult] = field(default_factory=list)

    @property
    def has_critical_failure(self) -> bool:
        return any((not item.passed) and item.severity == SEVERITY_CRITICAL for item in self.scenarios)


@dataclass(slots=True)
class ConformanceReport:
    generated_at: str
    profile: str
    server_feature_set: str
    clients: list[ClientReport]

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "profile": self.profile,
            "server_feature_set": self.server_feature_set,
            "clients": [
                {
                    "client_id": client.client_id,
                    "client_name": client.client_name,
                    "client_version": client.client_version,
                    "transport": client.transport,
                    "server_feature_set": client.server_feature_set,
                    "has_critical_failure": client.has_critical_failure,
                    "scenarios": [asdict(item) for item in client.scenarios],
                }
                for client in self.clients
            ],
        }

    def has_critical_failure(self) -> bool:
        return any(client.has_critical_failure for client in self.clients)


def classify_failure(*, scenario_id: str, detail: str) -> str:
    lowered = f"{scenario_id} {detail}".lower()
    if "auth" in lowered or "token" in lowered or "www-authenticate" in lowered:
        return TRIAGE_AUTH
    if "http" in lowered or "ws" in lowered or "transport" in lowered or "connection" in lowered:
        return TRIAGE_TRANSPORT
    return TRIAGE_PROTOCOL


def make_report(*, profile: str, server_feature_set: str, clients: list[ClientReport]) -> ConformanceReport:
    return ConformanceReport(
        generated_at=datetime.now(UTC).isoformat(),
        profile=profile,
        server_feature_set=server_feature_set,
        clients=clients,
    )


def write_json_report(report: ConformanceReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


def render_markdown_matrix(report: ConformanceReport) -> str:
    lines: list[str] = []
    lines.append("# MCP Compatibility Matrix")
    lines.append("")
    lines.append(f"- Generated: `{report.generated_at}`")
    lines.append(f"- Profile: `{report.profile}`")
    lines.append(f"- Server feature set: `{report.server_feature_set}`")
    lines.append("")
    lines.append("| Client | Version | Transport | Scenario | Result | Severity | Triage |")
    lines.append("|---|---|---|---|---|---|---|")
    for client in report.clients:
        for scenario in client.scenarios:
            result = "PASS" if scenario.passed else "FAIL"
            triage = scenario.triage_tag or "-"
            lines.append(
                "| "
                + " | ".join(
                    [
                        client.client_name,
                        client.client_version,
                        client.transport,
                        scenario.scenario_id,
                        result,
                        scenario.severity,
                        triage,
                    ]
                )
                + " |"
            )
    lines.append("")
    return "\n".join(lines).strip() + "\n"


def write_markdown_matrix(report: ConformanceReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_matrix(report), encoding="utf-8")

