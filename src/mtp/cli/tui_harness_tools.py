from __future__ import annotations

import ast
import fnmatch
import os
from pathlib import Path
import subprocess
from typing import Any

from mtp.protocol import ToolRiskLevel, ToolSpec
from mtp.runtime import RegisteredTool, ToolkitLoader


_TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".md", ".txt", ".toml", ".yaml", ".yml",
    ".css", ".html", ".sql", ".rs", ".go", ".java", ".c", ".cpp", ".h", ".hpp", ".sh",
    ".ps1", ".bat", ".ini", ".cfg",
}
_DEFAULT_IGNORES = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", "dist", "build",
    ".mypy_cache", ".ruff_cache", ".next", ".turbo",
}


def _schema(properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": required or [],
        "additionalProperties": False,
    }


class _Workspace:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()

    def resolve(self, path: str = ".") -> Path:
        target = (self.root / path).resolve(strict=False)
        base = os.path.normcase(str(self.root))
        normalized = os.path.normcase(str(target))
        if os.path.commonpath([base, normalized]) != base:
            raise ValueError("Path escapes workspace.")
        return target

    def rel(self, path: Path) -> str:
        return str(path.resolve(strict=False).relative_to(self.root)).replace("\\", "/")

    def is_ignored(self, path: Path) -> bool:
        return any(part in _DEFAULT_IGNORES for part in path.parts)

    def text_files(self, path: str = ".") -> list[Path]:
        start = self.resolve(path)
        if start.is_file():
            return [start]
        files: list[Path] = []
        for item in start.rglob("*"):
            if item.is_file() and not self.is_ignored(item) and item.suffix.lower() in _TEXT_EXTENSIONS:
                files.append(item)
        return files


class ContextToolkit(ToolkitLoader):
    def __init__(self, root: str | Path) -> None:
        self.ws = _Workspace(root)

    def list_tool_specs(self) -> list[ToolSpec]:
        return [
            ToolSpec("project.inspect", "Summarize project files, languages, git state, and dependency manifests.", _schema({}), risk_level=ToolRiskLevel.READ_ONLY),
            ToolSpec("fs.glob", "Find files by glob pattern under the workspace.", _schema({"pattern": {"type": "string"}, "limit": {"type": "integer"}}, ["pattern"]), risk_level=ToolRiskLevel.READ_ONLY),
            ToolSpec("fs.read_text", "Read a text file with secret-file guardrails.", _schema({"path": {"type": "string"}, "max_chars": {"type": "integer"}}, ["path"]), risk_level=ToolRiskLevel.READ_ONLY),
            ToolSpec("fs.search", "Search text files for a literal or regex pattern.", _schema({"query": {"type": "string"}, "path": {"type": "string"}, "regex": {"type": "boolean"}, "limit": {"type": "integer"}}, ["query"]), risk_level=ToolRiskLevel.READ_ONLY),
            ToolSpec("agent.explore_codebase", "Subagent-style deep codebase search. Use for broad grep and locating relevant files.", _schema({"task": {"type": "string"}, "query": {"type": "string"}, "limit": {"type": "integer"}}, ["task"]), risk_level=ToolRiskLevel.READ_ONLY),
            ToolSpec("agent.debug_context", "Subagent-style debug context gatherer: project summary, git diff, and likely files.", _schema({"symptom": {"type": "string"}, "query": {"type": "string"}}, ["symptom"]), risk_level=ToolRiskLevel.READ_ONLY),
        ]

    def load_tools(self) -> list[RegisteredTool]:
        specs = {spec.name: spec for spec in self.list_tool_specs()}

        def project_inspect() -> dict[str, Any]:
            files = [p for p in self.ws.root.iterdir() if not self.ws.is_ignored(p)]
            manifests = [name for name in ("pyproject.toml", "package.json", "Cargo.toml", "go.mod", "requirements.txt", "README.md", "AGENTS.md") if (self.ws.root / name).exists()]
            extensions: dict[str, int] = {}
            for item in self.ws.text_files(".")[:2000]:
                extensions[item.suffix.lower() or "(none)"] = extensions.get(item.suffix.lower() or "(none)", 0) + 1
            git = _run(["git", "status", "--short"], self.ws.root, timeout=8)
            return {
                "root": str(self.ws.root),
                "top_level": [p.name + ("/" if p.is_dir() else "") for p in files[:80]],
                "manifests": manifests,
                "extensions": dict(sorted(extensions.items(), key=lambda kv: (-kv[1], kv[0]))[:20]),
                "git_status": git.get("stdout", "")[:4000],
            }

        def fs_glob(pattern: str, limit: int = 200) -> list[str]:
            matches = []
            for item in self.ws.root.rglob(pattern):
                if len(matches) >= max(1, limit):
                    break
                if self.ws.is_ignored(item):
                    continue
                matches.append(self.ws.rel(item) + ("/" if item.is_dir() else ""))
            return matches

        def fs_read_text(path: str, max_chars: int = 20000) -> str:
            target = self.ws.resolve(path)
            rel = self.ws.rel(target)
            if _looks_secret(rel):
                raise ValueError("Reading secret-like files is blocked by the TUI harness.")
            data = target.read_text(encoding="utf-8", errors="replace")
            return data[: max(1000, int(max_chars))]

        def fs_search(query: str, path: str = ".", regex: bool = False, limit: int = 80) -> list[dict[str, Any]]:
            import re

            hits: list[dict[str, Any]] = []
            rx = re.compile(query) if regex else None
            for file in self.ws.text_files(path):
                if _looks_secret(self.ws.rel(file)):
                    continue
                try:
                    lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
                except Exception:
                    continue
                for line_no, line in enumerate(lines, start=1):
                    matched = bool(rx.search(line)) if rx else query.lower() in line.lower()
                    if matched:
                        hits.append({"file": self.ws.rel(file), "line": line_no, "text": line[:300]})
                        if len(hits) >= max(1, limit):
                            return hits
            return hits

        def explore_codebase(task: str, query: str = "", limit: int = 120) -> dict[str, Any]:
            probe = query or _keywords(task)
            return {"task": task, "query": probe, "hits": fs_search(probe, regex=False, limit=limit), "project": project_inspect()}

        def debug_context(symptom: str, query: str = "") -> dict[str, Any]:
            probe = query or _keywords(symptom)
            diff = _run(["git", "diff", "--", "."], self.ws.root, timeout=8).get("stdout", "")
            return {"symptom": symptom, "project": project_inspect(), "hits": fs_search(probe, limit=80), "git_diff": diff[:12000]}

        handlers = {
            "project.inspect": project_inspect,
            "fs.glob": fs_glob,
            "fs.read_text": fs_read_text,
            "fs.search": fs_search,
            "agent.explore_codebase": explore_codebase,
            "agent.debug_context": debug_context,
        }
        return [RegisteredTool(spec=specs[name], handler=handler) for name, handler in handlers.items()]


