# 阶段 16：知识管理、文档与上下文恢复规范

## 目标

一人公司的文档问题不是“没人写”，而是文档散落、入口不清、术语漂移、过期无提示，导致中断几周后难以恢复上下文，AI 助手也只能重新猜。第 16 阶段定义最小知识管理规范，让产品意图、系统边界、命令、常见任务、术语和未决问题有稳定入口。

默认原则：文档是代码库的一部分，必须服务下一次行动。没有入口、没有 owner、没有复审规则的文档，长期会变成噪音。

## 核心依据

- 《人月神话》：概念完整性需要共享语言和一致文档，不能只靠代码堆叠。
- 小型项目管理：小项目文档必须可维护，重点记录目标、风险、决策和下一步，而不是写大型说明书。
- Diátaxis：文档满足四种不同需求：tutorial、how-to、reference、explanation；混在一起会降低查找效率。
- Google Software Engineering at Google, Knowledge Sharing：知识共享需要机制，不应依赖单个人脑中的隐性知识。
- Google Software Engineering at Google, Documentation is Like Code：文档应有 canonical 入口、版本控制、可审查和持续维护。
- Google Developer Documentation Style Guide：技术文档应清晰、一致、面向开发者，用主动语态和可执行语言。
- Write the Docs documentation principles：在开发前或开发中写文档，让需求、规格和实现互相校准。
- Docs-as-code：文档使用与代码相同的版本控制、review 和自动化检查，降低同步成本。
- OpenSpec：变更 intent、spec、design、tasks 是研发知识的 canonical source，知识工件应链接 OpenSpec，而不是替代 OpenSpec。

## 范围

适用对象：

- 生产服务、前端应用、AI workflow、数据 schema、SLO/runbook、release、security、product discovery。
- 新人或 Codex 需要接手的项目上下文。
- 跨阶段复用的术语、命令、常见任务和故障排查入口。
- 超过 1 周的产品 bet 或架构/安全/数据/AI 高风险变更。

不适用对象：

- 一次性实验草稿，且不进入生产、不影响用户、不调用真实供应商。
- 自动生成且可随时再生成的 API reference，除非它是 canonical 入口。
- 已由 OpenSpec change 短期承载的临时讨论，前提是归档后不需要长期检索。

## 最小工件

每个产品、服务、前端应用或 AI workflow 使用同一个 `<target>` 文件名：

```text
knowledge/
  docs-map/<target>.json
  context-packs/<target>.md
  glossary/<target>.md
  how-to/<target>.md
  freshness/<target>.jsonl
```

### `knowledge/docs-map/<target>.json`

知识地图用于机器检查和入口导航，必须包含：

- `target`
- `owner`
- `audiences`
- `canonical_entrypoints`
- `diataxis_coverage`
- `context_pack`
- `glossary`
- `how_to`
- `linked_openspec_changes`
- `linked_runtime_artifacts`
- `freshness_policy`
- `human_checkpoint`
- `review_cadence`

`canonical_entrypoints` 每条必须包含：

- `title`
- `path`
- `type`：tutorial、how_to、reference、explanation、runbook、spec、adr、context_pack。
- `audience`
- `owner`
- `review_on`
- `stale_after_days`

### `knowledge/context-packs/<target>.md`

Context pack 是给人和 Codex 快速恢复上下文的入口，必须包含：

- `Mission`
- `Current Product Bet`
- `System Shape`
- `Key Commands`
- `Data / Auth / Cost / Security Boundaries`
- `AI Behavior`
- `Operational Links`
- `Current Risks`
- `Open Decisions`
- `Handoff Prompt`

默认控制在 200 行以内。Context pack 不复制所有规范，只链接 canonical artifacts。

### `knowledge/glossary/<target>.md`

术语表必须包含：

- `Domain Terms`
- `Bounded Context Language`
- `API Names`
- `Data Names`
- `AI Terms`
- `Avoided Terms`

术语表的目的不是写百科，而是防止同一个概念在产品、代码、数据库、prompt、UI 中有多个名字。

### `knowledge/how-to/<target>.md`

常见任务入口必须包含：

- `Setup`
- `Develop`
- `Test`
- `Run Locally`
- `Release`
- `Rollback`
- `Debug`
- `Update Knowledge`

每个任务只写最短可执行步骤和链接，不写长篇背景。

### `knowledge/freshness/<target>.jsonl`

记录知识工件复审和过期处理：

```json
{"date":"2026-06-24","target":"ai-assistant","doc":"knowledge/context-packs/ai-assistant.md","change":"reviewed","reason":"stage 16 baseline","result":"fresh","reviewer":"solo-founder"}
```

默认在 release、incident、security change、schema migration、AI workflow change、product pivot 后追加记录。

## Diátaxis 裁剪规则

一人公司不需要每个 target 都立刻写四大类完整文档，但必须在 docs map 中明确当前覆盖：

- tutorial：只有外部用户、插件、SDK、CLI 或复杂 onboarding 需要。
- how-to：生产 target 必须有，因为它保护常见动作。
- reference：API、config、schema、events、flags、telemetry 需要链接 reference。
- explanation：架构、产品 bet、AI 行为、安全边界用 explanation 或 ADR 解释为什么。

## Codex 上下文恢复规则

每次让 Codex 接手一个 target，优先读取：

1. `knowledge/docs-map/<target>.json`
2. `knowledge/context-packs/<target>.md`
3. 当前 OpenSpec change
4. 相关阶段 skill
5. 具体任务涉及的 artifact

Context pack 的 `Handoff Prompt` 应短到可以直接复制给 Codex，包含目标、当前状态、必须遵守的边界和下一步。

## 文档风格默认规则

- 用中文记录项目事实和流程；命令、路径、API 名称、字段名保留英文。
- 用主动语态、祈使句和可执行步骤。
- 每个文档开头说明目标、适用范围和最后复审日期。
- 避免“显而易见”的长解释；链接 canonical artifact。
- 不在文档中记录 secret、private key、用户个人信息、完整 prompt/response 或生产凭据。
- 文档变更应随相关 OpenSpec、release、incident、migration 或 config change 一起更新。

## 需要人判断的关键点

只把这些知识判断交给人：

- 哪个文档是 canonical source。
- 术语是否代表真实产品语言。
- 哪些文档可以删除、归档或降级为历史记录。
- Context pack 是否足够让人/Codex 接手。
- 高风险变更后是否需要立即复审知识工件。

其他索引、字段完整性、路径存在性、过期提醒由 Codex 和脚本检查。

## Review 1：一人公司注意力审查

- 保留：五类工件都是入口型，不要求写厚文档。
- 保留：人只判断 canonical、术语、删除/归档和 handoff 是否足够。
- 调整：不强制 tutorial；一人公司早期多用 how-to、reference 和 context pack。
- 调整：freshness log 只在 release/incident/pivot/高风险变更后记录，避免日常噪音。
- 风险：context pack 可能复制太多内容。缓解：限制 200 行以内，并要求链接 canonical artifacts。

结论：可落地。该规范把“知识恢复”变成一组小入口，适合一人公司和 Codex 长期协作。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：glossary 和 current product bet 能减少产品语言漂移。
- 工程角度：context pack 链接架构、测试、配置、观测性和 release artifacts，减少重复探索。
- 运维角度：how-to、runbook、incident、SLO 入口统一，能缩短排障准备时间。
- 安全隐私角度：明确禁止 secret、PII 和原始 prompt/response 进入知识工件。
- 成本角度：删除/归档过期文档，减少人和 AI 的上下文浪费。

结论：可落地。第 16 阶段补上“研发知识如何被下一次行动使用”的闭环。
