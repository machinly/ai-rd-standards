from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from .baseline import (
    capture_git_status_lines,
    capture_workspace_entries,
    canonical_path,
    file_sha256,
    path_matches,
    verify_source_entries,
    verify_tool_manifest,
)
from .model import CheckResult, ResultStatus, combine_results


RECOVERY_ID = "G1R-2026-07-19-windows-openspec-launcher"
RECOVERY_MANIFEST_REL = (
    "governance/rd-standards-rebuild/reports/"
    "2026-07-19-tool-recovery-manifest.json"
)
RECOVERY_BOOTSTRAP_REL = (
    "governance/rd-standards-rebuild/reports/"
    "2026-07-19-tool-recovery-bootstrap.json"
)
RECOVERY_FAILURE_REL = (
    "governance/rd-standards-rebuild/reports/"
    "2026-07-19-g8-openspec-launcher-tool-error.json"
)
RECOVERY_BASELINE_REL = "governance/rd-standards-rebuild/baseline-manifest.json"
RECOVERY_RUN_STATE_REL = "governance/rd-standards-rebuild/run-state.json"
RECOVERY_BASELINE_MANIFEST_SHA256 = (
    "ed321bd580495acc2bd28464d1665ed8b2061ec96e6e650ea377b615d88250c3"
)
RECOVERY_BASE_TOOL_MANIFEST_SHA256 = (
    "76c857c9187c03bf3b41e4e55f1cffd72862ac1824b31f7b8b78f0651082592f"
)
RECOVERY_SOURCE_MANIFEST_SHA256 = (
    "ac382ac1d71fae8e012b543b173e2c6eba7c1dfaabd4701c8d3633d5af5f653c"
)
RECOVERY_BOOTSTRAP_SHA256 = (
    "d72b427eb1a17a7390abe02b8b7c33b865d0cd1d7140b3a169a27a4a89ec28e6"
)
RECOVERY_IMPLEMENTATION_AUTHORIZATION_ID = (
    "G1R-2026-07-19-user-approved-tool-recovery-protocol"
)
RECOVERY_ALLOWED_PATHS = (
    "tools/rd_rebuild_core/gates.py",
    "tools/rd_rebuild_core/scope.py",
    "tools/test_rd_rebuild_gates.py",
    "tools/test_rd_rebuild_scope.py",
    "openspec/changes/build-rd-rewrite-guardrails/",
    "governance/rd-standards-rebuild/tool-manifest.json",
    "governance/rd-standards-rebuild/approvals.jsonl",
    RECOVERY_BOOTSTRAP_REL,
    RECOVERY_MANIFEST_REL,
)
RECOVERY_DYNAMIC_PATHS = {
    "governance/rd-standards-rebuild/tool-manifest.json",
    "governance/rd-standards-rebuild/approvals.jsonl",
    RECOVERY_MANIFEST_REL,
}
RECOVERY_FROZEN_EXCLUSIONS = RECOVERY_ALLOWED_PATHS + (RECOVERY_RUN_STATE_REL,)
RECOVERY_GATE_BY_STATE = {
    "audit_ready": "G7",
    "awaiting_user_review": "G8",
    "approved_for_migration_design": "G9",
}
RECOVERY_SCOPE_FIELDS = (
    "schema_version",
    "recovery_id",
    "authorization",
    "base_tool_manifest_sha256",
    "replacement_tool_manifest_sha256",
    "source_manifest_sha256",
    "allowed_recovery_paths",
    "bootstrap",
    "failure",
    "protected_workspace_snapshot",
    "durable_workspace_snapshot",
    "frozen_workspace_snapshot",
    "changed_files",
    "verification",
    "producer_self_check",
    "independent_review",
    "approval_id",
)
APPROVAL_REQUIRED_FIELDS = (
    "approval_id",
    "gate",
    "decision",
    "decided_by",
    "decided_at",
    "scope_sha256",
    "decision_source",
    "notes",
)
RECOVERY_REQUIRED_CHECKS = (
    "full-unit-tests",
    "fixtures",
    "source-baseline",
    "protected-workspace",
    "candidate-tool-manifest",
    "openspec-internal-change-b",
    "openspec-standalone-change-b",
    "openspec-strict-change-a",
    "openspec-status-change-a",
    "openspec-status-change-b",
    "workflow-index",
)


