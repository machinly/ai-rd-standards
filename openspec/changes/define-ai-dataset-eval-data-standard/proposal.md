# Change: Define AI Dataset Eval Data Standard

## Why

Existing AI workflow guidance covers prompts, eval runs, graders, agent behavior, safety checks, and release gates. It does not yet define the minimum governance for the datasets behind those evals: provenance, consent/license, privacy class, train/eval separation, labeling rubrics, quality checks, drift, and refresh cadence.

For a one-person AI company, unmanaged eval data creates hidden risk: metrics can improve because examples leaked into prompts or training, public data can violate terms, raw user prompts can be copied into repo artifacts, and failed cases can disappear without review.

## What

- Add a stage 26 standard for AI datasets, eval examples, labeling, quality reports, and refresh reviews.
- Define five minimal artifacts under `ai-data/`.
- Require dataset cards, JSONL eval sets, labeling guides, quality reports, and refresh reviews for AI capabilities used as release evidence.
- Define human checkpoints for real/sensitive data, unclear license, eval-to-training movement, third-party sharing, synthetic-only evidence, rubric/threshold changes, and deletion of failed eval cases.
- Create `ai-dataset-eval-data-guard` skill and verifier.

## Impact

- AI release gates become tied to versioned, reviewable data.
- Prompt/model/tool changes can cite dataset versions and quality reports.
- Go/Kratos/sqlc/gRPC services can store dataset metadata without leaking raw examples.
- Vite labeling/review surfaces get a compact, auditable data contract.
- The solo founder reviews only high-risk data decisions; structure and formatting are automated.
