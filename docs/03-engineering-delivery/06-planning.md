# 计划

## 项目目的与边界

计划把已经确认的交付目标转成可执行、可跟踪且中断后可恢复的工作安排。它负责工作拆分、先后顺序、状态记录、专项路由和恢复上下文；它不重新决定产品方向，不生产代码、配置或迁移，也不维护验证证据、发布动作和生产处置的权威内容。

## 根本原则

- **ITEM-PLANNING-001**：工作跨会话、需要独立验收或中断后难以恢复上下文时，应显式跟踪；一份记录足够时不再拆分计划工件。

## 核心判断

以下问题是非规范性阅读提示，不替代带 rule-id 的规范：

- 当前交付是否需要跨会话恢复、独立验收或显式状态跟踪？
- 工作能否由一份记录承载，还是确实需要独立 change 或专项工件？
- 产品输入、体验输入、非目标、失败模式和人工判断点是否已经进入计划？
- 实现前必须先准备哪些 fixture、rubric、清单或迁移指南？
- 中断后，接手者能否从权威入口恢复目标、状态、边界、风险和开放决策？
- 哪些事项已超出计划，应转交实现、验证、发布、运行或评估？

## 重新组织后的规范要求

### 计划入口与治理边界

<!-- rule-id: PLAN-TRACKED-BATCH-APPLICABILITY -->
- Explore 使用一份包含 question、hypothesis、sandbox boundary、shortest slice、active tasks、showcase、evidence/limits、decision 和 next 的短记录；Deliver 工作跨会话、需要独立验收，或中断后难以恢复上下文时，才须进入可持续记录状态的规格与计划路径。

<!-- rule-id: PLAN-RISK-ROUTE-NOT-DURATION -->
- Quick、Standard 和 High-risk 只属于 Deliver。判断 Deliver 是否使用 Standard/High-risk 规格路径时，以影响、可逆性、问责性和变更性质为依据；任务时长、文件数或 Explore 类型本身不得单独触发该路径。

<!-- rule-id: PLAN-MINIMAL-KERNEL-PRECEDENCE -->
- 计划规则与本规范的正式分类及项目原则冲突时，以正式规范为准。

<!-- rule-id: PLAN-SINGLE-RECORD-DEFAULT -->
- 一份记录足以支持取舍、跟踪和恢复时，禁止再平行拆出 strategy map、work-intake、decision board、roadmap 与 focus review。已有 OpenSpec `tasks.md` 足够时跳过 `writing-plans` 和 Superpowers plan；Explore 已有短记录时不再创建平行 work brief。多项任务共享写域或存在顺序依赖时保持单 Agent；只有用户允许、任务独立、写域不重叠且并行确有净收益时，才使用 parallel agents。

<!-- rule-id: PLAN-EXPLORE-WIP-LIMIT -->
- 轻量 Explore 同时最多 5 个 active tasks；其余进入 `Next` 或 `Later`。新任务进入 active 前必须完成、移出或让位一个现有任务。

<!-- rule-id: PLAN-EXPLORE-SHOWCASE-CADENCE -->
- 轻量 Explore 每 120 分钟或每 5 次提交进行一次真实 showcase，以先到者为准；连续 2 小时没有新增可见产品事实时停止并缩小 question 或 shortest slice，不得用补文档、横向治理或追溯延长期限掩盖停滞。

<!-- rule-id: PLAN-EXPLORE-DELIVER-HANDOFF -->
- promote 时只把 selected increment 转成 Deliver tasks；Explore 的短记录保留证据链接，Deliver Standard/High-risk 使用 OpenSpec `tasks.md` 作为状态权威，不并行维护 Superpowers plan 或 work brief。

<!-- rule-id: PLAN-AI-COMPLEX-CHANGE-SEPARATION -->
- 触发完整 RAG 平台、向量库选型、finetuning、复杂多 agent 组织、实时语音、多模态产品、成本平台或供应商抽象层任一事项时，须为该事项单独建立 OpenSpec change，不在普通 prompt/eval 批次中展开。

<!-- rule-id: PLAN-SERVICE-CHANGE-START -->
- 推进 Deliver Standard/High-risk 服务端 change 前，须确认权威产品输入与体验设计，并创建或继续对应的 OpenSpec change；轻量 Technical Spike 只在 sandbox 内形成不可发布 shortest slice，不因此预建 Deliver 合同。

<!-- rule-id: PLAN-VISUAL-UX-READINESS -->
- Explore promote 后的 Deliver Standard/High-risk change 计划须读取 proposal 中的 `visual_ux` 判定。值为 `required` 时，计划链接当前 `flow.md`、关键 wireframes 和 `review.md`；尚未取得人类 `approved` 时可以记录技术调查或开放问题，但不得把生产性实现任务标记为 ready。值为 `not-required` 时保留理由，不补造 UX 工件；探索期不追溯伪造批准。

<!-- rule-id: PLAN-AI-CHANGE-SCOPE-FAILURE -->
- 按默认顺序推进 AI change 时，OpenSpec 须同时记录本次不做的事项与已知失败模式。

