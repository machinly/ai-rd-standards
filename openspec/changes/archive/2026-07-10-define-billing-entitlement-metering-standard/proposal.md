# Proposal: define billing entitlement metering standard

## 意图

建立一人公司计费、权益、用量计量与对账规范，覆盖产品目录、套餐、权益来源、用量事件契约、Webhook 幂等、账本、对账和 AI 成本/额度边界，避免付费产品出现重复扣费、少扣费、错误放权、无限 AI 成本或账单不可解释。

## 范围

- 新增 `billing-entitlement-metering-standard` spec。
- 新增 W4 计费与权益触发专项文档。
- 创建 `billing-entitlement-metering-guard` skill 和 verifier。
- 补充来源索引与 README。

## 不做什么

- 不替代公司财务、税务申报、收入确认或法律合规服务。
- 不连接真实 Stripe 账号、真实客户、真实发票、真实退款或生产 Webhook。
- 不要求自建计费平台；默认使用 Stripe 或类似托管支付平台。
- 不把 OpenAI project budget 误当应用硬额度；应用仍需本地 quota 和账本。

## 依据

- 《人月神话》和小型项目管理裁剪原则。
- Monetizing Innovation：产品、套餐与愿付价格一起设计。
- Martin Fowler Accounting Entry / Accounting Transaction。
- Stripe Billing、Entitlements、Meter Events、Webhooks、Idempotent Requests、Integration Security。
- Stripe Ledger 工程实践。
- OpenAI Rate Limits、Production Best Practices、Prompt Caching。
- Google SRE 可靠性、告警、重放和 runbook 思想。

## 需要人的判断

只有这些需要人工 checkpoint：定价/套餐/价值计量单位、usage-based billing 或 credit 扣减语义、退款/补偿策略、生产 Webhook replay、批量补账/撤权、手工权益覆盖、failed payment 宽限期、税务/PCI 范围、外部计费供应商替换、无限 AI 用量或没有 hard cap。
