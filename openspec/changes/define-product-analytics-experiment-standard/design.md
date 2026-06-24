# Design: Product Analytics and Experiment Standard

## Context

Stage 11 defines product bets and learning loops, stage 15 defines observability, and stage 10 defines security/privacy. Stage 39 sits between them: it makes product analytics events, metric definitions, experiment assignment, privacy review, and data quality review concrete enough to implement and verify.

The one-person-company default is vendor-neutral. Start with a tracking plan, a typed frontend client, backend authoritative outcome events, a small event table or vendor destination, and a weekly data quality review. Avoid building a full experimentation platform until traffic and decision stakes justify it.

## Decisions

- Use `analytics/` as the governance folder for product analytics and experiments.
- Require five artifacts per target:
  - `tracking-plans/<target>.json`
  - `metrics-map/<target>.json`
  - `experiments/<target>.json`
  - `privacy-review/<target>.md`
  - `data-quality-review/<target>.md`
- Prefer backend-generated business outcome events and frontend-generated UI/experience events.
- Require controlled experiments to define assignment unit, targeting key policy, variants, exposure event, stop rule, trustworthiness checks, and rollback policy.
- Treat PII, raw prompt/response, free text, URL query, session replay, third-party analytics, and long retention as high-risk data boundaries.

## Alternatives Considered

- Reuse only `product/metrics`: too broad; it does not define event schema, destination, privacy review, or experiment trustworthiness.
- Fold into observability telemetry: product analytics asks product questions and often touches personal behavior; SRE telemetry asks health and debugging questions.
- Adopt a single vendor schema: premature; a one-person company should keep the durable contract in repo and use vendors as replaceable destinations.
- Autocapture everything: fast at first but high privacy, cost, and interpretation risk.

## Rollout

1. Add the stage 39 standard and OpenSpec spec.
2. Create `analytics-experiment-guard`.
3. Add a verifier for required analytics artifacts, event naming, property boundaries, metric maps, experiment trustworthiness checks, privacy review, data quality headings, and sensitive-content patterns.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture and remove it.
