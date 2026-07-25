---
status: ready-for-independent-review
producer: Codex
target_revision: sha256-tree:d50e56c5778a3a46330d63683cd9e6a6729e4c41e3e05ff5de9cee017e2ef8ed
producer_self_check: complete
independent_decision: pending
---

# 研发规范整改：独立审查交接包

本文件供未参与本次整改的 reviewer 使用。它只规定审查输入、覆盖范围和拒绝条件，不预填接受结论。

当前工作树没有 commit，但使用 [逐文件 SHA-256 manifest](2026-07-10-rd-standards-snapshot-manifest.json) 形成内容寻址快照。`target_revision` 必须与 manifest 的 `tree_sha256` 一致；任何非审查记录文件变化都会使快照检查失败。

## 审查目标

判断 [外部元审查](2026-07-10-rd-standards-review.md) 提出的结构性问题是否在目标版本中真实关闭，同时确认仓库没有把未完成的 pilot、生产者自检、格式验证或历史规范包装成有效性证明。

独立审查不负责宣布新流程已经有效。流程净收益只能由 [10 项真实任务试验](../experiments/minimal-rd-kernel-comparison.md) 证明。

## 必读输入

按以下顺序读取，避免被历史 W/OpenSpec 叙事先入为主：

1. [用户授权与边界](../decisions/2026-07-10-rd-standards-reset.md)
2. [OpenSpec 默认启用决策](../decisions/2026-07-11-default-enable-openspec.md)
3. [原始外部审查](2026-07-10-rd-standards-review.md)
4. [README](../README.md)
5. [快速分流](../docs/00-start-here.md)
6. [最小研发内核](../docs/01-minimal-rd-kernel.md)
7. [逐项整改审计](2026-07-10-rd-standards-remediation-audit.md)
8. [首轮用户中心终止证据回灌](2026-07-10-user-center-experiment-ingestion.md)
9. [第二轮用户中心复盘回灌](2026-07-11-user-center-pilot-2-ingestion.md)
10. [去敏 pilot 聚合记录](../experiments/rd-standard-pilot.jsonl)
11. [runtime skill 同步证据](2026-07-10-runtime-skill-sync-evidence.json)
12. 目标版本相对整改前基线的完整 diff
13. [治理验证器](../tools/verify_rd_standards.py)与[项目证据验证器](../tools/verify_project_evidence.py)源码

按需抽查：

- [可选 playbook 索引](../docs/02-standard-index.md) 与 40 份 W 文件的状态头；
- [OpenSpec 资产说明](../openspec/README.md) 与 56 份主规格的状态头；
- [轻量 planning 主规格](../openspec/specs/roadmap-prioritization-work-intake-standard/spec.md)；
- [轻量 AI coding 主规格](../openspec/specs/ai-coding-workflow-standard/spec.md)；
- [review contract](../skills/one-person-openspec-rd/references/review-rubric.md)；
- [证据政策](../docs/sources/README.md) 与 [关键声明 registry](../docs/sources/evidence-registry.jsonl)。

## 必须独立回答的问题

### 1. 默认路径是否真的改变

- 普通任务是否可以不定位 W0-W9？
- Quick 是否可以不创建 work brief、OpenSpec 或 review 文件？
- Standard/High-risk 实现是否默认创建或继续一个 OpenSpec change，同时避免恢复旧四件套和全量 W0-W9？
- 试点 schema 是否显式记录 OpenSpec 使用；Standard/High-risk 没有批准而跳过时，是否能诚实保留为负面证据但绝不计入 eligible？
- High-risk 是否由影响和不可逆性触发，而不是耗时触发？

### 2. 历史材料是否会重新夺回规范效力

- 40 份 W 文档是否逐份标为可选？
- 56 份主规格是否逐份在文件内标为可选历史主题规格？
- 小型项目管理草案是否明确撤销“已纳入正式规范”和半天门槛？
- playbook 内的 `MUST` 是否只在主动选择相应主题后适用？

### 3. 当前能力描述是否真实

- 是否明确没有多 Agent 调度器、自动策略门或无人值守生产 runtime？
- 实验性编排是否被描述为待验证，而不是当前已实现能力？
- 是否仍有未经验证的 L0/L1、A0-A4、M0-M4 默认等级？

### 4. 人的责任与审查是否真实分离

- 产品方向、用户理解、价值边界和最终问责是否持续属于人？
- Producer Self-Check 是否与 Independent Final Review 明确分离？
- 是否还存在预填“可落地”“风险可控”或 Review A/B 充当最终接受？
- 当前整改是否诚实保持 `independent_decision: pending`？

### 5. 生命周期与知识入口是否一致