def _canonical_digest(payload: Any) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def recovery_workspace_snapshot(
    root: Path, excluded_paths: Iterable[str]
) -> dict[str, Any]:
    files = capture_workspace_entries(root, excluded_paths)
    git_status = capture_git_status_lines(root, excluded_paths)
    return {
        "file_count": len(files),
        "file_digest": _canonical_digest(files),
        "missing_path_count": sum(not item["exists"] for item in files),
        "git_status_count": len(git_status),
        "git_status_digest": _canonical_digest(git_status),
    }


def recovery_scope_digest(payload: dict[str, Any]) -> str:
    return _canonical_digest(
        {field: payload.get(field) for field in RECOVERY_SCOPE_FIELDS}
    )


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def approval_record_findings(
    record: dict[str, Any],
    *,
    require_decided_at: bool,
    context: str,
) -> list[str]:
    findings: list[str] = []
    for field in APPROVAL_REQUIRED_FIELDS:
        if field not in record:
            findings.append(f"{context} missing required field: {field}")
    for field in (
        "approval_id",
        "gate",
        "decision",
        "decided_by",
        "scope_sha256",
        "decision_source",
    ):
        if field in record and not _nonempty_string(record.get(field)):
            findings.append(f"{context} field must be a nonempty string: {field}")
    if "decided_at" in record:
        decided_at = record.get("decided_at")
        if require_decided_at:
            if not _nonempty_string(decided_at):
                findings.append(
                    f"{context} field must be a nonempty string: decided_at"
                )
        elif decided_at is not None and not _nonempty_string(decided_at):
            findings.append(
                f"{context} field must be null or a nonempty string: decided_at"
            )
    if "notes" in record and not isinstance(record.get("notes"), str):
        findings.append(f"{context} field must be a string: notes")
    scope_sha256 = record.get("scope_sha256")
    if _nonempty_string(scope_sha256) and (
        len(scope_sha256) != 64
        or any(character not in "0123456789abcdef" for character in scope_sha256)
    ):
        findings.append(f"{context} scope_sha256 must be lowercase SHA-256")
    return findings


def match_approval_event(
    records: list[dict[str, Any]],
    *,
    gate: str,
    scope_sha256: str,
    approval_id: str | None = None,
) -> tuple[dict[str, Any] | None, list[str]]:
    findings: list[str] = []
    approval_id_lines: dict[str, int] = {}
    for line_number, record in enumerate(records, 1):
        context = f"approval record {line_number}"
        findings.extend(
            approval_record_findings(
                record,
                require_decided_at=False,
                context=context,
            )
        )
        record_id = record.get("approval_id")
        if _nonempty_string(record_id):
            if record_id in approval_id_lines:
                findings.append(
                    "duplicate approval_id: "
                    f"{record_id} at records {approval_id_lines[record_id]} "
                    f"and {line_number}"
                )
            else:
                approval_id_lines[record_id] = line_number

    scoped = [
        record
        for record in records
        if record.get("gate") == gate
        and record.get("scope_sha256") == scope_sha256
    ]
    if len(scoped) > 1:
        findings.append(
            "conflicting or duplicate approval events for "
            f"gate {gate} and scope {scope_sha256}"
        )

    if approval_id is None:
        candidates = scoped
    else:
        candidates = [
            record
            for record in records
            if record.get("approval_id") == approval_id
        ]
    candidate = candidates[0] if len(candidates) == 1 else None
    if candidate is not None:
        findings.extend(
            approval_record_findings(
                candidate,
                require_decided_at=True,
                context=f"approval event {candidate.get('approval_id')}",
            )
        )
        if candidate.get("gate") != gate:
            findings.append(
                f"approval event {candidate.get('approval_id')} gate mismatch"
            )
        if candidate.get("scope_sha256") != scope_sha256:
            findings.append(
                f"approval event {candidate.get('approval_id')} scope mismatch"
            )
    if findings:
        return None, findings
    if (
        candidate is not None
        and candidate.get("decision") == "approved"
        and candidate.get("decided_by") == "user"
    ):
        return candidate, []
    return None, []


def _load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON object required: {path}")
    return payload


