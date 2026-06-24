# Design: Commercial Contract Obligation Standard

## Context

Previous stages cover SRE, billing entitlements, trust commitments, vendor processing, audit evidence, IP provenance, and AI workflow governance. They do not provide one source of truth for customer-specific contract obligations, order-form deviations, SLA terms, service credits, sales redlines, or commercial commitments that must be fulfilled by engineering and operations.

The one-person-company default is small: record obligations, map agreement surfaces, define only supportable SLAs, keep a redline playbook, and review contract changes before they become hidden production obligations. Avoid CLM/CRM/CPQ tooling until enterprise volume justifies it.

## Decisions

- Use `commercial-contracts/` as the governance folder for customer contracts and commercial commitments.
- Require five artifacts per production target:
  - `obligation-register/<target>.json`
  - `agreement-map/<target>.md`
  - `sla-service-credit/<target>.json`
  - `redline-playbook/<target>.md`
  - `contract-review/<target>.md`
- Treat public claims and sales promises as potential obligations when customers can reasonably rely on them.
- Treat SLA terms as downstream of SLOs, observability, runbooks, incident communication, dependency exclusions, and billing/service-credit mechanics.
- Treat non-standard customer terms as engineering change requests until mapped to facts, config, runbooks, vendor terms, and owner capacity.

## Alternatives Considered

- Fold into trust policy: public commitments need evidence, but customer-specific order terms, redlines, SLAs, and service credits need their own lifecycle.
- Fold into billing: billing covers plans, entitlements, usage, invoices, and credits, but not security, AI, support, DPA, vendor, IP, or operational commitments.
- Fold into SRE: SLO/SLA coverage does not cover contract maps, redlines, customer-specific obligations, renewals, or AI/data commitments.
- Adopt a CLM platform: too heavy before contract volume and enterprise review load justify it.

## Rollout

1. Add the stage 43 standard and OpenSpec spec.
2. Create `commercial-contract-guard`.
3. Add a verifier for required files, obligation fields, agreement-map headings, SLA/SLO evidence, redline headings, contract-review headings, high-risk promises, and sensitive-content patterns.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture and remove it.
