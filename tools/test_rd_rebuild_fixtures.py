from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from rd_rebuild_core import baseline, coverage, drafts, principles, records, scope
from rd_rebuild_core.drafts import (
    CATEGORY_FILES,
    CATEGORY_SECTIONS,
    ITEM_FILES,
    ITEM_SECTIONS,
)
from rd_rebuild_core.model import CheckResult, ResultStatus


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tools" / "fixtures" / "rd_rebuild"
FIXTURE_NAMES = (
    "valid",
    "source_changed",
    "line_gap",
    "duplicate_owner",
    "unsupported_principle",
    "unauthorized_write",
)


class PlanFixtureTests(unittest.TestCase):
    def load_case(self, name: str) -> dict[str, Any]:
        path = FIXTURE_ROOT / name / "case.json"
        self.assertTrue(path.is_file(), f"plan-defined fixture is missing: {path}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(name, payload.get("name"))
        self.assertIn("expected_status", payload)
        return payload

    def write_csv(
        self, path: Path, fields: set[str], rows: list[dict[str, str]]
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        ordered = sorted(fields)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=ordered)
            writer.writeheader()
            writer.writerows(rows)

    def make_common_root(self, case: dict[str, Any]) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        relative = "docs/W0-intake/00-main.md"
        source = root / relative
        source.parent.mkdir(parents=True)
        lines = case.get("source_lines", ["Synthetic rule."])
        source.write_text("\n".join(lines) + "\n", encoding="utf-8")
        review = root / "rebuild-draft" / "review"
        inventory = {
            "source_id": "SRC-001",
            "path": relative,
            "title": "Synthetic source",
            "original_purpose": "Exercise deterministic checks",
            "applicability": "Fixture only",
            "major_topics": "fixture",
            "referenced_sources": "",
            "known_overlaps": "",
            "known_conflicts": "",
            "review_status": "reviewed",
            "reviewed_at": "2026-07-15",
        }
        self.write_csv(
            review / "source-inventory.csv", records.INVENTORY_FIELDS, [inventory]
        )
        segments: list[dict[str, str]] = []
        ranges = case.get(
            "segment_ranges", [[number, number] for number in range(1, len(lines) + 1)]
        )
        rule_lines = {
            int(rule.get("line", 1)): rule.get("rule_id", "RULE-001")
            for rule in case.get("rules", [])
        }
        for number, (start, end) in enumerate(ranges, 1):
            linked = [
                rule_id
                for line, rule_id in sorted(rule_lines.items())
                if start <= line <= end
            ]
            segments.append(
                {
                    "segment_id": f"SEG-{number:03d}",
                    "source_id": "SRC-001",
                    "source_start_line": str(start),
                    "source_end_line": str(end),
                    "segment_kind": "rule-bearing" if linked else "context",
                    "atomic_rule_ids": ";".join(linked),
                    "disposition": "rule extracted" if linked else "context only",
                    "notes": "synthetic fixture",
                }
            )
        self.write_csv(
            review / "source-segments.csv", records.SEGMENT_FIELDS, segments
        )
        rule_rows: list[dict[str, str]] = []
        for number, value in enumerate(case.get("rules", []), 1):
            line = int(value.get("line", number))
            rule_rows.append(
                {
                    "rule_id": value.get("rule_id", f"RULE-{number:03d}"),
                    "source_id": "SRC-001",
                    "source_path": relative,
                    "source_start_line": str(line),
                    "source_end_line": str(line),
                    "source_text": value.get("source_text", lines[line - 1]),
                    "intent": "Protect a synthetic decision",
                    "applies_when": "The fixture runs",
                    "subject": "Fixture",
                    "rule_layer": "normative-requirement",
                    "candidate_category": value.get("category", "立项"),
                    "candidate_item": value.get("item", "选题"),
                    "secondary_impacts": value.get("secondary_impacts", ""),
                    "cluster_id": value.get("cluster_id", f"CLUSTER-{number:03d}"),
                    "treatment": value.get("treatment", "rewrite"),
                    "target_rule_id": value.get("target_rule_id", f"NEW-{number:03d}"),
                    "notes": value.get("notes", "synthetic fixture"),
                }
            )
        self.write_csv(
            review / "atomic-rules.csv", records.RULE_FIELDS, rule_rows
        )
        principle_rows: list[dict[str, str]] = []
        for value in case.get("principles", []):
            principle_rows.append(
                {
                    "principle_id": value["principle_id"],
                    "level": value["level"],
                    "category": value.get("category", "立项"),
                    "item": value.get("item", ""),
                    "statement": value.get("statement", "Stable synthetic principle."),
                    "supporting_cluster_ids": value.get(
                        "supporting_cluster_ids", "CLUSTER-001"
                    ),
                    "supporting_rule_ids": value.get(
                        "supporting_rule_ids", "RULE-001"
                    ),
                    "decision_guidance": "Guide a synthetic decision.",
                    "stability_check": "Remains true when tooling changes.",
                    "conflicting_rule_ids": "",
                    "status": "candidate",
                }
            )
        if principle_rows:
            self.write_csv(
                review / "principle-traceability.csv",
                principles.PRINCIPLE_FIELDS,
                principle_rows,
            )
        return root

    def write_complete_draft(self, root: Path, target_ids: list[str]) -> None:
        draft_root = root / "rebuild-draft"
        (draft_root / "README.md").write_text(
            "# Synthetic rebuild\n\n持续演进。\n", encoding="utf-8"
        )
        for relative, category in CATEGORY_FILES.items():
            path = draft_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            body = "\n\n".join(
                f"## {section}\nSynthetic {category} content."
                for section in CATEGORY_SECTIONS
            )
            path.write_text(f"# {category}\n\n{body}\n", encoding="utf-8")
        first_item = next(iter(ITEM_FILES))
        for relative, item in ITEM_FILES.items():
            path = draft_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            markers = ""
            if relative == first_item:
                markers = "\n".join(
                    f"<!-- rule-id: {target} -->" for target in target_ids
                )
            body = "\n\n".join(
                f"## {section}\nSynthetic {item} content."
                for section in ITEM_SECTIONS
            )
            path.write_text(
                f"# {item}\n\n{markers}\n\n{body}\n", encoding="utf-8"
            )

    def run_case(self, case: dict[str, Any]) -> list[CheckResult]:
        name = case["name"]
        if name == "source_changed":
            temporary = tempfile.TemporaryDirectory()
            self.addCleanup(temporary.cleanup)
            root = Path(temporary.name)
            relative = Path(case["path"])
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_text(case["current_text"], encoding="utf-8")
            expected = {
                "path": relative.as_posix(),
                "sha256": hashlib.sha256(
                    case["baseline_text"].encode("utf-8")
                ).hexdigest(),
            }
            return [baseline.verify_source_entries(root, [expected])]
        if name == "unauthorized_write":
            temporary = tempfile.TemporaryDirectory()
            self.addCleanup(temporary.cleanup)
            root = Path(temporary.name)
            existing = root / case["baseline_file"]
            existing.parent.mkdir(parents=True, exist_ok=True)
            existing.write_text("preserve\n", encoding="utf-8")
            policy = {
                "source_roots": [],
                "allowed_write_roots_by_phase": {
                    "tooling": case["allowed_write_roots"]
                },
            }
            manifest = {
                "protected_sources": [],
                "existing_workspace": {
                    "files": baseline.capture_workspace_entries(
                        root, case["allowed_write_roots"]
                    )
                },
            }
            outside = root / case["unauthorized_file"]
            outside.parent.mkdir(parents=True, exist_ok=True)
            outside.write_text("unauthorized\n", encoding="utf-8")
            return [scope.check_scope(root, policy, manifest, "tooling")]
        root = self.make_common_root(case)
        if name == "line_gap":
            return [records.segment_check(root)]
        if name == "duplicate_owner":
            return [records.classification_check(root)]
        if name == "unsupported_principle":
            return [principles.principle_check(root, {"principle_review_patterns": []})]
        target_ids = [
            rule.get("target_rule_id", f"NEW-{number:03d}")
            for number, rule in enumerate(case["rules"], 1)
        ]
        self.write_complete_draft(root, target_ids)
        policy = case["policy"]
        sources = baseline.capture_source_entries(root, ["docs/W0-intake/"])
        workspace = baseline.capture_workspace_entries(root, [])
        baseline_manifest = {
            "protected_sources": sources,
            "existing_workspace": {"files": workspace},
        }
        return [
            baseline.verify_source_entries(root, sources, ["docs/W0-intake/"]),
            scope.check_scope(
                root,
                {
                    "source_roots": ["docs/W0-intake/"],
                    "allowed_write_roots_by_phase": {"tooling": []},
                },
                baseline_manifest,
                "tooling",
            ),
            records.inventory_check(root),
            records.segment_check(root),
            records.rule_check(root),
            records.classification_check(root),
            coverage.rewrite_check(root, policy),
            principles.principle_check(root, policy),
            drafts.draft_check(root, policy),
        ]

    def assert_fixture(self, name: str) -> None:
        case = self.load_case(name)
        expected = ResultStatus(case["expected_status"])
        first = self.run_case(case)
        second = self.run_case(case)
        self.assertTrue(first, "fixture must execute at least one check")
        self.assertEqual(
            [result.to_dict() for result in first],
            [result.to_dict() for result in second],
            "repeated fixture input must produce deterministic results",
        )
        if expected == ResultStatus.PASS:
            self.assertTrue(all(result.status == expected for result in first))
        else:
            self.assertEqual(expected, first[0].status)
            fragment = case.get("expected_finding_contains")
            if fragment:
                self.assertTrue(
                    any(fragment in finding for finding in first[0].findings),
                    first[0].findings,
                )

    def test_valid_fixture(self) -> None:
        self.assert_fixture("valid")

    def test_source_changed_fixture(self) -> None:
        self.assert_fixture("source_changed")

    def test_line_gap_fixture(self) -> None:
        self.assert_fixture("line_gap")

    def test_duplicate_owner_fixture(self) -> None:
        self.assert_fixture("duplicate_owner")

    def test_unsupported_principle_fixture(self) -> None:
        self.assert_fixture("unsupported_principle")

    def test_unauthorized_write_fixture(self) -> None:
        self.assert_fixture("unauthorized_write")

    def test_review_required_exit_is_distinct_from_blocked(self) -> None:
        review = CheckResult(ResultStatus.REVIEW_REQUIRED, "review")
        blocked = CheckResult(ResultStatus.BLOCKED, "blocked")
        self.assertEqual(2, review.exit_code)
        self.assertEqual(1, blocked.exit_code)
        self.assertNotEqual(review.exit_code, blocked.exit_code)


if __name__ == "__main__":
    unittest.main()
