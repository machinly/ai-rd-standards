from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from .baseline import canonical_path
from .model import CheckResult, ResultStatus


INVENTORY_REL = Path("rebuild-draft/review/source-inventory.csv")
SEGMENTS_REL = Path("rebuild-draft/review/source-segments.csv")
RULES_REL = Path("rebuild-draft/review/atomic-rules.csv")

INVENTORY_FIELDS = {
    "source_id",
    "path",
    "title",
    "original_purpose",
    "applicability",
    "major_topics",
    "referenced_sources",
    "known_overlaps",
    "known_conflicts",
    "review_status",
    "reviewed_at",
}
SEGMENT_FIELDS = {
    "segment_id",
    "source_id",
    "source_start_line",
    "source_end_line",
    "segment_kind",
    "atomic_rule_ids",
    "disposition",
    "notes",
}
RULE_FIELDS = {
    "rule_id",
    "source_id",
    "source_path",
    "source_start_line",
    "source_end_line",
    "source_text",
    "intent",
    "applies_when",
    "subject",
    "rule_layer",
    "candidate_category",
    "candidate_item",
    "secondary_impacts",
    "cluster_id",
    "treatment",
    "target_rule_id",
    "notes",
}

SEGMENT_KINDS = {
    "rule-bearing",
    "context",
    "example",
    "navigation",
    "duplicate",
    "empty",
}
RULE_LAYERS = {
    "principle-input",
    "normative-requirement",
    "risk-or-approval-boundary",
    "artifact-or-evidence",
    "implementation-detail",
    "reference-or-rationale",
}
TREATMENTS = {
    "unreviewed",
    "rewrite",
    "merge",
    "split",
    "supersede",
    "retire",
    "conflict",
}

CATEGORY_ITEMS = {
    "立项": {"选题", "调研"},
    "产品设计": {"定义", "体验设计"},
    "工程交付": {"技术设计", "计划", "实现", "验证", "发布"},
    "运行维护": {"运行", "评估"},
}

BATCH_ROOTS = {
    "w0-w2": ("docs/W0-intake/", "docs/W1-discovery/", "docs/W2-openspec-risk/"),
    "w3-w4": ("docs/W3-ai-behavior/", "docs/W4-build/"),
    "w5-w6": ("docs/W5-verify/", "docs/W6-release/"),
    "w7-w9": ("docs/W7-operate/", "docs/W8-learn/", "docs/W9-maintain/"),
}


def _load_csv(
    path: Path, required_fields: set[str]
) -> tuple[list[dict[str, str]], list[str]]:
    if not path.is_file():
        return [], [f"required record file missing: {path.as_posix()}"]
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = set(reader.fieldnames or [])
            missing = sorted(required_fields - fields)
            if missing:
                return [], [
                    f"missing CSV fields in {path.as_posix()}: {', '.join(missing)}"
                ]
            return [
                {key: (value or "").strip() for key, value in row.items() if key}
                for row in reader
            ], []
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        return [], [f"cannot read CSV {path.as_posix()}: {exc}"]


def _source_files(root: Path, batch: str | None) -> set[str]:
    if batch is not None and batch not in BATCH_ROOTS:
        raise ValueError(f"unknown batch: {batch}")
    roots = BATCH_ROOTS[batch] if batch else tuple(
        canonical_path(path.relative_to(root)) + "/"
        for path in sorted((root / "docs").glob("W[0-9]-*"))
        if path.is_dir()
    )
    files: set[str] = set()
    for relative_root in roots:
        source_root = root / relative_root
        if not source_root.is_dir():
            continue
        files.update(
            canonical_path(path.relative_to(root))
            for path in source_root.rglob("*")
            if path.is_file()
        )
    return files


def _in_batch(path: str, batch: str | None) -> bool:
    if batch is None:
        return True
    return any(canonical_path(path).startswith(root) for root in BATCH_ROOTS[batch])


