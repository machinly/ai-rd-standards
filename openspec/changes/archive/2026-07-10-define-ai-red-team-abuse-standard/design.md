# Design: AI Red Team Abuse Standard

## Context

Stage 4 covers AI behavior changes and evals. Stage 26 covers dataset and eval data governance. Stage 27 focuses on adversarial discovery and abuse-risk handling before release.

The design intentionally avoids a heavy enterprise red-team program. It uses repo-native artifacts, short manual exercises, and a verifier that catches missing structure. High-risk decisions remain human-owned.

## Artifact Model

Each user-visible AI capability uses one stable `<capability>` name:

```text
ai-safety/
  abuse-case-register/<capability>.json
  red-team-plan/<capability>.md
  adversarial-cases/<capability>.jsonl
  mitigation-map/<capability>.md
  safety-release-review/<capability>.md
```

The split keeps each review question small:

- abuse case register: how can this be abused;
- red-team plan: what will be tested and under what rules;
- adversarial cases: which repeatable cases exercise safety behavior;
- mitigation map: which controls exist and where gaps remain;
- safety release review: can this version ship.

## Human Attention Budget

The verifier checks required files, headings, JSON shape, risk/status enums, sensitive-content patterns, human checkpoint coverage, and release-decision language. The human decides only:

- whether to ship with unresolved critical/high findings;
- whether to accept residual risk;
- whether to store real attack payloads, user harmful content, or vulnerability details;
- whether to invite external red-teamers or disclose findings;
- whether to change safety thresholds or policy boundaries;
- whether to allow high-permission tools or autonomous agents.

## Backend Fit

For Go/Kratos/sqlc/gRPC systems, safety decisions should be represented explicitly:

- `allow`
- `block`
- `review`
- `degrade`
- `rate-limit`
- `tool-deny`

Suggested tables:

- `ai_abuse_cases`
- `ai_safety_findings`
- `ai_safety_decisions`
- `ai_tool_safety_reviews`
- `ai_abuse_reports`

Every safety decision should be traceable to actor, tenant, capability, prompt version, model id, tool schema version, release id, and finding id where available.

## Frontend Fit

Vite safety review screens should be dense, not marketing-like. The reviewer needs severity, category, affected surface, mitigation status, owner, release decision, and linked evidence visible before changing status.

## Tradeoffs

- Storing redacted or synthetic adversarial prompts reduces replay fidelity, but keeps the repo safer. Full sensitive payloads require controlled storage and human approval.
- Manual red teaming is not systematic measurement. It should seed automated evals and stage 26 datasets.
- External red teaming is valuable but not a default one-person expense; use it for high-impact, specialized, or security-sensitive releases.
