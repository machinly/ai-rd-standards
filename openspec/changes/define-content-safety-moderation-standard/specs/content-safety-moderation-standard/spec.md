# content-safety-moderation-standard 规格

## ADDED Requirements

### Requirement: 可发布内容 surface 必须定义 content-safety artifacts

Any product surface that accepts, stores, displays, shares, ranks, labels, removes, or enforces against user-generated content or AI-generated content MUST define content safety moderation artifacts.

#### Scenario: 新内容 surface 准备上线

- GIVEN 一个 surface 允许用户提交内容、AI 生成内容、公开展示内容、分享内容、上传文件、评论、聊天或触发账号/内容 enforcement
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `content-safety/policy/<surface>.md`
- AND 创建 `content-safety/moderation-rules/<surface>.json`
- AND 创建 `content-safety/enforcement-runbook/<surface>.md`
- AND 创建 `content-safety/notice-appeal/<surface>.md`
- AND 创建 `content-safety/moderation-review/<surface>.md`

### Requirement: Policy 必须定义允许、禁止、限制、AI/UGC、未成年人、执行和申诉

Policy MUST record scope、allowed content、disallowed content、restricted/sensitive content、AI-generated content、user-generated content、minors/age boundaries、enforcement actions、appeals、policy sources、owner/review cadence 和 linked artifacts。

#### Scenario: Reviewer 判断内容规则是否可执行

- GIVEN 一个 surface 有内容输入或输出
- WHEN reviewer 打开 `content-safety/policy/<surface>.md`
- THEN 能看到允许、禁止、限制、AI 生成内容、用户生成内容、未成年人边界、执行动作和申诉路径
- AND policy sources 连接 OpenAI usage policy、产品政策、法律/区域限制或供应商政策

### Requirement: Moderation rules 必须把政策映射到 category、threshold、action、review 和 appeal

Moderation rules MUST record surface、owner、content types、categories、actions、automation level、human review、appealable actions、notice policy、logging、privacy、provider refs、test refs、human checkpoint 和 review cadence。

#### Scenario: 自动化或人工审核执行规则

- GIVEN moderation service、人工审核队列或 release gate 读取 `content-safety/moderation-rules/<surface>.json`
- WHEN 处理内容
- THEN 每个 category 包含 id、name、source_policy、severity、action、threshold、human_review、appealable、user_notice、retention 和 status
- AND 自动化 action 超过 label/limit/review 时有 notice、appeal、audit 和 human checkpoint 覆盖

### Requirement: Enforcement runbook 必须定义决策流、队列、升级、账号动作、恢复和审计

Enforcement runbook MUST record scope、decision flow、pre-publish checks、post-publish checks、human review queue、escalation、account actions、emergency actions、restoration、audit trail、rollback/correction 和 linked artifacts。

#### Scenario: 内容或账号需要执行动作

- GIVEN 一个 moderation decision 要 label、limit、review、hide、remove、suspend、escalate 或 report
- WHEN 使用 `content-safety/enforcement-runbook/<surface>.md`
- THEN reviewer 能看到执行步骤、升级路径、恢复路径、审计记录和回滚/修正方式
- AND 对用户权益影响越大的动作需要越强 notice、appeal 和人审

### Requirement: Notice and appeal 必须提供原因、用户消息、申诉、二次复核和恢复

Notice and appeal MUST record scope、notice triggers、statement of reasons、user message templates、appeal intake、appeal review、restoration/correction、abuse of appeals、response targets 和 linked artifacts。

#### Scenario: 用户内容被移除或账号受限

- GIVEN 内容或账号 action 影响用户可见性、发布、访问、权益或账号状态
- WHEN 向用户发 notice 或处理 appeal
- THEN 用户能看到发生了什么、违反哪条规则、影响是什么、如何申诉
- AND appeal review 不得只重复原自动化结果

### Requirement: Moderation review 必须复盘队列健康、自动化质量、申诉、误判、用户报告和审核者安全

Moderation review MUST record recent changes、volume/queue health、automation quality、appeals/reversals、user reports、false positives/false negatives、moderator wellbeing、policy gaps、open risks 和 next one change。

#### Scenario: 内容安全周期复盘

- GIVEN surface 有近期内容、政策、分类器、阈值、申诉、举报或 enforcement 变化
- WHEN 更新 `content-safety/moderation-review/<surface>.md`
- THEN 记录队列健康、自动化质量、申诉反转、误判样本、用户报告、审核者暴露风险和开放缺口
- AND 只选择一个最高影响的 next one change

### Requirement: 自动化 punitive enforcement 必须有人审、通知、申诉和审计边界

Automated content removal, account restriction, suspension, public demotion, appeal denial, external reporting, or irreversible enforcement MUST require human checkpoint, notice, appealability rules, audit trail, and rollback/correction path.

#### Scenario: 自动化审核准备移除内容或限制账号

- GIVEN moderation rules 将 category action 设置为 remove、suspend、report 或其他 punitive action
- WHEN 准备发布或执行
- THEN `human_checkpoint.required_for` 包含 automated_enforcement_without_human_review 或对应高风险项
- AND notice-appeal、enforcement-runbook 和 audit trail 记录通知、申诉、复核和恢复方式

### Requirement: 高风险内容类别必须人工 checkpoint

Child safety, self-harm or crisis, sexual content, violence or extremism, medical/legal/financial advice, civic integrity, public safety, regulated content, sensitive personal data, synthetic media, and external reporting MUST have human checkpoint coverage.

#### Scenario: 高风险类别进入 policy 或 moderation rules

- GIVEN policy、rules、AI generated content、user reports 或 appeal 涉及高风险类别
- WHEN 准备将规则标为 ready 或执行 enforcement
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、升级或阻塞状态

### Requirement: Content safety artifacts 不得保存敏感内容

Content safety artifacts MUST NOT store secrets, production tokens, private keys, payment data, unredacted personal data, reporter identity, full harmful content, full raw prompts/responses, or unnecessary distressing content.

#### Scenario: 记录内容审核规则、样本、举报或申诉

- GIVEN 需要保存审核证据、规则样本、举报、申诉或误判案例
- WHEN 写入 `content-safety/` artifacts
- THEN 使用 content id、hash、redacted snippet、synthetic example、case id 或 controlled attachment reference
- AND 不保存 secrets、生产 token、私钥、支付数据、未脱敏个人数据、举报人身份、完整有害内容、完整 raw prompt/response 或不必要的刺激性内容
