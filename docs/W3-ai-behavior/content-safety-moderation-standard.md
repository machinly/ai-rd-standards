# AI 产品内容安全、用户生成内容与审核策略规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/main.md` 已经判断需要内容安全、UGC、AI 生成内容审核、用户通知、申诉或审核复盘时，才读取本文件。

如果当前只是判断 AI 行为应该如何定义好坏、失败和降级，先回到 `docs/W3-ai-behavior/main.md`。

## 目标

AI 产品很容易同时拥有两类内容风险：用户提交的内容可能违规、骚扰、欺诈或伤害他人；AI 生成的内容也可能被发布、分享、引用或自动执行。本专项定义内容安全、用户生成内容与审核策略规范，让每个可发布内容 surface 都能回答：允许什么、禁止什么、自动化怎么判、什么时候人审、怎么通知用户、用户如何申诉、审核质量怎么复盘。

默认原则：内容审核不是一个分类器调用。它是政策、自动化、人工复核、用户通知、申诉、日志和复盘的组合；任何自动化 enforcement 都要能解释、能纠错、能恢复。

## 核心依据

- 《人月神话》：内容政策是系统边界的一部分；如果规则、产品文案、后端动作和客服解释不一致，复杂度会以误封、漏放、争议和信任损失的形式回来。
- 小型项目管理：一人公司不能维护大型 Trust & Safety 团队；只保留 policy、moderation rules、enforcement runbook、notice/appeal、moderation review 五个可执行工件。
- OpenAI Moderation / Safety Best Practices / Usage Policies：应用应检测 harmful content，用 moderation 结果执行过滤、review、干预或账号处理，并结合人审、反馈、safety identifier 和使用政策。
- Santa Clara Principles：内容审核需要透明、可解释、可申诉，用户应知道规则、原因和救济路径。
- EU Digital Services Act：即使不直接适用，一人公司也可借鉴 notice-and-action、statement of reasons、appeal、透明度报告和未成年人保护的产品原则。
- TSPA Content Moderation and Operations：内容审核是按平台政策审查 UGC 的流程，可由人工、自动化或两者组合完成；成熟流程需要队列、申诉和指标。
- TSPA Metrics for Content Moderation：只看处理量不够；要看 enforcement、appeal、速度、质量、误判和恢复。
- Building Successful Online Communities：社区安全不是事后清扫，规则、反馈、激励和成员承诺会影响社区行为。
- Custodians of the Internet：平台通过内容审核塑造公共空间和用户信任，审核不是边缘功能。
- Behind the Screen：人工审核有心理和劳动成本；一人公司尤其要避免把自己暴露在不必要的极端内容里。
- Partnership on AI Responsible Practices for Synthetic Media：AI 生成或修改的媒体需要合适的披露、标签、来源信号和使用场景约束。

## 范围

适用对象：

- 用户生成内容：评论、帖子、聊天消息、文件上传、图片、音频、视频、资料页、prompt、反馈、工单、公开分享内容。
- AI 生成内容：文本、图片、音频、视频、代码、摘要、建议、自动回复、公开页面、可下载文件和可转发内容。
- Moderation API、第三方内容审核服务、自建规则、人工复核、用户举报、notice-and-action、账号限制、内容移除、申诉和恢复。
- Go/Kratos/sqlc/gRPC 后端中的内容状态、moderation decision、review queue、appeal、audit log、safety identifier 和 enforcement action。
- Vite 前端中的举报入口、审核队列、用户通知、申诉表单、内容标签、AI disclosure 和审核复盘页面。

不适用对象：

- 正式法律意见、执法协作、强监管行业内容审查或区域法律适配；这些需要单独专业审阅。
- 纯内部、不保存、不对用户展示、不影响账号/权益的临时测试内容。
- W3 AI 红队发现管理；本专项关注日常内容进入产品和用户沟通路径。

## 最小工件

每个可发布内容 surface 使用同一个 `<surface>` 文件名：

```text
content-safety/
  policy/<surface>.md
  moderation-rules/<surface>.json
  enforcement-runbook/<surface>.md
  notice-appeal/<surface>.md
  moderation-review/<surface>.md
```

### `content-safety/policy/<surface>.md`

Policy 必须包含：

- `Scope`
- `Allowed Content`
- `Disallowed Content`
- `Restricted / Sensitive Content`
- `AI-Generated Content`
- `User-Generated Content`
- `Minors / Age Boundaries`
- `Enforcement Actions`
- `Appeals`
- `Policy Sources`
- `Owner And Review Cadence`
- `Linked Artifacts`

