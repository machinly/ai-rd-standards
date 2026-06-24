# W4 Build 触发专项：用户通知、邮件/SMS/Push 与触达治理规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及邮件、SMS、push、in-app 通知、模板、偏好/同意、退订、bounce/complaint、送达事件、事故/账单/安全通知或 AI 辅助文案时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/main.md`，由主入口判断是否触发本专项。

## 目标

一人公司的 AI 产品很快会需要给用户发消息：注册验证、密码重置、账单失败、AI 任务完成、安全告警、事故更新、产品变更、营销邮件、短信提醒、浏览器 push。问题在于，通知系统一旦失控，会直接伤害信任：误发敏感内容、营销和事务消息混发、退订无效、短信缺少同意、邮件进垃圾箱、AI 自动生成不当文案、事故通知口径不一致、重试风暴刷屏用户。本专项定义用户通知、邮件/SMS/Push 与触达治理规范，让每个生产 target 能回答：哪些 channel 可用，哪些消息可以发，模板在哪里，谁同意了，如何退订，如何限流，如何处理 bounce/complaint，何时人工判断。

默认原则：用户触达是产品行为，不是日志输出。每条外发消息都要有合法/合约/产品目的、触发条件、偏好/同意边界、模板版本、送达证据、退订路径和失败处理。

## 核心依据

- 《人月神话》：触达系统的复杂度来自概念边界不清；事务、安全、营销、支持、事故和 AI 自动消息混在一起会制造长期维护成本。
- 小型项目管理：一人公司不能维护大型营销自动化平台；先保留 channel registry、template catalog、preference/consent、delivery runbook、messaging review 五个可执行工件。
- FTC CAN-SPAM：商业邮件需要真实 header/subject、识别广告、包含地址、提供退订并及时处理；事务/关系消息也不能使用误导性路由信息。
- FCC TCPA / robotext guidance：自动短信通常需要事先同意，退订请求必须可被识别和执行；短信是高风险触达渠道。
- Gmail sender guidelines / RFC 8058：批量商业邮件需要身份认证、低投诉率、清晰退订和 one-click unsubscribe 机制。
- Amazon SES / deliverability：bounce、complaint、delivery、rendering failure 等送达事件应被监控；硬退信和投诉要进入 suppression，保护发信声誉。
- Twilio SMS guidance：短信营销是 permission-based，必须清晰 opt-in、确认、退订和 help 说明。
- Firebase Cloud Messaging / W3C Push API / APNs：push 需要用户授权、设备 token、速率/配额、失败处理和平台约束；不能把 push 当可靠事务日志。
- Google SRE Incident Response / Atlassian incident communication：用户影响事件需要单一事实来源、及时更新、准确口径和行动项。
- Vercel Geist：通知偏好和消息状态 UI 应清晰、克制、可扫描，不用暗色小字隐藏退订或风险信息。

## 范围

适用对象：

- 邮件、SMS、push、web push、in-app notification、产品内 inbox、chat/Slack/Discord 集成消息、support autoresponse、incident/security/billing/legal/product update 通知。
- Go/Kratos/sqlc/gRPC 后端中的 notification service、template renderer、message queue、delivery worker、provider webhook、suppression/preference tables。
- Vite 前端中的通知中心、偏好设置、退订页面、消息预览、送达状态、in-app banner、push permission UI。
- AI 自动生成或辅助生成的邮件、短信、push、事故更新、支持回复、营销文案、产品公告。

不适用对象：

- W8 客户支持专项的人工支持队列和回复流程；本专项关注系统或工作流触发的外发消息。
- W4 事件/Webhook 专项的外部系统 webhook；本专项关注发给用户或用户设备的通知。
- 正式法律意见、区域营销合规判断、跨国短信法规审查；这些需要专业审阅或单独 change。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
messaging/
  channel-registry/<target>.json
  template-catalog/<target>.json
  preference-consent/<target>.json
  delivery-runbook/<target>.md
  messaging-review/<target>.md
