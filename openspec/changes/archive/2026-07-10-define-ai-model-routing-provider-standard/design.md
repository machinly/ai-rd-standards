# Design: AI Model Routing Provider Standard

## Context

Stage 4 governs prompt/eval workflow. Stage 9 governs cost/capacity/vendor boundaries. Stage 14 governs runtime config and feature flags. Stage 15 governs telemetry. Stage 30 ties these together at the model route boundary: which model/provider is called, with which options, for which task, under which data boundary, and what happens when it fails.

The design assumes a one-person company should start with one primary model route per capability, one safe fallback, a kill switch, and route-level eval evidence. Multi-provider AI gateway behavior can come later only after the simple route is observable.

## Artifact Model

Each production AI capability uses one stable `<capability>` name:

```text
ai-routing/
  model-registry/<capability>.json
  route-policy/<capability>.md
  fallback-runbook/<capability>.md
  eval-gate/<capability>.json
  provider-review/<capability>.md
```

The split keeps review questions clear:

- model registry: what routes/providers exist and what the default is;
- route policy: how a route is selected and constrained;
- fallback runbook: what happens under rate limit, timeout, outage, schema failure, safety block, cost cap, or quality regression;
- eval gate: whether a candidate route may replace or supplement the baseline;
- provider review: whether quality, reliability, cost, safety, privacy, and provider terms remain acceptable.

## Human Attention Budget

The verifier checks required files, headings, JSON fields, route references, timeout/retry shape, fallback chains, telemetry keys, eval evidence, human checkpoints, and sensitive-content patterns. The human decides only:

- whether a production default model/provider/route changes;
- whether a new external provider or data retention boundary is acceptable;
- whether sensitive or high-impact data can use a route;
- whether safety/refusal behavior changes;
- whether tools or agentic routes get enabled;
- whether paid or high-risk flows may use lower-quality fallback;
- whether budget, context window, or reasoning defaults increase;
- whether a user-visible AI feature can ship without fallback;
- whether a production model snapshot can be removed.

## Backend Fit

Go/Kratos services should use a small route boundary:

- `ModelRouter.Select(ctx, request) -> Route`
- provider adapters hidden behind internal interfaces;
- sqlc tables for route versions, eval runs, fallback events, and provider events;
- gRPC errors that distinguish user, auth, capacity, provider, schema, safety, and internal failures;
- trace/log attributes that include route id, provider, model, prompt/workflow version, eval version, token/cost bucket, and fallback reason.

## Frontend Fit

Vite surfaces need:

- clear degraded-mode states;
- background/async states for slow routes;
- retry/cancel controls;
- honest but short user messaging;
- no supplier-internal error leakage.

## Tradeoffs

- Explicit route artifacts add small overhead, but prevent silent product behavior changes.
- A single provider is acceptable early, but must have a documented fallback or kill switch.
- The verifier cannot prove model quality; it verifies that model quality evidence exists and is linked.
- Latest-model recommendations change often, so artifacts store internal decisions and evidence instead of freezing external price/capability tables.
