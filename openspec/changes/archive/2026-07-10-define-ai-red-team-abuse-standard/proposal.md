# Change: Define AI Red Team Abuse Standard

## Why

The existing standards define AI prompt/eval workflows, data governance, security baselines, support feedback, admin action safety, and trust claims. They do not yet define the minimum process for AI-specific red teaming and abuse-risk management.

Without a dedicated standard, a solo founder can easily treat red teaming as a few ad hoc jailbreak attempts. That misses prompt injection, indirect prompt injection, sensitive information disclosure, insecure output handling, excessive agency, tool misuse, retrieval poisoning, cost abuse, and user reporting loops.

## What

- Add a stage 27 standard for AI red team, abuse cases, adversarial cases, mitigations, and safety release review.
- Define five minimal artifacts under `ai-safety/`.
- Require abuse-case registers, red-team plans, adversarial JSONL cases, mitigation maps, and safety release reviews for user-visible AI capabilities.
- Define release decisions and human checkpoints for unresolved high-risk findings, real attack payloads, external red-team disclosure, safety threshold changes, and high-permission agents.
- Create `ai-red-team-abuse-guard` skill and verifier.

## Impact

- AI safety findings become connected to release gates, mitigations, eval evidence, owners, and incident/support workflows.
- Prompt/model/tool/RAG/agent changes can cite abuse cases and adversarial cases.
- Go/Kratos/sqlc/gRPC services get a safety decision and telemetry contract.
- Vite review surfaces get a compact, auditable safety-review contract.
- The solo founder reviews only high-impact safety decisions; structure and formatting are automated.
