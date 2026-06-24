# Design: AI Quality Regression Incident Standard

## Context

Existing stages define AI prompt/eval artifacts, observability signals, release gates, model routing, support triage, and security/privacy incidents. They do not define one focused path for production AI behavior quality regressions: when quality drops, which signal matters, how to classify severity, how to roll back, what evidence to keep, and how to turn the incident into future eval coverage.

For a one-person company, the risk is not lack of tooling. The risk is noticing quality issues through scattered user complaints and then debugging from memory. The standard keeps this lean by requiring five artifacts and a small verifier.

## Decisions

- Use `ai-quality/` as the governance folder for AI quality operations.
- Require five artifacts per production AI capability:
  - `signal-contract/<capability>.json`
  - `regression-triage/<capability>.md`
  - `rollback-runbook/<capability>.md`
  - `incident-log/<capability>.json`
  - `quality-review/<capability>.md`
- Require at least one offline eval signal and one online production/user signal.
- Treat AI quality incidents as SRE-style incidents when users are affected, but escalate security/privacy/abuse/funds/permissions to the specialized stages.
- Store references and redacted summaries only.

## Alternatives Considered

- Fold into prompt/eval: evals catch many problems before release, but do not define production detection, severity, rollback, and incident logging.
- Fold into observability: telemetry says what happened, but not which quality thresholds require rollback or eval follow-up.
- Fold into model routing: routing handles provider/model fallback, but quality regression can also come from prompt, schema, retrieval, memory, tool behavior, guardrails, or dataset drift.
- Require full MLOps monitoring: too heavy before scale; the one-person default is artifacts plus focused signals.

## Rollout

1. Add the stage 48 standard and OpenSpec spec.
2. Create `ai-quality-regression-guard`.
3. Add a verifier for required JSON fields, markdown headings, signal coverage, severity/actions, high-risk checkpoints, and sensitive content.
4. Validate a positive fixture and remove it.
5. Run OpenSpec and skill validation.
