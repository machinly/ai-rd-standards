# Design: Accessibility AI UX Standard

## Context

Stage 3 defines Vite + Geist frontend basics. Stage 4 defines AI prompt/eval workflow. Stage 23 handles support and feedback. Stage 25 covers trust policy. Stage 31 connects these at the user interface boundary: the user must be able to perceive, operate, understand, correct, and recover from AI-assisted flows.

The design assumes a one-person company should not start with a large design ops system. The first version should cover critical surfaces with small artifacts, repeatable checks, and clear human escalation.

## Artifact Model

Each critical surface uses one stable `<surface>` name:

```text
ux-accessibility/
  surface-map/<surface>.md
  interaction-contract/<surface>.json
  accessibility-test-plan/<surface>.json
  ai-ux-disclosure/<surface>.md
  ux-review/<surface>.md
```

The split keeps review questions clear:

- surface map: who uses this surface and what tasks matter;
- interaction contract: which components, states, input modes, keyboard behavior, focus behavior, forms, errors, responsive/theme behavior, and AI interactions exist;
- accessibility test plan: which standards, tools, manual checks, assistive technology smoke tests, gates, exceptions, and evidence are required;
- AI UX disclosure: how the interface tells users AI is involved and gives control;
- UX review: what changed, what was found, what risks remain, and the one next improvement.

## Human Attention Budget

The verifier checks required files, headings, JSON fields, component shape, required states, input modes, accessibility standards, required checks, gates, exception shape, AI disclosure linkage, and sensitive-content patterns. The human decides only:

- whether to launch a critical path without WCAG 2.2 AA or keyboard smoke;
- whether a custom complex widget is worth its accessibility burden;
- whether high-impact AI advice is acceptable in the UI;
- whether disclosure, feedback, human review, or user controls can be reduced;
- whether an interaction is deceptive, coercive, or hard to undo;
- whether sensitive data capture is justified;
- whether a new brand or marketing surface changes user expectations.

## Backend Fit

Go/Kratos services should expose user-safe state:

- stable error codes and field errors;
- retryability and next-step hints;
- async task states for AI flows;
- feedback/correction/retry/cancel/handoff endpoints;
- audit fields for surface, AI feature, request id, actor, and tenant.

## Frontend Fit

Vite + React + TypeScript surfaces should:

- prefer semantic HTML and small local components;
- implement light/dark semantic tokens from Geist-inspired rules;
- keep focus visible and managed;
- cover loading, empty, error, success, and AI-specific states;
- provide keyboard, screen reader smoke, reduced-motion, responsive, and contrast evidence.

## Tradeoffs

- Manual keyboard and screen reader smoke add work, but catch issues automation misses.
- WCAG AA is a baseline, not a guarantee that every user need is covered.
- AI UX disclosure can feel like extra copy, but reduces overtrust, support burden, and trust-policy risk.
- A one-person company should test the few most important surfaces deeply before trying to audit every page shallowly.
