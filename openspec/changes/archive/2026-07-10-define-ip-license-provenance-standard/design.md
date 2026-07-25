# Design: IP License Provenance Standard

## Context

Previous stages cover supply-chain security, dependency maintenance, AI coding workflow, trust commitments, datasets/evals, content safety, and vendor processing. They do not provide one source of truth for whether code, data, media, prompts, examples, AI-generated outputs, customer content, or public release artifacts have usable rights, correct licenses, and required attribution.

The one-person-company default is small: record materials and AI outputs, define allowed/restricted/forbidden licenses, write a practical AI output policy, keep NOTICE/attribution ready for releases, and review only high-risk changes. Avoid an enterprise OSPO/GRC platform until public distribution, enterprise contracts, or regulated content require it.

## Decisions

- Use `ip-rights/` as the governance folder for IP, license, and provenance.
- Require five artifacts per production target:
  - `source-register/<target>.json`
  - `license-policy/<target>.json`
  - `ai-output-policy/<target>.md`
  - `notice-attribution/<target>.md`
  - `ip-review/<target>.md`
- Treat AI-generated code/content as material requiring provenance and review, not automatically license-free.
- Treat output ownership terms, copyrightability, similarity risk, third-party rights, and publication claims as separate checks.
- Treat public distribution as a release gate that requires NOTICE/attribution/source-offer evidence.

## Alternatives Considered

- Fold into supply-chain security: SBOM/provenance does not answer attribution, copyleft, CC/ODbL, AI authorship, customer-content reuse, or release claims.
- Fold into maintenance dependency policy: dependency updates do not cover media, datasets, prompts, eval examples, generated outputs, or public content.
- Fold into trust policy: trust claims need evidence, but IP evidence needs its own material/source registry.
- Buy a license-compliance platform: too heavy before dependency volume, public distribution, or enterprise customer demands justify it.

## Rollout

1. Add the stage 42 standard and OpenSpec spec.
2. Create `ip-license-provenance-guard`.
3. Add a verifier for required files, source register fields, license policy, AI output policy headings, NOTICE/attribution headings, IP review headings, high-risk license checkpoints, customer-content checkpoints, AI output claims, and sensitive-content patterns.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture and remove it.
