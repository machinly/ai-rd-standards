# billing-entitlement-metering-standard 规格

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义一人公司付费 AI 产品的计费、权益、用量计量、Webhook 处理和对账规则，确保套餐、功能访问、AI 用量、支付平台状态、本地账本和客户账单能被服务端执行、幂等重试和周期性核对。

## Requirements

### Requirement: 付费 target 必须定义 billing artifacts

付费服务、前端应用、用户可见 AI workflow 或任何会影响客户访问/账单的 target MUST 在发布前具备 billing entitlement metering artifacts。

#### Scenario: 新付费 target 进入发布准备

- GIVEN 一个 target 存在订阅、套餐、用量计费、credit 扣减、试用、退款或客户权益差异
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `billing/product-catalog/<target>.json`
- AND 创建 `billing/entitlement-policy/<target>.md`
- AND 创建 `billing/usage-metering/<target>.json`
- AND 创建 `billing/webhook-ledger/<target>.md`
- AND 创建 `billing/reconciliation/<target>.json`

### Requirement: Product catalog 必须定义套餐、功能、额度和支付边界

Product catalog MUST 记录 target、owner、provider、currency、pricing model、value metric、plans、features、limits、payment surface、tax compliance、人审点和复审节奏。

#### Scenario: 创建付费产品目录

- GIVEN 一个 target 有付费计划或权益差异
- WHEN 创建 `billing/product-catalog/<target>.json`
- THEN 文件包含 `target`、`owner`、`provider`、`currency`、`pricing_model`、`value_metric`、`plans`、`features`、`limits`、`payment_surface`、`tax_compliance`、`human_checkpoint`、`review_cadence`
- AND 每个 plan 记录 id、name、billing interval、provider product/price reference、included features、included usage、overage policy、trial 和 status

### Requirement: Entitlement policy 必须定义权益来源和服务端执行规则

Entitlement policy MUST 记录 scope、source of truth、feature access、grant/revoke、failed payment、trial/cancellation、grace period、manual override、tenant mapping 和 human checkpoints。

#### Scenario: 检查付费功能访问

- GIVEN 用户请求付费功能或 AI 用量
- WHEN Go/Kratos/gRPC 服务处理请求
- THEN 服务端根据 subscription、entitlement、tenant mapping 和本地策略判断访问
- AND Vite 前端只展示后端返回的权益状态，不在浏览器本地解锁付费能力

### Requirement: Usage metering 必须定义可重试、可归因、可对账的事件契约

Usage metering MUST 记录 meters、event contract、idempotency、aggregation、late events、customer mapping、quota enforcement、cost guard、sync、reconciliation 和 human checkpoint。

#### Scenario: 记录一次 billable AI 用量

- GIVEN 用户完成一次可计费 AI workflow
- WHEN 系统写入用量事件
- THEN 事件包含 event_id、tenant_id、customer_id、subscription_id、feature、meter、quantity、occurred_at 和 request_id
- AND AI 用量能追踪 model 或 tier、prompt/workflow version、tool iteration/agent loop、token 或成本字段
- AND 本地账本先持久化，再用幂等 identifier 同步到支付平台

### Requirement: Webhook ledger 必须幂等处理签名验证、重试、无序和重放

Webhook ledger MUST 记录 scope、events、signature verification、idempotency、ordering、retry/replay、state transitions、ledger tables、dead letter、alerts 和 runbook。

#### Scenario: 支付平台重复投递或无序投递事件

- GIVEN Webhook handler 收到 provider event
- WHEN 处理事件
- THEN handler 验证签名
- AND 持久化 provider event id、处理状态和结果
- AND 已成功处理的事件不会重复修改权益或账本
- AND 状态不确定时主动查询 provider 当前对象，而不是依赖事件顺序

### Requirement: Reconciliation 必须核对本地账本、支付平台、权益和 AI 成本

Reconciliation MUST 记录 cadence、sources、checks、sample queries、discrepancy policy、refund/credit policy、customer support、release gates、human checkpoint 和 status。

#### Scenario: 周期性对账发现差异

- GIVEN 本地 usage ledger、Stripe meter/invoice/subscription、应用 entitlement 和 OpenAI usage/cost 存在差异
- WHEN 运行 reconciliation check
- THEN 记录差异、影响范围、处理动作和人审状态
- AND 影响客户收费、退款、credit、访问权限或 AI 成本失控的差异必须人工确认

### Requirement: 高风险计费决策必须人工 checkpoint

Pricing model change、paid plan launch、customer charge/refund policy、manual entitlement override、failed payment deprovision policy、meter semantics change、production webhook replay、tax/PCI scope change、external billing provider change 或 unlimited AI usage/no hard cap MUST 有人工 checkpoint。

#### Scenario: 变更触发高风险计费条件

- GIVEN OpenSpec change、release 或运营动作触发高风险计费条件
- WHEN 准备合并、发布或执行
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND 对应 product catalog、entitlement policy、usage metering、webhook ledger 或 reconciliation artifact 记录需要人的判断

### Requirement: Billing artifacts 不得保存敏感支付、凭据或原始 AI 内容

Billing artifacts MUST NOT 保存银行卡号、CVC、真实 secret、生产 token、供应商凭据、真实客户联系方式、raw prompt、raw response 或完整个人账单内容。

#### Scenario: 记录计费配置和对账证据

- GIVEN 需要记录支付平台引用、账本字段、对账查询或 Webhook 处理证据
- WHEN 写入 `billing/` artifacts
- THEN 使用 provider object reference、占位符、角色名、查询模板和 runbook 链接
- AND 不保存真实卡数据、secret、生产 token、客户联系方式、raw prompt 或 raw response
