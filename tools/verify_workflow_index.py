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
ROLE_INDEX_PATH = "docs/03-role-index.md"
ROLE_DOCS = {
    "product": "docs/roles/product.md",
    "tech-lead": "docs/roles/tech-lead.md",
    "backend": "docs/roles/backend.md",
    "frontend": "docs/roles/frontend.md",
    "qa": "docs/roles/qa.md",
    "ops": "docs/roles/ops.md",
    "support-ops": "docs/roles/support-ops.md",
    "security-compliance": "docs/roles/security-compliance.md",
}
ROLE_DOC_REQUIRED_HEADINGS = [
    "## 职责",
    "## 默认参与的 W",
    "## 必须参与的触发条件",
    "## 默认读取",
    "## 固定输出",
    "## 交给总控 Agent 的情况",
    "## 必须问人的情况",
]
ROLE_DOC_REF_RE = re.compile(r"docs/roles/[a-z0-9-]+\.md")
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
        ROLE_INDEX_PATH,
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
    if ROLE_INDEX_PATH not in text:
        add_issue(issues, "error", path, f"Workflow entrypoint must link {ROLE_INDEX_PATH}.")
    if "角色" not in text or "泳道" not in text:
        add_issue(issues, "error", path, "Workflow entrypoint must explain roles as swimlanes.")


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
    if ROLE_INDEX_PATH not in text:
        add_issue(issues, "error", path, f"Workflow index must link {ROLE_INDEX_PATH}.")
    if "角色泳道" not in text:
        add_issue(issues, "error", path, "Workflow index must include role swimlane navigation.")

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


def check_role_index(root: Path, issues: list[dict[str, str]]) -> None:
    path = root / ROLE_INDEX_PATH
    text = read_text(path, issues, "role swimlane index")
    if not text:
        return

    if "W0-W9" not in text:
        add_issue(issues, "error", path, "Role index must preserve W0-W9 as the mainline.")
    if "泳道" not in text:
        add_issue(issues, "error", path, "Role index must define roles as swimlanes.")
    if "总控 Agent" not in text or "角色 Agent" not in text:
        add_issue(issues, "error", path, "Role index must define the total-controller and role-agent contract.")
    refs = set(ROLE_DOC_REF_RE.findall(text))
    for role, doc_path in ROLE_DOCS.items():
        role_file = root / doc_path.replace("/", "\\")
        if not role_file.exists():
            add_issue(issues, "error", role_file, f"Missing role document for {role}.")
            continue
        if doc_path not in refs:
            add_issue(issues, "error", path, f"Role index must link {doc_path}.")

    for role, doc_path in ROLE_DOCS.items():
        role_file = root / doc_path.replace("/", "\\")
        role_text = read_text(role_file, issues, f"role document for {role}")
        if not role_text:
            continue

        for heading in ROLE_DOC_REQUIRED_HEADINGS:
            if heading not in role_text:
                add_issue(issues, "error", role_file, f"Role document must include heading: {heading}")
        if not re.search(r"\bW[0-9]\b", role_text):
            add_issue(issues, "error", role_file, "Role document must mention at least one W0-W9 workflow step.")
        if "docs/02-standard-index.md" not in role_text and "当前主导 W" not in role_text:
            add_issue(
                issues,
                "error",
                role_file,
                "Role document must route through the workflow index or current W, not standalone topic reading.",
            )

        line_count = role_text.count("\n") + 1
        if line_count > 90 or len(role_text) > 6000:
            add_issue(
                issues,
                "error",
                role_file,
                "Role documents should stay short dispatch entries instead of copying standards text.",
            )


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
    check_role_index(root, issues)

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
