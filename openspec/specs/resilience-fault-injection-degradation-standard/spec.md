# resilience-fault-injection-degradation-standard Specification

## Purpose

定义一人公司韧性演练、故障注入、降级验证和复盘的最小规范，使关键用户路径、Go/Kratos/gRPC 服务、sqlc/PostgreSQL 路径、Vite 降级 UI、AI workflow、worker、Webhook 和外部依赖能在低风险实验中证明 timeout、retry、circuit breaker、fallback、backpressure 和 degraded mode 真的可用。

## Requirements

### Requirement: 高风险韧性目标必须定义 resilience artifacts

Critical user journeys, paid paths, AI workflows, external-dependency paths, workers, webhooks, data pipelines, and high-risk degraded modes MUST have resilience artifacts before claiming graceful degradation or fault tolerance.

#### Scenario: 新目标进入韧性验证

- GIVEN 一个 target 依赖外部服务、AI provider、数据库、队列、Webhook、RAG source、工具调用、前端关键路径或后台任务
- WHEN 创建 resilience artifacts
- THEN 创建 `resilience/failure-mode-map/<target>.json`
- AND 创建 `resilience/experiment-plan/<target>.md`
- AND 创建 `resilience/fault-injection-run/<target>.json`
- AND 创建 `resilience/degradation-check/<target>.md`
- AND 在 OpenSpec design 或 tasks 中链接 resilience artifacts

#### Scenario: 低风险目标暂不演练

- GIVEN 一个变更不影响用户可见路径、数据写入、外部依赖、AI 行为、队列、成本、权限、安全或性能
- WHEN 不创建 resilience artifacts
- THEN 在 OpenSpec tasks 或变更说明中记录跳过原因

### Requirement: Failure-mode map 必须定义依赖、失败模式、steady state、blast radius 和控制

Failure-mode map MUST record target, owner, user journeys, dependencies, failure modes, steady-state signals, blast radius, controls, rollback/disable path, observability refs, linked SLO refs, human checkpoint, review cadence, and status.

#### Scenario: 创建 failure-mode map

- GIVEN target 需要韧性验证
- WHEN 创建 `resilience/failure-mode-map/<target>.json`
- THEN 文件包含 `target`、`owner`、`user_journeys`、`dependencies`、`failure_modes`、`steady_state_signals`、`blast_radius`、`controls`、`rollback_or_disable`、`observability_refs`、`linked_slo_refs`、`human_checkpoint`、`review_cadence`、`status`
- AND `failure_modes` 至少包含一条 `id`、`dependency`、`type`、`trigger`、`expected_behavior`、`user_impact`、`detection`、`mitigation`、`priority`
- AND `steady_state_signals` 至少包含 latency、error、traffic、saturation、fallback rate、queue age、AI token/cost 或 user task success 中适用项

### Requirement: Experiment plan 必须提出可反驳假设并定义安全边界

Experiment plan MUST record scope, hypothesis, steady state, failure mode, blast radius, environment, injection method, safety controls, stop conditions, observability, expected degradation, rollback/abort, human checkpoints, linked artifacts, and review cadence.

#### Scenario: 创建 experiment plan

- GIVEN target 准备故障注入或 game-day 演练
- WHEN 创建 `resilience/experiment-plan/<target>.md`
- THEN 文档包含 Scope、Hypothesis、Steady State、Failure Mode、Blast Radius、Environment、Injection Method、Safety Controls、Stop Conditions、Observability、Expected Degradation、Rollback / Abort、Human Checkpoints、Linked Artifacts、Review Cadence
- AND Hypothesis、Steady State、Safety Controls、Stop Conditions 不为空

#### Scenario: 高风险实验

- GIVEN experiment 涉及 production、共享环境、真实客户流量、真实客户数据、真实供应商、真实付费 AI provider 或真实 side effect
- WHEN 准备执行实验
- THEN Human Checkpoints MUST 记录对应风险
- AND Safety Controls MUST 记录 blast radius、请求数或用户范围、费用或速率上限、停止方式和 rollback/abort 路径

### Requirement: Fault-injection run 必须记录实际观察、决策、gap 和行动

Fault-injection run MUST record experiment ref, date, environment, injection, steady state before/after, observations, user impact, stop condition, rollback/abort, decision, gaps, actions, human checkpoint, and status.

#### Scenario: 记录故障注入运行

