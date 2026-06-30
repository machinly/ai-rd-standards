# W4 Build 触发专项：计费、权益、用量计量与对账规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及套餐、价格、权益、用量计量、Stripe 或类似支付平台、账本、Webhook、对账、退款或 AI 成本归因时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/00-main.md`，由主入口判断是否触发本专项。

## 目标

一人公司做 AI 产品时，最容易失控的不是“怎么接支付”，而是：套餐写在前端，权益散在代码里，用量只在供应商 dashboard 里，Webhook 重放会重复改状态，OpenAI 成本和客户账单对不上。本专项定义计费、权益、用量计量与对账规范，让每个付费 target 都能回答：卖什么，谁有权用，怎么算用量，如何同步支付平台，账怎么核对，何时必须停下来让人判断。

默认原则：产品后端才是权益执行点；本地账本先于外部同步；收费口径必须比实现更稳定。

## 核心依据

- 《人月神话》：计费复杂度来自隐藏耦合和概念不一致；一人公司不能让套餐、权益、数据库、前端和支付平台各自定义世界。
- 小型项目管理：把计费治理裁剪为少数可审工件和高影响 checkpoint，避免企业级财务流程压垮研发。
- Monetizing Innovation：产品、套餐和愿付价格要一起设计；不要等产品做完再临时补商业化。
- Martin Fowler Accounting Patterns：账务应保留可追踪 entry/transaction，纠错用补偿记录，不靠覆盖历史掩盖事实。
- Stripe Billing / Entitlements / Meter Events / Webhooks：订阅、权益、用量事件、幂等、Webhook 重试和无序到达都要显式处理。
- Stripe Ledger：资金和状态变动需要类似复式记账的可校验结构。
- OpenAI Rate Limits / Production Best Practices：OpenAI project budget 是提醒阈值，不是应用硬上限；AI 产品必须自己做用户级额度和成本保护。
- Google SRE：计费链路也需要可靠性思维，尤其是告警、重放、降级、runbook 和事后对账。

## 范围

适用对象：

- 付费 SaaS、订阅、一次性购买、seat-based、usage-based、credit-based 或混合计费。
- Stripe 或类似支付平台的 Checkout、Customer Portal、Subscription、Entitlement、Invoice、Meter Event、Webhook。
- Go/Kratos/gRPC 服务中的权益检查、用量账本、Webhook handler、对账 job。
- Vite 前端中的价格页、结账入口、账号权益展示、用量展示和升级/取消流程。
- AI workflow 的 token、请求、agent loop、tool fanout、缓存命中、成本归因和客户可理解的计量单位。

不适用对象：

- 纯内部工具、无付费计划、无客户权益差异、无外部支付或账单义务的实验。
- 公司财务报表、税务申报、收入确认和会计准则细节；这些进入专业服务或合规流程。
- 真实支付平台配置、真实客户账单操作和真实退款；规范阶段只定义工件和校验。

## 最小工件

每个付费 target 使用同一个 `<target>` 文件名：

```text
billing/
  product-catalog/<target>.json
  entitlement-policy/<target>.md
  usage-metering/<target>.json
  webhook-ledger/<target>.md
  reconciliation/<target>.json
```

### `billing/product-catalog/<target>.json`

产品目录必须包含：

- `target`
- `owner`
- `provider`
- `currency`
- `pricing_model`
- `value_metric`
- `plans`
- `features`
- `limits`
- `payment_surface`
- `tax_compliance`
- `human_checkpoint`
- `review_cadence`

`plans` 每项至少包含：

- `id`
- `name`
- `billing_interval`
- `stripe_product_ref`
- `stripe_price_refs`
- `included_features`
- `included_usage`
- `overage_policy`
- `trial`
- `status`

默认：

