# ai-quality-regression-incident-standard Specification

## Purpose

Define the minimum AI behavior quality regression, incident, rollback, and review standard for a one-person AI company.

## Requirements

### Requirement: 生产 AI capability 必须具备 ai-quality 工件

Any production user-visible AI capability MUST have AI quality regression artifacts.

#### Scenario: 上线或维护生产 AI capability

- GIVEN 一个 capability 产生用户可见 AI 输出、工具动作、检索答案、分类、抽取、总结、推荐、审核或 agent workflow
- WHEN 创建研发 OpenSpec change
- THEN 创建 `ai-quality/signal-contract/<capability>.json`
- AND 创建 `ai-quality/regression-triage/<capability>.md`
- AND 创建 `ai-quality/rollback-runbook/<capability>.md`
- AND 创建 `ai-quality/incident-log/<capability>.json`
- AND 创建 `ai-quality/quality-review/<capability>.md`
- AND 在 OpenSpec proposal 或 design 中链接 ai-quality artifacts

### Requirement: Signal contract 必须定义质量维度、离线/线上信号、阈值、eval、telemetry、采样、告警和回滚链接

Signal contract MUST connect offline evaluation and online production/user signals to concrete actions.

#### Scenario: 定义 AI 质量信号

- GIVEN 一个 production AI capability
- WHEN 创建 `ai-quality/signal-contract/<capability>.json`
- THEN it records capability、owner、user_journey、quality_dimensions、leading_signals、lagging_signals、thresholds、eval_links、telemetry_links、sampling_policy、alert_policy、rollback_link、human_checkpoint、review_cadence、status
- AND at least one signal links to offline eval evidence
- AND at least one signal links to online production, support, product, or user feedback evidence
- AND each threshold records condition, severity, action, and rollback or human checkpoint decision

### Requirement: Regression triage 必须定义严重度、检测信号、首 15 分钟、复现、范围、原因、决策、证据和升级

Regression triage MUST make AI quality degradation actionable for one maintainer.

#### Scenario: 分诊质量回归

- GIVEN quality signals or user feedback indicate possible regression
- WHEN 创建 `ai-quality/regression-triage/<capability>.md`
- THEN it includes Scope, Severity Levels, Detection Signals, First 15 Minutes, Reproduction, Scope Check, Likely Causes, Decision Matrix, Evidence To Capture, Escalation, Linked Artifacts, and Review Cadence
- AND Q-SEV1/Q-SEV2 decisions require human checkpoint

### Requirement: Rollback runbook 必须定义关闭开关、回滚路径、模型/prompt/route、检索/工具、用户提示、验证、安全检查和恢复标准

Rollback runbook MUST let the maintainer stop user harm before deep debugging.

#### Scenario: 回滚或降级 AI capability

- GIVEN quality regression affects users or release confidence
- WHEN 创建 `ai-quality/rollback-runbook/<capability>.md`
- THEN it includes Scope, Disable Switches, Rollback Paths, Model / Prompt / Route Rollback, Retrieval / Tool Rollback, User Messaging, Validation, Data / Safety Checks, Recovery Criteria, Post-Rollback Follow Up, Linked Artifacts, and Review Cadence
- AND rollback validation checks quality signals, not only service health

### Requirement: Incident log 必须记录质量事故、用户影响、版本/route、检测、响应、缓解、eval follow-up 和状态

Incident log MUST preserve enough evidence to learn without storing sensitive raw content.

#### Scenario: 记录 AI 质量事故

- GIVEN a capability has no incidents yet
- WHEN 创建 `ai-quality/incident-log/<capability>.json`
- THEN it may contain an empty `incidents` list
- AND records capability、owner、incidents、linked_artifacts、human_checkpoint、review_cadence、status

#### Scenario: 记录已发生事故

- GIVEN an AI quality incident occurred
- WHEN adding an item to `incidents`
- THEN it records id、date、severity、trigger、user_impact、affected_versions、affected_routes、detection、response、rollback_or_mitigation、eval_followup、owner、status
- AND Q-SEV1/Q-SEV2 incidents record rollback or mitigation and eval follow-up

### Requirement: Quality review 必须复盘近期变化、信号健康、eval/dataset drift、用户反馈、事故、噪声、回滚准备、开放风险和下一项改进

Quality review MUST keep the system improving without turning quality work into a platform project.

#### Scenario: 周期复盘 AI 质量

- GIVEN a production AI capability
- WHEN 更新 `ai-quality/quality-review/<capability>.md`
- THEN it includes Recent Changes, Signal Health, Eval / Dataset Drift, User Feedback / Support, Incidents / Regressions, False Positives / Noise, Rollback Readiness, Open Risks, One Next Change, and Review Cadence
- AND review selects one next change rather than an unbounded backlog
