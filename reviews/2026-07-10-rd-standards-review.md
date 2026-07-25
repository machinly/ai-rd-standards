# 研发规范系统审查报告

> 状态：External meta-review evidence（非 canonical 规范）
> 审查日期：2026-07-10
> 审查对象：当前工作树中的一人公司 AI 研发规范、OpenSpec 工件、知识恢复工件与既有模型修改
> 审查者：Codex
> 审查立场：站在现有研发规范之外，不以 W0-W9、OpenSpec 或仓库内 skill 作为最高审查准则
> 结论：作为知识库有明显价值；作为强制研发操作系统复杂度过高且核心假设尚未验证

## 整改状态（更新于 2026-07-11）

本节是原始外部 review 之后追加的当前状态摘要；下文的 58 个 active change、1,154 行冷启动等数字保留为整改前基线，不应读成当前事实。

| 问题 | 状态 | 当前证据 |
| --- | --- | --- |
| 默认入口过重 | 已整改 | 按治理 verifier 口径，README + 快速分流 + 最小内核共 307 行，仍低于 350 行预算；原基线约 1,154 行 |
| W0-W9 强制路由 | 已整改 | 改为 Quick / Standard / High-risk；39 份 W 文档为可选 playbook，W2 只在 Standard/High-risk 实现时作为默认 OpenSpec 入口 |
| OpenSpec 按时长强制触发 | 已整改 | 不再按时长触发；用户后续决定 Standard/High-risk 实现默认使用 OpenSpec、Quick 豁免，净收益仍由 pilot 验证 |
| 人只负责目标和例外 | 已整改 | 人持续拥有产品方向、用户价值、边界和最终问责 |
| 多 Agent 被描述为当前能力 | 已整改 | 操作模型和编排文档改为实验材料，明确没有 runtime |
| 生产者自评充当最终 review | 已整改 | 新 review contract 区分 self-check 与 independent final review；旧静态自评已删除 |
| 58 个 completed active change | 已整改 | 原 58 个全部归档；加上后续两项整改 change，当前 active=0、archive=60 |
| Canonical map / freshness 漂移 | 已整改 | docs map、context pack、freshness、decision record 已同步 |
| 格式 PASS 冒充行为验收 | 已整改 | 新 verifier 分离 format_valid、governance_complete、pilot_verified |
| 来源等级混杂与选择偏差 | 已整改当前规范声明 | registry 增加 `challenges` 与 `superseded_by`，补入 AI 编码负收益/测量漂移、多 Agent 负收益、自动化悖论与 automation bias；历史 source map 仅为检索目录 |
| 核心净收益未验证 | 负面证据 / paused | 首轮用户中心 High-risk 实现已终止；第二轮最终为 `changes_requested`，已汇总为 1 条去敏负面记录；pilot 仍为 0 completed、0/10 eligible，不能宣布流程有效 |
| 新应用模板来源、完整本地环境和产品输入缺失 | 已加入整改 | [终止证据回灌](2026-07-10-user-center-experiment-ingestion.md) 将 Kratos CLI/未来自有模板、完整本地集成、权威产品输入和证据分级写入默认规则 |
| runtime skill 与仓库规则漂移 | 已整改 | 全局 router 已逐文件同步；Go、Vite、quality、knowledge skills 与批准模板、默认 OpenSpec、MySQL/通用 SQL/无外键、完整本地集成、关键旅程和治理导航契约一致 |
| 当前整改的独立最终审查 | 待完成 | 自动检查和生产者自检已完成；[reviewer 交接包](2026-07-10-rd-standards-independent-review-packet.md) 与内容寻址 snapshot manifest 已就绪 |

逐项 disposition 与当前验收边界见 [整改审计](2026-07-10-rd-standards-remediation-audit.md)。

首轮用户中心试验没有证明三档路径有效。它提供的是负面证据：独立终审发现重要问题并避免了更强完成声明，但产品输入、批准模板、完整本地环境和 High-risk 实现前审查均缺失，说明最终审查本身不足以阻止前期方向偏差。

