# 实现：外部副作用、billing 与消息

## 规范要求

<!-- rule-id: IMPL-EXTERNAL-SIDE-EFFECT-CONTROLS -->
- 每个外部副作用都须具备审计、重放保护与人工 checkpoint。

<!-- rule-id: IMPL-BILLING-ARTIFACT-PATHS -->
- billing 工件缺省位于 `billing/product-catalog/<target>.json`、`billing/entitlement-policy/<target>.md`、`billing/usage-metering/<target>.json` 与 `billing/reconciliation/<target>.json`。

<!-- rule-id: IMPL-MESSAGING-ARTIFACT-PATHS -->
- messaging 工件缺省位于 `messaging/channel-registry/<target>.json`、`messaging/template-catalog/<target>.json` 与 `messaging/preference-consent/<target>.json`。

<!-- rule-id: IMPL-DEVELOPER-SURFACE-CROSS-STAGE -->
- 发布 public/stable API、SDK、CLI 或示例时，须由技术设计、实现与发布项目共同承接；实现只生产其技术产物。

<!-- rule-id: IMPL-SERVER-ENTITLEMENT-CHECK -->
- entitlement 裁决须由服务端执行。

<!-- rule-id: IMPL-ENTITLEMENT-UI-DISPLAY-ONLY -->
- Vite 只能展示后端返回的权益和用量状态。

<!-- rule-id: IMPL-BILLABLE-EVENT-LOCAL-LEDGER -->
- billable event 须在业务完成的耐久边界写入本地账本。

<!-- rule-id: IMPL-BILLABLE-EVENT-ASYNC-SYNC -->
- 本地记账成功后，再异步同步支付平台。

<!-- rule-id: IMPL-WEBHOOK-SLOW-WORKER -->
- 入站 Webhook 的慢处理须进入 worker。

<!-- rule-id: IMPL-OUTBOX-DISPATCHER-DUTIES -->
- outbox dispatcher 须负责投递、有限重试与死信处理。

<!-- rule-id: IMPL-MESSAGE-CLASSIFY-BEFORE-SEND -->
- 通知发送前须先分类。

<!-- rule-id: IMPL-BILLING-LEDGER-APPEND-ONLY -->
- billing ledger 须为 append-only。

<!-- rule-id: IMPL-REPLAY-SELECTION-SAFETY -->
- 手工 replay 只允许处理失败或明确选择的 delivery，禁止重复处理已成功副作用。

<!-- rule-id: IMPL-MARKETING-TRANSACTIONAL-SEPARATION -->
- 营销消息与事务消息须分流。

<!-- rule-id: IMPL-SMS-PUSH-CONSENT -->
- SMS 或 push 缺省需要 opt-in 或平台授权。

<!-- rule-id: IMPL-AI-EXTERNAL-MESSAGE-DRAFT-ONLY -->
- AI 可以生成消息草稿或 event payload 草案，但不得自动发送或执行外部写入。

<!-- rule-id: IMPL-COMMERCIAL-MODEL-HUMAN-GATE -->
- 定价模型、套餐、价格、价值计量单位、超额策略、退款或补偿的发布或改变须交由人工判断。

<!-- rule-id: IMPL-OUTBOUND-SENSITIVE-DATA-HUMAN-GATE -->
- 出站事件会发送敏感数据、用户内容、AI 输出、支付或计费状态、跨租户信息任一项时，须交由人工判断。

<!-- rule-id: IMPL-MESSAGING-EXPANSION-HUMAN-GATE -->
- 新增 channel、provider、sender domain、SMS number、push app，或启用高量、事故、安全、账单、法律通知时，须交由人工判断。

<!-- rule-id: IMPL-EXTERNAL-EFFECT-IDEMPOTENCY-AUDIT -->
- 每个外部副作用须能追溯到 idempotency key 与 audit/ref。
