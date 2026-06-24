# Design: Audit Evidence Compliance Standard

## Context

Previous stages produce many useful artifacts: OpenSpec changes, SLOs, release gates, incident notes, migration plans, support records, admin action logs, trust claims, AI evals, red-team cases, model routing records, tool runtime policies, async job runbooks, and webhook ledgers. A one-person company needs a light way to connect these artifacts when answering customer, security, privacy, incident, or audit questions.

The design intentionally avoids enterprise GRC complexity. The standard defines a small evidence index and evidence package workflow. Raw systems of record stay where they belong: source control, CI, observability backend, database, ticket/support tool, provider dashboard, object storage, or controlled log archive.

## Decisions

- Use `audit-evidence/` as the durable evidence governance folder.
- Treat evidence as references plus integrity metadata, not copied sensitive data.
- Require five artifacts per production target:
  - `evidence-register/<target>.json`
  - `audit-log-policy/<target>.md`
  - `evidence-retention/<target>.json`
  - `evidence-package/<target>.md`
  - `audit-review/<target>.md`
- Require retention classes for operational, audit, security, and customer evidence.
- Require audit log fields that support actor/action/resource/outcome/request/trace/artifact correlation.
- Require AI evidence to reference prompt version, model route, eval run, trace id, safety decision, and human review where relevant.
- Put human attention only on disclosure, sensitive content, legal/retention exceptions, public claims, production data/admin evidence, incident disclosure, integrity exceptions, and external exports.

## Alternatives Considered

- Full GRC platform: too heavy before customer or regulatory pressure proves the need.
- Keep everything in logs: logs are expensive, sensitive, hard to read, and not designed as customer-ready evidence.
- Manual security questionnaire answers: fast once, unreliable over time.
- Store raw evidence copies in the repo: easy to review but unsafe for secrets, customer content, prompt/response data, and personal data.

## Rollout

1. Add the standard and OpenSpec spec.
2. Create `audit-evidence-compliance-guard`.
3. Add a verifier for required files, fields, headings, retention classes, audit log fields, human checkpoints, evidence domain coverage, and sensitive-content patterns.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture.
