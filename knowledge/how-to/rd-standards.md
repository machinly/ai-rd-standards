# rd-standards How-To

## Setup

1. Open `README.md`.
2. Read `docs/00-start-here.md`.
3. Identify the current W0-W9 workflow step.
4. Use `docs/02-standard-index.md` only to find standards for that step.

## Develop

1. Create or update one OpenSpec change for work that takes more than 30 minutes or affects users, production, data, security, cost, or AI behavior.
2. Select one workflow step from `docs/00-start-here.md`.
3. Use the matching skill.
4. Keep new navigation content short and link canonical standards instead of copying them.

## Test

1. Run `openspec validate --all`.
2. Run `python tools\verify_workflow_index.py .`.
3. Run `python C:\Users\machinly\.codex\skills\knowledge-context-recovery-guard\scripts\verify_knowledge_context.py .`.
4. Check that new docs do not reintroduce a flat full list or topic-first index as the root entrypoint.

## Run Locally

This repository is a documentation and OpenSpec repository. There is no app server to run by default.

## Release

1. Confirm the root README still points to `docs/00-start-here.md`.
2. Confirm the index attaches any new stage or skill to a W0-W9 workflow step.
3. Confirm workflow index validation passes.
4. Confirm OpenSpec validation passes.
5. Append a freshness record after meaningful navigation cleanup.

## Rollback

1. Keep `README.md` short.
2. Restore the previous canonical entrypoint only after a human checkpoint.
3. If a new index is confusing, park it and return to `docs/00-start-here.md` as the primary guide.

## Debug

1. If a task feels overloaded, reduce the path to three standards or fewer.
2. If a standard cannot be found, search `docs/02-standard-index.md` by workflow step first, then by stage number.
3. If Codex scans too broadly, give it the handoff prompt from `knowledge/context-packs/rd-standards.md`.

## Update Knowledge

1. Update `docs/02-standard-index.md` when adding or renaming standards.
2. Update `README.md` only when the first-click entrypoint changes.
3. Update `knowledge/docs-map/rd-standards.json` when canonical entrypoints change.
4. Append `knowledge/freshness/rd-standards.jsonl` after cleanup.
