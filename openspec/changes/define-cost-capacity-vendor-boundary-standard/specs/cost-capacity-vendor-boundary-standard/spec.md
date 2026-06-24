# cost-capacity-vendor-boundary-standard 的变更规格

## ADDED Requirements

### Requirement: 生产服务必须定义成本容量边界

生产服务、付费供应商集成或用户可见 AI workflow MUST 在发布前具备成本容量 artifact。

#### Scenario: 新服务进入生产

- GIVEN 一个服务或 AI workflow 会进入生产
- WHEN 创建 cost artifacts
- THEN 创建 `cost/budgets/<service>.json`
- AND 文件包含 `service`、`owner`、`currency`、`monthly_budget`、`unit_metric`、`cost_drivers`、`usage_units`、`alerts`、`limits`、`degradation`、`vendors`、`review_cadence`、`human_checkpoint`

#### Scenario: 仅本地实验

- GIVEN 一个实验不会访问生产数据、不会产生可计费供应商调用、不会对用户开放
- WHEN 不创建 cost artifacts
- THEN 在 OpenSpec tasks 或 design 中记录豁免原因
- AND 不得把该实验作为 production workflow 使用

### Requirement: 预算必须具备阈值、硬限制和行动

成本预算 MUST 定义可执行阈值、硬限制和超支动作。

#### Scenario: 创建预算

- GIVEN 一个服务定义月度预算
- WHEN 编写 `cost/budgets/<service>.json`
- THEN `monthly_budget` 为正数
- AND `alerts` 至少包含 50%、80%、100% 或等价阈值
- AND 100% 阈值包含 hard cap、disable、manual approval 或明确风险接受动作

#### Scenario: 请求取消硬限制

- GIVEN 预算文件没有硬限制或取消 100% 后动作
- WHEN 准备发布
- THEN `human_checkpoint.required_for` MUST 记录 `no_hard_cap` 或等价条目
- AND OpenSpec design MUST 说明现金流、用户影响和恢复方案

### Requirement: AI workflow 必须限制 token、请求和工具循环

用户可见 AI workflow MUST 定义 token、请求、工具调用和 agent loop 的成本容量限制。

#### Scenario: AI workflow 使用 OpenAI 或其他 LLM 供应商

- GIVEN `cost_drivers` 包含 AI、LLM、OpenAI、tokens 或 model usage
- WHEN 创建成本容量预算
- THEN `limits` 包含 `ai_max_tokens_per_task`
- AND `limits` 包含 `ai_max_tool_iterations` 或等价工具循环限制
- AND `limits` 包含 per-user、per-tenant、per-day 或等价请求限制

#### Scenario: 引入 autonomous agent loop

- GIVEN AI workflow 会自主循环调用模型或工具
- WHEN 准备生产发布
- THEN `human_checkpoint.required_for` MUST 记录 `autonomous_agent_loop`
- AND runbook MUST 包含 disable switch、timeout 和成本异常动作

### Requirement: 过载必须有降级或拒绝策略

服务 MUST 定义容量信号和过载处理方式，避免无限排队、无限重试或雪崩。

#### Scenario: 服务接近容量上限

- GIVEN 容量信号触发阈值
- WHEN 服务进入过载状态
- THEN 执行 `degradation` 中至少一个动作
- AND 动作可包括 load shedding、queue noncritical work、serve cached result、switch smaller model、disable expensive workflow

#### Scenario: 调用下游或第三方 API

- GIVEN 服务调用第三方 API 或供应商服务
- WHEN 实现请求
- THEN 必须有 timeout/deadline
- AND retry MUST 有上限和 backoff
- AND 不得无限重试或无限并发消耗按次付费资源

### Requirement: 供应商依赖必须记录锁定和退出边界

关键或付费供应商依赖 MUST 记录 fallback、lock-in、exit plan 和复审节奏。

#### Scenario: 创建供应商边界

- GIVEN 服务依赖关键或付费外部供应商
- WHEN 创建 `cost/vendors/<service>.md`
- THEN 文档包含 Vendors、Critical Paths、Lock-In Risk、Fallback、Exit Plan、Contract/SLA Notes、Review Cadence
- AND `cost/budgets/<service>.json` 的 vendors 条目引用该 exit plan

#### Scenario: 关键路径只有单一供应商且无 fallback

- GIVEN 供应商 criticality 为 high 且 fallback 为空或不可运行
- WHEN 准备生产发布
- THEN `human_checkpoint.required_for` MUST 记录 `single_vendor_no_fallback`
- AND design MUST 说明接受原因、迁移触发条件和人工恢复方案

### Requirement: 成本容量 runbook 必须覆盖超支、过载和供应商事故

生产服务 MUST 维护成本容量 runbook，用于一个人在超支或过载时快速行动。

#### Scenario: 创建 runbook

- GIVEN 服务进入生产
- WHEN 创建 `cost/runbooks/<service>.md`
- THEN 文档包含 Signals、50 Percent Budget Action、80 Percent Budget Action、100 Percent Budget Action、Overload / Rate Limit Action、Vendor Incident Action、Rollback / Disable Switch

#### Scenario: 真实账单或用量异常

- GIVEN 预算、供应商账单、rate limit 或容量信号异常
- WHEN 进行月度复审或事故处理
- THEN 更新 `cost/usage/<service>.md` 或 incident/release 记录
- AND 最多选择一个最高影响成本容量改进动作
