from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any

from .model import (
    STATUS_PRIORITY,
    CheckResult,
    ResultStatus,
    read_json,
    write_json_atomic,
)
from .baseline import file_sha256, verify_source_entries, verify_tool_manifest
from .scope import check_scope, match_approval_event


GOVERNANCE_REL = Path("governance/rd-standards-rebuild")
STATE_SEQUENCE = (
    "planned",
    "tooling_ready",
    "sources_frozen",
    "sources_reviewed",
    "rules_classified",
    "rules_rewritten",
    "principles_derived",
    "audit_ready",
    "awaiting_user_review",
    "approved_for_migration_design",
)
GATE_BY_STATE = {
    state: f"G{index}" for index, state in enumerate(STATE_SEQUENCE)
}
OPENSPEC_CHANGE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
WINDOWS_OPENSPEC_WRAPPER_ENV = "RD_REBUILD_OPENSPEC_WRAPPER"
WINDOWS_OPENSPEC_CHANGE_ENV = "RD_REBUILD_OPENSPEC_CHANGE"
WINDOWS_OPENSPEC_COMMAND = (
    '"cmd.exe" /d /s /v:off /c '
    '""%RD_REBUILD_OPENSPEC_WRAPPER%" validate '
    '"%RD_REBUILD_OPENSPEC_CHANGE%" --strict --no-interactive"'
)
REQUIRED_CHECKS_BY_TARGET = {
    "tooling_ready": (
        "unit-tests",
        "fixtures",
        "baseline-dry-run",
        "baseline-verify",
        "scope-check",
        "openspec-strict",
    ),
    "sources_frozen": ("baseline-verify", "scope-check", "tool-manifest"),
    "sources_reviewed": (
        "baseline-verify",
        "scope-check",
        "inventory-check",
        "segment-check",
        "rule-check",
    ),
    "rules_classified": ("classification-check",),
    "rules_rewritten": ("rewrite-check",),
    "principles_derived": ("principle-check", "draft-check"),
    "audit_ready": ("report-build",),
    "awaiting_user_review": ("verify-all", "openspec-strict"),
    "approved_for_migration_design": ("scope-check", "user-review"),
}


def _paths(root: Path) -> dict[str, Path]:
    governance = root.resolve() / GOVERNANCE_REL
    return {
        "governance": governance,
        "policy": governance / "policy.json",
        "baseline": governance / "baseline-manifest.json",
        "tool_manifest": governance / "tool-manifest.json",
        "run_state": governance / "run-state.json",
        "approvals": governance / "approvals.jsonl",
    }


def gate_scope_digest(root: Path) -> str:
    paths = _paths(root)
    baseline = read_json(paths["baseline"])
    tool_manifest = read_json(paths["tool_manifest"])
    payload = {
        "plan_sha256": baseline.get("plan_sha256"),
        "policy_sha256": file_sha256(paths["policy"]),
        "source_manifest_sha256": baseline.get("g0", {}).get(
            "source_manifest_sha256",
            baseline.get("source_manifest_sha256"),
        ),
        "tool_manifest_sha256": tool_manifest.get("aggregate_sha256"),
    }
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _approvals(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"approval line {number} must be an object")
        records.append(payload)
    return records


def _required_file_findings(
    root: Path, policy: dict[str, Any], target: str
) -> list[str]:
    findings: list[str] = []
    for relative in policy.get("required_files_by_gate", {}).get(target, []):
        path = root / relative
        if relative.endswith("/"):
            if not path.is_dir():
                findings.append(f"required gate directory missing: {relative}")
        elif not path.is_file():
            findings.append(f"required gate file missing: {relative}")
    return findings


