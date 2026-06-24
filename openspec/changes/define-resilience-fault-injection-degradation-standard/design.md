# Design: Resilience Fault Injection Degradation Standard

## Context

Existing stages require SLOs, capacity limits, fallbacks, backup drills, async job tests, AI model routing, quality rollback, and performance gates. They do not define a lightweight way to prove that a fallback, timeout, retry budget, circuit breaker, degraded UI, or AI provider fallback actually works under a realistic failure.

For a one-person company, the risk is not failing to adopt a chaos platform. The risk is believing resilience exists because a runbook or config says it should. The standard keeps this lean by requiring five artifacts and a verifier.

## Decisions

- Use `resilience/` as the governance folder for failure-mode and degradation evidence.
- Require five artifacts per target:
  - `failure-mode-map/<target>.json`
  - `experiment-plan/<target>.md`
  - `fault-injection-run/<target>.json`
  - `degradation-check/<target>.md`
  - `resilience-review/<target>.md`
- Default to mock, staging, sandbox, tabletop, dependency stub, local proxy, or targeted contract fault injection.
- Treat production fault injection, real provider experiments, real data, real side effects, and expanded blast radius as human checkpoints.
- Keep this standard linked to SLO, capacity, continuity, AI route, async job, quality rollback, and performance artifacts instead of replacing them.

## Alternatives Considered

- Fold into SRE-lite: stage 5 defines runbooks and incident response, but not failure hypotheses, injection methods, blast radius, and degradation evidence.
- Fold into backup/continuity: stage 21 proves restore and continuity, but not day-to-day dependency failure behavior.
- Fold into performance: stage 52 validates budgets and load, but not failure injection, bad responses, timeouts, and degraded UX.
- Require continuous chaos engineering: too risky and expensive before scale; one maintainer needs small experiments with strong stop conditions.

## Rollout

1. Add the stage 53 standard and OpenSpec spec.
2. Create `resilience-fault-injection-guard`.
3. Add a verifier for required artifacts, markdown headings, JSON fields, allowed decisions, failure-mode semantics, high-risk checkpoints, degradation evidence, and sensitive content.
4. Validate a positive fixture and remove it.
5. Run OpenSpec and skill validation.
