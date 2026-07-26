# 评估

评估把运行后的真实信号或受控 Explore 结果转成一个可问责的判断。运行评估选择继续观察、改进、回滚、停止或维护；Explore 评估记录学习 outcome、证据限制和流程净收益。它不替代调研的 hypothesis owner、交付前验证、实时事故处置或下一轮实现。

## 项目目的与边界

<!-- rule-id: EVALUATION-SCOPE-001 -->
进入评估时先使用本项目的核心入口，再按真实触发条件加载支持/信任运营、AI 质量或其他专项。评估只处理已经出现的用户反馈、指标、生产信号、事故、支持与维护事实，不维护无限 support backlog，也不把每条反馈自动升级成需求；专项仍是可选材料，与本规范的正式分类及项目原则冲突时以正式规范为准。

<!-- rule-id: EVALUATION-SCOPE-002 -->
需要把既有结果沉淀为可恢复上下文、可维护依赖、可信证据或可持续的对外维护边界时进入维护评估。它不继续开发新功能，也不把所有遗留项堆进 backlog；进入维护范围后先读核心入口，仅在触发条件成立时加载知识恢复、依赖/债务、审计证据或开源维护专项。

<!-- rule-id: EVALUATION-SCOPE-007 -->
不进入生产、不会复用且不接触真实数据或真实供应商的一次性实验，以及可自动重建、可丢弃的本地缓存，不进入依赖维护评估。

<!-- rule-id: EVALUATION-SCOPE-008 -->
只有涉及 SLO、告警、runbook、incident、postmortem、toil、发布后 watch 或运维复盘时，才加载 SRE-lite 评估内容；该专项不是运行维护的默认入口。

## 根本原则

- **ITEM-EVALUATION-001**：评估不维护无限待办，也不把每条反馈都变成需求；它应从真实信号中选择一个最高影响的下一步。

## 核心判断

### 信号、结论与下一步

<!-- rule-id: EVALUATION-SIGNAL-001 -->
每次学习判断必须登记实际信号来源。允许的来源包括 support、产品指标、AI telemetry、eval、事故、客户上线、社群、GitHub issue 与人工抽样；只有触发条件出现时才加载相应专项，不能仅凭专项名称制造工作。

<!-- rule-id: EVALUATION-SIGNAL-002 -->
反馈评估覆盖支持消息、用户投诉、退款或 credit 请求、事故反馈、计费/权益困惑、隐私或安全请求及流失信号。它们是待分流的事实，不等同于已确认需求。

<!-- rule-id: EVALUATION-SIGNAL-003 -->
发布后若出现做错问题、质量下降、用户误解承诺或重复支持量，应记录为回流信号并重新判断问题、质量、承诺或自助能力，而不是只修表面症状。

<!-- rule-id: EVALUATION-DECISION-001 -->
每次评估必须从 `continue`、`improve`、`rollback`、`stop`、`maintain` 五个出口中只选一个并记录理由。`continue` 表示信号健康并继续观察，`improve` 表示转入选题至运行中的一个适用改进项目，`rollback` 表示交给发布或运行执行回滚或降级；`stop` 的停止或杀掉决策由 `TOPIC-LEARNING-REASSESSMENT` 权威定义，`maintain` 的维护证据入口由 `VERIFY-EVIDENCE-W8-001-L083` 权威定义，本目标只引用其出口而不复制动作正文。

<!-- rule-id: EVALUATION-DECISION-002 -->
评估产物只保留一个最高影响的下一步，不建立无限 backlog，也不把每条反馈都变成需求。下一步必须足以改变决定、风险或行动顺序；其余观察保留为证据，不冒充已承诺工作。

<!-- rule-id: EVALUATION-DECISION-003 -->
UX review 每轮也只选择一个最高影响改进，避免一人执行者陷入无边界的界面打磨。

### 人工判断边界

<!-- rule-id: EVALUATION-HUMAN-001 -->
涉及用户信任、AI 实际或潜在伤害、误导、歧视、越权、资金、权限、法律、医疗、安全、隐私、退款、公开说明或合同风险时必须记录人的判断。事故通知、状态页、道歉、补偿、refund、credit、合同或权益调整均由人决定，不能由信号或模板自动推出。

<!-- rule-id: EVALUATION-HUMAN-002 -->
是否查看或采样原始 prompt/response、客户数据、支持工单、个人数据或受监管内容必须由人批准；没有批准时只使用脱敏摘要、引用或经过裁剪的样本。

<!-- rule-id: EVALUATION-HUMAN-003 -->
接受 eval 失败或 AI 质量回归、把质量问题定为 `Q-SEV1`/`Q-SEV2`，以及由此触发用户通知、公开说明、退款/补偿或合同 SLA 风险，必须由人明确决定并留下接受、停止、回滚或升级结论。

<!-- rule-id: EVALUATION-HUMAN-004 -->
把支持反馈提升为产品路线、OpenSpec change、公开 bug、安全公告、合同承诺或对外声明修正，属于人工决策，不能由反馈数量自动升级。

<!-- rule-id: EVALUATION-HUMAN-005 -->
以下维护决定必须人审：改变许可证、开源支持边界、security fix window、贡献权利、公开 roadmap、SDK/API 兼容性或维护期限；升级 runtime、framework、数据库或 auth/payment/security/AI provider 的 major version；替换、fork、长期 pin 关键依赖；接受可达漏洞例外、删除弃用对象或改变 AI 行为契约；以及自动化提出的重大升级、破坏性变更、fork/replace 或付费供应商 SDK 替换。

