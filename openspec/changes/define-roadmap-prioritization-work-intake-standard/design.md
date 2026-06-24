# Design: Roadmap Prioritization Work Intake Standard

## Context

Existing stages define the one-person OpenSpec operating model, product discovery, analytics, AI coding batches, customer support, customer onboarding, commercial commitments, and many engineering gates. They do not define the narrow decision layer that answers: what enters the system, what gets current focus, what is parked or killed, and what is safe to communicate as a roadmap.

For a one-person company, the risk is not lack of ideas. The risk is treating every idea, customer request, incident follow-up, AI quality concern, and technical debt item as equally actionable. The standard keeps this lean by requiring five planning artifacts and a verifier that catches missing evidence, too many active now items, high-risk decisions without human checkpoints, and sensitive content.

## Decisions

- Use `planning/` as the governance folder for roadmap, prioritization, and work intake.
- Require five artifact types:
  - `strategy-map/<period>.md`
  - `work-intake/<work-id>.json`
  - `decision-board/<period>.json`
  - `roadmap/<period>.md`
  - `focus-review/<period>.md`
- Treat `parked` and `killed` as first-class states, not failures.
- Use Now/Next/Later rather than date-heavy roadmap commitments.
- Limit `now` by default to two items: one focus work item and one maintenance/risk item.
- Keep scoring as decision support only; human checkpoints govern high-impact focus changes and commitments.

## Alternatives Considered

- Fold into product discovery: product discovery handles a single bet, but does not manage cross-domain intake, interrupts, maintenance, security work, or roadmap communication.
- Fold into OpenSpec: OpenSpec governs chosen changes, but should not become an infinite backlog of unchosen ideas.
- Use issue tracker only: issue trackers capture work items, but do not enforce strategy, appetite, human checkpoints, and roadmap boundaries.
- Full portfolio tooling: too heavy before scale; docs-as-code plus verifier is enough for one maintainer.

## Rollout

1. Add the stage 50 standard and OpenSpec spec.
2. Create `roadmap-prioritization-guard`.
3. Add a verifier for planning artifact presence, markdown headings, JSON fields, lane/decision values, now limits, high-risk checkpoints, linked work intake, and sensitive content.
4. Validate a positive fixture and remove it.
5. Run OpenSpec and skill validation.
