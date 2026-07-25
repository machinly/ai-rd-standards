---
status: producer-self-check-complete
independent_final_review: pending
pilot: pending
review_snapshot: content-addressed-manifest
reviewed_scope: 2026-07-11-working-tree
---

# 研发规范整改审计

这份文件逐项核对 [外部元审查](2026-07-10-rd-standards-review.md) 的发现是否已经转化为仓库事实。它不是第二次“自己审自己”：当前结论只是生产者自检，独立最终审查和真实任务试验仍明确为 pending。

## 审计结论

- 默认体系已从 W0-W9 + 按时长升级 OpenSpec 改为 Quick / Standard / High-risk + 最小内核；Quick 不创建 OpenSpec，Standard/High-risk 实现按用户后续决定默认使用。
- W0-W9、角色、OpenSpec 主规格和多 Agent 材料已降为按需参考或历史材料。
- 结构、生命周期、知识入口、审查契约、证据政策和自动检查的整改已经落地。
- 规范是否真的减少总注意力、恢复和返工成本，尚未得到 10 个真实任务的数据支持。
- 首个用户中心 High-risk 实现试验已终止，出现 producer-stage 高风险遗漏；这不是 completed 样本，而是对核心假设的负面证据。
- 第二轮用户中心试验最终为 `changes_requested`；缺少关键用户旅程、真实 Browser E2E、单一当前状态和可导航治理入口，仍不计入 completed/eligible 样本。
- 终止复盘已促成权威产品输入、批准应用模板、完整本地集成环境、证据分级和 High-risk 实现前审查；用户随后确认 Go 使用 Kratos CLI/未来自有模板，数据默认 MySQL + sqlc、尽量通用 SQL 且默认无 foreign key。
- 用户随后明确决定 Standard/High-risk 实现默认启用 OpenSpec、Quick 豁免；第二轮遗漏被保留为 `used=false`，没有追溯性伪造使用记录。
- 当前整改没有独立 reviewer，因此不能被标记为最终接受。
- 独立审查输入、拒绝条件和复现命令已整理为 [reviewer 交接包](2026-07-10-rd-standards-independent-review-packet.md)；目标内容由 [逐文件 SHA-256 manifest](2026-07-10-rd-standards-snapshot-manifest.json) 标识。

状态词含义：

- `resolved`：仓库事实已改变，且有静态或命令证据；
- `resolved-for-current-policy`：当前强制声明已有适用边界和反证；历史检索目录仍不自动获得规范效力；
- `partially-resolved`：结构已补齐，但仍缺真实数据或更完整证据；
- `pending-independent-review`：生产者不能自行关闭；
- `superseded`：原问题依赖的政策已退出默认体系，不做追认。

## Findings 对照

