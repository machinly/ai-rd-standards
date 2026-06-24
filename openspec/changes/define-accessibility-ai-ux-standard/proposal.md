# Change: Define Accessibility AI UX Standard

## Why

Existing standards cover Vite/Geist frontend structure, trust policy, prompt/eval workflow, content safety, and AI model routing. They do not yet define a focused contract for accessibility, interaction states, keyboard/focus behavior, AI UX disclosure, user feedback, and degraded interface states.

Without this standard, AI products can ship surfaces that look polished but are not operable by keyboard, do not expose useful error states, hide AI limitations, provide no correction or feedback path, or make high-impact actions feel more certain than they are.

## What

- Add a stage 31 standard for accessibility, AI UX, and interface trust.
- Define five minimal artifacts under `ux-accessibility/`.
- Require surface map, interaction contract, accessibility test plan, AI UX disclosure, and UX review for critical user-facing surfaces.
- Define human checkpoints for accessibility exceptions, custom complex widgets, high-impact AI UI, hidden disclosures, dark patterns, sensitive data capture, and brand/claim changes.
- Create `accessibility-ai-ux-guard` skill and verifier.

## Impact

- Vite/Geist frontends get a concrete accessibility and interaction-state contract.
- AI surfaces expose disclosure, uncertainty, feedback, correction, handoff, and degraded states.
- Go/Kratos/gRPC services must provide user-safe errors and task states that the UI can render accessibly.
- The solo founder reviews only high-risk UX choices; structure, headings, JSON fields, status coverage, and test-plan completeness are automated.
