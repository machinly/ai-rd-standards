from __future__ import annotations

import shutil
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path

from check_runtime_skill_sync import ROUTER_FILES, validate_runtime_skills
from verify_rd_standards import (
    CATEGORY_LAYOUT,
    RULE_ID_RE,
    execution_detail_paths,
    parse_target_ids,
    validate_repository,
)


ROOT = Path(__file__).resolve().parents[1]

VISUAL_UX_RULE_IDS_BY_FILE = {
    "docs/02-product-design/04-experience-design.md": {
        "EXPERIENCE-VISUAL-UX-APPLICABILITY",
        "EXPERIENCE-VISUAL-UX-ARTIFACTS",
        "EXPERIENCE-VISUAL-UX-APPROVAL",
        "EXPERIENCE-VISUAL-UX-HIGH-FIDELITY",
    },
    "docs/03-engineering-delivery/06-planning.md": {
        "PLAN-VISUAL-UX-READINESS",
    },
    "docs/03-engineering-delivery/07-implementation.md": {
        "IMPL-VISUAL-UX-GATE",
        "IMPL-VISUAL-UX-DEVIATION",
    },
    "docs/03-engineering-delivery/08-verification.md": {
        "VERIFY-VISUAL-UX-CONFORMANCE",
    },
}

EXPLORE_DELIVER_RULE_IDS_BY_FILE = {
    "docs/01-initiation/01-topic-selection.md": {
        "TOPIC-RD-APPLICABILITY",
        "TOPIC-MIXED-TASK-BOUNDARY",
        "TOPIC-WORK-MODE-ROUTING",
        "TOPIC-SUPERPOWERS-COMPLEXITY-GATE",
    },
    "docs/01-initiation/02-research.md": {
        "RESEARCH-EXPLORE-SANDBOX-BOUNDARY",
    },
    "docs/02-product-design/03-definition.md": {
        "DEFINITION-EXPLORE-PROMOTION",
    },
    "docs/02-product-design/04-experience-design.md": {
        "EXPERIENCE-UX-PROTOTYPE-BOUNDARY",
    },
    "docs/03-engineering-delivery/05-technical-design.md": {
        "TECH-EXPLORE-WALKING-SKELETON",
    },
    "docs/03-engineering-delivery/06-planning.md": {
        "PLAN-EXPLORE-WIP-LIMIT",
        "PLAN-EXPLORE-SHOWCASE-CADENCE",
        "PLAN-EXPLORE-DELIVER-HANDOFF",
    },
    "docs/03-engineering-delivery/07-implementation.md": {
        "IMPL-SELECTIVE-TEST-FIRST",
    },
    "docs/03-engineering-delivery/08-verification.md": {
        "VERIFY-EXPLORE-HUMAN-READABLE-FIXTURES",
        "VERIFY-EXPLORE-SHOWCASE-BOUNDARY",
    },
    "docs/04-operations-maintenance/11-evaluation.md": {
        "EVALUATION-EXPLORE-OUTCOME",
        "EVALUATION-PROCESS-NET-BENEFIT",
    },
}

MANAGED_SCOPE_FIXTURE = """<!-- rd-standards:superpowers-scope:start -->
## Scoped Superpowers

Use one directly relevant skill.
<!-- rd-standards:superpowers-scope:end -->
"""


def read_item_details(relative_item: str) -> str:
    detail_dir = (ROOT / relative_item).with_suffix("")
    return "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(detail_dir.glob("*.md"))
    )


@contextmanager
def workspace_temp_directory():
    path = ROOT / (".runtime-sync-test-" + uuid.uuid4().hex)
    path.mkdir()
    try:
        yield path
    finally:
        shutil.rmtree(path)


