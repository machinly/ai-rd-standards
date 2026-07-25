#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rd_rebuild_core.baseline import create_baseline, verify_source_entries
from rd_rebuild_core.coverage import rewrite_check
from rd_rebuild_core.drafts import draft_check
from rd_rebuild_core.gates import (
    STATE_SEQUENCE,
    gate_checks_for_target,
    status_check,
    transition_gate,
    verify_all_applicable,
)
from rd_rebuild_core.model import CheckResult, ResultStatus, read_json
from rd_rebuild_core.principles import principle_check
from rd_rebuild_core.records import (
    BATCH_ROOTS,
    classification_check,
    inventory_check,
    rule_check,
    segment_check,
)
from rd_rebuild_core.report import build_report
from rd_rebuild_core.scope import check_scope


POLICY_REL = Path("governance/rd-standards-rebuild/policy.json")
BASELINE_REL = Path("governance/rd-standards-rebuild/baseline-manifest.json")
RUN_STATE_REL = Path("governance/rd-standards-rebuild/run-state.json")


def emit(result: CheckResult) -> int:
    print(f"STATUS={result.status.value}")
    print(f"SUMMARY={result.summary}")
    for finding in result.findings:
        print(f"FINDING={finding}")
    print("EVIDENCE=" + json.dumps(result.evidence, ensure_ascii=False, sort_keys=True))
    return result.exit_code


def add_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=".", help="Repository root")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Guardrails for the approved R&D standards rebuild plan."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    baseline_create = subparsers.add_parser("baseline-create")
    add_root(baseline_create)
    baseline_create.add_argument("--dry-run", action="store_true")

    baseline_verify = subparsers.add_parser("baseline-verify")
    add_root(baseline_verify)

    scope_check = subparsers.add_parser("scope-check")
    add_root(scope_check)
    scope_check.add_argument("--phase", choices=("tooling", "content"), required=True)

    inventory = subparsers.add_parser("inventory-check")
    add_root(inventory)
    inventory.add_argument("--batch", choices=tuple(BATCH_ROOTS))

    segments = subparsers.add_parser("segment-check")
    add_root(segments)
    segments.add_argument("--batch", choices=tuple(BATCH_ROOTS))

    rules = subparsers.add_parser("rule-check")
    add_root(rules)
    rules.add_argument("--batch", choices=tuple(BATCH_ROOTS))

    for name in (
        "classification-check",
        "rewrite-check",
        "principle-check",
        "draft-check",
        "verify-all",
        "status",
    ):
        command = subparsers.add_parser(name)
        add_root(command)

    gate = subparsers.add_parser("gate")
    add_root(gate)
    gate.add_argument(
        "--target",
        required=True,
        choices=(
            "tooling_ready",
            "sources_frozen",
            "sources_reviewed",
            "rules_classified",
            "rules_rewritten",
            "principles_derived",
            "audit_ready",
            "awaiting_user_review",
            "approved_for_migration_design",
        ),
    )
    gate.add_argument("--dry-run", action="store_true")

    report = subparsers.add_parser("report-build")
    add_root(report)
    report.add_argument("--dry-run", action="store_true")
    return parser


def run(args: argparse.Namespace) -> CheckResult:
    root = Path(args.root).resolve()
    policy = read_json(root / POLICY_REL)
    baseline_path = root / BASELINE_REL
    if args.command == "baseline-create":
        run_state = read_json(root / RUN_STATE_REL)
        current_state = run_state.get("current_state")
        if current_state not in STATE_SEQUENCE:
            raise ValueError(f"unknown current_state: {current_state}")
        kind = (
            "tooling-bootstrap"
            if current_state == "planned"
            else "content-frozen"
        )
        return create_baseline(
            root,
            policy,
            baseline_path,
            dry_run=args.dry_run,
            kind=kind,
        )
    baseline = read_json(baseline_path)
    if args.command == "baseline-verify":
        return verify_source_entries(
            root,
            baseline.get("protected_sources", []),
            policy.get("source_roots", []),
        )
    if args.command == "scope-check":
        return check_scope(root, policy, baseline, args.phase)
    if args.command == "inventory-check":
        return inventory_check(root, args.batch)
    if args.command == "segment-check":
        return segment_check(root, args.batch)
    if args.command == "rule-check":
        return rule_check(root, args.batch)
    if args.command == "classification-check":
        return classification_check(root)
    if args.command == "rewrite-check":
        return rewrite_check(root, policy)
    if args.command == "principle-check":
        return principle_check(root, policy)
    if args.command == "draft-check":
        return draft_check(root, policy)
    if args.command == "gate":
        return transition_gate(
            root,
            args.target,
            gate_checks_for_target(root, args.target),
            dry_run=args.dry_run,
        )
    if args.command == "report-build":
        return build_report(root, dry_run=args.dry_run)
    if args.command == "verify-all":
        return verify_all_applicable(root)
    if args.command == "status":
        return status_check(root)
    raise ValueError(f"unsupported command: {args.command}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return emit(run(args))
    except Exception as exc:  # CLI boundary converts unknown failures to TOOL_ERROR.
        return emit(
            CheckResult(
                ResultStatus.TOOL_ERROR,
                "tool error",
                (f"{type(exc).__name__}: {exc}",),
            )
        )


if __name__ == "__main__":
    sys.exit(main())
