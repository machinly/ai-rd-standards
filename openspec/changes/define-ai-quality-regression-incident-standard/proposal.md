# Proposal: Define AI Quality Regression Incident Standard

## Intent

Add stage 48: a one-person-company standard for detecting, triaging, rolling back, logging, and reviewing AI behavior quality regressions in production.

## Scope

- Define required `ai-quality/` artifacts for production AI capabilities.
- Cover quality signal contracts, regression triage, rollback runbooks, quality incident logs, and periodic quality reviews.
- Connect prompt/eval artifacts, observability, model routing, support feedback, release gates, and security/privacy incident escalation.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Replacing prompt/eval fixtures, dataset governance, model routing, observability, support, safety, or security incident response.
- Full MLOps platforms, online training, bandit optimization, automated model retraining, or large review councils.
- Storing raw prompts, responses, customer data, secrets, or sensitive regulated content in quality artifacts.

## Sources

- The Mythical Man-Month and small project management.
- Hidden Technical Debt in Machine Learning Systems and The ML Test Score.
- Google Rules of Machine Learning.
- Google SRE SLO, alerting, incident response, and postmortem practices.
- OpenAI evaluation best practices, evals, agent evals, and Agents tracing.
- OpenTelemetry GenAI semantic conventions.
- NIST AI RMF and Generative AI Profile.
- Kratos, sqlc, gRPC, Vite, and Vercel design references.

## Human Attention

Keep human judgment only for:

- declaring Q-SEV1/Q-SEV2, user notices, refunds/credits, public statements, or contract/SLA risk;
- continuing rollout, rolling back, disabling a core AI capability, falling back to lower quality, or moving work to humans;
- sampling raw prompt/response, support tickets, customer data, personal data, or regulated content;
- accepting eval failures, human review failures, or ongoing user complaints before release;
- changing safety/refusal/guardrail thresholds to improve apparent quality;
- adding incident examples to long-lived eval/dataset artifacts when they include customer content or unclear rights.
