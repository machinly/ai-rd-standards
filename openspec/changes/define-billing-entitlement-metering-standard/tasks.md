# 任务

## 1. 来源与约束

- [x] 1.1 查证 Stripe Billing subscriptions、Entitlements、Meter Events、Meters、Webhooks、Idempotent Requests 和 Integration Security。
- [x] 1.2 查证 OpenAI Rate Limits、Projects budgets、Production Best Practices 和 Prompt Caching。
- [x] 1.3 查证 Martin Fowler Accounting Patterns、Stripe Ledger 和 Monetizing Innovation。
- [x] 1.4 补充阶段 22 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 计费权益用量规范

- [x] 2.1 编写阶段 22 规范正文。
- [x] 2.2 定义 product catalog、entitlement policy、usage metering、webhook ledger、reconciliation artifacts。
- [x] 2.3 定义 Go/Kratos/sqlc/gRPC、Vite、AI workflow 默认规则和人审点。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 22 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `billing-entitlement-metering-guard` skill。
- [x] 4.2 添加 billing artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 billing 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实 target 的 `billing` artifacts，因此不连接真实支付平台、客户账单、供应商或生产环境。

验证说明：本仓库是研发规范仓库，不包含真实产品 target 的 `billing` artifacts，也不应在规范阶段连接真实 Stripe、OpenAI billing、客户、发票、退款或生产 Webhook。已通过 `verify_billing_entitlements.py` 的临时 `assistant-app` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `billing/product-catalog`。