def transition_gate(
    root: Path,
    target: str,
    checks: dict[str, CheckResult],
    *,
    dry_run: bool,
) -> CheckResult:
    root = root.resolve()
    paths = _paths(root)
    try:
        policy = read_json(paths["policy"])
        state = read_json(paths["run_state"])
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return CheckResult(
            ResultStatus.BLOCKED,
            "gate inputs invalid",
            (str(exc),),
        )
    current = state.get("current_state")
    if current not in STATE_SEQUENCE or target not in STATE_SEQUENCE:
        return CheckResult(
            ResultStatus.BLOCKED,
            "illegal gate transition",
            (f"invalid current or target state: {current} -> {target}",),
        )
    expected_current_gate = GATE_BY_STATE[current]
    last_passed_gate = state.get("last_passed_gate")
    if last_passed_gate != expected_current_gate:
        return CheckResult(
            ResultStatus.BLOCKED,
            "illegal gate transition",
            (
                "current state/last gate mismatch: "
                f"{current} requires {expected_current_gate}, got {last_passed_gate}",
            ),
            {
                "current_state": current,
                "last_passed_gate": last_passed_gate,
                "expected_last_passed_gate": expected_current_gate,
                "target_state": target,
            },
        )
    if STATE_SEQUENCE.index(target) != STATE_SEQUENCE.index(current) + 1:
        return CheckResult(
            ResultStatus.BLOCKED,
            "illegal gate transition",
            (f"gate must advance exactly one state: {current} -> {target}",),
        )
    findings = _required_file_findings(root, policy, target)
    required_checks = REQUIRED_CHECKS_BY_TARGET.get(target, ())
    missing_checks = [name for name in required_checks if name not in checks]
    findings.extend(f"required check missing: {name}" for name in missing_checks)
    present = [checks[name] for name in required_checks if name in checks]
    hard_failing = [
        (name, checks[name])
        for name in required_checks
        if name in checks
        and checks[name].status in {ResultStatus.BLOCKED, ResultStatus.TOOL_ERROR}
    ]
    review_required = [
        (name, checks[name])
        for name in required_checks
        if name in checks and checks[name].status == ResultStatus.REVIEW_REQUIRED
    ]
    if target == "tooling_ready":
        try:
            tool_manifest = read_json(paths["tool_manifest"])
            if (
                tool_manifest.get("status") != "verified"
                or not tool_manifest.get("aggregate_sha256")
            ):
                findings.append("verified tool manifest is required for G1")
            else:
                findings.extend(
                    verify_tool_manifest(root, tool_manifest).findings
                )
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
            findings.append(f"tool manifest invalid: {exc}")
        if not findings:
            current_scope = gate_scope_digest(root)
            for name, result in zip(required_checks, present):
                if result.evidence.get("scope_sha256") != current_scope:
                    findings.append(
                        f"required check evidence is stale for current scope: {name}"
                    )
    if findings:
        return CheckResult(
            ResultStatus.BLOCKED,
            "gate prerequisites blocked",
            tuple(findings),
            {"current_state": current, "target_state": target},
        )
    if hard_failing:
        status = max(
            (result.status for _, result in hard_failing),
            key=STATUS_PRIORITY.__getitem__,
        )
        return CheckResult(
            status,
            "gate checks did not pass",
            tuple(
                f"{name}: {result.status.value}"
                for name, result in hard_failing
            ),
            {"current_state": current, "target_state": target},
        )
    gate = GATE_BY_STATE[target]
    gate_policy = next(
        (
            value
            for value in policy.get("approval_gates", {}).values()
            if value.get("target_state") == target
        ),
        {"human_required": False},
    )
    scope_sha = gate_scope_digest(root)
    approval = None
    if gate_policy.get("human_required"):
        try:
            approval, approval_findings = match_approval_event(
                _approvals(paths["approvals"]),
                gate=gate,
                scope_sha256=scope_sha,
            )
        except (ValueError, json.JSONDecodeError) as exc:
            return CheckResult(
                ResultStatus.BLOCKED,
                "approval record validation blocked",
                (str(exc),),
                {
                    "current_state": current,
                    "target_state": target,
                    "scope_sha256": scope_sha,
                },
            )
        except OSError as exc:
            return CheckResult(
                ResultStatus.TOOL_ERROR,
                "approval record error",
                (str(exc),),
            )
        if approval_findings:
            return CheckResult(
                ResultStatus.BLOCKED,
                "approval record validation blocked",
                tuple(approval_findings),
                {
                    "current_state": current,
                    "target_state": target,
                    "scope_sha256": scope_sha,
                },
            )
    if review_required and not gate_policy.get("human_required"):
        return CheckResult(
            ResultStatus.REVIEW_REQUIRED,
            "gate checks require human review",
            tuple(
                f"{name}: {result.status.value}"
                for name, result in review_required
            ),
            {
                "current_state": current,
                "target_state": target,
                "scope_sha256": scope_sha,
            },
        )
    if gate_policy.get("human_required") and approval is None:
        return CheckResult(
            ResultStatus.REVIEW_REQUIRED,
            f"{gate} user approval required",
            tuple(
                [f"no scope-matching approved event for {gate}"]
                + [
                    f"{name}: {result.status.value}"
                    for name, result in review_required
                ]
            ),
            {
                "current_state": current,
                "target_state": target,
                "scope_sha256": scope_sha,
            },
        )
    if dry_run:
        return CheckResult(
            ResultStatus.PASS,
            "gate dry-run",
            evidence={
                "current_state": current,
                "target_state": target,
                "scope_sha256": scope_sha,
                "would_write": paths["run_state"].as_posix(),
            },
        )
    updated = deepcopy(state)
    updated["current_state"] = target
    updated["last_passed_gate"] = gate
    updated["blockers"] = []
    updated["next_action"] = f"Evaluate prerequisites for {STATE_SEQUENCE[STATE_SEQUENCE.index(target) + 1]}" if target != STATE_SEQUENCE[-1] else "Wait for separately approved migration planning"
    updated["last_transition"] = {
        "gate": gate,
        "target_state": target,
        "scope_sha256": scope_sha,
        "check_results": {
            name: checks[name].to_dict() for name in required_checks
        },
    }
    updated.setdefault("history", []).append(
        {
            "gate": gate,
            "state": target,
            "scope_sha256": scope_sha,
            "check_results": {
                name: checks[name].to_dict() for name in required_checks
            },
        }
    )
    try:
        write_json_atomic(paths["run_state"], updated)
    except Exception as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "gate state write failed",
            (f"{type(exc).__name__}: {exc}",),
            {"state_preserved": True},
        )
    return CheckResult(
        ResultStatus.PASS,
        f"{gate} transition recorded",
        evidence={"current_state": target, "scope_sha256": scope_sha},
    )


