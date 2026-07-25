from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

from .model import CheckResult, ResultStatus, read_json, write_json_atomic


GOVERNANCE_REL = Path("governance/rd-standards-rebuild")
REPORT_REL = GOVERNANCE_REL / "reports" / "g1-fact-report.json"
CONTENT_REPORT_REL = GOVERNANCE_REL / "reports" / "content-review-report.json"
CONTENT_INPUTS = {
    "inventory": Path("rebuild-draft/review/source-inventory.csv"),
    "segments": Path("rebuild-draft/review/source-segments.csv"),
    "rules": Path("rebuild-draft/review/atomic-rules.csv"),
    "principles": Path("rebuild-draft/review/principle-traceability.csv"),
}
CONTENT_OUTPUTS = {
    "coverage": Path("rebuild-draft/review/coverage-matrix.csv"),
    "conflicts": Path("rebuild-draft/review/conflicts.md"),
    "retirements": Path("rebuild-draft/review/retirement-candidates.md"),
    "report": CONTENT_REPORT_REL,
}


def _read_approvals(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"approval line {number} must be an object")
        records.append(payload)
    return records


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items() if key}
            for row in csv.DictReader(handle)
        ]


def _write_text_atomic(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", text=True
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _content_input_digest(root: Path) -> str:
    paths = [root / relative for relative in CONTENT_INPUTS.values()]
    draft_root = root / "rebuild-draft"
    if draft_root.is_dir():
        paths.extend(
            path
            for path in sorted(draft_root.rglob("*.md"))
            if "review" not in path.relative_to(draft_root).parts
        )
    lines: list[str] = []
    for path in sorted(set(paths)):
        relative = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{relative}\t{digest}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def _ids(value: str) -> list[str]:
    return [
        item.strip()
        for item in re.split(r"[;,|；]", value or "")
        if item.strip()
    ]


def _build_content_report(root: Path, *, dry_run: bool) -> CheckResult:
    inputs = {name: root / relative for name, relative in CONTENT_INPUTS.items()}
    missing = [name for name, path in inputs.items() if not path.is_file()]
    if missing:
        return CheckResult(
            ResultStatus.BLOCKED,
            "content report inputs missing",
            tuple(f"required content report input missing: {name}" for name in missing),
        )
    try:
        inventory = _read_csv(inputs["inventory"])
        segments = _read_csv(inputs["segments"])
        rules = _read_csv(inputs["rules"])
        principle_rows = _read_csv(inputs["principles"])
        input_digest = _content_input_digest(root)
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "content report input error",
            (str(exc),),
        )
    principle_by_rule: dict[str, list[str]] = {}
    for principle in principle_rows:
        for rule_id in _ids(principle.get("supporting_rule_ids", "")):
            principle_by_rule.setdefault(rule_id, []).append(
                principle.get("principle_id", "")
            )
    coverage_fields = [
        "rule_id",
        "source_id",
        "source_path",
        "source_start_line",
        "source_end_line",
        "treatment",
        "target_rule_id",
        "principle_ids",
        "retirement_reason",
        "conflict_status",
    ]
    coverage_rows: list[dict[str, str]] = []
    conflicts: list[dict[str, str]] = []
    retirements: list[dict[str, str]] = []
    for rule in sorted(rules, key=lambda item: item.get("rule_id", "")):
        treatment = rule.get("treatment", "")
        if treatment == "conflict":
            conflicts.append(rule)
        if treatment == "retire":
            retirements.append(rule)
        coverage_rows.append(
            {
                "rule_id": rule.get("rule_id", ""),
                "source_id": rule.get("source_id", ""),
                "source_path": rule.get("source_path", ""),
                "source_start_line": rule.get("source_start_line", ""),
                "source_end_line": rule.get("source_end_line", ""),
                "treatment": treatment,
                "target_rule_id": rule.get("target_rule_id", ""),
                "principle_ids": ";".join(
                    sorted(principle_by_rule.get(rule.get("rule_id", ""), []))
                ),
                "retirement_reason": rule.get("notes", "")
                if treatment == "retire"
                else "",
                "conflict_status": "requires recorded decision"
                if treatment == "conflict"
                else "",
            }
        )
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=coverage_fields, lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(coverage_rows)
    coverage_text = stream.getvalue()
    conflicts_text = "# Conflicts\n\n" + (
        "\n".join(
            f"- `{item.get('rule_id', '')}`: {item.get('notes', '') or 'Decision required.'}"
            for item in conflicts
        )
        if conflicts
        else "None recorded."
    ) + "\n"
    retirements_text = "# Retirement candidates\n\n" + (
        "\n".join(
            f"- `{item.get('rule_id', '')}`: {item.get('notes', '')}"
            for item in retirements
        )
        if retirements
        else "None recorded."
    ) + "\n"
    report = {
        "schema_version": "1.0",
        "report_type": "content-rewrite-audit",
        "input_digest": input_digest,
        "facts": {
            "source_inventory_count": len(inventory),
            "segment_count": len(segments),
            "atomic_rule_count": len(rules),
            "principle_count": len(principle_rows),
            "conflict_count": len(conflicts),
            "retirement_candidate_count": len(retirements),
            "coverage_row_count": len(coverage_rows),
        },
        "traceability": {
            "sources": CONTENT_INPUTS["inventory"].as_posix(),
            "segments": CONTENT_INPUTS["segments"].as_posix(),
            "rules": CONTENT_INPUTS["rules"].as_posix(),
            "principles": CONTENT_INPUTS["principles"].as_posix(),
            "coverage": CONTENT_OUTPUTS["coverage"].as_posix(),
            "conflicts": CONTENT_OUTPUTS["conflicts"].as_posix(),
            "retirements": CONTENT_OUTPUTS["retirements"].as_posix(),
        },
        "semantic_correctness": "not-assessed",
        "user_review": "required",
    }
    planned = [
        (root / relative).as_posix() for relative in CONTENT_OUTPUTS.values()
    ]
    if dry_run:
        return CheckResult(
            ResultStatus.PASS,
            "content report build dry-run",
            evidence={"planned_writes": planned, "input_digest": input_digest},
        )
    try:
        _write_text_atomic(root / CONTENT_OUTPUTS["coverage"], coverage_text)
        _write_text_atomic(root / CONTENT_OUTPUTS["conflicts"], conflicts_text)
        _write_text_atomic(
            root / CONTENT_OUTPUTS["retirements"], retirements_text
        )
        write_json_atomic(root / CONTENT_OUTPUTS["report"], report)
    except Exception as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "content report write failed",
            (f"{type(exc).__name__}: {exc}",),
        )
    return CheckResult(
        ResultStatus.PASS,
        "content audit reports built",
        evidence={"writes": planned, "input_digest": input_digest},
    )


