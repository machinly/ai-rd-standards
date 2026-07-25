#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable


SCHEMA_REL = "experiments/rd-pilot-record.schema.json"
RECORDS_REL = "experiments/rd-standard-pilot.jsonl"
ROUTES = {"A", "B"}
RISK_PATHS = {"Quick", "Standard", "High-risk"}
TASK_TYPES = {
    "docs",
    "code",
    "ai",
    "data",
    "release",
    "ops",
    "auth",
    "frontend",
    "backend",
    "other",
}
STATUSES = {
    "planned",
    "in-progress",
    "self-check-complete",
    "independent-review",
    "changes-requested",
    "completed",
    "terminated",
}
CORE_METRICS = (
    "startup_minutes",
    "context_amount",
    "human_interruptions",
    "human_interruption_minutes",
    "rework_count",
    "process_minutes",
    "total_minutes",
    "tool_calls",
    "failed_retries",
    "total_tokens",
    "artifacts_created",
)
NUMERIC_FIELDS = CORE_METRICS + ("token_cost_usd",)
INTEGER_FIELDS = {
    "human_interruptions",
    "rework_count",
    "tool_calls",
    "failed_retries",
    "total_tokens",
    "artifacts_created",
}
CONTEXT_UNITS = {"lines", "tokens", "bytes", "unknown"}
EVIDENCE_LEVELS = {
    "unit",
    "component",
    "host-integration",
    "dependency-container",
    "complete-local-integration",
    "browser-e2e",
    "provider-sandbox",
    "production-observation",
    "manual",
}
VERIFICATION_RESULTS = {"pass", "fail", "skipped", "not-applicable"}


def mean(values: list[float]) -> float:
    return statistics.fmean(values)


def paired_ratio(
    records: list[dict[str, Any]], extractor: Callable[[dict[str, Any]], float]
) -> tuple[float | None, int]:
    groups: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: {"A": [], "B": []}
    )
    for record in records:
        groups[record["comparison_group"]][record["route"]].append(extractor(record))
    paired = [routes for routes in groups.values() if routes["A"] and routes["B"]]
    if not paired:
        return None, 0
    baseline = sum(mean(routes["A"]) for routes in paired)
    candidate = sum(mean(routes["B"]) for routes in paired)
    if baseline == 0:
        return (1.0 if candidate == 0 else None), len(paired)
    return candidate / baseline, len(paired)


