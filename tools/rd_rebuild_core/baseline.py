from __future__ import annotations

import fnmatch
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .model import CheckResult, ResultStatus, write_json_atomic


def canonical_path(value: str | Path) -> str:
    return str(value).replace("\\", "/").removeprefix("./")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_manifest_digest(entries: Iterable[dict[str, Any]]) -> str:
    normalized = sorted(
        (
            canonical_path(str(entry["path"])),
            str(entry["sha256"]).lower(),
        )
        for entry in entries
    )
    text = "\n".join(f"{path}\t{sha256}" for path, sha256 in normalized)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def tool_manifest_digest(entries: Iterable[dict[str, Any]]) -> str:
    normalized = sorted(
        (
            canonical_path(str(entry["path"])),
            str(entry["sha256"]).lower(),
        )
        for entry in entries
    )
    text = "\n".join(f"{path}\t{sha256}" for path, sha256 in normalized)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def capture_source_entries(root: Path, source_roots: Iterable[str]) -> list[dict[str, Any]]:
    root = root.resolve()
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for relative_root in source_roots:
        source_root = root / canonical_path(relative_root)
        if not source_root.is_dir():
            continue
        for path in sorted(item for item in source_root.rglob("*") if item.is_file()):
            relative = canonical_path(path.relative_to(root))
            if relative in seen:
                continue
            seen.add(relative)
            entries.append(
                {
                    "path": relative,
                    "size": path.stat().st_size,
                    "sha256": file_sha256(path),
                }
            )
    return sorted(entries, key=lambda item: item["path"])


def capture_tool_entries(root: Path, tool_paths: Iterable[str]) -> list[dict[str, Any]]:
    root = root.resolve()
    selected: dict[str, Path] = {}
    for raw_path in tool_paths:
        relative = canonical_path(raw_path)
        candidate = root / relative
        if candidate.is_file():
            selected[relative] = candidate
            continue
        if candidate.is_dir():
            for path in candidate.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts:
                    selected[canonical_path(path.relative_to(root))] = path
            continue
        if any(character in relative for character in "*?["):
            for path in root.glob(relative):
                if path.is_file() and "__pycache__" not in path.parts:
                    selected[canonical_path(path.relative_to(root))] = path
    return [
        {
            "path": relative,
            "size": path.stat().st_size,
            "sha256": file_sha256(path),
        }
        for relative, path in sorted(selected.items())
    ]


def verify_tool_manifest(root: Path, manifest: dict[str, Any]) -> CheckResult:
    expected_entries = manifest.get("files", [])
    findings: list[str] = []
    if manifest.get("status") != "verified":
        findings.append("frozen tool manifest is not verified")
    if not isinstance(expected_entries, list) or not expected_entries:
        findings.append("frozen tool manifest has no file entries")
        expected_entries = []
    expected_digest = str(manifest.get("aggregate_sha256", ""))
    calculated_digest = tool_manifest_digest(expected_entries)
    if not expected_digest:
        findings.append("frozen tool manifest has no aggregate digest")
    elif calculated_digest != expected_digest:
        findings.append("frozen tool manifest aggregate does not match its entries")
    for entry in expected_entries:
        relative = canonical_path(str(entry.get("path", "")))
        path = root.resolve() / relative
        if not relative or not path.is_file():
            findings.append(f"frozen tool missing: {relative or '<empty path>'}")
            continue
        if file_sha256(path) != str(entry.get("sha256", "")).lower():
            findings.append(f"frozen tool changed: {relative}")
    return CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "frozen tool verification",
        tuple(findings),
        {
            "tool_file_count": len(expected_entries),
            "tool_manifest_sha256": expected_digest,
        },
    )


def verify_source_entries(
    root: Path,
    expected_entries: Iterable[dict[str, Any]],
    source_roots: Iterable[str] | None = None,
) -> CheckResult:
    root = root.resolve()
    expected = {
        canonical_path(str(entry["path"])): entry for entry in expected_entries
    }
    findings: list[str] = []
    for relative, entry in sorted(expected.items()):
        path = root / relative
        if not path.is_file():
            findings.append(f"protected source missing: {relative}")
            continue
        actual = file_sha256(path)
        if actual != str(entry.get("sha256", "")).lower():
            findings.append(f"protected source changed: {relative}")
    if source_roots is not None:
        actual = {
            entry["path"]: entry
            for entry in capture_source_entries(root, source_roots)
        }
        for relative in sorted(set(actual) - set(expected)):
            findings.append(f"unregistered protected source: {relative}")
    status = ResultStatus.BLOCKED if findings else ResultStatus.PASS
    return CheckResult(
        status,
        "protected source verification",
        tuple(findings),
        {
            "expected_file_count": len(expected),
            "source_manifest_sha256": source_manifest_digest(expected.values()),
        },
    )


def path_matches(relative: str, rules: Iterable[str]) -> bool:
    path = canonical_path(relative)
    for raw_rule in rules:
        rule = canonical_path(raw_rule)
        if rule.endswith("/") and path.startswith(rule):
            return True
        if any(character in rule for character in "*?[") and fnmatch.fnmatchcase(
            path, rule
        ):
            return True
        if path == rule:
            return True
    return False


