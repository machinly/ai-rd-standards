# Design: AI Memory Context Standard

## Context

Stage 4 covers AI prompt/eval workflow. Stage 25 covers public trust commitments. Stage 26 covers AI datasets. Stage 28 covers content moderation. Stage 29 governs the long-lived personalization and retrieval context that can silently change AI behavior across sessions.

The design assumes a one-person company should not start with a large personalization platform. The first version should be small, explicit, user-controllable, and easy to delete.

## Artifact Model

Each long-context AI capability uses one stable `<capability>` name:

```text
ai-memory/
  memory-policy/<capability>.md
  preference-schema/<capability>.json
  context-source-map/<capability>.md
  retrieval-rules/<capability>.json
  memory-review/<capability>.md
```

The split keeps review questions clear:

- memory policy: what may be remembered and under what controls;
- preference schema: what fields exist and how they are used;
- context source map: where long-term context comes from and who can access it;
- retrieval rules: what context may enter the model request;
- memory review: whether memory remains useful, correct, private, and deletable.

## Human Attention Budget

The verifier checks required files, headings, JSON fields, enums, TTLs, user controls, sensitivity, default injection, delete/export coverage, and sensitive-content patterns. The human decides only:

- whether long-term memory is default-on;
- whether sensitive or restricted memory can be saved or injected;
- whether AI can write inferred preferences;
- whether memory is reused for training, fine-tuning, evals, or supplier processing;
- whether context can cross user, tenant, workspace, or project boundaries;
- whether deletion leaves audit, cache, embedding, or conversation-state remnants;
- whether memory is used in high-impact domains.

## Backend Fit

Go/Kratos services should represent memory operations explicitly:

- `write`
- `read`
- `inject`
- `delete`
- `export`
- `disable`

Suggested sqlc tables:

- `ai_memory_items`
- `ai_memory_preferences`
- `ai_context_sources`
- `ai_context_injections`
- `ai_memory_audit_events`
- `ai_memory_deletion_jobs`

## Frontend Fit

Vite surfaces need:

- memory settings and temporary mode;
- view/edit/delete/export controls;
- source and purpose visibility;
- clear labels when AI uses preferences, workspace context, or retrieved knowledge;
- confirmation for destructive memory actions.

## Tradeoffs

- Explicit user controls add UI work, but reduce support, privacy, and trust risk.
- Default-off memory may slow personalization; default-on memory is a product/legal/privacy decision requiring human checkpoint.
- Storing raw chat history improves recall but makes deletion and privacy harder. Prefer small, typed, user-visible memories.
