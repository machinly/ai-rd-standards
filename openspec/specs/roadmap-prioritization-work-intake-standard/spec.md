# roadmap-prioritization-work-intake-standard Specification

## Purpose

Define the minimum roadmap, prioritization, work intake, Now/Next/Later planning, and focus-review standard for a one-person AI company.

## Requirements

### Requirement: 超过半天或高影响研发工作必须进入 planning intake

Any work that may consume more than half a day, affect users, change production risk, or create an OpenSpec change MUST enter planning intake before implementation unless it is an active incident response.

#### Scenario: 新研发请求进入系统

- GIVEN a product idea, customer request, bug, reliability issue, security/privacy item, compliance task, technical debt item, platform task, AI quality issue, cost item, or docs task is proposed
- WHEN it may consume more than half a day or affect user-visible behavior, data, security, billing, contracts, operations, or production risk
- THEN 创建 `planning/work-intake/<work-id>.json`
- AND record id, title, source, request_type, target_user_or_system, problem, evidence_refs, value_hypothesis, risk_or_obligation, appetite, expected_scope, non_goals, dependencies, required_artifacts, human_checkpoint, status, and review_by
- AND do not implement until the item has a decision or is explicitly marked as an active incident/emergency path

### Requirement: 每个计划周期必须具备 strategy map、decision board、roadmap 和 focus review

Each planning period MUST preserve strategy, decisions, communication boundaries, and review state.

#### Scenario: 创建计划周期

- GIVEN a planning period exists for roadmap or prioritization decisions
- WHEN 创建 planning artifacts
- THEN 创建 `planning/strategy-map/<period>.md`
- AND 创建 `planning/decision-board/<period>.json`
- AND 创建 `planning/roadmap/<period>.md`
- AND 创建 `planning/focus-review/<period>.md`
- AND link accepted or reviewed work items from `planning/work-intake/`

### Requirement: Strategy map 必须定义诊断、结果、目标用户、指导方针、赌注、约束、非目标、风险和 capacity

Strategy map MUST keep roadmap decisions tied to a diagnosis and coherent action.

#### Scenario: 定义周期策略

- GIVEN a planning period is active
- WHEN 创建 `planning/strategy-map/<period>.md`
- THEN it includes Scope, Diagnosis, North Star Outcome, Target Segment, Guiding Policy, Strategic Bets, Constraints, Non Goals, Risk Appetite, Capacity Budget, Human Checkpoints, Linked Artifacts, and Review Cadence
- AND capacity budget distinguishes focus work, maintenance or risk work, and interrupt buffer

### Requirement: Decision board 必须限制 now/expedite 并记录 evidence、appetite、confidence、risk 和 next review

Decision board MUST protect current focus and make prioritization recoverable.

#### Scenario: 更新决策板

- GIVEN work intake items are ready for prioritization
- WHEN 创建 `planning/decision-board/<period>.json`
- THEN it records period, owner, capacity, decision_policy, work_items, human_checkpoint, review_cadence, and status
- AND each work item records id, lane, decision, request_type, appetite, evidence_strength, urgency, risk_reduction, value, effort, confidence, score_summary, linked_artifacts, next_review, human_checkpoint, and status
- AND lane is now, next, later, parked, killed, expedite, or maintenance
- AND decision is start_now, schedule_next, shape, needs_evidence, park, kill, expedite, or done
- AND now lane defaults to at most two active items unless a human checkpoint accepts the focus cost
- AND high-impact expedite decisions require a human checkpoint

### Requirement: Roadmap 必须使用 Now/Next/Later 并明确非承诺边界

Roadmap MUST communicate uncertainty without creating accidental customer commitments.

#### Scenario: 更新路线图

- GIVEN a roadmap period is updated
- WHEN 创建 `planning/roadmap/<period>.md`
- THEN it includes Scope, Now, Next, Later, Parked / Killed, Explicit Non Commitments, Customer / Public Claim Boundary, Dependencies, Evidence Links, Change Log, and Review Cadence
- AND roadmap content that may be shared with customers, sales, website, docs, contracts, or support links to external-claim or commercial-contract evidence gates

### Requirement: Focus review 必须记录近期工作、学习、请求、容量、决策、停止项、风险和一个下一步

Focus review MUST prevent roadmap drift and repeated re-discussion.

#### Scenario: 周期复盘当前焦点

- GIVEN a planning period reaches its review cadence
- WHEN 创建 `planning/focus-review/<period>.md`
- THEN it includes Recent Work, Shipped / Learned, Incoming Requests, Active Now Slots, Capacity / Energy, Decisions Made, Stopped / Parked, Risks, One Next Change, and Review Cadence
- AND One Next Change records one highest-impact improvement to the planning or delivery system

### Requirement: 高风险路线图和优先级动作必须保留人工 checkpoint

High-risk roadmap actions MUST be reviewed by the maintainer before they consume focus or create commitments.

#### Scenario: 高风险规划动作

- GIVEN artifacts mention now, expedite, public roadmap, committed date, customer commitment, custom feature, SLA, pricing, target segment, data boundary, production, security, privacy, compliance, real customer data, live billing, vendor lock-in, or multi-week work
- WHEN verifier checks planning artifacts
- THEN the artifact records a human checkpoint or Human Checkpoints section
- AND the maintainer decides whether to start, defer, narrow, park, kill, escalate, or create an OpenSpec/product bet
