# Change: Define User Notification Messaging Standard

## Why

Existing standards cover support operations, incidents, billing, event/webhook integration, async jobs, trust claims, audit evidence, and frontend UX. They do not yet define one focused standard for user-facing outbound messages: email, SMS, push, web push, in-app notifications, templates, preferences, consent, unsubscribe, suppression, delivery events, and AI-generated message drafts.

Without this standard, a solo founder can harm trust quickly: transactional and marketing email get mixed, SMS lacks consent, unsubscribe requests are ignored, bounces and complaints are not suppressed, AI output is sent through insecure channels, provider retries spam users, and incident/security messages have inconsistent facts.

## What

- Add a stage 38 standard for user notification, email/SMS/push, and messaging governance.
- Define five minimal artifacts under `messaging/`.
- Require channel registry, template catalog, preference/consent policy, delivery runbook, and messaging review for production targets that send outbound user messages.
- Define human checkpoints for new providers/channels/senders, marketing and high-impact notifications, sensitive content, transactional/marketing reclassification, consent/opt-out bypass, AI-generated messages, high-volume sends, and deliverability incidents.
- Create `notification-messaging-guard` skill and verifier.

## Impact

- Go/Kratos/sqlc/gRPC systems get a unified notification service, template, preference, suppression, delivery, and provider-event pattern.
- Vite products get visible preference centers, unsubscribe surfaces, push permission behavior, and message preview/confirmation UI.
- AI workflows can draft or summarize messages but cannot directly send high-impact external messages without review.
- The solo founder reviews only high-risk messaging choices; artifact shape, required controls, sensitive-content screening, and fixture validation are automated.
