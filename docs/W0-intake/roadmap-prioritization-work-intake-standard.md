# 路线图、工作入口与研发优先级规范

## W0 定位

本文件是 W0 Intake 的核心规范。它负责判断一件事是否应该占用当前研发注意力，并定义 intake、decision board、roadmap、focus review 的最小治理方式。

其它工作不要在本文件里展开：产品证据进入 W1，OpenSpec 和风险边界进入 W2，AI 行为进入 W3，实现进入 W4，验证进入 W5，发布进入 W6，运行事故进入 W7，学习回流进入 W8，知识维护进入 W9。

## 场景触发规范

- 产品机会、增长实验、用户问题不清：进入 `docs/W1-discovery/product-discovery-feedback-loop-standard.md`。
- 需要采集指标、埋点或做实验：进入 `docs/W1-discovery/product-analytics-experiment-standard.md`。
- 工作会影响生产、数据、安全、成本、AI 行为或超过 30 分钟：进入 `docs/W2-openspec-risk/01-one-person-ai-rd-operating-model.md`。
- 支持反馈、投诉、退款、信任请求进入：参考 `docs/W8-learn/23-customer-support-trust-ops-standard.md`。
- 客户试点、租户交付、真实客户上线进入：参考 `docs/W6-release/49-customer-pilot-onboarding-launch-standard.md`。
- 安全/隐私事故、漏洞、凭据泄露进入：先走 `docs/W7-operate/44-security-privacy-incident-vulnerability-standard.md`，事后再回到 W0 复盘。
- AI 质量回归或线上行为漂移进入：先走 `docs/W8-learn/48-ai-quality-regression-incident-standard.md`，事后再回到 W0 决定下一步。
- 文档、索引、依赖、维护类请求进入：参考 `docs/W9-maintain/16-knowledge-context-recovery-standard.md` 或 `docs/W9-maintain/17-maintenance-dependency-debt-standard.md`。

## 目标

一人公司最常见的研发失控不是没有想法，而是想法、客户请求、bug、技术债、安全事项、AI 质量问题、增长实验和基础设施改造同时涌进来，最后每件事都“有道理”，但当前焦点被切碎。

本规范负责把研发入口做成一个可恢复的选择系统：所有请求先进入 intake，只有少数进入当前 focus；路线图用 Now / Next / Later 表达不确定性；每次复盘只做有限决策：开始、延后、停车、杀掉、补证据，或升级为 W1 产品 bet / W2 OpenSpec change。

默认原则：**一人公司不维护无限 backlog，只维护当前选择、下一批候选、明确拒绝/停车的理由和复盘节奏。** 没有证据、appetite、风险边界和下一步的请求，不进入研发。

## 核心依据

- 《人月神话》：概念完整性来自少数清晰判断；把所有请求都并行推进会增加协调成本，而不是增加产能。
- 小型项目管理：小项目管理的价值在于明确范围、责任、节奏和停止条件；不要把工具和仪式误当管理。
- Good Strategy / Bad Strategy：好策略需要诊断、指导方针和连贯行动；路线图不能只是功能清单。
- Escaping the Build Trap：产品组织容易用输出代替结果；一人公司也会陷入“多发功能等于进步”的陷阱。
- Shape Up：用 appetite 约束方案，用 fixed time / variable scope 控制风险；原始想法先 soft no，不进入无限 backlog；赌注需要边界和停止机制。
- Continuous Discovery / Opportunity Solution Tree：机会、方案和实验要连接到目标结果，避免从解决方案列表直接跳进实现。
- Now / Next / Later Roadmap：路线图应表达不确定性，越远越少承诺，避免把未来想法写成客户可依赖日期。
- RICE：reach、impact、confidence、effort 可帮助比较候选，但分数只是讨论输入，不是自动决策。
- DORA Working in Small Batches / Trunk-Based Development：小批量让假设更快得到反馈，也降低返工和合并风险。
- Google SRE Dealing with Interrupts / Eliminating Toil：中断会破坏专注时间；interrupt、toil、项目工作要分开处理，并定期分析根因。
- GitHub Projects / Issue Templates / Linear Triage：入口模板、元数据、triage 状态和项目视图能减少低质量请求和重复上下文。