## 1. 审查目标

从独立于现有规范体系的视角，系统审查当前研发规范项目，核对设立目的与参考依据，评估：

- 结构一致性；
- 内容完整性；
- 一人可执行性；
- 流程、门禁与证据链是否真实闭环；
- 对人的注意力成本和 Codex 上下文恢复成本；
- 既有模型 review 已覆盖什么、遗漏什么；
- 长期维护成本及最小整改顺序。

本报告还要回答更上层的问题：

- 这套研发规范是否真的有必要以当前规模存在？
- W0-W9 是否是最合适的基本模型，而不只是内部自洽的分类方式？
- “增加规范、工件和 Agent”是否真的降低了一人公司的注意力成本？
- “人只注入目标、裁决例外”的目标是否现实且值得追求？
- 如果去掉大部分文档，哪些最小规则仍不可缺少？

本报告只记录审查结论，不修改 canonical 规范，不替代人的产品、价值和风险裁决。

## 2. 审查立场与方法

本次审查不接受以下循环论证：

- 不能因为 W9 要求维护文档，就证明本次 review 必须属于 W9。
- 不能因为 OpenSpec validate 通过，就证明 OpenSpec 是正确的治理选择。
- 不能因为规范要求两轮 review，就把规范自身生成的两轮自检当作独立证据。
- 不能因为 40 份文档都加入承接条款，就证明这种全量承接值得维护。
- 不能因为来源数量很多，就证明由这些来源推导出的强制规则成立。

审查采用四层判断：

1. **目的层**：它解决的真实问题是否清楚、重要、可测量？
2. **机制层**：所选机制是否比更简单的替代方案有效？
3. **执行层**：规则是否有真实 runtime、工具和证据承接？
4. **内部一致性层**：文件、索引、OpenSpec、review 和 freshness 是否相互一致？

其中前三层优先于第四层。一个体系即使完全内部一致，也可能没有必要、成本过高或解决错了问题。

## 3. 总体判断

总体结论：**不建议把当前体系直接设为强制研发操作系统；建议先收缩成最小可执行内核并通过对照试运行验证。**

作为知识库和风险清单，这个项目价值较高：它系统整理了研发、AI、安全、发布、运维、维护和多 Agent 失败模式。作为日常强制工作流，它目前明显偏重；作为“人只给目标、AI 公司自主运行”的操作系统，它仍主要是设计文档，而不是已经被 runtime、数据和真实案例证明的系统。

分层判断：

- **作为参考知识库**：可以保留，覆盖面广，检索价值高。
- **作为默认研发方法**：需要大幅裁剪，不能让所有工作默认穿过完整体系。
- **作为多 Agent 编排协议**：可以作为候选设计，但尚无实现和试运行证据。
- **作为无人值守公司操作系统**：当前不成立，距离目标仍有执行器、策略门、状态系统、评测和运营证据的明显缺口。

现阶段的主要问题不是缺少更多规范，而是已有规范没有完成以下闭环：

- completed OpenSpec change 的同步与归档；
- 高影响 L0/L1 变更的人工批准记录；
- 独立 reviewer 与生产者自检的区分；
- 规范目标的可量化验收；
- verifier 对新治理要求的真实覆盖；
- canonical docs map 与 freshness 的同步；
- 外部来源的证据等级和适用边界。

因此，当前版本最准确的定位是：**一套内容丰富但尚未证明净收益的研发治理设计与参考资料库。** 不应被描述为已经具备 M2-M4、无人值守执行能力，或已经证明能够降低一人公司的总认知负担。

## 4. 已有模型 review 的实际成果

其他模型留下的主要成果是实现性修改，而不是独立 review 报告：

- 新增 `docs/04-operating-model.md`；
- 新增 `docs/05-agent-orchestration.md`；
- 新增小型项目管理来源整理；
- 修改 README、工作流入口、索引、角色入口和 context pack；
- 为 10 个 W 主入口加入 L0/L1/小项目承接条款；
- 为 30 个触发专项加入专项承接条款；
- 创建 `openspec/changes/add-operating-model-and-agent-orchestration/`；
- 在 proposal 中完成两轮自审。

