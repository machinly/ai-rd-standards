# 架构决策、代码组织与模块边界规范
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/one-person-ai-rd-operating-model.md 的场景触发规范命中“架构边界、模块职责、数据所有权或依赖方向变化”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/one-person-ai-rd-operating-model.md。
## 目标

一人公司最容易累积的长期债务，是代码一开始跑得很快，几个月后所有东西互相依赖，任何改动都牵动后端、前端、数据库、prompt、权限和发布。本触发专项定义最小架构边界规范，让重要架构决策、模块职责、依赖方向、API/data/AI 边界能被记录和检查。

默认原则：不为未来假想规模设计复杂架构，但所有会影响依赖方向、数据所有权、API contract、AI 工具边界或供应商锁定的决定，必须写入架构工件。

## 核心依据

- 《人月神话》：概念完整性比人员堆叠更重要；架构边界应服务于一致的系统概念，而不是组织图或临时文件夹。
- 小型项目管理：只记录高影响决策和可恢复上下文，不创建大型架构文档。
- D. L. Parnas 模块分解：模块化的价值取决于分解标准，模块应隐藏可能变化或困难的设计决策。
- Michael Nygard ADR：记录影响结构、非功能特性、依赖、接口或构建技术的架构决策，并保留 context、decision、consequences。
- C4 Model：多数团队只需要 context 和 container 级别视图；只有有价值时再展开 component/code。
- Domain-Driven Design / Bounded Context：当语言、规则或模型含义变化时，应显式划分边界和上下游关系。
- Ports and Adapters：核心应用应通过 port 与外部技术连接，数据库、HTTP、gRPC、CLI、AI model、test harness 都是 adapter。
- Go 官方模块组织与 `internal`：Go 用 package/module 和 `internal` 目录表达可见性边界。
- Kratos layout：Kratos 默认用 `api`、`cmd`、`configs`、`internal` 和 DDD 风格结构组织服务。
- Vite / React：Vite 以 project root 和 `index.html` 为入口；前端文件结构应优先按 feature/route 贴近用户心智，避免过深嵌套。
- OpenAI prompt engineering / Agents：生产 prompt builder 应靠近 feature，使用 typed inputs；只有应用拥有编排、工具执行、审批和状态时才引入 Agents SDK。
- Google SRE Simplicity：清晰、最小 API 和松耦合能同时提高稳定性与敏捷性。

## 范围

适用对象：

- 新服务、新 bounded context、新 Go module、服务拆分或合并。
- 影响 `api/`、`internal/`、`pkg/`、`web/src/features`、AI workflow、数据库 schema 所有权的改动。
- gRPC/Protobuf contract、数据所有权、外部供应商、AI tool、权限边界变化。
- 引入新框架、跨服务同步调用、共享 package、shared kernel、SDK 或公共前端组件库。

不适用对象：

- 只改局部实现且不改变依赖方向、接口、数据所有权或可见性。
- 小 bug fix，前提是没有新增跨模块 import 或公共 API。
- 一次性实验代码，前提是标明过期日期且不进入生产。

## 最小工件

每个生产系统、服务、前端应用或 AI workflow 使用同一个 `<target>` 文件名：

```text
architecture/
  decisions/<yyyymmdd>-<decision>.md
  boundaries/<target>.json
  module-maps/<target>.md
  dependency-rules/<target>.json
```

### `architecture/decisions/<yyyymmdd>-<decision>.md`

使用轻量 ADR，必须包含：

- `Status`：proposed、accepted、superseded、deprecated。
- `Context`：触发决策的事实和约束。
- `Decision`：这次采用什么。
- `Consequences`：正面、负面和中性后果。
- `Alternatives`：至少一个被拒方案。
- `Review Date`：什么时候复审。
- `Supersedes`：如果替代旧决策，写旧 ADR。

默认只为架构显著决策写 ADR：结构、依赖、接口、数据、非功能约束、构建或部署技术。

### `architecture/boundaries/<target>.json`

用于机器检查，必须包含：

- `target`、`owner`、`status`、`bounded_context`
- `modules`
- `dependency_direction`
- `allowed_dependencies`
- `forbidden_dependencies`
- `external_interfaces`
- `data_ownership`
- `api_contracts`
- `ai_boundaries`
- `source_roots`
- `adr_links`
- `human_checkpoint`
- `review_cadence`

每个 module 至少包含：

- `name`
- `type`：domain、usecase、service、data、transport、frontend_feature、ai_workflow、shared、config、cmd。
- `path`
- `owns`
- `public_api`
- `may_depend_on`
- `must_not_depend_on`

### `architecture/module-maps/<target>.md`

给人恢复上下文，必须包含：

- `Context`
- `Containers`
- `Modules`
- `Dependency Direction`
- `Data Ownership`
- `API Contracts`
- `AI Boundaries`
- `Operational Boundaries`
- `Open Decisions`

默认不用画完整 UML。需要图时优先 context/container 级别，只有调试复杂边界时才写 component/code 级别。

### `architecture/dependency-rules/<target>.json`

用于检查依赖方向，必须包含：

