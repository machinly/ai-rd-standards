from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

from .model import CheckResult, ResultStatus
from .records import CATEGORY_ITEMS, _load_csv, load_atomic_rules


PRINCIPLES_REL = Path("rebuild-draft/review/principle-traceability.csv")
PRINCIPLE_FIELDS = {
    "principle_id",
    "level",
    "category",
    "item",
    "statement",
    "supporting_cluster_ids",
    "supporting_rule_ids",
    "decision_guidance",
    "stability_check",
    "conflicting_rule_ids",
    "status",
}


def _ids(value: str) -> list[str]:
    return [
        item.strip()
        for item in re.split(r"[;,|；]", value or "")
        if item.strip()
    ]


def principle_check(root: Path, policy: dict[str, Any]) -> CheckResult:
    root = root.resolve()
    rows, findings = _load_csv(root / PRINCIPLES_REL, PRINCIPLE_FIELDS)
    rules, rule_findings = load_atomic_rules(root)
    findings.extend(rule_findings)
    rule_map = {row.get("rule_id", ""): row for row in rules if row.get("rule_id")}
    principle_ids = Counter(row.get("principle_id", "") for row in rows)
    for value, count in sorted(principle_ids.items()):
        if not value:
            findings.append("principle_id must be non-empty")
        elif count != 1:
            findings.append(f"duplicate principle_id: {value}")
    try:
        patterns = [
            re.compile(pattern)
            for pattern in policy.get("principle_review_patterns", [])
        ]
    except re.error as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "principle check tool error",
            (f"invalid principle review pattern: {exc}",),
        )
    review_findings: list[str] = []
    for index, row in enumerate(rows, 2):
        principle_id = row.get("principle_id") or f"row-{index}"
        for field in (
            "level",
            "category",
            "statement",
            "supporting_rule_ids",
            "decision_guidance",
            "stability_check",
            "status",
        ):
            if not row.get(field, "").strip():
                findings.append(f"{principle_id} missing value: {field}")
        level = row.get("level", "")
        category = row.get("category", "")
        item = row.get("item", "")
        if category not in CATEGORY_ITEMS:
            findings.append(f"{principle_id} has invalid category")
        if level == "item":
            if item not in CATEGORY_ITEMS.get(category, set()):
                findings.append(f"{principle_id} has invalid item")
            if not _ids(row.get("supporting_cluster_ids", "")):
                findings.append(f"{principle_id} lacks supporting clusters")
        elif level == "category":
            if item:
                findings.append(f"{principle_id} category principle must not own an item")
        else:
            findings.append(f"{principle_id} has invalid level")
        support_ids = _ids(row.get("supporting_rule_ids", ""))
        valid_support = [rule_map[value] for value in support_ids if value in rule_map]
        for value in support_ids:
            if value not in rule_map:
                findings.append(f"{principle_id} support rule does not exist: {value}")
        if not valid_support:
            findings.append(f"{principle_id} has no valid supporting rules")
        if level == "item":
            for rule in valid_support:
                if (
                    rule.get("candidate_category") != category
                    or rule.get("candidate_item") != item
                ):
                    findings.append(
                        f"{principle_id} support rule is outside its category/item"
                    )
        if level == "category":
            covered_items = {
                rule.get("candidate_item")
                for rule in valid_support
                if rule.get("candidate_category") == category
            }
            if len(covered_items) < 2:
                findings.append(
                    f"{principle_id} category principle must cover multiple items"
                )
        for value in _ids(row.get("conflicting_rule_ids", "")):
            if value not in rule_map:
                findings.append(f"{principle_id} conflicting rule does not exist: {value}")
        statement = row.get("statement", "")
        for pattern in patterns:
            if pattern.search(statement):
                review_findings.append(
                    f"{principle_id} contains tool-specific language matching {pattern.pattern}"
                )
                break
    required_category_items = (
        policy.get("allowed_enums", {}).get("category_item", {})
    )
    if isinstance(required_category_items, dict):
        item_principles = {
            (row.get("category", ""), row.get("item", ""))
            for row in rows
            if row.get("level") == "item"
        }
        category_principles = {
            row.get("category", "")
            for row in rows
            if row.get("level") == "category"
        }
        for category, items in required_category_items.items():
            if category not in category_principles:
                findings.append(f"missing category principle: {category}")
            for item in items:
                if (category, item) not in item_principles:
                    findings.append(
                        f"missing item principle: {category}/{item}"
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
        "principle traceability check",
        tuple(combined),
        {
            "principle_count": len(rows),
            "item_principle_count": sum(row.get("level") == "item" for row in rows),
            "category_principle_count": sum(
                row.get("level") == "category" for row in rows
            ),
            "review_required_count": len(review_findings),
        },
    )
