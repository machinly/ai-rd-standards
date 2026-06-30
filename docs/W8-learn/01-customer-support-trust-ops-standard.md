# W8 Learn 触发专项：客户支持、反馈分流与信任运营规范

## W8 触发定位

本文件是 W8 Learn 的触发型专项，不是 W8 主入口。只有当当前工作涉及支持队列、用户反馈、回复模板、反馈账本、事故沟通、退款/权益/隐私安全请求或 top contact drivers 时，才需要读取本文件。

普通 W8 学习入口应先回到 `docs/W8-learn/00-main.md`，由主入口判断是否触发本专项。

## 目标

一人公司上线 AI 产品后，支持消息会同时包含 bug、用法困惑、计费权益、AI 输出投诉、安全隐私请求、事故反馈和流失信号。如果这些都停留在聊天记录里，研发会被动救火，产品学习也会丢失。本专项定义客户支持、反馈分流与信任运营规范，把支持队列变成可恢复用户、可保护信任、可反哺研发的最小闭环。

默认原则：支持不是为了把人训练成客服，而是为了减少下一次支持需求。能用产品、文档、默认配置、监控、eval 或 runbook 消除的联系原因，不应该永远靠人工回复。

## 核心依据

- 《人月神话》：用户支持暴露的是系统概念不一致和隐藏复杂度；不能靠更多人或更多消息线程解决。
- 小型项目管理：一人公司需要短流程、清晰优先级和可恢复上下文，避免支持工作吞掉连续研发时间。
- The Best Service is No Service：客户联系支持往往是产品或流程失效的数据点；最好的支持是消除重复联系原因。
- The Effortless Experience：用户并不需要被“惊喜”，更需要低努力地解决问题。
- ITIL Incident Management：支持中的事故目标是尽快恢复正常服务，而不是先追求完美根因。
- Google SRE Incident Response / Postmortem Culture：事故和用户影响需要结构化沟通、工作记录、复盘和行动项。
- Atlassian Incident Communication：用户影响事件要有单一事实来源，尽早、准确、持续沟通。
- Zendesk / Intercom 支持实践：支持队列要有分类、优先级、响应/解决指标和反馈闭环。
- OpenAI Safety Best Practices / Moderation / Safety Checks：AI 产品需要 moderation、人审、red team、用户级安全标识和对有害输出的处理流程。
- NIST AI RMF：部署后的 AI 系统需要持续监控、外部反馈、申诉/覆盖、事故响应、恢复和变更管理。

## 范围

适用对象：

- 生产 SaaS、付费 AI 产品、公开 beta、用户可见 AI workflow、计费/权益/账号相关支持。
- 用户通过邮件、表单、聊天、社区、GitHub issue、Linear、社交媒体或内嵌反馈提交的问题。
- AI 输出错误、有害输出、越权工具调用、隐私请求、账号删除、退款、服务事故、重大流失风险。

不适用对象：

- 纯内部工具、无外部用户、无生产支持承诺的实验。
- 正式法律通知、监管问询、合规审计和合同谈判；这些需要专业服务或单独 OpenSpec。
- 大型客服团队排班、QA 评分体系、客服机器人平台和呼叫中心流程。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
support/
  intake/<target>.json
  playbooks/<target>.md
  templates/<target>.md
  feedback-ledger/<target>.jsonl
  reviews/<target>.md
