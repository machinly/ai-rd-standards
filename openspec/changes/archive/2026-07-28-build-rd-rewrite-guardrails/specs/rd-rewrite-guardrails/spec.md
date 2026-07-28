## ADDED Requirements

### Requirement: CLI contract and result semantics

The guardrail tool SHALL expose exactly the plan-defined commands through `python tools/rd_rebuild.py <command> --root .`, SHALL use the fixed result statuses, and MUST return the fixed exit code for the aggregated result.

#### Scenario: Passing check returns zero
- **WHEN** a command completes with `PASS` or only `WARN` findings
- **THEN** the CLI returns exit code 0 and does not count skipped checks as passed

#### Scenario: Review and blocking results remain distinct
- **WHEN** a command finds a semantic decision requiring a person or a deterministic policy failure
- **THEN** it returns `REVIEW_REQUIRED` with exit code 2 or `BLOCKED` with exit code 1 respectively

#### Scenario: Unexpected tool failure is not hidden
- **WHEN** an unexpected exception prevents a command from producing a trustworthy result
- **THEN** the CLI returns `TOOL_ERROR` with exit code 3 and does not report PASS

### Requirement: Protected source baseline

The tool SHALL inventory actual W0–W9 workspace files and SHA-256 content, MUST detect missing, moved, changed, or unregistered source files, and MUST distinguish the tooling bootstrap manifest from the future G2 content-frozen baseline.

#### Scenario: Unchanged source passes verification
- **WHEN** every protected source path and SHA-256 matches the recorded manifest
- **THEN** `baseline-verify` returns PASS with the matched file count and manifest digest

#### Scenario: Changed source blocks execution
- **WHEN** a protected source is deleted, moved, changed, or added without registration
- **THEN** `baseline-verify` returns BLOCKED and identifies the affected path without updating the baseline

#### Scenario: Tooling dry-run writes nothing
- **WHEN** `baseline-create --dry-run` runs against the real workspace during Change A
- **THEN** it reports planned reads and writes but does not modify W0–W9, draft files, baseline, run-state, or reusable gate evidence

### Requirement: Incremental write scope protection

The tool SHALL preserve G0 existing modified and untracked content and MUST block Change A writes outside the exact tooling policy whitelist.

#### Scenario: Existing dirty work is preserved
- **WHEN** an already modified or untracked G0 path remains byte-for-byte and status-equivalent to the tooling bootstrap manifest
- **THEN** `scope-check --phase tooling` does not attribute it to Change A

#### Scenario: Allowed tooling delta passes
- **WHEN** every Change A delta is under an exact allowed file or prefix and protected sources match
- **THEN** the scope check returns PASS and lists the matched policy rules

#### Scenario: Unauthorized delta blocks execution
- **WHEN** Change A creates or changes a path outside the exact whitelist
- **THEN** the scope check returns BLOCKED with the unauthorized path and does not relax policy or rebuild the baseline

### Requirement: Source inventory and segment validation

The tool SHALL validate source inventory uniqueness and SHALL require every nonblank source line in an applicable batch to be covered exactly once by an in-range continuous segment.

#### Scenario: Valid source ledger passes
- **WHEN** every source appears once with `reviewed` status and each nonblank line is covered by exactly one valid segment
- **THEN** inventory and segment checks return PASS with traceable counts

#### Scenario: Segment gap or overlap blocks
- **WHEN** a nonblank source line is uncovered, multiply covered, out of range, or a rule-bearing segment lacks an atomic rule reference
- **THEN** `segment-check` returns BLOCKED with source and line evidence

### Requirement: Atomic rule and classification validation

The tool SHALL validate required atomic-rule fields, IDs, source references, line ranges and enums, and MUST require exactly one valid primary category/item for each classified rule.

#### Scenario: Invalid atomic record blocks
- **WHEN** a rule has a duplicate ID, missing field, invalid source or line range, or disallowed enum
- **THEN** `rule-check` returns BLOCKED with the record identifier and field

#### Scenario: Duplicate or absent owner blocks
- **WHEN** a rule has more than one primary item, no primary item, or an invalid secondary reference
- **THEN** `classification-check` returns BLOCKED and does not select an owner

#### Scenario: Semantic ownership stays human-reviewed
- **WHEN** structural ownership is valid but its semantic fitness cannot be determined mechanically
- **THEN** the tool returns REVIEW_REQUIRED rather than moving or rewriting the rule

### Requirement: Rewrite and retirement traceability

The tool MUST require target mappings for retained treatments, MUST require a per-rule retirement reason, and SHALL detect exact normalized source copying according to policy without rewriting content automatically.

