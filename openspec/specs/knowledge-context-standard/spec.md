# knowledge-context-standard Specification

## Purpose

定义一人公司知识管理、文档与上下文恢复的最小基线，使生产 target 拥有稳定文档入口、上下文包、术语表、常见任务 how-to 和复审记录，降低中断后难以恢复、Codex 接手靠猜、术语漂移和过期文档误导的风险。

## Requirements

### Requirement: 生产 target 必须定义知识入口和上下文包

生产服务、前端应用、AI workflow、超过 1 周的 product bet 或高风险架构/安全/数据变更 MUST 具备知识管理 artifacts。

#### Scenario: 新生产 target 进入研发

- GIVEN 一个 target 会进入生产或需要长期维护
- WHEN 创建 OpenSpec change
- THEN 创建 `knowledge/docs-map/<target>.json`
- AND 创建 `knowledge/context-packs/<target>.md`
- AND 创建 `knowledge/glossary/<target>.md`
- AND 创建 `knowledge/how-to/<target>.md`

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
