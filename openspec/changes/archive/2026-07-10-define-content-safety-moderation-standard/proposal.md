# Change: Define Content Safety Moderation Standard

## Why

Existing standards cover AI prompt/eval, support trust ops, public commitments, dataset governance, and red-team abuse findings. They do not yet define the daily content moderation path for user-generated content and AI-generated content that appears in product surfaces.

Without a dedicated standard, a solo founder can over-rely on a moderation score, remove content without notice, lose appeal evidence, expose themselves to disturbing content, or make user-facing promises that the enforcement system cannot support.

## What

- Add a stage 28 standard for content safety, user-generated content, AI-generated content, moderation rules, enforcement, notice, appeals, and review.
- Define five minimal artifacts under `content-safety/`.
- Require policy, moderation rules, enforcement runbook, notice/appeal, and moderation review for public or user-impacting content surfaces.
- Define human checkpoints for policy boundary changes, automated punitive actions, high-risk content, appeal denial/restoration, external reporting, synthetic media, and public transparency claims.
- Create `content-safety-moderation-guard` skill and verifier.

## Impact

- Moderation becomes a versioned product capability rather than an API call.
- Go/Kratos/sqlc/gRPC systems get explicit moderation decision states and audit contracts.
- Vite frontends get clear report, notice, appeal, and review-workbench expectations.
- AI-generated content and user-generated content share a consistent policy/review path.
- The solo founder reviews only policy and high-impact enforcement decisions; structure and formatting are automated.
