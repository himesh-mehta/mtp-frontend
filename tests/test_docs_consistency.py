from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_FILES = [REPO_ROOT / "README.md", *sorted((REPO_ROOT / "docs").glob("*.md"))]
PROVIDERS_INIT = REPO_ROOT / "src" / "mtp" / "providers" / "__init__.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registered_aliases() -> list[str]:
    text = _read(PROVIDERS_INIT)
    return sorted(set(re.findall(r'alias="([^"]+)"', text)))


def _registered_model_provider_classes() -> list[str]:
    text = _read(PROVIDERS_INIT)
    classes = re.findall(r'class_name="([^"]+)"', text)
    model_classes = [name for name in classes if name.endswith("ToolCallingProvider")]
    return sorted(set(model_classes))


def _extract_markdown_links(markdown: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown)


def _inline_code_tokens(markdown: str) -> set[str]:
    return set(re.findall(r"(?<!`)`([^`\n]+)`(?!`)", markdown))


def _resolve_link(target: str, doc_path: Path) -> Path | None:
    cleaned = target.strip()
    if not cleaned:
        return None
    cleaned = cleaned.split("#", 1)[0].split("?", 1)[0].strip()
    if not cleaned:
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", cleaned):
        return None
    if cleaned.startswith("/"):
        cleaned = cleaned[1:]
    if re.match(r"^[A-Za-z]:[\\/]", cleaned):
        return Path(cleaned)
    return (doc_path.parent / cleaned).resolve()


def test_example_links_point_to_existing_files() -> None:
    missing: list[str] = []
    for doc in DOC_FILES:
        for target in _extract_markdown_links(_read(doc)):
            if "examples/" not in target.replace("\\", "/") or not target.lower().endswith(".py"):
                continue
            resolved = _resolve_link(target, doc)
            if resolved is None or not resolved.exists():
                missing.append(f"{doc.relative_to(REPO_ROOT)} -> {target}")
    assert not missing, "Broken examples links:\n" + "\n".join(missing)


def test_docs_provider_alias_claims_match_exports() -> None:
    providers_doc = _read(REPO_ROOT / "docs" / "PROVIDERS.md")
    documented_tokens = _inline_code_tokens(providers_doc)

    for alias in _registered_aliases():
        assert alias in documented_tokens, (
            f"docs/PROVIDERS.md is missing alias `{alias}` that is exported in src/mtp/providers/__init__.py"
        )

    assert "MockPlannerProvider" in documented_tokens, (
        "docs/PROVIDERS.md should document `MockPlannerProvider` alias for SimplePlannerProvider"
    )
    assert "SimplePlannerProvider" in documented_tokens, (
        "docs/PROVIDERS.md should mention `SimplePlannerProvider` for the MockPlannerProvider alias"
    )


def test_architecture_provider_coverage_matches_exports() -> None:
    architecture_doc = _read(REPO_ROOT / "docs" / "ARCHITECTURE.md")
    documented_tokens = _inline_code_tokens(architecture_doc)

    for cls_name in _registered_model_provider_classes():
        assert cls_name in documented_tokens, (
            f"docs/ARCHITECTURE.md is missing provider class `{cls_name}` exported in src/mtp/providers/__init__.py"
        )

    assert "SimplePlannerProvider" in documented_tokens
    assert "MockPlannerProvider" in documented_tokens