- 套餐、功能、额度和超额策略只能从 product catalog 派生，不在 Vite 页面或 Go 常量里另写一份。
- `value_metric` 必须是客户能理解且业务愿意长期承诺的单位，例如 seat、workspace、project、AI task、credit，不默认暴露原始 provider token。
- `payment_surface` 默认优先 hosted Checkout / Customer Portal，降低前端和 PCI 范围。

### `billing/entitlement-policy/<target>.md`

权益策略必须包含：

- `Scope`
- `Source Of Truth`
- `Feature Access`
- `Grant / Revoke`
- `Failed Payment`
- `Trial / Cancellation`
- `Grace Period`
- `Manual Override`
- `Tenant Mapping`
- `Human Checkpoints`

默认：

- Stripe entitlements / subscription state 可以作为来源，但 Go 后端必须在每个相关请求上执行权益判断。
- Vite 只能展示后端返回的权益和用量状态，不能本地解锁付费能力。
- failed payment、cancel、trial end、downgrade 必须有明确宽限期和撤权策略。
- 手工权益覆盖必须有到期时间、原因和审计记录。

### `billing/usage-metering/<target>.json`

用量计量必须包含：

- `target`
- `owner`
- `meters`
- `event_contract`
- `idempotency`
- `aggregation`
- `late_events`
- `customer_mapping`
- `quota_enforcement`
- `cost_guard`
- `sync`
- `reconciliation`
- `human_checkpoint`

`event_contract` 至少包含：

- `event_id`
- `tenant_id`
- `customer_id`
- `subscription_id`
- `feature`
- `meter`
- `quantity`
- `occurred_at`
- `request_id`

AI 用量还必须能归因：

- model 或 model tier
- prompt / workflow version
- tool iteration 或 agent loop 次数
- input / output / cached token 或等价成本字段
- cost class 或内部成本估计

默认：

- billable event 在业务完成的耐久边界写入本地账本，再异步同步到支付平台。
- `event_id` 使用 UUID-like 唯一值，本地唯一约束先去重，发送 Stripe meter event 时复用 provider identifier。
- OpenAI 成本和客户收费单位分开记录；客户账单口径稳定，内部成本口径可随模型和缓存策略调整。
- 任何 AI agent loop、批处理、导出或 tool fanout 都必须有 hard cap。

### `billing/webhook-ledger/<target>.md`

Webhook 与账本策略必须包含：

- `Scope`
- `Events`
- `Signature Verification`
- `Idempotency`
- `Ordering`
- `Retry / Replay`
- `State Transitions`
- `Ledger Tables`
- `Dead Letter`
- `Alerts`
- `Runbook`

默认：

- Webhook handler 必须验证签名，持久化 provider event id、状态和处理结果，再做业务状态迁移。
- 不依赖事件顺序；缺少对象或状态不确定时，主动向 provider 查询当前 subscription / entitlement / invoice。
- Handler 快速 ack；慢处理进入队列或后台 job。
- 手工 replay 只处理未完成或失败事件，不重复处理已成功事件。
- 不保存银行卡号、CVC、真实 token、生产 secret 或客户可识别联系方式。

### `billing/reconciliation/<target>.json`

对账策略必须包含：

- `target`
- `owner`
- `cadence`
- `sources`
- `checks`
- `sample_queries`
- `discrepancy_policy`
- `refund_credit_policy`
- `customer_support`
- `release_gates`
- `human_checkpoint`
- `status`

默认：

- 至少每日轻量检查 webhook 失败和权益漂移，每周检查本地 usage ledger、Stripe meter summaries / invoice、OpenAI usage/cost 与应用 quota。
- 对客户收费、访问权限、退款、补偿、降级产生影响的差异必须人工确认。
- 对账发现历史用量错误时，用补偿事件、credit 或明确调整记录，不直接改旧账本行。

## Go / Kratos / sqlc / gRPC 默认规则

