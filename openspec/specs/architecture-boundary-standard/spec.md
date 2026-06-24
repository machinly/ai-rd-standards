# architecture-boundary-standard Specification

## Purpose

定义一人公司架构决策、代码组织与模块边界的最小基线，使生产服务、前端应用和用户可见 AI workflow 能记录重要架构决策、模块职责、依赖方向、API/data/AI 边界和架构例外人审点。

## Requirements

### Requirement: 架构显著变更必须定义架构边界工件

影响依赖方向、服务边界、数据所有权、API contract、AI tool boundary、shared package、框架或供应商 SDK 的变更 MUST 具备 architecture artifacts。

#### Scenario: 新生产 target 进入研发

- GIVEN 一个服务、前端应用或 AI workflow 会进入生产
- WHEN 创建影响架构边界的 OpenSpec change
- THEN 创建 `architecture/boundaries/<target>.json`
- AND 创建 `architecture/module-maps/<target>.md`
- AND 创建 `architecture/dependency-rules/<target>.json`
- AND 在 OpenSpec design 中链接相关 architecture artifacts

#### Scenario: 架构显著决策

- GIVEN 一个决策影响结构、非功能特性、依赖、接口、数据、构建、部署或供应商锁定
- WHEN 决策被 proposed 或 accepted
- THEN 创建或更新 `architecture/decisions/<yyyymmdd>-<decision>.md`

### Requirement: ADR 必须记录 context、decision 和 consequences

Architecture decision record MUST 记录状态、背景、决策、后果、备选方案、复审日期和替代关系。

#### Scenario: 创建 ADR

- GIVEN 一个架构显著决策
- WHEN 创建 `architecture/decisions/<yyyymmdd>-<decision>.md`
- THEN 文档包含 Status、Context、Decision、Consequences、Alternatives、Review Date、Supersedes

#### Scenario: 替代旧决策

- GIVEN 一个新 ADR supersedes 旧 ADR
- WHEN 更新架构决策
- THEN 旧 ADR 不得删除
- AND 旧 ADR 或新 ADR 记录 superseded 关系

### Requirement: Boundary record 必须定义模块、依赖、API、数据和 AI 边界

Boundary record MUST 用机器可检查格式记录 target、owner、bounded context、modules、dependency direction、allowed/forbidden dependencies、external interfaces、data ownership、api contracts、ai boundaries、source roots、ADR links、人审点和复审节奏。

#### Scenario: 创建 boundary record

- GIVEN 一个 target 需要架构边界
- WHEN 创建 `architecture/boundaries/<target>.json`
- THEN 文件包含 `target`、`owner`、`status`、`bounded_context`、`modules`、`dependency_direction`、`allowed_dependencies`、`forbidden_dependencies`、`external_interfaces`、`data_ownership`、`api_contracts`、`ai_boundaries`、`source_roots`、`adr_links`、`human_checkpoint`、`review_cadence`

#### Scenario: 定义 module

- GIVEN boundary record 包含 modules
- WHEN 校验 modules
- THEN 每个 module 包含 `name`、`type`、`path`、`owns`、`public_api`、`may_depend_on`、`must_not_depend_on`

### Requirement: Module map 必须让人恢复系统结构

Module map MUST 以 Markdown 记录 context、containers、modules、dependency direction、data ownership、API contracts、AI boundaries、operational boundaries 和 open decisions。

#### Scenario: 创建 module map

- GIVEN 一个 target 需要人读架构上下文
- WHEN 创建 `architecture/module-maps/<target>.md`
- THEN 文档包含 Context、Containers、Modules、Dependency Direction、Data Ownership、API Contracts、AI Boundaries、Operational Boundaries、Open Decisions

### Requirement: Dependency rules 必须能检查禁止依赖

Dependency rules MUST 记录 source roots、rules、exceptions 和 human checkpoint，并能检查禁止 import 或跨边界依赖。

#### Scenario: 创建 dependency rules

- GIVEN 一个 target 有代码边界
- WHEN 创建 `architecture/dependency-rules/<target>.json`
- THEN 文件包含 `target`、`source_roots`、`rules`、`exceptions`、`human_checkpoint`
- AND 每条 rule 包含 `name`、`applies_to`、`forbidden_imports`、`reason`、`severity`

#### Scenario: 接受 dependency exception

- GIVEN 代码需要违反 dependency rule
- WHEN 添加 exception
- THEN `exceptions` 记录 rule、path、reason、owner、expires_on
- AND `human_checkpoint.required_for` 包含 `dependency_exception` 或等价条目

### Requirement: Go/Kratos 服务必须遵守默认依赖方向

Go/Kratos/sqlc/gRPC 服务 MUST 将 API contract、启动、transport、domain/usecase、data adapter、server wiring 和 AI workflow 边界分开。

#### Scenario: Go/Kratos target

- GIVEN boundary record 表示 stack 包含 Go 或 Kratos
- WHEN 定义 modules
- THEN module paths 覆盖 api、cmd、internal/biz、internal/data、internal/service 或等价结构
- AND `internal/biz` 或 domain module 的 `must_not_depend_on` 覆盖 data、transport、SQL driver、model vendor SDK 中适用项

#### Scenario: sqlc repository

- GIVEN target 使用 sqlc
- WHEN 定义 data ownership
- THEN data adapter module 记录 sqlc query/schema ownership
- AND domain/usecase module 不直接 import generated sqlc package，除非有 dependency exception

### Requirement: Vite 前端必须显式区分 feature 与 shared

Vite frontend target MUST 显式记录 feature boundaries、shared UI/lib 规则和跨 feature 交互方式。

#### Scenario: Vite target

- GIVEN boundary record 表示 frontend 是 Vite
- WHEN 定义 module map
- THEN module map 记录 feature/route 结构
- AND boundary record 或 dependency rules 禁止 feature 私自 import 其他 feature 的 private files

### Requirement: AI workflow 必须定义 prompt、tool、model 和审批边界

AI workflow MUST 记录 prompt builder 位置、tool port、model/vendor adapter、eval fixtures、权限、成本、dry-run/approval 和审计边界。

#### Scenario: AI workflow target

- GIVEN boundary record 表示包含 AI workflow
- WHEN 定义 ai boundaries
- THEN `ai_boundaries` 记录 prompt_builder、tool_ports、model_adapters、eval_fixtures、approval_required_for、audit_log
- AND dependency rules 禁止 domain module 直接 import model vendor SDK 或 production writer adapter

### Requirement: 架构例外必须人工 checkpoint

新增 service、shared package、public API、data ownership change、cross-service sync call、新框架/供应商 SDK、agent runtime、dependency exception、实验转生产 MUST 有人工 checkpoint。

#### Scenario: 架构锁定动作

- GIVEN 变更会引入长期架构锁定
- WHEN 更新 architecture artifacts
- THEN `human_checkpoint.required_for` 记录对应动作
- AND ADR 记录 alternatives、consequences 和 review date