#### Scenario: Missing target or retirement reason blocks
- **WHEN** a rewrite, merge, split, or supersede record lacks a target, or a retire record lacks its own reason
- **THEN** `rewrite-check` returns BLOCKED with the rule ID

#### Scenario: Exact long copy blocks
- **WHEN** normalized source text of at least the configured minimum length is copied completely into a draft rule
- **THEN** `rewrite-check` returns BLOCKED while preserving the source and draft

#### Scenario: Similarity or retirement acceptability needs review
- **WHEN** text is highly similar but not an exact prohibited copy, or a retirement rationale requires semantic acceptance
- **THEN** the tool returns REVIEW_REQUIRED and does not approve retirement

### Requirement: Principle traceability and draft structure

The tool MUST require every principle to cite valid supporting rules and traceable rule clusters, MUST require category principles to cover multiple items, and SHALL validate the four categories, eleven items, required sections and canonical rule references without deciding principle quality.

#### Scenario: Unsupported principle blocks
- **WHEN** a principle lacks valid supporting rules or a category principle does not cover multiple items
- **THEN** `principle-check` returns BLOCKED with the unsupported principle ID

#### Scenario: Tool-specific principle language requests review
- **WHEN** a principle contains a policy-matched database, framework, command, directory, field or tool term
- **THEN** `principle-check` returns REVIEW_REQUIRED and does not delete or rewrite the principle

#### Scenario: Missing draft structure blocks
- **WHEN** a required category, item, section or canonical reference is absent
- **THEN** `draft-check` returns BLOCKED with the missing structural element

### Requirement: Ordered state machine and human approval gates

The tool SHALL enforce only the plan-defined state order, SHALL make `gate` the only state writer, MUST prevent skipped prerequisites, and MUST require a scope-matching human approval event for human gates.

#### Scenario: Illegal transition blocks
- **WHEN** a requested target is not the immediate legal successor or required checks are missing or stale
- **THEN** `gate` returns BLOCKED and leaves `run-state.json` unchanged

#### Scenario: Missing G1 approval requires review
- **WHEN** all G1 automated evidence passes but no matching user approval event exists
- **THEN** `gate --target tooling_ready` returns REVIEW_REQUIRED and leaves the state at `planned`

#### Scenario: Tool exception cannot advance state
- **WHEN** an exception occurs while evaluating or persisting a gate
- **THEN** the command returns TOOL_ERROR and the last trustworthy state remains unchanged

### Requirement: Deterministic status and fact-only reporting

The tool SHALL report the last trustworthy gate, blockers, evidence and next action, and SHALL build deterministic reports whose counts trace back to source records without generating semantic conclusions.

#### Scenario: Interrupted run is recoverable
- **WHEN** a run stops after a failed or review-required check
- **THEN** `status` shows the unchanged last passed state, current blocker, evidence location and safe next action

#### Scenario: Same input yields same result
- **WHEN** a check or report is repeated without changing its inputs
- **THEN** it produces the same status, counts and deterministic content

#### Scenario: Missing report input is not invented
- **WHEN** a required record or check result is absent
- **THEN** `report-build` returns BLOCKED and does not substitute a zero count or semantic PASS

#### Scenario: Report dry-run writes nothing
- **WHEN** `report-build --dry-run` runs
- **THEN** it lists planned report output and state effects without creating a report or reusable gate evidence

### Requirement: No semantic automation or out-of-scope side effects

The CLI MUST NOT expose automatic classification, principle generation, retirement approval, human approval, migration or deletion commands and MUST NOT modify protected sources or formal entry points.

#### Scenario: Command surface excludes forbidden actions
- **WHEN** the CLI help and parser command registry are inspected
- **THEN** no `auto-classify`, `auto-principles`, `auto-retire`, `approve`, `migrate` or `delete` command exists

#### Scenario: Stage A uses only local synthetic and read-only evidence
- **WHEN** the full Change A verification suite runs
- **THEN** it uses synthetic fixtures and real-source read-only checks without network, provider, production, customer-data or W0–W9 writes

### Requirement: Cross-platform OpenSpec strict launcher

The guardrail tool SHALL resolve the installed OpenSpec CLI before invoking strict validation, SHALL launch ordinary executable entries directly, and MUST launch a resolved Windows `.cmd` or `.bat` npm wrapper with `executable=COMSPEC`, `shell=False`, a fixed command string, disabled delayed expansion, a validated change identifier, and wrapper/change values carried only in child-process environment variables expanded inside quoted argument positions.