默认：

- 内容政策用产品语言写，不复制供应商政策全文；供应商政策作为 `Policy Sources` 引用。
- 禁止和限制类别至少覆盖：违法/危险、仇恨/骚扰、性内容、儿童安全、自伤/危机、暴力/极端主义、欺诈/诈骗、隐私泄露、垃圾/滥用、误导/冒充、IP/版权、平台规则绕过。
- AI 生成内容要说明何时需要标签、来源说明、限制传播或人工复核。
- 任何账号限制、内容移除、公开降权或不可逆 action 都要连接申诉路径。

### `content-safety/moderation-rules/<surface>.json`

Moderation rules 必须包含：

- `surface`
- `owner`
- `content_types`
- `categories`
- `actions`
- `automation_level`
- `human_review`
- `appealable_actions`
- `notice_policy`
- `logging`
- `privacy`
- `provider_refs`
- `test_refs`
- `human_checkpoint`
- `review_cadence`

`categories` 每项至少包含：

- `id`
- `name`
- `source_policy`
- `severity`
- `action`
- `threshold`
- `human_review`
- `appealable`
- `user_notice`
- `retention`
- `status`

默认 `severity`：

- `critical`
- `high`
- `medium`
- `low`
- `info`

默认 `action`：

- `allow`
- `label`
- `limit`
- `review`
- `block`
- `hide`
- `remove`
- `suspend`
- `rate-limit`
- `escalate`
- `report`

默认：

- `critical` 内容默认 `block` / `remove` / `escalate`，并进入人工 checkpoint。
- 自动化 action 超过 `label`、`limit` 或 `review` 时，必须有 notice、appeal、audit 和复盘样本。
- 第三方模型分数不是最终政策；必须映射到本产品的 category、threshold、action 和 appealability。
- Perspective API 等外部审核服务可以作为参考，但必须记录供应商、模型/版本边界、阈值和替代方案；不要把不可 pin 的分数当唯一长期控制。

### `content-safety/enforcement-runbook/<surface>.md`

Enforcement runbook 必须包含：

- `Scope`
- `Decision Flow`
- `Pre-Publish Checks`
- `Post-Publish Checks`
- `Human Review Queue`
- `Escalation`
- `Account Actions`
- `Emergency Actions`
- `Restoration`
- `Audit Trail`
- `Rollback / Correction`
- `Linked Artifacts`

默认：

- 内容动作按风险从低到高排列：allow、label、limit、review、hide、remove、suspend、report。
- 对用户权益影响越大，越需要人审、notice、appeal 和恢复路径。
- AI 生成内容被用于自动回复、公开发布、医疗/法律/金融/安全建议或未成年人场景时，默认进入更高等级复核。
- 审核队列必须避免把一个人暴露给大量极端内容；用摘要、redaction、二次确认和停止条件保护审核者。

### `content-safety/notice-appeal/<surface>.md`

Notice and appeal 必须包含：

- `Scope`
- `Notice Triggers`
- `Statement Of Reasons`
- `User Message Templates`
- `Appeal Intake`
- `Appeal Review`
- `Restoration / Correction`
- `Abuse Of Appeals`
- `Response Targets`
- `Linked Artifacts`

默认：

- 用户应知道内容或账号发生了什么、违反了哪条规则、影响是什么、如何申诉。
- 通知不暴露模型阈值、审核绕过细节、举报人身份、系统提示或安全漏洞。
- 申诉需要二次判断；同一个自动化结果不能作为唯一复核证据。
- 恢复内容或账号时记录原因、时间、影响面和是否需要用户沟通。

### `content-safety/moderation-review/<surface>.md`

Moderation review 必须包含：

- `Recent Changes`
- `Volume And Queue Health`
- `Automation Quality`
- `Appeals And Reversals`
- `User Reports`
- `False Positives / False Negatives`
- `Moderator Wellbeing`
- `Policy Gaps`
- `Open Risks`
- `Next One Change`

默认：

