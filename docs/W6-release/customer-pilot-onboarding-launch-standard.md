# W6 Release 触发专项：客户试点、上线导入与租户交付规范

## W6 触发定位

本文件是 W6 Release 的触发型专项，不是 W6 主入口。只有当当前工作涉及 design partner、private beta、paid pilot、客户 production go-live、租户导入、客户数据、SSO/SCIM、live billing、客户验收或 offboarding 时，才需要读取本文件。

普通 W6 发布入口应先回到 `docs/W6-release/main.md`，由主入口判断是否触发本专项。

## 目标

一人公司的客户上线风险不只在代码发布。真正容易失控的是：设计伙伴变成免费定制、试点目标不清、生产租户靠记忆配置、客户数据导入没有回滚、SSO/SCIM/计费/集成各有半套流程、AI 在客户数据上启用却没有验收和支持路径。

本专项负责把“一个客户要试用或上线”变成可重复交付流程：先定义试点成功标准，再记录租户事实，再做轻量上线 readiness，最后把客户成功、支持和退出路径交接清楚。

默认原则：**没有成功标准、租户事实、上线 gates、支持路径和退出路径，就不把客户带入生产。** 一人公司不做厚重交付项目，只维护五个能保护注意力的工件。

## 核心依据

- 《人月神话》：概念完整性和沟通成本决定项目质量；每个客户特例都会增加系统和人的协调面。
- 小型项目管理：小项目需要明确范围、责任、节奏和退出条件；一人公司用少数高价值工件替代会议和大型 PMO。
- The Lean Startup / Customer Development / The Mom Test：试点验证真实行为和业务结果，不验证客户口头表扬。
- Crossing the Chasm：客户上线不是交付一个功能碎片，而是交付一个能让客户完成工作的 whole product。
- Google SRE Reliable Product Launches / Launch Checklist / Production Readiness Review：外部可见变化需要轻量、可靠、可重复的 launch process；checklist 必须具体、可执行、不过度膨胀。
- Google Cloud Well-Architected Operational Readiness：go-live 和 day-2 运营需要明确期望、监控告警、容量、性能和支持承诺。
- AWS SaaS Lens：tenant onboarding 应自动化、可预测、可重复，覆盖租户、身份、隔离、计费、配置和基础设施。
- OpenAI Production / Data / Safety Best Practices：AI 生产上线要覆盖安全、速率、成本、数据控制、人工监督和对抗性测试。
- Stripe Go-live Checklist：真实收款前要切 live key、live webhook、错误处理、安全日志和 test/live 数据边界。
- Gainsight / Intercom Customer Onboarding：客户价值实现依赖 welcome/setup、培训、支持、参与度指标和生命周期内的 onboarding。

## 范围

适用对象：

- design partner、private beta、proof of concept、pilot、paid pilot、enterprise onboarding、production go-live。
- 新建客户 workspace/tenant、启用 SSO/SCIM、客户专属 feature flag、entitlement、billing、webhook/API 集成、数据导入/同步、AI route/RAG/memory/tool action。
- 从试点转付费、从内部试用转外部客户、从单客户 beta 转公开可用。

不适用对象：

- 产品发现访谈、机会判断和实验设计；走 W1 Discovery。
- 认证、授权、租户隔离的底层实现；走 W2 auth/tenant 专项。
- 数据导入、导出、删除和生命周期细节；走 W2 客户数据生命周期专项。
- 计费、entitlement、metering 和 webhook 对账；走 W4 计费与权益专项。
- 客户支持、投诉、信任运营；走 W8 客户支持专项。
- 合同、SLA、商业承诺；走 W6 商业承诺专项。
- 发布流水线、SRE、观测、事故处理；走 W7 SRE-lite 专项、6、15、44、48。

## 最小工件

每个客户试点或上线使用同一个 `<account>` 别名。别名不使用真实公司名、真实姓名、邮箱、手机号或客户 secret。

