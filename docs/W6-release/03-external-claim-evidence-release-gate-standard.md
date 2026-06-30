# W6 Release 触发专项：对外承诺、声明与证据发布门禁规范

## W6 触发定位

本文件是 W6 Release 的触发型专项，不是 W6 主入口。只有当当前工作涉及官网、pricing、docs、developer portal、AI disclosure、trust/security/privacy、support/sales 文案、release notes 或任何对外强声明时，才需要读取本文件。

普通 W6 发布入口应先回到 `docs/W6-release/00-main.md`，由主入口判断是否触发本专项。

## 目标

一人公司做 AI 产品时，风险常常不是“没有做”，而是“说法跨了界”：官网写了不训练，供应商配置没有核对；文档说稳定 API，契约还在 experimental；销售邮件承诺 24/7，SRE 只定义了工作时间响应；AI disclosure 说有人审，但产品里没有状态机；客服模板把临时 workaround 说成长期能力。本专项的目标是把所有对外承诺、声明和强说法压成一个发布前门禁：每句话都能追到证据、owner、最后验证时间、适用范围和更正路径。

本专项不替代 W2 信任政策、W9 证据保全、W2 客户数据生命周期、W2 供应商处理、W6 商业义务和 W4 开发者文档。它负责在发布前确认这些工件对同一个 claim 给出一致答案。

默认原则：**对外声明即产品接口**。没有证据的强声明只能是 draft；证据过期的声明必须降级、隐藏、改写或进入人工判断。

## 核心依据

- 《人月神话》：概念完整性要靠少数一致决策维持；官网、合同、文档、产品 UI 和客服回复如果各说各话，会形成长期概念债。
- 小型项目管理：一人公司不能维护大型法务、GRC、营销审批和销售运营流程；只保留能拦住高损失错误承诺的 5 个工件。
- FTC Advertising Substantiation / Advertising and Marketing：客观产品声明需要合理依据，广告声明要真实、不可欺骗且有证据。
- FTC Operation AI Comply：AI 不是监管例外；用 AI hype、专业替代、收入增长或能力夸大误导用户，会变成真实执法风险。
- NIST AI RMF / Generative AI Profile：生成式 AI 风险管理要贯穿设计、开发、使用、评估和持续管理。
- NIST Privacy Framework：隐私实践要连接业务目标、角色、数据处理和沟通；声明必须能落到实际数据处理活动。
- OECD AI Principles：AI 系统需要透明、可解释、可挑战、稳健安全和问责追踪。
- Google SRE SLO/SLA：SLO 是内部可测目标，SLA 是对外协议或商业后果；不能先写 SLA 再补观测。
- OpenAI Data Controls / Usage Policies / DPA：模型供应商的数据使用、保留、可接受使用、处理方条款和项目级设置会影响你能对客户说什么。
- Vercel `design.md` / `design.dark.md`：面向用户的声明页面、trust center 或设置界面应清晰、克制、可扫描，不用营销视觉掩盖限制。

## 范围

适用对象：

- 官网、pricing、landing page、help center、docs、developer portal、API reference、SDK README、release notes、status page、security page、privacy、terms、DPA、AUP、AI disclosure。
- 产品内 Vite UI、设置页、控制台、empty state、错误页、提示框、AI 功能说明、权限/删除/导出/账单界面。
- 销售邮件、客服模板、support macro、RFP/安全问卷、合同侧信、订单、SLA、公开 roadmap、blog、案例研究。
- AI capability、accuracy、latency、availability、security、privacy、data retention、no-training、data residency、human review、compliance、billing/refund、IP/license、support response、developer API stability 等 claim。

不适用对象：

- 正式法律意见、广告审查意见、监管申报、诉讼保全、法务审批系统；这些需要专业服务或单独 change。
- 纯内部草稿，只要不发送给用户、客户、公众、审核方或供应商。
- 已经由 W2/W9/W6/W4 管理的底层工件本身；本专项只做跨 surface 的发布一致性和证据门禁。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
claim-control/
  surface-inventory/<target>.json
  claim-evidence-map/<target>.json
  release-gate/<target>.json
  correction-runbook/<target>.md
  claim-review/<target>.md