- pre-revenue：每月一次或每次内容 surface / policy / moderation provider 变化前。
- 有活跃用户：每两周一次或每次会影响自动化 enforcement 的 release 前。
- 涉及未成年人、违法内容、危机、自伤、暴力、性内容、账号封禁、外部投诉、媒体/公共风险：立即复盘。
- 每次只选一个最高影响改进，避免内容安全复盘变成无限 backlog。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端必须把 moderation decision 表达成显式状态：`allow`、`label`、`limit`、`review`、`block`、`hide`、`remove`、`suspend`、`escalate`。
- sqlc 表默认包含：`content_items`、`moderation_decisions`、`moderation_reviews`、`moderation_appeals`、`content_reports`、`policy_versions`。
- gRPC API 必须区分用户提交、AI 生成、人工审核、系统自动化和管理员动作的 actor。
- Moderation request/response 不默认保存完整原文；保存 hash、content id、category、score bucket、decision、policy version、reviewer、appeal id 和 audit link。
- Safety identifier 使用稳定 hash，不把 email、手机号、真实姓名或未脱敏个人数据发给模型供应商。
- 内容移除、账号限制、申诉驳回、恢复和 report-to-authority 属于高风险 action，连接 W7 后台动作审计。

## Vite 前端默认规则

- 举报入口必须明显、短路径、移动端可用；不要用深层菜单或暗色小字隐藏。
- 用户通知要清楚说明 action、rule、影响、申诉入口和预计响应，不承诺无法保证的处理时间。
- 审核工作台保持密集但清晰：category、severity、content type、decision、policy version、appeal status、linked artifact 同屏可见。
- 展示敏感内容默认 redacted 或点击展开；高危内容需要二次确认和停止条件。
- AI 生成内容需要标签或上下文说明时，前端使用稳定的标签、tooltip 和链接，不用营销文案掩盖限制。

## AI workflow 默认规则

- Moderation 不是唯一安全控制；prompt policy、red-team cases、structured output、tool permission、rate limit、support escalation 和 human review 一起生效。
- 输入和输出都要考虑审核：用户输入可能违法或滥用，模型输出也可能 harmful 或不适合展示。
- 变更 moderation threshold、category mapping、policy boundary、AI disclosure 或 appeal policy 时，必须走 OpenSpec change。
- 自动化审核误判样本应进入 W3 eval/data 或 W3 adversarial cases。
- 模型不得自行决定账号封禁、退款、法律结论、执法报告或不可逆内容删除；这些必须有人审或明确后台 action gate。

## 需要人判断的关键点

只把这些判断交给人：

- 是否新增或修改 prohibited category、policy boundary、moderation threshold 或 enforcement action。
- 是否自动移除内容、限制账号、封禁、公开降权、拒绝申诉或报告给外部机构。
- 是否处理儿童安全、自伤/危机、性内容、暴力/极端主义、医疗/法律/金融、选举/公共安全或受监管内容。
- 是否发布或分享 AI 生成媒体、synthetic media、深度伪造、人物肖像或可能误导的内容。
- 是否保存或查看高危原文、极端内容、真实用户隐私、举报人信息或法律敏感证据。
- 是否公开透明度报告、用户承诺、审核准确率、申诉数据或供应商能力声明。

其他字段完整性、章节、JSON/枚举、notice/appeal 覆盖、敏感内容扫描、必需 checkpoint 和 OpenSpec linkage 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“规则是什么、自动化怎么判、怎么执行、怎么告知/申诉、多久复盘”。
- 保留：人只判断政策边界、自动化惩罚、高危内容、申诉拒绝、外部报告和公开承诺。
- 调整：不要求 24/7 审核队列；先用低风险自动化 + 少量人工复核 + 用户举报入口。
- 调整：不要求复杂透明度报告；先记录 volume、appeal reversal、false positive/negative 和 next one change。
- 风险：分类器分数容易被当成“真相”。缓解：rules 必须把 provider score 映射到产品 policy、action、appeal 和 review。

结论：可落地。一个人可以先为最重要内容 surface 写 10 到 15 条 category/action 规则，再用 verifier 保持字段和申诉路径完整。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户知道规则、原因和申诉路径，减少误封带来的信任损失。
- 工程角度：policy version、decision、appeal、review 和 audit link 可追踪，便于回滚和修正。
- 运维角度：queue health、appeal reversal、误判样本和用户报告进入周期复盘。
- 安全隐私角度：高危内容、未成年人、隐私泄露、举报人身份和审核者暴露都有边界。
- 成本角度：先用轻量规则和少量人工抽样，不提前购买重型审核平台或外包队列。

结论：可落地。本专项把内容安全从“接一个 moderation API”提升为可解释、可申诉、可复盘的最小产品能力，同时仍控制在一人公司可维护范围内。