#### Scenario: Windows npm wrapper is launched successfully
- **WHEN** OpenSpec resolves to a Windows `.cmd` or `.bat` wrapper
- **THEN** the tool invokes the resolved wrapper through fixed `COMSPEC /d /s /v:off /c` processing, preserves every argument boundary, and maps an OpenSpec exit code 0 to PASS

#### Scenario: Windows wrapper path contains command metacharacters
- **WHEN** the resolved `.cmd` or `.bat` path contains a valid Windows path character such as `&`
- **THEN** the wrapper still receives exactly `validate`, the single change identifier, `--strict`, and `--no-interactive`, and no path fragment is executed as another command

#### Scenario: Direct executable is launched directly
- **WHEN** OpenSpec resolves to an executable that the operating system can launch without a command processor
- **THEN** the tool invokes it as an argument list without a shell and evaluates its actual exit code

#### Scenario: Missing or failing OpenSpec remains visible
- **WHEN** the launcher cannot be resolved or started
- **THEN** the check returns TOOL_ERROR; when OpenSpec starts but strict validation exits nonzero, the check returns BLOCKED with captured evidence

### Requirement: Approved append-only post-freeze tool recovery

The guardrail tool SHALL preserve and unconditionally authenticate the original content-frozen baseline against fixed baseline-file, original-tool, source, and bootstrap digests; MUST reject an unapproved, rebound, or mismatched replacement tool; and MAY accept exactly one fixed-scope replacement only through an append-only recovery record bound to those anchors, the replacement tool digest, unchanged protected and frozen-workspace aggregates, distinct producer/independent-review identities, and the unique identifier of a user renewed-G1 approval event distinct from implementation authorization.

#### Scenario: Original baseline is never overwritten
- **WHEN** a post-freeze tool defect requires a repair
- **THEN** the recovery process leaves the recorded G2 baseline and its original tool digest unchanged and represents the replacement as a linked recovery event

#### Scenario: Rebinding the baseline cannot bypass recovery
- **WHEN** the baseline file and its workspace snapshot are recaptured against the replacement tool so that the mutable baseline and replacement manifest agree
- **THEN** content scope returns BLOCKED because the baseline file and original tool digest no longer match the fixed G2 anchors

#### Scenario: Unapproved or mismatched recovery blocks
- **WHEN** the recovery record is absent, pending, expands the fixed whitelist, lacks the renewed user approval, or any tool/source/bootstrap/protected-workspace digest differs
- **THEN** content scope and gate evaluation return BLOCKED and do not advance state

#### Scenario: Recovery review identities and approvals are independent
- **WHEN** either reviewer identity is absent, blank or not a JSON string, the producer identity equals the independent reviewer after normalization, or the implementation-authorization ID is reused as renewed-G1 acceptance
- **THEN** recovery validation returns BLOCKED even when all other fields and approval scope digests match

#### Scenario: Renewed approval identity is scope-bound
- **WHEN** only the renewed-G1 `approval_id` in a recovery record changes
- **THEN** the canonical recovery approval scope digest changes and the previously approved event cannot authorize the rebound identifier

#### Scenario: Approval events are complete and unambiguous
- **WHEN** an approval line contains invalid JSON or a non-object value, an approval record omits any plan-required field, uses an invalid field type, reuses an `approval_id`, or multiple events target the same gate and scope
- **THEN** recovery and human-gate evaluation return BLOCKED without selecting an older approved event, misreporting deterministic governance data as TOOL_ERROR, or advancing state

#### Scenario: Independent-review finding counts are exact integers
- **WHEN** any critical, important or minor finding count is a boolean, floating-point number, string, null or nonzero integer
- **THEN** recovery validation returns BLOCKED rather than treating the value as zero findings

#### Scenario: G8 and G9 preserve the frozen semantic workspace
- **WHEN** run-state reports `audit_ready/G7`, `awaiting_user_review/G8`, or `approved_for_migration_design/G9`
- **THEN** the state and last gate must be paired exactly and every workspace path outside the recovery whitelist and run-state must still match the frozen recovery snapshot

#### Scenario: G9 re-evaluates live content scope
- **WHEN** `gate` evaluates the transition from `awaiting_user_review/G8` to `approved_for_migration_design/G9`
- **THEN** it requires a fresh content `scope-check`, rejects any state/last-gate mismatch or post-G8 workspace drift, and leaves run-state unchanged even when a matching user approval exists

#### Scenario: Exact approved recovery chain passes
- **WHEN** the approved recovery record links the baseline tool digest to the currently verified replacement manifest, all fixed-scope and protected aggregate checks match, and the bound user approval exists
- **THEN** content scope accepts the replacement, exposes the recovery ID and both tool digests as evidence, and leaves all semantic content and source records unchanged
