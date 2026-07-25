from __future__ import annotations

import difflib
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .model import CheckResult, ResultStatus
from .records import load_atomic_rules


RETAINED_TREATMENTS = {"rewrite", "merge", "split", "supersede"}
FINAL_TREATMENTS = RETAINED_TREATMENTS | {"retire", "conflict"}


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def _target_ids(value: str) -> list[str]:
    return [
        item.strip()
        for item in re.split(r"[;,|；]", value or "")
        if item.strip()
    ]


def _draft_material(root: Path) -> tuple[str, list[str], Counter[str]]:
    draft_root = root / "rebuild-draft"
    texts: list[str] = []
    lines: list[str] = []
    markers: Counter[str] = Counter()
    if not draft_root.is_dir():
        return "", [], markers
    for path in sorted(draft_root.rglob("*.md")):
        if "review" in path.relative_to(draft_root).parts:
            continue
        text = path.read_text(encoding="utf-8")
        texts.append(text)
        lines.extend(
            line.strip()
            for line in text.splitlines()
            if line.strip()
            and not line.lstrip().startswith(("<!--", "#", "```"))
        )
        markers.update(
            match.strip()
            for match in re.findall(
                r"<!--\s*rule-id:\s*([^>]+?)\s*-->", text, flags=re.IGNORECASE
            )
        )
    return "\n".join(texts), lines, markers


def rewrite_check(root: Path, policy: dict[str, Any]) -> CheckResult:
    root = root.resolve()
    rows, findings = load_atomic_rules(root)
    review_findings: list[str] = []
    warning_findings: list[str] = []
    draft_text, draft_lines, marker_counts = _draft_material(root)
    normalized_draft = _normalize_text(draft_text)
    thresholds = policy.get("copy_detection_thresholds", {})
    minimum = int(thresholds.get("normalized_exact_copy_min_chars", 40))
    similarity_threshold = float(thresholds.get("similarity_review_ratio", 0.9))
    required_targets: set[str] = set()
    for index, row in enumerate(rows, 2):
        rule_id = row.get("rule_id") or f"row-{index}"
        treatment = row.get("treatment", "")
        if treatment not in FINAL_TREATMENTS:
            findings.append(f"{rule_id} has no final treatment")
            continue
        if treatment in RETAINED_TREATMENTS:
            targets = _target_ids(row.get("target_rule_id", ""))
            if not targets:
                findings.append(f"{rule_id} retained treatment lacks target rule")
            required_targets.update(targets)
        if treatment == "retire":
            if not row.get("notes", "").strip():
                findings.append(f"{rule_id} retire treatment lacks per-rule reason")
            else:
                warning_findings.append(
                    f"{rule_id} retirement reason requires user acceptance"
                )
        if treatment == "conflict":
            review_findings.append(f"{rule_id} conflict requires user decision")
        source = _normalize_text(row.get("source_text", ""))
        if treatment not in RETAINED_TREATMENTS or len(source) < minimum:
            continue
        if source and source in normalized_draft:
            findings.append(f"{rule_id} exact copy from source appears in draft")
            continue
        best_ratio = max(
            (
                difflib.SequenceMatcher(None, source, _normalize_text(line)).ratio()
                for line in draft_lines
                if len(_normalize_text(line)) >= minimum
            ),
            default=0.0,
        )
        if best_ratio >= similarity_threshold:
            review_findings.append(
                f"{rule_id} high-similarity draft text requires review ({best_ratio:.3f})"
            )
    for target in sorted(required_targets):
        count = marker_counts[target]
        if count == 0:
            findings.append(f"target rule marker missing from draft: {target}")
        elif count > 1:
            findings.append(f"target rule marker is not authoritative: {target}")
    if findings:
        status = ResultStatus.BLOCKED
        combined = findings + review_findings + warning_findings
    elif review_findings:
        status = ResultStatus.REVIEW_REQUIRED
        combined = review_findings + warning_findings
    elif warning_findings:
        status = ResultStatus.WARN
        combined = warning_findings
    else:
        status = ResultStatus.PASS
        combined = []
    return CheckResult(
        status,
        "rewrite traceability and copy check",
        tuple(combined),
        {
            "rule_count": len(rows),
            "target_marker_count": sum(marker_counts.values()),
            "review_required_count": len(review_findings),
            "warning_count": len(warning_findings),
            "exact_copy_min_chars": minimum,
            "similarity_review_ratio": similarity_threshold,
        },
    )