class EditToolkit(ToolkitLoader):
    def __init__(self, root: str | Path) -> None:
        self.ws = _Workspace(root)

    def list_tool_specs(self) -> list[ToolSpec]:
        return [
            ToolSpec("edit.apply_patch", "Main-agent edit tool. Replace an exact old_text block with new_text and return a diff.", _schema({"path": {"type": "string"}, "old_text": {"type": "string"}, "new_text": {"type": "string"}, "replace_all": {"type": "boolean"}}, ["path", "old_text", "new_text"]), risk_level=ToolRiskLevel.WRITE),
            ToolSpec("edit.create_file", "Create a new text file if it does not already exist.", _schema({"path": {"type": "string"}, "content": {"type": "string"}}, ["path", "content"]), risk_level=ToolRiskLevel.WRITE),
        ]

    def load_tools(self) -> list[RegisteredTool]:
        import difflib

        specs = {spec.name: spec for spec in self.list_tool_specs()}

        def apply_patch(path: str, old_text: str, new_text: str, replace_all: bool = False) -> dict[str, Any]:
            target = self.ws.resolve(path)
            before = target.read_text(encoding="utf-8", errors="replace")
            count = before.count(old_text)
            if count == 0:
                raise ValueError("old_text was not found exactly. Re-read the file and try a smaller exact block.")
            if count > 1 and not replace_all:
                raise ValueError(f"old_text appears {count} times. Set replace_all=true or choose a more specific block.")
            after = before.replace(old_text, new_text) if replace_all else before.replace(old_text, new_text, 1)
            target.write_text(after, encoding="utf-8")
            diff = "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile=f"a/{path}", tofile=f"b/{path}"))
            return {"file": self.ws.rel(target), "replacements": count if replace_all else 1, "diff": diff[:20000]}

        def create_file(path: str, content: str) -> dict[str, Any]:
            target = self.ws.resolve(path)
            if target.exists():
                raise ValueError("Refusing to overwrite existing file.")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return {"file": self.ws.rel(target), "bytes": len(content.encode("utf-8"))}

        return [
            RegisteredTool(spec=specs["edit.apply_patch"], handler=apply_patch),
            RegisteredTool(spec=specs["edit.create_file"], handler=create_file),
        ]