结构覆盖检查结果：

- W 主入口：10/10 存在承接条款；
- 触发专项：30/30 存在承接条款；
- `python tools\verify_workflow_index.py .`：PASS；
- knowledge context verifier：PASS；
- `openspec validate --all`：114/114 通过格式验证。

这些结果证明修改在结构和格式上完整，但不能证明治理决策已批准、行为已试运行或规范已经形成唯一事实源。

## 5. 超越现有框架的 Meta Findings

### [P1] 核心产品假设尚未验证：更多治理是否真的减少注意力成本

项目的核心产品假设是：通过更多规范、工件、Agent、验证门禁和持久账本，减少创始人的注意力成本和 Codex 的上下文恢复成本。

当前仓库事实同时支持相反假设：

- `docs/` 有 56 份 Markdown，共约 11,603 行；
- `openspec/` 有 288 份 Markdown；
- 有 58 个 completed 但仍 active 的 change；
- 一次默认 W0 冷启动可能读取约 1,154 行入口内容；
- 最近一次 L0/L1 修改影响 46 个既有文件并新增 4 个路径；
- 尚无任务级数据证明这些工件减少了总耗时、返工或人工判断。

这意味着项目目前证明的是“可以建立一套完整治理体系”，而不是“这套体系比更简单的方法更有效”。

建议：先把核心假设写成可证伪命题，例如：

> 对同类中等风险研发任务，使用最小规范内核后，冷启动时间、人工中断次数和返工率至少下降 30%，同时交付周期增加不超过 10%。

如果对照试运行不能满足目标，应删减规则，而不是继续增加 skill、索引和 verifier。

### [P1] 规范先于执行器：当前更像“制度设计”，不是“操作系统”

规范定义了总控 Agent、工人池、任务契约、状态账本、升级队列、策略门、并发控制、熔断、预算传播和成熟度升级，但仓库中没有对应 runtime：

- 没有任务调度器；
- 没有状态账本实现或 schema；
- 没有策略门引擎；
- 没有预算与熔断执行器；
- 没有 `ai-coding/` 或 `escalations/` 运行记录；
- 没有 M1/M2 真实试运行数据。

纯文本规范不能强制 Agent 停止、限流、隔离工作区、阻止危险副作用或保证独立审查。把期望写成 MUST 不会自动产生执行能力。

因此，“虚拟公司操作系统”是目标或设计隐喻，不是当前产品事实。当前 README 应明确区分：

- 已实现并可验证的机制；
- 依赖人工遵循的流程；
- 计划中的 runtime；
- 尚未验证的研究假设。

### [P1] 项目混合了过多不同性质的对象，导致治理自身成为单体系统

当前仓库同时承担：

- 公司操作哲学；
- 产品发现和项目管理方法；
- 软件研发流程；
- Go/Vite/sqlc/gRPC 技术规范；
- AI prompt/eval/RAG/tool/model 治理；
- 安全、隐私、合同、许可证与审计提醒；
- 发布、SRE、事故与凭据运行手册；
- 多 Agent runtime 设计；
- 文档知识库和外部参考文献库；
- OpenSpec 变更历史。

这些对象的稳定性、使用者、风险和更新频率不同。把它们放进一个统一规范主线，会让任何抽象层变化向大量文件扩散；这次新增 L0/L1 后修改 46 个文件就是直接证据。

建议把体系拆成四类资产，而不是继续增加 W 内承接条款：

1. **最小内核**：不超过 10-15 条、与栈无关、可执行的硬规则。
2. **运行契约**：task packet、side-effect policy、状态机和 verifier schema。
3. **按需 playbook**：Go、Vite、AI、SRE、安全等可选主题入口。
4. **证据与历史**：source map、review、archive，不进入默认上下文。

### [P1] “人只注入目标和裁决例外”低估了人的持续产品责任

