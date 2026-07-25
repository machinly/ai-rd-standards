---
name: one-person-openspec-rd
description: "Route solo AI-assisted R&D through Quick, Standard, or High-risk paths, defaulting Standard/High-risk implementation changes to OpenSpec while keeping Quick lightweight. Use for planning, implementing, reviewing, or governing AI-assisted product and engineering work."
---

# Minimal Solo R&D Router

## Purpose

帮助一个人在不增加无价值仪式的前提下，选择足够安全的研发路径。人的产品判断、价值边界和最终问责不可外包。

## Default Reading

把当前任务所在项目的仓库根记为 `<repo-root>`；仓库路径始终相对 `<repo-root>` 解析，不能相对本 skill 目录解析。

1. 先读 `<repo-root>/README.md`。
2. 按任务的主要决定只读一个分类入口：
   - `docs/01-initiation/README.md`
   - `docs/02-product-design/README.md`
   - `docs/03-engineering-delivery/README.md`
   - `docs/04-operations-maintenance/README.md`
3. 再读该分类中一个或少数直接相关的项目正文，不默认扫描全部十一项。

如果项目仓库没有自己的正式研发入口，改读本 skill 自带的 `references/workflow-map.md`；这是明确 fallback，不要把它当成项目事实。只有实际实现需要确认 Go、前端或数据默认时，才读 `references/stack-defaults.md`。

## Route

### Quick

用于低风险、可逆、无用户/生产/敏感数据影响的工作。

- 不强制创建 OpenSpec 或流程文件。
- 完成后给出产物、验证和剩余风险。

### Standard

用于用户可见、跨文件、跨会话、AI 行为或需要独立验收的工作。

- 在实现前创建或继续一个 OpenSpec change。
- 用 proposal/specs/design/tasks 写清 outcome、non-goals、acceptance、risks、verification、rollback 和 next；`tasks.md` 是执行状态的权威来源。
- 新用户能力、新服务或重大体验变化在生产性实现前，确认产品输入和体验设计；OpenSpec 只链接它们，不能替代。用户可见 Standard/High-risk change 还要在 proposal 记录 `visual_ux: required | not-required` 与理由；required 时须链接当前静态 UX 和明确的人类 `approved` review 后再开始相关生产性实现。
- 用户可见工作先在 `governance/quality/user-journeys.json` 定义少量关键旅程，并在扩大专项工件前尽早跑通一条真实 Browser E2E。
- 新应用先从批准模板生成并记录 template/version/revision、命令和首次构建；当前 Go 服务使用 Kratos CLI，未来可由自有应用模板替换。
- 多组件项目定义一套完整本地集成环境，统一启动、等待、smoke 和清理全部后端、前端与依赖；前端可运行在宿主机，但不能缺席完整集成验收。
- 最终 reviewer 不能是生产者。

### High-risk

用于生产、客户数据、安全、权限、凭据、付款、公开承诺、外部通信或不可逆操作。

- 在执行副作用前取得明确人类批准。
- 产品决策、权限边界或验收设计未确认时，只做澄清/原型，不进入生产性代码、migration 或稳定 API。
- auth、数据迁移、管理员权限和难回退契约在实现前先由未参与设计的人审查风险与回滚。
- 记录 impact、stop conditions、rollback、decision owner 和 evidence。
- 权限不足或门禁失败时停止，不绕过。

## OpenSpec

Quick 不创建 OpenSpec。Standard/High-risk 的代码、配置、schema、API、AI 行为、数据、基础设施或发布设计变更，默认在实现前创建或继续一个 OpenSpec change，并先运行 strict validation。

纯产品澄清、只读 review、报告和事故止血不自动创建 change；它们产生后续实现时再创建。只有用户明确批准并记录 decision owner、理由、适用范围和恢复方式时，Standard/High-risk 实现性变更才可跳过。不要用“已有文档足够”自行豁免。

OpenSpec 只记录本次 change 增量并链接产品、体验、review 和验证证据。`tasks.md` 替代重复 work brief；OpenSpec validation 不替代真实验收、独立审查或发布批准。

所有 guard/流程工件默认写入 `governance/<registered-domain>/`；若专项 skill 给出旧的根目录相对路径，重映射到 governance domain，并更新 `governance/project-map.json`。项目使用 `governance/current-status.json` 作为单一当前状态；较新的 `changes_requested`、失败旅程或失效 manifest 否决旧完成摘要。

## Multi-Agent

默认单 Agent。只有任务可独立切分、写域不重叠且有基线证据时，才进行有限的多 Agent 协作；并行结果必须由主执行者整合和验证。

## Review

- 所有路径都做 producer self-check。
- Standard 和 High-risk 需要独立 final review。
- High-risk 的 auth/data/admin/irreversible 设计还需要 pre-implementation independent review，不能只在完成后审。
- 独立 reviewer 不能是产出生产者，并记录目标版本、证据和结论。
- reviewer 对照权威产品输入、体验设计和验收映射，不以 OpenSpec 代替需求；`visual_ux: required` 时还核对当前人类批准、实现偏差和重新 review 证据。
- 用户可见范围由陌生验收者从干净完整环境执行关键旅程；review 轮数不算质量指标。
- unit、integration、依赖容器、完整本地集成、浏览器 E2E 和真实 provider 证据必须分开命名。
- 同一执行者的 Review A/B 只是两种自检视角，不是两次独立审查。

使用 references/review-rubric.md。

## Completion

最终总结包含：

- 选择的路径及原因；
- 变更或产物；
- 验证证据；
- 剩余风险；
- 实际证据层级和明确未覆盖项；
- done、stopped 或 terminated 的真实状态；
- 新应用的模板 provenance 或明确的不适用原因；
- OpenSpec change id、validation 和 archive/review 状态，或经用户批准的跳过记录；
- 用户可见 Standard/High-risk 的 `visual_ux` 判定；required 时包含批准状态与当前工件入口；
- 需要人的决策；
- 如果使用了 playbook 或多 Agent，说明它产生的净收益；同时记录 OpenSpec 的实际维护成本和是否减少返工/恢复成本。
