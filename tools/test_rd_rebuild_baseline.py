from __future__ import annotations

import hashlib
import importlib
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    ROOT / "governance" / "rd-standards-rebuild" / "baseline-manifest.json"
)


class BootstrapManifestTests(unittest.TestCase):
    def test_protected_source_paths_are_canonical_and_match_g0_digest(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        entries = manifest["protected_sources"]

        self.assertTrue(entries)
        self.assertTrue(
            all("\\" not in entry["path"] for entry in entries),
            "protected source paths must use repository-relative POSIX separators",
        )

        lines = [f'{entry["path"]}\t{entry["sha256"]}' for entry in entries]
        digest = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
        self.assertEqual(manifest["g0"]["source_manifest_sha256"], digest)


class BaselineBehaviorTests(unittest.TestCase):
    def load_api(self):
        try:
            baseline = importlib.import_module("rd_rebuild_core.baseline")
            model = importlib.import_module("rd_rebuild_core.model")
        except ModuleNotFoundError as exc:
            self.fail(f"baseline API is missing: {exc}")
        return baseline, model.ResultStatus

    def make_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path, dict]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        source = root / "docs" / "W0-intake" / "00-main.md"
        source.parent.mkdir(parents=True)
        source.write_text("# source\nrule\n", encoding="utf-8")
        policy = {
            "source_roots": ["docs/W0-intake/"],
            "protected_roots": ["docs/W0-intake/"],
            "allowed_write_roots_by_phase": {
                "tooling": [
                    "tools/rd_rebuild.py",
                    "tools/rd_rebuild_core/",
                    "governance/rd-standards-rebuild/",
                ]
            },
        }
        return temp, root, policy

    def test_source_digest_is_canonical_and_deterministic(self) -> None:
        baseline, _ = self.load_api()
        entries = [
            {"path": "docs\\W1\\b.md", "sha256": "b" * 64, "size": 2},
            {"path": "docs/W0/a.md", "sha256": "a" * 64, "size": 1},
        ]
        first = baseline.source_manifest_digest(entries)
        second = baseline.source_manifest_digest(list(reversed(entries)))
        self.assertEqual(first, second)

    def test_unchanged_sources_pass_and_changed_source_blocks(self) -> None:
        baseline, status = self.load_api()
        _, root, policy = self.make_root()
        entries = baseline.capture_source_entries(root, policy["source_roots"])

        passing = baseline.verify_source_entries(root, entries)
        self.assertEqual(status.PASS, passing.status)

        (root / "docs" / "W0-intake" / "00-main.md").write_text(
            "changed\n", encoding="utf-8"
        )
        blocked = baseline.verify_source_entries(root, entries)
        self.assertEqual(status.BLOCKED, blocked.status)
        self.assertTrue(any("00-main.md" in item for item in blocked.findings))

    def test_baseline_create_dry_run_has_zero_writes(self) -> None:
        baseline, status = self.load_api()
        _, root, policy = self.make_root()
        target = root / "governance" / "rd-standards-rebuild" / "baseline.json"

        before = sorted(path.relative_to(root) for path in root.rglob("*"))
        result = baseline.create_baseline(
            root, policy, target, dry_run=True, kind="tooling-bootstrap"
        )
        after = sorted(path.relative_to(root) for path in root.rglob("*"))

        self.assertEqual(status.PASS, result.status)
        self.assertEqual(before, after)
        self.assertFalse(target.exists())
        self.assertEqual(target.as_posix(), result.evidence["planned_write"])

    def test_existing_baseline_is_not_overwritten(self) -> None:
        baseline, status = self.load_api()
        _, root, policy = self.make_root()
        target = root / "governance" / "rd-standards-rebuild" / "baseline.json"
        target.parent.mkdir(parents=True)
        target.write_text('{"sentinel":true}\n', encoding="utf-8")

        result = baseline.create_baseline(
            root, policy, target, dry_run=False, kind="tooling-bootstrap"
        )

        self.assertEqual(status.BLOCKED, result.status)
        self.assertEqual('{"sentinel":true}\n', target.read_text(encoding="utf-8"))

    def test_content_baseline_transition_requires_g1_and_verified_tool(self) -> None:
        baseline, status = self.load_api()
        _, root, policy = self.make_root()
        policy["allowed_write_roots_by_phase"]["content"] = [
            "rebuild-draft/",
            "governance/rd-standards-rebuild/baseline.json",
        ]
        governance = root / "governance" / "rd-standards-rebuild"
        target = governance / "baseline.json"
        target.parent.mkdir(parents=True)
        target.write_text(
            json.dumps({"kind": "tooling-bootstrap"}) + "\n", encoding="utf-8"
        )

        blocked = baseline.create_baseline(
            root, policy, target, dry_run=False, kind="content-frozen"
        )
        self.assertEqual(status.BLOCKED, blocked.status)

        (governance / "run-state.json").write_text(
            json.dumps({"current_state": "tooling_ready"}) + "\n",
            encoding="utf-8",
        )
        tool = root / "tools" / "rd_rebuild.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("verified tool\n", encoding="utf-8")
        tool_entries = baseline.capture_tool_entries(
            root, ["tools/rd_rebuild.py"]
        )
        (governance / "tool-manifest.json").write_text(
            json.dumps(
                {
                    "status": "verified",
                    "files": tool_entries,
                    "aggregate_sha256": baseline.tool_manifest_digest(tool_entries),
                }
            )
            + "\n",
            encoding="utf-8",
        )
        passing = baseline.create_baseline(
            root, policy, target, dry_run=False, kind="content-frozen"
        )
        self.assertEqual(status.PASS, passing.status)
        payload = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual("content-frozen", payload["kind"])
        self.assertTrue(payload["content_baseline_frozen"])

    def test_frozen_tool_manifest_detects_tool_change(self) -> None:
        baseline, status = self.load_api()
        self.assertTrue(
            hasattr(baseline, "capture_tool_entries"),
            "capture_tool_entries API is missing",
        )
        self.assertTrue(
            hasattr(baseline, "tool_manifest_digest"),
            "tool_manifest_digest API is missing",
        )
        self.assertTrue(
            hasattr(baseline, "verify_tool_manifest"),
            "verify_tool_manifest API is missing",
        )
        _, root, _ = self.make_root()
        tool = root / "tools" / "rd_rebuild.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("original\n", encoding="utf-8")
        entries = baseline.capture_tool_entries(root, ["tools/rd_rebuild.py"])
        manifest = {
            "status": "verified",
            "files": entries,
            "aggregate_sha256": baseline.tool_manifest_digest(entries),
        }
        self.assertEqual(
            status.PASS, baseline.verify_tool_manifest(root, manifest).status
        )
        tool.write_text("changed\n", encoding="utf-8")
        result = baseline.verify_tool_manifest(root, manifest)
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("rd_rebuild.py" in item for item in result.findings))

    def test_content_baseline_transition_rejects_stale_verified_manifest(self) -> None:
        baseline, status = self.load_api()
        _, root, policy = self.make_root()
        policy["allowed_write_roots_by_phase"]["content"] = ["rebuild-draft/"]
        governance = root / "governance" / "rd-standards-rebuild"
        governance.mkdir(parents=True)
        target = governance / "baseline.json"
        target.write_text(
            json.dumps({"kind": "tooling-bootstrap"}) + "\n", encoding="utf-8"
        )
        (governance / "run-state.json").write_text(
            json.dumps({"current_state": "tooling_ready"}) + "\n",
            encoding="utf-8",
        )
        tool = root / "tools" / "rd_rebuild.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("original\n", encoding="utf-8")
        entries = baseline.capture_tool_entries(root, ["tools/rd_rebuild.py"])
        manifest = {
            "status": "verified",
            "files": entries,
            "aggregate_sha256": baseline.tool_manifest_digest(entries),
        }
        (governance / "tool-manifest.json").write_text(
            json.dumps(manifest) + "\n", encoding="utf-8"
        )
        tool.write_text("changed\n", encoding="utf-8")

        result = baseline.create_baseline(
            root, policy, target, dry_run=False, kind="content-frozen"
        )
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("frozen tool" in item for item in result.findings))
        self.assertEqual(
            "tooling-bootstrap",
            json.loads(target.read_text(encoding="utf-8"))["kind"],
        )

    def test_content_baseline_cannot_be_created_without_bootstrap_manifest(self) -> None:
        baseline, status = self.load_api()
        _, root, policy = self.make_root()
        policy["allowed_write_roots_by_phase"]["content"] = ["rebuild-draft/"]
        governance = root / "governance" / "rd-standards-rebuild"
        governance.mkdir(parents=True)
        (governance / "run-state.json").write_text(
            json.dumps({"current_state": "tooling_ready"}) + "\n",
            encoding="utf-8",
        )
        tool = root / "tools" / "rd_rebuild.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("verified\n", encoding="utf-8")
        entries = baseline.capture_tool_entries(root, ["tools/rd_rebuild.py"])
        (governance / "tool-manifest.json").write_text(
            json.dumps(
                {
                    "status": "verified",
                    "files": entries,
                    "aggregate_sha256": baseline.tool_manifest_digest(entries),
                }
            )
            + "\n",
            encoding="utf-8",
        )
        target = governance / "baseline.json"
        result = baseline.create_baseline(
            root, policy, target, dry_run=False, kind="content-frozen"
        )
        self.assertEqual(status.BLOCKED, result.status)
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
