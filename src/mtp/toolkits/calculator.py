from __future__ import annotations

import math

from ..protocol import ToolRiskLevel, ToolSpec
from ..runtime import RegisteredTool, ToolkitLoader
from .common import allow_ref


class CalculatorToolkit(ToolkitLoader):
    def list_tool_specs(self) -> list[ToolSpec]:
        return [
            ToolSpec(
                name="calculator.add",
                description="Add two numbers.",
                input_schema={
                    "type": "object",
                    "properties": {"a": allow_ref({"type": "number"}), "b": allow_ref({"type": "number"})},
                    "required": ["a", "b"],
                    "additionalProperties": False,
                },
                risk_level=ToolRiskLevel.READ_ONLY,
            ),
            ToolSpec(
                name="calculator.subtract",
                description="Subtract b from a.",
                input_schema={
                    "type": "object",
                    "properties": {"a": allow_ref({"type": "number"}), "b": allow_ref({"type": "number"})},
                    "required": ["a", "b"],
                    "additionalProperties": False,
                },
                risk_level=ToolRiskLevel.READ_ONLY,
            ),
            ToolSpec(
                name="calculator.multiply",
                description="Multiply two numbers.",
                input_schema={
                    "type": "object",
                    "properties": {"a": allow_ref({"type": "number"}), "b": allow_ref({"type": "number"})},
                    "required": ["a", "b"],
                    "additionalProperties": False,
                },
                risk_level=ToolRiskLevel.READ_ONLY,
            ),
            ToolSpec(
                name="calculator.divide",
                description="Divide a by b.",
                input_schema={
                    "type": "object",
                    "properties": {"a": allow_ref({"type": "number"}), "b": allow_ref({"type": "number"})},
                    "required": ["a", "b"],
                    "additionalProperties": False,
                },
                risk_level=ToolRiskLevel.READ_ONLY,
            ),
            ToolSpec(
                name="calculator.sqrt",
                description="Square root of a non-negative number.",
                input_schema={
                    "type": "object",
                    "properties": {"x": allow_ref({"type": "number"})},
                    "required": ["x"],
                    "additionalProperties": False,
                },
                risk_level=ToolRiskLevel.READ_ONLY,
            ),
        ]

    def load_tools(self) -> list[RegisteredTool]:
        def add(a: float, b: float) -> float:
            return a + b

        def subtract(a: float, b: float) -> float:
            return a - b

        def multiply(a: float, b: float) -> float:
            return a * b

        def divide(a: float, b: float) -> float:
            if b == 0:
                raise ValueError("Division by zero.")
            return a / b

        def sqrt(x: float) -> float:
            if x < 0:
                raise ValueError("Square root of negative number.")
            return math.sqrt(x)

        handlers = {
            "calculator.add": add,
            "calculator.subtract": subtract,
            "calculator.multiply": multiply,
            "calculator.divide": divide,
            "calculator.sqrt": sqrt,
        }
        specs = {spec.name: spec for spec in self.list_tool_specs()}
        return [RegisteredTool(spec=specs[name], handler=handler) for name, handler in handlers.items()]
