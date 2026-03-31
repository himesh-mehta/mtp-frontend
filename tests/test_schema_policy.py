from __future__ import annotations

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp.policy import PolicyDecision, RiskPolicy
from mtp.protocol import ExecutionPlan, ToolBatch, ToolCall, ToolRiskLevel, ToolSpec
from mtp.schema import MessageEnvelope, PlanValidationError, validate_execution_plan


class SchemaPolicyTests(unittest.TestCase):
    def test_envelope_to_dict(self) -> None:
        envelope = MessageEnvelope.create(
            kind="tool_plan",
            payload={"ok": True},
            metadata={"trace_id": "abc"},
        )
        data = envelope.to_dict()
        self.assertEqual(data["kind"], "tool_plan")
        self.assertEqual(data["payload"]["ok"], True)
        self.assertEqual(data["metadata"]["trace_id"], "abc")

    def test_validate_execution_plan_cycle(self) -> None:
        plan = ExecutionPlan(
            batches=[
                ToolBatch(
                    mode="parallel",
                    calls=[
                        ToolCall(id="a", name="x", depends_on=["b"]),
                        ToolCall(id="b", name="y", depends_on=["a"]),
                    ],
                )
            ]
        )
        with self.assertRaises(PlanValidationError):
            validate_execution_plan(plan)

    def test_validate_execution_plan_missing_dep(self) -> None:
        plan = ExecutionPlan(
            batches=[
                ToolBatch(
                    mode="sequential",
                    calls=[ToolCall(id="a", name="x", depends_on=["z"])],
                )
            ]
        )
        with self.assertRaises(PlanValidationError):
            validate_execution_plan(plan)

    def test_risk_policy_override(self) -> None:
        policy = RiskPolicy(
            by_tool_name={"danger.delete": PolicyDecision.DENY},
        )
        spec = ToolSpec(
            name="danger.delete",
            description="delete",
            risk_level=ToolRiskLevel.DESTRUCTIVE,
        )
        decision = policy.decide(spec, ToolCall(id="1", name=spec.name), {})
        self.assertEqual(decision, PolicyDecision.DENY)


if __name__ == "__main__":
    unittest.main()
