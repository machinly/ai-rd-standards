# rd-standards Glossary

## Domain Terms

- One-person company: A product company operated by one founder with AI assistance and low process overhead.
- Standard: A durable rule set that changes how work is done.
- Directory-local order: The two-digit filename prefix inside each `docs/Wx-*` directory; it defines reading order only within that workflow step.
- Navigation layer: The root README, start-here guide, full index, and knowledge context pack.
- Workflow step: One of W0-W9 in the AI R&D lifecycle, from intake to context recovery.
- Role swimlane: A role-specific dispatch lane used after the current W0-W9 step is known.

## Bounded Context Language

- OpenSpec change: The working unit under `openspec/changes/<change-id>/`.
- Canonical entrypoint: The document that should be read first for a target.
- Context pack: A short handoff document for humans and Codex.
- Human checkpoint: A decision that must be made by the user rather than automated.
- Workflow-to-standard map: The mapping from each W0-W9 step to the small set of standards required for that step.
- Total controller Agent: The coordinating Codex instance that locates the current W, selects role swimlanes, and merges outputs.
- Role Agent: A focused Codex instance that reads one role entry plus the current W documents and returns role-specific artifacts, risks, and handoffs.

## API Names

- Not applicable for the standards repository. If a future management UI or service is added, name APIs from the planning and knowledge domains.

## Data Names

- `knowledge/docs-map/<target>.json`: Machine-checkable documentation map.
- `knowledge/context-packs/<target>.md`: Handoff context.
- `knowledge/glossary/<target>.md`: Shared terms.
- `knowledge/how-to/<target>.md`: Common task guide.
- `knowledge/freshness/<target>.jsonl`: Review and freshness log.

## AI Terms

- Skill: A reusable Codex instruction package with optional scripts.
- Eval: A small versioned test set for AI behavior.
- AI workflow: Prompt, model, tool, schema, retrieval, and review behavior treated as a versioned system.

## Avoided Terms

- Backlog: Prefer `work-intake`, `decision-board`, `now`, `next`, `later`, `parked`, and `killed`.
- All docs: Prefer `current workflow step`.
- Topic index: Prefer `workflow index`.
- Role lifecycle: Prefer `role swimlane`.
- Approval flow: Prefer `human checkpoint`.
