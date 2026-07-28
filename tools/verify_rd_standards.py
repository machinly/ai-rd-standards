#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

from check_runtime_skill_sync import LEGACY_RD_SKILLS


CATEGORY_LAYOUT = {
    "docs/01-initiation": ("01-topic-selection.md", "02-research.md"),
    "docs/02-product-design": ("03-definition.md", "04-experience-design.md"),
    "docs/03-engineering-delivery": (
        "05-technical-design.md",
        "06-planning.md",
        "07-implementation.md",
        "08-verification.md",
        "09-release.md",
    ),
    "docs/04-operations-maintenance": ("10-operation.md", "11-evaluation.md"),
}

REVIEW_FILES = (
    "atomic-rules.csv",
    "conflicts.md",
    "coverage-matrix.csv",
    "principle-traceability.csv",
    "retirement-candidates.md",
    "source-inventory.csv",
    "source-segments.csv",
)

LEGACY_NAV_FILES = (
    "docs/00-start-here.md",
    "docs/01-minimal-rd-kernel.md",
    "docs/01-workflow-diagram.md",
    "docs/02-standard-index.md",
    "docs/03-role-index.md",
    "docs/04-operating-model.md",
    "docs/05-agent-orchestration.md",
)

EXPECTED_LEDGER_ROWS = {
    "source-inventory.csv": 40,
    "source-segments.csv": 573,
    "atomic-rules.csv": 5956,
    "coverage-matrix.csv": 5956,
    "principle-traceability.csv": 15,
}

EXPECTED_FORMAL_RULE_IDS = 2337
EXECUTION_DETAILS_INDEX = "docs/execution-details.md"

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
RULE_ID_RE = re.compile(r"<!--\s*rule-id:\s*([^\s]+)\s*-->")
LEGACY_W_REF_RE = re.compile(r"docs/W[0-9]|\bW0(?:-|–)W9\b")
HEADING_RE = re.compile(r"^#{1,6} .+$", re.MULTILINE)
PRINCIPLE_ID_RE = re.compile(r"^- \*\*((?:CATEGORY|ITEM)-[A-Z0-9-]+)\*\*：.+$")


def read_text(path: Path, errors: list[str], label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"Missing required file: {label}")
    except UnicodeDecodeError:
        errors.append(f"File is not valid UTF-8: {label}")
    return ""


def read_csv_rows(path: Path, errors: list[str], label: str) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    except FileNotFoundError:
        errors.append(f"Missing required ledger: {label}")
    except (UnicodeDecodeError, csv.Error) as exc:
        errors.append(f"Invalid CSV ledger {label}: {exc}")
    return []


def formal_paths(root: Path) -> tuple[list[Path], list[Path]]:
    categories = [root / rel / "README.md" for rel in CATEGORY_LAYOUT]
    items = [
        root / rel / item
        for rel, item_names in CATEGORY_LAYOUT.items()
        for item in item_names
    ]
    return categories, items


def execution_detail_paths(root: Path) -> tuple[dict[Path, list[Path]], list[Path]]:
    by_item: dict[Path, list[Path]] = {}
    all_details: list[Path] = []
    for rel, item_names in CATEGORY_LAYOUT.items():
        for item_name in item_names:
            item = root / rel / item_name
            details = sorted(item.with_suffix("").glob("*.md"))
            by_item[item] = details
            all_details.extend(details)
    return by_item, all_details