一人公司创始人的不可替代职责不只是输入目标和处理异常，还包括：

- 形成产品判断与品味；
- 持续理解用户和市场；
- 识别哪些指标会诱导错误行为；
- 对价值取舍、伦理、安全和承诺负责；
- 判断何时不应优化已有目标；
- 发现规范本身没有提出的新问题。

如果把人的默认角色压缩为“目标输入器 + 例外审批器”，系统容易优化旧目标、强化已有假设，并把真正的产品发现误分类为异常。

更合理的目标应是：

> AI 承担可验证、可恢复、低问责的执行与准备工作；人持续拥有方向、产品判断、价值边界和最终问责。

这不是文字修饰，而会改变 W0/W1、反馈回路、自动优先级和自主等级的设计。

### [P2] W0-W9 是一种分类设计，不是已经证明优于替代方案的自然规律

W0-W9 在内部较自洽，但目前没有证据证明十个生命周期坐标优于更简单的路由方式，例如：

- 低风险可逆修改：目标、diff、test；
- 普通用户可见变更：spec、implementation、verification；
- 高风险变更：risk、approval、rollback、operations；
- 事故和学习：incident、decision、follow-up。

对一个 30-120 分钟的低风险任务，先判断 W、读取相邻门禁、创建 OpenSpec 四件套、选择角色和 skill，可能比任务本身更贵。

建议用真实任务对比至少两种模型：

- 当前 W0-W9；
- 三档风险路由（quick / standard / high-risk）。

没有对照数据前，不应把 W0-W9 设为所有任务的强制入口。

### [P2] 参考体系存在选择偏差，缺少反证和失败采用研究

来源数量很多，但重点集中在 AI 厂商工程博客、新兴 agent 产品、预印本和大型工程组织方法。缺少同等强度的反方材料：

- 小团队采用重流程后效率下降的证据；
- 文档和 checklist 对认知负担的负面影响；
- automation bias、deskilling 和目标固化研究；
- solo founder 的真实时间分配和失败模式；
- AI 生成政策长期漂移、形式合规和“paper process”风险；
- 多 Agent 在软件写入任务中没有净收益的研究。

来源体系不仅要回答“为什么可以这样设计”，还要回答：

- 什么情况下不该这样设计？
- 哪些规则最可能无效？
- 什么证据会推翻当前架构？
- 哪些结论只适用于特定厂商、模型、任务或组织规模？

### [P2] 规范体系正在用自身规则证明自身正确

当前存在自指风险：

- 规范要求 OpenSpec，于是用 OpenSpec change 证明规范完整；
- 规范要求两轮 review，于是由同一体系生成 Review A/B；
- 规范要求 verifier，于是使用只检查自身结构的 verifier 给出 PASS；
- 规范要求 W9 沉淀，于是把对规范的 review 分类为 W9；
- 规范要求所有主题挂 W，于是“成功挂 W”被当作体系合理性的证据。

这些只能证明内部一致性，不能证明外部有效性。真正的外部证据应来自：

- 真实任务对照数据；
- 独立 reviewer；
- 用户/创始人的注意力与交付结果；
- 失败案例；
- 删除规则后的性能变化。

## 6. 内部一致性 Findings

### [P1] OpenSpec 生命周期与唯一事实源失真

证据：

- `README.md:55` 规定研发节奏为“一个 active change”。
- `openspec list --json` 返回 58 个 active change。
- 58 个 change 全部为 `status: complete`，没有未完成任务。
- `openspec/specs/agent-operating-model/spec.md` 不存在。
- `openspec/changes/add-operating-model-and-agent-orchestration/specs/agent-operating-model/spec.md` 存在，说明新规则仍只存在于 delta spec。
- `docs/W9-maintain/00-main.md:13` 要求把完成状态沉淀到 OpenSpec archive。

OpenSpec 官方说明：

- `openspec list` 用于列出 active changes；
- archive 会把 delta spec 合并进 `openspec/specs/`，并把 change 移入 archive；
- `openspec/specs/` 才是当前系统行为的 source of truth。

