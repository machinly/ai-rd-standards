from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib
import json
import tempfile
import unittest
from pathlib import Path
import subprocess
from unittest import mock


RECOVERY_ALLOWED_PATHS = (
    "tools/rd_rebuild_core/gates.py",
    "tools/rd_rebuild_core/scope.py",
    "tools/test_rd_rebuild_gates.py",
    "tools/test_rd_rebuild_scope.py",
    "openspec/changes/build-rd-rewrite-guardrails/",
    "governance/rd-standards-rebuild/tool-manifest.json",
    "governance/rd-standards-rebuild/approvals.jsonl",
    "governance/rd-standards-rebuild/reports/2026-07-19-tool-recovery-bootstrap.json",
    "governance/rd-standards-rebuild/reports/2026-07-19-tool-recovery-manifest.json",
)
RECOVERY_ID = "G1R-2026-07-19-windows-openspec-launcher"
RECOVERY_FAILURE_REL = (
    "governance/rd-standards-rebuild/reports/"
    "2026-07-19-g8-openspec-launcher-tool-error.json"
)
RECOVERY_REQUIRED_CHECKS = (
    "full-unit-tests",
    "fixtures",
    "source-baseline",
    "protected-workspace",
    "candidate-tool-manifest",
    "openspec-internal-change-b",
    "openspec-standalone-change-b",
    "openspec-strict-change-a",
    "openspec-status-change-a",
    "openspec-status-change-b",
    "workflow-index",
)
RECOVERY_SCOPE_FIELDS = (
    "schema_version",
    "recovery_id",
    "authorization",
    "base_tool_manifest_sha256",
    "replacement_tool_manifest_sha256",
    "source_manifest_sha256",
    "allowed_recovery_paths",
    "bootstrap",
    "failure",
    "protected_workspace_snapshot",
    "durable_workspace_snapshot",
    "frozen_workspace_snapshot",
    "changed_files",
    "verification",
    "producer_self_check",
    "independent_review",
    "approval_id",
)


def canonical_digest(payload) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def recovery_workspace_snapshot(baseline, root: Path, excluded_paths) -> dict:
    files = baseline.capture_workspace_entries(root, excluded_paths)
    git_status = baseline.capture_git_status_lines(root, excluded_paths)
    return {
        "file_count": len(files),
        "file_digest": canonical_digest(files),
        "missing_path_count": sum(not item["exists"] for item in files),
        "git_status_count": len(git_status),
        "git_status_digest": canonical_digest(git_status),
    }


def recovery_scope_digest(payload: dict) -> str:
    return canonical_digest(
        {field: payload.get(field) for field in RECOVERY_SCOPE_FIELDS}
    )


