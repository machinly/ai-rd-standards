#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


ROUTER_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/workflow-map.md",
    "references/stack-defaults.md",
    "references/review-rubric.md",
    "references/superpowers-scope.md",
)
RUNTIME_SKILL_NAME = "opc-rd"

SUPERPOWERS_SCOPE_START = "<!-- rd-standards:superpowers-scope:start -->"
SUPERPOWERS_SCOPE_END = "<!-- rd-standards:superpowers-scope:end -->"

LEGACY_RD_SKILLS = (
    "accessibility-ai-ux-guard",
    "admin-ops-action-guard",
    "ai-coding-workflow-guard",
    "ai-dataset-eval-data-guard",
    "ai-memory-context-guard",
    "ai-model-optimization-guard",
    "ai-model-routing-guard",
    "ai-prompt-eval-loop",
    "ai-quality-regression-guard",
    "ai-red-team-abuse-guard",
    "ai-tool-runtime-guard",
    "analytics-experiment-guard",
    "api-contract-compatibility-guard",
    "architecture-boundary-guard",
    "async-job-worker-guard",
    "audit-evidence-compliance-guard",
    "auth-boundary-guard",
    "backup-recovery-continuity-guard",
    "billing-entitlement-metering-guard",
    "commercial-contract-guard",
    "config-flag-runtime-guard",
    "content-safety-moderation-guard",
    "cost-capacity-guard",
    "credential-secret-lifecycle-guard",
    "customer-data-lifecycle-guard",
    "customer-launch-onboarding-guard",
    "customer-support-trust-ops-guard",
    "data-migration-guard",
    "dev-workspace-automation-guard",
    "developer-experience-docs-guard",
    "event-webhook-integration-guard",
    "external-claim-evidence-guard",
    "go-kratos-sqlc-service",
    "infra-iac-environment-guard",
    "ip-license-provenance-guard",
    "knowledge-context-recovery-guard",
    "localization-locale-ai-guard",
    "maintenance-dependency-debt-guard",
    "notification-messaging-guard",
    "observability-telemetry-guard",
    "one-person-openspec-rd",
    "open-source-maintainer-guard",
    "performance-load-regression-guard",
    "processor-transfer-guard",
    "product-discovery-learning-loop",
    "quality-test-strategy-guard",
    "rag-retrieval-source-guard",
    "release-pipeline-gates",
    "resilience-fault-injection-guard",
    "roadmap-prioritization-guard",
    "security-incident-response-guard",
    "security-privacy-supply-chain-guard",
    "sre-lite-ops",
    "trust-policy-compliance-guard",
    "vite-geist-frontend",
)

PRESERVED_RUNTIME_SKILLS = (
    ".system",
    RUNTIME_SKILL_NAME,
    "hatch-pet",
    "tdx-automation",
)


