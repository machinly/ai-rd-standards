#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

WORKFLOW_STEPS = {f"W{index}" for index in range(10)}
STAGE_DOC_RE = re.compile(r"^(\d{2})-.+\.md$")
DOC_REF_RE = re.compile(r"docs/(?:W[0-9][^/]+/)?[0-9]{2}[^`\s|)]+\.md")
WORKFLOW_DIR_RE = re.compile(r"^(W[0-9])-.+")
INDEX_STAGE_ROW_RE = re.compile(
    r"^\|\s*(?P<stage>\d{2})\s*\|\s*(?P<step>W[0-9])\s*\|\s*`(?P<path>docs/[^`]+\.md)`\s*\|",
    re.MULTILINE,
)
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


def stage_docs(root: Path) -> dict[str, str]:
    docs: dict[str, str] = {}
    for path in sorted((root / "docs").rglob("*.md")):
        match = STAGE_DOC_RE.match(path.name)
        if not match or match.group(1) == "00":
            continue
        docs[match.group(1)] = rel(path, root)
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
        "docs/00-standard-index.md",
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
            "README appears to contain a flat stage list; keep stage mappings in docs/00-standard-index.md.",
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


def check_index(root: Path, issues: list[dict[str, str]]) -> None:
    path = root / "docs" / "00-standard-index.md"
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

    docs = stage_docs(root)
    for stage, doc_path in docs.items():
        actual_step = workflow_step_from_path(doc_path)
        if actual_step not in WORKFLOW_STEPS:
            add_issue(
                issues,
                "error",
                path,
                f"Stage {stage} must live under docs/Wx-* workflow directory: {doc_path}",
            )

    mapped_by_stage: dict[str, list[dict[str, str]]] = {}
    mapped_steps: dict[str, set[str]] = {step: set() for step in WORKFLOW_STEPS}
    for match in INDEX_STAGE_ROW_RE.finditer(text):
        item = match.groupdict()
        mapped_by_stage.setdefault(item["stage"], []).append(item)
        mapped_steps[item["step"]].add(item["stage"])

        ref_path = root / item["path"].replace("/", "\\")
        if not ref_path.exists():
            add_issue(issues, "error", path, f"Mapped document does not exist: {item['path']}")
        expected_path = docs.get(item["stage"])
        if expected_path and item["path"] != expected_path:
            add_issue(
                issues,
                "error",
                path,
                f"Stage {item['stage']} must map to {expected_path}, not {item['path']}.",
            )
        actual_step = workflow_step_from_path(item["path"])
        if actual_step != item["step"]:
            add_issue(
                issues,
                "error",
                path,
                f"Stage {item['stage']} path must live under docs/{item['step']}-*: {item['path']}",
            )

    for stage, doc_path in docs.items():
        rows = mapped_by_stage.get(stage, [])
        if not rows:
            add_issue(issues, "error", path, f"Stage {stage} is not mapped to any workflow step: {doc_path}")
        elif len(rows) > 1:
            steps = ", ".join(row["step"] for row in rows)
            add_issue(issues, "error", path, f"Stage {stage} is mapped more than once: {steps}")

    for step, stages in sorted(mapped_steps.items()):
        if not stages:
            add_issue(issues, "warning", path, f"{step} has no mapped numbered standard.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify workflow-first index for one-person AI R&D standards.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    issues: list[dict[str, str]] = []

    check_readme(root, issues)
    check_start_here(root, issues)
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
