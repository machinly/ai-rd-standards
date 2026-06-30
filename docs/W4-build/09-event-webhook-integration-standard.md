# W4 Build 触发专项：事件驱动、Webhook 与外部系统集成治理规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及入站 webhook、出站事件、外部 provider、inbox/outbox、事件 catalog、验签、去重、重放、死信或集成 schema 演进时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/00-main.md`，由主入口判断是否触发本专项。

## 目标

一人公司的外部集成通常从“接一个 webhook”开始，最后变成最难排查的生产边界：第三方重复投递、乱序到达、签名过期、事件重放、双写不一致、出站事件丢失、订阅状态漂移、AI agent 误触发外部动作、用户不知道集成是否正常。本专项定义事件驱动、Webhook 与外部系统集成治理规范，让每个集成都能回答：有哪些事件，谁生产、谁消费，如何验签，如何去重，是否有顺序要求，如何快速 ack，如何入 inbox/outbox，如何重试和死信，如何安全重放，如何演进 schema，如何观察外部系统是否健康。

默认原则：Webhook 是不可信的外部输入，事件是长期契约。入站事件先验签、去重、持久化，再异步处理；出站事件先和业务状态同事务写入 outbox，再由 dispatcher 发送。任何会改变钱、权益、权限、用户数据、外部消息、AI 工具或生产配置的事件，都必须有幂等、审计、重放保护和人工 checkpoint。

## 核心依据

- 《人月神话》：事件系统不是银弹；当事件名、语义、顺序和所有权不清楚时，异步只会把复杂度藏起来。
- 小型项目管理：一人公司不能维护大型事件平台；先保留能防止重复副作用、双写不一致和上下文丢失的五个小工件。
- Enterprise Integration Patterns：事件、消息通道、幂等接收者、消息存储、消息历史、死信通道和竞争消费者提供外部集成的经典词汇。
- Designing Data-Intensive Applications：分布式系统默认要面对重试、重复、乱序、部分失败和最终一致；exactly-once 不能当作应用层副作用安全的替代品。
- CloudEvents：使用统一事件元数据，如 `id`、`source`、`type`、`subject`、`time`、`datacontenttype` 和 schema/data，降低跨系统事件歧义。
- Transactional Outbox：业务数据库写入和消息发布是双写风险；outbox 让业务状态与待发送事件在本地事务中一起持久化。
- Stripe Webhooks：Webhook 需要签名验证、处理重复事件、快速返回成功，并能处理自动重试和手工处理未送达事件。
- GitHub Webhooks：接收方应在处理前验证签名；delivery id 可用于排障和去重；平台提供查看和重投递能力但保留时间有限。
- OWASP API Security：Webhook endpoint 是外部 API，必须防伪造、重放、资源消耗、权限绕过、敏感数据泄漏和不安全第三方数据消费。
- Google SRE Handling Overload / Cascading Failures：事件风暴、webhook 重试和出站 fanout 会导致级联故障；需要背压、限流、快速 ack、队列、死信和降级。
- OpenTelemetry Messaging Semantic Conventions：生产、发送、接收、处理和结算消息应有统一 trace/metric/log 属性，方便跨供应商排障。

## 范围

适用对象：

- 入站 webhook：Stripe、GitHub、Linear、OpenAI/模型供应商、邮件/短信、支付、CRM、存储、身份、内容审核、第三方 SaaS。
- 出站 webhook / event / callback：通知客户系统、发送集成事件、发布内部事件、同步供应商状态、触发外部自动化。
- 内部事件：domain event、integration event、outbox/inbox、event replay、event-driven worker、event-to-tool workflow。
- Go/Kratos/gRPC 后端里的 webhook endpoint、signature verifier、event normalizer、inbox/outbox、dispatcher、consumer、dead letter、replay admin action。
- sqlc/PostgreSQL 表中的 inbound delivery、outbox event、consumer offset、processing attempt、delivery result、dead letter 和 schema version。
- Vite 前端里的集成连接状态、webhook 测试、重放确认、错误解释、第三方连接范围和事件日志。