| 原 finding | 状态 | 整改事实 | 仍需什么 |
| --- | --- | --- | --- |
| 核心产品假设尚未验证 | negative-evidence | 建立 [最小内核对照试验](../experiments/minimal-rd-kernel-comparison.md)；首轮已终止并出现 producer-stage 高风险遗漏；第二轮最终 `changes_requested`，已汇总为 1 条去敏负面记录；runtime skill 漂移已修复 | 独立审查整改结果，再用无关新项目开始可计量任务；当前 0 completed、0/10 eligible |
| 规范先于执行器 | resolved | [README](../README.md) 明确本项目是工作台和参考库，不再声称存在无人公司 runtime；[操作模型](../docs/04-operating-model.md) 与 [编排说明](../docs/05-agent-orchestration.md) 标为研究/实验材料 | 若未来实现 runtime，另行用运行证据验证 |
| 不同性质对象混成治理单体 | resolved | 默认读取面压缩为三个入口；主题规范、角色、来源、历史规格和实验各自分层 | 是否物理删除历史材料由试验数据决定 |
| 低估人的持续产品责任 | resolved | [最小内核](../docs/01-minimal-rd-kernel.md) 和 [重置决策](../decisions/2026-07-10-rd-standards-reset.md) 明确保留产品方向、用户价值、价值边界和最终问责 | 无 |
| W0-W9 被当成自然规律 | resolved | [快速分流](../docs/00-start-here.md) 不再先定位 W；40 份 W 文档均标为可选 playbook | 用试验比较三档路径与旧路径 |
| 参考体系存在选择偏差 | resolved-for-current-policy | [证据政策](../docs/sources/README.md) 和 registry 现要求 `supports`、`challenges`、适用边界、限制与 `superseded_by`；新增 AI 编码变慢/更新不确定性、多 Agent 负收益、自动化悖论与 automation bias 等反证；历史 source map 仅为检索目录 | 未来若把历史来源提升为强制声明，先登记并满足相同字段 |
| 用自身规则证明自身正确 | partially-resolved | 外部审查不使用 W/OpenSpec 作为最高尺度；verifier 分离结构、pilot 和独立审查状态 | 独立 reviewer 仍未完成 |
| OpenSpec 生命周期失真 | resolved | 原 58 个 completed change 与后续两项整改 change 全部归档，archive=60、active=0；56 个主 specs 可验证；归档差异有明确处置记录 | 新 change 继续避免 completed-active 漂移 |
| L0/L1 高影响变更缺少批准记录 | superseded | [重置决策](../decisions/2026-07-10-rd-standards-reset.md) 使用 `decision/approved_by/approved_at/conditions/revisit_on` 记录本次授权与后续模板、环境、MySQL/SQL/无外键裁决，并明确不追认 L0/L1、A/M 等旧政策 | 若未来恢复旧政策或命中 revisit 条件，必须重新提请决定 |
| Canonical map 与 freshness 漂移 | resolved | docs map、context pack、how-to、glossary 和 freshness 记录已同步到最小内核 | 到期或结构变化时复查 |
| 格式 PASS 被当成行为验收 | resolved | verifier 分开输出 format、governance、pilot 和 independent review；后两项不得被结构 PASS 替代 | 完成 pilot 与独立审查 |
| 两轮自检与独立审查冲突 | pending-independent-review | [review contract](../skills/one-person-openspec-rd/references/review-rubric.md) 已区分 producer self-check 和 independent final review；旧静态 Review 结论已删除 | 由未参与整改的人或模型审查目标版本 |
| 缺少量化成功标准和真实试运行 | partially-resolved | 对照试验已有可证伪阈值；新增 JSON schema 与聚合 verifier，要求至少 10 条合格记录、3 个无关项目、5A/5B、4 个配对组、2 组 7 天恢复、工具/token/失败重试和独立证据；第二轮负面记录已进入聚合 | 在无关真实项目中产生合格记录；当前 1 record、0 completed、0/10 eligible，synthetic test 不计入 pilot |
| 外部来源无等级和适用边界 | resolved-for-current-policy | evidence registry 要求 claim、来源类型、等级、支持/挑战对象、适用性、限制、状态、复查日期和替代记录；verifier 检查原 review 点名来源与至少 6 条显式反证 | 剩余历史 source map 不作为规范证据；被引用为当前规则前再登记 |
| 默认冷启动与 W0 仪式偏重 | resolved | 按治理 verifier 口径，默认三文件 307 行且不超过 350 行；Quick 不强制新建流程文件；Standard/High-risk OpenSpec 由风险路径而非时长触发 | 用真实 startup 数据复核收益 |

## 整改顺序对照

| 原建议 | 当前结果 |
| --- | --- |
| 停止扩张并重定义产品假设 | 已完成结构重置；效果验证 pending |
| 提取 10–15 条最小内核 | 已完成 15 条硬规则与三档路径 |
| 做至少 10 项对照试运行 | 已建立试验并保留 1 条负面记录；0 completed、0/10 eligible |
| 恢复仓库治理 | 原 58/58 change 与后续两项整改 change 已归档；archive=60、active=0 |
| 修复知识与审查闭环 | 知识工件已同步；独立终审 pending |
| 只为保留规则增加机器门禁 | verifier 已覆盖当前最小内核、可选边界、生命周期、证据与状态分离 |

## 首轮真实实验的回灌

