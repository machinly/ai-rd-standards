# knowledge-context-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义一人公司知识管理、文档与上下文恢复的最小基线，使生产 target 拥有稳定文档入口、上下文包、术语表、常见任务 how-to 和复审记录，降低中断后难以恢复、Codex 接手靠猜、术语漂移和过期文档误导的风险。
## Requirements
### Requirement: 生产 target 必须定义知识入口和上下文包

生产服务、前端应用、AI workflow、超过 1 周的 product bet 或高风险架构/安全/数据变更 MUST 在 `governance/knowledge/` 具备知识管理 artifacts，并由项目根导航链接。

#### Scenario: 新生产 target 进入研发

- GIVEN 一个 target 会进入生产或需要长期维护
- WHEN 创建 OpenSpec change
- THEN 创建 `governance/knowledge/docs-map/<target>.json`
- AND 创建 `governance/knowledge/context-packs/<target>.md`
- AND 创建 `governance/knowledge/glossary/<target>.md`
- AND 创建 `governance/knowledge/how-to/<target>.md`

#### Scenario: 仅本地实验

- GIVEN 一个实验不会进入生产、不会访问生产数据、不会对用户开放
- WHEN 不创建 knowledge artifacts
- THEN 在 OpenSpec tasks 或 design 中记录跳过原因

### Requirement: Docs map 必须定义 canonical 入口、覆盖类型和复审策略

Docs map MUST 用机器可检查格式记录 target、owner、audiences、canonical entrypoints、Diátaxis coverage、context pack、glossary、how-to、OpenSpec links、runtime artifact links、freshness policy、人审点和复审节奏。

#### Scenario: 创建 docs map

- GIVEN 一个 target 需要知识入口
- WHEN 创建 `knowledge/docs-map/<target>.json`
- THEN 文件包含 `target`、`owner`、`audiences`、`canonical_entrypoints`、`diataxis_coverage`、`context_pack`、`glossary`、`how_to`、`linked_openspec_changes`、`linked_runtime_artifacts`、`freshness_policy`、`human_checkpoint`、`review_cadence`

#### Scenario: 定义 canonical entrypoint

- GIVEN docs map 包含 canonical_entrypoints
- WHEN 校验 entrypoint
- THEN 每条 entrypoint 包含 `title`、`path`、`type`、`audience`、`owner`、`review_on`、`stale_after_days`
- AND `path` 指向仓库内存在的文件

### Requirement: Context pack 必须足够支持人和 Codex 接手

Context pack MUST 记录 mission、current product bet、system shape、key commands、boundaries、AI behavior、operational links、risks、open decisions 和 handoff prompt。

#### Scenario: 创建 context pack

- GIVEN 一个 target 需要上下文恢复
- WHEN 创建 `knowledge/context-packs/<target>.md`
- THEN 文档包含 Mission、Current Product Bet、System Shape、Key Commands、Data / Auth / Cost / Security Boundaries、AI Behavior、Operational Links、Current Risks、Open Decisions、Handoff Prompt

### Requirement: Glossary 必须稳定产品、代码、数据和 AI 语言

Glossary MUST 记录 domain terms、bounded context language、API names、data names、AI terms 和 avoided terms。

#### Scenario: 创建 glossary

- GIVEN 一个 target 有产品或技术术语
- WHEN 创建 `knowledge/glossary/<target>.md`
- THEN 文档包含 Domain Terms、Bounded Context Language、API Names、Data Names、AI Terms、Avoided Terms

### Requirement: How-to 必须覆盖常见行动入口

How-to MUST 记录 setup、develop、test、run locally、release、rollback、debug 和 update knowledge 的最短可执行步骤。

#### Scenario: 创建 how-to

- GIVEN 一个 target 需要人或 Codex 执行常见任务
- WHEN 创建 `knowledge/how-to/<target>.md`
- THEN 文档包含 Setup、Develop、Test、Run Locally、Release、Rollback、Debug、Update Knowledge

### Requirement: Freshness log 必须记录重要知识复审

Release、incident、security/data/AI/config 高风险变更、product pivot 后 MUST 追加 freshness 记录或说明不适用。

#### Scenario: 记录 freshness

- GIVEN target 的知识工件被复审
- WHEN 写入 `knowledge/freshness/<target>.jsonl`
- THEN 每行 JSON 包含 `date`、`target`、`doc`、`change`、`reason`、`result`、`reviewer`
- AND `doc` 指向仓库内存在的文件

### Requirement: 知识工件不得包含敏感内容

Knowledge artifacts MUST NOT 包含 secret、private key、生产凭据、用户个人联系信息、完整 prompt/response 或生产连接串。

#### Scenario: 写入知识工件

- GIVEN 更新 docs map、context pack、glossary、how-to 或 freshness
- WHEN 运行检查
- THEN 不得出现 password、secret、token、private key、database URL、完整 email、手机号或完整 prompt/response 内容

### Requirement: Canonical 和过期例外必须人工 checkpoint

改变 canonical source、删除/归档文档、接受过期文档、术语变更、context pack 不足以接手 MUST 有人工 checkpoint。

#### Scenario: 接受过期文档

- GIVEN entrypoint 超过 stale_after_days 或 review_on 已过期
- WHEN 准备继续使用
- THEN `human_checkpoint.required_for` 包含 `stale_doc_accepted` 或更新 freshness 记录

### Requirement: 项目必须提供统一治理根和项目地图

Standard/High-risk 项目 MUST 将流程/guard 工件放在 `governance/<registered-domain>/`，并提供 `governance/README.md` 与 `governance/project-map.json`，说明全部顶层目录、正式源码与过程证据、推荐阅读顺序、运行进程、常用命令和权威来源。

#### Scenario: 新 guard 创建工件

- GIVEN guard 建议写入 `quality/`、`auth/`、`reviews/` 或其他根目录
- WHEN 项目使用统一治理根
- THEN 将路径重映射到 `governance/<registered-domain>/`
- AND 更新 project map 中的 domain registry
- AND 不新增未登记的治理顶层目录

#### Scenario: 新会话接手项目

- GIVEN Codex 只获得仓库路径
- WHEN 阅读根 README 和 governance/project-map.json
- THEN 能区分源码、运行资产和过程证据
- AND 能找到 active OpenSpec、当前状态、关键旅程、运行进程和常用命令