def _recovery_anchor_findings(
    root: Path, baseline_manifest: dict[str, Any]
) -> list[str]:
    findings: list[str] = []
    baseline_path = root.resolve() / RECOVERY_BASELINE_REL
    try:
        frozen_baseline = _load_json_object(baseline_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        findings.append(f"original G2 baseline cannot be read: {exc}")
        frozen_baseline = {}
    else:
        if file_sha256(baseline_path) != RECOVERY_BASELINE_MANIFEST_SHA256:
            findings.append("original G2 baseline file digest mismatch")
        if frozen_baseline != baseline_manifest:
            findings.append("supplied content baseline differs from original G2 baseline")
    if baseline_manifest.get("content_baseline_frozen") is not True:
        findings.append("original G2 baseline is not marked frozen")
    if (
        baseline_manifest.get("tool_manifest_sha256")
        != RECOVERY_BASE_TOOL_MANIFEST_SHA256
    ):
        findings.append("original G2 baseline tool digest mismatch")
    if (
        baseline_manifest.get("source_manifest_sha256")
        != RECOVERY_SOURCE_MANIFEST_SHA256
    ):
        findings.append("original G2 baseline source digest mismatch")

    bootstrap_path = root.resolve() / RECOVERY_BOOTSTRAP_REL
    try:
        bootstrap = _load_json_object(bootstrap_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        findings.append(f"fixed tool recovery bootstrap cannot be read: {exc}")
        bootstrap = {}
    else:
        if file_sha256(bootstrap_path) != RECOVERY_BOOTSTRAP_SHA256:
            findings.append("fixed tool recovery bootstrap digest mismatch")
    if bootstrap:
        base_state = bootstrap.get("base_state", {})
        bootstrap_authorization = bootstrap.get("authorization", {})
        if bootstrap.get("recovery_id") != RECOVERY_ID:
            findings.append("fixed tool recovery bootstrap id mismatch")
        if tuple(bootstrap.get("allowed_recovery_paths", ())) != RECOVERY_ALLOWED_PATHS:
            findings.append("fixed tool recovery bootstrap whitelist mismatch")
        if (
            base_state.get("tool_manifest_sha256")
            != RECOVERY_BASE_TOOL_MANIFEST_SHA256
        ):
            findings.append("fixed bootstrap tool digest mismatch")
        if (
            base_state.get("source_manifest_sha256")
            != RECOVERY_SOURCE_MANIFEST_SHA256
        ):
            findings.append("fixed bootstrap source digest mismatch")
        if (
            not isinstance(bootstrap_authorization, dict)
            or bootstrap_authorization.get("approval_id")
            != RECOVERY_IMPLEMENTATION_AUTHORIZATION_ID
        ):
            findings.append("fixed bootstrap implementation authorization mismatch")
    return findings


def _recovery_anchor_check(
    root: Path, baseline_manifest: dict[str, Any]
) -> CheckResult:
    findings = _recovery_anchor_findings(root, baseline_manifest)
    return CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "original G2 recovery anchor verification",
        tuple(findings),
        {
            "baseline_manifest_sha256": RECOVERY_BASELINE_MANIFEST_SHA256,
            "base_tool_manifest_sha256": RECOVERY_BASE_TOOL_MANIFEST_SHA256,
            "source_manifest_sha256": RECOVERY_SOURCE_MANIFEST_SHA256,
            "bootstrap_sha256": RECOVERY_BOOTSTRAP_SHA256,
        },
    )


def _snapshot_findings(
    name: str, expected: Any, actual: dict[str, Any]
) -> list[str]:
    if not isinstance(expected, dict):
        return [f"tool recovery {name} is missing or invalid"]
    findings: list[str] = []
    for field in (
        "file_count",
        "file_digest",
        "missing_path_count",
        "git_status_count",
        "git_status_digest",
    ):
        if expected.get(field) != actual.get(field):
            findings.append(f"tool recovery {name} mismatch: {field}")
    return findings


def _git_status_line_is_excluded(line: str, rules: Iterable[str]) -> bool:
    if len(line) < 4:
        return False
    paths = [
        canonical_path(value) for value in line[3:].split(" -> ")
    ]
    return bool(paths) and all(path_matches(path, rules) for path in paths)


def _expected_recovery_files(root: Path) -> set[str]:
    root = root.resolve()
    expected: set[str] = set()
    for rule in RECOVERY_ALLOWED_PATHS:
        if rule in RECOVERY_DYNAMIC_PATHS:
            continue
        candidate = root / canonical_path(rule)
        if rule.endswith("/"):
            if candidate.is_dir():
                expected.update(
                    canonical_path(path.relative_to(root))
                    for path in candidate.rglob("*")
                    if path.is_file() and "__pycache__" not in path.parts
                )
        elif candidate.is_file():
            expected.add(canonical_path(rule))
    return expected


def _recovery_file_findings(root: Path, records: Any) -> list[str]:
    if not isinstance(records, list):
        return ["tool recovery changed_files must be a list"]
    findings: list[str] = []
    actual_records: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict):
            findings.append("tool recovery changed_files entry must be an object")
            continue
        relative = canonical_path(str(record.get("path", "")))
        if not relative:
            findings.append("tool recovery changed_files entry has no path")
            continue
        if relative in actual_records:
            findings.append(f"tool recovery duplicate changed file: {relative}")
            continue
        actual_records[relative] = record
    expected_paths = _expected_recovery_files(root)
    if set(actual_records) != expected_paths:
        for relative in sorted(expected_paths - set(actual_records)):
            findings.append(f"tool recovery file not frozen: {relative}")
        for relative in sorted(set(actual_records) - expected_paths):
            findings.append(f"tool recovery unexpected changed file: {relative}")
    if list(actual_records) != sorted(actual_records):
        findings.append("tool recovery changed_files must be sorted by path")
    for relative, record in sorted(actual_records.items()):
        path = root.resolve() / relative
        if not path.is_file():
            findings.append(f"tool recovery changed file missing: {relative}")
        elif file_sha256(path) != str(record.get("sha256", "")).lower():
            findings.append(f"tool recovery changed file digest mismatch: {relative}")
    return findings