参考：

- https://raw.githubusercontent.com/Fission-AI/openspec/main/docs/getting-started.md
- https://raw.githubusercontent.com/Fission-AI/openspec/main/docs/commands.md

影响：

- 当前规则同时存在于 `docs/`、主 specs 和未归档 delta specs；
- Agent 无法可靠判断哪个 change 仍在工作；
- `openspec list` 的选择噪音持续增加；
- 新 L0/L1 行为没有进入 OpenSpec 当前规格。

建议：

1. 暂停创建新的规范 change。
2. 先对 58 个 completed change 执行 verify 和冲突审查。
3. 按依赖和时间顺序分批同步、归档。
4. 归档后确认主 specs 包含当前实际规范。
5. 恢复“默认一个 active change”的可验证状态。

归档会修改 canonical specs，应由用户明确批准后执行。

### [P1] 高影响 L0/L1 变更缺少可恢复的人工批准记录

证据：

- `openspec/changes/add-operating-model-and-agent-orchestration/proposal.md:38-44` 将以下事项列为需要人的判断：
  - 是否接受 L0 操作模型和 L1 编排协议；
  - 是否接受 A0-A4 自主等级；
  - 是否接受生产发布默认挂起的人审边界；
  - 是否投入后续调度与门禁工具化；
  - 是否固化小项目计划工件。
- 该 change 的 58 个 tasks 已全部勾选。
- 仓库中未发现包含批准人、日期、裁决结果和附加条件的 decision artifact。
- `docs/04-operating-model.md`、`docs/05-agent-orchestration.md` 当前仍为 untracked 文件。

影响：

- 下一个人或 Agent 只能看到“需要批准”和“任务已完成”，无法恢复是否真的批准；
- 高影响规则可能被误当作已生效规范；
- 违反“工件是唯一可信事实”和 canonical source 变更必须人审的项目原则。

建议：

- 在当前 change 内新增或补充明确的 decision record；
- 至少记录 `decision`、`approved_by`、`approved_at`、`conditions`、`revisit_on`；
- 未批准前把 L0/L1 标为 proposed，而不是 current policy；
- 批准后再同步主 specs、docs map 和 freshness。

### [P1] Canonical docs map 与 freshness 没有跟上结构性变更

证据：

- `knowledge/docs-map/rd-standards.json:8-53` 的 canonical entrypoints 未包含 `docs/04-operating-model.md` 和 `docs/05-agent-orchestration.md`。
- `knowledge/docs-map/rd-standards.json:76-82` 的 linked changes 未包含 `add-operating-model-and-agent-orchestration`。
- `knowledge/docs-map/rd-standards.json:83-90` 的 runtime artifacts 未包含 L0/L1 文档。
- `knowledge/freshness/rd-standards.jsonl` 最后一条记录日期为 2026-06-30。
- 当前 L0/L1 和小项目管理修改发生于 2026-07-08。
- knowledge verifier 仍返回 PASS。

影响：

- context pack 和 docs map 对 canonical 入口给出不同答案；
- freshness 记录不能证明 7 月 8 日的结构性修改已复审；
- PASS 容易制造“知识闭环已经完成”的错误印象。

建议：

- 在用户批准 L0/L1 后更新 docs map、linked change、runtime artifacts 和 freshness log；
- verifier 应检查 context pack 中出现的 canonical 入口是否也出现在 docs map；
- 结构性变更后必须产生一条 freshness 记录。

### [P1] 当前 verifier 的 PASS 被错误解释为行为验收

证据：

- `tools/verify_workflow_index.py:260-264` 只调用：
  - `check_readme`；
  - `check_start_here`；
  - `check_workflow_files`；
  - `check_index`；
  - `check_role_index`。
- 它没有检查：
  - L0/L1 文件及内容；
  - 10/10 和 30/30 承接条款；
  - active change 数量；
  - completed change 是否归档；
  - 人工批准记录；
  - maturity/autonomy 放权记录；
  - `status.md`、batch log 和 escalation artifact；
  - source evidence 等级和 freshness。