<!-- rule-id: EVALUATION-HUMAN-006 -->
真实可达漏洞的临时例外只能由人接受，并必须记录适用范围、期限、缓解措施和复审点。

<!-- rule-id: EVALUATION-HUMAN-007 -->
哪个文档或工件是 canonical source、术语是否代表真实产品语言、哪些文档可删除/归档/降级为历史，以及高风险变更后是否立即复审知识工件，均需要人的语义判断。

<!-- rule-id: EVALUATION-HUMAN-008 -->
机械性或低风险工作默认由规则直接处理，无需逐项升级给人：命名和字段完整性检查、gate 编排、低风险 `internal_trial`、空 integration list、无真实数据的 sandbox 测试与普通复盘文案；低风险链接、字段顺序、typo、普通 freshness log 和无行为影响的 README 小修同样适用。

### 跨项目回流

<!-- rule-id: EVALUATION-ROUTE-001 -->
上线后出现反馈、质量回归、支持投诉或事故时进入评估；实现阶段的用户/质量/支持信号改变下一步时也先进入评估再重定问题；运行中出现 AI 质量回归或线上输出事故时进入 AI 质量专项。

<!-- rule-id: EVALUATION-ROUTE-002 -->
评估发现新工作优先级时回到[选题](../01-initiation/01-topic-selection.md)；风险边界、合同、安全、成本或信任承诺变化时回到[技术设计](../03-engineering-delivery/05-technical-design.md)；用户可见 AI 行为或输入变化时回到[定义](../02-product-design/03-definition.md)，交互感知变化时回到[体验设计](../02-product-design/04-experience-design.md)，prompt/eval、模型路由、RAG、工具权限或记忆方案变化时回到[技术设计](../03-engineering-delivery/05-technical-design.md)；代码、配置、数据或通知需要修复时回到[实现](../03-engineering-delivery/07-implementation.md)；需要补交付前证据时回到[验证](../03-engineering-delivery/08-verification.md)；发布、回滚、声明更正或客户沟通回到[发布](../03-engineering-delivery/09-release.md)；线上事故、凭据或恢复缺口回到[运行](10-operation.md)。`improve` 必须只选择一条适用路线，不得同时开启多条路线。

<!-- rule-id: EVALUATION-ROUTE-003 -->
维护项变成新产品工作时回到[选题](../01-initiation/01-topic-selection.md)；文档暴露产品语言或成功指标漂移时回到[调研](../01-initiation/02-research.md)或[定义](../02-product-design/03-definition.md)；发布、客户上线、对外声明或合同承诺回到[发布](../03-engineering-delivery/09-release.md)；运行事故、凭据、恢复或生产操作回到[运行](10-operation.md)；支持或质量信号需先在本评估项目完成学习再收尾。

<!-- rule-id: EVALUATION-OUTPUT-001 -->
每个评估工作至少留下一个可追溯评估包：所用信号及脱敏事实、单一决策、一个最高影响下一步，并在命中高风险边界时附人工判断记录。

<!-- rule-id: EVALUATION-OUTPUT-002 -->
每个维护评估工作至少更新一个适用的 canonical 入口；可选入口包括根 `README.md`、四个分类入口、相关项目正文、docs map 或 context pack，并与维护事实、证据或对外边界相互链接。

<!-- rule-id: EVALUATION-ARTIFACT-001 -->
某个 planning 工件若连续两次复盘都没有改变决定、风险或下一步，应合并或删除，避免评估仪式本身成为维护负担。

<!-- rule-id: EVALUATION-EXPLORE-OUTCOME -->
- Explore 结束时记录 `validated | invalidated | revise | stopped | promote`、showcase 观察、证据限制和一个 next；这些结果都不表示产品完成或生产就绪。调研的 question、hypothesis 与产品结论仍由其原始短记录拥有，本评估项目只引用而不复制第二份权威。

<!-- rule-id: EVALUATION-PROCESS-NET-BENEFIT -->
- 评估 Explore 与可选方法时记录 time to first visible fact、process minutes、showcase 次数、active-task 峰值、Superpowers 实际使用及其解决的问题、OpenSpec promote 边界、rework/恢复成本和未覆盖证据。文件数与提交数只作上下文，不能单独证明成功或浪费。

## 重新组织后的规范要求

### 数据可信度、客户结果与外部声明

<!-- rule-id: EVALUATION-DATA-001 -->
定期数据可信度复盘写入 `analytics/data-quality-review/<target>.md`，并完整记录 `Scope`、`Recent Changes`、`Schema Violations`、`Event Volume`、`Missing / Duplicate Events`、`Attribution / Identity`、`Experiment Trustworthiness`、`Dashboard Decisions`、`Privacy Findings`、`Open Risks`、`One Next Change` 与 `Review Cadence`。实验结论只有在该复盘确认对应数据可信时才能作为学习证据。

<!-- rule-id: EVALUATION-CUSTOMER-001 -->
客户使用产品期间维护 `customer-onboarding/success-plan/<account>.md`。标题使用 `<account> Success Plan`，并包含 `Scope`、`Stakeholders`、`Activation Milestones`、`Customer Responsibilities`、`Product Responsibilities`、`Training / Docs`、`Adoption Signals`、`Risk Signals`、`Support Path`、`Expansion / Conversion`、`Exit / Offboarding`、`Linked Artifacts` 与 `Review Cadence`。

