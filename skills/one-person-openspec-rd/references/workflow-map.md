# Explore / Deliver R&D Fallback Map

Only use this reference when a repository has no formal README and R&D routing files.

## 1. R&D Applicability

Enter this workflow only when the primary result changes, verifies, releases, operates, recovers, or directly decides a product/engineering system, or when research directly supports an identified product/engineering decision.

Writing, translation, summaries, content production, administration, general queries, general research, and unauthorized read-only reports are Non-R&D. Use their own workflow and do not create OpenSpec, R&D status, or Superpowers artifacts. Split mixed requests by result.

## 2. Work Mode

- **Explore** when a falsifiable unknown still dominates and the goal is learning.
- **Deliver** when behavior is clear enough and the goal is a stable increment.

Prototype is an Explore artifact. Walking Skeleton is a tactic. Quick, Standard, and High-risk are Deliver routes only.

## 3. Explore

Choose the highest-priority unknown:

- Product Discovery: user, problem, value, scope, or success;
- UX Prototype: task flow, information architecture, interaction, or comprehension;
- Technical Spike: architecture, integration, contract, or feasibility.

Keep one local/isolated, synthetic, resettable sandbox with no production, real customer data, real credentials, unapproved external systems, payments, external communication, public commitment, or irreversible action. Maintain one short record: question, hypothesis, sandbox boundary, shortest slice, active tasks, showcase, evidence/limits, decision, next.

Use at most 5 active tasks. Close a Walking Skeleton from an actual product entry to a visible business result. Showcase every 120 minutes or 5 commits, whichever comes first; shrink or stop after 2 hours without a new visible fact. Outcomes are `validated | invalidated | revise | stopped | promote`.

Explore does not default to OpenSpec, formal visual UX, a full quality matrix, Browser E2E, or independent final review. Actual safety, auth, data, and side-effect controls still apply. Promote only a human-selected stable increment and reroute it through Deliver.

## 4. Deliver

### Quick

Choose for clear, local, reversible work without user, production, sensitive-data, permission, money, commitment, or external-system impact. Provide the artifact/diff, relevant check, and residual risk. Do not require OpenSpec.

### Standard

Choose for clear user-visible, cross-file/session, AI-behavior, or independently accepted work. Create or continue one OpenSpec change before implementation; keep `tasks.md` as the status source. Link authoritative product/UX inputs, record `visual_ux: required | not-required`, define critical journeys, and obtain an independent final review.

### High-risk

Choose for real production, customer data, security, auth, credentials, payment, public commitments, external communication, irreversible changes, or unclear rollback. Before side effects, identify a human owner, record blast radius/stop/rollback, obtain explicit approval, and independently review applicable auth/data/admin/irreversible design.

## 5. OpenSpec

OpenSpec defaults only to Deliver Standard/High-risk implementation. It records the selected stable increment and links Explore evidence; it does not copy all exploration history. Skip only with explicit user approval and a recorded owner, reason, scope, and recovery path.

## 6. Superpowers

Read `superpowers-scope.md`. Select the smallest directly relevant skill only for a concrete complexity trigger. Invoking one skill does not authorize another and must not create a duplicate authority artifact.

## 7. Review and Evidence

All R&D work gets producer self-check. Explore checks sandbox, actual entry, human-readable fixture, showcase, outcome, evidence limits, active-task peak, and any Superpowers trigger. Deliver Standard/High-risk requires an independent final reviewer. Name unit, integration, dependency-container, complete local integration, Browser E2E, provider sandbox, and production evidence separately.
