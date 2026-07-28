## MODIFIED Requirements

### Requirement: 服务必须使用默认 Kratos 分层

新 Go 服务 MUST 默认采用 Kratos layout 风格的目录结构，并保持 transport、business、data 三层职责清晰。所有内部路径 MUST 相对该服务的应用根解释；含多个可部署应用的仓库 MUST 默认把 Go 服务应用根放在 `services/<service>/`，不得把聚合仓库根静默当成服务根。

#### Scenario: 多应用仓库创建用户服务

- **GIVEN** 仓库包含后端服务和一个或多个独立前端
- **WHEN** 创建名为 `user-center` 的 Go 服务
- **THEN** 先在项目地图声明 `services/user-center`
- **AND** 模板在该空目录生成
- **AND** `go.mod`、`api/`、`cmd/user-center/`、`configs/`、`internal/`、`migrations/`、`queries/` 与 `sqlc.yaml` 位于 `services/user-center/` 内
- **AND** 仓库根不存在归属于该服务的 `internal/`、`cmd/` 或 `api/`

#### Scenario: 单应用仓库创建服务

- **GIVEN** 仓库只包含一个可部署 Go 服务
- **AND** 项目地图声明 `repository_mode: single-application` 与 `path: .`
- **WHEN** 使用批准模板创建服务
- **THEN** 仓库根可以同时作为服务应用根
- **AND** 不要求增加无价值的 `services/<service>/` 包装层

#### Scenario: 小服务裁剪

- **GIVEN** 服务少于 3 个核心 usecase
- **WHEN** 建立应用根内部结构
- **THEN** 不继续拆分额外业务子包
- **AND** 不预建 message queue、cache、registry、多租户或插件系统