<!-- rule-id: EVALUATION-CUSTOMER-002 -->
`Activation Milestones` 只描述客户首次获得价值的最短路径，不写产品愿望清单。`Adoption Signals` 只选少数可观察信号，例如首次配置、关键任务完成、活跃席位、集成成功率、人工节省、反馈质量或支持量。`Risk Signals` 记录无人登录、关键集成未通、数据质量差、AI 输出频繁被改写、支持受阻或验收延迟等早期失败信号；`Support Path` 必须写明响应窗口和升级条件，不口头承诺 24/7。

<!-- rule-id: EVALUATION-CUSTOMER-003 -->
客户阶段结束时维护 `customer-onboarding/handoff-review/<account>.md`。标题使用 `<account> Launch Handoff Review`，并包含 `Recent Progress`、`Success Criteria Result`、`Adoption / Usage`、`Reliability / Support`、`Data / Security / Privacy`、`AI Quality / Safety`、`Commercial / Billing`、`Open Risks`、`Decision`、`One Next Change` 与 `Review Cadence`。

<!-- rule-id: EVALUATION-CUSTOMER-004 -->
handoff 的 `Decision` 是闭集，只能选择：继续试点、转生产、转付费、延长、暂停、终止、转人工、清理数据或补 gate；`One Next Change` 只能保留一个下一步，防止客户交付变成无限 backlog。

<!-- rule-id: EVALUATION-CUSTOMER-005 -->
客户使用中持续用 success plan 跟踪激活、采用、风险与支持路径；阶段结束必须完成 handoff review，再决定继续、转生产、转付费、终止或清理。

<!-- rule-id: EVALUATION-CUSTOMER-006 -->
客户提出自定义功能、特殊 SLA、专属数据处理、公开背书、案例引用或 roadmap 承诺时，必须转入商业承诺与对外声明证据审查；`Expansion / Conversion` 不得把产品路线图或公开案例写成隐性承诺。

<!-- rule-id: EVALUATION-CLAIM-001 -->
每个生产 target 维护 `claim-control/claim-review/<target>.md`。标题使用 `<target> External Claim Review`，并包含 `Recent Surface Changes`、`New / Changed Claims`、`Evidence Gaps`、`Expiring Claims`、`AI / Data / Security Claims`、`SLA / Contract / Billing Claims`、`Developer / API Stability Claims`、`Corrections / Notices`、`Open Risks`、`One Next Change` 与 `Review Cadence`。

<!-- rule-id: EVALUATION-CLAIM-002 -->
pre-revenue 阶段每月复盘一次 claim，且官网、pricing、privacy、AI disclosure、developer docs、support template、合同或 SLA 改动前也要复盘。发现错误承诺、客户投诉、合规问题、供应商政策变化、事故、SLA 偏差或 AI 能力退化时立即复盘，不等待固定周期。

### 支持、投诉与反馈闭环

<!-- rule-id: EVALUATION-SUPPORT-SCOPE-001 -->
支持队列、用户反馈、回复模板、feedback ledger、事故沟通、退款/权益/隐私安全请求和 top contact drivers 触发支持/信任运营专项；未出现这些条件时不加载该专项。

<!-- rule-id: EVALUATION-SUPPORT-001 -->
`support/feedback-ledger/<target>.jsonl` 的每条记录必须包含 `id`、`date`、`source`、`category`、`severity`、`summary`、`evidence`、`customer_impact`、`linked_artifact`、`next_action` 与 `redacted`。证据只保存足以行动的脱敏描述或引用。

<!-- rule-id: EVALUATION-SUPPORT-002 -->
`support/reviews/<target>.md` 必须包含 `Queue Health`、`Top Contact Drivers`、`Root Cause Fixes`、`Product Feedback`、`Docs / Self-Service`、`AI Trust And Safety`、`Risks And Escalations` 与 `Next One Change`。

<!-- rule-id: EVALUATION-SUPPORT-003 -->
pre-revenue 的 support review 默认每两周 30 分钟；有付费用户后默认每周 30 分钟。SEV1/SEV2、退款潮、AI 伤害投诉或安全与隐私请求的紧急复盘触发和当天或次日时限，由 `IMPL-SUPPORT-URGENT-REVIEW-TIMING` 权威定义；本目标只规定常规节奏。

<!-- rule-id: EVALUATION-SUPPORT-004 -->
每次 support review 只选一个最高影响的改进；不得用评估结果建立无法关闭的 support backlog。

<!-- rule-id: EVALUATION-SUPPORT-005 -->
关闭 support case 前必须逐项确认用户影响、临时方案、后续动作以及是否需要复盘；任一项未知时，不得把“已回复”当作已关闭。

<!-- rule-id: EVALUATION-AI-FEEDBACK-001 -->
用户对 AI 输出的纠错和反馈必须进入可查询的 eval、prompt 或 routing 改进闭环，不能只落入不可查询日志。

<!-- rule-id: EVALUATION-AI-FEEDBACK-002 -->
AI 输出投诉优先转成 eval fixture 候选，但只有完成脱敏和裁剪后才可进入候选集；原始客户内容不直接复制到 eval。

<!-- rule-id: EVALUATION-AI-ENFORCEMENT-001 -->
自动化 enforcement 一旦超过 label 或 review，除 notice、appeal 与 audit 外，还必须保留可用于复盘的样本。

### AI 质量、eval 与回归