```

### `claim-control/surface-inventory/<target>.json`

Surface inventory 必须包含：

- `target`
- `owner`
- `surfaces`
- `source_artifacts`
- `claim_sources`
- `scan_policy`
- `human_checkpoint`
- `review_cadence`
- `status`

`surfaces` 每项至少包含：

- `id`
- `name`
- `surface_type`
- `location`
- `audience`
- `owner`
- `source_of_truth`
- `last_scanned`
- `status`

`surface_type` 默认包含：

- `marketing`
- `pricing`
- `docs`
- `developer_docs`
- `product_ui`
- `contract`
- `support`
- `security`
- `privacy`
- `status`
- `release_notes`
- `sales`

默认规则：

- 只登记会被外部依赖的 surface，不登记私人笔记。
- `source_of_truth` 必须链接 W2、W9、W6、W4 或代码/配置/eval/观测中的事实源。
- 如果 surface 对应 AI、隐私、安全、SLA、计费、合同或开发者稳定性，必须有 owner 和 last_scanned。

### `claim-control/claim-evidence-map/<target>.json`

Claim evidence map 必须包含：

- `target`
- `owner`
- `claims`
- `evidence_sources`
- `substantiation_policy`
- `expiry_policy`
- `human_checkpoint`
- `status`

`claims` 每项至少包含：

- `id`
- `claim_text`
- `claim_type`
- `surface_refs`
- `risk_level`
- `scope`
- `evidence_refs`
- `substantiation_level`
- `last_verified`
- `expires_at`
- `owner`
- `status`

`claim_type` 默认包含：

- `ai_capability`
- `ai_limitation`
- `accuracy_or_quality`
- `latency_or_performance`
- `availability_sla`
- `security`
- `privacy_data_use`
- `data_retention`
- `no_training`
- `data_residency`
- `human_review`
- `compliance`
- `billing_refund`
- `support_response`
- `api_stability`
- `ip_license`

`substantiation_level` 默认包含：

- `source_link`
- `config_verified`
- `test_or_eval`
- `slo_measurement`
- `contract_or_dpa`
- `manual_attestation`
- `unsupported`

默认规则：

- `risk_level=high` 或 `claim_type` 涉及 AI 能力、安全、隐私、数据保留、不训练、合规、SLA、合同、费用、专业建议时，必须有人审 checkpoint。
- `unsupported` 只能用于 `draft` 或 `blocked`，不能进入 `approved`、`published`。
- `expires_at` 过期后，claim 进入 `needs_review`，不得继续发布强声明。
- 证据优先引用事实源，不复制敏感证据内容。

### `claim-control/release-gate/<target>.json`

Release gate 必须包含：

- `target`
- `owner`
- `change_id`
- `release_or_surface`
- `changed_claims`
- `new_claims`
- `removed_claims`
- `evidence_checks`
- `surface_checks`
- `human_decisions`
- `rollback_or_correction`
- `linked_artifacts`
- `status`

`changed_claims`、`new_claims` 每项至少包含：

- `claim_id`
- `change_type`
- `old_text`
- `new_text`
- `risk_level`
- `evidence_ref`
- `human_checkpoint`
- `decision`

默认规则：

- 任何对外 surface 改动如果新增强承诺、扩大适用范围、减少限制说明或改变数据/AI/安全/费用/SLA 含义，必须更新 release gate。
- 只修 typo、格式或链接，不改变 claim 含义时可以记录为低风险，不需要人判断。
- `decision=approve` 前，必须确认 claim evidence map 没有 unsupported、expired、missing owner、missing scope。
- Release gate 必须能链接 OpenSpec change、release checklist、evidence package 或 PR/commit。

### `claim-control/correction-runbook/<target>.md`

Correction runbook 必须包含：

```markdown
# <target> Claim Correction Runbook

## Scope

## Trigger Conditions

## Triage

## Surfaces To Update

## Customer / Developer Notice

## Contract / Support Handling

## Evidence Preservation

## Rollback / Mitigation

## Owner And Timeline

## Review Cadence
```

默认规则：

- 如果发现 claim 错误、过期、证据失效、供应商政策变化或系统能力退化，先降级/隐藏/更正，再评估是否需要客户通知。
- 更正不只改官网；要检查 docs、SDK、support macro、contract/order、AI disclosure、privacy、security page、developer changelog 和 sales material。
- 客户/开发者通知由风险决定：普通文案更正可以不通知；数据、安全、隐私、SLA、计费、AI 能力或合同承诺错误必须人审。
- 保留证据时只保存链接、版本、hash、截图摘要或 release id，不复制 secret、客户内容、raw prompt/response。

### `claim-control/claim-review/<target>.md`

Claim review 必须包含：

```markdown
# <target> External Claim Review

## Recent Surface Changes

## New / Changed Claims

## Evidence Gaps

## Expiring Claims

## AI / Data / Security Claims

## SLA / Contract / Billing Claims

## Developer / API Stability Claims

## Corrections / Notices

## Open Risks

## One Next Change