def status_check(root: Path) -> CheckResult:
    paths = _paths(root)
    try:
        state = read_json(paths["run_state"])
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "status unavailable",
            (str(exc),),
        )
    current = state.get("current_state")
    if current not in STATE_SEQUENCE:
        return CheckResult(
            ResultStatus.BLOCKED,
            "status invalid",
            (f"unknown current_state: {current}",),
        )
    return CheckResult(
        ResultStatus.PASS,
        "current rebuild status",
        evidence={
            "current_state": current,
            "last_passed_gate": state.get("last_passed_gate"),
            "blockers": state.get("blockers", []),
            "next_action": state.get("next_action"),
            "evidence": state.get("evidence", {}),
        },
    )


def recorded_gate_checks(root: Path, target: str) -> dict[str, CheckResult]:
    paths = _paths(root)
    try:
        tool_manifest = read_json(paths["tool_manifest"])
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return {}
    records = tool_manifest.get("verification", {}).get("checks", {})
    checks: dict[str, CheckResult] = {}
    for name in REQUIRED_CHECKS_BY_TARGET.get(target, ()):
        payload = records.get(name)
        if not isinstance(payload, dict):
            continue
        try:
            status = ResultStatus(payload.get("status"))
        except ValueError:
            status = ResultStatus.TOOL_ERROR
        checks[name] = CheckResult(
            status,
            str(payload.get("summary", name)),
            tuple(str(item) for item in payload.get("findings", [])),
            dict(payload.get("evidence", {})),
        )
    return checks


def _openspec_validation_check(root: Path, change: str) -> CheckResult:
    try:
        if not OPENSPEC_CHANGE_PATTERN.fullmatch(change):
            raise ValueError(f"invalid OpenSpec change identifier: {change!r}")
        executable = shutil.which("openspec")
        if not executable:
            raise FileNotFoundError("OpenSpec executable not found on PATH")
        arguments = [
            executable,
            "validate",
            change,
            "--strict",
            "--no-interactive",
        ]
        command: list[str] | str = arguments
        run_options: dict[str, Any] = {}
        if os.name == "nt" and executable.lower().endswith((".cmd", ".bat")):
            comspec = os.environ.get("COMSPEC") or shutil.which("cmd.exe")
            if not comspec:
                raise FileNotFoundError(
                    "Windows command processor not found for OpenSpec wrapper"
                )
            child_environment = os.environ.copy()
            child_environment[WINDOWS_OPENSPEC_WRAPPER_ENV] = executable
            child_environment[WINDOWS_OPENSPEC_CHANGE_ENV] = change
            command = WINDOWS_OPENSPEC_COMMAND
            run_options = {
                "executable": comspec,
                "env": child_environment,
            }
        process = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            shell=False,
            **run_options,
        )
    except (OSError, ValueError) as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "OpenSpec strict validation tool error",
            (str(exc),),
        )
    output = (process.stdout + process.stderr).strip()
    return CheckResult(
        ResultStatus.PASS if process.returncode == 0 else ResultStatus.BLOCKED,
        "OpenSpec strict validation",
        () if process.returncode == 0 else (output or "OpenSpec validation failed",),
        {"change": change, "exit_code": process.returncode, "output": output},
    )