- `proposal.md:60` 却把该脚本和 `openspec validate --all` 描述为机器可验证验收。

影响：

- 格式正确被误认为行为正确；
- 新治理规则可以完全未执行，但 CI 仍显示 PASS；
- 规范越复杂，false confidence 越高。

建议：

- 保留现有脚本作为 navigation/schema verifier；
- 新增 governance verifier，检查归档、批准、freshness、独立审查和 maturity evidence；
- 使用 OpenSpec `/opsx:verify` 检查 completeness、correctness 和 coherence；
- 验证输出明确区分 `format_valid`、`governance_complete` 和 `pilot_verified`。

### [P1] 两轮自检与独立审查原则冲突

证据：

- `docs/04-operating-model.md:88` 规定“生产者与审查者分离”。
- `skills/one-person-openspec-rd/SKILL.md:54-61` 只要求执行者做 Review A 和 Review B。
- `skills/one-person-openspec-rd/references/review-rubric.md` 没有独立 reviewer、干净上下文、日期、目标版本或证据字段。
- 21 份 W 文档包含静态 Review 1/2，但几乎没有 reviewer/date/evidence 元数据。
- 多数 review 直接以“可落地”结束，无法证明是否由独立模型或独立上下文审查。

影响：

- 两个观察角度被误当作两次独立审查；
- 生产者可以为自己的工作做最终裁决；
- 用户提到的“其他模型 review”无法从仓库恢复模型身份、范围和裁决。

建议：

- Review A/B 明确改名为 producer self-check；
- Final review 由干净上下文的独立 reviewer 执行；
- 审查记录包含 reviewer、模型/版本、日期、目标 commit 或 tree、证据和结论；
- 生产者不得填写最终 merge/accept decision。

### [P2] 目标清楚，但缺少可量化成功标准和真实试运行

证据：

- `knowledge/context-packs/rd-standards.md:7-10` 的 current product bet 是降低创始人注意力成本和 Codex 上下文恢复成本。
- `docs/04-operating-model.md:112` 把 A1 标为当前默认。
- `docs/05-agent-orchestration.md:235` 把 M0 单 Agent 会话标为现状。
- 仓库不存在 `ai-coding/`、`escalations/` 或任何 change 下的 `status.md`。
- `proposal.md:55` 明确说下一步是用真实小项目试运行 M1/M2。

影响：

- 无法判断 56 份 docs、58 个 change 和新编排协议究竟降低还是增加认知成本；
- “目标态”容易被误读成“当前能力”；
- 没有数据支持从 M0/A1 升级。

建议至少定义以下指标：

- 冷启动到正确 W 和下一动作的时间与 token；
- 每个 change 需要用户判断的次数；
- 首次门禁通过率和返工次数；
- 中断 7 天后恢复上下文的成功率与耗时；
- 规范工件维护时间占交付时间的比例；
- 每个 change 的总 token、工具调用和失败重试成本。

先使用 3 个不同类型的真实小项目试运行 M1/M2，再决定是否进入 M3。

### [P2] 外部来源缺少证据等级和适用边界

总体评价：来源丰富且大多真实相关，但 source map 把厂商经验、预印本、单实例案例、个人博客和二手事故报道放在同一层级。

具体问题：

- Anthropic 的约 15 倍 token 数据来自 multi-agent research 产品；原文同时明确 coding 任务通常具有更少的可并行部分，不能无条件推广到所有研发任务。
  - https://www.anthropic.com/engineering/multi-agent-research-system
- METR 的约 7 个月翻倍是特定任务集和 50% 成功率 time horizon 的经验趋势，应保留测量口径。
  - https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/
- Springdrift 作者明确说明是单实例、单 operator 的案例研究，不是 benchmark-driven evaluation。
  - https://arxiv.org/abs/2604.04660