## Review Cadence
```

默认节奏：

- pre-revenue：每月一次，或每次改官网、pricing、privacy、AI disclosure、developer docs、support template、合同/SLA 前。
- 有付费客户：每次 release、销售材料、合同条款、供应商政策、模型/路由、SLO/SLA、数据处理或开发者 API 稳定性变化前。
- 发现错误承诺、客户投诉、合规问题、供应商政策变化、事故、SLA 偏差或 AI 能力退化：立即复盘。

## Go / Kratos / sqlc / gRPC 默认规则

- 对外 claim 如果依赖后端行为，必须能追到 Go/Kratos config、feature flag、tenant setting、model route、SLO、audit event、release gate、sqlc 数据状态机或供应商 client boundary。
- 可选 sqlc 表：`external_claims`、`claim_surfaces`、`claim_evidence_links`、`claim_release_gates`、`claim_correction_events`、`claim_reviews`。
- 内部 gRPC API 可以提供 `ListExternalClaims`、`GetClaimEvidence`、`RecordClaimGateDecision`、`RecordClaimCorrection`，但浏览器不得自行决定 claim 是否可发布。
- 影响数据保留、删除、训练、供应商、SLA、计费、权限或 AI 行为的配置变更，必须能更新 claim gate 或阻止 release。
- 日志记录 claim gate 事件时保存 claim id、surface id、actor、decision、evidence ref、request id、trace id，不保存敏感内容。

## Vite 前端默认规则

- 面向用户的设置页、trust center、pricing、AI disclosure、developer docs 和支持入口应使用克制、可扫描的信息结构；不靠 hero 或装饰性文案承载限制。
- 强声明旁边要能找到范围、限制、更新时间或链接；尤其是 AI、隐私、安全、SLA、数据驻留、删除、训练、费用和稳定 API。
- 不在按钮、tooltip、empty state 或成功提示里加入未经 gate 的“保证”“永远”“完全”“实时”“无限”“不训练”“合规级”“专业级”等词。
- 如果 claim 被降级或更正，UI 应显示真实状态和下一步，不用含糊状态掩盖能力退化。
- 使用 Vercel/Geist 风格时，优先清晰排版、状态徽标、表格、时间戳和链接证据，避免用营销感视觉削弱限制说明。

## AI workflow 默认规则

- AI 不能自行发布、扩写或强化对外 claim；AI 可生成 draft、扫描差异、建议降级措辞，但发布前必须通过 release gate。
- AI 生成营销、help center、developer docs、contract summary、RFP/security questionnaire、support macro 时，必须标记新增或强化的 claim。
- AI 能力声明必须连接 eval、red-team/safety finding、model route、prompt version、tool/runtime guard、RAG eval、human review 或供应商官方边界。
- 不承诺“总是正确”“无幻觉”“替代律师/医生/财务顾问”“不会泄露”“不用于训练”“零保留”“完全合规”“实时响应”“100% uptime”，除非证据、范围和例外明确存在。
- AI 发现 claim 与证据冲突时，默认输出阻断结论和最低风险改写建议，不自动发布 correction。

## 需要人判断的关键点

默认不问：

- 字段顺序、低风险 wording、链接修正、内部草稿、没有改变 claim 含义的 typo。

必须问：

- 是否发布或保留高风险 claim：AI 能力/准确性、专业替代、安全、隐私、数据保留、不训练、数据驻留、SLA、合规、费用、退款、IP、人工审核。
- 是否把 claim 的范围从 beta/internal/experimental 扩大到 public/stable/customer-contract。
- 是否接受证据不足、证据过期、供应商政策不清、系统能力不一致或无法复现的 claim。
- 是否需要对客户、开发者、审计方、监管方或公众更正/通知。
- 是否承认合同、SLA、DPA、隐私政策、security page、sales email 或 support reply 中已经形成承诺。
- 是否需要律师、隐私/安全顾问、客户合同审阅、广告审查或专业合规意见。

其他字段完整性、章节、枚举、敏感内容、证据链接、过期时间、surface 覆盖、OpenSpec linkage、positive/negative fixture 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“哪里有声明、声明证据在哪、这次发布改了什么、错了怎么改、多久复盘”。
- 保留：人只判断高风险 claim、证据不足接受、范围扩大、更正通知和专业意见。
- 调整：不要求每句普通文案都审批；只抓客观、可依赖、可造成损失的声明。
- 调整：不复制合同、日志或客户数据，只保存 claim id、surface、证据链接、验证时间和状态。
- 风险：门禁可能变成营销/法务流程负担。缓解：release gate 只在 claim 含义变化时触发，脚本处理字段和过期检查。

结论：可落地。一个人可以先把官网、pricing、privacy、AI disclosure、developer docs 和前几个合同里的 20 个强声明登记起来，立即降级没有证据的 claim。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：减少用户因误解 AI 能力、数据用途、删除能力或 SLA 而流失或投诉。
- 工程角度：claim 映射到 Go/Kratos 配置、sqlc 状态、eval、SLO、供应商设置和 release gate，避免“文案比系统先行”。
- 运维角度：SLO/SLA、status、incident、correction runbook 和客户通知有共同入口。
- 安全隐私角度：不训练、零保留、数据驻留、安全认证、删除完成等声明必须连接真实供应商和系统证据。
- 成本角度：提前拦住 24/7、高 SLA、专业级 AI、无限退款、专属区域等昂贵承诺。

结论：可落地。本专项把“能不能对外这样说”变成小而硬的发布门禁，保护一人公司的注意力、信任和现金流。
