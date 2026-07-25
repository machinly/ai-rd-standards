from __future__ import annotations

import csv
import importlib
import tempfile
import unittest
from pathlib import Path


INVENTORY_FIELDS = [
    "source_id",
    "path",
    "title",
    "original_purpose",
    "applicability",
    "major_topics",
    "referenced_sources",
    "known_overlaps",
    "known_conflicts",
    "review_status",
    "reviewed_at",
]
SEGMENT_FIELDS = [
    "segment_id",
    "source_id",
    "source_start_line",
    "source_end_line",
    "segment_kind",
    "atomic_rule_ids",
    "disposition",
    "notes",
]
RULE_FIELDS = [
    "rule_id",
    "source_id",
    "source_path",
    "source_start_line",
    "source_end_line",
    "source_text",
    "intent",
    "applies_when",
    "subject",
    "rule_layer",
    "candidate_category",
    "candidate_item",
    "secondary_impacts",
    "cluster_id",
    "treatment",
    "target_rule_id",
    "notes",
]
PRINCIPLE_FIELDS = [
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
]


class RecordCheckTests(unittest.TestCase):
    def load_api(self):
        try:
            records = importlib.import_module("rd_rebuild_core.records")
            model = importlib.import_module("rd_rebuild_core.model")
        except ModuleNotFoundError as exc:
            self.fail(f"record API is missing: {exc}")
        return records, model.ResultStatus

    def load_coverage_api(self):
        try:
            coverage = importlib.import_module("rd_rebuild_core.coverage")
            model = importlib.import_module("rd_rebuild_core.model")
        except ModuleNotFoundError as exc:
            self.fail(f"rewrite API is missing: {exc}")
        return coverage, model.ResultStatus

    def load_classification_api(self):
        records, status = self.load_api()
        self.assertTrue(
            hasattr(records, "classification_check"),
            "classification_check API is missing",
        )
        return records, status

    def load_principle_api(self):
        try:
            principles = importlib.import_module("rd_rebuild_core.principles")
            model = importlib.import_module("rd_rebuild_core.model")
        except ModuleNotFoundError as exc:
            self.fail(f"principle API is missing: {exc}")
        return principles, model.ResultStatus

    def load_draft_api(self):
        try:
            drafts = importlib.import_module("rd_rebuild_core.drafts")
            model = importlib.import_module("rd_rebuild_core.model")
        except ModuleNotFoundError as exc:
            self.fail(f"draft API is missing: {exc}")
        return drafts, model.ResultStatus

    def write_csv(self, path: Path, fields: list[str], rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def make_root(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        source = root / "docs" / "W0-intake" / "00-main.md"
        source.parent.mkdir(parents=True)
        source.write_text("rule line\n\ncontext line\n", encoding="utf-8")
        inventory = {
            "source_id": "SRC-001",
            "path": "docs/W0-intake/00-main.md",
            "title": "source",
            "original_purpose": "fixture",
            "applicability": "fixture",
            "major_topics": "rules",
            "referenced_sources": "",
            "known_overlaps": "",
            "known_conflicts": "",
            "review_status": "reviewed",
            "reviewed_at": "2026-07-15T00:00:00Z",
        }
        segments = [
            {
                "segment_id": "SEG-001",
                "source_id": "SRC-001",
                "source_start_line": "1",
                "source_end_line": "1",
                "segment_kind": "rule-bearing",
                "atomic_rule_ids": "RULE-001",
                "disposition": "rule extracted",
                "notes": "fixture",
            },
            {
                "segment_id": "SEG-002",
                "source_id": "SRC-001",
                "source_start_line": "2",
                "source_end_line": "3",
                "segment_kind": "context",
                "atomic_rule_ids": "",
                "disposition": "context only",
                "notes": "does not create a rule",
            },
        ]
        rule = {
            "rule_id": "RULE-001",
            "source_id": "SRC-001",
            "source_path": "docs/W0-intake/00-main.md",
            "source_start_line": "1",
            "source_end_line": "1",
            "source_text": "rule line",
            "intent": "protect fixture behavior",
            "applies_when": "fixture runs",
            "subject": "fixture",
            "rule_layer": "normative-requirement",
            "candidate_category": "立项",
            "candidate_item": "选题",
            "secondary_impacts": "",
            "cluster_id": "",
            "treatment": "unreviewed",
            "target_rule_id": "",
            "notes": "fixture",
        }
        review = root / "rebuild-draft" / "review"
        self.write_csv(review / "source-inventory.csv", INVENTORY_FIELDS, [inventory])
        self.write_csv(review / "source-segments.csv", SEGMENT_FIELDS, segments)
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [rule])
        return root, review, inventory, segments, rule

    def write_valid_drafts(self, root: Path) -> None:
        draft_root = root / "rebuild-draft"
        (draft_root / "README.md").parent.mkdir(parents=True, exist_ok=True)
        (draft_root / "README.md").write_text(
            "# Rebuild draft\n\n持续演进\n", encoding="utf-8"
        )
        category_headings = [
            "分类目的与边界",
            "根本原则",
            "包含的项目",
            "项目之间的关系",
            "进入条件",
            "结束或循环条件",
            "与其他分类的接口",
        ]
        item_headings = [
            "项目目的与边界",
            "根本原则",
            "核心判断",
            "重新组织后的规范要求",
            "按主题整理的执行细则",
            "输入与产物",
            "完成、停止或退出条件",
            "相关项目引用",
        ]
        categories = [
            "01-initiation",
            "02-product-design",
            "03-engineering-delivery",
            "04-operations-maintenance",
        ]
        items = [
            ("01-initiation", "01-topic-selection.md"),
            ("01-initiation", "02-research.md"),
            ("02-product-design", "03-definition.md"),
            ("02-product-design", "04-experience-design.md"),
            ("03-engineering-delivery", "05-technical-design.md"),
            ("03-engineering-delivery", "06-planning.md"),
            ("03-engineering-delivery", "07-implementation.md"),
            ("03-engineering-delivery", "08-verification.md"),
            ("03-engineering-delivery", "09-release.md"),
            ("04-operations-maintenance", "10-operation.md"),
            ("04-operations-maintenance", "11-evaluation.md"),
        ]
        for category in categories:
            path = draft_root / category / "README.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "# Category\n\n"
                + "\n\n".join(f"## {heading}\nFixture." for heading in category_headings)
                + "\n",
                encoding="utf-8",
            )
        for category, filename in items:
            path = draft_root / category / filename
            path.write_text(
                "# Item\n\n"
                + "\n\n".join(f"## {heading}\nFixture." for heading in item_headings)
                + "\n",
                encoding="utf-8",
            )

    def test_valid_inventory_passes(self) -> None:
        records, status = self.load_api()
        root, _, _, _, _ = self.make_root()
        result = records.inventory_check(root)
        self.assertEqual(status.PASS, result.status)
        self.assertEqual(1, result.evidence["source_count"])

    def test_duplicate_inventory_source_blocks(self) -> None:
        records, status = self.load_api()
        root, review, inventory, _, _ = self.make_root()
        self.write_csv(
            review / "source-inventory.csv",
            INVENTORY_FIELDS,
            [inventory, dict(inventory)],
        )
        result = records.inventory_check(root)
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("duplicate" in item for item in result.findings))

    def test_continuous_nonblank_segment_coverage_passes(self) -> None:
        records, status = self.load_api()
        root, _, _, _, _ = self.make_root()
        result = records.segment_check(root)
        self.assertEqual(status.PASS, result.status)
        self.assertEqual(2, result.evidence["covered_nonblank_line_count"])

    def test_segment_gap_and_missing_rule_reference_block(self) -> None:
        records, status = self.load_api()
        root, review, _, segments, _ = self.make_root()
        invalid = [dict(segments[0])]
        invalid[0]["atomic_rule_ids"] = ""
        self.write_csv(review / "source-segments.csv", SEGMENT_FIELDS, invalid)
        result = records.segment_check(root)
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("uncovered" in item for item in result.findings))
        self.assertTrue(any("rule-bearing" in item for item in result.findings))

    def test_segment_reference_to_unknown_rule_blocks(self) -> None:
        records, status = self.load_api()
        root, review, _, segments, _ = self.make_root()
        invalid = [dict(item) for item in segments]
        invalid[0]["atomic_rule_ids"] = "RULE-MISSING"
        self.write_csv(review / "source-segments.csv", SEGMENT_FIELDS, invalid)
        result = records.segment_check(root)
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("does not exist" in item for item in result.findings))

    def test_valid_atomic_rule_passes(self) -> None:
        records, status = self.load_api()
        root, _, _, _, _ = self.make_root()
        result = records.rule_check(root)
        self.assertEqual(status.PASS, result.status)
        self.assertEqual(1, result.evidence["rule_count"])

    def test_duplicate_id_and_invalid_line_block(self) -> None:
        records, status = self.load_api()
        root, review, _, _, rule = self.make_root()
        invalid = dict(rule)
        invalid["source_start_line"] = "99"
        self.write_csv(
            review / "atomic-rules.csv", RULE_FIELDS, [invalid, dict(invalid)]
        )
        result = records.rule_check(root)
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("duplicate" in item for item in result.findings))
        self.assertTrue(any("line" in item for item in result.findings))

    def test_valid_unique_classification_passes(self) -> None:
        records, status = self.load_classification_api()
        root, _, _, _, _ = self.make_root()
        result = records.classification_check(root)
        self.assertEqual(status.PASS, result.status)
        self.assertEqual(1, result.evidence["classified_rule_count"])

    def test_duplicate_primary_owner_and_invalid_secondary_block(self) -> None:
        records, status = self.load_classification_api()
        root, review, _, _, rule = self.make_root()
        invalid = dict(rule)
        invalid["candidate_item"] = "选题;调研"
        invalid["secondary_impacts"] = "不存在的项目"
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [invalid])
        result = records.classification_check(root)
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("primary" in item for item in result.findings))
        self.assertTrue(any("secondary" in item for item in result.findings))

    def test_conflict_classification_requires_human_review(self) -> None:
        records, status = self.load_classification_api()
        root, review, _, _, rule = self.make_root()
        conflicted = dict(rule)
        conflicted["treatment"] = "conflict"
        conflicted["notes"] = "user decision required"
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [conflicted])
        result = records.classification_check(root)
        self.assertEqual(status.REVIEW_REQUIRED, result.status)

    def test_rewrite_with_target_marker_passes(self) -> None:
        coverage, status = self.load_coverage_api()
        root, review, _, _, rule = self.make_root()
        rewritten = dict(rule)
        rewritten["treatment"] = "rewrite"
        rewritten["target_rule_id"] = "NEW-001"
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [rewritten])
        draft = root / "rebuild-draft" / "01-initiation" / "01-topic-selection.md"
        draft.parent.mkdir(parents=True)
        draft.write_text(
            "<!-- rule-id: NEW-001 -->\nRephrased fixture requirement.\n",
            encoding="utf-8",
        )
        policy = {"copy_detection_thresholds": {"normalized_exact_copy_min_chars": 40, "similarity_review_ratio": 0.9}}
        result = coverage.rewrite_check(root, policy)
        self.assertEqual(status.PASS, result.status)

    def test_missing_target_and_retirement_reason_block(self) -> None:
        coverage, status = self.load_coverage_api()
        root, review, _, _, rule = self.make_root()
        rewrite = dict(rule)
        rewrite["treatment"] = "rewrite"
        rewrite["target_rule_id"] = ""
        retire = dict(rule)
        retire["rule_id"] = "RULE-002"
        retire["treatment"] = "retire"
        retire["notes"] = ""
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [rewrite, retire])
        result = coverage.rewrite_check(root, {"copy_detection_thresholds": {}})
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("target" in item for item in result.findings))
        self.assertTrue(any("retire" in item for item in result.findings))

    def test_exact_long_source_copy_blocks(self) -> None:
        coverage, status = self.load_coverage_api()
        root, review, _, _, rule = self.make_root()
        source_text = "This synthetic source sentence is deliberately longer than forty characters."
        source = root / rule["source_path"]
        source.write_text(source_text + "\n", encoding="utf-8")
        copied = dict(rule)
        copied["source_text"] = source_text
        copied["treatment"] = "rewrite"
        copied["target_rule_id"] = "NEW-001"
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [copied])
        draft = root / "rebuild-draft" / "01-initiation" / "01-topic-selection.md"
        draft.parent.mkdir(parents=True)
        draft.write_text(
            "<!-- rule-id: NEW-001 -->\n" + source_text + "\n", encoding="utf-8"
        )
        policy = {"copy_detection_thresholds": {"normalized_exact_copy_min_chars": 40, "similarity_review_ratio": 0.9}}
        result = coverage.rewrite_check(root, policy)
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("exact copy" in item for item in result.findings))

    def test_high_similarity_requires_review_not_block(self) -> None:
        coverage, status = self.load_coverage_api()
        root, review, _, _, rule = self.make_root()
        source_text = "This synthetic source sentence protects an important deterministic behavior."
        source = root / rule["source_path"]
        source.write_text(source_text + "\n", encoding="utf-8")
        similar = dict(rule)
        similar["source_text"] = source_text
        similar["treatment"] = "rewrite"
        similar["target_rule_id"] = "NEW-001"
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [similar])
        draft = root / "rebuild-draft" / "01-initiation" / "01-topic-selection.md"
        draft.parent.mkdir(parents=True)
        draft.write_text(
            "<!-- rule-id: NEW-001 -->\n"
            "This synthetic source sentence protects one important deterministic behavior.\n",
            encoding="utf-8",
        )
        policy = {"copy_detection_thresholds": {"normalized_exact_copy_min_chars": 40, "similarity_review_ratio": 0.9}}
        result = coverage.rewrite_check(root, policy)
        self.assertEqual(status.REVIEW_REQUIRED, result.status)

    def test_retirement_reason_is_warned_for_later_user_review(self) -> None:
        coverage, status = self.load_coverage_api()
        root, review, _, _, rule = self.make_root()
        retired = dict(rule)
        retired["treatment"] = "retire"
        retired["target_rule_id"] = ""
        retired["notes"] = "Superseded by a broader synthetic decision."
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [retired])
        result = coverage.rewrite_check(
            root,
            {
                "copy_detection_thresholds": {
                    "normalized_exact_copy_min_chars": 40,
                    "similarity_review_ratio": 0.9,
                }
            },
        )
        self.assertEqual(status.WARN, result.status)
        self.assertEqual(0, result.exit_code)
        self.assertTrue(any("retirement" in item for item in result.findings))

    def test_supported_item_and_category_principles_pass(self) -> None:
        principles, status = self.load_principle_api()
        root, review, _, _, rule = self.make_root()
        first = dict(rule)
        first["cluster_id"] = "CLUSTER-001"
        second = dict(rule)
        second["rule_id"] = "RULE-002"
        second["candidate_item"] = "调研"
        second["cluster_id"] = "CLUSTER-002"
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [first, second])
        rows = [
            {
                "principle_id": "PRINCIPLE-ITEM-001",
                "level": "item",
                "category": "立项",
                "item": "选题",
                "statement": "投入判断必须有明确的价值依据。",
                "supporting_cluster_ids": "CLUSTER-001",
                "supporting_rule_ids": "RULE-001",
                "decision_guidance": "决定是否投入。",
                "stability_check": "更换技术后仍成立。",
                "conflicting_rule_ids": "",
                "status": "candidate",
            },
            {
                "principle_id": "PRINCIPLE-ITEM-002",
                "level": "item",
                "category": "立项",
                "item": "调研",
                "statement": "不确定性必须通过证据逐步收敛。",
                "supporting_cluster_ids": "CLUSTER-002",
                "supporting_rule_ids": "RULE-002",
                "decision_guidance": "决定是否继续调研。",
                "stability_check": "更换技术后仍成立。",
                "conflicting_rule_ids": "",
                "status": "candidate",
            },
            {
                "principle_id": "PRINCIPLE-CATEGORY-001",
                "level": "category",
                "category": "立项",
                "item": "",
                "statement": "投入应由价值和证据共同约束。",
                "supporting_cluster_ids": "CLUSTER-001;CLUSTER-002",
                "supporting_rule_ids": "RULE-001;RULE-002",
                "decision_guidance": "决定是否进入持续演进。",
                "stability_check": "更换技术后仍成立。",
                "conflicting_rule_ids": "",
                "status": "candidate",
            },
        ]
        self.write_csv(
            review / "principle-traceability.csv", PRINCIPLE_FIELDS, rows
        )
        result = principles.principle_check(root, {"principle_review_patterns": []})
        self.assertEqual(status.PASS, result.status)

    def test_unsupported_principle_and_single_item_category_block(self) -> None:
        principles, status = self.load_principle_api()
        root, review, _, _, _ = self.make_root()
        row = {
            "principle_id": "PRINCIPLE-CATEGORY-001",
            "level": "category",
            "category": "立项",
            "item": "",
            "statement": "Fixture principle.",
            "supporting_cluster_ids": "CLUSTER-001",
            "supporting_rule_ids": "RULE-001;RULE-MISSING",
            "decision_guidance": "Fixture decision.",
            "stability_check": "Stable.",
            "conflicting_rule_ids": "",
            "status": "candidate",
        }
        self.write_csv(
            review / "principle-traceability.csv", PRINCIPLE_FIELDS, [row]
        )
        result = principles.principle_check(root, {"principle_review_patterns": []})
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("support" in item for item in result.findings))
        self.assertTrue(any("multiple items" in item for item in result.findings))

    def test_tool_specific_principle_requires_review(self) -> None:
        principles, status = self.load_principle_api()
        root, review, _, _, _ = self.make_root()
        row = {
            "principle_id": "PRINCIPLE-ITEM-001",
            "level": "item",
            "category": "立项",
            "item": "选题",
            "statement": "所有判断必须使用 MySQL 完成。",
            "supporting_cluster_ids": "CLUSTER-001",
            "supporting_rule_ids": "RULE-001",
            "decision_guidance": "Fixture decision.",
            "stability_check": "Claims stability.",
            "conflicting_rule_ids": "",
            "status": "candidate",
        }
        self.write_csv(
            review / "principle-traceability.csv", PRINCIPLE_FIELDS, [row]
        )
        result = principles.principle_check(
            root, {"principle_review_patterns": ["(?i)mysql"]}
        )
        self.assertEqual(status.REVIEW_REQUIRED, result.status)

    def test_policy_required_principle_coverage_blocks_missing_lists(self) -> None:
        principles, status = self.load_principle_api()
        root, review, _, _, _ = self.make_root()
        row = {
            "principle_id": "PRINCIPLE-ITEM-001",
            "level": "item",
            "category": "立项",
            "item": "选题",
            "statement": "Fixture principle.",
            "supporting_cluster_ids": "CLUSTER-001",
            "supporting_rule_ids": "RULE-001",
            "decision_guidance": "Fixture decision.",
            "stability_check": "Stable.",
            "conflicting_rule_ids": "",
            "status": "candidate",
        }
        self.write_csv(
            review / "principle-traceability.csv", PRINCIPLE_FIELDS, [row]
        )
        policy = {
            "principle_review_patterns": [],
            "allowed_enums": {"category_item": {"立项": ["选题", "调研"]}},
        }
        result = principles.principle_check(root, policy)
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("调研" in item for item in result.findings))
        self.assertTrue(any("category principle" in item for item in result.findings))

    def test_complete_four_category_eleven_item_draft_passes(self) -> None:
        drafts, status = self.load_draft_api()
        root, _, _, _, _ = self.make_root()
        self.write_valid_drafts(root)
        result = drafts.draft_check(root, {})
        self.assertEqual(status.PASS, result.status)
        self.assertEqual(4, result.evidence["category_count"])
        self.assertEqual(11, result.evidence["item_count"])

    def test_missing_category_and_section_block(self) -> None:
        drafts, status = self.load_draft_api()
        root, _, _, _, _ = self.make_root()
        self.write_valid_drafts(root)
        missing = root / "rebuild-draft" / "04-operations-maintenance" / "README.md"
        missing.unlink()
        item = root / "rebuild-draft" / "01-initiation" / "01-topic-selection.md"
        item.write_text("# Item\n", encoding="utf-8")
        result = drafts.draft_check(root, {})
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("category" in item for item in result.findings))
        self.assertTrue(any("section" in item for item in result.findings))

    def test_missing_canonical_target_reference_blocks(self) -> None:
        drafts, status = self.load_draft_api()
        root, review, _, _, rule = self.make_root()
        rewritten = dict(rule)
        rewritten["treatment"] = "rewrite"
        rewritten["target_rule_id"] = "NEW-001"
        self.write_csv(review / "atomic-rules.csv", RULE_FIELDS, [rewritten])
        self.write_valid_drafts(root)
        result = drafts.draft_check(root, {})
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("NEW-001" in item for item in result.findings))


if __name__ == "__main__":
    unittest.main()
