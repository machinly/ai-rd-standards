# Proposal: Define Open Source Release Community Maintenance Standard

## Intent

Add stage 47: a one-person-company standard for publishing open source repositories, accepting community contributions, defining maintainer boundaries, handling security reports, and releasing SDKs/examples/templates/packages safely.

## Scope

- Define required `open-source/` artifacts for public or externally contributed repositories.
- Cover project registration, community health files, contribution policy, maintainer runbook, and release/security review.
- Connect IP/license provenance, developer docs, API compatibility, security incident response, support, and claim gates.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Formal OSPO, foundation governance, trademark policy, CLA legal drafting, dual licensing, commercial open source strategy, or bug bounty operation.
- Replacing IP/license provenance, security incident response, developer experience, or API compatibility artifacts.
- Managing private repositories that do not accept external contributions and do not distribute public packages.

## Sources

- The Mythical Man-Month and small project management.
- The Cathedral and the Bazaar, Producing Open Source Software, and Working in Public.
- GitHub Open Source Guides for maintainer practices and community building.
- GitHub Community Health files, issue/PR templates, SECURITY.md, private vulnerability reporting, and repository security advisories.
- Contributor Covenant and Developer Certificate of Origin.
- OpenSSF Scorecard, Best Practices Badge, and SLSA.
- SPDX, REUSE, and OSI license references.

## Human Attention

Keep human judgment only for:

- publishing a new public repository, package, SDK, CLI, template, MCP server, prompt/eval/RAG/tool example, or official integration;
- accepting non-trivial external contributions, AI-generated contributions, unclear license/provenance, customer content, data, prompt, model, or media;
- changing license, DCO/CLA, governance, code-of-conduct enforcement, support boundary, security-fix window, compatibility, roadmap, or maintenance commitment;
- handling security vulnerabilities, private advisories, CVEs, exploit details, high-risk dependencies, secrets, customer data, or internal prompt exposure;
- pausing, archiving, transferring maintainer rights, adding maintainers, issuing breaking releases, or deprecating packages.
