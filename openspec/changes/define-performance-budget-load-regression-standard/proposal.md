# Proposal: Define Performance Budget Load Regression Standard

## Intent

Add stage 52: a one-person-company standard for performance budgets, load profiles, benchmark plans, regression reports, and recurring performance reviews.

## Scope

- Define required `performance/` artifacts for user-visible services, frontend flows, AI workflows, database-heavy paths, workers, integrations, and high-risk changes.
- Cover latency, throughput, frontend Web Vitals, bundle size, database query plans, AI latency/token/tool loops, saturation, overload safety, and regression decisions.
- Connect SRE-lite SLOs, cost/capacity boundaries, test strategy, observability telemetry, model routing, and AI quality rollback.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Replacing SLOs, incident response, cost/capacity budgets, observability dashboards, general test matrices, AI model routing, or AI quality incident rollback.
- Enterprise performance labs, full load-testing platforms, production traffic replay systems, capacity forecasting platforms, continuous profiling platforms, or multi-team performance programs.
- Storing raw payloads, raw prompts/responses, customer data, production logs, secrets, provider tokens, or regulated content in performance artifacts.

## Sources

- The Mythical Man-Month and small project management.
- Google SRE Monitoring and Handling Overload.
- Brendan Gregg Systems Performance / USE Method.
- The Art of Capacity Planning.
- Go testing benchmarks and pprof.
- gRPC performance best practices.
- Web Vitals, PostgreSQL EXPLAIN, Vite Performance, and OpenAI Latency Optimization.
- Kratos, sqlc, gRPC, Vite, and Vercel design references.

## Human Attention

Keep human judgment only for:

- loosening p95/p99, Core Web Vitals, bundle, token, timeout, SLO, or saturation budgets;
- running load/stress/soak against production, real customer data, real paid AI providers, third-party APIs, or shared environments;
- accepting regressions, publishing `accepted_risk`, or releasing core paths with weak/unknown baselines;
- adding significant cloud resources, database indexes, caches, CDN, queues, provider priority, or model-serving cost;
- removing or weakening benchmark, load test, traces, timeouts, rate limits, fallback, backpressure, or release gates;
- releasing paid-customer, contractual-SLA, core-conversion, or high-risk AI paths with unknown performance.
