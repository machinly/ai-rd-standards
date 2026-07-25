# Design: Customer Data Portability Lifecycle Standard

## Context

Previous stages cover database changes, security/privacy records, backup recovery, webhook integrations, audit evidence, AI memory, RAG, and product analytics. Customer data import/export/sync/delete cuts across all of them and needs its own source of truth because a data rights request or migration request must locate data across primary stores, derived stores, third parties, AI/vector stores, logs, exports, caches, and backups.

The one-person-company default is small: keep a repo-level data map, use explicit transfer contracts, run imports/exports/deletions as auditable jobs, propagate tombstones to derived stores, and review the lifecycle regularly. Avoid buying or building a full data governance platform until customer volume or legal commitments require it.

## Decisions

- Use `customer-data/` as the governance folder for customer data portability and lifecycle operations.
- Require five artifacts per production target:
  - `data-map/<target>.json`
  - `transfer-contract/<target>.json`
  - `sync-runbook/<target>.md`
  - `rights-deletion-policy/<target>.json`
  - `lifecycle-review/<target>.md`
- Treat import files, sync payloads, and export packages as untrusted data boundaries.
- Treat deletion as a state machine over many targets, not a single SQL statement.
- Require AI/vector/cache/log/backup/third-party boundaries to be explicitly documented.

## Alternatives Considered

- Fold into data migrations: migration safety does not answer customer export, data portability, derived stores, third-party propagation, or user-facing deletion requests.
- Fold into privacy record: privacy records describe processing; they do not define operational schemas, sync cursors, job states, import validation, export artifacts, or tombstone propagation.
- Build a full data catalog: too heavy before volume and customer requirements justify it.
- Handle deletion synchronously: unsafe for large tenants, third-party propagation, AI/vector deletion, backups, and retryable failures.

## Rollout

1. Add the stage 40 standard and OpenSpec spec.
2. Create `customer-data-lifecycle-guard`.
3. Add a verifier for required files, data map fields, transfer contracts, sync runbook headings, rights/deletion policies, lifecycle review headings, required controls, and sensitive-content patterns.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture and remove it.
