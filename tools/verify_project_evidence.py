#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

STATUS_VALUES = {
    "in_progress",
    "independent_review",
    "changes_requested",
    "accepted",
    "stopped",
    "terminated",
}
REVIEW_DECISIONS = {"accepted", "changes_requested", "rejected"}
MAP_FIELDS = {
    "top_level",
    "read_first",
    "runtime_processes",
    "common_commands",
    "canonical_sources",
    "governance_domains",
}
COMMAND_FIELDS = {
    "path",
    "purpose",
    "kind",
    "environment",
    "lifecycle",
    "starter",
    "dependencies",
    "privileges",
    "data_writes",
    "failure_recovery",
    "retirement",
}
JOURNEY_FIELDS = {
    "id",
    "role",
    "goal",
    "preconditions",
    "steps",
    "success",
    "failure",
    "evidence_level",
    "command",
    "evidence",
    "status",
    "last_run_at",
}
IGNORED_TOP_LEVEL = {".git", ".local", "node_modules"}


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing {path}")
        return None
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path}: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"JSON root must be an object: {path}")
        return None
    return data


def nonempty(value: Any) -> bool:
    return value not in (None, "", [], {})


def check_project_map(root: Path, errors: list[str]) -> None:
    governance = root / "governance"
    if not (governance / "README.md").is_file():
        errors.append("missing governance/README.md")
    path = governance / "project-map.json"
    data = load_json(path, errors)
    if data is None:
        return
    for field in MAP_FIELDS:
        if not nonempty(data.get(field)):
            errors.append(f"governance/project-map.json missing {field}")

    top_level = data.get("top_level")
    mapped: dict[str, dict[str, Any]] = {}
    if isinstance(top_level, list):
        for index, item in enumerate(top_level):
            if not isinstance(item, dict):
                errors.append(f"project-map top_level[{index}] must be an object")
                continue
            for field in ("path", "kind", "purpose"):
                if not nonempty(item.get(field)):
                    errors.append(f"project-map top_level[{index}] missing {field}")
            item_path = str(item.get("path", "")).replace("\\", "/").strip("/")
            if item_path:
                if item_path in mapped:
                    errors.append(f"duplicate top-level map path: {item_path}")
                mapped[item_path] = item
            if item.get("kind") == "governance" and not item_path.startswith("governance"):
                errors.append(f"governance artifact directory must live under governance/: {item_path}")
    actual = {
        item.name
        for item in root.iterdir()
        if item.is_dir() and item.name not in IGNORED_TOP_LEVEL and not item.name.startswith(".")
    }
    for missing in sorted(actual - set(mapped)):
        errors.append(f"unmapped top-level directory: {missing}")

    domains = data.get("governance_domains")
    registered: set[str] = set()
    if isinstance(domains, list):
        for index, item in enumerate(domains):
            if not isinstance(item, dict):
                errors.append(f"project-map governance_domains[{index}] must be an object")
                continue
            for field in ("name", "path", "owner", "trigger", "decision_or_gate", "retention"):
                if not nonempty(item.get(field)):
                    errors.append(f"project-map governance_domains[{index}] missing {field}")
            domain_path = str(item.get("path", "")).replace("\\", "/").strip("/")
            if domain_path:
                if not domain_path.startswith("governance/"):
                    errors.append(f"registered governance domain is outside governance/: {domain_path}")
                registered.add(domain_path)
                if not (root / domain_path).is_dir():
                    errors.append(f"registered governance domain does not exist: {domain_path}")
    if governance.is_dir():
        actual_domains = {
            rel(item, root)
            for item in governance.iterdir()
            if item.is_dir()
        }
        for missing in sorted(actual_domains - registered):
            errors.append(f"unregistered governance domain: {missing}")

    for field in ("read_first", "canonical_sources"):
        values = data.get(field)
        if isinstance(values, list):
            for value in values:
                candidate = root / str(value)
                if not candidate.exists():
                    errors.append(f"project-map {field} path does not exist: {value}")


def check_current_status(root: Path, errors: list[str]) -> None:
    path = root / "governance" / "current-status.json"
    data = load_json(path, errors)
    if data is None:
        return
    for field in ("status", "target_revision", "updated_at", "latest_review"):
        if not nonempty(data.get(field)):
            errors.append(f"governance/current-status.json missing {field}")
    status = data.get("status")
    if status not in STATUS_VALUES:
        errors.append(f"invalid current status: {status}")
    review = data.get("latest_review")
    if not isinstance(review, dict):
        errors.append("current-status latest_review must be an object")
        return
    for field in ("path", "decision", "target_revision"):
        if not nonempty(review.get(field)):
            errors.append(f"current-status latest_review missing {field}")
    decision = review.get("decision")
    if decision not in REVIEW_DECISIONS:
        errors.append(f"invalid latest review decision: {decision}")
    if review.get("path") and not (root / str(review["path"])).is_file():
        errors.append(f"latest review path does not exist: {review['path']}")
    if data.get("target_revision") != review.get("target_revision"):
        errors.append("current status and latest review target_revision differ")
    expected = {
        "accepted": "accepted",
        "changes_requested": "changes_requested",
        "rejected": "changes_requested",
    }.get(str(decision))
    if expected and status != expected:
        errors.append(f"latest review {decision} requires current status {expected}, found {status}")