```

### `messaging/channel-registry/<target>.json`

Channel registry 必须包含：

- `target`
- `owner`
- `channels`
- `providers`
- `sender_identities`
- `event_webhooks`
- `suppression_sources`
- `rate_limits`
- `human_checkpoint`
- `review_cadence`

`channels` 每项至少包含：

- `id`
- `type`
- `provider`
- `purpose`
- `message_classes`
- `sender_identity`
- `authentication`
- `opt_in_required`
- `opt_out_path`
- `suppression_source`
- `quiet_hours`
- `rate_limit`
- `status`

默认：

- 邮件至少区分 transactional 与 broadcast/marketing；不要用营销流量污染事务发信声誉。
- SMS、push、web push 默认需要显式 opt-in 或平台授权；不要把填写手机号等同于短信营销同意。
- 安全、账单、事故、法律/政策更新属于高重要性，但仍要避免敏感内容和刷屏。
- 新 provider、sender domain、SMS number、push app id、bulk stream 或高量发送前必须人工 checkpoint。

### `messaging/template-catalog/<target>.json`

Template catalog 必须包含：

- `target`
- `owner`
- `templates`
- `rendering_policy`
- `localization_policy`
- `pii_policy`
- `test_policy`
- `approval_policy`
- `human_checkpoint`
- `status`

`templates` 每项至少包含：

- `id`
- `name`
- `message_class`
- `channels`
- `trigger`
- `audience`
- `source_of_truth`
- `variables`
- `sensitive_data_allowed`
- `unsubscribe_required`
- `owner`
- `status`

默认：

- 模板进入版本控制或 provider template id 有对应 source-of-truth；不得只存在控制台。
- 变量默认只允许最小必要字段，不放 secret、token、完整 AI 输出、完整用户输入、支付信息、敏感个人数据。
- AI 生成文案只能作为 draft；安全、账单、事故、法律、退款、营销和高影响通知必须人工 review。
- 每个模板至少有 rendering test、missing variable test、redaction/sensitive test 和 fallback copy。

### `messaging/preference-consent/<target>.json`

Preference/consent 必须包含：

- `target`
- `owner`
- `preference_groups`
- `consent_policy`
- `unsubscribe_policy`
- `suppression_policy`
- `quiet_hours_policy`
- `data_retention`
- `audit_policy`
- `required_controls`
- `human_checkpoint`
- `status`

`required_controls` 默认至少包含：

- `explicit_opt_in_for_marketing`
- `transactional_vs_marketing_classification`
- `unsubscribe_link_for_commercial_email`
- `one_click_unsubscribe_for_bulk_email`
- `sms_stop_handling`
- `bounce_complaint_suppression`
- `preference_center`
- `quiet_hours_for_sms_push`
- `idempotency_key`
- `rate_limit`
- `delivery_event_webhook`
- `redaction_policy`
- `audit_log`

默认：

- 退订不能阻止必要的安全、账单、账号、法律或事务通知，但这类通知不得夹带营销内容。
- 商业/营销邮件必须有退订入口；批量邮件按 provider 要求支持 one-click unsubscribe。
- SMS opt-out、email complaint、hard bounce、push token invalid 都要进入 suppression 或对应状态。
- 用户偏好、同意、退订、suppression、送达事件都要有审计或事件记录。

### `messaging/delivery-runbook/<target>.md`

Delivery runbook 必须包含：

- `Scope`
- `Classify Message`
- `Render / Validate`
- `Consent / Suppression Check`
- `Send / Retry`
- `Delivery Events`
- `Bounce / Complaint / Opt-Out`
- `Incident / Security Messaging`
- `Provider Failure`
- `Linked Artifacts`

默认执行顺序：

1. 先分类：transactional、security、billing、incident、ai_result、product_update、marketing、support、legal_policy。
2. 检查 preference、consent、suppression、quiet hours、rate limit、tenant/user scope、idempotency key。
3. 渲染模板并做敏感字段扫描；失败则不发送，进入 dead letter 或人工 review。
4. 发送后记录 provider message id、template version、recipient hash、channel、status、request id、trace id。
5. 接收 delivery/bounce/complaint/unsubscribe/webhook 事件，更新 suppression 和 delivery ledger。
6. provider 失败时降级、重试或切换渠道，但不得绕过退订/同意。

### `messaging/messaging-review/<target>.md`

Messaging review 必须包含：

- `Recent Changes`
- `Message Volume`
- `Deliverability`
- `Suppression / Preferences`
- `Template Quality`
- `Incident / Security Messages`
- `AI-Generated Messages`
- `Cost / Rate Limits`
- `Open Risks`
- `Next One Change`

默认节奏：

- pre-revenue：每月一次，或新增 channel/provider/template/bulk message 前。
- 有付费用户：每两周一次，或 bounce/complaint/退订异常、事故通知、安全通知、账单通知、AI 结果通知异常后。
- 每次只选一个最高影响改进：补退订、分离 message stream、补 bounce 处理、收紧 SMS、补模板测试、减少噪音、加送达 webhook。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端默认用 Go/Kratos notification service 统一发消息，不让业务代码直接调用邮件/SMS/push provider。
- gRPC API 默认包含 message class、recipient scope、tenant、template id/version、idempotency key、request id、trace id、dry-run/commit。
- sqlc 表默认包含：`message_templates`、`message_preferences`、`message_consents`、`message_suppressions`、`message_deliveries`、`message_events`、`message_provider_failures`。
- provider webhook 进入 W4 事件/Webhook 专项治理；delivery worker 进入 W4 异步任务专项；敏感审计进入 W9 审计证据专项。
- 发送动作默认幂等；重复事件不得导致重复扣费、重复安全警报或重复营销触达。

## Vite 前端默认规则

- 通知偏好中心必须清楚区分 security/billing/account 必要通知、product updates、marketing、AI result、support updates。
- 退订页面和 one-click unsubscribe endpoint 不要求登录即可处理 opaque token，但不能泄露用户身份。
- Push permission UI 只能在用户动作后请求授权；不得进入页面立即弹系统 permission。
- 消息预览、模板测试和发送确认使用 Vercel/Geist 风格：状态清楚、危险动作明确、退订和偏好入口可见。

## AI workflow 默认规则

- AI 不得自动发送外部消息；最多生成 draft、摘要、候选 subject/body 和风险说明。
- AI 生成的营销、安全、事故、账单、退款、法律/政策、权限、医疗/法律/金融等高影响消息必须人工 checkpoint。
- AI 结果通知默认只发送“结果已准备好/需要查看”，不在邮件/SMS/push 中包含完整敏感输出。
- AI 发送建议必须连接 eval、template tests、redaction policy、rate limits 和 human approval。

## 需要人判断的关键点

只把这些判断交给人：

- 是否新增 channel、provider、sender domain、SMS number、push app、bulk stream 或高量发送。
- 是否发送营销、生命周期、产品公告、法律/政策、安全事故、账单失败、退款、权限变化或高影响通知。
- 是否把消息分类从 transactional 改成 marketing，或反过来绕过退订。
- 是否在 email/SMS/push 中包含敏感数据、AI 输出、用户内容、支付/健康/法律/金融/身份数据。
- 是否绕过退订、suppression、hard bounce、complaint、quiet hours、rate limit 或 consent。
- 是否使用 AI 生成文案直接对外发送。
- 是否在 provider 失败、投诉飙升、退订异常、误发、重复发送或 deliverability 下降时继续发送。

其他字段完整性、章节、JSON 枚举、required_controls、敏感内容扫描、positive/negative fixture 和 OpenSpec linkage 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“有哪些渠道、有哪些模板、谁同意了、怎么送达失败处理、怎么复盘”。
- 保留：人只判断新增高风险 channel/provider、营销/事故/安全/账单/法律通知、敏感内容、绕过退订、AI 直接发送和送达异常继续发送。
- 调整：不默认上营销自动化平台；先用 provider + 后端 notification service + 明确偏好/suppression。
- 调整：邮件、SMS、push 统一治理，但 verifier 只检查最小字段，不要求所有 channel 都启用。
- 风险：通知容易变成用户噪音。缓解：rate limit、quiet hours、preference center 和 messaging review 每次只改一个最高影响问题。

结论：可落地。一个人可以先为注册、密码重置、账单、安全和 AI 结果通知写五个文件，再决定是否开启营销触达。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户能管理偏好，重要通知不夹带营销，低价值触达不会吞掉信任。
- 工程角度：Go/Kratos notification service、sqlc delivery/preference/suppression 表和 gRPC idempotency 让发送链路可控。
- 运维角度：bounce/complaint/provider failure、delivery webhook、dead letter、rate limit 和 incident messaging 有 runbook。
- 安全隐私角度：敏感内容、AI 输出、支付/身份/健康/法律/金融信息默认不进外部 channel；退订和 consent 有审计。
- 成本角度：SMS/push/email 高量发送有 rate limit、cost review 和 provider failure 降级，不让重试风暴烧钱。

结论：可落地。本专项把“给用户发一条消息”变成可审查的产品动作：分类、同意、模板、发送、送达、退订、复盘都留有最小控制。