- MAKER 证明的是特定百万步任务在极端分解和投票条件下可以零错误，不等于所有研发流程成本都只按任务长度对数增长。
  - https://arxiv.org/abs/2511.09030
- “两个 Agent 对话 11 天、花费 4.7 万美元”来自个人博客转引的二手报道，不应在 L0 中作为无保留事实。
  - https://tianpan.co/blog/2026-04-12-backpressure-in-agent-pipelines-when-ai-generates-work-faster-than-it-can-execute

建议 source map 为关键声明增加：

- `claim_id`；
- `source_type`；
- `evidence_level`；
- `supports`；
- `applicability`；
- `limitations`；
- `reviewed_on`；
- `superseded_by`。

### [P2] 默认冷启动与 W0 仪式仍偏重

测量结果：

按当前 skill 和 context pack 的默认路径，一个新 W0 请求可能需要读取：

- `README.md`：79 行；
- `docs/00-start-here.md`：295 行；
- `docs/02-standard-index.md`：232 行；
- `knowledge/context-packs/rd-standards.md`：71 行；
- `docs/W0-intake/00-main.md`：366 行；
- 下一门禁 `docs/W1-discovery/00-main.md`：111 行。

合计约 1,154 行、55KB，尚未读取任何触发专项或当前代码。

同时：

- `docs/W0-intake/00-main.md:15` 说最小产出是 work-intake 和 decision-board；
- `docs/W0-intake/00-main.md:76-87` 又在“最小工件”下列出五类工件；
- README 和 W2 对超过 30 分钟的工作默认要求四件套 OpenSpec。

影响：

- 对低风险 30-120 分钟任务可能产生高于实现本身的规格成本；
- 路由入口消耗的上下文与“最小高信号 token 集”目标冲突；
- 一人公司可能为了合规于规范而维护没有决策价值的工件。

建议：

- 增加短小、机器可读的 workflow router manifest；
- 把长模板和字段定义移出 `00-main.md`，按需加载；
- 明确 W0 的 required、periodic 和 optional 工件；
- 用风险、可逆性和上下文恢复需求共同决定是否进入 OpenSpec，不只使用 30 分钟阈值；
- 在真实试运行中记录规格成本与实现成本之比。

## 7. 正向评价

以下设计应保留：

- W0-W9 是路由坐标而不是线性瀑布；
- 角色是泳道，不替代生命周期；
- 高影响判断集中交给人；
- T0-T3 副作用分级明确限制生产、不可逆和对外动作；
- OpenSpec 把 intent、behavior、design 和 tasks 分开；
- W3 把 AI eval 和失败样例前置；
- W5 明确“代码完成不等于完成”；
- W8/W9 负责学习、归档、freshness 和上下文恢复；
- 新增规范必须挂靠 W、角色、artifact、skill 或 verifier；
- verifier 已能有效防止 W 目录、索引和角色入口的基础结构漂移。

## 8. 最小整改顺序

### 第一步：停止扩张，重新定义这套规范的产品假设

- 暂停新增规范和新阶段。
- 明确它首先是知识库、可选 playbook，还是强制操作系统。
- 为“降低注意力和恢复成本”定义基线、目标和失败条件。
- 明确人的角色不是只有目标输入和例外审批。

### 第二步：提取最小可执行内核

- 把硬规则压缩到 10-15 条。
- 定义 quick / standard / high-risk 三档最小路径。
- 把技术栈、合规和主题资料降为按需 playbook。
- 把 source、review 和历史从默认上下文移出。

### 第三步：做对照试运行

- 选择至少 10 个真实任务，而不是只验证文档样例。
- 对比当前 W0-W9 与更简单的风险路由。
- 测量总耗时、冷启动、人工中断、返工、门禁缺陷和 token 成本。
- 用数据决定保留、删减或自动化哪些规则。

### 第四步：在方向确认后恢复仓库治理

- 对 58 个 completed active change 做 verify。
- 检查 delta spec 与主 specs 冲突。
- 分批 sync/archive。
- 归档后确认 active change 数量和主 specs。

