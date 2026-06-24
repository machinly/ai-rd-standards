# W5 Verify 触发专项：韧性演练、故障注入与降级验证规范

## W5 触发定位

本文件是 W5 Verify 的触发型专项，不是 W5 主入口。只有当当前验证涉及依赖失败、timeout、429/5xx、重试、降级、故障注入、dead letter、blast radius、AI provider 故障或韧性演练时，才需要读取本文件。

普通 W5 验证入口应先回到 `docs/W5-verify/main.md`，由主入口判断是否触发本专项。

## 目标

一人公司的可靠性风险通常不是“不知道要加 timeout/fallback”，而是**从未验证这些保护在真实故障形态下是否工作**。代码里有重试，但供应商 429 时可能制造重试风暴；文档写了降级，但 UI 可能没有可用状态；队列有 dead letter，但没人演练回放；AI provider 超时后，用户可能卡在加载中。

本专项负责回答一个窄问题：**当关键依赖变慢、失败、限流、返回坏数据或部分不可用时，系统是否能保持可解释、可停止、可恢复，并把 blast radius 控制在一人公司能处理的范围内。**

默认原则：**没有失败模式、实验假设、注入运行、降级证据和复盘，就不要声称系统有韧性。** 本专项不追求大型 chaos 平台；先用低风险、可停止、可复盘的演练证明最关键路径。

## 核心依据

- 《人月神话》：复杂系统没有银弹；韧性来自概念完整性、接口边界和对隐藏耦合的持续暴露。
- 小型项目管理：一人公司不做重型 chaos program；只保留能支持一次低风险演练的五个工件。
- Google SRE Testing for Reliability：可靠性测试的目的不是证明“测试通过”，而是减少变更后对未来行为的不确定性。
- Google SRE Addressing Cascading Failures / Handling Overload：级联故障常由过载、无界重试、资源耗尽和依赖失败放大；需要 backoff、jitter、限流、降级和快速失败。
- Google SRE Incident Response / DiRT：演练能让人和系统在低风险情况下形成响应记忆；演练后要复盘流程缺口。
- Principles of Chaos Engineering：实验应先定义 steady state、提出假设、注入真实世界变量、最小化 blast radius，并用观测结果反驳假设。
- `Release It!`：生产稳定性模式包括 timeout、circuit breaker、bulkhead、fail fast、shed load、back pressure 和 test harness；这些模式必须被验证。
- Google `Building Secure and Reliable Systems`：单系统故障注入能在不打扰全系统或依赖方的情况下测试 timeout、错误处理和异常路径。
- gRPC Deadlines / Go context：RPC 默认不会自动设置 deadline；Go 服务要传播取消信号，避免下游故障造成资源泄漏。
- Kratos Circuit Breaker：client circuit breaker 触发后应快速失败，避免继续压垮下游。
- OpenAI Rate Limits：AI 供应商 rate limit 要使用带 jitter 的指数退避和最大重试次数；连续重发会继续消耗限额。
- AWS Well-Architected Game Days：game day 用受控方式模拟失败，测试系统、流程和人的恢复能力。

## 范围

适用对象：

- 用户可见核心路径、付费路径、AI workflow、后台 worker、Webhook、RAG ingestion、导入/导出、支付/邮件/认证等外部依赖路径。
- Go/Kratos/sqlc/gRPC 服务中的 timeout、deadline、retry budget、circuit breaker、bulkhead、backpressure、load shedding、idempotency、queue/dead letter。
- Vite 前端中的 degraded UI、重试状态、只读模式、维护页、错误提示、用户可行动状态。
- AI workflow 中的 OpenAI/LLM provider 429/5xx/timeout、schema failure、tool failure、RAG empty/poisoned context、fallback route、人工接管。

不适用对象：

- SLO、告警、incident/postmortem 基础结构；走 W7 SRE-lite 专项。
- 成本容量、限额、过载 runbook 和供应商退出计划；走 W2 成本容量专项。
- 通用测试矩阵和发布前 test run；走 W5 测试质量专项。
- 备份、恢复、RPO/RTO、PITR 和业务连续性；走 W7 备份恢复专项。
- 性能预算、负载画像和性能回归报告；走 W5 性能回归专项。
- 大规模生产 chaos automation、区域级故障注入、真实客户流量实验、持续故障平台；真实规模证明需要后再单独开 change。

## 最小工件

每个韧性目标使用同一个 `<target>` 文件名：

```text
resilience/
  failure-mode-map/<target>.json
  experiment-plan/<target>.md
  fault-injection-run/<target>.json
  degradation-check/<target>.md
  resilience-review/<target>.md
```

`<target>` 可以是服务、RPC、前端路径、AI capability、worker、集成或关键用户旅程，例如 `assistant-answer`、`billing-webhook`、`rag-ingestion`。

### `resilience/failure-mode-map/<target>.json`

失败模式地图必须包含：

- `target`
- `owner`
- `user_journeys`
- `dependencies`
- `failure_modes`
- `steady_state_signals`
- `blast_radius`
- `controls`
- `rollback_or_disable`
- `observability_refs`
- `linked_slo_refs`
- `human_checkpoint`
- `review_cadence`
- `status`

