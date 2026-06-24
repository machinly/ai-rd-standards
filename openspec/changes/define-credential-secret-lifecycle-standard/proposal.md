# Proposal: define credential and secret lifecycle standard

## Why

Existing standards require secrets not to be stored in docs, logs, prompts, frontends, or artifacts, and they define broad security incident response. They do not yet define a dedicated lifecycle ledger for production credentials: inventory, access boundaries, rotation plans, rotation evidence, and exposure review.

For a one-person AI company, a single OpenAI/API provider key, database credential, webhook secret, CI deploy token, JWT signing key, or connector token leak can create cost, data, availability, and customer-trust impact before anyone notices.

## What Changes

- Add stage 54 for credential, secret, service-account, API-key, and signing-key lifecycle management.
- Add `credential-secret-lifecycle-standard`.
- Define five minimal artifacts under `credentials/`.
- Create `credential-secret-lifecycle-guard` skill and verifier.
- Update README and source map.

## Scope

- Credential inventory, access policy, rotation plan, rotation run, and exposure review.
- Go/Kratos/sqlc/gRPC service credential injection and startup validation.
- Vite frontend secret exposure boundaries.
- AI provider keys, MCP/connector tokens, tool runtime credentials, prompt/eval/RAG secret exposure prevention.
- OpenSpec-linked human checkpoints for production rotation, revocation, client exposure, long-lived credentials, and exposure incidents.

## Non-Goals

- Replacing stage 10 security/privacy/supply-chain baseline.
- Replacing stage 14 config/feature-flag/runtime-change governance.
- Replacing stage 44 security/privacy incident response.
- Defining enterprise PAM, HSM, full KMS architecture, SOC 2 controls, or formal legal notification rules.
- Storing real secret values in the repository.

## Source Anchors

- Brooks, `The Mythical Man-Month`, and small-project management: keep credential governance conceptually simple and action-oriented.
- OWASP Secrets Management Cheat Sheet.
- NIST SP 800-57 Part 1 Rev. 5.
- Twelve-Factor App Config.
- GitHub Secret Scanning and Push Protection.
- OpenAI API key safety and production best practices.
- Google Cloud Secret Manager best practices.
- Building Secure and Reliable Systems, simplicity.
- Kratos config, gRPC auth, and Vite env/mode docs.

## Human Attention

Only escalate:

- production credential rotation, revocation, or accepted residual risk;
- long-lived production key, cross-environment sharing, or broadened scope;
- frontend/browser/mobile exposure;
- real or suspected exposure, active use, customer impact, provider notification, or incident linkage;
- inability to rotate, revoke, locate owner, or separate staging from production.
