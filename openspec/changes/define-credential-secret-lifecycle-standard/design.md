# Design: credential and secret lifecycle standard

## Decision

Add a narrow lifecycle layer under:

```text
credentials/
  inventory/<target>.json
  access-policy/<target>.md
  rotation-plan/<target>.md
  rotation-run/<target>.json
  exposure-review/<target>.md
```

This sits below broad security governance and above provider-specific secret-manager details. It records metadata, references, decisions, and evidence, never secret values.

## Artifact Shape

- `inventory`: machine-checkable list of credential references, owner, issuer, environment, consumer, scope, storage ref, injection path, rotation interval, revocation path, blast radius, and status.
- `access-policy`: human-readable access, least privilege, storage/injection, CI/CD, local dev, frontend boundary, audit, and review rules.
- `rotation-plan`: preconditions, dual-key/version strategy, steps, validation, rollback, revocation, communication, and evidence.
- `rotation-run`: JSON evidence of a completed or attempted rotation, validation, downtime, revoked old versions, decision, gaps, actions, and checkpoint.
- `exposure-review`: detection sources, findings, active exposure, revocation actions, impact, evidence, incident link, preventive controls, action items, and checkpoints.

## Human-Attention Defaults

The standard assumes Codex can create draft artifacts and run structural checks. The human decides only production rotation/revocation, accepted risk, frontend exposure, long-lived/cross-env credentials, real exposure, provider/customer notification, and inability to revoke or verify.

## Verifier

The skill verifier will check:

- required directory and file presence;
- JSON required keys and credential item keys;
- markdown required headings;
- no obvious secret values, private keys, connection strings, raw bearer tokens, payment data, raw prompts, or unredacted personal data;
- production or high-risk credentials have revocation path, rotation interval, storage ref, and human checkpoint;
- rotation runs with `revoked_old_versions=false`, risky decisions, gaps, or production reason have checkpoint and action coverage;
- exposure reviews with findings or active exposure have revocation actions and human checkpoint;
- Vite/client-exposed wording does not mark secrets as safe.

## Alternatives Considered

- Keep secrets inside stage 10 security baseline: too broad; it says what not to do but does not prove rotation and revocation readiness.
- Use only cloud secret-manager inventory: provider-specific, misses OpenAI/project keys, CI tokens, frontend boundaries, AI tool tokens, and local/dev workflows.
- Require enterprise Vault/PAM/HSM by default: too heavy for a one-person company and likely to become shelfware.

## Stack Notes

- Go/Kratos: load typed config from runtime sources; fail fast on missing required secret references.
- sqlc/PostgreSQL: never log connection strings or put production DSNs in migrations/tests.
- gRPC: attach call credentials only over protected channels and track service identity references.
- Vite: treat `VITE_*` as public; never place API keys or server credentials in browser bundles.
- AI workflows: keep provider keys and connector tokens out of prompts, eval fixtures, traces, RAG sources, support artifacts, and tool output.
