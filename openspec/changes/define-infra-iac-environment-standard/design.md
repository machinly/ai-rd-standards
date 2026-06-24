# Design: Infra IaC Environment Standard

## Context

Release pipelines and runtime configuration are not enough to make production infrastructure reproducible. A production target also needs an environment map, a resource inventory, an IaC source of truth, state backend rules, plan/apply gates, drift review, and decommissioning procedures.

The one-person-company default avoids premature platform engineering. Terraform/OpenTofu, cloud-native IaC, Vercel project configuration, and Kubernetes declarative configuration are acceptable, but only when the current target records state ownership, sensitive state boundaries, plan/apply flow, and manual-change handling.

## Decisions

- Use `infra/` as the infrastructure governance folder.
- Require five artifacts per production target:
  - `environment-map/<target>.json`
  - `resource-inventory/<target>.json`
  - `iac-change-policy/<target>.md`
  - `provisioning-runbook/<target>.md`
  - `drift-review/<target>.md`
- Treat cloud console changes as exceptions that must be recorded, reconciled, and either reverted or backported to IaC.
- Treat state and plan files as sensitive by default.
- Keep human attention on production apply/destroy, critical resources, public exposure, IAM/secrets, state migration, manual drift acceptance, backup/encryption/monitoring reductions, and high-cost platforms.

## Alternatives Considered

- Require Kubernetes/GitOps for all targets: too heavy for early one-person products.
- Keep infra governance inside release pipeline artifacts: release gates do not express state backends, cloud resources, environment parity, or drift well enough.
- Allow console-first infrastructure until scale: fast initially, but it creates hidden state and weak recovery.
- Use a single generic operations checklist: too vague for destructive infra changes, state files, and environment boundaries.

## Rollout

1. Add the stage 37 standard and OpenSpec spec.
2. Create `infra-iac-environment-guard`.
3. Add a verifier for required files, environment/resource JSON fields, required markdown headings, human checkpoints, sensitive state patterns, and positive/negative fixture behavior.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture and remove it.
