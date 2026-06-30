#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

WORKFLOW_STEPS = {f"W{index}" for index in range(10)}
ORDERED_TRIGGER_DOC_RE = re.compile(r"^(\d{2})-.+\.md$")
DOC_REF_RE = re.compile(r"docs/(?:W[0-9][^/]+/)?[0-9]{2}[^`\s|)]+\.md")
WORKFLOW_DIR_RE = re.compile(r"^(W[0-9])-.+")
WORKFLOW_MAIN_NAME = "00-main.md"
WORKFLOW_INDEX_PATH = "docs/02-standard-index.md"
START_STEP_HEADING_RE = re.compile(r"^##\s+(?P<step>W[0-9])[:：]", re.MULTILINE)
INDEX_STEP_HEADING_RE = re.compile(r"^##\s+(?P<step>W[0-9])[:：]", re.MULTILINE)


def add_issue(issues: list[dict[str, str]], level: str, path: Path, message: str) -> None:
    issues.append({"level": level, "path": str(path), "message": message})


def read_text(path: Path, issues: list[dict[str, str]], label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        add_issue(issues, "error", path, f"{label} is missing.")
        return ""


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def trigger_docs(root: Path) -> set[str]:
    docs: set[str] = set()
    for workflow_dir in sorted((root / "docs").iterdir()):
        if not workflow_dir.is_dir() or not WORKFLOW_DIR_RE.match(workflow_dir.name):
            continue
        for path in sorted(workflow_dir.glob("*.md")):
            match = ORDERED_TRIGGER_DOC_RE.match(path.name)
            if not match or match.group(1) == "00":
                continue
            docs.add(rel(path, root))
    return docs


def workflow_step_from_path(path: str) -> str | None:
    parts = Path(path).parts
    if len(parts) < 3 or parts[0] != "docs":
        return None
    match = WORKFLOW_DIR_RE.match(parts[1])
    if not match:
        return None
    return match.group(1)


def check_readme(root: Path, issues: list[dict[str, str]]) -> None:
    path = root / "README.md"
    text = read_text(path, issues, "README")
    if not text:
        return

    required_links = [
        "docs/00-start-here.md",
        "docs/02-standard-index.md",
        "knowledge/context-packs/rd-standards.md",
    ]
    for link in required_links:
        if link not in text:
            add_issue(issues, "error", path, f"README must link {link}.")
    if "AI 研发工作流" not in text and "workflow step" not in text:
        add_issue(issues, "error", path, "README must tell readers to start from the AI R&D workflow.")

    stage_refs = sorted(set(DOC_REF_RE.findall(text)))
    if len(stage_refs) > 8:
        add_issue(
            issues,
            "error",
            path,
            "README appears to contain a flat standards list; keep detailed standard references in docs/02-standard-index.md.",
        )


def check_start_here(root: Path, issues: list[dict[str, str]]) -> None:
    path = root / "docs" / "00-start-here.md"
    text = read_text(path, issues, "workflow entrypoint")
    if not text:
        return

    steps = {match.group("step") for match in START_STEP_HEADING_RE.finditer(text)}
    missing = sorted(WORKFLOW_STEPS - steps)
    if missing:
        add_issue(issues, "error", path, "Missing workflow step headings: " + ", ".join(missing))
    if "W0 Intake" not in text or "W9 Maintain" not in text:
        add_issue(issues, "error", path, "Workflow overview must include W0 Intake and W9 Maintain.")
    if "给 Codex 的接手提示" not in text:
        add_issue(issues, "error", path, "Workflow entrypoint must include a Codex handoff prompt.")


def check_workflow_files(root: Path, issues: list[dict[str, str]]) -> None:
    docs_root = root / "docs"
    for workflow_dir in sorted(docs_root.iterdir()):
        if not workflow_dir.is_dir() or not WORKFLOW_DIR_RE.match(workflow_dir.name):
            continue

        main_file = workflow_dir / WORKFLOW_MAIN_NAME
        if not main_file.exists():
            add_issue(issues, "error", workflow_dir, f"{workflow_dir.name} must contain {WORKFLOW_MAIN_NAME}.")

        legacy_main = workflow_dir / "main.md"
        if legacy_main.exists():
            add_issue(issues, "error", legacy_main, f"Use {WORKFLOW_MAIN_NAME} for workflow main entrypoints.")

        order_numbers: list[int] = []
        for path in sorted(workflow_dir.glob("*.md")):
            if path.name == WORKFLOW_MAIN_NAME:
                continue
            match = ORDERED_TRIGGER_DOC_RE.match(path.name)
            if not match or match.group(1) == "00":
                add_issue(
                    issues,
                    "error",
                    path,
                    "Trigger standards must use '<local-order>-<semantic-name>.md'.",
                )
                continue
            order_numbers.append(int(match.group(1)))

        expected = list(range(1, len(order_numbers) + 1))
        if sorted(order_numbers) != expected:
            add_issue(
                issues,
                "error",
                workflow_dir,
                "Trigger standard prefixes must be consecutive within the directory: "
                + ", ".join(f"{number:02d}" for number in expected),
            )


def check_index(root: Path, issues: list[dict[str, str]]) -> None:
    path = root / WORKFLOW_INDEX_PATH
    text = read_text(path, issues, "workflow index")
    if not text:
        return

    if "Workflow-To-Standard Map" not in text:
        add_issue(issues, "error", path, "Workflow index must include Workflow-To-Standard Map.")
    if "新增规范准入规则" not in text:
        add_issue(issues, "error", path, "Workflow index must include admission rules for new standards.")

    headings = {match.group("step") for match in INDEX_STEP_HEADING_RE.finditer(text)}
    missing_headings = sorted(WORKFLOW_STEPS - headings)
    if missing_headings:
        add_issue(issues, "error", path, "Missing detailed workflow sections: " + ", ".join(missing_headings))

    docs = trigger_docs(root)
    index_refs = set(DOC_REF_RE.findall(text))
    for doc_path in sorted(index_refs):
        ref_path = root / doc_path.replace("/", "\\")
        if not ref_path.exists():
            add_issue(issues, "error", path, f"Referenced document does not exist: {doc_path}")

    for doc_path in sorted(docs):
        if doc_path not in index_refs:
            add_issue(issues, "error", path, f"Trigger standard is not referenced in the workflow index: {doc_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify workflow-first index for one-person AI R&D standards.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    issues: list[dict[str, str]] = []

    check_readme(root, issues)
    check_start_here(root, issues)
    check_workflow_files(root, issues)
    check_index(root, issues)

    errors = [issue for issue in issues if issue["level"] == "error"]
    warnings = [issue for issue in issues if issue["level"] == "warning"]
    ok = not errors
    payload: dict[str, Any] = {
        "ok": ok,
        "errors": errors,
        "warnings": warnings,
    }

    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("PASS" if ok else "FAIL")
        for issue in errors + warnings:
            print(f"{issue['level'].upper()} {issue['path']}: {issue['message']}")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
