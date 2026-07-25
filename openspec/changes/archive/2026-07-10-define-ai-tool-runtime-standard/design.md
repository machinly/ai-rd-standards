# Design: AI Tool Runtime Standard

## Context

Stage 4 defines prompt/eval workflow. Stage 8 defines auth and tenant boundaries. Stage 18 defines API/tool schema compatibility. Stage 24 defines manual admin actions. Stage 27 covers AI red-team and excessive agency. Stage 30 handles model routing. Stage 32 connects these at the execution boundary: a model may request a tool, but application code must decide whether and how the tool runs.

The design assumes a one-person company should not build a full agent platform first. The first version should make production AI tools explicit, bounded, testable, and recoverable.

## Artifact Model

Each production AI tool capability uses one stable `<capability>` name:

```text
ai-tools/
  tool-registry/<capability>.json
  permission-policy/<capability>.md
  execution-runbook/<capability>.md
  tool-test-plan/<capability>.json
  tool-review/<capability>.md
```

The split keeps review questions clear:

- tool registry: which tools and connectors exist, what side effects they have, and what runtime controls apply;
- permission policy: who can call what, under which tenant/data/connector boundary;
- execution runbook: how preflight, dry-run, approval, execution, idempotency, retry, rollback, audit, degradation, and incident handling work;
- tool test plan: how schema, auth, tenant, approval, dry-run, idempotency, rollback, timeout, rate limit, prompt injection, tool output, audit, and cost limits are verified;
- tool review: what changed, what was denied, which approvals were weak, where output injection or side effects appeared, and the next one improvement.

## Runtime Boundary

The application owns:

- schema validation and normalization;
- actor, tenant, capability, tool id, permission, scope, budget, rate limit, idempotency, approval, and deadline checks;
- connector grant storage and revocation;
- sandbox policy for code execution or local MCP;
- audit events and user-visible status;
- rollback, compensation, degradation, and kill switch.

The model owns only proposing a structured tool call and interpreting safe tool results within the allowed workflow.

## Human Attention Budget

The verifier checks required files, headings, JSON fields, side-effect enums, required tool fields, required test checks, human checkpoint coverage, output trust flags, retry/idempotency shape, telemetry fields, and sensitive-content patterns. The human decides only:

- whether to introduce a new connector, MCP server, local MCP, code execution, browser/computer-use, or third-party write surface;
- whether AI can trigger write, destructive, money, entitlement, admin, external-message, cross-tenant, or code-execution actions;
- whether to accept missing dry-run, rollback/compensation, idempotency, audit, or tests;
- whether sensitive data can be sent to a third party or broader scope can be granted;
- whether tool output can feed another execution surface;
- whether autonomy, loop/fanout/retry/budget, or kill-switch boundaries can change;
- whether a tool incident blocks release.

## Backend Fit

Go/Kratos services should expose a `ToolRuntime` or equivalent usecase. gRPC metadata carries actor, tenant, request id, tool run id, approval id, idempotency key, capability, and risk class, but the server recomputes authorization. sqlc records tool definitions, runs, approvals, audit events, connector grants, idempotency keys, and denials.

## Frontend Fit

Vite surfaces should show tool and connector consent in a dense workbench style: tool name, target, impact, dry-run result, approval state, scope, expiry, revoke action, and rollback/compensation. High-risk actions need concrete confirmation text, not generic warnings.

## Tradeoffs

- Approval and dry-run add friction, but only for tools that can create real damage.
- A small registry can feel redundant with code, but it gives AI coding agents and future-you a stable review surface.
- Local MCP and code execution can be powerful, but default sandboxing and explicit consent are cheaper than recovering from file, secret, or command exposure.
- One-person companies should start with a few high-impact tools rather than exhaustively cataloging every read-only helper.