`failure_modes` 每条至少包含：

- `id`
- `dependency`
- `type`
- `trigger`
- `expected_behavior`
- `user_impact`
- `detection`
- `mitigation`
- `priority`

默认规则：

- `type` 使用 `latency`、`timeout`、`5xx`、`429_rate_limit`、`malformed_response`、`partial_response`、`dependency_down`、`db_unavailable`、`queue_backlog`、`dead_letter`、`network_partition`、`auth_failure`、`quota_exhausted`、`cache_unavailable`、`ai_schema_failure`、`tool_failure`、`rag_empty`、`config_bad` 中适用项。
- `steady_state_signals` 必须连接 W7 SRE-lite、W7 观测性和 W5 性能专项：latency、error、traffic、saturation、fallback rate、queue age、AI token/cost、user task success 中适用项。
- 第一版只选 1-3 个最高影响失败模式；不要把所有可能故障一次性列满。
- 如果 failure mode 影响资金、权限、隐私、数据写入、付费客户或合同 SLA，必须有人审。

### `resilience/experiment-plan/<target>.md`

实验计划必须包含：

```markdown
# <target> Resilience Experiment Plan

## Scope

## Hypothesis

## Steady State

## Failure Mode

## Blast Radius

## Environment

## Injection Method

## Safety Controls

## Stop Conditions

## Observability

## Expected Degradation

## Rollback / Abort

## Human Checkpoints

## Linked Artifacts

## Review Cadence
```

默认规则：

- `Hypothesis` 必须可反驳，例如“OpenAI 429 持续 2 分钟时，服务最多重试 3 次，进入排队/基础模式，p95 不超过预算，用户看到可行动状态”。
- `Steady State` 写用户可见输出，不只写内部 CPU。
- `Injection Method` 默认用 mock、sandbox、staging、feature flag、dependency stub、local fault injection 或 contract test；不默认生产注入。
- `Safety Controls` 必须定义请求数、租户/用户范围、费用上限、数据边界、禁写、回滚开关、观察人和停止方式。
- `Stop Conditions` 必须能让一个人立刻停止实验：错误率、p95/p99、队列、费用、真实用户影响、数据写入、告警、供应商限流等。

### `resilience/fault-injection-run/<target>.json`

故障注入运行记录必须包含：

- `target`
- `owner`
- `experiment_ref`
- `date`
- `environment`
- `injection`
- `steady_state_before`
- `observations`
- `steady_state_after`
- `user_impact`
- `stop_condition_hit`
- `rollback_or_abort`
- `decision`
- `gaps`
- `actions`
- `human_checkpoint`
- `status`

`decision` 只允许：

- `pass`
- `pass_with_notes`
- `needs_fix`
- `abort`
- `accepted_risk`
- `defer`

默认规则：

- `observations` 必须包含实际信号，不只写“正常”。
- `stop_condition_hit = true` 时必须记录 `rollback_or_abort`。
- `accepted_risk`、`abort`、真实用户影响、生产环境、真实供应商、真实数据、资金/权限/隐私影响都必须有人审。
- 有 `gaps` 时必须有 `actions`；行动项最多 3 个。

### `resilience/degradation-check/<target>.md`

降级证据必须包含：

```markdown
# <target> Degradation Check

## Scope

## Degraded Mode

## User Experience

## Data / Side Effects

## AI / External Dependencies

## Timeout / Retry / Backpressure

## Observability

## Verification Commands

## Evidence

## Gaps

## Human Checkpoints

## Linked Artifacts

## Review Cadence
```

默认规则：

- `Degraded Mode` 必须说明降级后用户还能做什么、不能做什么、是否可稍后重试或转人工。
- `Data / Side Effects` 必须说明是否禁止写入、幂等、重复消费、外部副作用和补偿动作。
- `Timeout / Retry / Backpressure` 必须说明 deadline、最大重试、backoff、jitter、queue limit、circuit breaker 或 load shedding 中适用项。
- `Evidence` 必须链接日志、trace、测试输出、截图、run id、fixture 或命令结果；不保存 raw customer data 或 raw prompt/response。

### `resilience/resilience-review/<target>.md`

韧性复盘必须包含：

```markdown
# <target> Resilience Review

## Recent Changes

## Experiments Run

## Steady State Health

## Failure Modes Covered

## Degradation Evidence

## User / SLO Impact

## Open Gaps

## Action Items

## One Next Experiment

## Review Cadence
```

默认规则：

- `Action Items` 最多 3 个，必须有 owner 或跟踪引用。
- `One Next Experiment` 只选一个下一次最值得验证的失败模式；没有就写 `no action`。
- 如果连续两次发现同类缺口，必须升级到 W5 测试质量门禁、W5 性能门禁或 W7 SRE runbook。

## 默认流程