def inventory_check(root: Path, batch: str | None = None) -> CheckResult:
    root = root.resolve()
    rows, findings = _load_csv(root / INVENTORY_REL, INVENTORY_FIELDS)
    selected = [row for row in rows if _in_batch(row.get("path", ""), batch)]
    ids = Counter(row.get("source_id", "") for row in selected)
    paths = Counter(canonical_path(row.get("path", "")) for row in selected)
    for value, count in sorted(ids.items()):
        if not value:
            findings.append("inventory source_id must be non-empty")
        elif count != 1:
            findings.append(f"duplicate inventory source_id: {value}")
    for value, count in sorted(paths.items()):
        if not value:
            findings.append("inventory path must be non-empty")
        elif count != 1:
            findings.append(f"duplicate inventory path: {value}")
    required_nonempty = {
        "title",
        "original_purpose",
        "applicability",
        "major_topics",
        "reviewed_at",
    }
    for index, row in enumerate(selected, 2):
        for field in sorted(required_nonempty):
            if not row.get(field):
                findings.append(f"inventory row {index} missing value: {field}")
        if row.get("review_status") != "reviewed":
            findings.append(
                f"inventory row {index} review_status must be reviewed"
            )
    expected = _source_files(root, batch)
    recorded = set(paths)
    for path in sorted(expected - recorded):
        findings.append(f"source missing from inventory: {path}")
    for path in sorted(recorded - expected):
        findings.append(f"inventory path is not a source file: {path}")
    return CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "source inventory check",
        tuple(findings),
        {
            "source_count": len(expected),
            "inventory_row_count": len(selected),
            "batch": batch,
        },
    )


def _positive_int(value: str) -> int | None:
    if not re.fullmatch(r"[1-9][0-9]*", value or ""):
        return None
    return int(value)


def segment_check(root: Path, batch: str | None = None) -> CheckResult:
    root = root.resolve()
    inventory_rows, inventory_findings = _load_csv(
        root / INVENTORY_REL, INVENTORY_FIELDS
    )
    segment_rows, findings = _load_csv(root / SEGMENTS_REL, SEGMENT_FIELDS)
    rule_rows, rule_findings = _load_csv(root / RULES_REL, RULE_FIELDS)
    findings.extend(inventory_findings)
    findings.extend(rule_findings)
    rule_sources = {
        row.get("rule_id", ""): row.get("source_id", "")
        for row in rule_rows
        if row.get("rule_id")
    }
    inventory = {
        row["source_id"]: canonical_path(row["path"])
        for row in inventory_rows
        if row.get("source_id") and _in_batch(row.get("path", ""), batch)
    }
    selected = [
        row for row in segment_rows if row.get("source_id") in inventory
    ]
    segment_ids = Counter(row.get("segment_id", "") for row in selected)
    for value, count in sorted(segment_ids.items()):
        if not value:
            findings.append("segment_id must be non-empty")
        elif count != 1:
            findings.append(f"duplicate segment_id: {value}")
    coverage: dict[str, Counter[int]] = defaultdict(Counter)
    for index, row in enumerate(selected, 2):
        source_id = row.get("source_id", "")
        path = root / inventory[source_id]
        lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
        start = _positive_int(row.get("source_start_line", ""))
        end = _positive_int(row.get("source_end_line", ""))
        if start is None or end is None or start > end or end > len(lines):
            findings.append(
                f"segment row {index} has invalid line range for {inventory[source_id]}"
            )
            continue
        kind = row.get("segment_kind", "")
        if kind not in SEGMENT_KINDS:
            findings.append(f"segment row {index} has invalid segment_kind: {kind}")
        if kind == "rule-bearing" and not row.get("atomic_rule_ids"):
            findings.append(
                f"segment row {index} rule-bearing segment lacks atomic_rule_ids"
            )
        if kind == "rule-bearing":
            linked_rule_ids = [
                value.strip()
                for value in re.split(
                    r"[;,|；]", row.get("atomic_rule_ids", "")
                )
                if value.strip()
            ]
            for rule_id in linked_rule_ids:
                if rule_id not in rule_sources:
                    findings.append(
                        f"segment row {index} atomic rule does not exist: {rule_id}"
                    )
                elif rule_sources[rule_id] != source_id:
                    findings.append(
                        f"segment row {index} atomic rule belongs to another source: {rule_id}"
                    )
        if kind != "rule-bearing" and not (
            row.get("disposition") or row.get("notes")
        ):
            findings.append(
                f"segment row {index} non-rule segment lacks explanation"
            )
        for number in range(start, end + 1):
            if lines[number - 1].strip():
                coverage[source_id][number] += 1
    nonblank_count = 0
    for source_id, relative in sorted(inventory.items()):
        path = root / relative
        if not path.is_file():
            findings.append(f"segment source missing: {relative}")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, 1):
            if not line.strip():
                continue
            nonblank_count += 1
            count = coverage[source_id][number]
            if count == 0:
                findings.append(f"uncovered nonblank line: {relative}:{number}")
            elif count > 1:
                findings.append(f"overlapping segments: {relative}:{number}")
    return CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "source segment check",
        tuple(findings),
        {
            "segment_count": len(selected),
            "covered_nonblank_line_count": nonblank_count,
            "batch": batch,
        },
    )


