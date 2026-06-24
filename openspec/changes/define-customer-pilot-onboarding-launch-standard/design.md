# Design: Customer Pilot Onboarding Launch Standard

## Context

Existing stages define product discovery, tenant isolation, data lifecycle, billing, support, commercial obligations, external claims, release, SRE, and AI quality operations. They do not define the narrow customer delivery path between “this customer should try the product” and “this customer is safely onboarded or intentionally exited.”

For a one-person company, the risk is not the absence of a customer success department. The risk is that every customer launch becomes an undocumented bespoke project. The standard keeps the path lean by requiring five artifacts and a verifier that catches structure, missing gates, sensitive content, and high-risk decisions.

## Decisions

- Use `customer-onboarding/` as the governance folder for customer pilot and launch operations.
- Require five artifacts per customer alias:
  - `pilot-charter/<account>.md`
  - `tenant-provisioning/<account>.json`
  - `launch-readiness/<account>.json`
  - `success-plan/<account>.md`
  - `handoff-review/<account>.md`
- Use customer aliases only, not real names, emails, secrets, payment data, or raw customer content.
- Require fixed launch readiness areas for external customers to keep the checklist small and repeatable.
- Treat failed/blocked/accepted-risk required gates as human decisions, not script decisions.

## Alternatives Considered

- Fold into product discovery: discovery validates demand, but does not capture production tenant facts, gates, support, billing, and offboarding.
- Fold into release readiness: release gates validate software changes, but a customer launch can fail because identity, billing, data, support, integration, or acceptance is incomplete.
- Fold into support/customer success docs: support handles ongoing issues, but launch readiness must happen before customer exposure.
- Use a full CRM/customer success platform: too heavy before scale; the one-person default is docs-as-code plus focused checks.

## Rollout

1. Add the stage 49 standard and OpenSpec spec.
2. Create `customer-launch-onboarding-guard`.
3. Add a verifier for required artifacts, markdown headings, JSON fields, launch gate coverage, high-risk checkpoints, and sensitive content.
4. Validate a positive fixture and remove it.
5. Run OpenSpec and skill validation.