- 60 个 completed change 是否都有归档目标，active 是否为 0？
- docs map、context pack、freshness 和 README 是否指向同一默认入口？
- archive、历史 specs 和当前默认规则是否被清楚区分？

### 6. 验证器是否检查了关键语义

- 是否检查三档路径、人的责任、可选 W/OpenSpec、审查分离、证据政策和归档数量？
- 是否检查 56 份主规格的文件内可选状态？
- 是否拒绝半天 planning 触发、L0/L1 默认等级和静态自评结论？
- `governance_complete` 是否明确只代表结构，不代表 pilot 或独立接受？

### 7. 未完成项是否被诚实保留

- pilot 是否仍显示实际完成数量，而不是把本次整改自动计入？
- 第二轮外部八条 checkpoint 是否因缺 schema、指标不可比和 Browser E2E 过强命名而只汇总为一条 `changes_requested` 负面记录？
- evidence registry 是否承认只是第一阶段，而不是宣称覆盖全部来源？
- 是否存在任何用文件数量、格式 PASS 或自检替代真实效果的表述？
- 第二轮用户中心是否诚实保持 `changes_requested`，没有被包装成 completed 样本？

### 8. 第二轮回灌是否真正关闭产品验收缺口

- 关键用户旅程是否先于大量治理工件，并能映射到真实页面动作和结果？
- `browser-e2e` 是否只允许可重复自动化真实浏览器旅程；人工检查是否明确降级命名？
- 最新 `changes_requested`、失败旅程或失效 manifest 是否会使旧完成摘要失效？
- governance root、project map、current status 和多个 Go `cmd` 注册表是否形成可验证导航？
- 新增治理域是否需要可观察用途和保留策略，而不是追求文件数量？

### 9. 证据体系是否同时登记支持与反证

- 原 review 点名的 Anthropic、METR、Springdrift、MAKER 和二手成本故事是否保留适用边界？
- registry 是否使用 `challenges` 单独登记反证，而不是把所有来源都包装成支持当前规则？
- 早期 METR slowdown 是否通过 `superseded_by` 连接到后续测量更新，并保留两轮研究各自限制？
- 历史 source map 是否仍明确不能直接证明强制规则？

## 复现命令

```powershell
python tools\verify_rd_standards.py . --json
python tools\verify_pilot_records.py . --json
python tools\test_verify_pilot_records.py -v
python tools\test_verify_project_evidence.py -v
python tools\check_runtime_skill_sync.py . --json
python tools\build_review_snapshot.py . --check
python tools\verify_workflow_index.py .
python C:\Users\machinly\.codex\skills\knowledge-context-recovery-guard\scripts\verify_knowledge_context.py . --legacy-root
openspec validate --all
openspec list --json
git diff --check
```

还应人工核对：

- `openspec/changes/archive/` 下恰有 60 个目录；
- 被删除的 232 个旧 active 文件均有对应 archive 文件；
- 非归档 Markdown 本地链接没有断链；
- 默认三文件总行数不超过 350；
- verifier 的两条 pending 警告没有被隐藏。
- runtime skill sync 返回 PASS，且 reviewer 抽查 router 全文件同步与 Go service skill/verifier 的关键契约。
- `build_review_snapshot.py --check` 对目标快照返回 PASS。

## 直接拒绝条件

命中任一项时不得接受：

- 默认入口要求先定位 W0-W9 或按时长创建 OpenSpec；
- 生产者给自己填写 independent accept；
- `pilot_verified` 在少于 10 条合格记录、少于 3 个项目、A/B/恢复配额不足或效果阈值失败时为 true；
- 仓库声称已有不存在的多 Agent/无人值守 runtime；
- 归档文件缺失、completed change 仍 active 或主规格验证失败；
- 关键来源没有适用边界却被用来证明强制规则；
- 只检查文件存在或格式，不检查上述语义；
- reviewer 无法确定自己审查的目标版本。
- packet 的 `target_revision` 与 snapshot manifest 不一致。
- 多组件项目可以在缺少前端或只有依赖容器时被声明为完整本地集成。
- 新应用可以手工仿造批准模板，或 runtime skill 漂移不阻止下一轮 pilot。

## 独立审查记录

```text
Reviewer:
Reviewed at:
Target revision or immutable snapshot:
Scope:
Commands rerun:
Evidence sampled:
Findings:
Decision: accept | changes-requested | reject
Residual risks:
```

如果 Decision 为 `changes-requested` 或 `reject`，先修复 findings，再由独立 reviewer 复查；生产者不得自行把 `independent_decision` 改为 accepted。

如果整改内容发生变化，先运行 `python tools\build_review_snapshot.py .` 重新生成 manifest，再把新的 `sha256-tree` 写入本文件。只有 reviewer 自己的记录可以在不改变目标快照的情况下更新，因为本 packet 被明确排除在 hash 之外。