def _repository_paths(root: Path) -> list[str]:
    if (root / ".git").exists():
        process = subprocess.run(
            [
                "git",
                "-c",
                "core.quotepath=false",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
            ],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        )
        if process.returncode != 0:
            raise RuntimeError(process.stderr.strip() or "git ls-files failed")
        return sorted(
            {canonical_path(line) for line in process.stdout.splitlines() if line}
        )
    return sorted(
        canonical_path(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
    )


def capture_workspace_entries(
    root: Path, excluded_paths: Iterable[str]
) -> list[dict[str, Any]]:
    root = root.resolve()
    entries: list[dict[str, Any]] = []
    for relative in _repository_paths(root):
        if path_matches(relative, excluded_paths):
            continue
        path = root / relative
        exists = path.is_file()
        entries.append(
            {
                "path": relative,
                "exists": exists,
                "size": path.stat().st_size if exists else None,
                "sha256": file_sha256(path) if exists else None,
            }
        )
    return entries


def capture_git_status_lines(
    root: Path, excluded_paths: Iterable[str]
) -> list[str]:
    root = root.resolve()
    if not (root / ".git").exists():
        return []
    process = subprocess.run(
        [
            "git",
            "-c",
            "core.quotepath=false",
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
    )
    if process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or "git status failed")
    result: list[str] = []
    for line in process.stdout.splitlines():
        if len(line) < 4:
            continue
        prefix = line[:3]
        raw_paths = line[3:].split(" -> ")
        paths = [canonical_path(value) for value in raw_paths]
        if paths and all(path_matches(path, excluded_paths) for path in paths):
            continue
        result.append(prefix + " -> ".join(paths))
    return sorted(result)


def create_baseline(
    root: Path,
    policy: dict[str, Any],
    target: Path,
    *,
    dry_run: bool,
    kind: str,
) -> CheckResult:
    root = root.resolve()
    target = target.resolve()
    phase = "tooling" if kind == "tooling-bootstrap" else "content"
    allowed = policy.get("allowed_write_roots_by_phase", {}).get(phase, [])
    sources = capture_source_entries(root, policy.get("source_roots", []))
    tool_manifest: dict[str, Any] | None = None
    existing: dict[str, Any] = {}
    transition_allowed = False
    transition_findings: list[str] = []
    if kind == "content-frozen":
        if target.exists():
            try:
                existing = json.loads(target.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                transition_findings.append(f"existing baseline cannot be read: {exc}")
        else:
            transition_findings.append(
                "tooling-bootstrap baseline is required before content freeze"
            )
        governance = target.parent
        try:
            run_state = json.loads(
                (governance / "run-state.json").read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            transition_findings.append(f"G1 run state cannot be read: {exc}")
            run_state = {}
        try:
            tool_manifest = json.loads(
                (governance / "tool-manifest.json").read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            transition_findings.append(f"tool manifest cannot be read: {exc}")
            tool_manifest = {}
        if existing.get("kind") != "tooling-bootstrap":
            transition_findings.append(
                "content baseline can replace only a tooling-bootstrap baseline"
            )
        if run_state.get("current_state") != "tooling_ready":
            transition_findings.append("G1 approval state tooling_ready is required")
        if tool_manifest.get("status") != "verified" or not tool_manifest.get(
            "aggregate_sha256"
        ):
            transition_findings.append("verified tool manifest is required")
        else:
            transition_findings.extend(
                verify_tool_manifest(root, tool_manifest).findings
            )
        transition_allowed = not transition_findings
    manifest = {
        "schema_version": "1.0",
        "kind": kind,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "root": ".",
        "protected_sources": sources,
        "source_manifest_sha256": source_manifest_digest(sources),
        "existing_workspace": {
            "files": capture_workspace_entries(root, allowed),
            "git_status_lines": capture_git_status_lines(root, allowed),
        },
        "content_baseline_frozen": kind == "content-frozen",
        "reusable_for_gate": kind == "content-frozen",
    }
    plan_path = policy.get("plan_path")
    if plan_path:
        manifest["plan_path"] = plan_path
        resolved_plan = root / canonical_path(str(plan_path))
        manifest["plan_sha256"] = (
            file_sha256(resolved_plan) if resolved_plan.is_file() else None
        )
    if existing.get("g0"):
        manifest["g0"] = existing["g0"]
    if kind == "content-frozen":
        manifest["tool_manifest_sha256"] = (
            tool_manifest or {}
        ).get("aggregate_sha256")
    manifest["existing_workspace"]["file_count"] = len(
        manifest["existing_workspace"]["files"]
    )
    evidence = {
        "planned_read_count": len(sources),
        "planned_write": target.as_posix(),
        "kind": kind,
        "source_manifest_sha256": manifest["source_manifest_sha256"],
    }
    if dry_run:
        if kind == "content-frozen" and transition_findings:
            return CheckResult(
                ResultStatus.BLOCKED,
                "baseline create dry-run blocked",
                tuple(transition_findings),
                evidence,
            )
        return CheckResult(
            ResultStatus.PASS,
            "baseline create dry-run",
            evidence=evidence,
        )
    if transition_findings or (target.exists() and not transition_allowed):
        return CheckResult(
            ResultStatus.BLOCKED,
            "baseline creation blocked",
            tuple(transition_findings)
            or (f"baseline already exists and cannot be overwritten: {target}",),
            evidence,
        )
    write_json_atomic(target, manifest)
    return CheckResult(ResultStatus.PASS, "baseline created", evidence=evidence)
