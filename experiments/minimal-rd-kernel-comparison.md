# 最小研发内核对照试验

状态：paused。首个真实 High-risk 实现试验已终止，假设尚未验证。
目的：验证三档风险路径是否比原 W0-W9 默认路由更少打断、更易恢复，同时不增加高风险漏检。

## 可证伪假设

对同类 Standard 任务，最小内核相对原流程：

- 人工中断和恢复时间下降至少 30%；
- 总交付时间增加不超过 10%；
- 高风险漏检不增加；
- 返工率不增加。

未达到目标时，应删减或修改最小内核，而不是用更多文档解释失败。

## 基线

2026-07-10 仓库基线：

- docs Markdown：56 份；
- docs 行数：约 11,603；
- OpenSpec Markdown：288 份；
- active changes：58；
- completed active changes：58；
- 默认 W0 冷启动材料：约 1,154 行、55KB；
- 多 Agent runtime：不存在；
- status、escalation 和 batch log 运行证据：不存在。

## 对照方案

A：原 W0-W9 + 默认 OpenSpec 路由。
B：Quick / Standard / High-risk + 最小内核。

不要求在同一真实任务上重复制造两份实现。可以选相近规模任务配对，并记录差异与偏差来源。

只在本地、sandbox 或无真实用户/生产副作用的任务上运行路线 A；不能为了对照试验故意弱化真实高风险保护。

## 每项任务记录

机器契约见 [pilot record schema](rd-pilot-record.schema.json)。每个目标项目先写自己的 `experiments/rd-standard-pilot.jsonl`，保留原始命令/时间/审查证据；汇总时把去敏后的记录复制到本仓库 `experiments/rd-standard-pilot.jsonl`，并用 `source_evidence` 指向项目记录或内容哈希。不得从聊天回忆补造数字。

每条记录必须包含：

- `task_id`、`project_id`、`comparison_group`、路线、风险路径、任务类型和真实状态；
- `source_evidence` 与 `toolchain_fingerprint`，用于恢复项目证据、模型/skill/工具版本；
- `openspec.used`、`change_id`、跳过批准和原因；Standard/High-risk 未使用 OpenSpec 且没有用户明确批准时，可以作为结构合法的负面证据保留，但不能计入效果样本；
- 起止时间、冷启动时间、上下文数量及单位；
- 人工中断次数与分钟、返工、首次通过、流程维护和总交付分钟；
- 工具调用、失败重试、总 token、可得成本和新增治理工件数；
- 分层 verification、独立 review、high-risk miss、剩余风险和无法测量字段的明确原因；
- 需要恢复演练时记录 delay、恢复分钟、成功与所需上下文。null 只有在 `metrics_gaps` 解释时合法，但缺核心指标的 completed 记录不计入效果样本。

运行：

    python tools/verify_pilot_records.py . --json

## 任务记录

| task_id | route | risk_path | task_type | status |
| --- | --- | --- | --- | --- |
| reset-rd-standards-2026-07-10 | B | Standard | docs/governance | self-check-complete |
| user-center-plan-2026-07-10 | B | High-risk | product/auth planning | producer-self-check-complete |
| user-center-implementation-2026-07-10 | B | High-risk | code/auth/data/frontend | terminated |
| user-center-service-pilot-2-2026-07-11 | B | High-risk | code/auth/data/frontend | changes-requested |

### reset-rd-standards-2026-07-10 记录

- startup baseline：旧默认读取约 1,154 行；新默认读取 255 行；
- human interruptions：用户给出整改授权后为 0；
- mechanical rework：2 次 patch/PowerShell 机械错误，均未改变目标方向；
- governance verification：PASS；
- optional playbooks verification：40/40 PASS；
- OpenSpec lifecycle：58 archived，0 active，0 archive failure；
- OpenSpec format：56/56 PASS；
- independent final review：pending；
- 结论：本任务可作为 B 路径样本，但在独立 final review 前不计入 completed pilot。

### user-center-plan-2026-07-10 记录

- outcome：形成一份可带入新会话执行的用户中心方案，并内置研发规范试验方法；
- route：High-risk preparation，原因是未来工作涉及身份、权限、个人数据和管理员能力，本次没有生产副作用；
- artifacts：只新增一份项目方案，没有创建 OpenSpec 或 W0-W9 工件；
- human interruptions：1。生产者最初准备了过细的多技能研究路径，用户要求收缩为一份方案文本；
- rework_count：1。说明即使使用最小内核，技能触发仍可能扩大上下文和方案粒度；
- skill conflicts：旧 one-person/go/vite skill 仍默认 W/OpenSpec 或按时长触发，与当前最小内核冲突，本任务没有采用；
- startup_minutes / context volume：未在任务开始时可靠计量，记为数据缺口，不补造数字；
- high_risk_miss：producer self-check 未发现；仍需独立 reviewer 验证；
- 结论：保留为 B 路径 High-risk preparation 样本，但在独立 final review 前不计入 completed pilot。

### user-center-implementation-2026-07-10 记录

