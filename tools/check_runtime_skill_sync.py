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
)

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
    "one-person-openspec-rd",
    "hatch-pet",
    "tdx-automation",
)


def normalized(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(normalized(path)).hexdigest()


def validate_runtime_skills(
    canonical_dir: Path, runtime_skills_root: Path
) -> dict[str, object]:
    canonical_dir = canonical_dir.resolve()
    runtime_skills_root = runtime_skills_root.resolve()
    installed_dir = runtime_skills_root / "one-person-openspec-rd"
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
        help="Compatibility option: explicit installed one-person SKILL.md path.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    canonical_dir = root / "skills" / "one-person-openspec-rd"
    if args.runtime_skills_root:
        runtime_skills_root = Path(args.runtime_skills_root).expanduser().resolve()
    elif args.installed:
        runtime_skills_root = Path(args.installed).expanduser().resolve().parent.parent
    else:
        codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
        runtime_skills_root = codex_home / "skills"

    result = validate_runtime_skills(canonical_dir, runtime_skills_root)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        label = "PASS" if result["valid"] else "FAIL"
        print(
            f"RUNTIME_SKILL_SYNC={label} status={result['status']} "
            f"legacy_present={len(result['legacy_present'])} "
            f"preserved_missing={len(result['preserved_missing'])}"
        )
        for error in result["errors"]:
            print("ERROR " + str(error))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