- `target`
- `source_roots`
- `rules`
- `exceptions`
- `human_checkpoint`

每条 rule 至少包含：

- `name`
- `applies_to`
- `forbidden_imports`
- `reason`
- `severity`

示例：domain 不得 import data/transport；frontend feature 不得跨 feature 私有 import；AI workflow 不得直接 import production writer，而应通过授权 tool port。

## Go / Kratos / sqlc / gRPC 边界默认值

默认目录：

```text
api/<service>/v1/*.proto
cmd/<service>/main.go
configs/
internal/conf
internal/biz
internal/data
internal/service
internal/server
internal/ai
internal/pkg
```

默认依赖方向：

- `cmd` 只负责启动、配置、wire 和 shutdown。
- `api` 只放 Protobuf contract 和生成代码。
- `internal/service` 适配 gRPC/HTTP transport，调用 `biz/usecase`。
- `internal/biz` 持有领域规则、usecase、port interface，不 import `internal/data`、transport、SQL driver、model vendor SDK。
- `internal/data` 实现 repository port，持有 sqlc、transaction、external storage adapter。
- `internal/server` 组装 Kratos HTTP/gRPC server、middleware、health、observability。
- `internal/ai` 放 prompt builder、tool port、workflow orchestration 和 eval fixtures，但高风险副作用必须走 auth/cost/security 边界。
- `pkg` 默认不用。只有真正要跨 repo 复用且愿意承担公共 API 维护成本时才使用。

默认不把每个 feature 拆成单独微服务。一人公司优先 modular monolith 或少量服务，只有在数据所有权、发布节奏、可靠性隔离、供应商/安全边界明确时才拆服务。

## Vite 前端边界默认值

默认目录：

```text
web/
  index.html
  src/
    app/
    features/<feature>/
    shared/ui/
    shared/lib/
    routes/
    styles/
```

默认规则：

- feature 内部 co-locate component、hook、test、api adapter、types。
- `shared/ui` 只放跨 feature 真实复用且稳定的 UI 原语。
- `shared/lib` 只放无业务语义的纯函数。
- 禁止用 `shared`、`common`、`utils` 收纳未分类业务逻辑。
- feature 之间通过 route、API client、event 或显式 public index 交互，不互相 import 私有文件。
- Vercel/Geist token 和设计决策进入 design/system artifacts，不散落在各 feature 中。

## AI workflow 边界默认值

- prompt builder 靠近 feature，进入代码评审、测试和部署。
- workflow 优先 deterministic orchestration，只有开放式、多步、需工具选择和状态管理时才引入 agent。
- tool port 明确输入 schema、权限、tenant、成本限制、dry-run、审批要求和审计日志。
- AI model/vendor SDK 不进入 domain/biz 层，只在 adapter 或 workflow boundary 中使用。
- 输出进入 SQL、shell、文件、权限、支付、通知或生产写入前，必须经过 schema 校验和授权边界。

## 需要人判断的关键点

只把这些架构判断交给人：

- 是否新增 bounded context、服务、module 或 shared package。
- 是否改变数据所有权、API contract 或跨服务调用方向。
- 是否接受 dependency rule 例外。
- 是否引入新框架、供应商 SDK、agent runtime 或公共组件库。
- 是否拆服务、合并服务、或把实验代码转为生产代码。

其他文件结构、ADR 模板、boundary JSON 和 dependency rules 由 Codex 先按默认值创建，再由脚本检查。

## 默认取舍

- 默认单仓库、少服务、强边界，不默认微服务。
- 默认 Kratos layout，不发明新后端结构。
- 默认按 feature/route 组织 Vite 前端，不按技术类型过度分层。
- 默认 prompt builder 靠近 feature，不放进全局 prompt 仓库。
- 默认 architecture docs 只写能指导下一次改动的内容。
- 默认删除死代码，不保留长期关闭的 flag 或 commented code。

## Review 1：一人公司注意力审查

- 保留：只有四类工件，且只有架构显著决策才写 ADR。
- 保留：boundary JSON 和 dependency rules 可以脚本检查，不需要人逐个看 import。
- 调整：不要求完整 C4 图，只要求 context/container 级别文字 map。
- 调整：不默认拆微服务，避免把边界规范误用成服务拆分冲动。
- 风险：规则可能过严影响实验速度。缓解：允许过期实验代码和 dependency exceptions，但必须有 Review Date。

结论：可落地。一个人在 30 到 60 分钟内可以为服务建立边界基线，之后由脚本守住依赖方向。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：bounded context 依赖产品语言，避免工程文件夹反过来支配产品模型。
- 工程角度：Go/Kratos/sqlc/gRPC 和 Vite 都有默认结构，降低每次重想架构的负担。
- 运维角度：少服务、清晰 API、少跨服务同步调用，符合 SRE simplicity。
- 安全隐私角度：数据所有权、AI tool、tenant、auth boundary 在 architecture artifacts 中显式记录。
- 成本角度：新服务、新供应商 SDK、新 agent runtime 都触发人工 checkpoint，避免架构性成本漂移。

结论：可落地。第 13 阶段补上了“系统长期形状”的最小约束，并把架构例外交给人判断。


