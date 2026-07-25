# Design: Open Source Release Community Maintenance Standard

## Context

Previous stages cover IP/license provenance, security incident response, developer documentation, API compatibility, support, and external claims. They do not define how a one-person company should run public repositories as maintainable community surfaces.

Open source can reduce adoption friction for SDKs, examples, templates, CLIs, and integrations, but it also creates ongoing issue, PR, support, release, security, and community expectations. The one-person default is conservative: publish fewer repos, document the boundary, automate checks, and make it easy to say no.

## Decisions

- Use `open-source/` as the governance folder for public repository and community maintenance readiness.
- Require five artifacts per open source target:
  - `project-register/<target>.json`
  - `community-health/<target>.json`
  - `contribution-policy/<target>.md`
  - `maintainer-runbook/<target>.md`
  - `release-security-review/<target>.md`
- Treat public repositories as product surfaces with support, security, release, license, and contribution boundaries.
- Treat GitHub issue/PR/security templates as attention-saving tools, not bureaucracy.
- Treat public package release as a security and compatibility gate.

## Alternatives Considered

- Fold into IP/license stage: license provenance is necessary, but not enough for contribution triage, SECURITY.md, issue/PR templates, maintainer boundaries, and release security.
- Fold into developer experience: developer docs cover API consumers, but not community contribution and maintainer operations.
- Require full OSPO/foundation governance: too heavy for a one-person company before community size justifies it.

## Rollout

1. Add the stage 47 standard and OpenSpec spec.
2. Create `open-source-maintainer-guard`.
3. Add a verifier for required files, project register fields, community health files, contribution/maintainer/release headings, public active repo gates, high-risk maintenance decisions, and sensitive content.
4. Validate a positive fixture and remove it.
5. Run OpenSpec and skill validation.
