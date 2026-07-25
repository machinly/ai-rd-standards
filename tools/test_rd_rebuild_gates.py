from __future__ import annotations

import argparse
import importlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


class GateBehaviorTests(unittest.TestCase):
    def load_api(self):
        try:
            gates = importlib.import_module("rd_rebuild_core.gates")
            model = importlib.import_module("rd_rebuild_core.model")
        except ModuleNotFoundError as exc:
            self.fail(f"gate API is missing: {exc}")
        return gates, model

    def write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def make_root(self):
        baseline_api = importlib.import_module("rd_rebuild_core.baseline")
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        governance = root / "governance" / "rd-standards-rebuild"
        policy = {
            "required_files_by_gate": {"tooling_ready": []},
            "approval_gates": {
                "G1": {"target_state": "tooling_ready", "human_required": True}
            },
        }
        baseline = {
            "plan_sha256": "plan-sha",
            "g0": {"source_manifest_sha256": "source-sha"},
        }
        tool = root / "tools" / "rd_rebuild.py"
        tool.parent.mkdir(parents=True)
        tool.write_text("original tool\n", encoding="utf-8")
        tool_entries = baseline_api.capture_tool_entries(
            root, ["tools/rd_rebuild.py"]
        )
        tool_manifest = {
            "aggregate_sha256": baseline_api.tool_manifest_digest(tool_entries),
            "status": "verified",
            "files": tool_entries,
        }
        run_state = {
            "schema_version": "1.0",
            "current_state": "planned",
            "last_passed_gate": "G0",
            "history": [],
            "blockers": ["G1 pending"],
            "next_action": "run G1",
            "evidence": {"tooling": "tool-manifest.json"},
        }
        self.write_json(governance / "policy.json", policy)
        self.write_json(governance / "baseline-manifest.json", baseline)
        self.write_json(governance / "tool-manifest.json", tool_manifest)
        self.write_json(governance / "run-state.json", run_state)
        (governance / "approvals.jsonl").write_text("", encoding="utf-8")
        return root, governance

    def passing_checks(self, gates, model, root):
        scope_sha = gates.gate_scope_digest(root)
        return {
            name: model.CheckResult(
                model.ResultStatus.PASS,
                name,
                evidence={"scope_sha256": scope_sha},
            )
            for name in gates.REQUIRED_CHECKS_BY_TARGET["tooling_ready"]
        }

    def test_missing_g1_approval_requires_review_without_state_change(self) -> None:
        gates, model = self.load_api()
        root, governance = self.make_root()
        before = (governance / "run-state.json").read_bytes()
        result = gates.transition_gate(
            root,
            "tooling_ready",
            self.passing_checks(gates, model, root),
            dry_run=False,
        )
        self.assertEqual(model.ResultStatus.REVIEW_REQUIRED, result.status)
        self.assertEqual(before, (governance / "run-state.json").read_bytes())

    def test_non_user_approval_cannot_advance_human_gate(self) -> None:
        gates, model = self.load_api()
        root, governance = self.make_root()
        scope_sha = gates.gate_scope_digest(root)
        approval = {
            "approval_id": "G1-non-user-test",
            "gate": "G1",
            "decision": "approved",
            "decided_by": "Codex",
            "decided_at": "2026-07-15T00:00:00Z",
            "scope_sha256": scope_sha,
            "decision_source": "synthetic-test",
            "notes": "synthetic non-user decision",
        }
        (governance / "approvals.jsonl").write_text(
            json.dumps(approval) + "\n", encoding="utf-8"
        )
        before = (governance / "run-state.json").read_bytes()
        result = gates.transition_gate(
            root,
            "tooling_ready",
            self.passing_checks(gates, model, root),
            dry_run=False,
        )
        self.assertEqual(model.ResultStatus.REVIEW_REQUIRED, result.status)
        self.assertEqual(before, (governance / "run-state.json").read_bytes())

    def test_matching_approval_advances_only_immediate_state(self) -> None:
        gates, model = self.load_api()
        root, governance = self.make_root()
        scope_sha = gates.gate_scope_digest(root)
        approval = {
            "approval_id": "G1-test",
            "gate": "G1",
            "decision": "approved",
            "decided_by": "user",
            "decided_at": "2026-07-15T00:00:00Z",
            "scope_sha256": scope_sha,
            "decision_source": "synthetic-test",
            "notes": "synthetic fixture",
        }
        (governance / "approvals.jsonl").write_text(
            json.dumps(approval) + "\n", encoding="utf-8"
        )
        result = gates.transition_gate(
            root,
            "tooling_ready",
            self.passing_checks(gates, model, root),
            dry_run=False,
        )
        self.assertEqual(model.ResultStatus.PASS, result.status)
        state = json.loads((governance / "run-state.json").read_text())
        self.assertEqual("tooling_ready", state["current_state"])
        self.assertEqual("G1", state["last_passed_gate"])

    def test_illegal_jump_and_missing_check_block(self) -> None:
        gates, model = self.load_api()
        root, governance = self.make_root()
        before = (governance / "run-state.json").read_bytes()
        jump = gates.transition_gate(root, "sources_frozen", {}, dry_run=False)
        self.assertEqual(model.ResultStatus.BLOCKED, jump.status)
        missing = gates.transition_gate(root, "tooling_ready", {}, dry_run=False)
        self.assertEqual(model.ResultStatus.BLOCKED, missing.status)
        self.assertEqual(before, (governance / "run-state.json").read_bytes())

    def test_state_write_exception_returns_tool_error_and_preserves_state(self) -> None:
        gates, model = self.load_api()
        root, governance = self.make_root()
        scope_sha = gates.gate_scope_digest(root)
        approval = {
            "approval_id": "G1-test",
            "gate": "G1",
            "decision": "approved",
            "decided_by": "user",
            "decided_at": "2026-07-15T00:00:00Z",
            "scope_sha256": scope_sha,
            "decision_source": "synthetic-test",
            "notes": "synthetic fixture",
        }
        (governance / "approvals.jsonl").write_text(
            json.dumps(approval) + "\n", encoding="utf-8"
        )
        before = (governance / "run-state.json").read_bytes()
        with mock.patch(
            "rd_rebuild_core.gates.write_json_atomic",
            side_effect=OSError("synthetic write failure"),
        ):
            result = gates.transition_gate(
                root,
                "tooling_ready",
                self.passing_checks(gates, model, root),
                dry_run=False,
            )
        self.assertEqual(model.ResultStatus.TOOL_ERROR, result.status)
        self.assertEqual(before, (governance / "run-state.json").read_bytes())

    def test_changed_frozen_tool_blocks_gate_without_state_change(self) -> None:
        gates, model = self.load_api()
        root, governance = self.make_root()
        before = (governance / "run-state.json").read_bytes()
        (root / "tools" / "rd_rebuild.py").write_text(
            "changed tool\n", encoding="utf-8"
        )
        result = gates.transition_gate(
            root,
            "tooling_ready",
            self.passing_checks(gates, model, root),
            dry_run=False,
        )
        self.assertEqual(model.ResultStatus.BLOCKED, result.status)
        self.assertTrue(any("frozen tool" in item for item in result.findings))
        self.assertEqual(before, (governance / "run-state.json").read_bytes())

    def test_stale_g1_check_scope_blocks_gate(self) -> None:
        gates, model = self.load_api()
        root, governance = self.make_root()
        checks = self.passing_checks(gates, model, root)
        checks["unit-tests"] = model.CheckResult(
            model.ResultStatus.PASS,
            "unit-tests",
            evidence={"scope_sha256": "stale-scope"},
        )
        before = (governance / "run-state.json").read_bytes()
        result = gates.transition_gate(
            root, "tooling_ready", checks, dry_run=False
        )
        self.assertEqual(model.ResultStatus.BLOCKED, result.status)
        self.assertTrue(any("stale" in item for item in result.findings))
        self.assertEqual(before, (governance / "run-state.json").read_bytes())

    def test_matching_human_approval_resolves_review_required_gate(self) -> None:
        gates, model = self.load_api()
        root, governance = self.make_root()
        state = json.loads((governance / "run-state.json").read_text(encoding="utf-8"))
        state["current_state"] = "rules_rewritten"
        state["last_passed_gate"] = "G5"
        self.write_json(governance / "run-state.json", state)
        policy_path = governance / "policy.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        policy["required_files_by_gate"]["principles_derived"] = []
        policy["approval_gates"]["G6"] = {
            "target_state": "principles_derived",
            "human_required": True,
        }
        self.write_json(policy_path, policy)
        scope_sha = gates.gate_scope_digest(root)
        approval = {
            "approval_id": "G6-test",
            "gate": "G6",
            "decision": "approved",
            "decided_by": "user",
            "decided_at": "2026-07-15T00:00:00Z",
            "scope_sha256": scope_sha,
            "decision_source": "synthetic-test",
            "notes": "synthetic semantic approval",
        }
        (governance / "approvals.jsonl").write_text(
            json.dumps(approval) + "\n", encoding="utf-8"
        )
        checks = {
            "principle-check": model.CheckResult(
                model.ResultStatus.REVIEW_REQUIRED,
                "principle needs semantic review",
            ),
            "draft-check": model.CheckResult(model.ResultStatus.PASS, "draft"),
        }
        result = gates.transition_gate(
            root, "principles_derived", checks, dry_run=False
        )
        self.assertEqual(model.ResultStatus.PASS, result.status)
        updated = json.loads(
            (governance / "run-state.json").read_text(encoding="utf-8")
        )
        self.assertEqual("principles_derived", updated["current_state"])
        self.assertEqual(
            "REVIEW_REQUIRED",
            updated["last_transition"]["check_results"]["principle-check"][
                "status"
            ],
        )

    def test_gate_rejects_mismatched_current_state_and_last_gate(self) -> None:
        gates, model = self.load_api()
        root, governance = self.make_root()
        state_path = governance / "run-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["current_state"] = "awaiting_user_review"
        state["last_passed_gate"] = "G7"
        self.write_json(state_path, state)
        policy_path = governance / "policy.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        policy["required_files_by_gate"]["approved_for_migration_design"] = []
        policy["approval_gates"]["G9"] = {
            "target_state": "approved_for_migration_design",
            "human_required": True,
        }
        self.write_json(policy_path, policy)
        scope_sha = gates.gate_scope_digest(root)
        approval = {
            "approval_id": "G9-test",
            "gate": "G9",
            "decision": "approved",
            "decided_by": "user",
            "decided_at": "2026-07-15T00:00:00Z",
            "scope_sha256": scope_sha,
            "decision_source": "synthetic-test",
            "notes": "synthetic migration-design approval",
        }
        (governance / "approvals.jsonl").write_text(
            json.dumps(approval) + "\n", encoding="utf-8"
        )
        checks = {
            name: model.CheckResult(model.ResultStatus.PASS, name)
            for name in gates.REQUIRED_CHECKS_BY_TARGET[
                "approved_for_migration_design"
            ]
        }
        before = state_path.read_bytes()

        result = gates.transition_gate(
            root,
            "approved_for_migration_design",
            checks,
            dry_run=False,
        )

        self.assertEqual(model.ResultStatus.BLOCKED, result.status)
        self.assertTrue(
            any("state" in finding and "gate" in finding for finding in result.findings),
            result.findings,
        )
        self.assertEqual(before, state_path.read_bytes())

    def test_g9_requires_live_content_scope_check(self) -> None:
        gates, model = self.load_api()
        root, _ = self.make_root()
        blocked_scope = model.CheckResult(
            model.ResultStatus.BLOCKED,
            "synthetic post-G8 semantic drift",
        )

        with mock.patch.object(
            gates,
            "check_scope",
            return_value=blocked_scope,
        ) as scope_check:
            checks = gates.gate_checks_for_target(
                root,
                "approved_for_migration_design",
            )

        self.assertIn("scope-check", checks)
        self.assertIs(blocked_scope, checks["scope-check"])
        scope_check.assert_called_once()

    def test_human_gate_blocks_malformed_duplicate_or_conflicting_approvals(
        self,
    ) -> None:
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
                gates, model = self.load_api()
                root, governance = self.make_root()
                scope_sha = gates.gate_scope_digest(root)
                approval = {
                    "approval_id": "G1-schema-test",
                    "gate": "G1",
                    "decision": "approved",
                    "decided_by": "user",
                    "decided_at": "2026-07-15T00:00:00Z",
                    "scope_sha256": scope_sha,
                    "decision_source": "synthetic-test",
                    "notes": "synthetic complete approval",
                }
                records = [approval]
                if case == "missing-decided-at":
                    approval.pop("decided_at")
                elif case == "null-decided-at":
                    approval["decided_at"] = None
                elif case == "non-string-source":
                    approval["decision_source"] = []
                elif case == "non-string-notes":
                    approval["notes"] = None
                elif case == "duplicate-id":
                    records.append(dict(approval))
                else:
                    conflicting = dict(approval)
                    conflicting["approval_id"] = "G1-conflicting-test"
                    conflicting["decision"] = "rejected"
                    records.append(conflicting)
                (governance / "approvals.jsonl").write_text(
                    "".join(json.dumps(record) + "\n" for record in records),
                    encoding="utf-8",
                )
                state_path = governance / "run-state.json"
                before = state_path.read_bytes()

                result = gates.transition_gate(
                    root,
                    "tooling_ready",
                    self.passing_checks(gates, model, root),
                    dry_run=False,
                )

                self.assertEqual(model.ResultStatus.BLOCKED, result.status)
                self.assertTrue(
                    "approval" in result.summary
                    or any("approval" in finding for finding in result.findings),
                    (result.summary, result.findings),
                )
                self.assertEqual(before, state_path.read_bytes())

    def test_human_gate_blocks_invalid_approval_json_without_state_change(
        self,
    ) -> None:
        for invalid_json in ("[]\n", "{\n"):
            with self.subTest(payload=invalid_json.strip()):
                gates, model = self.load_api()
                root, governance = self.make_root()
                (governance / "approvals.jsonl").write_text(
                    invalid_json,
                    encoding="utf-8",
                )
                state_path = governance / "run-state.json"
                before = state_path.read_bytes()

                result = gates.transition_gate(
                    root,
                    "tooling_ready",
                    self.passing_checks(gates, model, root),
                    dry_run=False,
                )

                self.assertEqual(model.ResultStatus.BLOCKED, result.status)
                self.assertTrue(
                    "approval" in result.summary,
                    (result.summary, result.findings),
                )
                self.assertEqual(before, state_path.read_bytes())

    def test_status_reports_last_gate_blocker_and_next_action(self) -> None:
        gates, model = self.load_api()
        root, _ = self.make_root()
        result = gates.status_check(root)
        self.assertEqual(model.ResultStatus.PASS, result.status)
        self.assertEqual("G0", result.evidence["last_passed_gate"])
        self.assertEqual(["G1 pending"], result.evidence["blockers"])
        self.assertEqual("run G1", result.evidence["next_action"])
        self.assertEqual(
            {"tooling": "tool-manifest.json"}, result.evidence["evidence"]
        )

    def test_cli_exposes_plan_commands_and_excludes_semantic_automation(self) -> None:
        try:
            cli = importlib.import_module("rd_rebuild")
        except ModuleNotFoundError as exc:
            self.fail(f"CLI module is missing: {exc}")
        parser = cli.build_parser()
        subparsers = next(
            action
            for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)
        )
        commands = set(subparsers.choices)
        expected = {
            "baseline-create",
            "baseline-verify",
            "scope-check",
            "inventory-check",
            "segment-check",
            "rule-check",
            "classification-check",
            "rewrite-check",
            "principle-check",
            "draft-check",
            "gate",
            "report-build",
            "verify-all",
            "status",
        }
        forbidden = {
            "auto-classify",
            "auto-principles",
            "auto-retire",
            "approve",
            "migrate",
            "delete",
        }
        self.assertEqual(expected, commands)
        self.assertTrue(forbidden.isdisjoint(commands))

    def test_baseline_create_switches_to_content_freeze_only_after_g1(self) -> None:
        cli = importlib.import_module("rd_rebuild")
        _, model = self.load_api()
        root, governance = self.make_root()
        args = argparse.Namespace(
            command="baseline-create", root=str(root), dry_run=True
        )
        passing = model.CheckResult(model.ResultStatus.PASS, "synthetic")
        with mock.patch.object(cli, "create_baseline", return_value=passing) as call:
            cli.run(args)
        self.assertEqual("tooling-bootstrap", call.call_args.kwargs["kind"])

        state = json.loads((governance / "run-state.json").read_text(encoding="utf-8"))
        state["current_state"] = "tooling_ready"
        self.write_json(governance / "run-state.json", state)
        with mock.patch.object(cli, "create_baseline", return_value=passing) as call:
            cli.run(args)
        self.assertEqual("content-frozen", call.call_args.kwargs["kind"])

    def test_cli_gate_uses_live_checks_after_g1(self) -> None:
        cli = importlib.import_module("rd_rebuild")
        _, model = self.load_api()
        root, governance = self.make_root()
        state = json.loads((governance / "run-state.json").read_text(encoding="utf-8"))
        state["current_state"] = "tooling_ready"
        self.write_json(governance / "run-state.json", state)
        args = argparse.Namespace(
            command="gate",
            root=str(root),
            target="sources_frozen",
            dry_run=True,
        )
        live = {"baseline-verify": model.CheckResult(model.ResultStatus.PASS, "live")}
        self.assertTrue(
            hasattr(cli, "gate_checks_for_target"),
            "live gate check aggregator is missing",
        )
        with mock.patch.object(
            cli, "gate_checks_for_target", return_value=live
        ) as aggregate, mock.patch.object(
            cli,
            "transition_gate",
            return_value=model.CheckResult(model.ResultStatus.PASS, "gate"),
        ) as transition:
            cli.run(args)
        aggregate.assert_called_once_with(root.resolve(), "sources_frozen")
        self.assertIs(live, transition.call_args.args[2])

    def test_openspec_windows_wrappers_use_comspec_without_shell_string(self) -> None:
        gates, model = self.load_api()
        comspec = r"C:\Windows\System32\cmd.exe"
        for suffix in ("CMD", "bat"):
            with self.subTest(suffix=suffix):
                resolved = rf"C:\Users\test user\AppData\Roaming\npm\openspec.{suffix}"
                completed = subprocess.CompletedProcess([], 0, "valid\n", "")
                with mock.patch("shutil.which", return_value=resolved), mock.patch(
                    "os.name", "nt"
                ), mock.patch.dict(os.environ, {"COMSPEC": comspec}), mock.patch.object(
                    gates.subprocess, "run", return_value=completed
                ) as run:
                    result = gates._openspec_validation_check(
                        Path("."), "rewrite-rd-standards-content"
                    )

                self.assertEqual(model.ResultStatus.PASS, result.status)
                self.assertEqual(
                    gates.WINDOWS_OPENSPEC_COMMAND,
                    run.call_args.args[0],
                )
                self.assertEqual(comspec, run.call_args.kwargs["executable"])
                child_environment = run.call_args.kwargs["env"]
                self.assertEqual(
                    resolved,
                    child_environment[gates.WINDOWS_OPENSPEC_WRAPPER_ENV],
                )
                self.assertEqual(
                    "rewrite-rd-standards-content",
                    child_environment[gates.WINDOWS_OPENSPEC_CHANGE_ENV],
                )
                self.assertFalse(run.call_args.kwargs.get("shell", False))

    @unittest.skipUnless(os.name == "nt", "Windows command wrapper behavior")
    def test_openspec_windows_wrapper_preserves_arguments_in_metachar_path(self) -> None:
        gates, model = self.load_api()
        temp = tempfile.TemporaryDirectory(prefix="rd&wrapper-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        wrapper = root / "openspec.CMD"
        wrapper.write_text(
            "@echo off\r\n"
            'if not "%~1"=="validate" exit /b 41\r\n'
            'if not "%~2"=="rewrite-rd-standards-content" exit /b 42\r\n'
            'if not "%~3"=="--strict" exit /b 43\r\n'
            'if not "%~4"=="--no-interactive" exit /b 44\r\n'
            "echo arguments-preserved\r\n"
            "exit /b 0\r\n",
            encoding="utf-8",
        )

        with mock.patch("shutil.which", return_value=str(wrapper)):
            result = gates._openspec_validation_check(
                root, "rewrite-rd-standards-content"
            )

        self.assertEqual(model.ResultStatus.PASS, result.status, result.findings)
        self.assertIn("arguments-preserved", result.evidence["output"])

    def test_openspec_direct_executable_uses_resolved_argument_list(self) -> None:
        gates, model = self.load_api()
        resolved = r"C:\Program Files\OpenSpec\openspec.exe"
        completed = subprocess.CompletedProcess([], 0, "valid\n", "")
        with mock.patch("shutil.which", return_value=resolved), mock.patch.object(
            gates.subprocess, "run", return_value=completed
        ) as run:
            result = gates._openspec_validation_check(Path("."), "sample-change")

        self.assertEqual(model.ResultStatus.PASS, result.status)
        self.assertEqual(
            [resolved, "validate", "sample-change", "--strict", "--no-interactive"],
            run.call_args.args[0],
        )
        self.assertFalse(run.call_args.kwargs.get("shell", False))

    def test_missing_openspec_launcher_returns_tool_error_without_starting(self) -> None:
        gates, model = self.load_api()
        with mock.patch("shutil.which", return_value=None), mock.patch.object(
            gates.subprocess, "run"
        ) as run:
            result = gates._openspec_validation_check(Path("."), "sample-change")

        self.assertEqual(model.ResultStatus.TOOL_ERROR, result.status)
        self.assertTrue(any("not found" in item.lower() for item in result.findings))
        run.assert_not_called()

    def test_nonzero_openspec_strict_validation_is_blocked(self) -> None:
        gates, model = self.load_api()
        resolved = r"C:\Tools\openspec.exe"
        completed = subprocess.CompletedProcess([], 1, "", "invalid change\n")
        with mock.patch("shutil.which", return_value=resolved), mock.patch.object(
            gates.subprocess, "run", return_value=completed
        ) as run:
            result = gates._openspec_validation_check(Path("."), "sample-change")

        self.assertEqual(model.ResultStatus.BLOCKED, result.status)
        self.assertTrue(any("invalid change" in item for item in result.findings))
        self.assertEqual(resolved, run.call_args.args[0][0])


if __name__ == "__main__":
    unittest.main()
