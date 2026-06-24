# Design: Developer Experience API Docs SDK Standard

## Context

Previous stages cover internal knowledge recovery, API contract compatibility, support feedback, trust commitments, accessibility, release gates, and commercial commitments. They do not provide one dedicated workflow for customer/developer-facing quickstarts, generated API reference, SDK examples, developer changelogs, migration notes, and AI API limitations.

The one-person-company default is small: one docs map, one reference map, a few smoke-tested examples, a readable developer changelog, and a periodic DX review. Avoid a full developer portal, multi-language SDK program, and marketing content machine until developer adoption justifies the maintenance cost.

## Decisions

- Use `developer-experience/` as the governance folder for external developer documentation and SDK/example readiness.
- Require five artifacts per developer-facing target:
  - `docs-portal/<target>.json`
  - `api-reference/<target>.json`
  - `sdk-examples/<target>.json`
  - `changelog-release-notes/<target>.md`
  - `dx-review/<target>.md`
- Treat proto/OpenAPI/schema sources as the source of truth for reference documentation.
- Treat examples as release artifacts: they must be testable in sandbox, test mode, local mock, or be marked conceptual.
- Treat AI API docs as behavior and trust surfaces requiring limitations, schema/error/fallback examples, safety notes, and data-boundary links.

## Alternatives Considered

- Fold into knowledge management: internal context packs do not prove that external developers can safely integrate.
- Fold into API compatibility: compatibility protects evolution, but does not provide quickstarts, examples, migration notes, and developer onboarding.
- Fold into support: support receives feedback, but docs and SDK examples should prevent repeated support contact.
- Build a full docs portal: too heavy before public API usage or partner integrations justify it.

## Rollout

1. Add the stage 45 standard and OpenSpec spec.
2. Create `developer-experience-docs-guard`.
3. Add a verifier for required files, docs portal fields, API reference fields, SDK/example fields, changelog headings, DX review headings, runnable example metadata, public/stable docs gates, and sensitive-content patterns.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture and remove it.