<!-- rule-id: EVALUATION-AI-SCOPE-001 -->
AI 质量专项只在出现 AI 质量回归、线上 AI 输出事故、质量信号、回滚 runbook、质量 incident log、quality review 或事故样本回流 eval 时加载，并先经评估核心入口判定。它消费 support review、feedback ledger 与 top contact drivers 的脱敏结论，权威工件则是 quality signal contract、incident log、quality review 和学习决策；该专项不是默认流程。

<!-- rule-id: EVALUATION-AI-SCOPE-002 -->
通用可用性、延迟或容量事故不在 AI 质量评估中重复处理，应回到 SRE-lite、成本容量、可观测性或模型路由的权威规则。

<!-- rule-id: EVALUATION-AI-SCOPE-006 -->
完整在线学习、A/B bandit、自动模型训练平台或企业级 MLOps 只有出现真实规模后才单独开 change；一人公司评估不能以建设平台代替处理当前能力的真实质量问题。

<!-- rule-id: EVALUATION-AI-RUNBOOK-001 -->
先把最高影响 AI capability 的质量事故整理为一人可执行的 runbook；不以“大 MLOps 平台”作为开始评估的前置条件。

<!-- rule-id: EVALUATION-AI-SIGNAL-001 -->
每个生产 AI capability 使用 `ai-quality/signal-contract/<capability>.json`，并包含 `capability`、`owner`、`user_journey`、`quality_dimensions`、`leading_signals`、`lagging_signals`、`thresholds`、`eval_links`、`telemetry_links`、`sampling_policy`、`alert_policy`、`rollback_link`、`human_checkpoint`、`review_cadence` 与 `status`。

<!-- rule-id: EVALUATION-AI-SIGNAL-002 -->
`quality_dimensions` 从用户任务成功、事实/引用正确性、结构化输出成功率、安全/拒答合理性、工具调用成功率中选择适用的 2—3 个；不得用一个模糊“质量分”替代可判断维度。

<!-- rule-id: EVALUATION-AI-SIGNAL-003 -->
`leading_signals` 覆盖能较早暴露问题的 eval failure、schema parse failure、tool failure、fallback rate、guardrail spike、latency/cost spike 与人工抽检失败；`lagging_signals` 覆盖真实用户影响，包括 support complaint、thumbs down、task abandonment、refund/churn、人工修正率和关键业务转化下降。

<!-- rule-id: EVALUATION-AI-SIGNAL-004 -->
每个正式阈值必须绑定一个动作，动作闭集为：继续观察、补 eval、关闭 rollout、切 fallback、回滚 prompt/model/route/retrieval/tool 或升级事故。没有动作的阈值只可作为探索信号，不能写成正式门禁。

<!-- rule-id: EVALUATION-AI-SIGNAL-005 -->
每份 quality signal contract 至少同时包含一个离线 eval 信号和一个线上用户或生产信号；只看 eval 或只看投诉都不足以支持质量结论。

<!-- rule-id: EVALUATION-AI-REVIEW-001 -->
`ai-quality/quality-review/<capability>.md` 以 `<capability> AI Quality Review` 为标题，并包含 `Recent Changes`、`Signal Health`、`Eval / Dataset Drift`、`User Feedback / Support`、`Incidents / Regressions`、`False Positives / Noise`、`Rollback Readiness`、`Open Risks`、`One Next Change` 与 `Review Cadence`。

<!-- rule-id: EVALUATION-AI-REVIEW-002 -->
有活跃用户的核心 AI capability 每两周复盘一次；早期或低风险能力每月复盘一次。

<!-- rule-id: EVALUATION-AI-REVIEW-003 -->
每次 AI quality review 只选一个最高影响改进：新增一个 eval 类别、修一个 top regression、降低一个噪声告警、增加一个 rollback 验证或改一个用户提示。目标是稳定质量定义、检测、止血和学习闭环，而不是追求抽象的“把模型调到最好”。

<!-- rule-id: EVALUATION-AI-STORAGE-001 -->
可选的 `ai_quality_signals`、`ai_quality_incidents`、`ai_quality_actions` 与 `ai_quality_reviews` 表只保存引用和摘要，不保存敏感原文。

<!-- rule-id: EVALUATION-AI-ROLLBACK-001 -->
生产 AI 回滚由 config、feature flag 或 model route 控制；不得在业务代码中临时改 model name 或 prompt 字符串来冒充可审计回滚。

<!-- rule-id: EVALUATION-AI-INCIDENT-001 -->
AI 质量学习既要吸收线上任务失败、事故复盘和用户对输出的投诉，也要吸收 eval、schema、tool、retrieval、fallback 及其他回归信号；实时止血仍归运行，评估只负责把这些事实转成质量结论与下一轮输入。

## 按主题整理的执行细则

### 运营动作、异步任务与复盘

<!-- rule-id: EVALUATION-ASYNC-001 -->
异步任务使用 `async-jobs/operations-review/<target>.md` 复盘，字段为 `Recent Changes`、`Backlog / Latency`、`Failures / Retries`、`Dead Letters / Replays`、`Cancellation / Expiry`、`Cost / Capacity`、`User Impact`、`Incidents`、`Open Risks` 与 `Next One Change`。

<!-- rule-id: EVALUATION-ASYNC-002 -->
未收费或低流量阶段每月复盘一次，或在新增 job type、schedule、worker、vendor batch 前复盘；已有活跃用户时每两周复盘，发生 backlog SLO 失守、dead letter、批处理失败、重复副作用、成本异常或用户投诉时立即复盘。