```text
customer-onboarding/
  pilot-charter/<account>.md
  tenant-provisioning/<account>.json
  launch-readiness/<account>.json
  success-plan/<account>.md
  handoff-review/<account>.md
```

### `customer-onboarding/pilot-charter/<account>.md`

试点章程必须包含：

```markdown
# <account> Pilot Charter

## Scope

## Customer Alias

## Problem / Outcome

## Pilot Type

## Success Criteria

## In Scope

## Out Of Scope

## Data Boundary

## AI Boundary

## Integration Boundary

## Timeline / Appetite

## Exit Criteria

## Human Checkpoints

## Linked Artifacts

## Review Cadence
```

默认规则：

- `Success Criteria` 写可观察结果：激活、完成任务、节省时间、错误减少、付费转换、留存、人工验收或明确业务事件。
- `Out Of Scope` 比 `In Scope` 更重要；客户特例、临时人工服务、未承诺集成、未承诺 SLA 必须写出来。
- `Data Boundary` 写是否接触真实客户数据、个人数据、导入数据、日志、附件、RAG source 或训练/eval 材料。
- `AI Boundary` 写是否使用客户数据进入 prompt、RAG、memory、tool action、人工审核、eval、日志和供应商处理。
- `Exit Criteria` 必须覆盖：转生产、延长试点、终止、删除/导出数据、关闭 feature flag、取消 entitlement。

### `customer-onboarding/tenant-provisioning/<account>.json`

租户导入事实必须包含：

- `target`
- `owner`
- `customer_alias`
- `environment`
- `tenant_id_ref`
- `identity`
- `roles`
- `entitlements`
- `feature_flags`
- `data_imports`
- `integrations`
- `billing`
- `ai_settings`
- `observability`
- `support_refs`
- `rollback_or_offboarding`
- `audit_refs`
- `human_checkpoint`
- `review_cadence`
- `status`

默认规则：

- `tenant_id_ref` 只写系统引用，不写真实 tenant secret、session、JWT、API key 或客户邮箱。
- `identity` 记录身份来源、SSO/SCIM 状态、管理员角色来源、生命周期 owner；真实 IdP secret 不进入文件。
- `roles` 和 `entitlements` 必须能解释“客户能做什么、不能做什么、为什么”。
- `feature_flags` 每项包含 `key`、`value`、`environment`、`rollout_scope`、`rollback`、`owner`、`status`。
- `data_imports` 每项包含 `id`、`data_classification`、`source`、`contract_ref`、`dry_run_required`、`status`。
- `integrations` 每项包含 `id`、`kind`、`provider`、`data_boundary`、`secrets_ref`、`webhook_or_api_refs`、`test_plan`、`status`。
- `billing` 写 test/live、plan、entitlement source、invoice/payment boundary、Stripe/customer id 的安全引用。
- `ai_settings` 写 model route、RAG source、memory、tool action、human review、eval gate 和 provider data boundary。
- `rollback_or_offboarding` 必须能回答：如何关闭租户访问、撤销 flag、暂停同步、导出/删除数据、停用集成、通知客户。

### `customer-onboarding/launch-readiness/<account>.json`

上线 readiness 必须包含：

- `target`
- `owner`
- `customer_alias`
- `launch_type`
- `readiness_gates`
- `blockers`
- `success_criteria`
- `support_plan`
- `communication_plan`
- `rollback_or_exit`
- `linked_artifacts`
- `human_checkpoint`
- `status`

`launch_type` 使用：`design_partner`、`private_beta`、`pilot`、`paid_pilot`、`production`、`internal_trial`。

外部客户上线默认检查以下 gate：

- `commercial`
- `auth_tenant`
- `data`
- `billing_entitlement`
- `integrations`
- `ai_eval`
- `security_privacy`
- `observability_slo`
- `support`
- `rollback`
- `customer_acceptance`

每个 gate 至少包含：

- `id`
- `area`
- `check`
- `evidence_ref`
- `required`
- `result`
- `owner`
- `status`

