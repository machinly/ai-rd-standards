# rd-standards Context Pack

## Mission

Make the one-person AI R&D standards usable as a workflow, not a pile of documents. The user should locate the current work in W0-W9, read only that step and its adjacent gates, use the matching skill, and validate the result.

## Current Product Bet

The current bet is internal leverage: reduce solo-founder attention cost and Codex context recovery cost before adding more standards.

## System Shape

- Root entrypoint: `README.md`.
- AI R&D workflow entrypoint: `docs/00-start-here.md`.
- Workflow-to-standard index: `docs/00-standard-index.md`.
- Canonical standards: `docs/Wx-*/NN-*.md`.
- Specs and changes: `openspec/`.
- Source map: `docs/sources/2026-06-23-source-map.md`.
- Knowledge artifacts: `knowledge/`.

## Key Commands

```powershell
openspec validate --all
python tools\verify_workflow_index.py .
python C:\Users\machinly\.codex\skills\knowledge-context-recovery-guard\scripts\verify_knowledge_context.py .
```

## Data / Auth / Cost / Security Boundaries

- Do not store credentials, personal contact data, production connection strings, or full model conversation content in knowledge artifacts.
- Human judgment is required for changing canonical sources, accepting stale docs, deleting docs, or changing terminology.
- Keep context packs short and link canonical files instead of copying them.
- Avoid adding a new numbered stage when the work is only navigation cleanup.

## AI Behavior

Codex should first read `README.md`, `docs/00-start-here.md`, and this context pack. It should identify the current W0-W9 workflow step, then read the current step, prior-step inputs, and next-step gates from `docs/00-standard-index.md`.

## Operational Links

- Operating model: `docs/W2-openspec-risk/01-one-person-ai-rd-operating-model.md`.
- Knowledge recovery: `docs/W9-maintain/16-knowledge-context-recovery-standard.md`.
- Prioritization: `docs/W0-intake/main.md`.
- Workflow index: `docs/00-standard-index.md`.
- Navigation change: `openspec/changes/improve-rd-standards-navigation/`.

## Current Risks

- The standards can become unusable if README turns back into a flat full list.
- The index can become stale after adding new stages or skills.
- The user can lose focus if standards are added by topic instead of attached to W0-W9.

## Open Decisions

- Whether future stages should be paused unless they clearly fill a W0-W9 workflow gap.
- Whether to add broader docs checks beyond `tools/verify_workflow_index.py`.

## Handoff Prompt

```text
Use the rd-standards context pack. Start from README.md and docs/00-start-here.md, identify the current W0-W9 AI R&D workflow step, then use docs/00-standard-index.md to read only that step, its prior inputs, and next gate. Only escalate high-impact human decisions.
```



