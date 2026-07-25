# Change: Define Audit Evidence Compliance Standard

## Why

Existing standards cover observability, trust commitments, support operations, admin actions, AI governance, async jobs, and webhooks. They do not yet define one focused standard for collecting, preserving, retaining, redacting, packaging, and reviewing audit evidence across these areas.

Without this standard, a solo founder may do the right work but fail to prove it later: release approvals get separated from commits, incident timelines live only in chat, AI eval evidence is detached from model routes, audit logs keep sensitive content too long, and customer security questionnaires are answered from memory instead of durable evidence.

## What

- Add a stage 35 standard for AI product audit, evidence preservation, and compliance evidence packages.
- Define five minimal artifacts under `audit-evidence/`.
- Require evidence register, audit log policy, evidence retention policy, evidence package, and audit review for production targets that need trust, security, AI, operational, billing, support, admin, or customer evidence.
- Define human checkpoints for external evidence sharing, sensitive evidence inclusion, legal hold/deletion exceptions, public trust/compliance claims, AI high-impact evidence, production data/admin evidence, incident disclosure, retention changes, audit-log integrity exceptions, and evidence export.
- Create `audit-evidence-compliance-guard` skill and verifier.

## Impact

- Go/Kratos/sqlc/gRPC systems get a clear audit event and evidence index pattern.
- Vite trust/admin surfaces get evidence package export and audit review expectations.
- AI workflows connect evals, model routes, traces, human reviews, and safety findings to evidence packages without storing raw customer content.
- The solo founder reviews only high-risk disclosure, retention, legal, and sensitive-data choices; artifact completeness, required fields, sensitive-content screening, and positive/negative validation are automated.
