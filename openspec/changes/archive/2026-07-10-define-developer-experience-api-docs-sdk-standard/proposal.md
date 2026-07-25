# Proposal: Define Developer Experience API Docs SDK Standard

## Intent

Add stage 45: a one-person-company standard for developer experience, external API documentation, generated references, SDKs, runnable examples, developer changelogs, migration notes, and AI API documentation boundaries.

## Scope

- Define required `developer-experience/` artifacts for production targets that expose public/stable APIs, SDKs, CLI, webhook, developer console, AI API, RAG API, tool/integration API, or customer-facing technical documentation.
- Cover docs portal maps, API references, SDK/examples, developer changelog/release notes, and DX reviews.
- Connect Go/Kratos/sqlc/gRPC/protobuf facts, OpenAPI, Vite documentation surfaces, AI eval/tool schema boundaries, support signals, contracts, release gates, and trust claims.
- Create a reusable Codex skill and local verifier.

## Out of Scope

- Replacing internal knowledge management, API compatibility policy, customer support queues, trust/legal policies, or marketing sites.
- Full developer portal platform, API marketplace, SEO/content program, partner certification, or multi-language SDK program before adoption justifies it.
- Formal legal or compliance review for API terms, data-processing claims, or security claims.

## Sources

- The Mythical Man-Month and small project management.
- Diátaxis documentation framework.
- Google Developer Documentation Style Guide, Google API Design Guide, AIP-192, AIP-180.
- OpenAPI Specification, gRPC documentation, Protobuf style guide, Buf breaking detection.
- SemVer, Keep a Changelog, GitHub API versioning/changelog practices.
- Stripe, GitHub, and OpenAI API docs patterns for auth, errors, rate limits, idempotency, request IDs, SDKs, sandbox/test mode, and changelogs.

## Human Attention

Keep human judgment only for:

- promoting an API, SDK, AI capability, CLI, webhook, template, or integration from experimental/internal to stable/public;
- breaking changes, deprecations, migration guides, support windows, and developer communication;
- claims about model, accuracy, latency, rate limit, cost, data retention, no-training, compliance, security, or availability;
- examples touching production data, customer content, money movement, permission changes, deletion, notifications, or external side effects;
- security-sensitive examples, exploit-like content, webhook bypasses, prompt-injection examples, or abuse-sensitive guidance.
