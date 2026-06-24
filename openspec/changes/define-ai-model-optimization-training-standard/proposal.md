# Proposal: Define AI Model Optimization Training Standard

## Intent

Add stage 51: a one-person-company standard for AI model optimization, fine-tuning/distillation candidates, training data plans, optimization runs, validation reports, and rollout decisions.

## Scope

- Define required `ai-optimization/` artifacts for model optimization candidates.
- Cover optimization briefs, training data plans, optimization runs, validation reports, and rollout decisions.
- Connect prompt/eval, dataset governance, model routing, RAG, quality regression rollback, admin operations, and vendor/data-boundary checks.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Replacing prompt/eval development, dataset provenance, production route policy, RAG source governance, or AI quality incident rollback.
- Full MLOps platforms, continuous training, online learning, RLHF platforms, GPU cluster orchestration, or research-team training workflows.
- Storing raw customer data, raw prompts/responses, training examples, secrets, provider tokens, payment data, or regulated content in optimization artifacts.

## Sources

- The Mythical Man-Month and small project management.
- OpenAI model optimization, optimizing LLM accuracy, supervised fine-tuning, fine-tuning best practices, model selection, and current fine-tuning availability/deprecation guidance.
- Hidden Technical Debt in Machine Learning Systems and The ML Test Score.
- Google Rules of Machine Learning.
- NIST AI RMF and Generative AI Profile.
- Kratos, sqlc, gRPC, Vite, and Vercel design references.

## Human Attention

Keep human judgment only for:

- starting real fine-tuning, DPO/RFT, distillation, OSS adapter, or provider customization;
- using real customer data, raw prompts/responses, support tickets, production logs, customer files, regulated data, or unclear-rights data;
- moving eval, canary, red-team, or incident examples into training/preference data;
- accepting regressions in high-risk user journeys, safety/privacy, permissions, funds, legal, or medical contexts;
- moving a candidate model into shadow, small-cohort, or production routing;
- depending on legacy/deprecated/experimental provider training capability for core production behavior;
- increasing training budgets, expanding data retention, changing provider data boundaries, or deleting model/training evidence.