<!-- rule-id: EVALUATION-ASYNC-003 -->
每次异步任务复盘只选一个最高影响改进，可从 queue latency、cancellation、retry、dead letter、idempotency、concurrency、拆分大任务、用户状态 UI 或 managed queue 中选择；其余保留为风险，不同时启动。

<!-- rule-id: EVALUATION-ADMIN-001 -->
人工生产动作使用 `admin-ops/ops-review/<target>.md`，字段为 `Recent Actions`、`High Risk Actions`、`Failed / Aborted Actions`、`Audit Gaps`、`Permission Drift`、`Toil To Automate`、`AI Autonomy Review` 与 `Next One Change`。

<!-- rule-id: EVALUATION-ADMIN-002 -->
存在人工生产动作的目标按周或每两周复盘一次。

<!-- rule-id: EVALUATION-ADMIN-003 -->
同类人工动作重复达到 2 次时，必须明确选择产品修复、文档修复、受控 admin action、自动化或显式不处理，并记录依据；不得继续以临时脚本维持默认流程。

<!-- rule-id: EVALUATION-ADMIN-004 -->
每次人工生产动作复盘只推进一个改进：dry-run、audit、permission、删除危险脚本、runbook 或 automation，按风险和重复成本排序。

<!-- rule-id: EVALUATION-TOIL-001 -->
同时具备人工执行、重复发生、可自动化且工作量随使用量线性增长的任务应计为 toil；只恢复现状而没有永久改进，或持续打断开发却不增加产品价值与可靠性的工作，也应进入评估。

<!-- rule-id: EVALUATION-TOIL-002 -->
每周只选择一个影响最大的 toil 改进。目标是避免 toil 持续吞噬开发时间，不是追求零 toil，也不建立无法完成的自动化清单。

<!-- rule-id: EVALUATION-POSTMORTEM-001 -->
事故恢复后按 SRE-lite 的触发条件完成轻量 postmortem；评估接收事故事实与证据，不延迟实时止血，也不另建平行事故流程。

<!-- rule-id: EVALUATION-POSTMORTEM-002 -->
postmortem 至少包含 `Root Causes And Trigger`、`What Went Well`、`What Went Poorly` 与 `Action Items`；存在用户可见影响时必须量化，无法精确计量也要给出有依据的估算。

<!-- rule-id: EVALUATION-POSTMORTEM-003 -->
行动项表使用 `Action | Type | Owner | Due | Tracking`，至少有一项具备 owner、due 和 tracking，且总数最多三项；未进入跟踪系统的愿望不算行动项。

<!-- rule-id: EVALUATION-POSTMORTEM-004 -->
复盘必须无责，聚焦系统条件、触发因素和缺失控制，不以个人过错或追责叙事替代根因分析。

<!-- rule-id: EVALUATION-SECURITY-REVIEW-001 -->
安全事故使用 `security-incidents/post-incident-review/<target>.md`，标题为 `<target> Security Post-Incident Review`，并包含 `Summary`、`Impact`、`Detection`、`Timeline`、`Root Causes And Trigger`、`Response`、`Evidence Preserved`、`Notifications`、`Remediation`、`Lessons`、`Action Items` 与 `Review Cadence`。

<!-- rule-id: EVALUATION-SECURITY-REVIEW-002 -->
安全事故复盘保持无责、事实化且可审计，描述控制与系统如何失效，不写“谁犯了错”。

<!-- rule-id: EVALUATION-SECURITY-REVIEW-003 -->
安全复盘不得生成无人执行的长行动清单；只保留与根因、暴露面和复发风险直接相关的必要改进。

<!-- rule-id: EVALUATION-BREAKGLASS-001 -->
任何 R4 break-glass 动作结束后都必须进入事后复盘，核对必要性、授权、范围、审计证据、恢复状态与后续控制。

<!-- rule-id: EVALUATION-CREDENTIAL-001 -->
API key、service account、webhook secret、TLS/private key、OpenAI 或其他 provider key、CI/OIDC 等凭据一旦暴露，复盘必须覆盖影响范围、使用痕迹、撤销轮换和复发控制。

<!-- rule-id: EVALUATION-CREDENTIAL-002 -->
凭据轮换后的行动项最多三项，优先处理能减少再次暴露或缩短发现与撤销时间的控制。

<!-- rule-id: EVALUATION-CREDENTIAL-003 -->
Git 历史清理不是凭据暴露的第一动作；必须先撤销旧凭据，再评估影响并处理复发原因，历史清理只能作为后续风险降低措施。

### 依赖、升级与维护评估

<!-- rule-id: EVALUATION-MAINT-SCOPE-005 -->
依赖维护是经本评估规范触发的可选专项，最小工件包括 dependency inventory、update policy、`maintenance/upgrade-plans/<target>.md`、debt register 与 `maintenance/deprecation-plans/<target>.md`，并统一使用同一个 `<target>` 文件名、定义长期维护节奏。运行时、框架、外部 AI SDK、model route、prompt/tool/eval workflow、GitHub Actions、Docker、数据库 migration 工具及 observability/security/release 供应商出现维护信号时才加载；同一 target 的别名必须归并，不能制造重复台账。

<!-- rule-id: EVALUATION-DEPENDENCY-001 -->
依赖盘点使用 `maintenance/dependency-inventory/<target>.json`，顶层字段为 `target`、`owner`、`stack`、`package_managers`、`manifests`、`lockfiles`、`generated_artifacts`、`critical_dependencies`、`runtime_versions`、`update_channels`、`security_scanning`、`dependency_automation`、`human_checkpoint` 与 `review_cadence`。

