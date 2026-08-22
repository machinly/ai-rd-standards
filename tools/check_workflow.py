#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MAX_DEFAULT_LINES = 200
MAX_NORMATIVE_LINES = 350

REQUIRED_FILES = (
    "README.md",
    "WORKFLOW.md",
    "skills/opc-rd/SKILL.md",
    "openspec/README.md",
    "openspec/config.yaml",
    "tools/check_workflow.py",
)

RETIRED_PATHS = (
    "decisions",
    "experiments",
    "governance",
    "knowledge",
    "reviews",
    "docs/01-initiation",
    "docs/02-product-design",
    "docs/03-engineering-delivery",
    "docs/04-operations-maintenance",
    "docs/execution-details.md",
    "docs/roles",
    "docs/sources",
    "skills/opc-rd/references/workflow-map.md",
    "skills/opc-rd/references/review-rubric.md",
    "tools/verify_rd_standards.py",
    "tools/test_current_rd_standards.py",
    "tools/check_runtime_skill_sync.py",
    "tools/verify_project_evidence.py",
    "tools/test_verify_project_evidence.py",
    "tools/verify_pilot_records.py",
    "tools/test_verify_pilot_records.py",
)

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def read_text(path: Path, errors: list[str], label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"Missing required file: {label}")
    except UnicodeDecodeError:
        errors.append(f"File is not valid UTF-8: {label}")
    return ""


def physical_lines(text: str) -> int:
    return len(text.splitlines())


def is_under_ignored_tree(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    return bool(relative.parts and relative.parts[0].startswith("."))


def is_under_retired_path(root: Path, path: Path) -> bool:
    relative = path.relative_to(root).as_posix()
    return any(relative == retired or relative.startswith(f"{retired}/") for retired in RETIRED_PATHS)


def check_markdown_links(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*.md")):
        if is_under_ignored_tree(root, path) or is_under_retired_path(root, path):
            continue
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"File is not valid UTF-8: {relative}")
            continue

        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip().strip("<>")
            clean = target.split("#", 1)[0].strip()
            if not clean or "://" in clean or clean.startswith("mailto:"):
                continue
            destination = (path.parent / clean).resolve()
            if not destination.exists():
                errors.append(f"Broken local Markdown link in {relative}: {target}")


def check_active_changes(root: Path, errors: list[str]) -> int:
    changes_root = root / "openspec" / "changes"
    if not changes_root.exists():
        return 0
    if not changes_root.is_dir():
        errors.append("openspec/changes must be a directory when present")
        return 0

    active_changes = [path for path in sorted(changes_root.iterdir()) if not path.name.startswith(".")]
    count = 0
    for change in active_changes:
        if not change.is_dir():
            errors.append(f"Unexpected file in openspec/changes: {change.name}")
            continue
        count += 1
        for required in ("proposal.md", "tasks.md"):
            if not (change / required).is_file():
                errors.append(f"Active change {change.name} is missing {required}")
    return count


def validate_repository(root: Path) -> dict[str, object]:
    root = root.resolve()
    errors: list[str] = []
    contents: dict[str, str] = {}

    for relative in REQUIRED_FILES:
        contents[relative] = read_text(root / relative, errors, relative)

    readme = contents.get("README.md", "")
    readme_targets = {
        target.strip().strip("<>").split("#", 1)[0].removeprefix("./")
        for target in MARKDOWN_LINK_RE.findall(readme)
    }
    if readme and "WORKFLOW.md" not in readme_targets:
        errors.append("README.md must link to WORKFLOW.md")

    default_lines = physical_lines(readme) + physical_lines(contents.get("WORKFLOW.md", ""))
    normative_lines = default_lines + physical_lines(contents.get("skills/opc-rd/SKILL.md", ""))
    if default_lines > MAX_DEFAULT_LINES:
        errors.append(
            f"Default reading exceeds {MAX_DEFAULT_LINES} lines: {default_lines}"
        )
    if normative_lines > MAX_NORMATIVE_LINES:
        errors.append(
            f"Normative entry set exceeds {MAX_NORMATIVE_LINES} lines: {normative_lines}"
        )

    config = contents.get("openspec/config.yaml", "")
    if (root / "openspec/config.yaml").is_file() and not config.strip():
        errors.append("openspec/config.yaml must not be empty")

    for relative in RETIRED_PATHS:
        if (root / relative).exists():
            errors.append(f"Retired path is still active: {relative}")

    active_change_count = check_active_changes(root, errors)
    check_markdown_links(root, errors)

    return {
        "errors": errors,
        "default_lines": default_lines,
        "normative_lines": normative_lines,
        "active_change_count": active_change_count,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the minimal R&D workflow repository")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args(argv)

    result = validate_repository(Path(args.root))
    errors = result["errors"]
    if errors:
        print(
            "WORKFLOW_CHECK=FAIL "
            f"default_lines={result['default_lines']} "
            f"normative_lines={result['normative_lines']} "
            f"active_changes={result['active_change_count']}"
        )
        for error in errors:
            print(f"ERROR {error}")
        return 1

    print(
        "WORKFLOW_CHECK=PASS "
        f"default_lines={result['default_lines']} "
        f"normative_lines={result['normative_lines']} "
        f"active_changes={result['active_change_count']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
