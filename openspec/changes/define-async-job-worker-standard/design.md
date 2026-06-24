# Design: Async Job Worker Standard

## Context

Stage 5 defines SRE-lite operations. Stage 15 defines worker observability. Stage 19 defines local command automation. Stage 30 defines model routing. Stage 32 defines AI tool execution. Stage 33 connects these at the background execution layer: a user or AI workflow submits a durable job, workers process it with bounded concurrency and retry, and the product exposes clear status and recovery.

The design assumes a one-person company should not start with a large workflow platform. The first version should make async work explicit, testable, observable, and recoverable while keeping migration to managed queues possible.

## Artifact Model

Each production asynchronous workflow uses one stable `<target>` name:

```text
async-jobs/
  job-registry/<target>.json
  job-contract/<target>.json
  worker-runbook/<target>.md
  job-test-plan/<target>.json
  operations-review/<target>.md
```

The split keeps review questions clear:

- job registry: which queues, job types, schedules, workers, rate limits, retention, and telemetry exist;
- job contract: state machine, payload/result policy, idempotency, lease, retry, dead letter, cancellation, progress, user visibility, and retention;
- worker runbook: how enqueue, dequeue, lease, execute, retry, cancel, dead-letter, replay, observe, degrade, and respond to incidents;
- job test plan: how duplicates, leases, graceful shutdown, retries, dead letters, cancellation, stuck jobs, polling, telemetry, redaction, and AI cost limits are verified;
- operations review: backlog, latency, failures, retries, dead letters, cancellations, cost, user impact, incidents, and the next one improvement.

## Default Architecture

The default one-person-company implementation is:

- Go/Kratos service exposes explicit gRPC job APIs.
- PostgreSQL stores jobs, attempts, events, results, schedules, cancellations, dead letters, and idempotency keys.
- sqlc owns explicit claim, update, heartbeat, and status queries.
- Workers are separate process types with bounded concurrency, graceful shutdown, context deadlines, and kill switches.
- `FOR UPDATE SKIP LOCKED` may be used only to claim queue-like rows, with deterministic ordering and short transactions.
- External side effects go through idempotent adapters, outbox, or stage 32 tool runtime gates.

Managed queues, Temporal-style workflows, Kafka, Pub/Sub, Cloud Tasks, or Batch services are allowed when the job registry shows a real need: backlog, throughput, durability, scheduling, cost, or operational simplicity.

## Human Attention Budget

The verifier checks required files, headings, registry fields, job fields, state machine, finite retry, idempotency, lease, cancellation, data policy, telemetry, required test checks, status enums, sensitive-content patterns, and checkpoint coverage. The human decides only:

- whether to introduce a new durable queue, scheduler, workflow engine, Batch route, or provider;
- whether a core user path can become async;
- whether side-effecting jobs can retry or replay;
- whether missing idempotency, lease, dead letter, graceful shutdown, or stuck recovery can be accepted;
- whether job payload/result can store sensitive raw content;
- whether to increase concurrency, dispatch rate, retry, schedule frequency, or AI cost budget;
- whether to replay or delete dead letters;
- whether background/batch AI retention is acceptable for privacy-sensitive paths.

## Backend Fit

Go/Kratos services should expose job APIs through gRPC and store durable state through sqlc. Worker code should be restartable and stateless outside the database/queue. Lease/heartbeat and stuck recovery are required because worker processes can crash or be killed during deploys.

## Frontend Fit

Vite surfaces should treat long tasks as first-class UI states: queued, running, succeeded, failed, cancel requested, cancelled, expired, dead-lettered, or partial. Users should see a stable job id, last update, result location, retry/cancel availability, and next step.

## Tradeoffs

- A Postgres-backed queue is not a universal queue, but it is easy to review, migrate, back up, and query for a one-person company.
- Dead letters add workflow overhead, but they prevent infinite retry and preserve evidence for repair.
- Cancellation and progress fields take extra design, but they turn long AI work into a product experience instead of an opaque wait.
- Managed queues can reduce ops later, but choosing them before real pressure can add cost and vendor complexity.
