# Proposal: Define Resilience Fault Injection Degradation Standard

## Intent

Add stage 53: a one-person-company standard for failure-mode maps, resilience experiment plans, fault-injection runs, degradation checks, and resilience reviews.

## Scope

- Define required `resilience/` artifacts for critical user journeys, Go/Kratos/gRPC services, sqlc/PostgreSQL paths, Vite degraded UI, AI workflows, workers, webhooks, RAG pipelines, and external dependencies.
- Cover failure hypotheses, steady-state signals, blast radius, injection method, safety controls, stop conditions, degradation evidence, run decisions, and one-next-experiment review.
- Connect SRE-lite operations, cost/capacity boundaries, testing strategy, backup/continuity, model routing, async jobs, AI quality rollback, and performance budgets.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Replacing SLOs, alerts, incident response, cost/capacity budgets, general test matrices, backup/restore drills, model routing, AI quality rollback, or performance regression gates.
- Enterprise chaos platforms, continuous production fault automation, region-wide experiments, real customer traffic chaos, or multi-team game-day programs.
- Storing raw payloads, raw prompts/responses, customer data, production logs, secrets, provider tokens, payment data, or regulated content in resilience artifacts.

## Sources

- The Mythical Man-Month and small project management.
- Google SRE Testing for Reliability, Addressing Cascading Failures, Handling Overload, Incident Response, and DiRT-style drills.
- Principles of Chaos Engineering.
- Release It! stability patterns.
- Building Secure and Reliable Systems fault injection.
- gRPC deadlines, Go context, Kratos circuit breaker, OpenAI rate limits, and AWS game days.
- Kratos, sqlc, gRPC, Vite, and Vercel design references.

## Human Attention

Keep human judgment only for:

- injecting faults in production, shared environments, real customer traffic, real customer data, real providers, or real paid AI providers;
- experiments that can trigger writes, funds, permissions, privacy, security, compliance, outbound messages, webhook side effects, or user notifications;
- accepting `accepted_risk`, shipping with gaps, skipping degradation verification, or expanding blast radius;
- automatic failover, provider switching, core-feature shutdown, or paid/high-risk degraded modes;
- weakening timeouts, rate limits, retry budgets, circuit breakers, backpressure, fallbacks, dead letters, or approvals;
- automating chaos/fault injection as a recurring production task.
