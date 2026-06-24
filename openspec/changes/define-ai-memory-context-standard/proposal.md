# Change: Define AI Memory Context Standard

## Why

Existing standards cover prompts, evals, data governance, trust policy, content safety, and red-team findings. They do not yet define the product and engineering contract for long-term AI memory, user preferences, chat-history reference, workspace context, RAG sources, and context injection.

Without this standard, personalization can become hidden state: users cannot tell what the AI remembers, deletion may be incomplete, context can cross tenant boundaries, stale memories can bias outputs, and all retrieved data can quietly become prompt context.

## What

- Add a stage 29 standard for AI memory, preferences, long-term context, retrieval rules, user controls, deletion/export, and memory review.
- Define five minimal artifacts under `ai-memory/`.
- Require memory policy, preference schema, context source map, retrieval rules, and memory review for AI capabilities that use long-term context.
- Define human checkpoints for default memory, sensitive memory, inferred memory, training reuse, cross-tenant sharing, deletion retention, and high-impact domains.
- Create `ai-memory-context-guard` skill and verifier.

## Impact

- AI memory becomes explicit, versioned, auditable, and user-controllable.
- Go/Kratos/sqlc/gRPC services get a concrete memory action and audit contract.
- Vite surfaces get clear memory controls, temporary mode, delete/export paths, and source visibility.
- Prompt builders get bounded context injection rules instead of hidden state.
- The solo founder reviews only high-risk memory decisions; structure and formatting are automated.