### 第五步：修复知识与审查闭环

- 更新 docs map、context pack、freshness 和 linked changes。
- 更新 canonical skill 和 review rubric。
- 区分 producer self-check 与 independent final review。

### 第六步：只为保留下来的规则实现机器门禁

- 增加 governance verifier。
- 输出 format、governance、pilot 三种状态。
- 将 archive、approval、freshness、review evidence 和 maturity evidence 纳入检查。
- 不为尚未证明有净收益的规则继续增加脚本和 skill。

## 9. 审查时需要用户判断的事项（已处置）

用户随后授权从规范之外整改整个项目；[重置决策](../decisions/2026-07-10-rd-standards-reset.md) 保存了授权范围和未授权边界。当前 disposition：

- L0/L1、A0-A4、M0-M4 没有被接受为正式政策；
- 旧 T 分级没有被整体追认，高影响副作用必须人审的实质边界进入最小内核；
- 58 个 completed change 已核对后归档，归档结果为 58/58；
- 独立 reviewer 已成为 Standard/High-risk 的规则，但当前整改本身仍在等待独立审查；
- 允许真实试运行数据驱动删除或降级 W/OpenSpec 工件，不保留 30 分钟触发阈值；
- 项目已重定位为“最小内核 + 可选 playbook + 证据库”；
- 人持续拥有产品判断、用户理解、价值边界和最终问责。

## 10. 审查基线验证记录

本次审查执行的只读验证：

```text
python tools\verify_workflow_index.py .
PASS

python C:\Users\machinly\.codex\skills\knowledge-context-recovery-guard\scripts\verify_knowledge_context.py .
PASS

openspec validate --all
114 passed, 0 failed

openspec list --json
58 active changes; 58 complete; 0 incomplete
```

解释：以上是整改前的审查基线。前三个 PASS 只证明当时的文件格式、索引和基础知识工件可解析，不代表本报告所列治理问题已经解决。整改后的命令证据记录在 [整改审计](2026-07-10-rd-standards-remediation-audit.md)。

## 11. 报告自检 A：一人可执行性（不是整改终审）

- 本报告把整改压缩为五个顺序步骤，不要求同时修复全部规范。
- 最先处理批准、归档和 verifier，避免继续增加文件。
- 每一步都有明确输入、输出和验证方式，可由一个人在独立工作块内执行。
- 报告自身标记为 review evidence，不与 canonical 规范争夺事实源。
- 本报告当时提出的下一步是由用户裁决 L0/L1 和是否归档 completed changes；这些事项现已按第 9 节处置。

结论：通过。整改路径可以由一人串行推进，不需要并行角色或重型治理项目。

## 12. 报告自检 B：产品、工程与运维风险（不是整改终审）

- 没有建议立即扩大 Agent 自主权或执行生产动作。
- 归档、canonical spec 合并和高影响规则批准仍保留人工 checkpoint。
- 格式验证与行为验收已明确分开。
- 来源风险、维护成本、上下文成本和 rollback/side-effect 边界均已覆盖。
- 最小安全下一步是只做人工裁决和只读 verify，不执行 archive、merge、发布或其他副作用。

结论：通过。报告没有隐藏不可逆动作，且每个高优先级问题均有验证路径。

## 13. 审查时推荐的后续工作与当前结果

从外部视角看，下一步不应默认创建 OpenSpec change。应先完成“最小内核与对照试运行”的产品判断；使用 OpenSpec 记录这项判断本身，会再次预设 OpenSpec 已经是正确答案。

可以先创建一份独立实验记录：

```text
experiments/minimal-rd-kernel-comparison.md
```

实验已经创建但尚未完成。初始重置没有用 OpenSpec 证明 OpenSpec；用户后来明确决定 Standard/High-risk 实现默认启用 OpenSpec，因此两项后续整改通过 change 完成并归档。approval record、archive、docs map/freshness、独立 review contract 和必要 verifier 已落地；真实任务净收益和独立最终审查仍保持 pending，不用结构性 PASS 替代。
