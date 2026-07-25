# Change: Define Async Job Worker Standard

## Why

Existing standards cover SRE-lite operations, observability, development automation, AI tool runtime, model routing, and admin actions. They do not yet define a focused contract for long-running AI tasks, queues, background workers, job states, leases, retries, dead letters, cancellation, replay, user-visible status, and worker graceful shutdown.

Without this standard, a long AI workflow can hide inside an HTTP request, goroutine, cron, prompt, or admin script. Failures then become ambiguous: duplicate side effects, lost jobs, infinite retries, stuck queues, unclear user status, background model costs, or unsafe dead-letter replay.

## What

- Add a stage 33 standard for AI async jobs, queues, and background workers.
- Define five minimal artifacts under `async-jobs/`.
- Require job registry, job contract, worker runbook, job test plan, and operations review for production asynchronous workflows.
- Define human checkpoints for new durable queues/providers, user-visible async core paths, side-effect retry/replay, missing idempotency/lease/dead-letter/graceful shutdown, sensitive payload retention, concurrency/cost expansion, and OpenAI background/batch privacy boundaries.
- Create `async-job-worker-guard` skill and verifier.

## Impact

- Go/Kratos/gRPC services get explicit job APIs, worker lifecycle rules, sqlc storage expectations, and queue claim semantics.
- AI workflows get bounded duration, cost, retry, fanout, status polling, cancellation, and result retention.
- Vite frontends get clear long-task states instead of indefinite loading.
- The solo founder reviews only high-risk async decisions; structure, state machine, fields, tests, sensitive-content screening, and checkpoint coverage are automated.
