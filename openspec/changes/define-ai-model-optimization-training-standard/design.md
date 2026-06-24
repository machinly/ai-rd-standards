# Design: AI Model Optimization Training Standard

## Context

Existing stages define prompt/eval artifacts, dataset governance, model route policy, RAG governance, and AI quality regression rollback. They do not define the narrow decision path for model optimization: when to fine-tune or distill, how to decide whether a failure is actually a data/context/prompt/route issue, how to run one optimization experiment, and how to decide whether the candidate model should ever reach production.

For a one-person company, the risk is not inability to train. The risk is starting model optimization too early and inheriting data governance, leakage, cost, provider availability, and rollback obligations without enough evidence. The standard keeps this lean by requiring five artifacts and a verifier.

## Decisions

- Use `ai-optimization/` as the governance folder for optimization candidates.
- Require five artifacts per capability:
  - `optimization-brief/<capability>.md`
  - `training-data-plan/<capability>.json`
  - `optimization-run/<capability>.json`
  - `validation-report/<capability>.md`
  - `rollout-decision/<capability>.md`
- Treat `no_training_baseline` as a valid method so the system can record “do not train” decisions.
- Require provider availability/deprecation checks because fine-tuning surfaces and model support change over time.
- Require rollout through model routing, not direct production substitution.

## Alternatives Considered

- Fold into dataset governance: stage 26 governs data provenance and quality, but not optimization go/no-go, training runs, validation reports, and rollout decisions.
- Fold into model routing: stage 30 governs production route behavior, but not whether a candidate model should be trained in the first place.
- Fold into AI quality incidents: stage 48 handles production regressions and rollback; optimization is a planned experiment, not incident response.
- Require a full MLOps platform: too heavy before scale; one maintainer needs artifacts, evals, and clear stop rules.

## Rollout

1. Add the stage 51 standard and OpenSpec spec.
2. Create `ai-model-optimization-guard`.
3. Add a verifier for required artifacts, markdown headings, JSON fields, allowed methods/decisions, high-risk checkpoints, train/eval separation, provider availability checks, and sensitive content.
4. Validate a positive fixture and remove it.
5. Run OpenSpec and skill validation.