class CurrentStandardsTests(unittest.TestCase):
    def test_split_coverage_targets_are_compared_individually(self) -> None:
        self.assertEqual(
            {"RELEASE-WATCH-003", "RELEASE-WATCH-004"},
            parse_target_ids("RELEASE-WATCH-003;RELEASE-WATCH-004"),
        )

    def test_repository_uses_only_the_formal_four_category_structure(self) -> None:
        result = validate_repository(ROOT)
        self.assertEqual([], result["errors"])
        self.assertEqual(4, result["category_count"])
        self.assertEqual(11, result["item_count"])
        self.assertGreaterEqual(result["detail_file_count"], 22)
        self.assertEqual(2337, result["rule_id_count"])

    def test_categories_and_items_contain_only_principles(self) -> None:
        category_paths = [ROOT / rel / "README.md" for rel in CATEGORY_LAYOUT]
        item_paths = [
            ROOT / rel / item
            for rel, item_names in CATEGORY_LAYOUT.items()
            for item in item_names
        ]

        for path in category_paths + item_paths:
            text = path.read_text(encoding="utf-8")
            headings = [line for line in text.splitlines() if line.startswith("#")]
            self.assertEqual(2, len(headings), path.as_posix())
            self.assertEqual("## 根本原则", headings[1], path.as_posix())
            self.assertNotIn("<!-- rule-id:", text, path.as_posix())

    def test_execution_details_index_covers_every_split_file_once(self) -> None:
        _, details = execution_detail_paths(ROOT)
        index = (ROOT / "docs/execution-details.md").read_text(encoding="utf-8")

        self.assertGreaterEqual(len(details), 22)
        for detail in details:
            relative = detail.relative_to(ROOT / "docs").as_posix()
            self.assertEqual(1, index.count(f"]({relative})"), relative)

    def test_visual_ux_step_has_one_owner_and_delivery_gates(self) -> None:
        expected_all: set[str] = set()

        for rel, expected in VISUAL_UX_RULE_IDS_BY_FILE.items():
            text = read_item_details(rel)
            actual = set(RULE_ID_RE.findall(text))
            self.assertTrue(expected <= actual, f"{rel} missing {sorted(expected - actual)}")
            self.assertTrue(expected_all.isdisjoint(expected))
            expected_all.update(expected)

        self.assertEqual(8, len(expected_all))

    def test_explore_deliver_rules_have_explicit_owners(self) -> None:
        expected_all: set[str] = set()

        for rel, expected in EXPLORE_DELIVER_RULE_IDS_BY_FILE.items():
            text = read_item_details(rel)
            actual = set(RULE_ID_RE.findall(text))
            self.assertTrue(expected <= actual, f"{rel} missing {sorted(expected - actual)}")
            self.assertTrue(expected_all.isdisjoint(expected))
            expected_all.update(expected)

        self.assertEqual(16, len(expected_all))

    def test_applicability_precedes_explore_deliver_and_deliver_risk_routes(
        self,
    ) -> None:
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        topic_selection = read_item_details(
            "docs/01-initiation/01-topic-selection.md"
        )

        self.assertLess(root_readme.index("R&D applicability"), root_readme.index("Quick"))
        self.assertIn("Explore", root_readme)
        self.assertIn("Deliver", root_readme)
        self.assertIn("Product Discovery", topic_selection)
        self.assertIn("UX Prototype", topic_selection)
        self.assertIn("Technical Spike", topic_selection)
        self.assertNotIn("Prototype | Quick | Standard | High-risk", root_readme)

    def test_component_reuse_does_not_wait_for_shared_abstraction(self) -> None:
        experience = read_item_details(
            "docs/02-product-design/04-experience-design.md"
        )
        implementation = read_item_details(
            "docs/03-engineering-delivery/07-implementation.md"
        )

        self.assertIn("重复交互只实现一次并通过组合复用", experience)
        self.assertIn("从第二个调用点起复用已有实现", implementation)
        self.assertIn("至少 3 个真实调用点且语义稳定", implementation)
        self.assertIn("不得为达到阈值复制实现", implementation)

    def test_application_layout_distinguishes_repository_and_application_roots(self) -> None:
        implementation = read_item_details(
            "docs/03-engineering-delivery/07-implementation.md"
        )
        evaluation = read_item_details(
            "docs/04-operations-maintenance/11-evaluation.md"
        )

        self.assertIn("多应用仓库的 Go 服务缺省位于 `services/<service>/`", implementation)
        self.assertIn("多应用仓库的可部署前端缺省位于 `web/<app>/`", implementation)
        self.assertIn("多应用仓库根不得出现归属于单个服务的 `internal/`", implementation)
        self.assertIn("repository_mode: single-application | multi-application", evaluation)

    def test_runtime_validator_rejects_a_retired_rd_skill(self) -> None:
        with workspace_temp_directory() as root:
            canonical = root / "repo" / "skills" / "one-person-openspec-rd"
            runtime = root / "runtime" / "skills"
            installed = runtime / "one-person-openspec-rd"

            for rel in ROUTER_FILES:
                canonical_file = canonical / rel
                installed_file = installed / rel
                canonical_file.parent.mkdir(parents=True, exist_ok=True)
                installed_file.parent.mkdir(parents=True, exist_ok=True)
                canonical_file.write_text(rel, encoding="utf-8")
                installed_file.write_text(rel, encoding="utf-8")

            for name in (".system", "hatch-pet", "tdx-automation"):
                (runtime / name).mkdir(parents=True, exist_ok=True)
            (runtime / "release-pipeline-gates").mkdir()

            result = validate_runtime_skills(canonical, runtime)

            self.assertFalse(result["valid"])
            self.assertEqual(["release-pipeline-gates"], result["legacy_present"])

    def test_runtime_validator_accepts_only_the_new_rd_skill(self) -> None:
        with workspace_temp_directory() as root:
            canonical = root / "repo" / "skills" / "one-person-openspec-rd"
            runtime = root / "runtime" / "skills"
            installed = runtime / "one-person-openspec-rd"

            for rel in ROUTER_FILES:
                canonical_file = canonical / rel
                installed_file = installed / rel
                canonical_file.parent.mkdir(parents=True, exist_ok=True)
                installed_file.parent.mkdir(parents=True, exist_ok=True)
                canonical_file.write_text(rel, encoding="utf-8")
                installed_file.write_text(rel, encoding="utf-8")

            for name in (".system", "hatch-pet", "tdx-automation"):
                (runtime / name).mkdir(parents=True, exist_ok=True)

            result = validate_runtime_skills(canonical, runtime)

            self.assertTrue(result["valid"])
            self.assertEqual([], result["legacy_present"])
            self.assertEqual([], result["preserved_missing"])

    def test_runtime_router_exposes_explore_types_and_scoped_superpowers(
        self,
    ) -> None:
        skill = (ROOT / "skills/one-person-openspec-rd/SKILL.md").read_text(
            encoding="utf-8"
        )
        scope = (
            ROOT
            / "skills/one-person-openspec-rd/references/superpowers-scope.md"
        ).read_text(encoding="utf-8")

        for explore_type in (
            "Product Discovery",
            "UX Prototype",
            "Technical Spike",
        ):
            self.assertIn(explore_type, skill)
        self.assertIn("Deliver Standard/High-risk", skill)
        self.assertNotIn("Quick 不创建 OpenSpec。Standard/High-risk", skill)
        self.assertIn("does not authorize another", scope)
        self.assertIn("Do not automatically chain", scope)

    def test_global_superpowers_scope_rejects_missing_managed_block(self) -> None:
        from check_runtime_skill_sync import validate_global_agents

        with workspace_temp_directory() as root:
            canonical_scope = root / "canonical-scope.md"
            global_agents = root / "AGENTS.md"
            canonical_scope.write_text(MANAGED_SCOPE_FIXTURE, encoding="utf-8")

            global_agents.write_text("", encoding="utf-8")
            empty_result = validate_global_agents(canonical_scope, global_agents)
            self.assertFalse(empty_result["valid"])

            global_agents.write_text("# Existing user instructions\n", encoding="utf-8")
            missing_result = validate_global_agents(canonical_scope, global_agents)
            self.assertFalse(missing_result["valid"])

    def test_global_superpowers_scope_accepts_exact_managed_block(self) -> None:
        from check_runtime_skill_sync import validate_global_agents

        with workspace_temp_directory() as root:
            canonical_scope = root / "canonical-scope.md"
            global_agents = root / "AGENTS.md"
            canonical_scope.write_text(MANAGED_SCOPE_FIXTURE, encoding="utf-8")
            global_agents.write_text(
                "# Existing user instructions\n\n"
                + MANAGED_SCOPE_FIXTURE
                + "\nKeep this unrelated footer.\n",
                encoding="utf-8",
            )

            result = validate_global_agents(canonical_scope, global_agents)

            self.assertTrue(result["valid"])
            self.assertEqual("synced", result["status"])


if __name__ == "__main__":
    unittest.main()
