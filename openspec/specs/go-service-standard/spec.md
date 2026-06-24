# go-service-standard Specification

## Purpose

定义一人公司默认 Go 服务端研发规范，使新服务能以 Kratos、Protobuf/gRPC、sqlc、测试和最小运维信号稳定落地。

## Requirements

### Requirement: 服务必须使用默认 Kratos 分层

新 Go 服务 MUST 默认采用 Kratos layout 风格的目录结构，并保持 transport、business、data 三层职责清晰。

#### Scenario: 创建新服务

- GIVEN 需要创建新的后端服务
- WHEN 没有已有项目结构约束
- THEN 使用 `api/`、`cmd/`、`configs/`、`internal/server/`、`internal/service/`、`internal/biz/`、`internal/data/`、`third_party/`、`migrations/`、`queries/`、`sqlc.yaml`
- AND 删除无真实需求的示例代码和空包

#### Scenario: 小服务裁剪

- GIVEN 服务少于 3 个核心 usecase
- WHEN 建立目录结构
- THEN 不继续拆分额外业务子包
- AND 不预建 message queue、cache、registry、多租户或插件系统

### Requirement: API 契约必须 Protobuf-first

服务 API MUST 先由 OpenSpec scenario 和 `.proto` 表达，再生成 Go 代码。

#### Scenario: 新增 RPC

- GIVEN 一个新服务端能力需要对调用方暴露
- WHEN 开始实现
- THEN 先写或更新 OpenSpec scenario
- AND 更新 `.proto` 中的 request、response、service 和约束
- AND 生成 gRPC 服务端和客户端代码

#### Scenario: gRPC 调用

- GIVEN 客户端调用服务 RPC
- WHEN 发起请求
- THEN 设置 deadline
- AND 传递必要 metadata
- AND 服务端尊重 context cancellation

### Requirement: 数据访问必须 SQL-first 并通过 sqlc 生成

持久化数据访问 MUST 以 schema、migration 和 SQL query 为事实来源，并通过 sqlc 生成 Go 代码。

#### Scenario: 新增数据库读写

- GIVEN 一个 usecase 需要新的数据库读写
- WHEN 实现数据层
- THEN 先写 migration/schema
- AND 写 sqlc query
- AND 运行 `sqlc generate`
- AND repository 实现调用生成代码而不是手写扫描样板代码

#### Scenario: 需要动态 SQL

- GIVEN sqlc 静态查询不能满足需求
- WHEN 设计动态查询
- THEN 在 `design.md` 说明原因、边界和测试策略
- AND 限制动态 SQL 的输入来源和拼接方式

### Requirement: 服务必须有最小质量门禁

服务端变更交付前 MUST 运行可适用的生成、格式化、测试和查询检查命令。

#### Scenario: 标准 Go 服务交付

- GIVEN 服务端 change 准备交付
- WHEN 执行验证
- THEN 运行 `go mod tidy`
- AND 运行 `gofmt -w .`
- AND 运行 `go test ./...`
- AND 运行 `sqlc generate`
- AND 在配置存在时运行 `sqlc vet`

#### Scenario: 命令不能运行

- GIVEN 某个门禁命令在当前环境不能运行
- WHEN 交付总结
- THEN 记录未运行命令、原因和后续补救项

### Requirement: 服务必须具备最小运维信号

每个新服务 MUST 从第一天提供健康检查、结构化日志和四个黄金信号的落点。

#### Scenario: 服务启动

- GIVEN 服务启动
- WHEN 初始化完成
- THEN 输出 service、version、env、commit 或 build time
- AND 注册 health check 或等价 readiness endpoint

#### Scenario: 请求处理

- GIVEN 服务处理请求
- WHEN 记录日志或指标
- THEN 包含 request id 或 trace id
- AND 能统计 latency、traffic、errors、saturation 中至少可落地的信号
