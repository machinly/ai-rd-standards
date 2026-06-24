# Design: Content Safety Moderation Standard

## Context

Stage 23 covers support and trust operations. Stage 25 covers public commitments. Stage 27 covers adversarial red-team findings. Stage 28 covers the operational path for content that enters, leaves, or is displayed by the product.

The design keeps one-person constraints explicit: do not build a large moderation operation before the product needs it. Use policy, rules, runbooks, notice/appeal, and review artifacts to create a small but auditable workflow.

## Artifact Model

Each content surface uses one stable `<surface>` name:

```text
content-safety/
  policy/<surface>.md
  moderation-rules/<surface>.json
  enforcement-runbook/<surface>.md
  notice-appeal/<surface>.md
  moderation-review/<surface>.md
```

This split keeps review questions clear:

- policy: what is allowed, restricted, and prohibited;
- moderation rules: how policy maps to categories, thresholds, actions, and review;
- enforcement runbook: how actions are executed, audited, restored, or escalated;
- notice/appeal: how users are informed and can challenge decisions;
- moderation review: whether the system is working and what one improvement matters next.

## Human Attention Budget

The verifier checks required files, headings, JSON fields, enums, sensitive-content patterns, and required checkpoints. The human decides only:

- policy and category boundary changes;
- automated removal, account restriction, appeal denial, restoration, or external reporting;
- high-risk categories such as minors, self-harm, sexual content, violence, extremism, civic integrity, medical/legal/financial, or public safety;
- storing or reviewing disturbing content, reporter identity, or sensitive evidence;
- synthetic media labeling and public transparency claims.

## Backend Fit

Go/Kratos services should represent moderation as explicit state, not as hidden control flow:

- `allow`
- `label`
- `limit`
- `review`
- `block`
- `hide`
- `remove`
- `suspend`
- `escalate`

Suggested sqlc tables:

- `content_items`
- `moderation_decisions`
- `moderation_reviews`
- `moderation_appeals`
- `content_reports`
- `policy_versions`

## Frontend Fit

Vite surfaces need:

- visible report path;
- understandable enforcement notice;
- appeal path for punitive actions;
- internal review workbench with policy version and decision evidence;
- redaction and click-to-view controls for sensitive content.

## Tradeoffs

- Strong automation reduces toil but increases false-positive harm. Punitive actions require notice, appeal, and review evidence.
- Raw content improves auditability but increases privacy and reviewer-wellbeing risk. Use content ids, hashes, redacted snippets, and controlled attachments first.
- Public transparency is valuable but can become a promise. Publish only metrics that the system actually records.
