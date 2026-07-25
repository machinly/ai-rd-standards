## ADDED Requirements

### Requirement: Frozen source and tool scope

The rewrite SHALL use the G2 content-frozen W0–W9 baseline and verified tool manifest, and MUST stop on any protected source, frozen tool or unauthorized workspace delta.

#### Scenario: Frozen inputs remain unchanged
- **WHEN** a content batch is checked
- **THEN** all protected sources, frozen tool files, tool manifest identity and pre-existing workspace files match the content baseline

#### Scenario: Scope delta blocks
- **WHEN** a protected source, frozen tool or out-of-scope path changes
- **THEN** the applicable check returns BLOCKED and no later gate advances

### Requirement: Complete source review ledger

Every W0–W9 file MUST appear exactly once in the reviewed inventory, and every nonblank source line MUST be covered exactly once by a valid continuous segment.

#### Scenario: Batch coverage passes
- **WHEN** an applicable batch has one reviewed inventory row per source and exact segment coverage
- **THEN** inventory and segment checks return PASS with source and line counts

#### Scenario: Missing or overlapping content blocks
- **WHEN** a source or nonblank line is absent, duplicated, out of range, or linked to an unknown rule
- **THEN** the batch remains incomplete and the affected path and line are reported

### Requirement: Traceable atomic rules

Each rule-bearing segment MUST produce one or more atomic rules with unique IDs, exact source ranges, source text, intent, applicability, subject, layer and treatment.

#### Scenario: Valid atomic extraction passes
- **WHEN** every rule is independently actionable and traces to its source range
- **THEN** rule checking returns PASS without deciding semantic quality

#### Scenario: Invalid rule record blocks
- **WHEN** a rule has missing fields, duplicate IDs, invalid lines, invalid enums or a mismatched source
- **THEN** rule checking returns BLOCKED with the record identifier

### Requirement: Four-category eleven-item ownership

Every atomic rule MUST have exactly one primary owner among the fixed four categories and eleven items, while secondary impacts remain references rather than duplicated owners.

#### Scenario: Unique ownership passes
- **WHEN** each rule has one valid category/item and all secondary references are valid
- **THEN** classification checking returns PASS

#### Scenario: Conflict remains human-owned
- **WHEN** ownership or rule conflict cannot be resolved structurally
- **THEN** the record remains REVIEW_REQUIRED until a scope-matching user decision is recorded

### Requirement: Rewrite traceability without direct copying

Every retained rule MUST map to an authoritative target rule, every retirement MUST have its own reason, and prohibited exact source copying MUST be blocked.

#### Scenario: Retained rules are mapped
- **WHEN** rewrite, merge, split or supersede is selected
- **THEN** all target IDs exist exactly once in the draft and preserve source traceability

#### Scenario: Copy or missing disposition blocks
- **WHEN** a retained rule lacks a target, a retirement lacks a reason, or a normalized long source passage is copied exactly
- **THEN** rewrite checking returns BLOCKED without modifying source or draft

### Requirement: Derived principles and fixed draft structure

The draft MUST contain four category documents, eleven item documents, all required sections, item-level principles for all eleven items, category-level principles for all four categories, and valid supporting rule traceability.

#### Scenario: Complete principle structure passes
- **WHEN** all fifteen principle lists and fixed draft files have valid support and canonical rule references
- **THEN** principle and draft checks pass structurally while semantic correctness remains user-reviewed

#### Scenario: Unsupported or tool-bound principle stops progression
- **WHEN** a principle lacks support or embeds policy-matched implementation language
- **THEN** it returns BLOCKED or REVIEW_REQUIRED respectively and is not silently rewritten by the tool

### Requirement: Audit package and stop before migration

The change SHALL generate deterministic coverage, conflict, retirement and review reports, SHALL pass all applicable checks before G8, and MUST stop before modifying formal entry points.

#### Scenario: Audit package is current
- **WHEN** report inputs and draft content are unchanged
- **THEN** report verification matches the current input digest and every reported count traces to source records

#### Scenario: G8 stops for user review
- **WHEN** the full package and strict validation pass
- **THEN** the state advances to `awaiting_user_review`, all content writes stop, and no migration or deletion occurs