## 范围

适用对象：

- 新功能、AI workflow、增长实验、客户请求、设计伙伴反馈、支持反馈、bug、可靠性改进、安全隐私事项、合规证据、技术债、开发者体验、开源维护、成本优化。
- 会占用超过半天、改变用户可见行为、改变数据/安全/计费/合同边界，或会产生新 OpenSpec change 的工作。
- 从日常想法、issue、support ticket、客户会议、事故复盘、eval 失败、成本异常到 roadmap 候选的入口治理。

不适用对象：

- 具体产品 bet 的用户、问题、指标、实验和学习决策；走 W1。
- 具体实现批次、AI 编码、自审和验证；走 W4。
- 事故响应、紧急止血和安全漏洞披露；走 W7/W8，事后再回到 W0。
- 客户上线的 launch readiness；走 W6。
- 完整 OKR、企业 PMO、跨团队资源管理或年度预算系统；一人公司先不做。

## 最小工件

每个计划周期使用 `<period>`，例如 `2026-q3`、`2026-07` 或 `current`。每个入口请求使用 `<work-id>`，例如 `wk-ai-export-001`。

```text
planning/
  strategy-map/<period>.md
  work-intake/<work-id>.json
  decision-board/<period>.json
  roadmap/<period>.md
  focus-review/<period>.md
```

### `planning/strategy-map/<period>.md`

战略地图必须包含：

```markdown
# <period> Strategy Map

## Scope

## Diagnosis

## North Star Outcome

## Target Segment

## Guiding Policy

## Strategic Bets

## Constraints

## Non Goals

## Risk Appetite

## Capacity Budget

## Human Checkpoints

## Linked Artifacts

## Review Cadence
```

默认规则：

- `Diagnosis` 写当前最重要的约束或机会，不写愿景口号。
- `North Star Outcome` 只保留一个周期内最重要的结果，和 W1 的产品发现、指标和实验连接。
- `Guiding Policy` 说明为什么这些工作值得做、哪些请求默认不做。
- `Capacity Budget` 默认分三类：focus work、maintenance/risk、interrupt buffer。没有真实运营压力前，不给 interrupt 留过大预算。
- `Non Goals` 是保护注意力的核心；明确不做哪些用户、渠道、平台、集成、商业承诺或重构。

### `planning/work-intake/<work-id>.json`

工作入口必须包含：

- `id`
- `title`
- `source`
- `request_type`
- `target_user_or_system`
- `problem`
- `evidence_refs`
- `value_hypothesis`
- `risk_or_obligation`
- `appetite`
- `expected_scope`
- `non_goals`
- `dependencies`
- `required_artifacts`
- `human_checkpoint`
- `status`
- `review_by`

`request_type` 使用：

- `product_bet`
- `customer_request`
- `bug`
- `reliability`
- `security_privacy`
- `compliance`
- `tech_debt`
- `platform`
- `ai_quality`
- `cost`
- `docs`

默认规则：

- `source` 写入口来源：support、customer-onboarding、incident、eval、analytics、cost review、security review、personal idea、market signal。
- `problem` 必须描述具体痛点、风险或义务，不写“做一个 X”。
- `appetite` 必须先写时间/精力预算，再决定 scope；超过 2 周默认需要拆分或阶段性验证。
- `required_artifacts` 写进入下一步前需要的工件，例如 product bet、OpenSpec、eval、threat model、release gate、customer launch gate。
- `status` 使用 `new`、`needs-evidence`、`shaping`、`ready-for-decision`、`accepted`、`parked`、`killed`、`done`。

### `planning/decision-board/<period>.json`

决策板必须包含：

- `period`
- `owner`
- `capacity`
- `decision_policy`
- `work_items`
- `human_checkpoint`
- `review_cadence`
- `status`