def validate_pilot_records(root: Path) -> dict[str, Any]:
    root = root.resolve()
    schema_path = root / SCHEMA_REL
    records_path = root / RECORDS_REL
    errors: list[str] = []
    warnings: list[str] = []

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        required = set(schema["required"])
        allowed = set(schema["properties"])
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError, KeyError) as exc:
        return {
            "format_valid": False,
            "records_present": records_path.is_file(),
            "pilot_effect_verified": False,
            "errors": [f"invalid or missing pilot schema: {exc}"],
            "warnings": [],
        }

    if not records_path.is_file():
        return {
            "format_valid": True,
            "records_present": False,
            "record_count": 0,
            "completed_count": 0,
            "eligible_count": 0,
            "pilot_effect_verified": False,
            "errors": [],
            "warnings": [
                f"{RECORDS_REL} is absent; pilot has no measurable completed records"
            ],
        }

    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for number, line in enumerate(records_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {number}: invalid JSON: {exc}")
            continue
        if not isinstance(record, dict):
            errors.append(f"line {number}: record must be an object")
            continue
        missing = sorted(required - set(record))
        if missing:
            errors.append(f"line {number}: missing fields: {', '.join(missing)}")
        extra = sorted(set(record) - allowed)
        if extra:
            errors.append(f"line {number}: unexpected fields: {', '.join(extra)}")
        task_id = record.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            errors.append(f"line {number}: task_id must be non-empty")
        elif task_id in seen:
            errors.append(f"line {number}: duplicate task_id: {task_id}")
        else:
            seen.add(task_id)
        if record.get("route") not in ROUTES:
            errors.append(f"line {number}: route must be A or B")
        if record.get("risk_path") not in RISK_PATHS:
            errors.append(f"line {number}: invalid risk_path")
        if record.get("status") not in STATUSES:
            errors.append(f"line {number}: invalid status")
        openspec = record.get("openspec")
        openspec_required = {"used", "change_id", "skip_approval", "reason"}
        if not isinstance(openspec, dict) or set(openspec) != openspec_required:
            errors.append(f"line {number}: openspec fields do not match schema")
        else:
            used = openspec.get("used")
            change_id = openspec.get("change_id")
            skip_approval = openspec.get("skip_approval")
            reason = openspec.get("reason")
            if not isinstance(used, bool) or not isinstance(reason, str) or not reason:
                errors.append(f"line {number}: openspec value is invalid")
            if change_id is not None and not isinstance(change_id, str):
                errors.append(f"line {number}: openspec.change_id must be string or null")
            if skip_approval is not None and not isinstance(skip_approval, str):
                errors.append(f"line {number}: openspec.skip_approval must be string or null")
            if used and not change_id:
                errors.append(f"line {number}: openspec.change_id is required when used=true")
            if (
                record.get("risk_path") in {"Standard", "High-risk"}
                and not used
                and not skip_approval
            ):
                warnings.append(
                    f"line {number}: Standard/High-risk without OpenSpec or explicit skip approval is retained as negative evidence but is ineligible"
                )
        if record.get("task_type") not in TASK_TYPES:
            errors.append(f"line {number}: invalid task_type")
        if record.get("high_risk_miss") not in {
            "no",
            "yes-producer-stage",
            "yes-reviewer-stage",
            "unknown",
        }:
            errors.append(f"line {number}: invalid high_risk_miss")
        if record.get("context_unit") not in CONTEXT_UNITS:
            errors.append(f"line {number}: invalid context_unit")
        for field in (
            "project_id",
            "comparison_group",
            "source_evidence",
            "toolchain_fingerprint",
            "started_at",
        ):
            if not isinstance(record.get(field), str) or not record[field]:
                errors.append(f"line {number}: {field} must be a non-empty string")
        if not isinstance(record.get("notes"), str):
            errors.append(f"line {number}: notes must be a string")
        for field in ("started_at", "finished_at"):
            value = record.get(field)
            if value is None and field == "finished_at":
                continue
            if not isinstance(value, str):
                errors.append(f"line {number}: {field} must be an ISO-8601 string or null")
                continue
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"line {number}: {field} is not valid ISO-8601")
        for field in NUMERIC_FIELDS:
            value = record.get(field)
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                errors.append(f"line {number}: {field} must be a non-negative number or null")
            elif field in INTEGER_FIELDS and not isinstance(value, int):
                errors.append(f"line {number}: {field} must be an integer or null")
        if record.get("first_pass") is not None and not isinstance(
            record.get("first_pass"), bool
        ):
            errors.append(f"line {number}: first_pass must be boolean or null")
        gaps = record.get("metrics_gaps")
        if not isinstance(gaps, list) or not all(isinstance(item, str) for item in gaps):
            errors.append(f"line {number}: metrics_gaps must be a string list")
        verification = record.get("verification")
        if not isinstance(verification, list):
            errors.append(f"line {number}: verification must be a list")
        else:
            verification_required = {
                "name",
                "command",
                "environment",
                "evidence_level",
                "result",
                "covered",
                "not_covered",
            }
            for index, item in enumerate(verification):
                if not isinstance(item, dict):
                    errors.append(
                        f"line {number}: verification[{index}] must be an object"
                    )
                    continue
                if set(item) != verification_required:
                    errors.append(
                        f"line {number}: verification[{index}] fields do not match schema"
                    )
                if item.get("evidence_level") not in EVIDENCE_LEVELS:
                    errors.append(
                        f"line {number}: verification[{index}] invalid evidence_level"
                    )
                if item.get("result") not in VERIFICATION_RESULTS:
                    errors.append(f"line {number}: verification[{index}] invalid result")
                for field in ("covered", "not_covered"):
                    if not isinstance(item.get(field), list) or not all(
                        isinstance(value, str) for value in item.get(field, [])
                    ):
                        errors.append(
                            f"line {number}: verification[{index}].{field} must be a string list"
                        )
        review = record.get("review")
        if review is not None:
            review_required = {"reviewer", "target", "decision", "findings"}
            if not isinstance(review, dict) or set(review) != review_required:
                errors.append(f"line {number}: review fields do not match schema")
            elif (
                not isinstance(review.get("reviewer"), str)
                or not review.get("reviewer")
                or not isinstance(review.get("target"), str)
                or not review.get("target")
                or review.get("decision")
                not in {"accepted", "changes-requested", "rejected"}
                or not isinstance(review.get("findings"), list)
                or not all(isinstance(value, str) for value in review.get("findings", []))
            ):
                errors.append(f"line {number}: review value is invalid")
        drill = record.get("resume_drill")
        if drill is not None:
            drill_required = {
                "delay_days",
                "resume_minutes",
                "success",
                "context_amount",
                "context_unit",
            }
            if not isinstance(drill, dict) or set(drill) != drill_required:
                errors.append(f"line {number}: resume_drill fields do not match schema")
            elif (
                isinstance(drill.get("delay_days"), bool)
                or not isinstance(drill.get("delay_days"), (int, float))
                or drill.get("delay_days", -1) < 0
                or isinstance(drill.get("resume_minutes"), bool)
                or not isinstance(drill.get("resume_minutes"), (int, float))
                or drill.get("resume_minutes", -1) < 0
                or not isinstance(drill.get("success"), bool)
                or isinstance(drill.get("context_amount"), bool)
                or not isinstance(drill.get("context_amount"), (int, float))
                or drill.get("context_amount", -1) < 0
                or drill.get("context_unit") not in CONTEXT_UNITS
            ):
                errors.append(f"line {number}: resume_drill value is invalid")
        records.append(record)

    completed = [record for record in records if record.get("status") == "completed"]
    eligible: list[dict[str, Any]] = []
    for record in completed:
        task_id = str(record.get("task_id"))
        if (
            record.get("route") not in ROUTES
            or record.get("risk_path") not in RISK_PATHS
            or record.get("task_type") not in TASK_TYPES
            or not isinstance(record.get("project_id"), str)
            or not record.get("project_id")
            or not isinstance(record.get("comparison_group"), str)
            or not record.get("comparison_group")
            or not isinstance(record.get("source_evidence"), str)
            or not record.get("source_evidence")
            or not isinstance(record.get("toolchain_fingerprint"), str)
            or not record.get("toolchain_fingerprint")
        ):
            warnings.append(f"{task_id}: completed but ineligible; identity fields are invalid")
            continue
        gaps = record.get("metrics_gaps") if isinstance(record.get("metrics_gaps"), list) else []
        missing_metrics = [field for field in CORE_METRICS if record.get(field) is None]
        unexplained = [
            field
            for field in missing_metrics
            if not any(str(gap).startswith(field + ":") for gap in gaps)
        ]
        if unexplained:
            errors.append(
                f"{task_id}: completed record has unexplained metric gaps: {', '.join(unexplained)}"
            )
        if missing_metrics:
            warnings.append(
                f"{task_id}: completed but ineligible for effect comparison; missing {', '.join(missing_metrics)}"
            )
            continue
        invalid_metrics = [
            field
            for field in CORE_METRICS
            if isinstance(record.get(field), bool)
            or not isinstance(record.get(field), (int, float))
            or record[field] < 0
        ]
        if invalid_metrics:
            warnings.append(
                f"{task_id}: completed but ineligible; invalid metrics {', '.join(invalid_metrics)}"
            )
            continue
        if record.get("finished_at") is None or record.get("first_pass") is None:
            warnings.append(
                f"{task_id}: completed but ineligible; finished_at/first_pass is missing"
            )
            continue
        if not isinstance(record.get("verification"), list) or not record["verification"]:
            warnings.append(f"{task_id}: completed but ineligible; verification is empty")
            continue
        if record.get("risk_path") in {"Standard", "High-risk"}:
            openspec = record.get("openspec")
            if not isinstance(openspec, dict) or (
                openspec.get("used") is not True and not openspec.get("skip_approval")
            ):
                warnings.append(
                    f"{task_id}: completed but ineligible; OpenSpec use or explicit skip approval is missing"
                )
                continue
            review = record.get("review")
            if not isinstance(review, dict) or review.get("decision") != "accepted":
                warnings.append(
                    f"{task_id}: completed but ineligible; independent review is not accepted"
                )
                continue
            if not review.get("reviewer") or not review.get("target"):
                warnings.append(
                    f"{task_id}: completed but ineligible; reviewer/target is missing"
                )
                continue
        if record.get("high_risk_miss") == "unknown":
            warnings.append(
                f"{task_id}: completed but ineligible; high_risk_miss is unknown"
            )
            continue
        drill = record.get("resume_drill")
        if drill is not None and (
            not isinstance(drill, dict)
            or isinstance(drill.get("delay_days"), bool)
            or not isinstance(drill.get("delay_days"), (int, float))
            or isinstance(drill.get("resume_minutes"), bool)
            or not isinstance(drill.get("resume_minutes"), (int, float))
            or not isinstance(drill.get("success"), bool)
        ):
            warnings.append(
                f"{task_id}: completed but ineligible; resume_drill is malformed"
            )
            continue
        eligible.append(record)

    route_counts = Counter(record.get("route") for record in eligible)
    risk_counts = Counter(record.get("risk_path") for record in eligible)
    type_counts = Counter(record.get("task_type") for record in eligible)
    projects = {record.get("project_id") for record in eligible}
    paired_groups = {
        group
        for group in {record.get("comparison_group") for record in eligible}
        if {record["route"] for record in eligible if record.get("comparison_group") == group}
        == ROUTES
    }
    resume_groups: set[str] = set()
    for group in paired_groups:
        by_route = {
            route: [
                record
                for record in eligible
                if record.get("comparison_group") == group
                and record.get("route") == route
                and isinstance(record.get("resume_drill"), dict)
                and record["resume_drill"].get("delay_days", 0) >= 7
                and record["resume_drill"].get("success") is True
            ]
            for route in ROUTES
        }
        if by_route["A"] and by_route["B"]:
            resume_groups.add(str(group))

    attention_ratio, attention_pairs = paired_ratio(
        eligible,
        lambda record: float(record["human_interruption_minutes"])
        + (
            float(record["resume_drill"]["resume_minutes"])
            if isinstance(record.get("resume_drill"), dict)
            else 0.0
        ),
    )
    total_time_ratio, _ = paired_ratio(
        eligible, lambda record: float(record["total_minutes"])
    )
    rework_ratio, _ = paired_ratio(
        eligible, lambda record: float(record["rework_count"])
    )
    interruption_ratio, _ = paired_ratio(
        eligible, lambda record: float(record["human_interruptions"])
    )
    high_risk_misses = Counter(
        record["route"]
        for record in eligible
        if str(record.get("high_risk_miss", "no")).startswith("yes-")
    )

    quota_checks = {
        "eligible_records_at_least_10": len(eligible) >= 10,
        "route_a_at_least_5": route_counts["A"] >= 5,
        "route_b_at_least_5": route_counts["B"] >= 5,
        "projects_at_least_3": len(projects) >= 3,
        "paired_groups_at_least_4": len(paired_groups) >= 4,
        "quick_at_least_3": risk_counts["Quick"] >= 3,
        "standard_at_least_4": risk_counts["Standard"] >= 4,
        "high_risk_at_least_3": risk_counts["High-risk"] >= 3,
        "ai_at_least_2": type_counts["ai"] >= 2,
        "data_release_ops_at_least_2": sum(
            type_counts[item] for item in ("data", "release", "ops")
        )
        >= 2,
        "paired_7_day_resume_groups_at_least_2": len(resume_groups) >= 2,
    }
    effect_checks = {
        "attention_and_recovery_ratio_at_most_0_70": attention_ratio is not None
        and attention_ratio <= 0.70,
        "total_time_ratio_at_most_1_10": total_time_ratio is not None
        and total_time_ratio <= 1.10,
        "rework_ratio_at_most_1_00": rework_ratio is not None and rework_ratio <= 1.0,
        "high_risk_miss_not_increased": high_risk_misses["B"]
        <= high_risk_misses["A"],
    }
    pilot_verified = (
        not errors
        and all(quota_checks.values())
        and all(effect_checks.values())
    )
    return {
        "format_valid": not errors,
        "records_present": True,
        "record_count": len(records),
        "completed_count": len(completed),
        "eligible_count": len(eligible),
        "projects": len(projects),
        "route_counts": dict(route_counts),
        "risk_counts": dict(risk_counts),
        "type_counts": dict(type_counts),
        "paired_groups": len(paired_groups),
        "paired_resume_groups": len(resume_groups),
        "ratios": {
            "attention_and_recovery_b_over_a": attention_ratio,
            "human_interruptions_b_over_a": interruption_ratio,
            "total_minutes_b_over_a": total_time_ratio,
            "rework_b_over_a": rework_ratio,
            "paired_groups_used": attention_pairs,
        },
        "high_risk_misses": dict(high_risk_misses),
        "quota_checks": quota_checks,
        "effect_checks": effect_checks,
        "pilot_effect_verified": pilot_verified,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and aggregate measurable R&D standards pilot records."
    )
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    payload = validate_pilot_records(Path(args.root))
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("PILOT_RECORD_FORMAT=" + ("PASS" if payload["format_valid"] else "FAIL"))
        print(
            "PILOT_EFFECT_VERIFIED="
            + ("PASS" if payload["pilot_effect_verified"] else "PENDING")
        )
        print(
            f"records={payload.get('record_count', 0)} completed={payload.get('completed_count', 0)} "
            f"eligible={payload.get('eligible_count', 0)}"
        )
        for item in payload["errors"]:
            print(f"ERROR: {item}")
        for item in payload["warnings"]:
            print(f"WARNING: {item}")
    return 0 if payload["format_valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