```

### `support/intake/<target>.json`

支持入口必须包含：

- `target`
- `owner`
- `channels`
- `categories`
- `severity_levels`
- `first_response_targets`
- `data_handling`
- `routing`
- `linked_artifacts`
- `metrics`
- `human_checkpoint`
- `review_cadence`

默认分类至少覆盖：

- bug / defect
- billing / entitlement / account access
- incident / outage
- privacy / security request
- AI output concern / safety / abuse
- feature request / product feedback
- docs / usability confusion

默认指标只保留少量可行动信号：

- 未处理 backlog
- first response time
- time to resolution
- reopen rate
- top contact drivers
- customer effort 或“是否一次解决”的轻量替代

### `support/playbooks/<target>.md`

支持 playbook 必须包含：

- `Scope`
- `Triage`
- `Severity`
- `First Response`
- `Reproduction`
- `Workaround`
- `Escalation`
- `Billing / Access`
- `AI Output Complaints`
- `Privacy / Security Requests`
- `Incident Handoff`
- `Close Criteria`

默认处理顺序：

1. 识别是否正在影响多个用户、资金、权限、隐私、安全或 AI 伤害。
2. 先恢复用户： workaround、降级、撤销错误权益、补发 credit、关闭高风险 workflow 或进入 incident。
3. 最小复现：request id、时间、环境、版本、feature flag、错误类别，不默认收集完整 raw prompt 或用户私密内容。
4. 链接研发 artifact：bug、OpenSpec change、eval case、security incident、billing reconciliation 或 docs issue。
5. 关闭前确认：用户影响、临时方案、后续动作和是否需要复盘。

### `support/templates/<target>.md`

回复模板必须包含：

- `Bug / Defect`
- `Billing / Access`
- `AI Output Concern`
- `Privacy / Security Request`
- `Incident Update`
- `Refund / Credit`
- `Feature Request`
- `Closure`

默认模板规则：

- 先承认事实和影响，再说明正在做什么。
- 不承诺未经验证的修复时间、退款、法律结论、数据删除完成或 24/7 支持。
- 事故更新使用同一事实来源；不要在多个渠道写不同版本。
- AI 输出投诉回复必须说明已记录、会按安全/质量流程检查，避免把模型输出当成公司立场。

### `support/feedback-ledger/<target>.jsonl`

支持反馈账本每行一条，字段至少包含：

```json
{"id":"sup-001","date":"2026-06-24","source":"email","category":"ai_output_concern","severity":"S2","summary":"用户报告助手在账单解释中引用了不存在的优惠","evidence":"redacted description and request id","customer_impact":"billing confusion","linked_artifact":"openspec/changes/fix-billing-answer-eval","next_action":"add eval case and clarify template","redacted":true}
```

默认：

- 账本记录可行动事实，不保存邮箱、电话、真实姓名、支付信息、密钥、完整 raw prompt、完整 raw response 或隐私数据。
- AI 输出投诉优先转成 eval fixture 的候选样本，但必须先脱敏和裁剪。
- 重复反馈进入 top contact drivers，不让同一个问题每次都从零处理。

### `support/reviews/<target>.md`

支持 review 必须包含：

- `Queue Health`
- `Top Contact Drivers`
- `Root Cause Fixes`
- `Product Feedback`
- `Docs / Self-Service`
- `AI Trust And Safety`
- `Risks And Escalations`
- `Next One Change`

默认节奏：

- pre-revenue：每两周 30 分钟。
- 有付费用户：每周 30 分钟。
- 有 SEV1/SEV2、退款潮、AI 伤害投诉、安全隐私请求：当天或次日复盘。

每次 review 只选一个“下一步最高影响改进”。一人公司不做无限 support backlog。

## Go / Kratos / sqlc / gRPC 默认规则

- 支持相关后台默认用 Go/Kratos 服务端执行权限检查，不让前端直接读取跨租户支持数据。
- sqlc 表默认包含：`support_cases`、`support_events`、`support_feedback_links`、`support_template_versions`、`support_review_items`。
- 支持 case 关联 `tenant_id`、`actor_id`、`request_id`、`trace_id`、`release_id`、`prompt_version`、`model` 时使用最小必要字段。
- 支持人员或 founder 访问用户数据必须审计；生产数据 access、impersonation、手工修复必须人工 checkpoint。
- 支持动作如果改变计费、权益、数据删除、权限或外部通知，必须走对应阶段规范。

## Vite 前端默认规则

- 支持入口必须低摩擦：用户能从产品内带上 request id、feature、时间和错误类别提交问题。
- 表单默认不要求用户粘贴完整 prompt、response、secret、日志或支付信息。
- AI 输出旁边可以提供“报告问题”入口，但必须提示不要提交敏感信息。
- 帮助页和状态页使用 Vercel/Geist 风格：简洁、清晰、少装饰，突出当前状态、已知问题、下一步。

## AI workflow 默认规则

- AI 输出投诉必须记录 model、prompt/workflow version、tool path、request id 和安全类别。
- 有害内容、越权工具行为、幻觉影响钱/权限/法律/医疗/安全时，升级为 human checkpoint。
- 支持反馈可以进入 eval，但必须脱敏、最小化，并连接 W3 prompt/eval 规范。
- 面向用户的 AI support assistant 不得自行承诺退款、法律结论、数据删除、权限变更或事故恢复时间。
- 对可能违反 OpenAI 使用政策或产品安全边界的请求，使用 moderation/safety check、账户级 safety identifier 或等价机制帮助定位和处理。

## 需要人判断的关键点

只把这些判断交给人：

- 是否公开事故通知、状态页更新、道歉、补偿或事后说明。
- 是否退款、发 credit、改变合同承诺、改变权益或手工覆盖账号状态。
- 是否处理法律、隐私、安全、数据删除、数据导出或监管相关请求。
- 是否认定 AI 输出造成或可能造成实际伤害、歧视、误导、越权、滥用或政策风险。
- 是否查看生产用户数据、模拟用户、执行手工数据修复或跨租户排查。
- 是否承诺更短响应时间、24/7、专属支持或高价值客户例外。
- 是否把支持反馈提升为产品路线、OpenSpec change、公开 bug 或安全公告。

其他分类、字段完整性、模板章节、敏感内容、反馈账本格式和 review 节奏由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件覆盖入口、处理、回复、反馈账本和定期 review。
- 保留：只把钱、法律/隐私/安全、生产数据访问、公开沟通、AI 伤害和服务承诺交给人。
- 调整：不要求购买客服系统；JSON/Markdown/JSONL 足够先落地，也能迁移到 Linear、GitHub、Zendesk 或 Intercom。
- 调整：不把所有用户请求都变成 OpenSpec；只有重复、高影响或改变产品方向的反馈进入研发 change。
- 风险：支持 review 容易变成情绪复盘。缓解：`Top Contact Drivers` 和 `Next One Change` 强制回到减少重复联系原因。

结论：可落地。一个人可以先用半天为第一个产品 target 写完五个工件，然后每周用 30 分钟把支持噪音转成一个最高影响改进。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：反馈账本把支持消息接回产品发现、文档和 UX 修复，避免只按大声用户改产品。
- 工程角度：request id、trace id、release id、prompt version 和 linked artifact 让 bug 复现和 eval 补样有入口。
- 运维角度：incident handoff、状态页和单一事实来源连接 W7 SRE-lite。
- 安全隐私角度：默认不收 raw prompt、raw response、secret、支付信息或不必要个人数据；高风险请求进入人审。
- 成本角度：减少重复支持需求比堆客服自动化更适合一人公司，也能暴露 docs、UX 和计费权益缺陷。

结论：可落地。本专项把 W1 Discovery 的产品学习、W3 AI Behavior 的 AI eval、W7 Operate 的事故沟通、W4 Build 的计费权益和 W2 OpenSpec / Risk 的安全隐私串成一个用户信任闭环。