def _approval_findings(
    root: Path, recovery: dict[str, Any], scope_sha256: str
) -> list[str]:
    findings: list[str] = []
    if recovery.get("approval_scope_sha256") != scope_sha256:
        findings.append("tool recovery approval scope digest is invalid")
    approval_id = recovery.get("approval_id")
    if not isinstance(approval_id, str) or not approval_id:
        return findings + ["tool recovery renewed G1 approval id is missing"]
    if approval_id == RECOVERY_IMPLEMENTATION_AUTHORIZATION_ID:
        return findings + [
            "tool recovery renewed G1 approval must be distinct from implementation authorization"
        ]
    approvals_path = (
        root.resolve()
        / "governance"
        / "rd-standards-rebuild"
        / "approvals.jsonl"
    )
    try:
        records = []
        for number, line in enumerate(
            approvals_path.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"approval line {number} must be an object")
            records.append(record)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return findings + [f"tool recovery approvals cannot be read: {exc}"]
    approval, approval_record_errors = match_approval_event(
        records,
        gate="G1R",
        scope_sha256=scope_sha256,
        approval_id=approval_id,
    )
    findings.extend(approval_record_errors)
    if approval is None:
        findings.append("tool recovery renewed user G1 approval is missing")
    return findings


def validate_tool_recovery(
    root: Path,
    baseline_manifest: dict[str, Any],
    tool_manifest: dict[str, Any],
    content_allowed: Iterable[str],
) -> CheckResult:
    root = root.resolve()
    manifest_path = root / RECOVERY_MANIFEST_REL
    try:
        recovery = _load_json_object(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return CheckResult(
            ResultStatus.BLOCKED,
            "tool recovery validation",
            (f"tool recovery manifest cannot be read: {exc}",),
        )
    findings = _recovery_anchor_findings(root, baseline_manifest)
    if recovery.get("recovery_id") != RECOVERY_ID:
        findings.append("tool recovery id does not match the fixed recovery")
    if recovery.get("status") != "approved":
        findings.append("tool recovery status is not approved")
    authorization = recovery.get("authorization")
    if (
        not isinstance(authorization, dict)
        or authorization.get("approval_id")
        != RECOVERY_IMPLEMENTATION_AUTHORIZATION_ID
    ):
        findings.append("tool recovery implementation authorization is not bound")
    if tuple(recovery.get("allowed_recovery_paths", ())) != RECOVERY_ALLOWED_PATHS:
        findings.append("tool recovery whitelist differs from the fixed whitelist")
    base_digest = RECOVERY_BASE_TOOL_MANIFEST_SHA256
    replacement_digest = tool_manifest.get("aggregate_sha256")
    source_digest = RECOVERY_SOURCE_MANIFEST_SHA256
    if recovery.get("base_tool_manifest_sha256") != base_digest:
        findings.append("tool recovery base tool digest mismatch")
    if recovery.get("replacement_tool_manifest_sha256") != replacement_digest:
        findings.append("tool recovery replacement tool digest mismatch")
    if recovery.get("source_manifest_sha256") != source_digest:
        findings.append("tool recovery source digest mismatch")

    bootstrap_ref = recovery.get("bootstrap")
    if not isinstance(bootstrap_ref, dict):
        findings.append("tool recovery bootstrap reference is missing")
        bootstrap = {}
    else:
        bootstrap_path = canonical_path(str(bootstrap_ref.get("path", "")))
        if bootstrap_path != RECOVERY_BOOTSTRAP_REL:
            findings.append("tool recovery bootstrap path mismatch")
        resolved_bootstrap = root / bootstrap_path
        try:
            bootstrap = _load_json_object(resolved_bootstrap)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            findings.append(f"tool recovery bootstrap cannot be read: {exc}")
            bootstrap = {}
        else:
            if file_sha256(resolved_bootstrap) != str(
                bootstrap_ref.get("sha256", "")
            ).lower():
                findings.append("tool recovery bootstrap digest mismatch")
    if bootstrap:
        if bootstrap.get("recovery_id") != RECOVERY_ID:
            findings.append("tool recovery bootstrap id mismatch")
        if tuple(bootstrap.get("allowed_recovery_paths", ())) != RECOVERY_ALLOWED_PATHS:
            findings.append("tool recovery bootstrap whitelist mismatch")
        base_state = bootstrap.get("base_state", {})
        if base_state.get("tool_manifest_sha256") != base_digest:
            findings.append("tool recovery bootstrap base tool digest mismatch")
        if base_state.get("source_manifest_sha256") != source_digest:
            findings.append("tool recovery bootstrap source digest mismatch")
        if bootstrap.get("protected_workspace_snapshot") != recovery.get(
            "protected_workspace_snapshot"
        ):
            findings.append("tool recovery protected snapshot record mismatch")

    failure = recovery.get("failure")
    if not isinstance(failure, dict):
        findings.append("tool recovery failure report reference is missing")
    else:
        failure_path = canonical_path(str(failure.get("path", "")))
        bootstrap_failure = (
            bootstrap.get("base_state", {}).get("failure_report")
            if bootstrap
            else None
        )
        if (
            failure_path != RECOVERY_FAILURE_REL
            or bootstrap_failure != RECOVERY_FAILURE_REL
        ):
            findings.append("tool recovery failure report path mismatch")
        resolved_failure = root / failure_path
        if not resolved_failure.is_file():
            findings.append("tool recovery failure report is missing")
        elif file_sha256(resolved_failure) != str(
            failure.get("sha256", "")
        ).lower():
            findings.append("tool recovery failure report digest mismatch")

    try:
        current_protected = recovery_workspace_snapshot(root, RECOVERY_ALLOWED_PATHS)
        durable_exclusions = tuple(dict.fromkeys(
            tuple(content_allowed) + RECOVERY_ALLOWED_PATHS
        ))
        current_durable = recovery_workspace_snapshot(root, durable_exclusions)
        current_frozen = recovery_workspace_snapshot(
            root, RECOVERY_FROZEN_EXCLUSIONS
        )
    except (OSError, RuntimeError, UnicodeError) as exc:
        findings.append(f"tool recovery workspace snapshot failed: {exc}")
        current_protected = {}
        current_durable = {}
        current_frozen = {}
    run_state_path = (
        root / "governance" / "rd-standards-rebuild" / "run-state.json"
    )
    try:
        run_state = _load_json_object(run_state_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        findings.append(f"tool recovery run state cannot be read: {exc}")
        current_state = None
    else:
        current_state = run_state.get("current_state")
        expected_gate = RECOVERY_GATE_BY_STATE.get(str(current_state))
        if expected_gate is None:
            findings.append(f"tool recovery is invalid at state: {current_state}")
        elif run_state.get("last_passed_gate") != expected_gate:
            findings.append(
                "tool recovery state/gate mismatch: "
                f"{current_state} requires {expected_gate}, got "
                f"{run_state.get('last_passed_gate')}"
            )
    if current_state == "audit_ready" and current_protected:
        findings.extend(
            _snapshot_findings(
                "protected workspace snapshot",
                recovery.get("protected_workspace_snapshot"),
                current_protected,
            )
        )
    if current_durable:
        findings.extend(
            _snapshot_findings(
                "durable workspace snapshot",
                recovery.get("durable_workspace_snapshot"),
                current_durable,
            )
        )
    if current_frozen:
        findings.extend(
            _snapshot_findings(
                "frozen workspace snapshot",
                recovery.get("frozen_workspace_snapshot"),
                current_frozen,
            )
        )
    findings.extend(_recovery_file_findings(root, recovery.get("changed_files")))
    verification = recovery.get("verification")
    if not isinstance(verification, dict) or verification.get("status") != "PASS":
        findings.append("tool recovery verification is not PASS")
        verification_checks = {}
    else:
        verification_checks = verification.get("checks")
        if not isinstance(verification_checks, dict):
            findings.append("tool recovery verification checks are missing")
            verification_checks = {}
    for name in RECOVERY_REQUIRED_CHECKS:
        check = verification_checks.get(name)
        if (
            not isinstance(check, dict)
            or check.get("status") != "PASS"
            or check.get("exit_code") != 0
        ):
            findings.append(f"tool recovery verification check is not PASS: {name}")
    producer_self_check = recovery.get("producer_self_check")
    producer_reviewer_value = (
        producer_self_check.get("reviewer")
        if isinstance(producer_self_check, dict)
        else None
    )
    producer_reviewer = (
        producer_reviewer_value.strip().casefold()
        if isinstance(producer_reviewer_value, str)
        else ""
    )
    if (
        not isinstance(producer_self_check, dict)
        or producer_self_check.get("status") != "PASS"
        or not producer_reviewer
        or producer_self_check.get("candidate_tool_manifest_sha256")
        != replacement_digest
    ):
        findings.append("tool recovery producer self-check is not bound and PASS")
    independent_review = recovery.get("independent_review")
    review_findings = (
        independent_review.get("findings", {})
        if isinstance(independent_review, dict)
        else {}
    )
    independent_reviewer_value = (
        independent_review.get("reviewer")
        if isinstance(independent_review, dict)
        else None
    )
    independent_reviewer = (
        independent_reviewer_value.strip().casefold()
        if isinstance(independent_reviewer_value, str)
        else ""
    )
    if (
        not isinstance(independent_review, dict)
        or independent_review.get("decision") != "approved"
        or not independent_reviewer
        or independent_review.get("read_only") is not True
        or independent_review.get("candidate_tool_manifest_sha256")
        != replacement_digest
        or not isinstance(review_findings, dict)
        or any(
            type(review_findings.get(level)) is not int
            or review_findings.get(level) != 0
            for level in ("critical", "important", "minor")
        )
    ):
        findings.append(
            "tool recovery independent review is not bound, read-only, zero-finding and approved"
        )
    if (
        producer_reviewer
        and independent_reviewer
        and producer_reviewer == independent_reviewer
    ):
        findings.append(
            "tool recovery producer and independent reviewer must be distinct"
        )
    scope_sha256 = recovery_scope_digest(recovery)
    findings.extend(_approval_findings(root, recovery, scope_sha256))
    return CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "tool recovery validation",
        tuple(findings),
        {
            "recovery_id": RECOVERY_ID,
            "base_tool_manifest_sha256": base_digest,
            "replacement_tool_manifest_sha256": replacement_digest,
            "source_manifest_sha256": source_digest,
            "approval_scope_sha256": scope_sha256,
        },
    )


def check_scope(
    root: Path,
    policy: dict[str, Any],
    baseline_manifest: dict[str, Any],
    phase: str,
) -> CheckResult:
    allowed_by_phase = policy.get("allowed_write_roots_by_phase", {})
    if phase not in allowed_by_phase:
        return CheckResult(
            ResultStatus.BLOCKED,
            "scope check blocked",
            (f"unknown phase: {phase}",),
        )
    allowed = list(allowed_by_phase[phase])
    content_results: list[CheckResult] = []
    if phase == "content":
        anchor_result = _recovery_anchor_check(root, baseline_manifest)
        content_results.append(anchor_result)
        manifest_path = (
            root.resolve()
            / "governance"
            / "rd-standards-rebuild"
            / "tool-manifest.json"
        )
        try:
            tool_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if not isinstance(tool_manifest, dict):
                raise ValueError("tool manifest must be an object")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            tool_manifest = {}
            tool_result = CheckResult(
                ResultStatus.BLOCKED,
                "frozen tool verification",
                (f"frozen tool manifest cannot be read: {exc}",),
            )
        else:
            tool_result = verify_tool_manifest(root, tool_manifest)
        content_results.append(tool_result)
        expected_tool_digest = RECOVERY_BASE_TOOL_MANIFEST_SHA256
        actual_tool_digest = tool_manifest.get("aggregate_sha256", "")
        recovery_result: CheckResult | None = None
        recovery_accepted = False
        if (
            expected_tool_digest
            and actual_tool_digest != expected_tool_digest
            and tool_result.status == ResultStatus.PASS
        ):
            recovery_result = validate_tool_recovery(
                root, baseline_manifest, tool_manifest, allowed
            )
            recovery_accepted = recovery_result.status == ResultStatus.PASS
            if recovery_accepted:
                allowed.extend(RECOVERY_ALLOWED_PATHS)
        if expected_tool_digest:
            identity_findings: list[str] = []
            if anchor_result.status != ResultStatus.PASS:
                identity_findings.append(
                    "original G2 content baseline anchor is invalid"
                )
            if actual_tool_digest != expected_tool_digest and not recovery_accepted:
                identity_findings.append(
                    "frozen tool manifest changed from the content baseline"
                )
            content_results.append(
                CheckResult(
                    ResultStatus.BLOCKED
                    if identity_findings
                    else ResultStatus.PASS,
                    "frozen tool manifest identity verification",
                    tuple(identity_findings),
                    {
                        "expected_tool_manifest_sha256": expected_tool_digest,
                        "actual_tool_manifest_sha256": actual_tool_digest,
                        "recovery_id": RECOVERY_ID if recovery_accepted else None,
                    },
                )
            )
        if recovery_result is not None:
            content_results.append(recovery_result)
    source_result = verify_source_entries(
        root,
        baseline_manifest.get("protected_sources", []),
        policy.get("source_roots", []),
    )
    expected_entries = [
        entry
        for entry in baseline_manifest.get("existing_workspace", {}).get(
            "files", []
        )
        if not path_matches(canonical_path(str(entry.get("path", ""))), allowed)
    ]
    expected = {
        canonical_path(str(entry["path"])): entry for entry in expected_entries
    }
    current_entries = capture_workspace_entries(root, allowed)
    current = {entry["path"]: entry for entry in current_entries}
    findings: list[str] = []
    for relative in sorted(set(expected) | set(current)):
        before = expected.get(relative)
        after = current.get(relative)
        if before is None:
            findings.append(f"unauthorized new path: {relative}")
            continue
        if after is None:
            findings.append(f"existing workspace path missing: {relative}")
            continue
        for field in ("exists", "size", "sha256"):
            if before.get(field) != after.get(field):
                findings.append(f"existing workspace path changed: {relative}")
                break
    workspace_result = CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "workspace scope verification",
        tuple(findings),
        {
            "baseline_file_count": len(expected),
            "current_file_count": len(current),
            "allowed_rules": list(allowed),
        },
    )
    expected_git_status = baseline_manifest.get("existing_workspace", {}).get(
        "git_status_lines"
    )
    status_result: CheckResult | None = None
    if isinstance(expected_git_status, list):
        expected_git_status = [
            line
            for line in expected_git_status
            if not _git_status_line_is_excluded(line, allowed)
        ]
        current_git_status = capture_git_status_lines(root, allowed)
        status_findings = [
            f"git status baseline entry changed or missing: {line}"
            for line in sorted(set(expected_git_status) - set(current_git_status))
        ]
        status_findings.extend(
            f"git status has unauthorized delta: {line}"
            for line in sorted(set(current_git_status) - set(expected_git_status))
        )
        status_result = CheckResult(
            ResultStatus.BLOCKED if status_findings else ResultStatus.PASS,
            "workspace git status verification",
            tuple(status_findings),
            {
                "baseline_status_count": len(expected_git_status),
                "current_status_count": len(current_git_status),
            },
        )
    results = [source_result, workspace_result]
    if status_result is not None:
        results.append(status_result)
    results.extend(content_results)
    return combine_results(results, "scope check")