<!-- rule-id: EVALUATION-DEPENDENCY-002 -->
`critical_dependencies[]` 每项包含 `name`、`ecosystem`、`role`、`version_source`、`update_policy`、`risk`、`upstream_source` 与 `rollback`，以便把升级风险和恢复路径绑定到真实依赖。

<!-- rule-id: EVALUATION-DEPENDENCY-003 -->
`critical_dependencies` 默认列入 Go runtime、Kratos、grpc-go、protobuf、sqlc、migration 工具、MySQL driver、Vite、React/路由/状态库、OpenAI 或其他 AI SDK、auth provider SDK、payment/email/storage/observability SDK，以及 GitHub Actions runner/tooling。

<!-- rule-id: EVALUATION-UPDATE-001 -->
依赖更新策略使用 `maintenance/update-policy/<target>.md`，至少包含 `Scope`、`Supported Toolchains`、`Update Cadence`、`Security Updates`、`Batch Strategy`、`Verification Gates`、`Rollback` 与 `Human Checkpoints`。

<!-- rule-id: EVALUATION-UPDATE-002 -->
安全更新在一个工作块内完成 triage，可达、高危或面向公网的风险优先；普通 patch/minor 默认按月或维护窗口处理，除非安全、兼容性或成本信号要求提前，安全处置不得被普通版本节奏拖延。

<!-- rule-id: EVALUATION-UPDATE-003 -->
自动化只能提出依赖更新建议；major、breaking change、fork、replace 或付费 SDK 变更必须由人确认影响、验证门禁和回滚后再合并。

<!-- rule-id: EVALUATION-UPGRADE-001 -->
具体升级使用 `maintenance/upgrade-plans/<target>.md`，评估负责 `Scope`、`Trigger`、`Compatibility Notes`、`Steps`、`Generated Code`、`Release Strategy`、`Rollback` 与 `Decision Log`；`Test / Eval Matrix` 由验证权威提供并在同一计划中引用，不能由评估臆造。

<!-- rule-id: EVALUATION-UPGRADE-002 -->
没有待处理 major upgrade 时，upgrade plan 必须明确写“暂无待升级项”和下一次复审日期，不能用空文件表示已检查。

<!-- rule-id: EVALUATION-UPGRADE-003 -->
Go 依赖安全评估使用 `govulncheck` 或等价工具并优先处理可达漏洞；升级不得顺带改变协议，sqlc 等生成代码的差异只能由对应生成工具产生。

<!-- rule-id: EVALUATION-UPGRADE-004 -->
使用 replace、exclude、fork 或 private module 时，必须记录原因、到期复查时间和退出路径，避免临时绕行成为永久依赖策略。

<!-- rule-id: EVALUATION-UPGRADE-005 -->
仓库选定的 lockfile 必须入库；`npm audit` 或等价安全审计属于 release/security gate，不得把 `audit fix --force` 设为默认自动操作。

<!-- rule-id: EVALUATION-AI-UPGRADE-001 -->
AI SDK、model route、prompt builder、tool schema、eval dataset 或 guardrail 的变化都属于行为契约变更，必须按用户可见风险评估，不能降格为普通依赖 bump。

<!-- rule-id: EVALUATION-AI-UPGRADE-002 -->
AI 升级前记录成本、延迟和 fallback 基线；eval baseline 由 `VERIFY-AI-EVAL-FIXTURE-W9-003-L182` 提供，升级后的代表性、边界与失败样例比较由 `VERIFY-AI-UPGRADE-COMPARISON` 提供。评估引用这些验证证据形成升级决定，不自行建立竞争的比较口径或无来源的强制暂停与回滚规则。

<!-- rule-id: EVALUATION-AI-UPGRADE-003 -->
AI 升级理由必须说明预期产品结果、主要风险与成本影响；“新模型更强”不能单独构成升级依据。

<!-- rule-id: EVALUATION-DEPRECATION-001 -->
弃用计划使用 `maintenance/deprecation-plans/<target>.md`，包含 `Scope`、`Deprecated Surface`、`Consumers`、`Migration Path`、`Compatibility Window`、`Observability`、`Removal Steps`、`Rollback` 与 `Human Checkpoints`。

<!-- rule-id: EVALUATION-DEPRECATION-002 -->
可进入弃用评估的对象包括但不限于 API、gRPC method、DB field、config item、feature flag、AI prompt/model route、CLI、webhook、frontend route 与 third-party provider；这是一组可选表面，不构成封闭枚举。

<!-- rule-id: EVALUATION-DEPRECATION-003 -->
任何 surface 都必须记录 `deprecation`，compatibility policy 也必须记录 `Deprecation`；两者都要进入计划，说明消费者、迁移路径、兼容窗口和观测依据，公告本身不等于迁移完成。

<!-- rule-id: EVALUATION-DEPRECATION-004 -->
删除已弃用接口、配置、feature flag、prompt 或 model route 前必须由人确认消费者已迁移、回滚可用且观察窗口满足要求。

<!-- rule-id: EVALUATION-DEBT-001 -->
技术债登记在 `maintenance/debt-register/<target>.jsonl`，每行包含 `id`、`date`、`target`、`area`、`type`、`source`、`symptom`、`impact`、`interest`、`owner`、`status`、`planned_action`、`review_on` 与 `linked_change`。

<!-- rule-id: EVALUATION-DEBT-002 -->
`status` 只能取 `accepted`、`planned`、`in_progress`、`paid_down`、`closed` 或 `superseded`，不得用自由文本制造隐形状态。

