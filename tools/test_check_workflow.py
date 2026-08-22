from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from check_workflow import validate_repository


class WorkflowCheckerTests(unittest.TestCase):
    def make_repository(self, root: Path) -> None:
        files = {
            "README.md": "# 研发工作方式\n\n请阅读 [WORKFLOW](WORKFLOW.md)。\n",
            "WORKFLOW.md": "# 工作约定\n\n普通工作直接完成。\n",
            "skills/opc-rd/SKILL.md": (
                "---\n"
                "name: opc-rd\n"
                "description: Explicit-only R&D guidance.\n"
                "---\n\n"
                "# OPC R&D\n"
            ),
            "openspec/README.md": "# OpenSpec\n",
            "openspec/config.yaml": "project: test\n",
            "tools/check_workflow.py": "# checker fixture\n",
        }
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def validate_fixture(self, mutate=None) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_repository(root)
            if mutate is not None:
                mutate(root)
            return validate_repository(root)

    def test_minimal_repository_passes_without_fixed_wording(self) -> None:
        result = self.validate_fixture()

        self.assertEqual([], result["errors"])
        self.assertLessEqual(result["default_lines"], 200)
        self.assertLessEqual(result["normative_lines"], 350)
        self.assertEqual(0, result["active_change_count"])

    def test_missing_required_entry_fails(self) -> None:
        result = self.validate_fixture(lambda root: (root / "WORKFLOW.md").unlink())

        self.assertIn("Missing required file: WORKFLOW.md", result["errors"])

    def test_readme_must_link_to_workflow(self) -> None:
        def mutate(root: Path) -> None:
            (root / "README.md").write_text("# 研发工作方式\n", encoding="utf-8")

        result = self.validate_fixture(mutate)

        self.assertIn("README.md must link to WORKFLOW.md", result["errors"])

    def test_default_reading_budget_is_enforced(self) -> None:
        def mutate(root: Path) -> None:
            workflow = "# 工作约定\n" + "规则\n" * 200
            (root / "WORKFLOW.md").write_text(workflow, encoding="utf-8")

        result = self.validate_fixture(mutate)

        self.assertTrue(
            any(error.startswith("Default reading exceeds 200 lines") for error in result["errors"])
        )

    def test_retired_normative_tree_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "docs/03-engineering-delivery/README.md"
            path.parent.mkdir(parents=True)
            path.write_text("# old\n", encoding="utf-8")

        result = self.validate_fixture(mutate)

        self.assertIn(
            "Retired path is still active: docs/03-engineering-delivery",
            result["errors"],
        )

    def test_competing_current_status_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "governance/current-status.json"
            path.parent.mkdir(parents=True)
            path.write_text("{}\n", encoding="utf-8")

        result = self.validate_fixture(mutate)

        self.assertIn("Retired path is still active: governance", result["errors"])

    def test_active_change_requires_proposal_and_tasks(self) -> None:
        def mutate(root: Path) -> None:
            change = root / "openspec/changes/example"
            change.mkdir(parents=True)
            (change / "proposal.md").write_text("# Proposal\n", encoding="utf-8")

        result = self.validate_fixture(mutate)

        self.assertIn(
            "Active change example is missing tasks.md",
            result["errors"],
        )

    def test_broken_local_markdown_link_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            (root / "WORKFLOW.md").write_text(
                "# 工作约定\n\n[missing](missing.md)\n",
                encoding="utf-8",
            )

        result = self.validate_fixture(mutate)

        self.assertIn(
            "Broken local Markdown link in WORKFLOW.md: missing.md",
            result["errors"],
        )

    def test_old_rule_counts_are_not_a_success_condition(self) -> None:
        def mutate(root: Path) -> None:
            plan = root / "docs/superpowers/plans/history.md"
            plan.parent.mkdir(parents=True)
            plan.write_text(
                "# Historical note\n\nThe old corpus had 2,337 rule IDs.\n",
                encoding="utf-8",
            )

        result = self.validate_fixture(mutate)

        self.assertEqual([], result["errors"])


if __name__ == "__main__":
    unittest.main()
