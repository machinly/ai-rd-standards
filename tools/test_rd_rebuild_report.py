from __future__ import annotations

import csv
import importlib
import json
import tempfile
import unittest
from pathlib import Path


class ReportBehaviorTests(unittest.TestCase):
    def load_api(self):
        try:
            report = importlib.import_module("rd_rebuild_core.report")
            model = importlib.import_module("rd_rebuild_core.model")
        except ModuleNotFoundError as exc:
            self.fail(f"report API is missing: {exc}")
        return report, model.ResultStatus

    def write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def write_csv(self, path: Path, fields: set[str], rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        ordered = sorted(fields)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=ordered)
            writer.writeheader()
            writer.writerows(rows)

    def make_root(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        governance = root / "governance" / "rd-standards-rebuild"
        self.write_json(
            governance / "policy.json",
            {"schema_version": "1.0", "plan_path": "plan.md"},
        )
        self.write_json(
            governance / "baseline-manifest.json",
            {
                "kind": "tooling-bootstrap",
                "g0": {
                    "source_file_count": 2,
                    "source_manifest_sha256": "source-sha",
                },
                "existing_workspace": {"file_count": 3},
            },
        )
        self.write_json(
            governance / "tool-manifest.json",
            {
                "status": "verified",
                "aggregate_sha256": "tool-sha",
                "files": [{"path": "tools/rd_rebuild.py", "sha256": "x"}],
                "verification": {
                    "unit_tests": {"result": "pass", "count": 10}
                },
            },
        )
        self.write_json(
            governance / "run-state.json",
            {
                "current_state": "planned",
                "last_passed_gate": "G0",
                "blockers": ["G1 user review pending"],
                "next_action": "request G1 review",
            },
        )
        (governance / "approvals.jsonl").write_text(
            json.dumps({"gate": "G0", "decision": "approved"}) + "\n",
            encoding="utf-8",
        )
        return root, governance

    def test_report_dry_run_has_zero_writes(self) -> None:
        report, status = self.load_api()
        root, governance = self.make_root()
        before = sorted(path.relative_to(root) for path in root.rglob("*"))
        result = report.build_report(root, dry_run=True)
        after = sorted(path.relative_to(root) for path in root.rglob("*"))
        self.assertEqual(status.PASS, result.status)
        self.assertEqual(before, after)
        self.assertFalse((governance / "reports" / "g1-fact-report.json").exists())

    def test_missing_required_input_blocks_without_report(self) -> None:
        report, status = self.load_api()
        root, governance = self.make_root()
        (governance / "tool-manifest.json").unlink()
        result = report.build_report(root, dry_run=False)
        self.assertEqual(status.BLOCKED, result.status)
        self.assertFalse((governance / "reports" / "g1-fact-report.json").exists())

    def test_repeated_input_produces_identical_traceable_report(self) -> None:
        report, status = self.load_api()
        root, governance = self.make_root()
        first = report.build_report(root, dry_run=False)
        target = governance / "reports" / "g1-fact-report.json"
        first_bytes = target.read_bytes()
        second = report.build_report(root, dry_run=False)
        second_bytes = target.read_bytes()
        self.assertEqual(status.PASS, first.status)
        self.assertEqual(status.PASS, second.status)
        self.assertEqual(first_bytes, second_bytes)
        payload = json.loads(first_bytes)
        self.assertEqual(2, payload["facts"]["source_file_count"])
        self.assertEqual("baseline-manifest.json:g0.source_file_count", payload["traceability"]["source_file_count"])
        self.assertEqual("pending", payload["g1_review"])
        self.assertIn("independent review", " ".join(payload["limitations"]))
        self.assertIn("content rewrite", " ".join(payload["limitations"]))

    def test_stale_or_non_user_g1_event_is_not_reported_as_approval(self) -> None:
        report, status = self.load_api()
        root, governance = self.make_root()
        events = [
            {
                "gate": "G1",
                "decision": "approved",
                "decided_by": "user",
                "scope_sha256": "stale-scope",
            },
            {
                "gate": "G1",
                "decision": "approved",
                "decided_by": "Codex",
                "scope_sha256": "another-scope",
            },
        ]
        (governance / "approvals.jsonl").write_text(
            "\n".join(json.dumps(item) for item in events) + "\n",
            encoding="utf-8",
        )
        result = report.build_report(root, dry_run=False)
        self.assertEqual(status.PASS, result.status)
        payload = json.loads(
            (governance / "reports" / "g1-fact-report.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("pending", payload["g1_review"])

    def test_content_report_builds_deterministic_traceable_outputs(self) -> None:
        report, status = self.load_api()
        records = importlib.import_module("rd_rebuild_core.records")
        principles = importlib.import_module("rd_rebuild_core.principles")
        root, governance = self.make_root()
        state_path = governance / "run-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["current_state"] = "principles_derived"
        self.write_json(state_path, state)
        review = root / "rebuild-draft" / "review"
        inventory = {
            "source_id": "SRC-001",
            "path": "docs/W0-intake/00-main.md",
            "title": "Synthetic",
            "original_purpose": "Synthetic",
            "applicability": "Synthetic",
            "major_topics": "Synthetic",
            "referenced_sources": "",
            "known_overlaps": "",
            "known_conflicts": "",
            "review_status": "reviewed",
            "reviewed_at": "2026-07-15",
        }
        self.write_csv(
            review / "source-inventory.csv", records.INVENTORY_FIELDS, [inventory]
        )
        segment = {
            "segment_id": "SEG-001",
            "source_id": "SRC-001",
            "source_start_line": "1",
            "source_end_line": "1",
            "segment_kind": "rule-bearing",
            "atomic_rule_ids": "RULE-001",
            "disposition": "rule extracted",
            "notes": "Synthetic",
        }
        self.write_csv(
            review / "source-segments.csv", records.SEGMENT_FIELDS, [segment]
        )
        rule = {
            "rule_id": "RULE-001",
            "source_id": "SRC-001",
            "source_path": "docs/W0-intake/00-main.md",
            "source_start_line": "1",
            "source_end_line": "1",
            "source_text": "Synthetic rule",
            "intent": "Synthetic",
            "applies_when": "Synthetic",
            "subject": "Synthetic",
            "rule_layer": "normative-requirement",
            "candidate_category": "立项",
            "candidate_item": "选题",
            "secondary_impacts": "",
            "cluster_id": "CLUSTER-001",
            "treatment": "rewrite",
            "target_rule_id": "NEW-001",
            "notes": "Synthetic",
        }
        self.write_csv(review / "atomic-rules.csv", records.RULE_FIELDS, [rule])
        principle = {
            "principle_id": "PRINCIPLE-001",
            "level": "item",
            "category": "立项",
            "item": "选题",
            "statement": "Synthetic principle",
            "supporting_cluster_ids": "CLUSTER-001",
            "supporting_rule_ids": "RULE-001",
            "decision_guidance": "Synthetic",
            "stability_check": "Synthetic",
            "conflicting_rule_ids": "",
            "status": "candidate",
        }
        self.write_csv(
            review / "principle-traceability.csv",
            principles.PRINCIPLE_FIELDS,
            [principle],
        )

        dry_run = report.build_report(root, dry_run=True)
        self.assertEqual(status.PASS, dry_run.status)
        self.assertFalse((review / "coverage-matrix.csv").exists())
        first = report.build_report(root, dry_run=False)
        targets = [
            review / "coverage-matrix.csv",
            review / "conflicts.md",
            review / "retirement-candidates.md",
            governance / "reports" / "content-review-report.json",
        ]
        first_bytes = [path.read_bytes() for path in targets]
        second = report.build_report(root, dry_run=False)
        second_bytes = [path.read_bytes() for path in targets]
        self.assertEqual(status.PASS, first.status)
        self.assertEqual(status.PASS, second.status)
        self.assertEqual(first_bytes, second_bytes)
        payload = json.loads(targets[-1].read_text(encoding="utf-8"))
        self.assertEqual(1, payload["facts"]["atomic_rule_count"])
        self.assertEqual(1, payload["facts"]["principle_count"])
        self.assertEqual("not-assessed", payload["semantic_correctness"])
        self.assertTrue(
            hasattr(report, "content_report_check"),
            "content report freshness check is missing",
        )
        self.assertEqual(status.PASS, report.content_report_check(root).status)
        with (review / "atomic-rules.csv").open("a", encoding="utf-8") as handle:
            handle.write("\n")
        stale = report.content_report_check(root)
        self.assertEqual(status.BLOCKED, stale.status)
        self.assertTrue(any("stale" in item for item in stale.findings))


if __name__ == "__main__":
    unittest.main()