`capacity` 至少包含：

- `focus_slots`
- `maintenance_slots`
- `interrupt_buffer`

`work_items` 每项至少包含：

- `id`
- `lane`
- `decision`
- `request_type`
- `appetite`
- `evidence_strength`
- `urgency`
- `risk_reduction`
- `value`
- `effort`
- `confidence`
- `score_summary`
- `linked_artifacts`
- `next_review`
- `human_checkpoint`
- `status`

`lane` 使用 `now`、`next`、`later`、`parked`、`killed`、`expedite`、`maintenance`。

`decision` 使用 `start_now`、`schedule_next`、`shape`、`needs_evidence`、`park`、`kill`、`expedite`、`done`。

默认规则：

- `now` lane 默认最多 2 个：一个主要 focus，一个维护/风险项目。超过 2 个必须人工判断。
- `expedite` 只用于事故、安全、严重客户影响或硬性合规截止；不能把普通客户请求伪装成 expedite。
- RICE 或类似分数只能作为 `score_summary`，不能自动推翻战略约束、数据边界、安全风险或人的精力上限。
- `evidence_strength` 使用 `none`、`weak`、`directional`、`strong`。`none` 的产品功能默认不能 start_now，除非显式接受风险。

### `planning/roadmap/<period>.md`

路线图必须包含：

```markdown
# <period> Roadmap

## Scope

## Now

## Next

## Later

## Parked / Killed

## Explicit Non Commitments

## Customer / Public Claim Boundary

## Dependencies

## Evidence Links

## Change Log

## Review Cadence
```

默认规则：

- `Now` 可以写具体解决方案和 OpenSpec change。
- `Next` 优先写机会、风险或待 shaping 的问题，不提前承诺具体方案。
- `Later` 优先写目标结果或开放机会，不写客户可依赖交付日期。
- `Explicit Non Commitments` 写清楚尚未承诺的功能、平台、集成、SLA、路线图日期、客户定制和公开声明。
- 任何会进入销售材料、官网、客户邮件、合同或公开 roadmap 的内容，必须链接 W6 的商业承诺或对外声明门禁。

### `planning/focus-review/<period>.md`

焦点复盘必须包含：

```markdown
# <period> Focus Review

## Recent Work

## Shipped / Learned

## Incoming Requests

## Active Now Slots

## Capacity / Energy

## Decisions Made

## Stopped / Parked

## Risks

## One Next Change

## Review Cadence
```

默认规则：

- 每周或每两周复盘一次；复盘目标不是重排所有 backlog，而是确认当前焦点是否仍正确。
- `Incoming Requests` 只看新增高影响请求、expedite、重复中断和即将过期的 review_by。
- `Stopped / Parked` 必须记录停止理由，防止以后重新讨论时丢上下文。
- `One Next Change` 只写一个最高影响的系统改进：补模板、自动检查、拆 scope、更新路线图、创建 OpenSpec 或拒绝一个方向。

## 默认流程

1. 新请求先写 `work-intake`，不要直接加入路线图。
2. 每周或每两周更新 `decision-board`，把请求放入 now、next、later、parked、killed、maintenance 或 expedite。
3. 只有 `now` 和 `expedite` 能消耗当前专注时间。
4. 产品类 `start_now` 之前，链接 W1 的 bet/metrics/experiment；生产实现之前，链接 W2 OpenSpec change。
5. 路线图只同步已决策的 now/next/later，不把未塑形想法伪装成承诺。
6. `focus-review` 收尾时更新 one next change，并关闭或停车不再追踪的请求。

## Go / Kratos / sqlc / gRPC 默认规则