def gate_checks_for_target(root: Path, target: str) -> dict[str, CheckResult]:
    root = root.resolve()
    if target == "tooling_ready":
        return recorded_gate_checks(root, target)
    required = REQUIRED_CHECKS_BY_TARGET.get(target, ())
    paths = _paths(root)
    try:
        policy = read_json(paths["policy"])
        baseline = read_json(paths["baseline"])
        tool_manifest = read_json(paths["tool_manifest"])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        failure = CheckResult(
            ResultStatus.TOOL_ERROR,
            "live gate inputs invalid",
            (str(exc),),
        )
        return {name: failure for name in required}
    baseline_result = verify_source_entries(
        root,
        baseline.get("protected_sources", []),
        policy.get("source_roots", []),
    )
    if target == "sources_frozen":
        return {
            "baseline-verify": baseline_result,
            "scope-check": check_scope(root, policy, baseline, "content"),
            "tool-manifest": verify_tool_manifest(root, tool_manifest),
        }
    if target == "sources_reviewed":
        from .records import inventory_check, rule_check, segment_check

        return {
            "baseline-verify": baseline_result,
            "scope-check": check_scope(root, policy, baseline, "content"),
            "inventory-check": inventory_check(root),
            "segment-check": segment_check(root),
            "rule-check": rule_check(root),
        }
    if target == "rules_classified":
        from .records import classification_check

        return {"classification-check": classification_check(root)}
    if target == "rules_rewritten":
        from .coverage import rewrite_check

        return {"rewrite-check": rewrite_check(root, policy)}
    if target == "principles_derived":
        from .drafts import draft_check
        from .principles import principle_check

        return {
            "principle-check": principle_check(root, policy),
            "draft-check": draft_check(root, policy),
        }
    if target == "audit_ready":
        from .report import content_report_check

        return {"report-build": content_report_check(root)}
    if target == "awaiting_user_review":
        return {
            "verify-all": verify_all_applicable(root),
            "openspec-strict": _openspec_validation_check(
                root, "rewrite-rd-standards-content"
            ),
        }
    if target == "approved_for_migration_design":
        return {
            "scope-check": check_scope(root, policy, baseline, "content"),
            "user-review": CheckResult(
                ResultStatus.PASS,
                "human approval is evaluated by the gate",
            )
        }
    return {}


def _required_files_check(
    root: Path, policy: dict[str, Any], target: str
) -> CheckResult:
    findings = _required_file_findings(root, policy, target)
    return CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "required tooling files",
        tuple(findings),
        {"target_state": target},
    )


def verify_all_applicable(root: Path) -> CheckResult:
    root = root.resolve()
    paths = _paths(root)
    try:
        policy = read_json(paths["policy"])
        baseline = read_json(paths["baseline"])
        state = read_json(paths["run_state"])
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return CheckResult(
            ResultStatus.TOOL_ERROR,
            "verify-all inputs invalid",
            (str(exc),),
        )
    current = state.get("current_state")
    if current not in STATE_SEQUENCE:
        return CheckResult(
            ResultStatus.BLOCKED,
            "verify-all state invalid",
            (f"unknown current_state: {current}",),
        )
    phase = "tooling" if current == "planned" else "content"
    results: list[CheckResult] = [
        verify_source_entries(
            root,
            baseline.get("protected_sources", []),
            policy.get("source_roots", []),
        ),
        check_scope(root, policy, baseline, phase),
    ]
    next_index = STATE_SEQUENCE.index(current) + 1
    if next_index < len(STATE_SEQUENCE):
        results.append(_required_files_check(root, policy, STATE_SEQUENCE[next_index]))
    applicable_names = ["baseline-verify", "scope-check", "required-files"]
    content_checks = {
        "inventory-check",
        "segment-check",
        "rule-check",
        "classification-check",
        "rewrite-check",
        "principle-check",
        "draft-check",
    }
    if STATE_SEQUENCE.index(current) >= STATE_SEQUENCE.index("sources_frozen"):
        from .coverage import rewrite_check
        from .drafts import draft_check
        from .principles import principle_check
        from .records import (
            classification_check,
            inventory_check,
            rule_check,
            segment_check,
        )

        content_results = {
            "inventory-check": inventory_check(root),
            "segment-check": segment_check(root),
            "rule-check": rule_check(root),
            "classification-check": classification_check(root),
            "rewrite-check": rewrite_check(root, policy),
            "principle-check": principle_check(root, policy),
            "draft-check": draft_check(root, policy),
        }
        for name, result in content_results.items():
            applicable_names.append(name)
            results.append(result)
        not_applicable: list[str] = []
    else:
        not_applicable = sorted(content_checks)
    if STATE_SEQUENCE.index(current) >= STATE_SEQUENCE.index("audit_ready"):
        from .report import content_report_check

        applicable_names.append("report-check")
        results.append(content_report_check(root))
    combined_status = max(
        (result.status for result in results), key=STATUS_PRIORITY.__getitem__
    )
    return CheckResult(
        combined_status,
        "all applicable rebuild checks",
        tuple(finding for result in results for finding in result.findings),
        {
            "applicable_checks": applicable_names,
            "not_applicable": not_applicable,
            "results": [result.to_dict() for result in results],
        },
    )