def normalized(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(normalized(path)).hexdigest()


def normalized_text(path: Path) -> str:
    return normalized(path).decode("utf-8")


def managed_scope_block(text: str) -> tuple[str | None, str | None]:
    start_count = text.count(SUPERPOWERS_SCOPE_START)
    end_count = text.count(SUPERPOWERS_SCOPE_END)
    if start_count != 1 or end_count != 1:
        return None, (
            "Expected exactly one paired Superpowers scope marker block, "
            f"found start={start_count} end={end_count}"
        )

    start = text.index(SUPERPOWERS_SCOPE_START)
    end = text.index(SUPERPOWERS_SCOPE_END)
    if end < start:
        return None, "Superpowers scope end marker appears before start marker"
    end += len(SUPERPOWERS_SCOPE_END)
    return text[start:end], None


def validate_global_agents(
    canonical_scope: Path, global_agents: Path
) -> dict[str, object]:
    canonical_scope = canonical_scope.resolve()
    global_agents = global_agents.expanduser().resolve()
    errors: list[str] = []
    canonical_block: str | None = None
    global_block: str | None = None

    if not canonical_scope.is_file():
        errors.append(f"Missing canonical Superpowers scope: {canonical_scope}")
    else:
        canonical_block, marker_error = managed_scope_block(
            normalized_text(canonical_scope)
        )
        if marker_error:
            errors.append(f"Invalid canonical Superpowers scope: {marker_error}")

    if not global_agents.is_file():
        errors.append(f"Missing global AGENTS.md: {global_agents}")
    else:
        global_block, marker_error = managed_scope_block(normalized_text(global_agents))
        if marker_error:
            errors.append(f"Invalid global Superpowers scope: {marker_error}")

    matches = (
        canonical_block is not None
        and global_block is not None
        and canonical_block == global_block
    )
    if canonical_block is not None and global_block is not None and not matches:
        errors.append("Global Superpowers scope differs from canonical managed block")

    return {
        "valid": not errors,
        "status": "synced" if not errors else "invalid",
        "canonical_scope": str(canonical_scope),
        "global_agents": str(global_agents),
        "matches": matches,
        "errors": errors,
    }


def validate_runtime_skills(
    canonical_dir: Path, runtime_skills_root: Path
) -> dict[str, object]:
    canonical_dir = canonical_dir.resolve()
    runtime_skills_root = runtime_skills_root.resolve()
    installed_dir = runtime_skills_root / RUNTIME_SKILL_NAME
    errors: list[str] = []
    file_results: list[dict[str, object]] = []

    for rel in ROUTER_FILES:
        canonical = canonical_dir / rel
        installed = installed_dir / rel
        canonical_exists = canonical.is_file()
        installed_exists = installed.is_file()
        matches = (
            canonical_exists
            and installed_exists
            and sha256(canonical) == sha256(installed)
        )
        file_results.append(
            {
                "path": rel,
                "canonical_exists": canonical_exists,
                "installed_exists": installed_exists,
                "matches": matches,
            }
        )
        if not canonical_exists:
            errors.append(f"Missing canonical router file: {rel}")
        elif not installed_exists:
            errors.append(f"Missing installed router file: {rel}")
        elif not matches:
            errors.append(f"Installed router differs from canonical: {rel}")

    legacy_present = sorted(
        name for name in LEGACY_RD_SKILLS if (runtime_skills_root / name).exists()
    )
    preserved_missing = sorted(
        name
        for name in PRESERVED_RUNTIME_SKILLS
        if not (runtime_skills_root / name).is_dir()
    )
    errors.extend(f"Retired R&D skill is still installed: {name}" for name in legacy_present)
    errors.extend(f"Required preserved runtime skill is missing: {name}" for name in preserved_missing)

    return {
        "valid": not errors,
        "status": "synced" if not errors else "invalid",
        "canonical_dir": str(canonical_dir),
        "runtime_skills_root": str(runtime_skills_root),
        "installed_dir": str(installed_dir),
        "router_files": file_results,
        "legacy_present": legacy_present,
        "preserved_missing": preserved_missing,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify the single canonical R&D skill, its installed copy, and removal "
            "of the retired R&D skill set."
        )
    )
    parser.add_argument("root", nargs="?", default=".", help="Repository root.")
    parser.add_argument(
        "--runtime-skills-root",
        help="Codex runtime skills directory; defaults to CODEX_HOME/skills.",
    )
    parser.add_argument(
        "--installed",
        help="Compatibility option: explicit installed opc-rd SKILL.md path.",
    )
    parser.add_argument(
        "--global-agents",
        help="User-level AGENTS.md; defaults to CODEX_HOME/AGENTS.md.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    canonical_dir = root / "skills" / RUNTIME_SKILL_NAME
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    if args.runtime_skills_root:
        runtime_skills_root = Path(args.runtime_skills_root).expanduser().resolve()
    elif args.installed:
        runtime_skills_root = Path(args.installed).expanduser().resolve().parent.parent
    else:
        runtime_skills_root = codex_home / "skills"

    if args.global_agents:
        global_agents = Path(args.global_agents).expanduser().resolve()
    else:
        global_agents = codex_home / "AGENTS.md"

    result = validate_runtime_skills(canonical_dir, runtime_skills_root)
    global_result = validate_global_agents(
        canonical_dir / "references" / "superpowers-scope.md",
        global_agents,
    )
    result["global_superpowers_scope"] = global_result
    result["errors"].extend(global_result["errors"])
    result["valid"] = not result["errors"]
    result["status"] = "synced" if result["valid"] else "invalid"
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        label = "PASS" if result["valid"] else "FAIL"
        print(
            f"RUNTIME_SKILL_SYNC={label} status={result['status']} "
            f"legacy_present={len(result['legacy_present'])} "
            f"preserved_missing={len(result['preserved_missing'])} "
            f"global_superpowers_scope={global_result['status']}"
        )
        for error in result["errors"]:
            print("ERROR " + str(error))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