- 只有当 planning 状态需要进入产品内管理台、客户控制台或自动化流程时，才实现 `PlanningService` 或等价 backend；默认先 docs-as-code。
- gRPC API 可选：CreateWorkIntake、ListDecisionBoard、UpdateRoadmapDecision、RecordFocusReview；所有写入必须带 actor、reason 和 audit ref。
- sqlc 表可选：`planning_work_items`、`planning_decisions`、`planning_reviews`；只保存状态、引用和脱敏摘要，不保存客户原文、销售聊天或敏感工单。
- 若 work item 连接 issue tracker、support、incident、billing 或 customer launch，使用引用 ID，不复制敏感内容。
- 自动化只做格式检查、过期提醒、lane 限制和链接完整性，不自动决定路线图。

## Vite 前端默认规则

- 管理界面应是密集、可扫描的工作台：Now、Next、Later、Parked/Killed、Expedite 和 Review By。
- 使用 Vercel Geist 风格的克制层级、语义色和暗色 token；不要做营销式 roadmap hero。
- 关键操作使用明确控件：开始、停车、杀掉、请求证据、创建 OpenSpec、创建产品 bet、升级 expedite。
- 不把 roadmap 展示成确定日期承诺；客户可见版本必须有 external claim boundary。
- 高风险操作需要 confirm 和证据链接：公开承诺、客户定制、超过 appetite、忽略安全/合规、启动无证据产品 bet。

## AI workflow 默认规则

- AI 可以帮忙归类、摘要、发现重复请求和检查缺失字段，但不能自动决定 `start_now`、`expedite`、`kill` 高影响工作。
- AI 生成的优先级建议必须显示依据：证据、风险、appetite、依赖、当前 capacity，而不是只输出一个分数。
- 使用客户反馈、支持工单、销售记录或事故材料时，只保存脱敏摘要和引用，不把原文放进 planning artifacts。
- AI 相关 work item 必须链接 W3/W8 中适用的 eval、dataset、red-team、route 或 quality artifact。

## 需要人判断的关键点

默认不问：

- 新 intake 的普通字段、低风险分类、parking 文案、routine review_by、Now/Next/Later 格式、过期提醒和缺失链接修复。

必须问：

- 是否让某项工作进入 `now`、`expedite`，或打断当前 focus。
- 是否杀掉/停车一个仍有客户、合规、安全、收入或核心产品风险的请求。
- 是否公开 roadmap、承诺日期、承诺客户定制、承诺 SLA/支持窗口或承诺路线图。
- 是否接受无用户证据、无 eval、无安全/隐私审查、无 rollback 的高影响工作进入实现。
- 是否超过本周期 appetite、引入多日/多周工作、长期供应商/架构锁定或显著成本。
- 是否改变目标用户、定价、数据边界、产品定位或核心策略。

其他优先级计算、字段完整性、敏感内容扫描、OpenSpec 链接、positive/negative fixture 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“为什么这个周期、请求是什么、当前选什么、对外怎么说、复盘后改什么”。
- 保留：人只判断进入 now/expedite、杀掉高风险、公开承诺、无证据高影响启动、超过 appetite 和策略变化。
- 调整：不维护无限 backlog；parking/killing 是一等状态，避免反复重读旧请求。
- 调整：RICE 只作为输入，不让分数替代人的产品和风险判断。
- 风险：planning 可能吞掉研发时间。缓解：复盘只看新增高影响、过期 review_by、当前 slots 和 one next change。

结论：可落地。W0 把“我接下来做什么”变成可审查选择，而不是把一人公司拖进项目管理软件。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：路线图围绕 outcome、机会和证据，而不是功能堆叠；W1 仍负责具体 bet。
- 工程角度：只有 now/expedite 进入 OpenSpec/实现，减少半成品和上下文分裂。
- 运维角度：SRE interrupt/toil 被纳入 capacity，不把中断当作免费上下文切换。
- 安全隐私角度：安全、合规、客户数据、公开承诺和无证据高风险启动都保留人工 checkpoint。
- 成本角度：appetite、capacity budget、park/kill 状态能阻止低证据多周项目消耗现金和 token。

结论：可落地。它把 W2 的 OpenSpec 总入口、W1 的产品发现、W4 的 AI 编码和 W6 的客户请求连接成一条“先选择，再验证，再实现”的节奏。