- 来源：`D:\Workspace\user\docs\rd-experiment-termination\`；本仓库的 [证据回灌](../reviews/2026-07-10-user-center-experiment-ingestion.md) 保存事实摘要和文件指纹；
- outcome：尝试实现用户中心，但用户于 2026-07-10 终止实验；没有 commit、push 或 release。来源记录中的工作区后来已随整个用户服务删除，本实验不恢复或继续评价该服务；
- template provenance：失败。Go/Kratos 项目由人工按目录搭建，不是批准的 Kratos CLI 模板生成；
- product authority：失败。执行 work brief 替代了经人确认的产品输入、体验设计、验收映射和六项高影响决策；
- integration environment：失败。只有 PostgreSQL、OIDC mock 和部分工具/test runner 在容器中，后端仍在宿主机，两套前端不存在，因此没有完整本地集成环境，也没有浏览器 E2E；
- independent reviewer findings：发现 migration down 的 P1，以及 profile 并发覆盖、identity-link session 绑定、成功路径覆盖和 Proto/runtime 语义等四类 P2；
- high_risk_miss：`yes-at-producer-stage`。独立 reviewer 在发布前发现并阻止了更强完成声明，但问题出现得太晚，不能记为“没有漏检”；
- startup_minutes / context volume / process_minutes：没有可靠采集，不能补造，也不能比较路线注意力收益；
- rework_count / first_pass：由于终止和证据口径不完整，不给出伪精确数值；
- 结论：该任务不计入 completed pilot，并对“高风险漏检不增加”提供负面证据。reviewer 分离有价值，但 High-risk 设计审查必须提前到实现前。

### user-center-service-pilot-2-2026-07-11 记录

- 来源：`D:\Workspace\user\governance\user-center-service-pilot-2-review\`；本仓库的 [第二轮复盘回灌](../reviews/2026-07-11-user-center-pilot-2-ingestion.md) 冻结四份复盘文件的哈希、事实和处置；
- outcome：后端、管理端和登录端已形成大量实现及治理工件，但最终独立产品验收为 `changes_requested`，不能视为 completed；本次只回收规范验证内容，不修正该样例服务；
- product closure：失败。没有可执行的关键用户/管理员旅程矩阵，review 轮次主要证明局部代码和治理工件，不足以证明陌生用户可完成产品任务；
- Browser E2E：失败。所谓 E2E 没有以真实浏览器完成点击、输入、导航、确认和最终业务状态核验，API 调用绕过了前端交互；
- evidence state：失败。当前状态、review decision 和历史完成摘要不一致；最新 `changes_requested` 没有使旧完成声明自动失效；
- navigation and burden：治理文件散落根目录，缺少 project map、统一 governance root、多 `cmd/` 入口登记和工件预算，增加了恢复与审查成本；
- OpenSpec：`used=false`，且没有事前记录的用户批准例外。该遗漏促成了“Standard/High-risk 实现默认启用 OpenSpec、Quick 豁免”的后续决策，但本条样本仍不能追溯性改写为已使用；
- 结论：该任务不计入 completed pilot；它为“治理数量不能替代产品闭环”“手工浏览器检查不能命名为 Browser E2E”“当前状态必须由最新审查驱动”和“默认 OpenSpec 必须进入机器记录”提供负面证据。

## 阶段性结论与恢复条件

- 当前聚合包含 1 条去敏负面记录、0 completed、0/10 eligible；第二轮样例最终为 `changes_requested`，没有证据支持最小内核已经降低注意力或交付成本。
- 首个真实 High-risk 实验出现 producer-stage 高风险遗漏，因此核心安全假设未得到支持。
- 权威产品输入、批准模板、完整本地集成环境、证据分级、实现前独立审查、关键旅程、严格 Browser E2E、统一治理入口、单一当前状态和 runtime skill 同步规则均已落地；pilot 仍保持 paused，直到本次规范整改取得独立审查，并选择一个与用户中心样例无关的新项目开始可计量任务。
- 后续选择一个与已删除用户服务无关的新项目继续实验；数据库默认按用户确认使用 MySQL + sqlc，SQL 尽量通用、默认无 foreign key，并为应用层引用完整性提供并发、删除与孤儿检测证据。

## 决策门槛

至少完成 10 个指标完整、证据可追溯且审查状态合格的真实任务，覆盖至少 3 个互不依赖的项目，并包含：

- 5 个路线 A 和 5 个路线 B；
- 至少 4 个同时含 A/B 的 comparison group；
- 3 个 Quick；
- 4 个 Standard；
- 3 个 High-risk 或真实高风险准备任务；
- 2 个 AI 行为任务；
- 2 个数据/发布/运行任务。
- 至少 2 组 A/B 都完成的 7 天恢复演练。

聚合通过还要求：B/A 的人工中断与恢复分钟不高于 0.70，总交付分钟不高于 1.10，返工不增加，高风险漏检数不增加。该小样本只能作为方向性证据，不能声称统计普遍性；独立 reviewer 仍需检查任务是否真正可比、是否存在选择偏差和指标博弈。

数据不足时，只能说“试验未完成”，不能宣布流程有效。
