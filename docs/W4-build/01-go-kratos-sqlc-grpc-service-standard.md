# W4 Build 触发专项：Go/Kratos/sqlc/gRPC 服务端研发规范 v0.1

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及 Go/Kratos 服务、Protobuf/gRPC、sqlc、repository、service 层、后端测试或最小运维要求时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/00-main.md`，由主入口判断是否触发本专项。

## 目标

给一人公司定义一条默认服务端落地路径：从 OpenSpec 需求出发，用 Go + Kratos v3 + Protobuf/gRPC + sqlc 交付一个可运行、可测试、可观测、可恢复的服务。它不是微服务崇拜，而是为了让后端工作有稳定模板，减少每次重新决策。

## 本专项只解决什么

- 新服务的目录结构与职责边界。
- Protobuf/gRPC API 设计和兼容规则。
- sqlc 数据访问规则。
- 一人可执行的实现顺序与质量门禁。
- 服务上线前最小可观测和健康检查要求。

不在本专项展开：前端 Vite、完整 SRE 告警、CI/CD 平台、云部署、认证/多租户、事件总线。这些后续单独开 OpenSpec change。

## 依据转译

- 规范要减少偶然复杂度，不能把简单 CRUD 做成分布式系统论文。
- 小型项目管理：只保留能减少返工的计划项。本专项的计划项就是 API、数据、实现、测试、观测五个切面。
- Kratos 官方：Kratos 是 Go 微服务工具箱，支持 Protobuf-first、HTTP/gRPC 生成、middleware、config、logging、metrics、tracing；官方 layout 可作为起点，但不是强制枷锁。
- gRPC/Protobuf 官方：服务接口应从 `.proto` 定义，生成客户端/服务端代码；服务必须考虑 deadline、取消、health checking 和兼容演进。
- sqlc 官方：SQL schema/query 是事实来源，`sqlc.yaml` 配置生成类型安全 Go 代码，并可用 `sqlc vet` 做查询检查。
- Go 官方：测试是 `go test` 驱动的包级实践，优先把测试放在代码旁边；工作区和模块不要被复杂 monorepo 设计绑架。
- Google SRE：可靠性来自简单、小 API、可重复发布、四个黄金信号，而不是一开始堆满平台能力。

## 默认决策

- 新服务默认 Go 1.25+、Kratos v3。
- 服务间通信默认 gRPC；HTTP 只作为浏览器、webhook、第三方或公开 API 的兼容层。
- API 默认 Protobuf-first，`.proto` 是接口契约源头。
- 数据库默认 PostgreSQL；除非项目明确是本地单机工具，否则 SQLite 只用于本地测试或演示。
- 数据访问默认 sqlc；不默认引入 ORM。
- 目录默认参考 `go-kratos/kratos-layout`，但删掉不需要的示例代码。
- 每个服务先做一个用户可见 SLO 草案，再补观测，不反过来先搭大监控。

## 服务目录规范

新服务默认目录：

```text
api/                 Protobuf API 与生成代码
cmd/<service>/        程序入口
configs/             本地配置样例
internal/server/      HTTP/gRPC server 装配
internal/service/     transport-facing 方法，只做协议适配
internal/biz/         usecase、实体、领域错误、repository 接口
internal/data/        repository 实现、事务、sqlc 调用
internal/conf/        配置结构
third_party/          proto 依赖
migrations/           数据库迁移
queries/              sqlc 查询
sqlc.yaml             sqlc 配置
```

一人公司裁剪规则：

- 一个服务少于 3 个核心 usecase 时，不再拆更多包。
- `internal/service` 不写业务规则，只做请求校验、调用 usecase、映射响应。
- `internal/biz` 不依赖 Kratos transport 和数据库实现。
- `internal/data` 不把 SQL 结果结构泄漏到 API 层。
- 没有真实需求时，不预建 message queue、cache、registry、多租户、插件系统。

## API 规范

- 每个 API 变更先写 OpenSpec scenario，再改 `.proto`。
- `.proto` 必须有 `package` 和 `go_package`。
- gRPC 方法默认一元 RPC；只有真实长任务、增量输出或双向协作时才用 streaming。
- 请求字段必须表达业务约束：必填、长度、范围、分页、排序、filter 的允许范围。
- 对外暴露 HTTP 时，用明确 annotation 或 gateway 设计，不让 HTTP 形态反向污染内部 gRPC 契约。
- 错误模型必须区分业务错误、参数错误、权限错误、依赖错误、内部错误。
- metadata 只传 trace、auth、request id、tenant 等横切信息，不传核心业务数据。
- 客户端调用必须设置 deadline；服务端必须尊重 context cancellation。gRPC 文档提醒：取消不会自动回滚已经完成的副作用，所以写操作要有幂等或事务策略。

## 数据访问规范

- schema 和 migration 先于 query。
- query 先于 Go repository 实现。
- `sqlc.yaml` 使用 version 2；明确 `engine`、`schema`、`queries`、`gen.go.package`、`gen.go.out`。
- 查询文件按聚合或 usecase 分组，命名必须表达意图，例如 `CreateWorkspace`、`ListInvoicesByAccount`。
- 写操作必须说明事务边界；跨多个 repository 的事务由 `internal/data` 提供统一入口。
- 动态 SQL 不是默认路径；确实需要时必须写在 `design.md`，说明为什么 sqlc 静态查询不够。
- 禁止把生成代码手改成业务代码。生成代码只通过 schema/query/config 改变。
- 若配置了 `sqlc vet`，变更必须通过；若暂时不能配置，要在 tasks 中留下原因和后续项。

## 实现顺序

每个服务端 change 默认按这个顺序推进：

1. 写 OpenSpec：proposal、delta spec、design、tasks。
2. 写 `.proto`：请求、响应、service、错误和校验约束。
3. 写 schema/migration 与 sqlc query。
4. 跑代码生成：Kratos/protoc/sqlc。
5. 写 `internal/biz` usecase 和 repository 接口。
6. 写 `internal/data` repository 实现与事务。
7. 写 `internal/service` 协议适配。
8. 补测试：usecase 单元测试、repository 集成测试或可替代验证、service 适配测试。
9. 补最小观测：日志字段、metrics、tracing、health check。
10. 跑质量门禁并更新 tasks。

## 质量门禁

合并或交付前至少运行：

```bash
go mod tidy
gofmt -w .
go test ./...
sqlc generate
sqlc vet
```

如果项目使用 Kratos layout 或 Makefile，再运行：

```bash
make all
make api
```

如果项目使用 Buf 或直接 protoc，再运行对应生成命令。不能运行的命令必须在 final summary 和 `tasks.md` 中记录原因。

## 最小运维要求

每个新服务至少要有：

- health check：gRPC health checking 或等价 endpoint。
- readiness：依赖数据库、外部 API 或关键配置时要能表达不可服务。
- 四个黄金信号的落点：latency、traffic、errors、saturation。
- 结构化日志：包含 service、version、env、request_id、trace_id、关键业务 id。
- 版本信息：启动日志能看到服务名、版本、commit 或 build time。
- 关闭流程：接收 shutdown 后停止接新请求，给正在执行的请求有限时间完成。

## 只问人的关键判断

默认不问：包名、目录、代码生成命令、普通 CRUD 分层、局部测试结构。

必须问：

- 生产数据库是否不是 PostgreSQL。
- 是否要公开 HTTP API，而不只是内部 gRPC。
- 是否引入认证、多租户、计费、第三方登录。
- 是否引入异步消息、事件溯源、分布式事务。
- 是否选择特定云厂商或托管数据库。
- 是否接受会破坏已有 API 或数据兼容的变更。

## 本专项 Review A：一人公司可落地性

结论：可落地，但要把它当“默认路径”，不是每次都完整照抄。

- 目录结构来自 Kratos layout，降低重新设计成本。
- 实现顺序让 AI 和人都能恢复上下文：先契约，再数据，再业务，再适配。
- 质量门禁少而硬，适合一个人每天重复执行。
- 最大负担是 `proto + sqlc + Kratos` 三套生成链；后续需要 skill 和验证脚本降低操作摩擦。
- 当前规范没有要求一次性部署平台，因此不会把一人公司拖进平台建设。

## 本专项 Review B：产品/工程/运维风险

结论：风险可控，主要风险是过早微服务化和 gRPC 对外集成成本。

- 已把“一个服务少于 3 个核心 usecase 不再拆包”和“HTTP 只做兼容层”写成约束，能抑制过度设计。
- gRPC deadline、health checking、context cancellation 和最小黄金信号覆盖了早期生产风险。
- PostgreSQL 作为默认值稳定，但仍是重要业务选择；如果你偏好 MySQL/SQLite，应在下一轮明确。
- sqlc 降低运行时查询错误，但会要求 SQL discipline；动态查询和复杂报表需要单独设计。
- 下一步应产出 `go-kratos-sqlc-service` skill，用来生成/检查服务结构和执行门禁。

## 当前只需要你判断的事项

我建议默认接受：新生产服务默认 PostgreSQL + sqlc，不引入 ORM。只有你明确说 MySQL/SQLite/其他数据库时才改变。
