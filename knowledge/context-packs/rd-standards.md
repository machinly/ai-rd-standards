# rd-standards Context Pack

## Mission

Make the one-person AI R&D standards usable as a workflow, not a pile of documents. The user should locate the current work in W0-W9, read only that step and its adjacent gates, use the matching skill, and validate the result.

## Current Product Bet

The current bet is internal leverage: reduce solo-founder attention cost and Codex context recovery cost before adding more standards.

## System Shape

- Root entrypoint: `README.md`.
- AI R&D workflow entrypoint: `docs/00-start-here.md`.
- Workflow-to-standard index: `docs/02-standard-index.md`.
- Role swimlane index: `docs/03-role-index.md`.
- Canonical standards: `docs/Wx-*/00-main.md` plus `<local-order>-<semantic-name>.md` trigger standards in the same W directory.
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

Codex should first read `README.md`, `docs/00-start-here.md`, and this context pack. It should identify the current W0-W9 workflow step, then read the current step, prior-step inputs, and next-step gates from `docs/02-standard-index.md`. When role perspective is useful, read `docs/03-role-index.md` and only the matched `docs/roles/*.md` entries; roles are swimlanes, not a replacement lifecycle.

## Operational Links

- Operating model: `docs/00-start-here.md` and `docs/W2-openspec-risk/00-main.md`.
- Role swimlanes: `docs/03-role-index.md`.
- Knowledge recovery: `docs/W9-maintain/00-main.md`.
- Prioritization: `docs/W0-intake/00-main.md`.
- Workflow index: `docs/02-standard-index.md`.
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
Use the rd-standards context pack. Start from README.md and docs/00-start-here.md, identify the current W0-W9 AI R&D workflow step, then use docs/02-standard-index.md to read only that step, its prior inputs, and next gate. If a role view is needed, use docs/03-role-index.md and only the relevant docs/roles/*.md entry. Only escalate high-impact human decisions.
```



