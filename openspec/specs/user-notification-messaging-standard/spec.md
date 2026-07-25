# user-notification-messaging-standard 规格

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

Define the minimum one-person-company governance for user-facing outbound messages: email, SMS, push, web push, in-app notifications, templates, preferences, consent, unsubscribe, suppression, delivery events, provider failures, and AI-generated message drafts across Go/Kratos/sqlc/gRPC services, Vite surfaces, and AI workflows.

## Requirements

### Requirement: 生产 target 必须定义 messaging artifacts

Any production target that sends user-facing email, SMS, push, web push, in-app notifications, product inbox messages, support autoresponses, incident/security/billing/legal notices, AI result notifications, lifecycle messages, or marketing messages MUST define messaging artifacts.

#### Scenario: 新外发用户消息能力准备进入生产

- GIVEN 一个 target 会向用户或用户设备发送外发消息
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `messaging/channel-registry/<target>.json`
- AND 创建 `messaging/template-catalog/<target>.json`
- AND 创建 `messaging/preference-consent/<target>.json`
- AND 创建 `messaging/delivery-runbook/<target>.md`
- AND 创建 `messaging/messaging-review/<target>.md`

### Requirement: Channel registry 必须定义 channel、provider、sender identity、event webhook、suppression、rate limit 和人工 checkpoint

Channel registry MUST record target、owner、channels、providers、sender identities、event webhooks、suppression sources、rate limits、human checkpoint 和 review cadence.

#### Scenario: Reviewer 判断触达渠道

- GIVEN reviewer 打开 `messaging/channel-registry/<target>.json`
- WHEN 需要理解 email/SMS/push/in-app 触达边界
- THEN 每个 channel 包含 id、type、provider、purpose、message_classes、sender_identity、authentication、opt_in_required、opt_out_path、suppression_source、quiet_hours、rate_limit 和 status
- AND transactional 与 marketing/broadcast 能分离
- AND 新 provider、sender、SMS number、push app、bulk stream 或高量发送触发人工 checkpoint

### Requirement: Template catalog 必须定义模板、渲染、本地化、PII、测试、审批和人工 checkpoint

Template catalog MUST record target、owner、templates、rendering policy、localization policy、PII policy、test policy、approval policy、human checkpoint 和 status.

#### Scenario: 模板准备发送

- GIVEN template renderer 准备发送邮件、短信、push、in-app 或 AI draft
- WHEN 模板被渲染
- THEN 每个 template 包含 id、name、message_class、channels、trigger、audience、source_of_truth、variables、sensitive_data_allowed、unsubscribe_required、owner 和 status
- AND rendering test、missing variable test、redaction/sensitive test 和 fallback copy 覆盖该模板
- AND AI 生成外发文案只能作为 draft，安全/账单/事故/法律/营销/高影响消息需要人工 review

### Requirement: Preference/consent 必须定义偏好组、同意、退订、suppression、quiet hours、保留、审计、required controls 和人工 checkpoint

Preference/consent policy MUST record target、owner、preference groups、consent policy、unsubscribe policy、suppression policy、quiet hours policy、data retention、audit policy、required controls、human checkpoint 和 status.

#### Scenario: 发送前检查用户偏好和同意

- GIVEN 发送 worker 准备发送外发消息
- WHEN 执行发送前检查
- THEN required_controls 至少包含 explicit_opt_in_for_marketing、transactional_vs_marketing_classification、unsubscribe_link_for_commercial_email、one_click_unsubscribe_for_bulk_email、sms_stop_handling、bounce_complaint_suppression、preference_center、quiet_hours_for_sms_push、idempotency_key、rate_limit、delivery_event_webhook、redaction_policy 和 audit_log
- AND hard bounce、complaint、SMS STOP、invalid push token 和 unsubscribe 更新 suppression 或对应状态
- AND 必要事务/安全/账单通知不得夹带营销内容来绕过退订

### Requirement: Delivery runbook 必须定义分类、渲染校验、consent/suppression、发送重试、delivery events、bounce/complaint/opt-out、事故安全消息、provider failure 和关联工件

Delivery runbook MUST record scope、classify message、render/validate、consent/suppression check、send/retry、delivery events、bounce/complaint/opt-out、incident/security messaging、provider failure 和 linked artifacts.

#### Scenario: 消息发送、失败或退订事件发生

- GIVEN 外发消息被触发、provider 返回失败、webhook 送达事件到达或用户退订
- WHEN operator 读取 `messaging/delivery-runbook/<target>.md`
- THEN 能看到如何分类消息、渲染并扫描敏感字段、检查 consent/suppression/quiet hours/rate limit、幂等发送、记录 provider id、处理 bounce/complaint/opt-out、降级 provider failure
- AND provider failure 不得绕过用户退订、同意、suppression 或 quiet hours

### Requirement: Messaging review 必须复盘 recent changes、volume、deliverability、suppression/preferences、template quality、incident/security、AI-generated messages、cost/rate limits、risk 和 next one change

Messaging review MUST record recent changes、message volume、deliverability、suppression/preferences、template quality、incident/security messages、AI-generated messages、cost/rate limits、open risks 和 next one change.

#### Scenario: 周期性复查用户触达健康

- GIVEN target 新增 channel/provider/template/bulk message，或发生 bounce/complaint/退订异常、误发、重复发送、provider failure、事故通知、安全通知、账单通知、AI 结果通知异常
- WHEN 更新 `messaging/messaging-review/<target>.md`
- THEN 记录 message volume、deliverability、suppression/preferences、template quality、incident/security messages、AI-generated messages、cost/rate limits 和 open risks
- AND 每次只选择一个最高影响的 next one change

### Requirement: 高风险消息变更必须人工 checkpoint

New channels/providers/senders, marketing or high-impact notifications, sensitive content, transactional/marketing reclassification, consent/opt-out bypass, AI-generated external copy, high-volume sends, deliverability incidents, and provider failures MUST have human checkpoint coverage.

#### Scenario: 消息动作触发高风险条件

- GIVEN channel registry、template catalog、preference/consent、delivery runbook、messaging review 或 release 触发高风险条件
- WHEN 准备发送、重试、切换 provider、扩大 audience、修改模板、绕过退订或接受例外
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、阻塞、降级、回滚、补偿或专业审阅需求

### Requirement: Messaging artifacts 不得保存敏感消息内容

Messaging artifacts MUST NOT store production tokens, API keys, private keys, session cookies, database connection strings, provider credentials, SMS secrets, push credentials, full email/SMS/push body with personal data, raw prompts, raw responses, raw tool outputs, payment data, health/legal/financial/identity data, unredacted personal data, or customer-confidential payloads.

#### Scenario: 记录模板、送达、退订、投诉、事故或 AI draft 证据

- GIVEN 需要保存 message template evidence、delivery evidence、bounce/complaint evidence、unsubscribe event、incident message note、AI draft 或 provider failure
- WHEN 写入 `messaging/` artifacts
- THEN 使用 template id、template version、provider message id、recipient hash、redacted summary、request id、trace id、audit event id、controlled attachment reference 或 synthetic example
- AND 不保存生产 token、API key、private key、session cookie、数据库连接串、provider credentials、SMS secrets、push credentials、带个人数据的完整消息正文、原始 prompt/response/tool output、支付数据、健康/法律/金融/身份数据、未脱敏个人数据或客户机密 payload