- GIVEN 完成一次 fault injection、tabletop、staging drill、mock-provider run 或 game day
- WHEN 创建 `resilience/fault-injection-run/<target>.json`
- THEN 文件包含 `target`、`owner`、`experiment_ref`、`date`、`environment`、`injection`、`steady_state_before`、`observations`、`steady_state_after`、`user_impact`、`stop_condition_hit`、`rollback_or_abort`、`decision`、`gaps`、`actions`、`human_checkpoint`、`status`
- AND `decision` 是 `pass`、`pass_with_notes`、`needs_fix`、`abort`、`accepted_risk` 或 `defer`
- AND observations 包含实际信号

#### Scenario: 发现缺口或触发停止条件

- GIVEN `stop_condition_hit` 为 true
- OR `decision` 是 `accepted_risk`、`abort`、`pass_with_notes`
- OR `gaps` 非空
- WHEN 记录 run
- THEN `rollback_or_abort` MUST 记录可执行动作
- AND `actions` MUST 记录修复或后续验证
- AND `human_checkpoint` MUST 覆盖风险接受或停止条件

### Requirement: Degradation check 必须证明用户体验、数据副作用和保护机制

Degradation check MUST record degraded mode, user experience, data/side effects, AI/external dependency behavior, timeout/retry/backpressure, observability, verification commands, evidence, gaps, human checkpoints, linked artifacts, and review cadence.

#### Scenario: 创建 degradation check

- GIVEN target 声称有 fallback、degraded mode、queue、manual operation、read-only mode 或 provider fallback
- WHEN 创建 `resilience/degradation-check/<target>.md`
- THEN 文档包含 Scope、Degraded Mode、User Experience、Data / Side Effects、AI / External Dependencies、Timeout / Retry / Backpressure、Observability、Verification Commands、Evidence、Gaps、Human Checkpoints、Linked Artifacts、Review Cadence
- AND Verification Commands 与 Evidence 不为空

### Requirement: Resilience review 必须只保留少量行动和一个下一次实验

Resilience review MUST record recent changes, experiments run, steady-state health, failure modes covered, degradation evidence, user/SLO impact, open gaps, action items, one next experiment, and review cadence.

#### Scenario: 创建 resilience review

- GIVEN target 已执行故障注入或降级验证
- WHEN 创建 `resilience/resilience-review/<target>.md`
- THEN 文档包含 Recent Changes、Experiments Run、Steady State Health、Failure Modes Covered、Degradation Evidence、User / SLO Impact、Open Gaps、Action Items、One Next Experiment、Review Cadence
- AND One Next Experiment 为空时必须明确 `no action`

### Requirement: Go/Kratos/sqlc/gRPC 目标必须验证 deadline、cancel、retry 和隔离控制

Go/Kratos/sqlc/gRPC targets MUST verify context cancellation, gRPC deadlines, retry limits, backoff/jitter, circuit breaker, idempotency, and database/queue failure behavior where applicable.

#### Scenario: Go/Kratos/gRPC 目标

- GIVEN target 涉及 Go、Kratos、gRPC、sqlc、PostgreSQL、queue 或 worker
- WHEN 编写 experiment plan 和 degradation check
- THEN Injection Method 或 Verification Commands 包含 mock、test double、local proxy、staging config、contract test、integration test、gRPC deadline/cancel test、DB failure test 或 queue failure test 中适用项
- AND Timeout / Retry / Backpressure 覆盖 deadline、cancel、max retries、backoff/jitter、circuit breaker、queue limit 或 load shedding 中适用项

### Requirement: AI workflow 目标必须验证 provider、schema、tool、RAG 和 fallback 失败路径

AI workflow targets MUST verify provider timeout/rate-limit/5xx, schema parse failure, tool failure, RAG empty or unsafe context, fallback behavior, and user-visible degraded state where applicable.

#### Scenario: AI workflow 故障

- GIVEN target 涉及 prompt、model、OpenAI/LLM provider、RAG、tool、agent、schema、model route 或 AI fallback
- WHEN 创建 failure-mode map 和 degradation check
- THEN failure_modes 覆盖 provider timeout、429/5xx、schema failure、tool failure、RAG empty/unsafe context 或 fallback quality risk 中适用项
- AND degradation check 记录用户可行动状态、fallback reason、tool/agent stop condition、token/cost boundary 和安全/质量边界