不适用对象：

- 普通同步 gRPC/HTTP 请求；W2 管契约，W4 管异步 job。
- 只在本地开发中模拟的 webhook，且不访问真实数据、不调用真实供应商、不写生产。
- 企业级事件总线、Kafka 平台、复杂流处理、跨区域 exactly-once 语义、全量 CDC 平台；需要时单独开架构 change。

## 最小工件

每个生产集成或事件边界使用同一个 `<target>` 文件名：

```text
integrations/
  event-catalog/<target>.json
  webhook-contract/<target>.json
  delivery-runbook/<target>.md
  integration-test-plan/<target>.json
  integration-review/<target>.md
```

### `integrations/event-catalog/<target>.json`

Event catalog 必须包含：

- `target`
- `owner`
- `providers`
- `event_types`
- `producers`
- `consumers`
- `storage`
- `delivery_semantics`
- `schema_policy`
- `telemetry`
- `human_checkpoint`
- `review_cadence`

`event_types` 每项至少包含：

- `id`
- `name`
- `direction`
- `source`
- `destination`
- `schema_ref`
- `version`
- `stability`
- `subject`
- `event_id_key`
- `ordering_key`
- `delivery_semantics`
- `idempotency_key`
- `replay_policy`
- `data_classification`
- `status`

默认：

- 事件名必须是业务事实，不是命令愿望；例如 `subscription.updated` 优于 `syncSubscriptionNow`。
- 入站事件默认 at-least-once、可能重复、可能乱序；应用必须自己去重和处理乱序。
- 出站事件默认至少一次发送；消费者必须幂等，发送方必须有 outbox 和投递记录。
- `stable` 事件必须有 schema、兼容性策略、测试和消费者列表。
- 事件 payload 默认最小化，不发送 secret、token、完整 raw prompt/response/tool output 或不必要个人数据。

### `integrations/webhook-contract/<target>.json`

Webhook contract 必须包含：

- `target`
- `owner`
- `endpoints`
- `signature_verification`
- `timestamp_tolerance_seconds`
- `idempotency`
- `ordering`
- `ack_policy`
- `inbox_outbox`
- `retry_policy`
- `dead_letter_policy`
- `replay_policy`
- `payload_policy`
- `secret_rotation`
- `human_checkpoint`
- `status`

`endpoints` 每项至少包含：

- `id`
- `path`
- `direction`
- `provider`
- `event_types`
- `method`
- `signature_header`
- `delivery_id_header`
- `timestamp_header`
- `ack_timeout_seconds`
- `status`

默认：

- 入站 webhook 必须在解析业务 payload 前验证签名；需要 raw body 的 provider 必须保留 raw body 给 verifier，但不持久化完整 raw body。
- 必须校验 timestamp 或等价新鲜度，防 replay；没有 timestamp 的 provider 必须用 delivery id、短期 nonce cache 或更严格 endpoint 隔离补偿。
- Handler 必须快速 ack：验证、去重、持久化 inbox 后返回；慢处理进入 `async-jobs/`。
- 不依赖事件顺序；若业务需要顺序，必须定义 ordering key、version guard 或从 provider 拉取最新对象状态。
- 手工 replay 只处理未完成、失败或明确 selected delivery；不得重复处理已成功副作用。

### `integrations/delivery-runbook/<target>.md`

Delivery runbook 必须包含：

- `Scope`
- `Provider Setup`
- `Signature Verification`
- `Receive / Ack`
- `Inbox / Outbox`
- `Processing`
- `Idempotency / Ordering`
- `Retry / Replay`
- `Dead Letter`
- `Observability`
- `Secret Rotation`
- `Incident Actions`
- `Linked Artifacts`

默认执行顺序：