用户中心试验在 2026-07-10 被用户终止；没有 commit、push 或 release，整个用户服务后来已删除。来源文件位于 `D:\Workspace\user\docs\rd-experiment-termination\`，本仓库的 [回灌记录](2026-07-10-user-center-experiment-ingestion.md) 只保存文件指纹、规范验证事实和禁止结论；不恢复或继续评价该服务。

本轮不是成功案例。它直接暴露：work brief 替代产品输入、人工仿造 Kratos 目录、后端/依赖/前端环境零散、HTTP integration 冒充更宽证据的风险，以及独立审查发生过晚。独立 reviewer 发现 migration P1 与多项 P2，说明 reviewer 分离有效，但不能消除实现前设计审查的需要。

依据用户后续明确决定，整改后的全局默认是：新应用必须通过批准模板生成；当前 Go 使用 Kratos CLI，未来改用版本化自有模板；多组件项目必须有完整本地集成入口；数据库优先 MySQL + sqlc；SQL 尽量跨 MySQL/PostgreSQL 通用；默认不创建 foreign key，并由应用逻辑、事务、约束、补偿和一致性扫描承担完整性。

## 第二轮真实实验的回灌

第二轮用户中心复盘来源位于 `D:\Workspace\user\governance\user-center-service-pilot-2-review\`。本仓库的[正式回灌记录](2026-07-11-user-center-pilot-2-ingestion.md)冻结了四份复盘文件和外部八条 checkpoint 记录的哈希，并明确只回收规范验证内容，不修复或继续评价样例服务。原 checkpoint 缺 schema、OpenSpec 字段和可比较指标，且过强命名 Browser E2E；因此只生成一条 `changes_requested` 去敏负面记录，保持 0 eligible。

该轮最终独立产品验收为 `changes_requested`，不能作为 completed 样本。它证明大量 API、事务、安全和治理工件仍可能漏掉真实页面任务；人工浏览器局部检查不能命名为 Browser E2E；最新 review 必须否决旧完成摘要；散落的 guard 目录、缺少 project map 和未登记的多 `cmd/` 入口会放大恢复成本。相应规则已进入关键旅程、严格 Browser E2E、`governance/` 根目录、单一当前状态、command registry 和治理工件预算。

该轮还真实记录 `OpenSpec used=false`。用户随后决定 Standard/High-risk 实现默认启用 OpenSpec、Quick 豁免；pilot schema 现在要求显式记录 used/change id/批准例外，不能追溯性把第二轮改写为“已使用”。

## 第二轮全库语义加固

结构整改后的全量扫描又发现并处理了会绕过默认入口的遗留语义：

- 56/56 OpenSpec 主规格在文件内声明“可选历史主题规格”，不再只依赖目录 README 说明；
- planning 主规格删除“超过半天必须进入 intake”，改为按影响、可逆性和恢复需要分流；
- W0 主文档删除“所有请求先 intake”和五类默认 planning 工件，改为仅在多个候选争夺注意力时按需使用一份记录；
- AI coding 主规格删除默认四件套与 Review 1/2，改为 Quick 无额外工件、Standard 一份 brief、生产者自检和独立终审分离；
- 13 份 playbook 的 Review A/B 标题改为设计取舍/风险边界，删除预填“可落地”“风险可控”结论；
- admin ops playbook 删除 L0/L1 默认自治等级，直接表述只读/建议与人类执行边界；
- 小型项目管理草案撤销“已纳入正式规范”和半天强制门槛，保留为历史研究；
- verifier 增加相应回归检查，防止这些语义重新出现。

## 命令证据

2026-07-11 在仓库根目录重新执行：

```text
python tools\verify_rd_standards.py .
FORMAT_VALID=PASS
GOVERNANCE_COMPLETE=PASS
PILOT_VERIFIED=PENDING
RUNTIME_SKILL_SYNC=PASS
RUNTIME_EVIDENCE_VALID=PASS
REVIEW_SNAPSHOT_VALID=PASS
INDEPENDENT_REVIEW_VERIFIED=PENDING