def check_journeys(root: Path, require_browser_e2e: bool, errors: list[str]) -> None:
    path = root / "governance" / "quality" / "user-journeys.json"
    data = load_json(path, errors)
    if data is None:
        return
    journeys = data.get("journeys")
    if not isinstance(journeys, list) or not journeys:
        errors.append("user-journeys journeys must be a non-empty list")
        return
    seen: set[str] = set()
    browser_pass = False
    for index, journey in enumerate(journeys):
        if not isinstance(journey, dict):
            errors.append(f"journeys[{index}] must be an object")
            continue
        for field in JOURNEY_FIELDS:
            if not nonempty(journey.get(field)):
                errors.append(f"journeys[{index}] missing {field}")
        journey_id = str(journey.get("id", ""))
        if journey_id in seen:
            errors.append(f"duplicate journey id: {journey_id}")
        seen.add(journey_id)
        level = journey.get("evidence_level")
        if level == "browser-e2e":
            if journey.get("business_actions_via_ui") is not True:
                errors.append(f"journeys[{index}] browser-e2e must execute business actions through UI")
            if journey.get("api_used_for_setup_only") is not True:
                errors.append(f"journeys[{index}] browser-e2e may use API only for setup")
            assertions = journey.get("assertions")
            if not isinstance(assertions, dict) or not assertions.get("ui") or not assertions.get("business_state"):
                errors.append(f"journeys[{index}] browser-e2e needs UI and business-state assertions")
            artifacts = journey.get("failure_artifacts")
            if not isinstance(artifacts, list) or not {"trace", "screenshot", "video"}.intersection(map(str, artifacts)):
                errors.append(f"journeys[{index}] browser-e2e needs failure trace/screenshot/video")
            if not nonempty(journey.get("clean_environment_command")):
                errors.append(f"journeys[{index}] browser-e2e needs clean_environment_command")
            browser_pass = browser_pass or journey.get("status") == "pass"
        elif level not in {"manual-browser-check", "component", "host-integration"}:
            errors.append(f"journeys[{index}] invalid evidence_level: {level}")
    if require_browser_e2e and not browser_pass:
        errors.append("accepted scope requires at least one current browser-e2e journey pass")


def find_cmd_dirs(root: Path) -> set[str]:
    result: set[str] = set()
    for cmd_root in root.rglob("cmd"):
        if not cmd_root.is_dir() or any(part in {".git", "node_modules", "governance"} for part in cmd_root.parts):
            continue
        for item in cmd_root.iterdir():
            if item.is_dir():
                result.add(rel(item, root))
    return result


def check_command_registry(root: Path, required: bool, errors: list[str]) -> None:
    cmd_dirs = find_cmd_dirs(root)
    if not required and len(cmd_dirs) <= 1:
        return
    path = root / "governance" / "architecture" / "command-registry.json"
    data = load_json(path, errors)
    if data is None:
        return
    commands = data.get("commands")
    if not isinstance(commands, list) or not commands:
        errors.append("command-registry commands must be a non-empty list")
        return
    registered: list[str] = []
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            errors.append(f"command-registry commands[{index}] must be an object")
            continue
        for field in COMMAND_FIELDS:
            if not nonempty(command.get(field)):
                errors.append(f"command-registry commands[{index}] missing {field}")
        if command.get("path"):
            registered.append(str(command["path"]).replace("\\", "/").strip("/"))
    if len(registered) != len(set(registered)):
        errors.append("command-registry paths must be unique")
    for missing in sorted(cmd_dirs - set(registered)):
        errors.append(f"unregistered cmd entry: {missing}")


def validate(root: Path, require_journeys: bool, require_browser_e2e: bool, require_commands: bool) -> list[str]:
    errors: list[str] = []
    if not root.is_dir():
        return [f"project root is not a directory: {root}"]
    if not (root / "README.md").is_file():
        errors.append("missing root README.md")
    check_project_map(root, errors)
    check_current_status(root, errors)
    if require_journeys or require_browser_e2e:
        check_journeys(root, require_browser_e2e, errors)
    check_command_registry(root, require_commands, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify project governance navigation, current status, user journeys and command registry.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--require-user-journeys", action="store_true")
    parser.add_argument("--require-browser-e2e", action="store_true")
    parser.add_argument("--require-command-registry", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate(
        root,
        args.require_user_journeys,
        args.require_browser_e2e,
        args.require_command_registry,
    )
    payload = {
        "ok": not errors,
        "root": str(root),
        "errors": errors,
        "evidence_boundary": "static artifact/path/status contract only; does not prove browser execution, usability, code-comment quality, or independent review",
    }
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("PROJECT_EVIDENCE=" + ("PASS" if not errors else "FAIL"))
        for error in errors:
            print("ERROR: " + error)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