1. 入站：接收请求，校验 method、path、provider、签名、timestamp、大小和 content type。
2. 用 provider delivery id、event id、object id + event type 或内部 dedupe key 做去重。
3. 持久化 inbox 记录：provider、event type、schema version、delivery id、event id、received_at、signature result、status、redacted payload hash。
4. 快速 ack，然后通过 worker 处理业务状态。
5. 出站：业务状态与 outbox event 同事务写入；dispatcher 负责发送、重试、记录结果和死信。
6. 失败：按错误分类处理，可重试错误退避，不可重试错误死信；重放必须带影响摘要和幂等检查。

### `integrations/integration-test-plan/<target>.json`

Integration test plan 必须包含：

- `target`
- `owner`
- `environments`
- `cases`
- `required_checks`
- `evidence_refs`
- `human_checkpoint`
- `status`

`required_checks` 默认至少覆盖：

- `signature_verification`
- `timestamp_replay_protection`
- `delivery_id_dedupe`
- `idempotent_consumer`
- `schema_validation`
- `fast_ack`
- `inbox_persistence`
- `outbox_transaction`
- `retry_backoff`
- `dead_letter`
- `manual_replay_guard`
- `ordering_or_version_guard`
- `secret_rotation`
- `payload_redaction`
- `provider_status_degradation`
- `telemetry`

默认：

- 每个入站 webhook 覆盖签名失败、timestamp 过期、重复 delivery、乱序/旧版本、provider 重试、payload schema 错误和快速 ack。
- 每个出站 event 覆盖 outbox 同事务、发送失败、重复发送、消费者幂等、dead letter 和 replay。
- 会影响钱、权益、权限、用户数据、外部消息、AI 工具或生产配置的事件必须覆盖副作用幂等和审计。

### `integrations/integration-review/<target>.md`

Integration review 必须包含：

- `Recent Changes`
- `Deliveries / Failures`
- `Duplicates / Replays`
- `Signature / Auth Drift`
- `Schema / Contract Changes`
- `Inbox / Outbox Health`
- `Cost / Rate Limits`
- `User / Business Impact`
- `Incidents`
- `Open Risks`
- `Next One Change`

默认：

- pre-revenue 或低流量：每月复盘一次，或新增 provider/webhook/event type 前复盘。
- 有活跃用户：每两周复盘一次，或 webhook 失败、重复投递、死信、签名密钥轮换、schema 变化、外部供应商事件事故后复盘。
- 每次只选一个最高影响改进：补验签、补去重、改快速 ack、加 outbox、补死信、收紧 payload、加 replay guard、补 dashboard 或下线无用事件。

## Go / Kratos / sqlc / gRPC 默认规则

- 外部 webhook endpoint 只作为接入层；业务处理必须通过 Go/Kratos usecase、inbox/outbox 和 worker。
- 入站验签必须使用 raw body；验证前不做 JSON 解析，不把未验证 payload 写入业务表。
- gRPC 内部事件 API 使用 Protobuf 定义事件 schema；若与外部系统互通，事件 envelope 可映射 CloudEvents 字段。
- sqlc 默认表可包含：`integration_providers`、`event_catalog`、`inbound_webhook_deliveries`、`inbox_events`、`outbox_events`、`event_processing_attempts`、`event_delivery_attempts`、`event_dead_letters`、`webhook_secrets`、`event_replay_requests`。
- 入站 `provider_event_id`、`delivery_id`、`dedupe_key` 必须有唯一约束或等价去重；出站 outbox event 必须有状态、attempt、next_attempt_at、last_error_class。
- 出站事件和业务状态改变必须同事务写入本地数据库；不得在数据库事务中直接调用第三方 webhook。
- Webhook secret 通过配置/secret manager 注入，支持 rotation window；不进入日志、事件 payload、前端或 OpenSpec 工件。
- 所有 handler 设置 request size limit、timeout、rate limit、provider allowlist 或等价边界。

## Vite 前端默认规则

