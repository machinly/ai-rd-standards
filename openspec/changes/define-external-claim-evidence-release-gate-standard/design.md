# Design: External Claim Evidence Release Gate Standard

## Context

Earlier stages define the underlying facts:

- stage 25 records trust commitments and policy surfaces;
- stage 35 records audit evidence and evidence packages;
- stage 40 records data lifecycle and deletion/export boundaries;
- stage 41 records vendor processing, DPA, subprocessor, and transfer boundaries;
- stage 43 records commercial contract and SLA obligations;
- stage 45 records developer documentation and SDK/API surfaces.

The gap is the release moment: a single wording change can expand a claim beyond what those artifacts support. A one-person company needs a small gate that asks, "Can this statement be published as written, for this audience, on this surface, right now?"

## Decisions

- Use `claim-control/` as the governance folder for external claim release control.
- Require five artifacts per target:
  - `surface-inventory/<target>.json`
  - `claim-evidence-map/<target>.json`
  - `release-gate/<target>.json`
  - `correction-runbook/<target>.md`
  - `claim-review/<target>.md`
- Treat objective claims as versioned release artifacts with owners, scope, evidence refs, verification dates, expiration, and status.
- Treat high-risk AI/data/security/SLA/contract/billing/developer stability claims as human checkpoints.
- Keep evidence by reference, not by copying secrets, customer content, raw prompts/responses, or contract text.

## Alternatives Considered

- Fold into stage 25: trust policy tracks commitments, but does not scan every product/docs/contract/support surface at release time.
- Fold into stage 35: evidence register stores proof, but does not decide whether a claim can be published.
- Fold into stage 43: contract obligations are only one category of external claims.
- Make a legal approval process: too heavy and not enough engineering linkage for a solo operator.

## Rollout

1. Add the stage 46 standard and OpenSpec spec.
2. Create `external-claim-evidence-guard`.
3. Add a verifier for required files, fields, claim risk gates, evidence expiry, status rules, markdown headings, sensitive content, and expected missing-artifact failure.
4. Validate a positive fixture and remove it.
5. Run OpenSpec and skill validation.
