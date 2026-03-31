from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from ..protocol import ToolRiskLevel, ToolSpec
from ..runtime import RegisteredTool, ToolkitLoader
from .common import allow_ref


class ShellToolkit(ToolkitLoader):
    def __init__(self, base_dir: str | Path | None = None, timeout_seconds: int = 20) -> None:
        self.base_dir = Path(base_dir or Path.cwd()).resolve()
        self.timeout_seconds = timeout_seconds

    def list_tool_specs(self) -> list[ToolSpec]:
        return [
            ToolSpec(
                name="shell.run_command",
                description="Run a shell command in base_dir and return stdout/stderr.",
                input_schema={
                    "type": "object",
                    "properties": {"command": allow_ref({"type": "string"})},
                    "required": ["command"],
                    "additionalProperties": False,
                },
                risk_level=ToolRiskLevel.WRITE,
            )
        ]

    def load_tools(self) -> list[RegisteredTool]:
        def run_command(command: str) -> dict[str, Any]:
            completed = subprocess.run(
                command,
                shell=True,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
            return {
                "returncode": completed.returncode,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
            }

        return [
            RegisteredTool(
                spec=self.list_tool_specs()[0],
                handler=run_command,
            )
        ]
