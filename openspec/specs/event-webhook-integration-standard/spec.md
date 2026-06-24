# event-webhook-integration-standard 规格

## Purpose

Define the minimum one-person-company governance for inbound webhooks, outbound events, external integrations, event catalogs, signature verification, replay protection, inbox/outbox, delivery attempts, dead letters, schema evolution, and safe event-triggered AI/tool/job workflows.

## Requirements

### Requirement: 生产事件/Webhook 集成必须定义 integrations artifacts

Any production integration boundary that receives webhooks, sends outbound events, consumes third-party events, publishes internal integration events, replays deliveries, or triggers AI/tools/jobs from external events MUST define integration artifacts.

#### Scenario: 新外部集成准备进入生产

- GIVEN 一个 target 会接收入站 webhook、发送出站 webhook、发布/消费事件、处理第三方 delivery、重放事件或触发 AI/tool/job
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `integrations/event-catalog/<target>.json`
- AND 创建 `integrations/webhook-contract/<target>.json`
- AND 创建 `integrations/delivery-runbook/<target>.md`
- AND 创建 `integrations/integration-test-plan/<target>.json`
- AND 创建 `integrations/integration-review/<target>.md`

### Requirement: Event catalog 必须定义 provider、event type、producer、consumer、storage、delivery、schema、telemetry 和人工 checkpoint

Event catalog MUST record target、owner、providers、event types、producers、consumers、storage、delivery semantics、schema policy、telemetry、human checkpoint 和 review cadence.

#### Scenario: Reviewer 判断事件边界

- GIVEN reviewer 打开 `integrations/event-catalog/<target>.json`
- WHEN 需要理解集成事件
- THEN 每个 event type 包含 id、name、direction、source、destination、schema_ref、version、stability、subject、event_id_key、ordering_key、delivery_semantics、idempotency_key、replay_policy、data_classification 和 status
- AND `stable` 事件有 schema、消费者和兼容性策略
- AND 入站事件默认被视为 at-least-once、可能重复、可能乱序

### Requirement: Webhook contract 必须定义 endpoint、验签、timestamp、幂等、顺序、ack、inbox/outbox、retry、dead letter、replay、payload、secret rotation 和人工 checkpoint

Webhook contract MUST record target、owner、endpoints、signature verification、timestamp tolerance、idempotency、ordering、ack policy、inbox/outbox、retry policy、dead letter policy、replay policy、payload policy、secret rotation、human checkpoint 和 status.

#### Scenario: 入站 webhook 被接收

- GIVEN 外部 provider 调用 webhook endpoint
- WHEN handler 接收请求
- THEN 在业务解析前验证 method、path、raw-body signature、timestamp、content type 和大小限制
- AND 使用 provider delivery id、event id、object id + event type 或内部 dedupe key 去重
- AND 持久化 inbox 后快速 ack
- AND 慢处理进入 async job 或 worker

### Requirement: Delivery runbook 必须定义 provider setup、signature verification、receive/ack、inbox/outbox、processing、idempotency、retry、dead letter、observability、secret rotation 和 incident actions

Delivery runbook MUST record scope、provider setup、signature verification、receive/ack、inbox/outbox、processing、idempotency/ordering、retry/replay、dead letter、observability、secret rotation、incident actions 和 linked artifacts.

#### Scenario: 集成失败、重复投递或需要重放

- GIVEN operator 需要处理 webhook 失败、重复投递、死信或出站发送失败
- WHEN 读取 `integrations/delivery-runbook/<target>.md`
- THEN 能看到如何验证 provider、如何查 inbox/outbox、如何识别重复、如何安全重试、何时进入 dead letter、如何带影响摘要重放
- AND secret rotation 和 incident actions 不暴露 secret 或完整 raw payload

### Requirement: Integration test plan 必须覆盖验签、timestamp/replay、防重复、幂等消费者、schema、快速 ack、inbox、outbox、retry、dead letter、manual replay、ordering/version、secret rotation、payload redaction、provider degradation 和 telemetry

Integration test plan MUST record target、owner、environments、cases、required checks、evidence refs、human checkpoint 和 status.

#### Scenario: 发布前验证集成

- GIVEN 集成准备发布
- WHEN 读取 `integrations/integration-test-plan/<target>.json`
- THEN `required_checks` 至少包含 `signature_verification`、`timestamp_replay_protection`、`delivery_id_dedupe`、`idempotent_consumer`、`schema_validation`、`fast_ack`、`inbox_persistence`、`outbox_transaction`、`retry_backoff`、`dead_letter`、`manual_replay_guard`、`ordering_or_version_guard`、`secret_rotation`、`payload_redaction`、`provider_status_degradation` 和 `telemetry`
- AND cases 覆盖每个 required check
- AND 有副作用事件覆盖幂等、审计和重放保护

### Requirement: Integration review 必须复盘 delivery、failure、duplicate、replay、signature/auth drift、schema change、inbox/outbox health、cost、user impact、incident 和下一项改进

Integration review MUST record recent changes、deliveries/failures、duplicates/replays、signature/auth drift、schema/contract changes、inbox/outbox health、cost/rate limits、user/business impact、incidents、open risks 和 next one change.

#### Scenario: 周期性复查集成健康

- GIVEN target 有近期 provider、webhook、event type、schema、secret、replay、worker、AI/tool trigger 或用户影响变更
- WHEN 更新 `integrations/integration-review/<target>.md`
- THEN 记录 delivery/failure、duplicate/replay、signature/auth drift、schema/contract changes、inbox/outbox health、成本/限流、用户/业务影响、事故和开放风险
- AND 只选择一个最高影响的 next one change

### Requirement: 高风险事件/Webhook 变更必须人工 checkpoint

New providers/endpoints/outbound webhooks/brokers/customer events, inbound events that change money/rights/data/messages/tools/jobs/config, outbound sensitive data, missing verification/replay/dedupe/inbox/outbox/dead-letter/replay-guard, manual replay/delete/backfill, breaking event schema changes, and secret/incident actions MUST have human checkpoint coverage.

#### Scenario: 集成触发高风险条件

- GIVEN event catalog、webhook contract、runbook、test plan、review 或 release 触发高风险条件
- WHEN 准备发布或接受例外
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、阻塞、降级或补偿动作

### Requirement: Integration artifacts 不得保存敏感内容

Integration artifacts MUST NOT store secrets, webhook signing secrets, production tokens, API keys, OAuth refresh tokens, private keys, session cookies, database connection strings, payment data, raw webhook bodies, raw prompts, raw responses, raw tool outputs, unredacted personal data, provider raw payloads, or executable attack payloads.

#### Scenario: 记录 delivery、payload、死信、重放或事故证据

- GIVEN 需要保存 webhook delivery、payload example、dead-letter note、replay evidence、provider error 或 incident evidence
- WHEN 写入 `integrations/` artifacts
- THEN 使用 synthetic example、redacted summary、delivery id、event id、trace id、payload hash、artifact id、finding id 或 controlled attachment reference
- AND 不保存 secret、webhook signing secret、生产 token、API key、OAuth refresh token、私钥、session cookie、数据库连接串、支付数据、完整 raw webhook body、raw prompt/response/tool output、未脱敏个人数据、provider raw payload 或可直接执行的攻击 payload