- sqlc 表默认包含：`billing_customers`、`subscriptions`、`entitlements`、`usage_events`、`meter_sync_attempts`、`webhook_events`、`reconciliation_runs`。
- gRPC metadata 只携带 actor、tenant、request id；不接受浏览器传入“我已付费”的权益声明。
- 权益检查放在 middleware 或 usecase 边界，所有付费能力在服务端重复验证。
- `usage_events.event_id`、`webhook_events.provider_event_id`、外部 POST idempotency key 必须有唯一约束或等价保护。
- 账本 append-only；修正使用 compensating event、credit 或 adjustment。
- Stripe POST 请求使用 idempotency key；Webhook 处理和后台同步都必须可安全重试。

## Vite 前端默认规则

- 价格页、套餐卡、升级按钮和用量展示必须来自 product catalog 或后端配置，不手写散落副本。
- 付费入口默认跳 hosted Checkout / Customer Portal；不在前端处理原始卡数据。
- 权益、trial、cancel、past_due、usage remaining 只展示后端状态。
- 关键路径至少覆盖 pricing、checkout redirect、portal redirect、upgrade/downgrade/cancel 后状态刷新、quota exhausted 文案。

## AI workflow 默认规则

- AI 产品必须区分三个数：客户可理解的计费单位、内部 provider 用量、内部成本估算。
- 对 prompt cache、模型切换、batch/flex、tool call fanout 的成本变化做内部归因，但不让这些实现细节破坏客户账单语义。
- agent loop 必须有最大步数、最大 token、最大 tool call、最大成本或等价硬限制。
- OpenAI project budget / rate limit 只是外部保护层；应用仍然需要 per-user、per-tenant、per-subscription 的 hard quota。

## 需要人判断的关键点

只把这些判断交给人：

- 是否发布或改变 `pricing_model`、套餐、价格、价值计量单位或超额策略。
- 是否启用付费计划、usage-based billing、credit 扣减、试用、折扣、退款或补偿策略。
- 是否改变 billable event 语义、AI 用量折算规则、quota hard cap 或宽限期。
- 是否执行生产 Webhook replay、批量补账、批量撤权、批量 credit 或退款。
- 是否创建或延长手工权益覆盖。
- 是否把支付流程从 hosted surface 改为自处理卡数据，或改变税务/PCI 范围。
- 是否接受客户可能被重复扣费、少扣费、权益错误或 AI 成本无限增长的风险。

其他字段完整性、章节、幂等、重复处理、硬限制、敏感内容和基础对账由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“卖什么、谁能用、怎么算、怎么接收支付事件、怎么核账”。
- 保留：人只判断会影响钱、信任、税务/PCI、客户权益和不可逆生产操作的事项。
- 调整：不要求自建 billing platform；默认以 Stripe hosted surface、entitlements、meter events 和本地最小账本为主。
- 调整：不要求完整财务会计；只要求产品账、用量账和支付平台状态可对齐。
- 风险：usage-based AI billing 容易把 token 直接卖给客户。缓解：`value_metric` 和 `event_contract` 强制分离客户单位与 provider 成本。

结论：可落地。一个人可以先为第一个付费 target 写五个短工件，再用 verifier 把散落在前端、后端和支付平台里的计费知识收拢成可检查事实。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：套餐、权益、额度和退款/补偿策略进入显式工件，减少“页面写了但后端没认”的错位。
- 工程角度：Go/Kratos/sqlc/gRPC 有账本表、幂等键、唯一约束、服务端权益检查和可重试同步路径。
- 运维角度：Webhook retry/replay、dead letter、alerts 和 reconciliation 让计费事故有处理入口。
- 安全隐私角度：默认 hosted payment，禁止保存卡数据、secret、raw prompt/response 和个人联系方式。
- 成本角度：AI 内部成本、客户计费单位和 hard quota 分离，能防止单个客户或 agent loop 把现金流打穿。

结论：可落地。本专项把 W2 权限、W2 成本、W2 契约和 W7 运维串成“不会乱扣、不会乱放权、不会账不平”的最小商业化能力。
