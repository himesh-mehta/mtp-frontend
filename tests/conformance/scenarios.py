from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .harness import (
    SEVERITY_CRITICAL,
    SEVERITY_MAJOR,
    ScenarioResult,
    classify_failure,
)


@dataclass(slots=True)
class ScenarioContext:
    client: Any


def _pass(scenario_id: str, title: str, severity: str, *, details: str = "", evidence: dict[str, Any] | None = None) -> ScenarioResult:
    return ScenarioResult(
        scenario_id=scenario_id,
        title=title,
        passed=True,
        severity=severity,
        details=details,
        evidence=evidence or {},
    )


def _fail(scenario_id: str, title: str, severity: str, *, details: str, evidence: dict[str, Any] | None = None) -> ScenarioResult:
    return ScenarioResult(
        scenario_id=scenario_id,
        title=title,
        passed=False,
        severity=severity,
        triage_tag=classify_failure(scenario_id=scenario_id, detail=details),
        details=details,
        evidence=evidence or {},
    )


def scenario_initialize_lifecycle(ctx: ScenarioContext) -> ScenarioResult:
    scenario_id = "initialize_lifecycle"
    title = "initialize lifecycle"
    try:
        response = ctx.client.initialize()
        if "result" not in response:
            return _fail(scenario_id, title, SEVERITY_CRITICAL, details="initialize missing result", evidence=response)
        caps = response["result"].get("capabilities", {})
        if "tools" not in caps:
            return _fail(scenario_id, title, SEVERITY_CRITICAL, details="initialize capabilities missing tools", evidence=response)
        ctx.client.initialized_notification()
        return _pass(scenario_id, title, SEVERITY_CRITICAL, evidence={"protocolVersion": response["result"].get("protocolVersion")})
    except Exception as exc:  # noqa: BLE001
        return _fail(scenario_id, title, SEVERITY_CRITICAL, details=f"initialize exception: {exc}")


def scenario_tools_list_call(ctx: ScenarioContext) -> ScenarioResult:
    scenario_id = "tools_list_call"
    title = "tools list/call"
    try:
        listed = ctx.client.tools_list()
        tools = listed.get("result", {}).get("tools", [])
        names = [tool.get("name") for tool in tools]
        if "calc.add" not in names:
            return _fail(scenario_id, title, SEVERITY_CRITICAL, details="tools/list missing calc.add", evidence=listed)
        called = ctx.client.tools_call(request_id="call-tools", name="calc.add", arguments={"a": 2, "b": 3})
        result = called.get("result", {}).get("result", {})
        if int(result.get("output", -1)) != 5:
            return _fail(scenario_id, title, SEVERITY_CRITICAL, details="tools/call output mismatch for calc.add", evidence=called)
        return _pass(scenario_id, title, SEVERITY_CRITICAL)
    except Exception as exc:  # noqa: BLE001
        return _fail(scenario_id, title, SEVERITY_CRITICAL, details=f"tools scenario exception: {exc}")


def scenario_resources_prompts(ctx: ScenarioContext) -> ScenarioResult:
    scenario_id = "resources_prompts"
    title = "resources/prompts"
    try:
        resources = ctx.client.resources_list()
        resource_list = resources.get("result", {}).get("resources", [])
        if not resource_list:
            return _fail(scenario_id, title, SEVERITY_MAJOR, details="resources/list returned empty set", evidence=resources)
        uri = resource_list[0].get("uri")
        if not isinstance(uri, str) or not uri:
            return _fail(scenario_id, title, SEVERITY_MAJOR, details="resources/list returned invalid uri", evidence=resources)
        read = ctx.client.resources_read(uri=uri)
        contents = read.get("result", {}).get("contents", [])
        if not contents:
            return _fail(scenario_id, title, SEVERITY_MAJOR, details="resources/read returned no content", evidence=read)

        prompts = ctx.client.prompts_list()
        prompt_list = prompts.get("result", {}).get("prompts", [])
        if not prompt_list:
            return _fail(scenario_id, title, SEVERITY_MAJOR, details="prompts/list returned empty set", evidence=prompts)
        prompt_name = prompt_list[0].get("name")
        got = ctx.client.prompts_get(name=prompt_name, arguments={"topic": "MTP"})
        messages = got.get("result", {}).get("messages", [])
        if not messages:
            return _fail(scenario_id, title, SEVERITY_MAJOR, details="prompts/get returned no messages", evidence=got)
        return _pass(scenario_id, title, SEVERITY_MAJOR)
    except Exception as exc:  # noqa: BLE001
        return _fail(scenario_id, title, SEVERITY_MAJOR, details=f"resources/prompts exception: {exc}")


def scenario_cancellation_progress(ctx: ScenarioContext) -> ScenarioResult:
    scenario_id = "cancellation_progress"
    title = "cancellation/progress"
    try:
        request_id = "cancel-me"
        ctx.client.cancel_request(request_id=request_id)
        cancelled = ctx.client.tools_call(
            request_id=request_id,
            name="calc.add",
            arguments={"a": 1, "b": 2},
            progress_token="tok-cancel",
        )
        error = cancelled.get("error", {})
        if int(error.get("code", 0)) != -32800:
            return _fail(
                scenario_id,
                title,
                SEVERITY_MAJOR,
                details="cancelled call did not return MCP cancel code -32800",
                evidence=cancelled,
            )

        _ = ctx.client.tools_call(
            request_id="progress-me",
            name="calc.add",
            arguments={"a": 3, "b": 4},
            progress_token="tok-progress",
        )
        events = list(ctx.client.progress_events())
        if not any(event.get("progressToken") == "tok-progress" for event in events):
            return _fail(
                scenario_id,
                title,
                SEVERITY_MAJOR,
                details="missing progress event for progress token tok-progress",
                evidence={"events": events[-20:]},
            )
        return _pass(scenario_id, title, SEVERITY_MAJOR)
    except Exception as exc:  # noqa: BLE001
        return _fail(scenario_id, title, SEVERITY_MAJOR, details=f"cancellation/progress exception: {exc}")


def scenario_auth_challenge(ctx: ScenarioContext) -> ScenarioResult:
    scenario_id = "auth_challenge"
    title = "auth challenge behavior"
    try:
        status, denied, headers = ctx.client.auth_initialize(token=None)
        if status != 200 or "error" not in denied:
            return _fail(scenario_id, title, SEVERITY_CRITICAL, details="auth deny path missing JSON-RPC error", evidence=denied)
        denied_data = denied.get("error", {}).get("data", {})
        header_value = headers.get("WWW-Authenticate") or denied_data.get("www_authenticate")
        if not header_value:
            return _fail(
                scenario_id,
                title,
                SEVERITY_CRITICAL,
                details="auth deny path missing WWW-Authenticate challenge",
                evidence={"headers": headers, "response": denied},
            )

        _status_ok, allowed, _headers_ok = ctx.client.auth_initialize(token="ok-token")
        if "result" not in allowed:
            return _fail(scenario_id, title, SEVERITY_CRITICAL, details="auth allow path failed for valid token", evidence=allowed)
        return _pass(scenario_id, title, SEVERITY_CRITICAL)
    except Exception as exc:  # noqa: BLE001
        return _fail(scenario_id, title, SEVERITY_CRITICAL, details=f"auth scenario exception: {exc}")


ALL_SCENARIOS = [
    scenario_initialize_lifecycle,
    scenario_tools_list_call,
    scenario_resources_prompts,
    scenario_cancellation_progress,
    scenario_auth_challenge,
]