默认规则：

- `result` 使用 `pass`、`fail`、`blocked`、`not_applicable`、`pending`、`accepted_risk`。
- 外部客户上线不能带着 `required=true` 的 `fail`、`blocked` 或 `accepted_risk` 静默继续；必须有人工 checkpoint。
- `ai_eval` gate 至少链接 W3 eval、red-team、model route 或 W8 quality rollback 工件。
- `customer_acceptance` 记录客户验收证据或明确“尚未验收，不可转生产/付费/公开引用”。
- `rollback` 和 `support` gate 没有证据时，不能上线到付费或生产。

### `customer-onboarding/success-plan/<account>.md`

客户成功计划必须包含：

```markdown
# <account> Success Plan

## Scope

## Stakeholders

## Activation Milestones

## Customer Responsibilities

## Product Responsibilities

## Training / Docs

## Adoption Signals

## Risk Signals

## Support Path

## Expansion / Conversion

## Exit / Offboarding

## Linked Artifacts

## Review Cadence
```

默认规则：

- `Activation Milestones` 写客户第一次看到价值的最短路径，不写产品愿望清单。
- `Adoption Signals` 使用少数可观察信号：首次配置、关键任务完成、活跃席位、集成成功率、人工节省、反馈质量、支持量。
- `Risk Signals` 写早期流失/失败信号：无人登录、关键集成未通、数据质量差、AI 输出被频繁改写、支持卡住、验收延迟。
- `Support Path` 必须链接 W8 客户支持专项支持路径，写清楚响应窗口和升级条件，不口头承诺 24/7。
- `Expansion / Conversion` 必须受 W6 商业承诺专项和 W6 对外声明证据专项约束，不把产品路线图或公开案例写成隐性承诺。

### `customer-onboarding/handoff-review/<account>.md`

上线交接复盘必须包含：

```markdown
# <account> Launch Handoff Review

## Recent Progress

## Success Criteria Result

## Adoption / Usage

## Reliability / Support

## Data / Security / Privacy

## AI Quality / Safety

## Commercial / Billing

## Open Risks

## Decision

## One Next Change

## Review Cadence
```

默认规则：

- `Decision` 只允许明确状态：继续试点、转生产、转付费、延长、暂停、终止、转人工、清理数据、补 gate。
- `One Next Change` 只保留一个下一步，避免客户交付变成无限 backlog。
- 若客户提出自定义功能、特殊 SLA、专属数据处理、公开背书、案例引用或 roadmap 承诺，必须链接 W6 商业承诺专项和 W6 对外声明证据专项。

## 默认流程

1. 开试点前：写 `pilot-charter`，确认成功标准、边界、退出条件和人工 checkpoint。
2. 建租户前：写 `tenant-provisioning`，确认 identity、roles、entitlements、flags、billing、AI/data/integration 边界。
3. 上线前：写 `launch-readiness`，只让人判断 blocker、accepted risk、客户验收、生产/付费切换。
4. 使用中：维护 `success-plan`，跟踪激活、采用、风险和支持路径。
5. 阶段结束：写 `handoff-review`，决定继续、转生产、转付费、终止或清理。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端使用显式 `TenantOnboardingService`、`CustomerLaunchService` 或等价 usecase 管理租户导入、entitlement、feature flag、集成状态和审计事件。
- gRPC API 优先暴露：创建/读取 launch plan、验证 readiness、预检 tenant config、dry-run data import、启停 integration、查询 customer success state。
- gRPC error model 区分：tenant not ready、identity not configured、entitlement missing、integration unverified、data dry-run failed、ai eval gate failed、billing live mode missing、support path missing。
- sqlc 表可选：`customer_launches`、`tenant_provisioning_events`、`tenant_entitlements`、`customer_readiness_gates`、`customer_success_reviews`；只存引用、状态和脱敏摘要。
- 所有客户专属配置必须通过 config/feature flag/entitlement/tenant config 管理，不在 Go 代码里写客户特例。
- 租户上线相关 admin action 必须走 W7 后台运营专项审批、dry-run、rollback 和 audit log。

