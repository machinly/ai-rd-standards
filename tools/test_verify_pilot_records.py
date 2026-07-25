#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from verify_pilot_records import RECORDS_REL, SCHEMA_REL, validate_pilot_records


ROOT = Path(__file__).resolve().parents[1]


class PilotRecordVerifierTests(unittest.TestCase):
    def make_root(self, records: list[dict]) -> tempfile.TemporaryDirectory[str]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        schema_target = root / SCHEMA_REL
        schema_target.parent.mkdir(parents=True)
        schema_target.write_text(
            (ROOT / SCHEMA_REL).read_text(encoding="utf-8"), encoding="utf-8"
        )
        records_target = root / RECORDS_REL
        records_target.write_text(
            "\n".join(json.dumps(record, ensure_ascii=False) for record in records)
            + ("\n" if records else ""),
            encoding="utf-8",
        )
        return temp

    def record(
        self,
        index: int,
        route: str,
        risk_path: str,
        task_type: str,
        resume: bool,
    ) -> dict:
        is_a = route == "A"
        review = (
            None
            if risk_path == "Quick"
            else {
                "reviewer": f"reviewer-{index}",
                "target": f"sha256:test-{index}-{route}",
                "decision": "accepted",
                "findings": [],
            }
        )
        return {
            "task_id": f"task-{index}-{route}",
            "project_id": f"project-{((index - 1) % 3) + 1}",
            "comparison_group": f"group-{index}",
            "source_evidence": f"sha256:source-{index}-{route}",
            "toolchain_fingerprint": "codex:test;router:test;go-skill:test",
            "openspec": {
                "used": risk_path != "Quick",
                "change_id": f"pilot-{index}-{route}" if risk_path != "Quick" else None,
                "skip_approval": None,
                "reason": "Standard/High-risk default" if risk_path != "Quick" else "Quick is exempt",
            },
            "route": route,
            "risk_path": risk_path,
            "task_type": task_type,
            "status": "completed",
            "started_at": "2026-07-01T00:00:00Z",
            "finished_at": "2026-07-01T02:00:00Z",
            "startup_minutes": 10 if is_a else 5,
            "context_amount": 1000 if is_a else 500,
            "context_unit": "tokens",
            "human_interruptions": 2 if is_a else 1,
            "human_interruption_minutes": 10 if is_a else 5,
            "rework_count": 2 if is_a else 1,
            "first_pass": True,
            "process_minutes": 20 if is_a else 10,
            "total_minutes": 100 if is_a else 105,
            "tool_calls": 20 if is_a else 15,
            "failed_retries": 2 if is_a else 1,
            "total_tokens": 10000 if is_a else 8000,
            "token_cost_usd": 2.0 if is_a else 1.6,
            "artifacts_created": 4 if is_a else 1,
            "high_risk_miss": "no",
            "verification": [
                {
                    "name": "relevant-check",
                    "command": "test command",
                    "environment": "isolated-test",
                    "evidence_level": "component",
                    "result": "pass",
                    "covered": ["acceptance"],
                    "not_covered": [],
                }
            ],
            "review": review,
            "resume_drill": (
                {
                    "delay_days": 7,
                    "resume_minutes": 10 if is_a else 5,
                    "success": True,
                    "context_amount": 500 if is_a else 250,
                    "context_unit": "tokens",
                }
                if resume
                else None
            ),
            "metrics_gaps": [],
            "notes": "synthetic verifier fixture, not pilot evidence",
        }

    def valid_records(self) -> list[dict]:
        groups = [
            ("Quick", "ai", True),
            ("Standard", "data", True),
            ("High-risk", "auth", False),
            ("Standard", "code", False),
            ("Quick", "docs", False),
            ("High-risk", "release", False),
        ]
        return [
            self.record(index, route, risk_path, task_type, resume)
            for index, (risk_path, task_type, resume) in enumerate(groups, 1)
            for route in ("A", "B")
        ]

    def test_valid_balanced_records_verify_effect(self) -> None:
        temp = self.make_root(self.valid_records())
        self.addCleanup(temp.cleanup)
        result = validate_pilot_records(Path(temp.name))
        self.assertTrue(result["format_valid"], result["errors"])
        self.assertTrue(result["pilot_effect_verified"], result)
        self.assertEqual(result["eligible_count"], 12)
        self.assertEqual(result["projects"], 3)

    def test_effect_regression_stays_pending(self) -> None:
        records = self.valid_records()
        record = next(item for item in records if item["route"] == "B")
        record["total_minutes"] = 200
        record["high_risk_miss"] = "yes-producer-stage"
        temp = self.make_root(records)
        self.addCleanup(temp.cleanup)
        result = validate_pilot_records(Path(temp.name))
        self.assertTrue(result["format_valid"], result["errors"])
        self.assertFalse(result["pilot_effect_verified"])

    def test_missing_required_field_fails_format(self) -> None:
        records = self.valid_records()
        del records[0]["source_evidence"]
        records[0]["unexpected"] = "must fail additionalProperties"
        temp = self.make_root(records)
        self.addCleanup(temp.cleanup)
        result = validate_pilot_records(Path(temp.name))
        self.assertFalse(result["format_valid"])
        self.assertTrue(any("source_evidence" in item for item in result["errors"]))
        self.assertTrue(any("unexpected" in item for item in result["errors"]))

    def test_standard_without_openspec_or_approval_is_negative_evidence(self) -> None:
        records = self.valid_records()
        record = next(item for item in records if item["risk_path"] == "Standard")
        record["openspec"] = {
            "used": False,
            "change_id": None,
            "skip_approval": None,
            "reason": "forgotten",
        }
        temp = self.make_root(records)
        self.addCleanup(temp.cleanup)
        result = validate_pilot_records(Path(temp.name))
        self.assertTrue(result["format_valid"], result["errors"])
        self.assertEqual(result["eligible_count"], 11)
        self.assertTrue(any("ineligible" in item for item in result["warnings"]))

    def test_missing_record_file_is_pending_not_format_failure(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        schema_target = root / SCHEMA_REL
        schema_target.parent.mkdir(parents=True)
        schema_target.write_text(
            (ROOT / SCHEMA_REL).read_text(encoding="utf-8"), encoding="utf-8"
        )
        result = validate_pilot_records(root)
        self.assertTrue(result["format_valid"])
        self.assertFalse(result["pilot_effect_verified"])


if __name__ == "__main__":
    unittest.main()
