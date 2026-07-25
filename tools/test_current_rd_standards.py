from __future__ import annotations

import shutil
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path

from check_runtime_skill_sync import ROUTER_FILES, validate_runtime_skills
from verify_rd_standards import RULE_ID_RE, parse_target_ids, validate_repository


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
        self.assertEqual(2321, result["rule_id_count"])

    def test_visual_ux_step_has_one_owner_and_delivery_gates(self) -> None:
        expected_all: set[str] = set()

        for rel, expected in VISUAL_UX_RULE_IDS_BY_FILE.items():
            text = (ROOT / rel).read_text(encoding="utf-8")
            actual = set(RULE_ID_RE.findall(text))
            self.assertTrue(expected <= actual, f"{rel} missing {sorted(expected - actual)}")
            self.assertTrue(expected_all.isdisjoint(expected))
            expected_all.update(expected)

        self.assertEqual(8, len(expected_all))

    def test_component_reuse_does_not_wait_for_shared_abstraction(self) -> None:
        experience = (
            ROOT / "docs/02-product-design/04-experience-design.md"
        ).read_text(encoding="utf-8")
        implementation = (
            ROOT / "docs/03-engineering-delivery/07-implementation.md"
        ).read_text(encoding="utf-8")

        self.assertIn("重复交互只实现一次并通过组合复用", experience)
        self.assertIn("从第二个调用点起复用已有实现", implementation)
        self.assertIn("至少 3 个真实调用点且语义稳定", implementation)
        self.assertIn("不得为达到阈值复制实现", implementation)

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


if __name__ == "__main__":
    unittest.main()