## Vite 前端默认规则

- 管理台应让操作者看见一个客户上线的最小状态：试点目标、租户配置、readiness gates、支持路径、风险和下一步。
- Vercel Geist 风格用于密集信息：清晰层级、语义色、紧凑表格、可扫描状态，不做营销式 hero。
- 客户可见 onboarding UI 只展示他们需要完成的任务、状态和下一步，不暴露内部 route、prompt、trace、供应商错误或 secret 引用。
- 高风险按钮使用图标、tooltip、confirm、dry-run/result preview；生产启用、数据导入、SSO、计费、AI on customer data 要能看见证据链接。
- 空状态要给出下一步动作，不用大段说明文字占据操作界面。

## AI workflow 默认规则

- 启用客户数据进入 prompt/RAG/memory/tool action 前，必须有 data boundary、provider boundary、eval/refusal/safety gate、human review 或 fallback。
- 客户试点样例进入长期 eval/dataset 前，必须确认授权、脱敏和用途；默认只保存引用和合成/脱敏案例。
- 客户专属 prompt、tool、retrieval source 或 model route 都必须链接 W3 prompt/eval、数据集、红队、模型路由、RAG 和 W8 quality rollback 的相应工件。
- AI 输出用于客户公开材料、案例、承诺或建议时，必须走 W6 对外声明证据专项。

## 需要人判断的关键点

默认不问：

- 文件命名、普通字段完整性、gate 顺序、低风险 internal_trial、空 integration list、无真实数据的 sandbox 测试、普通复盘文案。

必须问：

- 是否把 design partner/private beta 转为 paid pilot 或 production。
- 是否导入真实客户数据、启用数据同步、RAG source、memory、AI tool action 或外部 connector。
- 是否启用 SSO/SCIM、admin impersonation、cross-tenant support、生产 webhook、live billing、客户专属 entitlement。
- 是否接受 `required` gate 的 `fail`、`blocked` 或 `accepted_risk`。
- 是否承诺自定义功能、路线图、SLA、安全/隐私条款、公开案例、客户引用或特定支持窗口。
- 是否在没有 rollback/offboarding/customer acceptance 的情况下上线。
- 是否把客户内容用于 eval、demo、训练、文档或公开材料。

其他章节、字段、敏感信息、OpenSpec 链接、positive/negative fixture 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“为什么试点、租户怎么配、能否上线、客户如何成功、下一步怎么决策”。
- 保留：人只判断生产/付费切换、真实数据、SSO/SCIM、计费、AI 客户数据、accepted risk、合同/公开承诺。
- 调整：不要求客户成功平台、CSM playbook 或企业实施方法论；先用少数 adoption/risk signals。
- 调整：readiness gate 固定 11 类，避免每个客户重新想 checklist。
- 风险：工件可能变成销售/交付笔记。缓解：所有条目必须链接系统证据、阶段工件或明确“不可上线/不可承诺”。

结论：可落地。本专项把客户上线从临时项目变成轻量但可重复的生产变更。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：试点按 outcome 和 adoption 验收，不按客户“感觉不错”验收。
- 工程角度：租户事实、feature flag、entitlement、integration、AI route 都有结构化记录和回滚路径。
- 运维角度：Google SRE 的 launch readiness 被裁剪为客户上线 gate，支持和 rollback 是上线前置条件。
- 安全隐私角度：客户真实数据、身份、secret、AI 数据使用和公开引用都需要边界与人工判断。
- 成本角度：防止一个客户拉出无限定制；`Out Of Scope`、`Exit Criteria` 和 `One Next Change` 保护研发注意力。

结论：可落地。它补上 W1 Discovery 到 W6 Release、W8 Learn 和商业承诺门禁之间的交付路径：知道要验证什么、如何建租户、何时能上线、如何收尾。
