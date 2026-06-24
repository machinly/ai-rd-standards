# W0-W9 AI R&D Workflow Map

Use this reference when the repository does not provide `docs/00-start-here.md` and `docs/00-standard-index.md`. If the repository has its own workflow docs, prefer the repository version.

## Steps

| Step | Question | Typical artifacts | Human checkpoint |
| --- | --- | --- | --- |
| W0 Intake | Should this be done now? | work-intake, decision-board | start now, expedite, park, kill, exceed appetite |
| W1 Discovery | Is this a real user/business problem? | product bet, metrics, evidence refs | target user, problem, success metric, weak evidence |
| W2 OpenSpec / Risk | What behavior, boundary, risk, and exit condition? | proposal, spec, design, tasks | product direction, data boundary, architecture lock-in |
| W3 AI Behavior | What AI behavior is good, bad, unsafe, or degraded? | prompt, eval fixtures, red-team cases, route policy | no-eval change, model/tool/RAG/memory change |
| W4 Build | How is the behavior implemented? | Go/Kratos/sqlc/gRPC, Vite, migration, config, coding batch | irreversible migration, production default, visible API/UI promise |
| W5 Verify | What evidence blocks or permits release? | tests, eval run, accessibility, performance, resilience | failed gate, accepted risk, quality regression |
| W6 Release | Can it be released, rolled back, or promised? | release checklist, smoke, rollback, launch readiness | production release, rollback, public/customer/SLA promise |
| W7 Operate | How is it observed and recovered? | SLO, dashboard, alert, runbook, incident, restore, rotation | incident escalation, customer/regulator notice, break-glass |
| W8 Learn | What did users, metrics, support, evals, and incidents teach? | learning decision, quality review, updated intake | continue, expand, park, kill, rollback, pivot |
| W9 Maintain | Can a human or Codex resume later? | docs map, context pack, freshness, debt, evidence | canonical source, terminology, archive/delete, stale doc accepted |

## Routing Heuristics

- New idea, request, customer ask, bug triage, or roadmap question: start at W0.
- User problem, metric, feedback, experiment, or evidence question: W1.
- Scope, requirements, architecture, API, security, privacy, cost, or data boundary: W2.
- Prompt, model, eval, RAG, tool, memory, red-team, or AI quality behavior: W3.
- Code, migration, Vite UI, Go service, config, worker, webhook, billing, notification: W4.
- Tests, eval run, accessibility, performance, resilience, release gate: W5.
- Deploy, launch, customer onboarding, public claim, contract, SLA: W6.
- SLO, alert, trace, incident, backup restore, credential rotation, break-glass: W7.
- Support feedback, analytics result, AI regression, post-incident learning, next roadmap decision: W8.
- Documentation, context recovery, dependency maintenance, audit evidence, open source maintenance: W9.

## Adjacent-Step Rule

Read the current step, the previous step input, and the next step gate. Avoid reading every standard unless the task is an audit of the standards repository itself.
