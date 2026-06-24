# Proposal: Define Product Analytics and Experiment Standard

## Intent

Add stage 39: a one-person-company standard for product analytics, event tracking, privacy-friendly experimentation, and data quality review.

## Scope

- Define required `analytics/` artifacts for each production target that collects product behavior or runs experiments.
- Require event tracking plans, metric definitions, experiment assignment/exposure records, privacy review, and data quality review.
- Connect Go/Kratos/sqlc/gRPC, Vite, AI workflows, OpenSpec, and product discovery artifacts.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Choosing or buying a specific analytics vendor.
- Building a data warehouse, BI platform, or experimentation platform.
- Replacing SRE telemetry, audit logs, billing ledgers, or product discovery artifacts.
- Providing legal advice.

## Sources

- The Mythical Man-Month, small project management, Lean Startup, Lean Analytics.
- Google HEART/GSM and Trustworthy Online Controlled Experiments.
- OpenTelemetry semantic conventions for events.
- W3C Privacy Principles, FTC personal information guidance, Google Analytics PII policy.
- Vite env docs, OpenFeature evaluation context, Segment/Snowplow/Amplitude tracking plan docs.

## Human Attention

Keep human judgment only for:

- third-party analytics, session replay, tag manager, advertising attribution, or cross-site tracking;
- personal behavior analytics, stable user identifiers, long retention, or cross-product data joins;
- primary metric changes;
- real-user experiment exposure and assignment-unit choices;
- SRM, guardrail, instrumentation, or privacy failures;
- using dashboard results for release, pricing, AI autonomy, marketing, or feature shutdown decisions.