<!-- rule-id: EVALUATION-DEBT-003 -->
技术债必须写清持续利息。TODO、FIXME、HACK、临时 workaround、skipped test、disabled lint、长期 flag 或 deprecated API 必须登记，或说明为何不构成债；只有影响未来变更、可靠性、安全、成本或 AI 行为的事项进入台账，普通代码洁癖不进入。

<!-- rule-id: EVALUATION-DEBT-004 -->
技术债从 `accepted` 转为长期 `planned`，或决定继续延期时，必须由人确认利息、优先级、复查时间和显式取舍。

### 知识、新鲜度与上下文恢复

<!-- rule-id: EVALUATION-KNOWLEDGE-SCOPE-004 -->
知识维护是经本评估规范触发的可选专项，覆盖 docs map、context pack、glossary、how-to、freshness log、canonical entrypoint 与上下文恢复。只有服务、前端、AI workflow、data schema、SLO/runbook、release、security、product discovery 等事实需要长期恢复，或术语、命令、常见任务与排障入口会跨项目复用时才加载；持续一周以上的 product bet，以及架构、安全、数据或 AI 高风险变更也必须建立可恢复上下文。

<!-- rule-id: EVALUATION-KNOWLEDGE-SCOPE-007 -->
可丢弃的一次性实验、可由权威源重新生成且不承担 canonical 入口的 API reference，以及归档后不再需要的临时 OpenSpec 讨论，均不进入长期知识维护。

<!-- rule-id: EVALUATION-KNOWLEDGE-QUALITY-001 -->
文档必须随仓库存在，并能让下一位执行者找到一个明确的下一动作；没有入口、owner 或 review 机制的文档集合不能判定为可恢复知识。

<!-- rule-id: EVALUATION-KNOWLEDGE-ENTRY-001 -->
最小知识工件统一位于 `governance/knowledge/`：docs map 使用 `docs-map/<target>.json`，context pack 使用 `context-packs/<target>.md`，其余分别使用 `glossary/<target>.md`、`how-to/<target>.md` 与 `freshness/<target>.jsonl`；不得在其他位置创建同义的第二套入口。

<!-- rule-id: EVALUATION-GOV-MAP-001 -->
Standard/High-risk 项目的统一治理入口由四部分构成：`governance/README.md` 提供治理说明，`governance/project-map.json` 提供项目映射，`governance/current-status.json` 记录当前状态，专项工件落在 `governance/<registered-domain>/`；根 `README.md` 必须链接上述三个文件，使执行者无需猜测当前状态与阅读顺序。

<!-- rule-id: EVALUATION-GOV-MAP-002 -->
`governance/project-map.json` 说明全部顶层目录、正式源码与过程证据、推荐阅读顺序、运行进程、常用命令和权威来源；每个 governance domain 记录 `trigger`、`owner`、`decision_or_gate` 与 `retention`。guard 提供旧根目录路径时，必须重映射到 `governance/<registered-domain>/`。

<!-- rule-id: EVALUATION-DOCSMAP-001 -->
docs map 写入 `governance/knowledge/docs-map/` 目录，文件名为 `<target>.json`；顶层字段为 `target`、`owner`、`audiences`、`canonical_entrypoints`、`diataxis_coverage`、`context_pack`、`glossary`、`how_to`、`linked_openspec_changes`、`linked_runtime_artifacts`、`freshness_policy`、`human_checkpoint` 与 `review_cadence`。

<!-- rule-id: EVALUATION-DOCSMAP-002 -->
docs map 的 `canonical_entrypoints[]` 每项包含 `title`、`path`、`type`、`audience`、`owner`、`review_on` 与 `stale_after_days`；`type` 只能取 `tutorial`、`how_to`、`reference`、`explanation`、`runbook`、`spec`、`adr` 或 `context_pack`。

<!-- rule-id: EVALUATION-CONTEXT-001 -->
context pack 写入 `governance/knowledge/context-packs/` 目录，文件名为 `<target>.md`；正文包含 `Mission`、`Current Product Bet`、`System Shape`、`Key Commands`、`Data/Auth/Cost/Security Boundaries`、`AI Behavior`、`Operational Links`、`Current Risks`、`Open Decisions` 与 `Handoff Prompt`；其中 `Open Decisions` 的权威字段合同由 `PLAN-CONTEXT-PACK-OPEN-DECISIONS` 提供。

<!-- rule-id: EVALUATION-CONTEXT-002 -->
context pack 默认控制在 200 行以内，只链接 canonical source，不复制长段规范、日志或运行证据；内容过长时先删除重复部分，并保留恢复任务所需的最短路径。

<!-- rule-id: EVALUATION-CONTEXT-003 -->
`Handoff Prompt` 应足够简短并可直接复制，至少说明目标、当前状态、不可越过的边界和下一步，不能把整个 context pack 重复一遍。

<!-- rule-id: EVALUATION-GLOSSARY-001 -->
glossary 使用 `governance/knowledge/glossary/<target>.md`，字段为 `Domain Terms`、`Bounded Context Language`、`API Names`、`Data Names`、`AI Terms` 与 `Avoided Terms`，只保留真实使用的产品语言。

<!-- rule-id: EVALUATION-HOWTO-001 -->
how-to 使用 `governance/knowledge/how-to/<target>.md`，包含 `Setup`、`Develop`、`Test`、`Run Locally`、`Release`、`Rollback`、`Debug` 与 `Update Knowledge`，每节都指向可执行命令或 canonical 说明。