- 集成设置页显示 provider、连接状态、最近 delivery、错误类别、重试/重放状态、密钥轮换状态和数据范围。
- 重放、禁用集成、扩大事件范围、重新发送出站事件必须有明确确认和影响摘要。
- 不显示 webhook secret、签名密钥、完整 raw payload、完整个人数据、支付敏感数据或完整 AI prompt/response。
- 对用户可见集成异常提供短文案：同步延迟、等待重试、需要重新授权、供应商不可用、部分事件失败或已暂停。
- UI 保持 Vercel/Geist 风格：状态密集但清晰，危险动作按钮少而明确，不用装饰掩盖风险。

## AI workflow 默认规则

- AI agent 不得直接相信 webhook payload 或外部事件文本；它们是工具输出/外部输入，必须通过 schema、权限和信任边界。
- 由事件触发 AI workflow 时，必须连接 W3 tool runtime 和 W4 async job；事件只触发登记过的 job 或工具。
- 外部事件中的自由文本、HTML、Markdown、URL、文件名、评论、issue 内容、support message 不得进入高优先级 prompt 指令。
- AI 生成的出站事件或 webhook payload 必须经过结构化 schema、业务校验、权限检查和 human checkpoint，才能产生外部副作用。
- 事件 replay 不得自动重新运行高成本 AI job 或高权限工具，除非有幂等、预算和审批。

## 需要人判断的关键点

只把这些判断交给人：

- 是否新增外部 provider、公开 webhook endpoint、出站 webhook、事件总线、event broker 或客户可订阅事件。
- 是否允许入站事件改变钱、权益、权限、用户数据、外部消息、生产配置或触发 AI 工具/后台任务。
- 是否允许出站事件发送敏感数据、用户内容、AI 输出、支付/计费状态或跨租户信息给第三方。
- 是否接受没有签名验证、timestamp/replay 防护、去重、inbox/outbox、dead letter、快速 ack 或 replay guard 的集成。
- 是否手工 replay、删除 dead letter、补发出站事件、重放历史事件或从 provider 拉取历史事件回填。
- 是否进行 breaking event schema change、删除事件类型、改变事件语义、改变 ordering/idempotency key 或扩大 payload。
- 是否轮换 webhook secret、处理签名失败尖峰、供应商事故、重复副作用或集成数据泄漏。

其他字段完整性、章节、JSON 枚举、测试覆盖、敏感内容扫描、OpenSpec linkage、positive/negative fixture 和基础验证由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“有哪些事件、Webhook 契约是什么、怎么收发、怎么测、怎么复盘”。
- 保留：人只判断新 provider/endpoint、钱/权限/数据/外部消息副作用、敏感出站数据、缺失验签/去重/outbox/dead letter、重放和 schema 破坏。
- 调整：不默认引入 Kafka、云事件总线或事件平台；先用 Postgres inbox/outbox + worker 落地。
- 调整：不要求所有内部事件 CloudEvents 化；只要求跨系统事件有稳定 envelope 和字段映射。
- 风险：集成容易散落到各业务服务。缓解：event catalog 和 webhook contract 成为唯一入口，verifier 检查每个 target 的最低边界。

结论：可落地。一个人可以先为最危险的 provider（通常是支付、身份或代码托管）写五个工件，把验签、去重、inbox/outbox 和重放保护做实。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户能看到集成是否延迟、失败、暂停或需要重新授权，不再把外部系统问题误认为产品坏了。
- 工程角度：Go/Kratos/sqlc/gRPC 有清晰 webhook 接入、事件 schema、inbox/outbox、唯一约束和处理 attempt 路径。
- 运维角度：快速 ack、死信、重放、provider status、delivery failure 和 dashboard 指标能支撑事故响应。
- 安全隐私角度：签名、timestamp、防重放、payload 最小化、secret rotation 和敏感数据出站 checkpoint 明确。
- 成本角度：事件风暴、重复投递、出站 fanout 和 AI replay 都有 rate limit、dead letter 和人工确认。

结论：可落地。本专项把“外部系统通知我一下”压成可审查的集成契约：先信任边界，再状态落库，再异步处理，最后可重放、可排障、可演进。