class ScopeBehaviorTests(unittest.TestCase):
    def load_api(self):
        try:
            baseline = importlib.import_module("rd_rebuild_core.baseline")
            scope = importlib.import_module("rd_rebuild_core.scope")
            model = importlib.import_module("rd_rebuild_core.model")
        except ModuleNotFoundError as exc:
            self.fail(f"scope API is missing: {exc}")
        return baseline, scope, model.ResultStatus

    def make_root(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        source = root / "docs" / "W0-intake" / "00-main.md"
        source.parent.mkdir(parents=True)
        source.write_text("source\n", encoding="utf-8")
        existing = root / "existing-user-note.md"
        existing.write_text("preserve me\n", encoding="utf-8")
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
        baseline, _, _ = self.load_api()
        excluded = policy["allowed_write_roots_by_phase"]["tooling"]
        manifest = {
            "protected_sources": baseline.capture_source_entries(
                root, policy["source_roots"]
            ),
            "existing_workspace": {
                "files": baseline.capture_workspace_entries(root, excluded)
            },
        }
        return root, policy, manifest

    def test_allowed_tooling_delta_preserves_existing_work(self) -> None:
        _, scope, status = self.load_api()
        root, policy, manifest = self.make_root()
        allowed = root / "tools" / "rd_rebuild_core" / "model.py"
        allowed.parent.mkdir(parents=True)
        allowed.write_text("new tool\n", encoding="utf-8")

        result = scope.check_scope(root, policy, manifest, "tooling")

        self.assertEqual(status.PASS, result.status)
        self.assertEqual("preserve me\n", (root / "existing-user-note.md").read_text())

    def test_unauthorized_new_path_blocks(self) -> None:
        _, scope, status = self.load_api()
        root, policy, manifest = self.make_root()
        (root / "outside.txt").write_text("unauthorized\n", encoding="utf-8")

        result = scope.check_scope(root, policy, manifest, "tooling")

        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("outside.txt" in item for item in result.findings))

    def test_existing_user_file_change_blocks(self) -> None:
        _, scope, status = self.load_api()
        root, policy, manifest = self.make_root()
        (root / "existing-user-note.md").write_text("changed\n", encoding="utf-8")

        result = scope.check_scope(root, policy, manifest, "tooling")

        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("existing-user-note.md" in item for item in result.findings))

    def test_protected_source_change_blocks(self) -> None:
        _, scope, status = self.load_api()
        root, policy, manifest = self.make_root()
        (root / "docs" / "W0-intake" / "00-main.md").write_text(
            "changed source\n", encoding="utf-8"
        )

        result = scope.check_scope(root, policy, manifest, "tooling")

        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("00-main.md" in item for item in result.findings))

    def test_content_scope_blocks_frozen_tool_change(self) -> None:
        baseline, scope, status = self.load_api()
        self.assertTrue(
            hasattr(baseline, "capture_tool_entries"),
            "capture_tool_entries API is missing",
        )
        root, policy, _ = self.make_root()
        policy["allowed_write_roots_by_phase"]["content"] = [
            "rebuild-draft/",
            "governance/rd-standards-rebuild/run-state.json",
            "governance/rd-standards-rebuild/tool-manifest.json",
        ]
        tool = root / "tools" / "rd_rebuild.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("original\n", encoding="utf-8")
        governance = root / "governance" / "rd-standards-rebuild"
        governance.mkdir(parents=True)
        entries = baseline.capture_tool_entries(root, ["tools/rd_rebuild.py"])
        tool_manifest = {
            "status": "verified",
            "files": entries,
            "aggregate_sha256": baseline.tool_manifest_digest(entries),
        }
        (governance / "tool-manifest.json").write_text(
            __import__("json").dumps(tool_manifest) + "\n", encoding="utf-8"
        )
        manifest = {
            "protected_sources": baseline.capture_source_entries(
                root, policy["source_roots"]
            ),
            "existing_workspace": {
                "files": baseline.capture_workspace_entries(
                    root, policy["allowed_write_roots_by_phase"]["content"]
                )
            },
        }
        tool.write_text("changed\n", encoding="utf-8")
        result = scope.check_scope(root, policy, manifest, "content")
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("frozen tool" in item for item in result.findings))

    def test_existing_git_status_change_blocks_even_when_bytes_match(self) -> None:
        baseline, scope, status = self.load_api()
        self.assertTrue(
            hasattr(baseline, "capture_git_status_lines"),
            "git status baseline API is missing",
        )
        root, policy, _ = self.make_root()
        process = subprocess.run(
            ["git", "init", "--quiet"], cwd=root, check=False, capture_output=True
        )
        self.assertEqual(0, process.returncode)
        expected_files = baseline.capture_workspace_entries(root, [])
        expected_status = baseline.capture_git_status_lines(root, [])
        manifest = {
            "protected_sources": baseline.capture_source_entries(
                root, policy["source_roots"]
            ),
            "existing_workspace": {
                "files": expected_files,
                "git_status_lines": expected_status,
            },
        }
        subprocess.run(
            ["git", "add", "--", "existing-user-note.md"],
            cwd=root,
            check=True,
            capture_output=True,
        )
        result = scope.check_scope(root, policy, manifest, "tooling")
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("git status" in item for item in result.findings))

    def test_content_scope_rejects_rebaselined_tool_manifest(self) -> None:
        baseline, scope, status = self.load_api()
        root, policy, _ = self.make_root()
        policy["allowed_write_roots_by_phase"]["content"] = [
            "rebuild-draft/",
            "governance/rd-standards-rebuild/tool-manifest.json",
        ]
        tool = root / "tools" / "rd_rebuild.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("original\n", encoding="utf-8")
        governance = root / "governance" / "rd-standards-rebuild"
        governance.mkdir(parents=True)
        original_entries = baseline.capture_tool_entries(
            root, ["tools/rd_rebuild.py"]
        )
        original_digest = baseline.tool_manifest_digest(original_entries)
        manifest = {
            "protected_sources": baseline.capture_source_entries(
                root, policy["source_roots"]
            ),
            "existing_workspace": {
                "files": baseline.capture_workspace_entries(
                    root, policy["allowed_write_roots_by_phase"]["content"]
                )
            },
            "tool_manifest_sha256": original_digest,
        }
        tool.write_text("changed\n", encoding="utf-8")
        changed_entries = baseline.capture_tool_entries(
            root, ["tools/rd_rebuild.py"]
        )
        changed_manifest = {
            "status": "verified",
            "files": changed_entries,
            "aggregate_sha256": baseline.tool_manifest_digest(changed_entries),
        }
        (governance / "tool-manifest.json").write_text(
            __import__("json").dumps(changed_manifest) + "\n", encoding="utf-8"
        )

        result = scope.check_scope(root, policy, manifest, "content")
        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(
            any("frozen tool manifest changed" in item for item in result.findings)
        )

    def make_recovery_case(
        self,
        *,
        status_value="approved",
        add_approval=True,
        with_git_status=False,
    ):
        baseline, scope, status = self.load_api()
        root, policy, _ = self.make_root()
        if with_git_status:
            process = subprocess.run(
                ["git", "init", "--quiet"],
                cwd=root,
                check=False,
                capture_output=True,
            )
            self.assertEqual(0, process.returncode)
        content_allowed = [
            "rebuild-draft/",
            "governance/rd-standards-rebuild/baseline-manifest.json",
            "governance/rd-standards-rebuild/tool-manifest.json",
            "governance/rd-standards-rebuild/approvals.jsonl",
            "governance/rd-standards-rebuild/reports/",
            "governance/rd-standards-rebuild/run-state.json",
        ]
        policy["allowed_write_roots_by_phase"]["content"] = content_allowed
        tool = root / "tools" / "rd_rebuild_core" / "gates.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("original tool\n", encoding="utf-8")
        governance = root / "governance" / "rd-standards-rebuild"
        reports = governance / "reports"
        reports.mkdir(parents=True)
        failure_path = root / RECOVERY_FAILURE_REL
        self.write_json(
            failure_path,
            {"status": "TOOL_ERROR", "finding": "synthetic launcher failure"},
        )
        original_entries = baseline.capture_tool_entries(root, [
            "tools/rd_rebuild_core/gates.py"
        ])
        original_digest = baseline.tool_manifest_digest(original_entries)
        source_entries = baseline.capture_source_entries(
            root, policy["source_roots"]
        )
        source_digest = baseline.source_manifest_digest(source_entries)
        existing_workspace = {
            "files": baseline.capture_workspace_entries(root, content_allowed)
        }
        if with_git_status:
            existing_workspace["git_status_lines"] = (
                baseline.capture_git_status_lines(root, content_allowed)
            )
        content_baseline = {
            "kind": "content-frozen",
            "content_baseline_frozen": True,
            "protected_sources": source_entries,
            "source_manifest_sha256": source_digest,
            "existing_workspace": existing_workspace,
            "tool_manifest_sha256": original_digest,
        }
        baseline_path = governance / "baseline-manifest.json"
        self.write_json(baseline_path, content_baseline)
        self.write_json(
            governance / "run-state.json",
            {"current_state": "audit_ready", "last_passed_gate": "G7"},
        )
        protected_snapshot = recovery_workspace_snapshot(
            baseline, root, RECOVERY_ALLOWED_PATHS
        )
        bootstrap = {
            "schema_version": "1.0",
            "recovery_id": RECOVERY_ID,
            "status": "implementation_authorized",
            "authorization": {
                "approval_id": "G1R-synthetic-implementation-authorization",
                "scope": "Implementation and verification only",
            },
            "base_state": {
                "current_state": "audit_ready",
                "last_passed_gate": "G7",
                "source_manifest_sha256": source_digest,
                "tool_manifest_sha256": original_digest,
                "failure_report": RECOVERY_FAILURE_REL,
            },
            "allowed_recovery_paths": list(RECOVERY_ALLOWED_PATHS),
            "protected_workspace_snapshot": protected_snapshot,
        }
        bootstrap_path = reports / "2026-07-19-tool-recovery-bootstrap.json"
        self.write_json(bootstrap_path, bootstrap)
        anchor_patch = mock.patch.multiple(
            scope,
            RECOVERY_BASELINE_MANIFEST_SHA256=baseline.file_sha256(baseline_path),
            RECOVERY_BASE_TOOL_MANIFEST_SHA256=original_digest,
            RECOVERY_SOURCE_MANIFEST_SHA256=source_digest,
            RECOVERY_BOOTSTRAP_SHA256=baseline.file_sha256(bootstrap_path),
            RECOVERY_IMPLEMENTATION_AUTHORIZATION_ID=(
                "G1R-synthetic-implementation-authorization"
            ),
        )
        anchor_patch.start()
        self.addCleanup(anchor_patch.stop)

        tool.write_text("recovered tool\n", encoding="utf-8")
        replacement_entries = baseline.capture_tool_entries(root, [
            "tools/rd_rebuild_core/gates.py"
        ])
        replacement_digest = baseline.tool_manifest_digest(replacement_entries)
        tool_manifest = {
            "schema_version": "1.0",
            "status": "verified",
            "files": replacement_entries,
            "aggregate_sha256": replacement_digest,
        }
        self.write_json(governance / "tool-manifest.json", tool_manifest)
        durable_snapshot = recovery_workspace_snapshot(
            baseline, root, tuple(content_allowed) + RECOVERY_ALLOWED_PATHS
        )
        frozen_workspace_snapshot = recovery_workspace_snapshot(
            baseline,
            root,
            RECOVERY_ALLOWED_PATHS
            + ("governance/rd-standards-rebuild/run-state.json",),
        )
        recovery = {
            "schema_version": "1.0",
            "recovery_id": RECOVERY_ID,
            "status": status_value,
            "authorization": {
                "approval_id": "G1R-synthetic-implementation-authorization",
                "scope": "Implementation and verification only",
            },
            "base_tool_manifest_sha256": original_digest,
            "replacement_tool_manifest_sha256": replacement_digest,
            "source_manifest_sha256": source_digest,
            "allowed_recovery_paths": list(RECOVERY_ALLOWED_PATHS),
            "bootstrap": {
                "path": "governance/rd-standards-rebuild/reports/2026-07-19-tool-recovery-bootstrap.json",
                "sha256": baseline.file_sha256(bootstrap_path),
            },
            "failure": {
                "path": RECOVERY_FAILURE_REL,
                "sha256": baseline.file_sha256(failure_path),
            },
            "protected_workspace_snapshot": protected_snapshot,
            "durable_workspace_snapshot": durable_snapshot,
            "frozen_workspace_snapshot": frozen_workspace_snapshot,
            "changed_files": sorted(
                [
                    {
                        "path": "tools/rd_rebuild_core/gates.py",
                        "sha256": baseline.file_sha256(tool),
                    },
                    {
                        "path": "governance/rd-standards-rebuild/reports/2026-07-19-tool-recovery-bootstrap.json",
                        "sha256": baseline.file_sha256(bootstrap_path),
                    },
                ],
                key=lambda item: item["path"],
            ),
            "verification": {
                "status": "PASS",
                "checks": {
                    name: {"status": "PASS", "exit_code": 0}
                    for name in RECOVERY_REQUIRED_CHECKS
                },
            },
            "producer_self_check": {
                "status": "PASS",
                "reviewer": "synthetic-producer",
                "candidate_tool_manifest_sha256": replacement_digest,
            },
            "independent_review": {
                "decision": "approved",
                "reviewer": "independent-synthetic-reviewer",
                "read_only": True,
                "candidate_tool_manifest_sha256": replacement_digest,
                "findings": {"critical": 0, "important": 0, "minor": 0},
            },
            "approval_id": "G1R-synthetic-renewed-g1",
        }
        recovery["approval_scope_sha256"] = recovery_scope_digest(recovery)
        recovery_path = reports / "2026-07-19-tool-recovery-manifest.json"
        self.write_json(recovery_path, recovery)
        approvals_path = governance / "approvals.jsonl"
        if add_approval:
            approval = {
                "approval_id": recovery["approval_id"],
                "gate": "G1R",
                "decision": "approved",
                "decided_by": "user",
                "decided_at": "2026-07-19T00:00:00Z",
                "scope_sha256": recovery["approval_scope_sha256"],
                "decision_source": "synthetic-test",
                "notes": "synthetic renewed G1 approval",
            }
            approvals_path.write_text(
                json.dumps(approval, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        else:
            approvals_path.write_text("", encoding="utf-8")
        return (
            baseline,
            scope,
            status,
            root,
            policy,
            content_baseline,
            recovery_path,
        )

    def test_recovery_contract_uses_the_fixed_identifier_and_whitelist(self) -> None:
        _, scope, _ = self.load_api()
        self.assertEqual(RECOVERY_ID, getattr(scope, "RECOVERY_ID", None))
        self.assertEqual(
            RECOVERY_ALLOWED_PATHS,
            getattr(scope, "RECOVERY_ALLOWED_PATHS", ()),
        )

    def write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def rewrite_recovery_and_approval(
        self, recovery_path: Path, recovery: dict
    ) -> None:
        recovery["approval_scope_sha256"] = recovery_scope_digest(recovery)
        self.write_json(recovery_path, recovery)
        approvals_path = recovery_path.parents[1] / "approvals.jsonl"
        approval = {
            "approval_id": recovery["approval_id"],
            "gate": "G1R",
            "decision": "approved",
            "decided_by": "user",
            "decided_at": "2026-07-19T00:00:00Z",
            "scope_sha256": recovery["approval_scope_sha256"],
            "decision_source": "synthetic-test",
            "notes": "synthetic renewed G1 approval",
        }
        approvals_path.write_text(
            json.dumps(approval, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    def test_content_scope_accepts_exact_approved_recovery_without_rebaselining(self) -> None:
        _, scope, status, root, policy, manifest, _, = self.make_recovery_case()
        original = deepcopy(manifest)

        result = scope.check_scope(root, policy, manifest, "content")

        self.assertEqual(status.PASS, result.status, result.findings)
        self.assertEqual(original, manifest)
        recovery_evidence = result.evidence["results"][-1]["evidence"]
        self.assertEqual(RECOVERY_ID, recovery_evidence["recovery_id"])
        self.assertNotEqual(
            recovery_evidence["base_tool_manifest_sha256"],
            recovery_evidence["replacement_tool_manifest_sha256"],
        )

    def test_recovery_scope_digest_binds_renewed_approval_id(self) -> None:
        _, scope, _ = self.load_api()
        first = {"schema_version": "1.0", "approval_id": "G1R-first"}
        second = {"schema_version": "1.0", "approval_id": "G1R-second"}

        self.assertNotEqual(
            scope.recovery_scope_digest(first),
            scope.recovery_scope_digest(second),
        )

    def test_approved_recovery_filters_matching_baseline_git_status_entries(self) -> None:
        _, scope, status, root, policy, manifest, _, = self.make_recovery_case(
            with_git_status=True
        )

        result = scope.check_scope(root, policy, manifest, "content")

        self.assertEqual(status.PASS, result.status, result.findings)

    def test_content_scope_blocks_pending_or_unapproved_recovery(self) -> None:
        for status_value, add_approval in (("pending", True), ("approved", False)):
            with self.subTest(status=status_value, approval=add_approval):
                _, scope, status, root, policy, manifest, _, = self.make_recovery_case(
                    status_value=status_value, add_approval=add_approval
                )
                result = scope.check_scope(root, policy, manifest, "content")
                self.assertEqual(status.BLOCKED, result.status)
                self.assertTrue(any("recovery" in item for item in result.findings))

    def test_content_scope_blocks_expanded_recovery_whitelist(self) -> None:
        _, scope, status, root, policy, manifest, recovery_path, = (
            self.make_recovery_case()
        )
        recovery = json.loads(recovery_path.read_text(encoding="utf-8"))
        recovery["allowed_recovery_paths"].append("outside.txt")
        recovery["approval_scope_sha256"] = recovery_scope_digest(recovery)
        self.write_json(recovery_path, recovery)

        result = scope.check_scope(root, policy, manifest, "content")

        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(any("whitelist" in item for item in result.findings))

    def test_content_scope_blocks_recovery_digest_or_workspace_mismatch(self) -> None:
        for mutation in ("digest", "workspace"):
            with self.subTest(mutation=mutation):
                _, scope, status, root, policy, manifest, recovery_path, = (
                    self.make_recovery_case()
                )
                if mutation == "digest":
                    recovery = json.loads(recovery_path.read_text(encoding="utf-8"))
                    recovery["replacement_tool_manifest_sha256"] = "0" * 64
                    self.write_json(recovery_path, recovery)
                else:
                    (root / "existing-user-note.md").write_text(
                        "unauthorized change\n", encoding="utf-8"
                    )

                result = scope.check_scope(root, policy, manifest, "content")

                self.assertEqual(status.BLOCKED, result.status)
                self.assertTrue(result.findings)

    def test_recovery_requires_bound_failure_verification_and_reviews(self) -> None:
        mutations = {
            "producer": lambda record: record.pop("producer_self_check"),
            "failure": lambda record: record["failure"].update(
                {"sha256": "0" * 64}
            ),
            "verification": lambda record: record["verification"]["checks"].pop(
                "full-unit-tests"
            ),
            "review": lambda record: record["independent_review"].update(
                {"candidate_tool_manifest_sha256": "0" * 64}
            ),
        }
        expected_terms = {
            "producer": "producer",
            "failure": "failure",
            "verification": "verification",
            "review": "review",
        }
        for name, mutate in mutations.items():
            with self.subTest(mutation=name):
                _, scope, status, root, policy, manifest, recovery_path, = (
                    self.make_recovery_case()
                )
                recovery = json.loads(recovery_path.read_text(encoding="utf-8"))
                mutate(recovery)
                self.rewrite_recovery_and_approval(recovery_path, recovery)

                result = scope.check_scope(root, policy, manifest, "content")

                self.assertEqual(status.BLOCKED, result.status)
                self.assertTrue(
                    any(
                        expected_terms[name] in finding
                        for finding in result.findings
                    ),
                    result.findings,
                )

    def test_content_scope_blocks_full_content_baseline_rebind(self) -> None:
        baseline, scope, status, root, policy, manifest, _, = (
            self.make_recovery_case()
        )
        governance = root / "governance" / "rd-standards-rebuild"
        tool_manifest = json.loads(
            (governance / "tool-manifest.json").read_text(encoding="utf-8")
        )
        manifest["tool_manifest_sha256"] = tool_manifest["aggregate_sha256"]
        content_allowed = policy["allowed_write_roots_by_phase"]["content"]
        manifest["existing_workspace"]["files"] = (
            baseline.capture_workspace_entries(root, content_allowed)
        )
        self.write_json(governance / "baseline-manifest.json", manifest)

        result = scope.check_scope(root, policy, manifest, "content")

        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(
            any("baseline" in finding for finding in result.findings),
            result.findings,
        )

    def test_recovery_blocks_state_and_last_gate_mismatch(self) -> None:
        _, scope, status, root, policy, manifest, _, = self.make_recovery_case()
        self.write_json(
            root / "governance" / "rd-standards-rebuild" / "run-state.json",
            {"current_state": "awaiting_user_review", "last_passed_gate": "G7"},
        )

        result = scope.check_scope(root, policy, manifest, "content")

        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(
            any("state" in finding and "gate" in finding for finding in result.findings),
            result.findings,
        )

    def test_recovery_freezes_semantic_workspace_after_g8(self) -> None:
        _, scope, status, root, policy, manifest, _, = self.make_recovery_case()
        self.write_json(
            root / "governance" / "rd-standards-rebuild" / "run-state.json",
            {"current_state": "awaiting_user_review", "last_passed_gate": "G8"},
        )
        semantic = root / "rebuild-draft" / "standards" / "changed.md"
        semantic.parent.mkdir(parents=True)
        semantic.write_text("post-G8 semantic mutation\n", encoding="utf-8")

        result = scope.check_scope(root, policy, manifest, "content")

        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(
            any("frozen workspace" in finding for finding in result.findings),
            result.findings,
        )

    def test_recovery_rejects_producer_as_independent_reviewer(self) -> None:
        _, scope, status, root, policy, manifest, recovery_path, = (
            self.make_recovery_case()
        )
        recovery = json.loads(recovery_path.read_text(encoding="utf-8"))
        recovery["independent_review"]["reviewer"] = "  SYNTHETIC-PRODUCER  "
        self.rewrite_recovery_and_approval(recovery_path, recovery)

        result = scope.check_scope(root, policy, manifest, "content")

        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(
            any("distinct" in finding for finding in result.findings),
            result.findings,
        )

    def test_recovery_rejects_non_string_reviewer_identities(self) -> None:
        for review_name in ("producer_self_check", "independent_review"):
            for malformed_identity in (None, {}, []):
                with self.subTest(
                    review=review_name,
                    identity=malformed_identity,
                ):
                    _, scope, status, root, policy, manifest, recovery_path, = (
                        self.make_recovery_case()
                    )
                    recovery = json.loads(
                        recovery_path.read_text(encoding="utf-8")
                    )
                    recovery[review_name]["reviewer"] = malformed_identity
                    self.rewrite_recovery_and_approval(recovery_path, recovery)

                    result = scope.check_scope(root, policy, manifest, "content")

                    self.assertEqual(status.BLOCKED, result.status)
                    self.assertTrue(
                        any(
                            term in finding
                            for finding in result.findings
                            for term in ("producer", "review")
                        ),
                        result.findings,
                    )

    def test_recovery_rejects_non_integer_zero_review_findings(self) -> None:
        for malformed_count in (False, 0.0, "0", None):
            with self.subTest(count=malformed_count):
                _, scope, status, root, policy, manifest, recovery_path, = (
                    self.make_recovery_case()
                )
                recovery = json.loads(
                    recovery_path.read_text(encoding="utf-8")
                )
                recovery["independent_review"]["findings"][
                    "critical"
                ] = malformed_count
                self.rewrite_recovery_and_approval(recovery_path, recovery)

                result = scope.check_scope(root, policy, manifest, "content")

                self.assertEqual(status.BLOCKED, result.status)
                self.assertTrue(
                    any("review" in finding for finding in result.findings),
                    result.findings,
                )

    def test_recovery_rejects_malformed_or_ambiguous_approval_events(self) -> None:
        cases = (
            "missing-decided-at",
            "null-decided-at",
            "non-string-source",
            "non-string-notes",
            "duplicate-id",
            "conflicting-event",
        )
        for case in cases:
            with self.subTest(case=case):
                _, scope, status, root, policy, manifest, recovery_path, = (
                    self.make_recovery_case()
                )
                approvals_path = recovery_path.parents[1] / "approvals.jsonl"
                records = [
                    json.loads(line)
                    for line in approvals_path.read_text(
                        encoding="utf-8"
                    ).splitlines()
                    if line.strip()
                ]
                approval = records[0]
                if case == "missing-decided-at":
                    approval.pop("decided_at")
                elif case == "null-decided-at":
                    approval["decided_at"] = None
                elif case == "non-string-source":
                    approval["decision_source"] = []
                elif case == "non-string-notes":
                    approval["notes"] = None
                elif case == "duplicate-id":
                    records.append(deepcopy(approval))
                else:
                    conflicting = deepcopy(approval)
                    conflicting["approval_id"] = "G1R-conflicting-decision"
                    conflicting["decision"] = "rejected"
                    records.append(conflicting)
                approvals_path.write_text(
                    "".join(
                        json.dumps(record, ensure_ascii=False) + "\n"
                        for record in records
                    ),
                    encoding="utf-8",
                )

                result = scope.check_scope(root, policy, manifest, "content")

                self.assertEqual(status.BLOCKED, result.status)
                self.assertTrue(
                    any("approval" in finding for finding in result.findings),
                    result.findings,
                )

    def test_recovery_rejects_reused_implementation_authorization(self) -> None:
        _, scope, status, root, policy, manifest, recovery_path, = (
            self.make_recovery_case()
        )
        recovery = json.loads(recovery_path.read_text(encoding="utf-8"))
        recovery["approval_id"] = recovery["authorization"]["approval_id"]
        self.rewrite_recovery_and_approval(recovery_path, recovery)

        result = scope.check_scope(root, policy, manifest, "content")

        self.assertEqual(status.BLOCKED, result.status)
        self.assertTrue(
            any("distinct" in finding for finding in result.findings),
            result.findings,
        )


if __name__ == "__main__":
    unittest.main()