<!-- rule-id: EVALUATION-FRESHNESS-001 -->
发布、事故、安全变更、schema migration、AI workflow 调整或 product pivot 后，必须向 `governance/knowledge/freshness/<target>.jsonl` 追加来源登记与复审结果；新鲜度以 source registry 为准，不以文件最近修改时间代替。

<!-- rule-id: EVALUATION-AI-FRESHNESS-001 -->
AI context source 没有明确 freshness 信息时，不得作为默认模型上下文注入；只能显式选择，并向使用者标明可能过期。

<!-- rule-id: EVALUATION-DIATAXIS-001 -->
docs map 必须说明 Diátaxis 覆盖：tutorial 仅用于外部插件、SDK、CLI 或复杂 onboarding；生产操作必须有 how-to；API、配置、schema、事件、flag 与 telemetry 必须链接 reference；架构、product bet、AI 与安全边界使用 explanation 或 ADR。

<!-- rule-id: EVALUATION-RECOVERY-001 -->
恢复上下文时按五步顺序读取：根 `README.md`；治理说明 `governance/README.md`、项目映射 `governance/project-map.json` 和当前状态 `governance/current-status.json`；`governance/knowledge/docs-map/` 目录中的 `<target>.json`；`governance/knowledge/context-packs/` 目录中的 `<target>.md`；最后读取当前 OpenSpec change、相关 skill 和具体 artifact。第二步的三入口合同由 `PLAN-CODEX-HANDOFF-FIRST-READS` 提供；遇到冲突时回到 canonical source，不靠聊天记录猜测。

<!-- rule-id: EVALUATION-DOCS-STYLE-001 -->
事实与流程用中文，命令、路径、API 和字段名保留英文；文档开头说明目标、范围与最近复审时间。明显冗长的解释应删除，并链接 canonical source。

<!-- rule-id: EVALUATION-DOCS-SECURITY-001 -->
知识工件不得包含 secret、private key、PII、完整 prompt/response 或生产凭据；需要证明事实时只保存脱敏摘要和受控证据引用。

<!-- rule-id: EVALUATION-DOCS-SYNC-001 -->
OpenSpec、release、incident、migration 或 config 改变长期事实时，必须在同一工作中更新对应文档入口和 freshness 记录，不能把同步留给未登记的以后。

<!-- rule-id: EVALUATION-W9-EXIT-001 -->
结束维护评估前必须能回答下一位执行者先读哪里、哪些内容是 canonical、哪些仅是历史，以及本次维护是否向其他研发项目暴露了新风险；不能回答时尚未完成收尾。

<!-- rule-id: EVALUATION-W9-EXIT-002 -->
维护评估结论只能取 `archive`、`refresh`、`maintain`、`evidence` 或 `new-work`，并记录所更新入口；选择 `new-work` 时必须先回到[选题](../01-initiation/01-topic-selection.md)建立下一项工作，再由该入口决定后续路由。

<!-- rule-id: EVALUATION-EVIDENCE-001 -->
审计证据维护必须连接 evidence review 与 evidence package、customer/auditor evidence、audit evidence、retention 及 audit log policy，并明确脱敏、完整性与导出边界；一旦要为真实客户或审计方导出证据包，必须另开 OpenSpec change 明确范围、授权和披露控制。

<!-- rule-id: EVALUATION-OSS-001 -->
公开仓库、SDK、CLI、template、MCP server 与 example 的维护评估必须明确许可证、community health、贡献策略、支持范围、安全报告与 advisory 路径、release/security review、兼容承诺、maintainer boundary 以及归档或暂停条件；任何变化先按人工判断边界确认，再同步公开说明与发布工件。

## 输入与产物

评估输入来自已脱敏的用户反馈、产品与 AI 指标、eval 结果、支持记录、事故证据、运行复盘、客户上线事实、依赖清单、技术债、文档入口和 freshness 登记，也可以链接一份受控 Explore canonical record。输入不足时只允许形成“继续观察”、revise、stopped 或补证据动作，不得伪造确定结论。

## 完成、停止或退出条件

完成运行评估时必须留下可追溯的信号、单一决策、一个最高影响下一步、适用的人工判断，以及更新后的 canonical 入口。完成 Explore 评估时必须留下真实 outcome、showcase 观察、证据限制、流程净收益和一个 next；只有 `promote` 才进入 Deliver 重新路由。需要实时止血、交付前验证、新功能实现或对外承诺时，按上文路由交回相应权威流程；完成路由即停止继续扩张本轮评估。

## 相关项目引用

- 问题与优先级变化回到[选题](../01-initiation/01-topic-selection.md)；产品信号定义回到[调研](../01-initiation/02-research.md)或[定义](../02-product-design/03-definition.md)。
- 风险、合同、安全、成本和信任边界回到[技术设计](../03-engineering-delivery/05-technical-design.md)；用户可见 AI 行为或输入回到[定义](../02-product-design/03-definition.md)，交互感知回到[体验设计](../02-product-design/04-experience-design.md)，prompt/eval 等 AI 技术方案回到技术设计。
- 实现修复回到[实现](../03-engineering-delivery/07-implementation.md)；交付前证据回到[验证](../03-engineering-delivery/08-verification.md)；发布、回滚和客户沟通回到[发布](../03-engineering-delivery/09-release.md)；实时事故处置回到[运行](10-operation.md)。
- OpenSpec 是 Standard/High-risk 变更的过程权威；本规范只消费其已批准事实，不替代提案、任务或归档。
