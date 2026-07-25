# Change: Define AI Model Routing Provider Standard

## Why

Existing standards cover prompt/eval workflow, cost, configuration, observability, security, red-team, content safety, memory, and support. They do not yet define the explicit contract for model/provider routing, fallback, model migration, timeout/retry behavior, and route-level release evidence.

Without this standard, a one-person AI product can silently change behavior by editing a model name, provider URL, reasoning effort, or fallback branch. That creates quality regressions, cost spikes, latency incidents, privacy boundary changes, and unreviewed safety behavior changes.

## What

- Add a stage 30 standard for AI model routing, provider boundaries, fallback, eval gates, and provider review.
- Define five minimal artifacts under `ai-routing/`.
- Require route registry, route policy, fallback runbook, eval gate, and provider review for production AI capabilities.
- Define human checkpoints for production default route changes, new providers, sensitive data routes, safety behavior changes, high-permission tools, paid/high-risk fallback, budget expansion, no-fallback launches, and model deprecation.
- Create `ai-model-routing-guard` skill and verifier.

## Impact

- Model and provider choices become versioned product contracts, not scattered config strings.
- Go/Kratos/sqlc/gRPC services get a concrete `ModelRouter` and provider adapter boundary.
- Vite surfaces get explicit degraded-mode and background-task behavior.
- Prompt/eval artifacts connect to route-level quality, latency, cost, safety, and rollback evidence.
- The solo founder reviews only high-risk route decisions; structure and formatting are automated.
