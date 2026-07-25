# Design: Performance Budget Load Regression Standard

## Context

Existing stages define SLOs, capacity boundaries, test strategy, observability, model routing, and AI quality rollback. They do not define a single path for deciding whether a change made a user journey slower, whether a target can handle expected load, or whether a regression should block release.

For a one-person company, the biggest risk is not missing an advanced profiler. The risk is shipping changes with no budget, no baseline, no load shape, and no explicit decision when p95, Web Vitals, DB time, or AI latency drifts. The standard keeps this lean by requiring five artifacts and a verifier.

## Decisions

- Use `performance/` as the governance folder for performance budgets and regression evidence.
- Require five artifacts per target:
  - `budget/<target>.json`
  - `load-profile/<target>.json`
  - `benchmark-plan/<target>.md`
  - `regression-report/<target>.json`
  - `performance-review/<target>.md`
- Treat early lab/staging baselines as acceptable when field data does not exist, but require the report to record baseline weakness.
- Require human checkpoints only for budget loosening, production/shared-environment load tests, accepted regressions, significant spend, weakened gates, and unknown-performance releases.
- Keep this standard linked to existing stages instead of replacing SLO, capacity, test, observability, route, or incident artifacts.

## Alternatives Considered

- Fold into SRE-lite: stage 5 defines SLOs and incident response, but not benchmark plans, load profiles, and release regression decisions.
- Fold into cost/capacity: stage 9 defines spending and capacity boundaries, but not user-facing performance budgets or regression evidence.
- Fold into test strategy: stage 12 defines test portfolios, but not performance budget semantics, Web Vitals, DB explain evidence, AI latency budgets, and accepted-risk gates.
- Require a full load-testing platform: too heavy before scale; one maintainer needs evidence files, commands, and clear stop rules first.

## Rollout

1. Add the stage 52 standard and OpenSpec spec.
2. Create `performance-load-regression-guard`.
3. Add a verifier for required artifacts, markdown headings, JSON fields, allowed decisions, high-risk checkpoints, budget/load/report semantics, and sensitive content.
4. Validate a positive fixture and remove it.
5. Run OpenSpec and skill validation.