def parse_target_ids(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def check_markdown_links(root: Path, paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        rel = path.relative_to(root).as_posix()
        text = read_text(path, errors, rel)
        for target in MARKDOWN_LINK_RE.findall(text):
            clean = target.strip().strip("<>").split("#", 1)[0]
            if not clean or "://" in clean or clean.startswith("mailto:"):
                continue
            candidate = (path.parent / clean).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                errors.append(f"Link escapes repository in {rel}: {target}")
                continue
            if not candidate.exists():
                errors.append(f"Broken local link in {rel}: {target}")


def check_principle_only(
    root: Path, path: Path, expected_prefix: str, errors: list[str]
) -> None:
    rel = path.relative_to(root).as_posix()
    text = read_text(path, errors, rel)
    if not text:
        return

    headings = HEADING_RE.findall(text)
    if len(headings) != 2 or not headings[0].startswith("# ") or headings[1] != "## 根本原则":
        errors.append(
            f"Principle file must contain only an H1 and 根本原则 section: {rel}"
        )

    content_lines = [
        line
        for line in text.splitlines()
        if line.strip() and not line.startswith("# ") and line != "## 根本原则"
    ]
    principle_ids: list[str] = []
    for line in content_lines:
        match = PRINCIPLE_ID_RE.fullmatch(line)
        if not match:
            errors.append(f"Non-principle content remains in {rel}: {line[:80]}")
            continue
        principle_ids.append(match.group(1))
    if not principle_ids:
        errors.append(f"Principle file has no principle: {rel}")
    for principle_id in principle_ids:
        if not principle_id.startswith(expected_prefix):
            errors.append(
                f"Wrong principle ID kind in {rel}: expected {expected_prefix}, found {principle_id}"
            )
    if RULE_ID_RE.search(text):
        errors.append(f"Execution rule remains in principle file: {rel}")


def check_execution_index(
    root: Path, index_path: Path, details: list[Path], errors: list[str]
) -> None:
    rel = index_path.relative_to(root).as_posix()
    text = read_text(index_path, errors, rel)
    if not text:
        return
    required_header = "| 分类 | 项目 | 项目原则 | 内容层 | 执行细节类型 | 细节文件 |"
    if required_header not in text:
        errors.append("Execution details index is missing the required classification header")
    if RULE_ID_RE.search(text):
        errors.append("Execution details index duplicates formal rule markers")

    detail_set = {path.resolve() for path in details}
    indexed: list[Path] = []
    for target in MARKDOWN_LINK_RE.findall(text):
        clean = target.strip().strip("<>").split("#", 1)[0]
        if not clean or "://" in clean or clean.startswith("mailto:"):
            continue
        candidate = (index_path.parent / clean).resolve()
        if candidate in detail_set:
            indexed.append(candidate)

    counts = Counter(indexed)
    missing = sorted(
        path.relative_to(root).as_posix()
        for path in details
        if counts[path.resolve()] == 0
    )
    duplicates = sorted(
        path.relative_to(root).as_posix()
        for path in details
        if counts[path.resolve()] > 1
    )
    if missing:
        errors.append(
            "Execution details missing from the total index: " + ", ".join(missing[:10])
        )
    if duplicates:
        errors.append(
            "Execution details listed more than once in the total index: "
            + ", ".join(duplicates[:10])
        )


def validate_repository(root: Path) -> dict[str, object]:
    root = root.resolve()
    errors: list[str] = []
    categories, items = formal_paths(root)
    details_by_item, details = execution_detail_paths(root)
    details_index = root / EXECUTION_DETAILS_INDEX
    formal = [root / "README.md", *categories, *items, details_index, *details]

    for path in [root / "README.md", *categories, *items, details_index]:
        if not path.is_file():
            errors.append(f"Missing formal standard: {path.relative_to(root).as_posix()}")

    for category in categories:
        if category.is_file():
            check_principle_only(root, category, "CATEGORY-", errors)
    for item in items:
        if item.is_file():
            check_principle_only(root, item, "ITEM-", errors)
        detail_dir = item.with_suffix("")
        if not detail_dir.is_dir():
            errors.append(
                f"Missing execution detail directory: {detail_dir.relative_to(root).as_posix()}"
            )
        elif len(details_by_item[item]) < 2:
            errors.append(
                f"Execution details must be split into multiple files: {detail_dir.relative_to(root).as_posix()}"
            )

    check_execution_index(root, details_index, details, errors)

    legacy_dirs = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "docs").glob("W[0-9]-*")
        if path.is_dir()
    )
    errors.extend(f"Legacy W directory remains: {path}" for path in legacy_dirs)
    for rel in LEGACY_NAV_FILES:
        if (root / rel).exists():
            errors.append(f"Legacy navigation entry remains: {rel}")
    if (root / "rebuild-draft").exists():
        errors.append("Parallel normative copy remains: rebuild-draft")

    review_root = root / "governance" / "rd-standards" / "review"
    for name in REVIEW_FILES:
        if not (review_root / name).is_file():
            errors.append(f"Missing governance review evidence: {name}")

    markers: list[str] = []
    for path in details:
        if path.is_file():
            detail_markers = RULE_ID_RE.findall(read_text(path, errors, str(path)))
            markers.extend(detail_markers)
    marker_counts = Counter(markers)
    duplicates = sorted(name for name, count in marker_counts.items() if count > 1)
    if len(markers) != EXPECTED_FORMAL_RULE_IDS:
        errors.append(
            f"Expected {EXPECTED_FORMAL_RULE_IDS} rule IDs, found {len(markers)}"
        )
    if duplicates:
        errors.append(f"Duplicate formal rule IDs: {', '.join(duplicates[:10])}")

    forbidden_tokens = (
        "rebuild-draft",
        "docs/00-start-here.md",
        "docs/01-minimal-rd-kernel.md",
        "docs/01-workflow-diagram.md",
        "docs/02-standard-index.md",
        "docs/03-role-index.md",
        "docs/04-operating-model.md",
        "docs/05-agent-orchestration.md",
        "并行审查草稿",
        "不是正式入口",
        *LEGACY_RD_SKILLS,
    )
    for path in formal:
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        text = read_text(path, errors, rel)
        for token in forbidden_tokens:
            if token in text:
                errors.append(f"Retired active reference in {rel}: {token}")
        if LEGACY_W_REF_RE.search(text):
            errors.append(f"Legacy W navigation reference remains in {rel}")

    check_markdown_links(root, [path for path in formal if path.is_file()], errors)

    ledgers: dict[str, list[dict[str, str]]] = {}
    for name, expected in EXPECTED_LEDGER_ROWS.items():
        rows = read_csv_rows(review_root / name, errors, name)
        ledgers[name] = rows
        if len(rows) != expected:
            errors.append(f"Expected {expected} rows in {name}, found {len(rows)}")

    atomic_ids = [row.get("rule_id", "") for row in ledgers.get("atomic-rules.csv", [])]
    coverage_rows = ledgers.get("coverage-matrix.csv", [])
    coverage_ids = [row.get("rule_id", "") for row in coverage_rows]
    target_ids = {
        target_id
        for row in coverage_rows
        for target_id in parse_target_ids(row.get("target_rule_id", ""))
    }
    if len(set(atomic_ids)) != len(atomic_ids):
        errors.append("atomic-rules.csv contains duplicate rule_id values")
    if set(coverage_ids) != set(atomic_ids):
        errors.append("coverage-matrix.csv does not cover exactly the atomic rule IDs")
    if target_ids != set(markers):
        errors.append("Coverage target IDs do not match the current formal rule markers")

    conflicts = read_text(review_root / "conflicts.md", errors, "conflicts.md")
    retirements = read_text(
        review_root / "retirement-candidates.md", errors, "retirement-candidates.md"
    )
    if "None recorded." not in conflicts:
        errors.append("Conflict ledger no longer records the approved zero-conflict result")
    if "None recorded." not in retirements:
        errors.append("Retirement ledger no longer records the approved zero-retirement result")

    governance_required = (
        "governance/README.md",
        "governance/project-map.json",
        "governance/current-status.json",
        "governance/rd-standards/approvals.jsonl",
        "governance/rd-standards/replacement-manifest.json",
    )
    for rel in governance_required:
        if not (root / rel).is_file():
            errors.append(f"Missing governance entry or evidence: {rel}")

    status_path = root / "governance" / "current-status.json"
    if status_path.is_file():
        try:
            status = json.loads(status_path.read_text(encoding="utf-8"))
            if status.get("project") != "rd-standards":
                errors.append("governance/current-status.json has the wrong project")
            if status.get("status") != "complete":
                errors.append("governance/current-status.json is not complete")
            if status.get("run_state") != "formal_replacement_complete":
                errors.append("governance/current-status.json has the wrong run_state")
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid governance/current-status.json: {exc}")

    map_path = root / "governance" / "project-map.json"
    if map_path.is_file():
        try:
            project_map = json.loads(map_path.read_text(encoding="utf-8"))
            ids = {item.get("id") for item in project_map.get("domains", [])}
            if "rd-standards" not in ids:
                errors.append("governance/project-map.json does not register rd-standards")
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid governance/project-map.json: {exc}")

    skill_path = root / "skills" / "one-person-openspec-rd" / "SKILL.md"
    skill = read_text(skill_path, errors, "skills/one-person-openspec-rd/SKILL.md")
    for required in (
        "docs/01-initiation/README.md",
        "docs/02-product-design/README.md",
        "docs/03-engineering-delivery/README.md",
        "docs/04-operations-maintenance/README.md",
        "docs/execution-details.md",
        "references/workflow-map.md",
    ):
        if required not in skill:
            errors.append(f"Canonical R&D skill is missing formal routing reference: {required}")
    for retired in LEGACY_NAV_FILES:
        if retired in skill:
            errors.append(f"Canonical R&D skill still references retired entry: {retired}")

    return {
        "valid": not errors,
        "errors": errors,
        "category_count": sum(path.is_file() for path in categories),
        "item_count": sum(path.is_file() for path in items),
        "detail_file_count": len(details),
        "rule_id_count": len(markers),
        "unique_rule_id_count": len(marker_counts),
        "legacy_directory_count": len(legacy_dirs),
        "review_file_count": sum((review_root / name).is_file() for name in REVIEW_FILES),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the formal four-category, eleven-item R&D standards."
    )
    parser.add_argument("root", nargs="?", default=".", help="Repository root.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    result = validate_repository(Path(args.root))
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        label = "PASS" if result["valid"] else "FAIL"
        print(
            f"RD_STANDARDS={label} categories={result['category_count']} "
            f"items={result['item_count']} details={result['detail_file_count']} "
            f"rule_ids={result['rule_id_count']} "
            f"review_files={result['review_file_count']}"
        )
        for error in result["errors"]:
            print("ERROR " + str(error))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
