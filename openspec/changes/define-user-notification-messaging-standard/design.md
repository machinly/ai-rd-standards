# Design: User Notification Messaging Standard

## Context

User messaging crosses product, operations, compliance, privacy, billing, support, and AI behavior. Previous stages cover many adjacent concerns, but outbound user messages need their own source of truth because consent, unsubscribe, suppression, sender identity, template variables, delivery events, and provider failures are channel-specific.

The one-person-company default is small: use one provider per channel, one backend notification service, versioned templates, a preference/suppression store, provider webhooks, and a simple review cadence. Avoid marketing automation platforms until the product has enough volume and segmentation to justify the complexity.

## Decisions

- Use `messaging/` as the outbound user messaging governance folder.
- Require five artifacts per production target:
  - `channel-registry/<target>.json`
  - `template-catalog/<target>.json`
  - `preference-consent/<target>.json`
  - `delivery-runbook/<target>.md`
  - `messaging-review/<target>.md`
- Separate transactional/security/billing/incident messages from marketing/lifecycle/broadcast messages.
- Treat email/SMS/push as external channels unsuitable for secrets, full AI outputs, full user input, or sensitive personal data by default.
- Keep human attention on new channels/providers, consent/opt-out boundary changes, sensitive content, high-impact messages, AI-generated copy, high-volume sends, and deliverability incidents.

## Alternatives Considered

- Fold messaging into support operations: support handles human replies, not automated delivery and suppression infrastructure.
- Use a marketing automation platform from day one: too much surface area before consent, classification, and template governance are clear.
- Let each service send its own messages: creates duplicated templates, inconsistent consent checks, and hard-to-debug retries.
- Store rendered messages in artifacts: unsafe for personal data, AI outputs, secrets, and customer content.

## Rollout

1. Add the stage 38 standard and OpenSpec spec.
2. Create `notification-messaging-guard`.
3. Add a verifier for required files, channel/template/preference JSON fields, required controls, markdown headings, human checkpoints, and sensitive-content patterns.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture and remove it.
