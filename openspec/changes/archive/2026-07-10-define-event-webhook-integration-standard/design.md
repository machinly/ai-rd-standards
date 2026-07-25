# Design: Event Webhook Integration Standard

## Context

Stage 18 defines API/event contract compatibility. Stage 22 covers billing-specific webhook ledger and reconciliation. Stage 32 defines AI tool runtime. Stage 33 defines async jobs and workers. Stage 34 connects these at the external event boundary: third-party deliveries enter through signed, deduped inbox records; outbound events leave through durable outbox records.

The design assumes a one-person company should not start with a large event platform. The first version should make each integration explicit, testable, observable, and safe to replay.

## Artifact Model

Each production integration boundary uses one stable `<target>` name:

```text
integrations/
  event-catalog/<target>.json
  webhook-contract/<target>.json
  delivery-runbook/<target>.md
  integration-test-plan/<target>.json
  integration-review/<target>.md
```

The split keeps review questions clear:

- event catalog: which providers, events, producers, consumers, schemas, delivery semantics, storage, and telemetry exist;
- webhook contract: how endpoints verify signatures, handle timestamp tolerance, dedupe, ordering, ack, inbox/outbox, retry, dead-letter, replay, payload, and secret rotation;
- delivery runbook: how to set up provider events, verify, receive, ack, persist, process, retry, replay, rotate secrets, and respond to incidents;
- integration test plan: how to prove signature verification, replay protection, dedupe, idempotency, schema validation, fast ack, inbox/outbox, retry, dead-letter, replay guard, redaction, degradation, and telemetry;
- integration review: how deliveries, duplicates, schema changes, inbox/outbox health, costs, incidents, and next improvements are reviewed.

## Default Architecture

The default one-person-company implementation is:

- inbound webhook endpoint verifies raw-body signatures before business parsing;
- endpoint persists a redacted inbox delivery with unique delivery/event/dedupe keys;
- endpoint returns fast success after validation and persistence;
- async worker processes inbox events through business usecases;
- outbound events are written to an outbox table in the same transaction as the business state change;
- dispatcher sends outbox events with idempotency keys and records attempts;
- dead letters and replays require impact summaries and checkpoints.

CloudEvents-like metadata is recommended for cross-system events, but the standard does not require adopting a broker or event platform before there is real operational need.

## Human Attention Budget

The verifier checks required files, headings, JSON fields, endpoint shape, event type fields, signature/timestamp/dedupe/outbox policies, required tests, telemetry, status enums, sensitive-content patterns, and checkpoint coverage. The human decides only:

- whether to add a new external provider, public endpoint, outbound webhook, broker, or customer event;
- whether inbound events can change money, rights, data, messages, tools, jobs, or config;
- whether outbound events can include sensitive data or AI output;
- whether missing signature verification, replay protection, dedupe, inbox/outbox, dead-letter, or replay guard can be accepted;
- whether to replay/delete/backfill events;
- whether to make breaking schema or semantic changes;
- whether to rotate secrets during incidents or handle duplicate side effects.

## Backend Fit

Go/Kratos services should keep webhook receipt, event normalization, inbox/outbox storage, and business processing as separate usecases. sqlc should own inbox/outbox and delivery attempt queries. gRPC and Protobuf remain the internal API boundary, while external webhooks stay HTTP by necessity.

## Frontend Fit

Vite integration/admin surfaces should show provider connection health, recent deliveries, failure categories, replay state, secret rotation state, scope, and data boundary. Dangerous replay/resend/disable actions require clear confirmation.

## Tradeoffs

- Postgres inbox/outbox is simpler than a broker, but needs worker discipline and retention cleanup.
- Fast ack improves provider reliability, but requires durable inbox and async processing.
- Signature verification can be provider-specific, but the artifact model keeps those differences explicit.
- Replay is useful for recovery, but dangerous when events have external side effects; it must be gated.
