# Change: Define AI Tool Runtime Standard

## Why

Existing standards cover prompt/eval workflow, red-team safety, model routing, admin operations, API contracts, auth boundaries, and AI UX. They do not yet define one focused contract for AI tool execution, external connectors, MCP servers, sandbox/code execution, approvals, idempotency, retry, audit, and tool output injection.

Without this standard, a model output can accidentally become a production action: writing data, sending messages, spending money, changing permissions, leaking data to a connector, executing code, or repeatedly retrying side effects during an outage.

## What

- Add a stage 32 standard for AI tool runtime, external connectors, and sandbox governance.
- Define five minimal artifacts under `ai-tools/`.
- Require tool registry, permission policy, execution runbook, tool test plan, and tool review for production AI tool capabilities.
- Define human checkpoints for new connectors/MCP servers, write/destructive/money/permission/message/code tools, sensitive data sharing, missing dry-run/rollback/idempotency/audit, tool-output-to-execution paths, autonomy expansion, and tool incidents.
- Create `ai-tool-runtime-guard` skill and verifier.

## Impact

- AI workflows gain an explicit runtime boundary: the model proposes tool calls, while the application owns execution, authorization, approval, idempotency, audit, and recovery.
- Go/Kratos/gRPC services get a concrete tool runtime contract and sqlc-backed records.
- Vite frontends get clear confirmation, connector consent, degraded-state, and rollback/compensation expectations.
- The solo founder reviews only high-risk tool and connector decisions; structure, fields, checks, status, and sensitive-content screening are automated.