1. 选一个 `<target>`：只选最关键用户路径或最近变更影响的依赖。
2. 写 `failure-mode-map`：列 1-3 个最可能造成用户伤害的失败模式。
3. 写 `experiment-plan`：给每个实验写 hypothesis、steady state、blast radius、安全控制和停止条件。
4. 先跑低风险演练：unit/contract fault injection、mock provider、staging sandbox 或 tabletop。
5. 写 `fault-injection-run`：记录真实观察、是否触发停止条件、gap 和决策。
6. 写 `degradation-check`：证明用户体验、数据副作用、AI/外部依赖、timeout/retry/backpressure 都符合预期。
7. 写 `resilience-review`：只保留一个下一次实验或一个修复动作。

## Go / Kratos / sqlc / gRPC 默认规则

- Go 服务用 `context.Context` 传播 cancel/deadline；长任务必须检查 `ctx.Done()`，避免 goroutine、DB query 或外部调用泄漏。
- gRPC client 必须显式设置 realistic deadline；server 侧要尊重取消，避免已超时请求继续消耗资源。
- Kratos middleware 优先使用 recovery、logging、metrics/tracing、circuit breaker、ratelimit 或 timeout 中适用能力；不要把韧性逻辑散落在每个 handler。
- 外部依赖调用必须有 timeout、最大重试、backoff+jitter、retry budget 和错误分类。
- sqlc/PostgreSQL 失败演练要覆盖连接耗尽、慢查询、事务取消、死锁/唯一约束冲突、重复消息幂等和只读降级中适用项。
- fault injection 默认通过接口 mock、test double、dependency stub、staging config 或本地 proxy；生产注入需要人审。

## Vite 前端默认规则

- 降级 UI 使用 Vercel Geist 风格：克制、清晰、可行动，不用花哨错误页掩盖失败。
- 用户可见状态至少区分：可重试、已排队、基础模式、只读模式、稍后通知、需要人工处理、不可恢复。
- 前端必须避免无限 spinner；外部依赖失败时要有 timeout、retry copy 或 fallback screen。
- Playwright 或等价 E2E 可验证 degraded UI；不要求第一天完整视觉回归。

## AI workflow 默认规则

- AI provider 429/5xx/timeout 默认先进入有上限的 backoff、排队、较小模型、缓存答案、基础模式或人工处理，不允许无限重试。
- tool failure、RAG empty、schema parse failure、safety block、provider outage 都必须有可观测 reason 和用户可行动状态。
- 不允许 agent 在故障状态下扩大权限、绕过审批、改用未验证工具或无限循环自救。
- 真实 OpenAI/LLM provider 故障演练默认使用 mock/recorded response；真实 provider 演练必须设置请求数、费用、速率和数据边界。
- fallback 降低质量、改变安全拒答、改变数据边界或影响付费/高风险路径时必须有人审。

## 需要人判断的关键点

默认不问：

- 文件命名、普通字段完整性、mock/staging 演练、tabletop、低风险 `pass`、没有 gap 的 `no action`。

必须问：

- 是否在 production、共享环境、真实客户流量、真实客户数据、真实供应商或真实付费 AI provider 上注入故障。
- 是否演练会触发真实写入、资金、权限、隐私、安全、合规、邮件/SMS、Webhook side effect 或用户通知。
- 是否接受 `accepted_risk`、带 gap 发布、跳过降级验证或扩大 blast radius。
- 是否自动 failover、自动切供应商、自动关闭核心功能、自动降级付费/高风险路径。
- 是否关闭/弱化 timeout、rate limit、retry budget、circuit breaker、backpressure、fallback、dead letter 或人工审批。
- 是否把 chaos/fault injection 自动化为定期生产任务。

其他字段、章节、敏感信息、正反 fixture、OpenSpec 链接、状态枚举和报告结构由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“会怎么坏、要证明什么、实际发生什么、降级是否可用、下一次测什么”。
- 保留：人只判断生产/真实数据/真实供应商、真实副作用、接受风险、扩大 blast radius、自动化故障和弱化保护。
- 调整：不要求 Chaos Monkey 或生产流量实验；一人公司先用 mock、staging、tabletop 和 targeted fault injection。
- 调整：每次只验证 1 个失败模式，行动项最多 3 个，防止演练变成新项目。
- 风险：韧性演练可能制造事故。缓解：强制 safety controls、stop conditions、blast radius 和 abort path。

结论：可落地。本专项让一个人在一两个专注块里验证最关键降级路径，而不是背上一套 chaos 工程平台。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：degraded mode 明确用户还能做什么，避免把失败变成空白页或无限等待。
- 工程角度：Go context、gRPC deadline、Kratos circuit breaker、sqlc 幂等和 AI fallback 都有验证入口。
- 运维角度：steady state、stop conditions、blast radius 和 run evidence 让演练可停止、可复盘。
- 安全隐私角度：真实数据、权限、资金、通知、供应商和 raw prompt/response 都进入人审边界。
- 成本角度：先用 mock/staging 演练，真实 provider 和生产故障注入必须有请求、费用和速率上限。

结论：可落地。它补上 W7 SRE-lite、W2 成本容量、W7 备份恢复、W3 模型路由、W4 异步任务、W8 AI 质量和 W5 性能之间的韧性验证空白：不是再写一个 runbook，而是证明 runbook 里的降级路径真的跑得通。
