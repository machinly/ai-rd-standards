# Design: Processor Transfer Vendor Standard

## Context

Previous stages cover cost/vendor lock-in, security/privacy records, trust commitments, audit evidence, customer data lifecycle, AI tool runtime, and model routing. They do not give one source of truth for vendors that process customer data and may change contracts, subprocessors, data residency, model training terms, breach notice behavior, or deletion assistance.

For a one-person AI company, the default is small: maintain a processor register, verify DPA/contract coverage, monitor subprocessor sources, document cross-border or data residency impact, and review only meaningful changes. Avoid enterprise TPRM/GRC until customer contracts or regulated data require it.

## Decisions

- Use `vendor-risk/` as the governance folder for customer-data-processing vendors.
- Require five artifacts per production target:
  - `processor-register/<target>.json`
  - `dpa-checklist/<target>.json`
  - `subprocessor-watch/<target>.md`
  - `transfer-impact/<target>.json`
  - `vendor-review/<target>.md`
- Treat vendor data processing as an engineering boundary, not only a legal artifact.
- Treat data residency as project/endpoint/feature evidence, not a marketing claim.
- Treat supplier changes as release and trust-policy inputs when they affect customer data.

## Alternatives Considered

- Fold into cost vendor boundary: cost/lock-in does not answer DPA, subprocessor, data rights assistance, breach notice, or cross-border safeguards.
- Fold into security privacy baseline: privacy records list processors but do not verify contract clauses, data residency limits, subprocessor changes, or transfer risk.
- Fold into trust policy: trust commitments need evidence, but supplier evidence needs its own operational source.
- Full TPRM system: too heavy before customer requirements justify questionnaires, risk scoring workflows, and legal repositories.

## Rollout

1. Add the stage 41 standard and OpenSpec spec.
2. Create `processor-transfer-guard`.
3. Add a verifier for required files, JSON fields, vendor roles, DPA clauses, AI training/retention controls, subprocessor watch headings, transfer impact, data residency evidence, review headings, and sensitive-content patterns.
4. Validate current repository expected-fail behavior.
5. Validate a positive fixture and remove it.
