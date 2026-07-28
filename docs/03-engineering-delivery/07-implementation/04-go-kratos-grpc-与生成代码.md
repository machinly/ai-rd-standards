# 实现：Go/Kratos、gRPC 与生成代码

## 规范要求

<!-- rule-id: IMPL-SERVICE-CHANGE-SOURCE -->
- Standard/High-risk 服务端需求须由链接权威产品输入的 OpenSpec change 承载。

<!-- rule-id: IMPL-SQLC-NOT-ORM-DEFAULT -->
- 数据访问缺省使用 sqlc，不默认引入 ORM。

<!-- rule-id: IMPL-NEW-SERVICE-TEMPLATE -->
- 新服务须在已由项目地图声明的空应用根目录使用当前批准的 Kratos CLI 模板生成。单应用仓库可以让仓库根同时作为应用根；多应用仓库不得把聚合仓库根当作某个服务的应用根。

<!-- rule-id: IMPL-SERVICE-DIRECTORY-LAYOUT -->
- 以下路径都相对所属 Go 服务的应用根解释，而不是无条件相对仓库根解释。单应用仓库可以使用仓库根；多应用仓库的 Go 服务缺省位于 `services/<service>/`，其 `go.mod`、`api/`、`cmd/<service>/`、`configs/`、`internal/server/`、`internal/service/`、`internal/biz/`、`internal/data/`、`internal/conf/`、`migrations/`、`queries/` 与 `sqlc.yaml` 必须留在该服务目录内。多应用仓库根不得出现归属于单个服务的 `internal/`、`cmd/`、`api/`、`configs/`、`migrations/`、`queries/` 或 `sqlc.yaml`；确属仓库级工具的例外必须在项目地图中以独立应用或工具入口登记，不得借例外承载业务服务代码。

<!-- rule-id: IMPL-COMMAND-REGISTRY-TRIGGER-PATH -->
- 当实际的 `cmd/<name>` 入口达到两个或更多时，须启用 command registry；其文件位于 `governance/architecture` 目录，名称为 `command-registry.json`。

<!-- rule-id: IMPL-COMMAND-REGISTRY-EXACT-REGISTRATION -->
- 每个实际 command 入口须在 registry 中恰好登记一次。

<!-- rule-id: IMPL-COMMAND-REGISTRY-SCHEMA -->
- 每个 command 入口须记录 `path`、`purpose`、`kind`、`environment`、`lifecycle`、`starter`、`dependencies`、`privileges`、`data_writes`、`failure_recovery` 与 `retirement`。

<!-- rule-id: IMPL-COMMAND-KIND-DISTINCTION -->
- production API、worker、管理 CLI 和开发工具须能从 command registry 明确区分。

<!-- rule-id: IMPL-SERVICE-PACKAGE-YAGNI -->
- 服务少于 3 个核心 usecase 时，不再拆更多包。

<!-- rule-id: IMPL-SERVICE-LAYER-SCOPE -->
- `internal/service` 禁止承载业务规则，只做请求校验、usecase 调用与响应映射。

<!-- rule-id: IMPL-BIZ-INDEPENDENCE -->
- `internal/biz` 禁止依赖 Kratos transport 或数据库实现。

<!-- rule-id: IMPL-DATA-RESULT-ENCAPSULATION -->
- `internal/data` 禁止把 SQL 结果结构泄漏到 API 层。

<!-- rule-id: IMPL-NO-SPECULATIVE-BACKEND-PLATFORM -->
- 只有现实需求能够证明必要性时，才可增加后端平台能力；在此之前，插件系统、多租户、registry、cache 与 message queue 均不得预建。

<!-- rule-id: IMPL-GRPC-CLIENT-DEADLINE -->
- gRPC 客户端调用须设置 deadline。

<!-- rule-id: IMPL-GRPC-SERVER-CANCELLATION -->
- gRPC 服务端须尊重 context cancellation。

<!-- rule-id: IMPL-QUERY-BEFORE-REPOSITORY -->
- 数据访问实现须先形成 query，再编写 Go repository。

<!-- rule-id: IMPL-NO-FK-APPLICATION-INTEGRITY -->
- 不使用 foreign key 时，应用层须实现引用存在性校验、事务或幂等控制、删除策略、唯一约束、非空约束和孤儿数据扫描。

<!-- rule-id: IMPL-CROSS-REPOSITORY-TRANSACTION-ENTRY -->
- 跨 repository 事务须由 `internal/data` 提供统一入口。

<!-- rule-id: IMPL-DYNAMIC-SQL-NONDEFAULT -->
- 动态 SQL 不得作为数据查询的缺省路径。

<!-- rule-id: IMPL-GENERATED-CODE-ONLY-FROM-SOURCES -->
- 禁止手工把生成代码改成业务代码；生成物只能通过 schema、query 或 config 的源变更重新产生。

<!-- rule-id: IMPL-GENERATED-CONTRACT-DIFF-SEPARATION -->
- 生成的契约代码 diff 须可 review，并与业务逻辑变更分离。

<!-- rule-id: IMPL-SERVICE-TASK-STATE -->
- 服务端 change 实现过程中须用 `tasks.md` 维护状态。

<!-- rule-id: IMPL-SERVICE-SEQUENCE-DATA-DEFINITION -->
- schema/migration 与 sqlc query 必须在 Proto 完成后才开始编写。

<!-- rule-id: IMPL-SERVICE-SEQUENCE-GENERATE -->
- Kratos、protoc 或 sqlc 代码生成必须等数据定义完成后再运行。

<!-- rule-id: IMPL-SERVICE-SEQUENCE-BIZ -->
- `internal/biz` usecase 与 repository 接口必须在代码生成完成后再实现。

<!-- rule-id: IMPL-SERVICE-SEQUENCE-DATA -->
- `internal/data` repository 与事务必须等 biz 接口确定后再实现。

<!-- rule-id: IMPL-SERVICE-SEQUENCE-TRANSPORT -->
- `internal/service` 协议适配必须在 data 实现完成后再编写。

<!-- rule-id: IMPL-SERVICE-MINIMUM-OBSERVABILITY -->
- 服务端实现须补齐适用的日志、metrics、tracing 与 health check 接口；证据与告警策略由验证和运行项目维护。

<!-- rule-id: IMPL-COMPLEX-CODE-COMMENT-CONTENTS -->
- 复杂状态、权限、事务、SQL、恢复或限制逻辑须在代码附近解释业务或安全意图、受保护不变量和失败风险。

<!-- rule-id: IMPL-NO-COMMENT-COVERAGE-GATE -->
- 禁止设置注释覆盖率门禁。

<!-- rule-id: IMPL-NO-SYNTAX-RESTATEMENT-COMMENT -->
- 注释不得复述代码语法。

<!-- rule-id: IMPL-SERVICE-STARTUP-IDENTITY -->
- 新服务启动日志须包含版本，以及 commit 或 build time 二者之一。

<!-- rule-id: IMPL-GRACEFUL-SERVICE-SHUTDOWN -->
- 服务收到 shutdown 后须停止接收新请求，并给正在执行的请求有限完成时间。

<!-- rule-id: IMPL-DATABASE-DEVIATION-HUMAN-GATE -->
- 采用非默认生产数据库或数据库专有能力须交由人工判断。

<!-- rule-id: IMPL-CLOUD-DATABASE-HUMAN-GATE -->
- 选择特定云厂商或托管数据库须交由人工判断。
