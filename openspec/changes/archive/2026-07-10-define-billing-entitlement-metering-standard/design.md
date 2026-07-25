# Design

## 工件形态

每个付费 target 使用轻量 billing 工件：

- `billing/product-catalog/<target>.json`
- `billing/entitlement-policy/<target>.md`
- `billing/usage-metering/<target>.json`
- `billing/webhook-ledger/<target>.md`
- `billing/reconciliation/<target>.json`

JSON 记录机器可检查的套餐、计量和对账事实。Markdown 记录权益语义、Webhook 状态迁移和人工 runbook。工件不得保存真实 secret、银行卡数据、生产 token、真实客户联系方式、raw prompt 或 raw response。

## 验证策略

`billing-entitlement-metering-guard` 提供 `verify_billing_entitlements.py`：

- 检查 product catalog 的 provider、pricing model、value metric、plans、features、limits 和人审点。
- 检查 entitlement policy 必要章节和服务端执行边界。
- 检查 usage metering 的 event contract、idempotency、quota enforcement、cost guard、AI 用量归因和 provider sync。
- 检查 webhook ledger 的签名验证、幂等、无序事件、retry/replay、dead letter 和 alerts。
- 检查 reconciliation 的来源、周期、差异处理、refund/credit policy、release gates 和状态。
- 检查 secret、卡数据、联系方式、raw prompt/response 不进入 billing artifacts。

## 裁剪原则

- pre-revenue 可以先写 product catalog 和 entitlement policy，真实 provider sync 可标为 draft。
- 有付费用户前必须补齐 Webhook、用量账本、对账和退款/credit 处理。
- verifier 不判断商业定价是否正确，只检查语义是否明确、幂等是否可重试、权益是否服务端执行、用量是否可对账。
- 默认使用 Stripe hosted surface 和 entitlements/meter events；只有业务证明后才扩大 PCI 或自建 billing。
