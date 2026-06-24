# Design: AI Dataset Eval Data Standard

## Context

Stage 4 introduced AI prompt/eval/agent workflow rules. Stage 10 and stage 25 cover privacy, suppliers, public promises, and compliance surfaces. Stage 26 fills the gap between those stages by governing the data that makes eval and model optimization meaningful.

The design follows a one-person constraint: do not introduce a data platform before there is evidence it is needed. Use repo-native artifacts first, keep raw sensitive data out of the repo, and make every release-relevant dataset easy to inspect.

## Artifact Model

Each release-relevant dataset uses one stable `<dataset>` name:

```text
ai-data/
  dataset-card/<dataset>.md
  eval-set/<dataset>.jsonl
  labeling-guide/<dataset>.md
  quality-report/<dataset>.json
  refresh-review/<dataset>.md
```

This structure separates the main review questions:

- dataset card: what is this data and can we use it;
- eval set: what examples are release evidence;
- labeling guide: how should examples be judged;
- quality report: is this data safe and representative enough for the current gate;
- refresh review: what changed and what one improvement matters next.

## Human Attention Budget

The verifier checks structure, fields, headings, enums, duplicates, sensitive-content patterns, and required checkpoints. The human decides only:

- real, sensitive, minor, or high-impact data use;
- unclear license/consent/provenance;
- eval case movement into training, fine-tuning, distillation, or prompt examples;
- third-party sharing or public dataset release;
- synthetic-only evidence for a high-risk release;
- rubric, grader, threshold, or benchmark changes;
- deletion, retirement, or downgrade of failed eval cases.

## Backend Fit

For Go/Kratos/sqlc/gRPC systems, the standard assumes application databases store metadata and references, not raw private examples. Suggested tables are:

- `ai_datasets`
- `ai_dataset_versions`
- `ai_eval_examples`
- `ai_label_reviews`
- `ai_data_quality_runs`

Release gates should reference dataset version/hash, eval run id, prompt version, model id, tool schema version, and release id.

## Frontend Fit

Vite review UIs should be dense and work-focused: source, privacy class, split, status, rubric, risk tags, and linked artifact visible near the reviewer action. Raw user content requires a separate permissioned path.

## Tradeoffs

- Repo-native JSON/JSONL is enough for early stages, but large datasets should move to controlled storage with hash references.
- The standard accepts small eval sets if they are high-quality and reviewed; breadth can grow after the first release evidence is trustworthy.
- Requiring all high-risk checkpoints in the quality report is slightly repetitive, but it keeps the release reviewer from hunting across docs.