def rule_check(root: Path, batch: str | None = None) -> CheckResult:
    root = root.resolve()
    inventory_rows, inventory_findings = _load_csv(
        root / INVENTORY_REL, INVENTORY_FIELDS
    )
    rows, findings = _load_csv(root / RULES_REL, RULE_FIELDS)
    findings.extend(inventory_findings)
    inventory = {
        row["source_id"]: canonical_path(row["path"])
        for row in inventory_rows
        if row.get("source_id")
    }
    selected = [
        row for row in rows if _in_batch(row.get("source_path", ""), batch)
    ]
    ids = Counter(row.get("rule_id", "") for row in selected)
    for value, count in sorted(ids.items()):
        if not value:
            findings.append("rule_id must be non-empty")
        elif count != 1:
            findings.append(f"duplicate rule_id: {value}")
    required_values = {
        "source_id",
        "source_path",
        "source_start_line",
        "source_end_line",
        "source_text",
        "intent",
        "applies_when",
        "subject",
        "rule_layer",
        "treatment",
    }
    for index, row in enumerate(selected, 2):
        rule_id = row.get("rule_id") or f"row-{index}"
        for field in sorted(required_values):
            if not row.get(field):
                findings.append(f"{rule_id} missing value: {field}")
        source_id = row.get("source_id", "")
        relative = canonical_path(row.get("source_path", ""))
        if source_id not in inventory:
            findings.append(f"{rule_id} source_id does not exist: {source_id}")
        elif inventory[source_id] != relative:
            findings.append(f"{rule_id} source_path does not match inventory")
        path = root / relative
        lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
        start = _positive_int(row.get("source_start_line", ""))
        end = _positive_int(row.get("source_end_line", ""))
        if start is None or end is None or start > end or end > len(lines):
            findings.append(f"{rule_id} has invalid source line range")
        elif row.get("source_text", "") not in "\n".join(lines[start - 1 : end]):
            findings.append(f"{rule_id} source_text is not present in source line range")
        if row.get("rule_layer") not in RULE_LAYERS:
            findings.append(f"{rule_id} has invalid rule_layer")
        if row.get("treatment") not in TREATMENTS:
            findings.append(f"{rule_id} has invalid treatment")
    return CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "atomic rule check",
        tuple(findings),
        {"rule_count": len(selected), "batch": batch},
    )


def load_atomic_rules(root: Path) -> tuple[list[dict[str, str]], list[str]]:
    return _load_csv(root.resolve() / RULES_REL, RULE_FIELDS)


def classification_check(root: Path) -> CheckResult:
    rows, findings = load_atomic_rules(root)
    review_findings: list[str] = []
    all_items = {item for items in CATEGORY_ITEMS.values() for item in items}
    classified = 0
    for index, row in enumerate(rows, 2):
        rule_id = row.get("rule_id") or f"row-{index}"
        category = row.get("candidate_category", "")
        item = row.get("candidate_item", "")
        if (
            category not in CATEGORY_ITEMS
            or item not in CATEGORY_ITEMS.get(category, set())
            or any(separator in item for separator in (";", ",", "|", "；"))
        ):
            findings.append(
                f"{rule_id} primary owner must be exactly one valid category/item"
            )
        else:
            classified += 1
        secondary = [
            value.strip()
            for value in re.split(r"[;,|；]", row.get("secondary_impacts", ""))
            if value.strip()
        ]
        for value in secondary:
            normalized = value.split("/", 1)[-1]
            if normalized not in all_items:
                findings.append(f"{rule_id} has invalid secondary impact: {value}")
        if row.get("treatment") == "conflict":
            review_findings.append(
                f"{rule_id} conflict requires an explicit user decision"
            )
    if findings:
        status = ResultStatus.BLOCKED
        combined = findings + review_findings
    elif review_findings:
        status = ResultStatus.REVIEW_REQUIRED
        combined = review_findings
    else:
        status = ResultStatus.PASS
        combined = []
    return CheckResult(
        status,
        "classification check",
        tuple(combined),
        {
            "rule_count": len(rows),
            "classified_rule_count": classified,
            "review_required_count": len(review_findings),
        },
    )
