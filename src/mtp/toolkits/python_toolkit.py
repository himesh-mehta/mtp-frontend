from __future__ import annotations

from pathlib import Path
from typing import Any

from ..protocol import ToolRiskLevel, ToolSpec
from ..runtime import RegisteredTool, ToolkitLoader
from .common import allow_ref


class PythonToolkit(ToolkitLoader):
    def __init__(self, base_dir: str | Path | None = None) -> None:
        self.base_dir = Path(base_dir or Path.cwd()).resolve()

    def _safe_builtins(self) -> dict[str, Any]:
        return {
            "abs": abs,
            "bool": bool,
            "dict": dict,
            "float": float,
            "int": int,
            "len": len,
            "list": list,
            "max": max,
            "min": min,
            "print": print,
            "range": range,
            "set": set,
            "sorted": sorted,
            "str": str,
            "sum": sum,
            "tuple": tuple,
        }

    def _resolve(self, path: str) -> Path:
        candidate = (self.base_dir / path).resolve()
        if self.base_dir not in candidate.parents and candidate != self.base_dir:
            raise ValueError("Path escapes base_dir.")
        return candidate

    def list_tool_specs(self) -> list[ToolSpec]:
        return [
            ToolSpec(
                name="python.run_code",
                description="Run Python code in a constrained execution context.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "code": allow_ref({"type": "string"}),
                        "return_variable": allow_ref({"type": "string"}),
                    },
                    "required": ["code"],
                    "additionalProperties": False,
                },
                risk_level=ToolRiskLevel.WRITE,
            ),
            ToolSpec(
                name="python.run_file",
                description="Run a Python file from base_dir and optionally return a variable.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": allow_ref({"type": "string"}),
                        "return_variable": allow_ref({"type": "string"}),
                    },
                    "required": ["path"],
                    "additionalProperties": False,
                },
                risk_level=ToolRiskLevel.WRITE,
            ),
        ]

    def load_tools(self) -> list[RegisteredTool]:
        def run_code(code: str, return_variable: str = "result") -> Any:
            globals_ctx = {"__builtins__": self._safe_builtins()}
            locals_ctx: dict[str, Any] = {}
            exec(code, globals_ctx, locals_ctx)
            return locals_ctx.get(return_variable)

        def run_file(path: str, return_variable: str = "result") -> Any:
            target = self._resolve(path)
            code = target.read_text(encoding="utf-8")
            return run_code(code=code, return_variable=return_variable)

        handlers = {
            "python.run_code": run_code,
            "python.run_file": run_file,
        }
        specs = {spec.name: spec for spec in self.list_tool_specs()}
        return [RegisteredTool(spec=specs[name], handler=handler) for name, handler in handlers.items()]