class CommandToolkit(ToolkitLoader):
    def __init__(self, root: str | Path) -> None:
        self.ws = _Workspace(root)

    def list_tool_specs(self) -> list[ToolSpec]:
        return [
            ToolSpec("shell.run", "Run a workspace command through the harness permission layer.", _schema({"command": {"type": "string"}, "timeout_seconds": {"type": "integer"}}, ["command"]), risk_level=ToolRiskLevel.WRITE),
            ToolSpec("git.status", "Return concise git status.", _schema({}), risk_level=ToolRiskLevel.READ_ONLY),
            ToolSpec("git.diff", "Return git diff for the workspace or one path.", _schema({"path": {"type": "string"}, "max_chars": {"type": "integer"}}), risk_level=ToolRiskLevel.READ_ONLY),
            ToolSpec("test.run", "Run a targeted test command after edits.", _schema({"command": {"type": "string"}, "timeout_seconds": {"type": "integer"}}, ["command"]), risk_level=ToolRiskLevel.WRITE),
            ToolSpec("agent.syntax_check", "Subagent-style syntax/lint check for Python files without editing.", _schema({"path": {"type": "string"}}), risk_level=ToolRiskLevel.READ_ONLY),
        ]

    def load_tools(self) -> list[RegisteredTool]:
        specs = {spec.name: spec for spec in self.list_tool_specs()}

        def shell_run(command: str, timeout_seconds: int = 60) -> dict[str, Any]:
            return _run_shell(command, self.ws.root, timeout_seconds)

        def git_status() -> dict[str, Any]:
            return _run(["git", "status", "--short", "--branch"], self.ws.root, timeout=10)

        def git_diff(path: str = ".", max_chars: int = 20000) -> str:
            cmd = ["git", "diff", "--", path]
            return _run(cmd, self.ws.root, timeout=10).get("stdout", "")[: max(1000, int(max_chars))]

        def test_run(command: str, timeout_seconds: int = 120) -> dict[str, Any]:
            compact = " ".join(command.split())
            allowed = ("pytest", "python -m pytest", "npm test", "npm run test", "python -m compileall", "python -m py_compile")
            if not compact.startswith(allowed):
                raise ValueError(f"Use a targeted test command. Allowed prefixes: {', '.join(allowed)}")
            return _run_shell(command, self.ws.root, timeout_seconds)

        def syntax_check(path: str = ".") -> dict[str, Any]:
            target = self.ws.resolve(path)
            files = [target] if target.is_file() else [p for p in self.ws.text_files(path) if p.suffix == ".py"]
            errors = []
            for file in files[:300]:
                try:
                    ast.parse(file.read_text(encoding="utf-8", errors="replace"), filename=str(file))
                except SyntaxError as exc:
                    errors.append({"file": self.ws.rel(file), "line": exc.lineno, "message": exc.msg})
            return {"checked": len(files[:300]), "errors": errors}

        handlers = {
            "shell.run": shell_run,
            "git.status": git_status,
            "git.diff": git_diff,
            "test.run": test_run,
            "agent.syntax_check": syntax_check,
        }
        return [RegisteredTool(spec=specs[name], handler=handler) for name, handler in handlers.items()]


def register_harness_toolkits(registry: Any, *, root: str | Path) -> None:
    registry.register_toolkit_loader("project", ContextToolkit(root))
    registry.register_toolkit_loader("fs", ContextToolkit(root))
    registry.register_toolkit_loader("agent", ContextToolkit(root))
    registry.register_toolkit_loader("edit", EditToolkit(root))
    registry.register_toolkit_loader("shell", CommandToolkit(root))
    registry.register_toolkit_loader("git", CommandToolkit(root))
    registry.register_toolkit_loader("test", CommandToolkit(root))


def _looks_secret(path: str) -> bool:
    name = Path(path).name.lower()
    return name == ".env" or fnmatch.fnmatch(name, "*.env") or fnmatch.fnmatch(name, "*.env.*")


def _keywords(text: str) -> str:
    words = [w.strip(".,:;()[]{}\"'`").lower() for w in text.split()]
    useful = [w for w in words if len(w) >= 4 and w not in {"that", "this", "with", "from", "when", "where", "there"}]
    return useful[0] if useful else text[:40]


def _run(cmd: list[str], cwd: Path, timeout: int) -> dict[str, Any]:
    try:
        completed = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        return {"returncode": completed.returncode, "stdout": completed.stdout.strip(), "stderr": completed.stderr.strip()}
    except Exception as exc:
        return {"returncode": 1, "stdout": "", "stderr": str(exc)}


def _run_shell(command: str, cwd: Path, timeout: int) -> dict[str, Any]:
    completed = subprocess.run(command, shell=True, cwd=str(cwd), capture_output=True, text=True, timeout=max(1, int(timeout)))
    return {"returncode": completed.returncode, "stdout": completed.stdout.strip()[:30000], "stderr": completed.stderr.strip()[:12000]}

