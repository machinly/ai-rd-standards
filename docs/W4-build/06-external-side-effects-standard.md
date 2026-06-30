# W4 触发专项：计费、Webhook、事件与用户通知外部副作用规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及收费/权益/用量、支付 Webhook、入站/出站事件、外部 provider、通知、邮件/SMS/push、退订、送达事件或对外 API/开发者示例副作用时，才读取本文件。

普通 W4 实现先回到 `docs/W4-build/00-main.md`。

## 目标

把计费、Webhook/事件和用户通知合并成一个外部副作用门禁：系统什么时候会改变钱、权益、第三方状态或用户触达，如何保证幂等、验签、审计、重试、退订、对账和回滚。

默认原则：外部副作用不是日志。任何会影响钱、权限、客户系统、用户设备、邮件/SMS/push、AI 工具或公开集成都必须有幂等、审计、重放保护和人工 checkpoint。

## 主要角色消费者

- 后端：实现账本、inbox/outbox、notification service、provider client。
- 运维：处理 replay、dead letter、delivery failure、对账和事故。
- 产品/运营：确认收费口径、模板、同意、退订和客户沟通。

## 最小工件

按触发选择：

```text
billing/
  product-catalog/<target>.json
  entitlement-policy/<target>.md
  usage-metering/<target>.json
  reconciliation/<target>.json

integrations/
  event-catalog/<target>.json
  webhook-contract/<target>.json
  delivery-runbook/<target>.md
  integration-test-plan/<target>.json

messaging/
  channel-registry/<target>.json
  template-catalog/<target>.json
  preference-consent/<target>.json
  delivery-runbook/<target>.md
```

开发者 API/SDK/docs 若只是说明文档，降级到 W4 主入口和 W9 知识恢复；若会发布 public/stable API、SDK、CLI 或示例，则由 W2 API 契约、W4 本专项和 W6 对外声明共同承接。

## 必须覆盖

- 服务端执行权益检查；Vite 只能展示后端权益和用量状态。
- billable event 在业务完成的耐久边界写入本地账本，再异步同步支付平台。
- Webhook 入站先验签、去重、持久化 inbox，再快速 ack，慢处理进 worker。
- 出站事件与业务状态同事务写 outbox；dispatcher 负责投递、重试、死信。
- 通知先分类，再检查 preference、consent、suppression、quiet hours、rate limit、idempotency。
- 邮件/SMS/push 不包含 secret、完整 AI 输出、完整用户输入、支付/健康/法律/金融/身份敏感数据。

## 默认规则

- 账本 append-only；修正使用 compensating event、credit 或 adjustment。
- Webhook 不依赖顺序；不确定时拉取 provider 当前对象状态。
- 手工 replay 只处理失败或明确 selected delivery，不重复处理已成功副作用。
- 营销和事务消息分流；商业邮件有退订，SMS/push 默认需要 opt-in 或平台授权。
- AI 可生成消息草稿或事件 payload 草案，但不得自动发送或执行外部写入。

## 需要人判断

- 发布或改变 pricing model、套餐、价格、价值计量单位、超额策略、退款或补偿。
- 生产 Webhook replay、批量补账、批量撤权、批量 credit、真实退款或重复副作用处理。
- 新外部 provider、公开 webhook endpoint、出站 webhook、客户可订阅事件或 breaking event schema change。
- 出站事件发送敏感数据、用户内容、AI 输出、支付/计费状态或跨租户信息。
- 新 channel/provider/sender domain/SMS number/push app、高量发送、事故/安全/账单/法律通知。
- 绕过退订、suppression、hard bounce、complaint、quiet hours、rate limit 或 consent。

## Review A：一人可执行性

合并后，所有外部副作用共享同一个 W4 入口，角色 Agent 不需要分别读三份重复的幂等、重试、审计和供应商边界文档。每次按触发只补对应工件。

## Review B：产品 / 工程 / 运维风险

保留了钱、权限、外部系统、通知和开发者依赖的硬门禁。最小安全下一步是任何外部副作用都能追到 event id、idempotency key、audit/ref 和回放/撤销策略。

