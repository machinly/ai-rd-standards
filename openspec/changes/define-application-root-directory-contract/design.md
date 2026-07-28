## Context

旧条文把 Kratos layout 描述成 `api/`、`cmd/`、`internal/` 等相对路径，却没有定义这些路径相对于仓库根还是应用根。单服务仓库中两者相同，问题不明显；用户服务仓库同时包含后端、多个前端、E2E、部署和治理资产，两者必须分开。

## Goals / Non-Goals

**Goals**

- 让新会话在生成任何代码前知道每个应用的准确根目录。
- 保留单应用仓库的简洁性，同时为实际多应用仓库提供一致默认值。
- 让目录合同可由项目地图和静态工具验证。
- 阻止聚合根出现归属于某个服务或前端的私有源码目录。

**Non-Goals**

- 不建立通用 monorepo 平台、共享包发布系统或构建图。
- 不把目录检查描述为架构正确、产品可用或模板 provenance 已通过。
- 不自动迁移现有仓库。

## Decisions

### 1. 项目先声明仓库模式

含可部署应用的 Standard/High-risk 项目在 `governance/project-map.json` 记录：

- `repository_mode: single-application | multi-application`；
- `applications[]` 的 `id`、`kind`、`path` 与 `manifest`。

单应用仓库使用 `path: .`，仓库根就是应用根。多应用仓库的聚合根只承载仓库级导航、workspace 编排、部署、测试和治理资产。

### 2. 多应用仓库采用稳定的应用根

- Go 服务：`services/<service>/`；
- Vite 前端：`web/<app>/`。

这是默认约定，不为尚不存在的应用预建目录。其他技术栈或确有既有约定的仓库需在技术设计中明确偏离及其验证方式。

### 3. 内部 layout 只相对应用根解释

Go 服务的 `go.mod`、`api/`、`cmd/`、`configs/`、`internal/`、`migrations/`、`queries/` 与 `sqlc.yaml` 必须位于该服务应用根。前端的 `package.json`、`index.html`、`src/` 与 `public/` 必须位于该前端应用根。

多应用聚合根禁止出现属于单个应用的 `api/`、`cmd/`、`configs/`、`internal/`、`migrations/`、`queries/` 或 `src/`。仓库级 `go.work`、workspace manifest、脚本和部署配置仍可位于根目录；根级工具必须作为工具入口显式登记，不能暗中承载业务服务。

### 4. 模板命令必须指向已声明的空应用根

模板 provenance 除版本和来源外，还必须显示生成目标路径。模板只能写入已声明的空应用根，不能先在仓库根生成再人工搬运并声称模板 provenance 完整。

### 5. 验证器只证明静态目录合同

`--application-layout-only` 只验证项目地图中的应用根、manifest、默认路径和根级私有目录；`--require-application-layout` 则把同一检查加入完整项目证据验证。两者都不证明模板来源、代码分层、运行能力、浏览器旅程或独立审查。

## Risks / Trade-offs

- 固定 `services/` 与 `web/` 可能不适合所有既有仓库：规则是新多应用仓库默认值；已有明确约定可以通过技术设计记录偏离。
- 项目地图可能变成额外负担：只对实际含可部署应用的 Standard/High-risk 项目要求，单应用只需一条 `path: .`。
- 静态检查可能误把仓库级工具当应用代码：工具通过 command registry 或项目地图显式登记，避免依赖目录名猜测。

## Migration / Rollback

1. 先增加 OpenSpec delta 和回归测试。
2. 收紧正式实现与项目地图条文，并扩展静态验证器。
3. 在用户服务第五轮的空基线上验证多应用正例和根级 `internal/` 反例。
4. 独立终审接受后归档本 change；若默认路径不适合真实仓库，通过后续 Standard change 调整默认值，不删除仓库根/应用根的概念区分。