python tools\check_runtime_skill_sync.py .
RUNTIME_SKILL_SYNC=PASS status=synced

python tools\verify_pilot_records.py .
PILOT_RECORD_FORMAT=PASS
PILOT_EFFECT_VERIFIED=PENDING

python tools\test_verify_pilot_records.py -v
Ran 5 tests; OK

python tools\test_verify_project_evidence.py -v
Ran 4 tests; OK

python tools\build_review_snapshot.py . --check
SNAPSHOT_VALID=PASS

python tools\verify_workflow_index.py .
PASS optional-playbooks=39 default-openspec-entry=1

python C:\Users\machinly\.codex\skills\knowledge-context-recovery-guard\scripts\verify_knowledge_context.py . --legacy-root
PASS targets: rd-standards

openspec validate --all
56 passed, 0 failed

openspec list --json
{"changes":[]}
```

`check_runtime_skill_sync.py` 逐文件比较 canonical router 与全局安装，并检查 Go、Vite、quality、knowledge skills 的主体、references、agent 元数据和 deterministic verifier 契约。全局 router 已同步；Go 契约覆盖模板/MySQL/通用 SQL/无外键/完整环境/cmd 注册表，quality 覆盖关键旅程和严格 Browser E2E，knowledge 覆盖统一治理导航和单一当前状态。文件哈希、命令、结果和静态检查边界保存在 [runtime skill 同步证据](2026-07-10-runtime-skill-sync-evidence.json)。

补充检查：

- 134 份非归档 Markdown；治理 verifier 报告 broken local links=0；
- 默认入口 65 + 116 + 126 = 307 行（与治理 verifier 的 `line_count` 口径一致）；
- W 文档共 40 份，其中 39 份可选 playbook、1 份为默认 OpenSpec 入口；可选角色视角 8/8；
- 可选历史主规格 56/56；
- L0/L1 重复块 0、静态 Review 1/2 结论 0；
- archive 目录 60、active change 0；
- 仓库治理、snapshot、runtime、pilot、project evidence 脚本和全局 Go/quality/knowledge verifiers 的语法解析通过；
- 审查 snapshot manifest 覆盖除 packet/manifest 自身和本地缓存外的完整工作树；
- `git diff --check` 退出码 0，仅报告工作树 LF/CRLF 转换提示；
- 快照明确排除 `__pycache__`、`.pyc` 和 reviewer packet/manifest；本地缓存不作为审查输入。

这些结果证明当前工作树可解析且结构性整改一致；它们不证明流程净收益，也不构成独立接受。

## Requirement-by-requirement 完成审计

以下矩阵以原 meta-review 的 finding 为需求源，要求每项都有与声明范围匹配的证据。`achieved` 只表示整改动作已完成；涉及真实效果或独立判断时，静态文件和生产者命令不能代替。

| Requirement | 验收证据 | 判定 |
| --- | --- | --- |
| 默认入口不强制 W0-W9 或按时长升级 | README、router、kernel；默认三文件 307 行；Quick 不创建 OpenSpec，Standard/High-risk 由风险路径默认使用 | achieved |
| 不把制度设计描述成已实现 runtime | README 与 capability boundary 明确没有调度器、策略门和无人值守发布 | achieved |
| 内核、运行契约、playbook、证据/历史分层 | 15 条内核；39 份 W 文档为可选 playbook，W2 OpenSpec 入口只对 Standard/High-risk implementation 默认；OpenSpec/archive/source/review 分区 | achieved |
| 人持续拥有产品方向和最终问责 | README、kernel、router、全局安装 skill 逐文件一致 | achieved |
| W0-W9 只是可选分类 | start-here、workflow map、skill 和 verifier 均拒绝默认 W 路由 | achieved |
| 参考体系记录等级、边界、反证和替代 | source policy、12 条 registry；`challenges`/`superseded_by`；原 review 点名来源和至少 6 条反证由 verifier 检查 | achieved for current normative claims |
| 不用自身格式证明外部有效性 | verifier 分开 format/governance/pilot/independent review；synthetic fixture 不计入 pilot | achieved structurally；external effect pending |
| OpenSpec 当前状态唯一且可恢复 | 原 58/58 completed changes 和后续两项整改 change 已归档；archive=60、active=0；56 主 specs 通过 | achieved |
| 旧 L0/L1 高影响政策不能无批准生效 | 用户授权记录只批准外部整改；旧 L0/L1/A/M 默认已 superseded，不被追认 | achieved by removal/supersession |
| docs map、context pack 与 freshness 一致 | knowledge verifier PASS；结构变化均追加 freshness；runtime/pilot artifacts 已链接 | achieved |
| PASS 不能冒充行为验收 | governance verifier 输出独立状态；pilot 无数据时保持 false | achieved |
| producer self-check 与 independent final review 分离 | review rubric、packet、内容寻址 snapshot 已落地；当前 producer 没有填写 accept | contract achieved；independent decision pending |
| 成功标准可量化且采集合同可执行 | pilot schema、聚合 verifier 与 5 个 pilot 正反测试；project evidence verifier 另有 4 个测试；要求 3 项目、5A/5B、7 天恢复、工具/token/失败重试和 OpenSpec 使用记录 | instrumentation achieved；1 negative record、0/10 eligible |
| 默认冷启动显著收缩且不会按时长升级 | 默认三文件 307 行；Quick 无工件；Standard/High-risk OpenSpec 由风险而非耗时触发；旧半天/30 分钟触发由 verifier 拒绝 | achieved structurally；attention benefit pending pilot |
| 仓库规则与实际 Codex runtime 一致 | router 5 文件 hash 一致；Go/Vite/quality/knowledge contracts 与元数据通过 quick_validate/runtime sync；runtime evidence PASS | achieved on recorded machine state |
| 两轮失败实验只回灌验证、不修复样例服务 | 首轮已删除；第二轮仅读取复盘；两份 ingestion 均明确禁止把回灌当成交付证据 | achieved |

完成审计结论：**整改实现和测量基础设施已经完成，但整个目标尚不能宣告 achieved。** 缺少的不是更多文档，而是两类不可由生产者伪造的证据：独立 reviewer 对当前 snapshot 的接受，以及至少 10 条合格真实任务记录证明新路径达到阈值。二者任何一个未完成时，`independent_review_verified` 或 `pilot_verified` 必须保持 false。

## 生产者自检

### 范围与保真

- 没有把 W9、OpenSpec 或仓库 skill 当作本次整改的上位依据。
- 没有声称多 Agent、无人值守公司或策略门 runtime 已经存在。
- 没有把归档历史等同于删除，也没有把主 specs 的格式有效等同于实现有效。
- 没有把 `pilot: pending` 或 `independent_final_review: pending` 改写成完成。

### 当前验收状态

| 维度 | 状态 | 解释 |
| --- | --- | --- |
| 文件与链接可解析 | pass | 由本地检查验证 |
| 结构性整改 | pass | 原 finding 已有明确 disposition 和仓库证据 |
| 流程净收益 | pending | 1 条真实负面记录已保留，但 0 completed、0/10 eligible |
| runtime skill 一致性 | pass | router 逐文件同步；Go/Vite/quality/knowledge contracts、metadata 与静态 verifiers 通过 runtime sync，已记录静态检查边界 |
| 独立最终审查 | pending | 本文件由生产者创建，不能自我接受 |

独立 reviewer 应使用 [交接包](2026-07-10-rd-standards-independent-review-packet.md)，并把结论绑定到 manifest 的 `sha256-tree`。packet 被排除在快照之外，允许 reviewer 写入结论；其它内容变化必须重新生成 manifest 并重新审查。

## 独立最终审查记录

在 reviewer 未参与本次产出的前提下填写：

    Reviewer:
    Reviewed at:
    Target revision:
    Scope:
    Evidence checked:
    Findings:
    Decision: accept | changes-requested | reject
    Residual risks:

只有 `Decision: accept` 且问题已处理后，才能把文件头的 `independent_final_review` 改为 `accepted`。
