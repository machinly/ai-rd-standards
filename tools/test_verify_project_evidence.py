from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from verify_project_evidence import validate


class ProjectEvidenceVerifierTests(unittest.TestCase):
    def make_project(self) -> tempfile.TemporaryDirectory[str]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "README.md").write_text("# Test\n", encoding="utf-8")
        for path in (
            "apps/api/cmd/api",
            "apps/api/cmd/worker",
            "governance/architecture",
            "governance/quality",
            "governance/reviews",
        ):
            (root / path).mkdir(parents=True, exist_ok=True)
        (root / "governance/README.md").write_text("# Governance\n", encoding="utf-8")
        review = "governance/reviews/final.json"
        (root / review).write_text("{}\n", encoding="utf-8")
        project_map = {
            "top_level": [
                {"path": "apps", "kind": "source", "purpose": "applications"},
                {"path": "governance", "kind": "governance", "purpose": "process evidence"},
            ],
            "read_first": ["README.md", "governance/README.md", "governance/current-status.json"],
            "runtime_processes": [{"name": "api", "kind": "service", "path": "apps/api", "command": "go run ./cmd/api"}],
            "common_commands": [{"name": "test", "command": "go test ./..."}],
            "canonical_sources": ["README.md"],
            "governance_domains": [
                {"name": "architecture", "path": "governance/architecture", "owner": "owner", "trigger": "multiple commands", "decision_or_gate": "command registry", "retention": "project lifetime"},
                {"name": "quality", "path": "governance/quality", "owner": "owner", "trigger": "user-visible", "decision_or_gate": "journey gate", "retention": "project lifetime"},
                {"name": "reviews", "path": "governance/reviews", "owner": "owner", "trigger": "independent review", "decision_or_gate": "acceptance", "retention": "project lifetime"},
            ],
        }
        (root / "governance/project-map.json").write_text(json.dumps(project_map), encoding="utf-8")
        status = {
            "status": "accepted",
            "target_revision": "sha256:test",
            "updated_at": "2026-07-11T00:00:00Z",
            "latest_review": {"path": review, "decision": "accepted", "target_revision": "sha256:test"},
        }
        (root / "governance/current-status.json").write_text(json.dumps(status), encoding="utf-8")
        journeys = {
            "target": "web",
            "journeys": [{
                "id": "UJ-1", "role": "user", "goal": "sign in",
                "preconditions": ["synthetic user"], "steps": ["open page", "submit"],
                "success": ["account visible"], "failure": ["error visible"],
                "evidence_level": "browser-e2e", "command": "pnpm test:e2e",
                "business_actions_via_ui": True, "api_used_for_setup_only": True,
                "assertions": {"ui": ["account"], "business_state": ["session"]},
                "failure_artifacts": ["trace"], "clean_environment_command": "pnpm e2e:local",
                "evidence": ["governance/quality/run.json"], "status": "pass",
                "last_run_at": "2026-07-11T00:00:00Z"
            }],
        }
        (root / "governance/quality/user-journeys.json").write_text(json.dumps(journeys), encoding="utf-8")
        commands = {"commands": []}
        for name, kind, lifecycle in (("api", "api", "long-running"), ("worker", "worker", "long-running")):
            commands["commands"].append({
                "path": f"apps/api/cmd/{name}", "purpose": name, "kind": kind,
                "environment": "production", "lifecycle": lifecycle, "starter": "service manager",
                "dependencies": ["mysql"], "privileges": ["service"], "data_writes": ["users"],
                "failure_recovery": "restart", "retirement": "remove deployment first"
            })
        (root / "governance/architecture/command-registry.json").write_text(json.dumps(commands), encoding="utf-8")
        return temp

    def test_valid_project_passes(self) -> None:
        temp = self.make_project()
        self.addCleanup(temp.cleanup)
        errors = validate(Path(temp.name), True, True, True)
        self.assertEqual(errors, [])

    def test_manual_browser_check_cannot_satisfy_e2e(self) -> None:
        temp = self.make_project()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "governance/quality/user-journeys.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["journeys"][0]["evidence_level"] = "manual-browser-check"
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = validate(Path(temp.name), True, True, True)
        self.assertTrue(any("browser-e2e journey pass" in item for item in errors))

    def test_changes_requested_invalidates_accepted(self) -> None:
        temp = self.make_project()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "governance/current-status.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["latest_review"]["decision"] = "changes_requested"
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = validate(Path(temp.name), True, True, True)
        self.assertTrue(any("requires current status changes_requested" in item for item in errors))

    def test_unregistered_command_fails(self) -> None:
        temp = self.make_project()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "governance/architecture/command-registry.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["commands"] = data["commands"][:1]
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = validate(Path(temp.name), True, True, True)
        self.assertTrue(any("unregistered cmd entry" in item for item in errors))


if __name__ == "__main__":
    unittest.main()