def content_report_check(root: Path) -> CheckResult:
    root = root.resolve()
    outputs = {name: root / relative for name, relative in CONTENT_OUTPUTS.items()}
    missing = [name for name, path in outputs.items() if not path.is_file()]
    if missing:
        return CheckResult(
            ResultStatus.BLOCKED,
            "content report verification",
            tuple(f"content report output missing: {name}" for name in missing),
        )
    try:
        report = read_json(outputs["report"])
        current_digest = _content_input_digest(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "content report verification error",
            (str(exc),),
        )
    findings: list[str] = []
    if report.get("report_type") != "content-rewrite-audit":
        findings.append("content report has the wrong report type")
    if report.get("input_digest") != current_digest:
        findings.append("content report is stale for the current inputs")
    return CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "content report verification",
        tuple(findings),
        {"input_digest": current_digest, "output_count": len(outputs)},
    )


def build_report(root: Path, *, dry_run: bool) -> CheckResult:
    root = root.resolve()
    governance = root / GOVERNANCE_REL
    inputs = {
        "policy": governance / "policy.json",
        "baseline": governance / "baseline-manifest.json",
        "tool_manifest": governance / "tool-manifest.json",
        "run_state": governance / "run-state.json",
        "approvals": governance / "approvals.jsonl",
    }
    missing = [name for name, path in inputs.items() if not path.is_file()]
    if missing:
        return CheckResult(
            ResultStatus.BLOCKED,
            "report inputs missing",
            tuple(f"required report input missing: {name}" for name in missing),
        )
    try:
        policy = read_json(inputs["policy"])
        baseline = read_json(inputs["baseline"])
        tool_manifest = read_json(inputs["tool_manifest"])
        run_state = read_json(inputs["run_state"])
        approvals = _read_approvals(inputs["approvals"])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "report input error",
            (str(exc),),
        )
    if run_state.get("current_state") != "planned":
        return _build_content_report(root, dry_run=dry_run)
    from .gates import gate_scope_digest

    current_scope_sha256 = gate_scope_digest(root)
    source_count = baseline.get("g0", {}).get(
        "source_file_count", len(baseline.get("protected_sources", []))
    )
    source_digest = baseline.get("g0", {}).get(
        "source_manifest_sha256", baseline.get("source_manifest_sha256")
    )
    workspace = baseline.get("existing_workspace", {})
    workspace_count = workspace.get("file_count", len(workspace.get("files", [])))
    g1_approved = any(
        item.get("gate") == "G1"
        and item.get("decision") == "approved"
        and item.get("decided_by") == "user"
        and item.get("scope_sha256") == current_scope_sha256
        for item in approvals
    )
    core = {
        "schema_version": "1.0",
        "report_type": "g1-tooling-facts",
        "phase": "tooling",
        "facts": {
            "source_file_count": source_count,
            "source_manifest_sha256": source_digest,
            "preserved_workspace_file_count": workspace_count,
            "tool_file_count": len(tool_manifest.get("files", [])),
            "tool_manifest_sha256": tool_manifest.get("aggregate_sha256"),
            "current_state": run_state.get("current_state"),
            "last_passed_gate": run_state.get("last_passed_gate"),
            "approval_record_count": len(approvals),
            "g1_scope_sha256": current_scope_sha256,
        },
        "verification": tool_manifest.get("verification", {}),
        "blockers": run_state.get("blockers", []),
        "next_action": run_state.get("next_action"),
        "g1_review": "approved" if g1_approved else "pending",
        "independent_review": "not-performed",
        "content_rewrite": "not-started",
        "limitations": [
            "independent review was not performed",
            "content rewrite was not started",
            "structural checks do not establish semantic correctness",
        ],
        "traceability": {
            "source_file_count": "baseline-manifest.json:g0.source_file_count",
            "source_manifest_sha256": "baseline-manifest.json:g0.source_manifest_sha256",
            "tool_file_count": "tool-manifest.json:files",
            "verification": "tool-manifest.json:verification",
            "state": "run-state.json",
            "approvals": "approvals.jsonl",
            "policy": policy.get("plan_path", "policy.json:plan_path"),
        },
        "prohibited_conclusions": [
            "G1 is approved without a matching user decision",
            "content semantics are correct",
            "independent final review is complete",
            "Change B may start before G1 approval",
        ],
    }
    encoded = json.dumps(
        core, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    core["input_digest"] = hashlib.sha256(encoded).hexdigest()
    target = root / REPORT_REL
    if dry_run:
        return CheckResult(
            ResultStatus.PASS,
            "report build dry-run",
            evidence={
                "planned_write": target.as_posix(),
                "input_digest": core["input_digest"],
            },
        )
    try:
        write_json_atomic(target, core)
    except Exception as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "report write failed",
            (f"{type(exc).__name__}: {exc}",),
        )
    return CheckResult(
        ResultStatus.PASS,
        "G1 fact report built",
        evidence={
            "report": target.as_posix(),
            "input_digest": core["input_digest"],
            "source_file_count": source_count,
        },
    )