<!-- rule-id: PLAN-AI-EVAL-BEFORE-IMPLEMENTATION -->
- 按默认顺序推进 AI change 时，须在实现前先形成 `cases.jsonl` 和 `rubric.md`。

<!-- rule-id: PLAN-AI-TASK-STATE-UPDATE -->
- AI change 完成一个实现步骤后，须同步更新 `tasks` 中的执行状态。

<!-- rule-id: PLAN-MAJOR-UPGRADE-SEPARATE-CHANGE -->
- major、runtime 或 framework 升级须使用独立 OpenSpec change；形成升级计划前先读取官方 migration guide。

### 中断恢复与接手

<!-- rule-id: PLAN-RECOVERABLE-CONTEXT-CONTENTS -->
- 为持续维护沉淀的可恢复上下文须覆盖目标、当前 product bet、系统形状、关键命令、边界、风险、开放决策与 handoff prompt；维护阶段应把此前结果转成可恢复上下文、可维护依赖、可信证据和可持续对外维护边界，而不是继续堆叠新功能 backlog。

<!-- rule-id: PLAN-MODULE-MAP-RECOVERY-PURPOSE -->
- 创建 module map 时，应使接手者能够据此恢复系统上下文。

<!-- rule-id: PLAN-CONTEXT-PACK-OPEN-DECISIONS -->
- context pack 须包含 `Open Decisions`，其落点为 `governance/knowledge/context-packs/` 目录中名为 `<target>.md` 的文件。

<!-- rule-id: PLAN-CODEX-HANDOFF-FIRST-READS -->
- 新人或 Codex 接手 target 时，须先从项目上下文恢复入口读取 `governance/README.md`、`governance/project-map.json` 与 `governance/current-status.json`，再继续加载目标相关材料。

<!-- rule-id: PLAN-OPS-RECOVERY-MINIMUM -->
- 为一人运行场景准备恢复上下文时，`slo.json`、runbook、release checklist 与 incident README 构成来源规定的最小闭合集；不得借此复制这些工件中属于运行或发布项目的规范正文。

### 阶段路由

<!-- rule-id: PLAN-OPERATIONS-WORK-EXCLUSION -->
- 事故止血和线上观测转交[运行](../04-operations-maintenance/10-operation.md)，发布执行转交[发布](09-release.md)，学习复盘和文档维护转交[评估](../04-operations-maintenance/11-evaluation.md)中的学习或知识维护主题；这些工作不在工程计划路径中继续展开。

## 按主题整理的执行细则

### 凭据治理的首轮安排

<!-- rule-id: PLAN-CREDENTIAL-INVENTORY-FIRST-SCOPE -->
- 为最高关键度 target 建立 `credentials/inventory/<target>.json` 时，首批须列出 production 凭据以及 OpenAI 或其他 provider key。

<!-- rule-id: PLAN-CREDENTIAL-ROTATION-FIRST-SCOPE -->
- 首份 `rotation-plan` 先覆盖 blast radius 最高的 1 至 3 个凭据。

<!-- rule-id: PLAN-CREDENTIAL-FIRST-LOW-RISK-RUN -->
- 首次低风险 rotation run 应优先选择开发或 staging key，并须记录验证证据和旧凭据撤销证据。

<!-- rule-id: PLAN-CREDENTIAL-EXPOSURE-FOLLOWUP -->
- `exposure-review` 须把两类后续信息分别落项：下一项预防动作和 detection controls；即便结论为未发生泄露，这两项也不能省略。

<!-- rule-id: PLAN-CREDENTIAL-VERIFIER-HANDOFF -->
- 凭据 verifier 须接入 release/security checklist；该 checklist 的验证权威仍由验证和发布项目维护。

<!-- rule-id: PLAN-CREDENTIAL-MONTHLY-FOCUS -->
- 一人执行真实项目时，每月只安排一个最高风险 credential 改进。

## 输入与产物

输入包括已经确认的产品与体验设计、OpenSpec change、适用的 `visual_ux` 判定及其当前 review、风险和人工判断边界、现有任务状态，以及专项要求的工件入口。产物包括唯一执行清单、排序后的批次、所需前置工件、恢复上下文、开放决策和下一步；计划只引用其他项目的证据或动作，不复制其权威规则。

## 完成、停止或退出条件

当工作已拆成有序批次、每个批次有权威状态、前置输入与专项路由明确，适用的可视 UX 已取得人类批准，且接手者可从记录恢复上下文时，计划可交给实现。产品或体验输入未确认、`visual_ux: required` 尚未批准、风险路径不清、需要人工判断而尚未决定，或 OpenSpec 与实际工作不一致时停止；实现中发现范围或边界变化时返回相应产品或技术设计项目重新计划。

## 相关项目引用

- 定义与体验设计决定本轮做什么以及用户如何感知结果；计划不得改写这些输入。
- 技术设计提供架构、契约、数据和风险边界；计划只据此拆分和排序。
- 实现生产代码、配置、迁移和技术产物，并把进度写回权威任务状态。
- 验证负责证明结果，发布负责进入真实环境，运行负责事故与持续服务，评估负责学习结论；计划只维护它们之间的工作依赖和交接点。
