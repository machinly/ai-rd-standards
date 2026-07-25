# Minimal Solo R&D Fallback Map

Use this reference only when the repository does not provide its own README and routing files.

## Quick

Choose Quick when the work is low-risk, reversible, local, and does not affect users, production, sensitive data, permissions, money, commitments, or external systems.

Required result:

- artifact or diff；
- relevant check；
- residual risk。

Do not require a process file or OpenSpec.

## Standard

Choose Standard when work is user-visible, crosses files/sessions, changes AI behavior, or needs independent acceptance.

Create or continue one OpenSpec change before implementation, with:

- outcome；
- non-goals；
- acceptance；
- scope；
- risks；
- verification；
- rollback；
- decisions and next action。

Use `tasks.md` as the implementation status source; do not duplicate a parallel work brief.

For user-visible Standard/High-risk work, record `visual_ux: required | not-required` and the reason in the proposal. When required, link the current static UX artifacts and explicit human `approved` review before production implementation. Also define critical journeys in `governance/quality/user-journeys.json` and close one real Browser E2E early. Put guard artifacts under `governance/<registered-domain>/`; use `governance/current-status.json` as the only current completion state.

Use an independent final reviewer.

The reviewer must execute blocking user journeys from a clean complete local environment. Manual browser checks do not count as Browser E2E, and a newer changes-requested decision invalidates older completion summaries.

## High-risk

Choose High-risk for production, customer data, security, auth, credentials, payment, public commitments, external communication, irreversible changes, or unclear rollback.

Before the side effect:

- identify a human decision owner；
- record blast radius, stop conditions and rollback；
- obtain explicit approval；
- verify the prepared action independently。

Stop when approval, permission, or rollback evidence is missing.

## Default and Optional Tools

- OpenSpec：default for Standard/High-risk implementation; skip only with explicit user approval and a recorded reason/scope/recovery path。
- Multi-Agent：only for independent tasks with measured benefit and non-overlapping write scopes。
- Role lenses：only when a specific professional perspective is needed。

Time alone does not select a path.
