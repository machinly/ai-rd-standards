# Change: Define Event Webhook Integration Standard

## Why

Existing standards cover API contracts, billing webhook ledgers, AI tool runtime, and async workers. They do not yet define one focused standard for event catalogs, inbound/outbound webhooks, signature verification, replay protection, inbox/outbox, delivery attempts, event schema evolution, integration health, and safe manual replay.

Without this standard, a webhook can become an untrusted production write path: duplicate delivery, out-of-order state changes, unsigned requests, replay attacks, dual-write inconsistency, sensitive payload leakage, or repeated AI/tool side effects.

## What

- Add a stage 34 standard for event-driven, webhook, and external integration governance.
- Define five minimal artifacts under `integrations/`.
- Require event catalog, webhook contract, delivery runbook, integration test plan, and integration review for production integration boundaries.
- Define human checkpoints for new providers/endpoints, money/permission/data/external-message side effects, sensitive outbound data, missing verification/dedupe/inbox/outbox/dead-letter/replay guard, event replay, and breaking event schema changes.
- Create `event-webhook-integration-guard` skill and verifier.

## Impact

- Go/Kratos/sqlc/gRPC systems get a clear inbound webhook and outbound event pattern.
- Vite admin/integration surfaces get explicit status, replay, secret rotation, and incident states.
- AI workflows treat external events as untrusted inputs and connect event triggers to registered tools/jobs.
- The solo founder reviews only high-risk integration choices; structure, fields, signature/replay/dedupe/outbox checks, and sensitive-content screening are automated.
