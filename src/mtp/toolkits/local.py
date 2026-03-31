from __future__ import annotations

import os
from pathlib import Path

from ..runtime import ToolRegistry
from .calculator import CalculatorToolkit
from .file_toolkit import FileToolkit
from .python_toolkit import PythonToolkit
from .shell_toolkit import ShellToolkit


def register_local_toolkits(
    registry: ToolRegistry,
    *,
    base_dir: str | Path | None = None,
) -> None:
    root = Path(base_dir or os.getcwd()).resolve()
    registry.register_toolkit_loader("calculator", CalculatorToolkit())
    registry.register_toolkit_loader("file", FileToolkit(base_dir=root))
    registry.register_toolkit_loader("python", PythonToolkit(base_dir=root))
    registry.register_toolkit_loader("shell", ShellToolkit(base_dir=root))
