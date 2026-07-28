# 技术设计：API、Protobuf 与错误契约

## 规范要求

<!-- rule-id: TECH-077-CHANGE-IMPACT-SURFACE -->
- 技术设计的影响面清单涵盖用户、系统、数据、权限、供应商、契约与承诺。

<!-- rule-id: TECH-088-DEVELOPER-SURFACE-SEPARATE-CHANGE -->
- 对外 API、SDK 或文档中的 public/stable 或客户依赖 surface 须由单独的 OpenSpec change 承载。

<!-- rule-id: TECH-089-PROTOBUF-FIRST-CONTRACT-SOURCE -->
- 服务 API 缺省采用 Protobuf-first，Proto 须作为接口契约源头。

<!-- rule-id: TECH-089-OPEN-SPEC-PROTO-LINKAGE -->
- 每个服务 API 变化须先由 OpenSpec scenario 固定行为，再修改对应 Proto。

<!-- rule-id: TECH-089-GRPC-METHOD-SHAPE -->
- gRPC 方法缺省使用一元 RPC；只有真实长任务、增量输出或双向协作才采用 streaming。

<!-- rule-id: TECH-089-HTTP-GATEWAY-BOUNDARY -->
- 对外 HTTP 须使用明确 annotation 或 gateway 设计，HTTP 形态禁止反向污染内部 gRPC 契约。

<!-- rule-id: TECH-089-GRPC-METADATA-SCOPE -->
- gRPC metadata 仅允许传横切信息，禁止承载核心业务数据。

<!-- rule-id: TECH-089-PUBLIC-HTTP-API-HUMAN-GATE -->
- 公开 HTTP API 须交由人工判断。

<!-- rule-id: TECH-073-DEPRECATED-SURFACE-UNKNOWN-CONSUMER-GATE -->
- deprecated surface 的消费者未知时，移除决定须交由人工判断。

<!-- rule-id: TECH-076-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：通过 gRPC 传播分析上下文时。gRPC metadata 禁止传播个人敏感值。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：发生所列边界变化时。本专项覆盖契约、数据、供应商、AI 工具或权限边界变化。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S03 -->
- 适用情形：小 bug fix 满足所列条件时。未新增跨模块 import 或公共 API 的小 bug fix 无需应用本专项。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S05 -->
- 适用情形：考虑创建 pkg 时。只在确需跨仓库复用且接受公共 API 成本时使用 pkg。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S06 -->
- 适用情形：考虑所列边界变化时。数据所有权、API contract 或跨服务调用方向变化须交由人工判断。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：技术设计总入口触发所列契约变化时。只在 API、Protobuf、错误、事件、webhook、AI schema 或兼容性变化时读取本专项。

<!-- rule-id: TECH-200-GOVERNANCE-API-CONTRACT-COMPATIBILITY-S01 -->
- 适用情形：当前仅需定义意图、行为、边界、风险与退出条件时。仅明确基础变更规格时回到 技术设计总入口。

<!-- rule-id: TECH-082-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：演进生产契约时。契约先稳定再扩展。

<!-- rule-id: TECH-082-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：演进生产契约时。优先考虑 additive change。

<!-- rule-id: TECH-083-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：契约发生所列变化时。删除、语义、编号、错误模型或 AI 工具输入输出变化视为高风险。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：变更所列 Protobuf surface 时。本专项覆盖 Protobuf package、message、enum、service 与 RPC。

<!-- rule-id: TECH-200-GOVERNANCE-API-CONTRACT-COMPATIBILITY-S02 -->
- 适用情形：变更服务端或生成客户端时。本专项覆盖服务端和生成客户端。

<!-- rule-id: TECH-071-API-CONTRACT-API-CONTRACT-COMPATIBILITY-S01 -->
- 适用情形：变更所列 HTTP surface 时。本专项覆盖浏览器 HTTP、BFF、webhook、OpenAPI 与手写客户端。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S03 -->
- 适用情形：变更所列异步契约时。本专项覆盖事件、作业载荷和 provider callback。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S04 -->
- 适用情形：变更所列 AI 契约时。本专项覆盖 AI 工具、结构化输出与外部返回结构。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S05 -->
- 适用情形：变更所列协议语义时。本专项覆盖错误、重试、分页、幂等和 auth/tenant metadata。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S06 -->
- 适用情形：数据库 schema 形成外部契约时。数据库 query/result 被外部依赖时纳入本专项。

<!-- rule-id: TECH-200-GOVERNANCE-API-CONTRACT-COMPATIBILITY-S03 -->
- 适用情形：本地实验满足全部条件时。未发布、无消费者且可删除的本地实验无需应用本专项。

<!-- rule-id: TECH-071-API-CONTRACT-API-CONTRACT-COMPATIBILITY-S02 -->
- 适用情形：函数未被任何所列 surface 依赖时。无外部依赖的纯内部函数无需应用本专项。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S07 -->
- 适用情形：数据或配置变更不改变外部契约时。实现项目已覆盖且不改变外部契约的纯数据或配置变更无需应用本专项。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S08 -->
- 适用情形：扩展 Protobuf 时。新增 optional 字段或 RPC 禁止改变旧字段含义。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S09 -->
- 适用情形：删除 Protobuf 字段时。删除字段前先 deprecated 再 reserve number 和 name。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S10 -->
- 适用情形：定义 Protobuf enum 时。enum 须保留 unspecified 或 zero value。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S11 -->
- 适用情形：删除 Protobuf enum value 时。删除 enum value 须 reserve。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S12 -->
- 适用情形：演进 Protobuf 时。禁止更改已发布字段号；禁止复用 tag；禁止把已有字段移入 oneof。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S13 -->
- 适用情形：定义或变更客户端可观察错误时。客户端可观察的错误、重试、权限和用户提示均属于契约。

<!-- rule-id: TECH-083-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：AI schema 发生所列变化时。所列 schema、side effect 或根结构变化均视为 AI 行为契约变更。

<!-- rule-id: TECH-082-API-CONTRACT-ERROR-MODEL-S03 -->
- 适用情形：实现 gRPC 服务时。proto 是服务契约 source of truth。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S14 -->
- 适用情形：实现 gRPC 服务时。handler 禁止定义与 proto 不一致的隐藏语义。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S15 -->
- 适用情形：演进 proto 时。proto package 和版本命名维持稳定。

<!-- rule-id: TECH-200-GOVERNANCE-API-CONTRACT-COMPATIBILITY-S05 -->
- 适用情形：需要破坏性版本时。breaking 版本新增版本边界而不修改旧包语义。

<!-- rule-id: TECH-083-API-CONTRACT-ERROR-MODEL-S03 -->
- 适用情形：删除所列 Protobuf surface 时。删除字段、enum 或 RPC 须进入 deprecation plan。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S16 -->
- 适用情形：删除 Protobuf 字段时。删除字段须 reserve 字段号和名称。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S17 -->
- 适用情形：实现 gRPC 错误时。业务错误详情须稳定、低敏感且可观测。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S18 -->
- 适用情形：实现前端 client 时。前端禁止依赖未记录的偶然响应行为。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S19 -->
- 适用情形：评估 UI 变化时。UI 文案变化不属于 API 契约。

<!-- rule-id: TECH-081-API-CONTRACT-ERROR-MODEL-S20 -->
- 适用情形：定义 AI workflow 时。AI tool schema、函数名、必填字段、副作用和权限结果均属于契约。

<!-- rule-id: TECH-247-SCHEMA-DATA-API-CONTRACT-COMPATIBILITY-S03 -->
- 适用情形：使用 structured output 时。不支持的 JSON Schema 特性禁止静默进入生产。

<!-- rule-id: TECH-083-API-CONTRACT-ERROR-MODEL-S04 -->
- 适用情形：定义高风险 AI tool 时。高风险工具须把 dry-run/commit 作为稳定契约字段或上下文；高风险工具须把 approval 作为稳定契约字段或上下文；高风险工具须把 tenant 作为稳定契约字段或上下文；高风险工具须把 actor 作为稳定契约字段或上下文；高风险工具须把 rollback 作为稳定契约字段或上下文。

<!-- rule-id: TECH-075-API-CONTRACT-API-CONTRACT-COMPATIBILITY-S01 -->
- 适用情形：考虑提升 surface 稳定级别时。surface 升级为 stable/public 须交由人工判断。

<!-- rule-id: TECH-083-API-CONTRACT-ERROR-MODEL-S05 -->
- 适用情形：出现 breaking 契约变化时。接受 breaking 契约变化须交由人工判断。

<!-- rule-id: TECH-083-API-CONTRACT-ERROR-MODEL-S06 -->
- 适用情形：考虑删除或重命名时。删除或重命名契约 surface 须交由人工判断。

<!-- rule-id: TECH-084-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：传播 gRPC metadata 时。gRPC metadata 禁止传 secret 或完整敏感内容。

<!-- rule-id: TECH-083-API-CONTRACT-ERROR-MODEL-S07 -->
- 适用情形：API contract 专项与本规范的正式分类及项目原则冲突时。冲突时以正式规范为准。

<!-- rule-id: TECH-090-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：实现前端 API 通信时。浏览器禁止直接使用内部 gRPC。

<!-- rule-id: TECH-090-API-CONTRACT-ERROR-MODEL-S03 -->
- 适用情形：改变前端 contract 时。前端 contract 须先写 OpenSpec scenario 再写 API adapter。

<!-- rule-id: TECH-090-API-CONTRACT-ERROR-MODEL-S04 -->
- 适用情形：实现前端 API 时。浏览器仅允许调用公开 HTTP/BFF endpoint；浏览器禁止直接依赖内部 gRPC 服务。

<!-- rule-id: TECH-090-API-CONTRACT-ERROR-MODEL-S05 -->
- 适用情形：实现前端请求时。前端请求必须集中在 src/lib/api 或 feature-local adapter，禁止把 fetch 散落在视图组件。

<!-- rule-id: TECH-091-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：实施高风险数据变更时。高风险数据变更默认走 expand/migrate/contract，禁止默认一次性 rename、drop 或 alter。

<!-- rule-id: TECH-091-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：执行生产迁移时。仅有确认旧代码不再使用后才 contract 删除旧结构。

<!-- rule-id: TECH-095-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：实现异步 API 时。HTTP/BFF 仅允许包装 job usecase。

<!-- rule-id: TECH-096-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：实现异步 API 时。服务端须重新计算权限和租户。

<!-- rule-id: TECH-096-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：使用 Batch API 时。Batch API 仅允许用于不要求即时响应的离线任务。

<!-- rule-id: TECH-098-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：维护 tenant_id_ref 时。tenant_id_ref 禁止写入真实 API key。

<!-- rule-id: TECH-098-API-CONTRACT-ERROR-MODEL-S03 -->
- 适用情形：实现客户上线 error model 时。gRPC error model须区分：tenant not ready、identity not configured、entitlement missing、integration unverified、data dry-run failed、ai eval gate failed、billing live mode missing、support path missing。

<!-- rule-id: TECH-099-API-CONTRACT-ERROR-MODEL-S03 -->
- 适用情形：校验 gRPC 请求携带的 approval metadata 时。不接受浏览器传入的“已批准”声明。


## 执行细则

<!-- rule-id: TECH-079-STABLE-SURFACE-COMPATIBILITY-POLICY -->
- stable 或已有外部消费者的 surface 须具有兼容性策略。

<!-- rule-id: TECH-079-GRPC-METADATA-CONTRACT -->
- gRPC metadata 中的 auth、tenant、trace 和幂等 key 属于契约内容并须登记。

<!-- rule-id: TECH-079-BROWSER-ENDPOINT-SURFACE-MAP -->
- 浏览器 HTTP/BFF 契约须由 schema 生成，或明确登记在 surface map 中。

<!-- rule-id: TECH-079-SURFACE-MAP-MINIMUM-ARTIFACT -->
- 契约专项的最小工件须包含 surface map。

<!-- rule-id: TECH-079-SURFACE-MAP-PROTOBUF-ROOTS -->
- surface map 须登记 Protobuf roots。

<!-- rule-id: TECH-079-PROTO-EVOLUTION-MINIMUM-ARTIFACT -->
- 契约专项的最小工件须包含 Protobuf evolution 计划。

<!-- rule-id: TECH-079-ERROR-MODEL-MINIMUM-ARTIFACT -->
- 契约专项的最小工件须包含 error model。

<!-- rule-id: TECH-079-PROTO-EVOLUTION-PLAN-SCHEMA -->
- Protobuf evolution plan 须记录 `Scope`、`Proto Sources`、`Safe Changes`、`Reserved Fields`、`Enum Rules`、`Breaking Change Checks`、`Generated Code` 和 `Rollback`。

<!-- rule-id: TECH-079-ERROR-MODEL-SCHEMA -->
- error model 须登记 `Scope`、`gRPC Status Codes`、`Validation Errors`、`Retry Semantics`、`Auth / Permission Errors`、`User-Facing Messages` 和 `Compatibility`。

<!-- rule-id: TECH-089-SERVICE-COMMUNICATION-PROTOCOL -->
- 服务间通信缺省采用 gRPC；HTTP 仅承担浏览器、Webhook、第三方或公开 API 的兼容层。

<!-- rule-id: TECH-089-PROTO-IDENTITY-FIELDS -->
- Proto 须声明 `package` 与 `go_package`。

<!-- rule-id: TECH-073-SURFACE-MAP-SCHEMA -->
- surface map 须登记 `target`、`audiences`、`surfaces`、`consumers`、`versioning`、`generated clients` 和 `review cadence`。

<!-- rule-id: TECH-073-SURFACE-ITEM-SCHEMA -->
- surface map 中每条 surface 须登记 `name`、`path`、`version`、`consumers` 和 `compatibility`。

<!-- rule-id: TECH-094-ASYNC-GRPC-API -->
- 异步 gRPC API 缺省提供 `SubmitJob`、`GetJob`、`CancelJob`、`ListJobs`、`RetryDeadLetterJob` 或各自的等价方法。

<!-- rule-id: TECH-076-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：通过 gRPC 传播分析上下文时。gRPC metadata 仅传播 request_id、traceparent、tenant/workspace context、feature flag variant 和实验 assignment；个人敏感值不得随 metadata 传播。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：架构决定影响所列边界时。影响依赖、数据、API、AI 工具或供应商锁定的决定须写入架构工件。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S04 -->
- 适用情形：组织 Go/Kratos 服务时。api 仅存放 Protobuf contract 和生成代码。

<!-- rule-id: TECH-247-SCHEMA-DATA-API-CONTRACT-COMPATIBILITY-S01 -->
- 适用情形：评估 source compatibility 时。source compatibility 要求旧客户端代码可用新 client 或 schema 编译。

<!-- rule-id: TECH-200-GOVERNANCE-API-CONTRACT-COMPATIBILITY-S04 -->
- 适用情形：评估 wire compatibility 时。wire compatibility 要求新旧客户端与服务端序列化互通。

<!-- rule-id: TECH-080-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：实现 gRPC 错误时。错误状态码采用标准 gRPC status。

<!-- rule-id: TECH-247-SCHEMA-DATA-API-CONTRACT-COMPATIBILITY-S02 -->
- 适用情形：定义 structured output 时。structured output 缺省使用严格 schema。

<!-- rule-id: TECH-084-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：传播 gRPC metadata 时。gRPC metadata 仅传认证、request id、trace 和必要横切信息。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S07 -->
- 适用情形：组织 Go/Kratos 服务时。Go/Kratos 缺省目录包含版本化 proto contract。

<!-- rule-id: TECH-085-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：change 导入导出或同步客户数据时。客户数据专项最小工件纳入 transfer contract。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S08 -->
- 适用情形：创建 architecture boundary 时。boundary JSON 须记录 API contracts。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S09 -->
- 适用情形：定义 boundary module 时。每个 module 须记录 public API。

<!-- rule-id: TECH-078-API-CONTRACT-ERROR-MODEL-S10 -->
- 适用情形：创建 module map 时。module map 须记录 API Contracts。

<!-- rule-id: TECH-074-API-CONTRACT-API-CONTRACT-COMPATIBILITY-S01 -->
- 适用情形：创建 surface map 时。surface map 须记录 owner。

<!-- rule-id: TECH-072-API-CONTRACT-API-CONTRACT-COMPATIBILITY-S01 -->
- 适用情形：创建 surface map 时。surface map 须记录 human checkpoint。

<!-- rule-id: TECH-075-API-CONTRACT-API-CONTRACT-COMPATIBILITY-S02 -->
- 适用情形：定义 surface 时。每条 surface 须登记 type 和 stability；type 只能取 `grpc_service`、`http_endpoint`、`webhook`、`event`、`db_contract`、`ai_tool_schema`、`frontend_route`、`config_contract`，stability 只能取 `experimental`、`internal`、`stable`、`deprecated`。

<!-- rule-id: TECH-074-API-CONTRACT-API-CONTRACT-COMPATIBILITY-S02 -->
- 适用情形：定义 surface 时。每条 surface 须记录 owner。

<!-- rule-id: TECH-200-GOVERNANCE-API-CONTRACT-COMPATIBILITY-S06 -->
- 适用情形：创建 compatibility policy 时。compatibility policy须登记：Scope、Compatibility Definition、Allowed Changes、Breaking Changes、Versioning、Consumer Communication、Human Checkpoints。

<!-- rule-id: TECH-247-SCHEMA-DATA-API-CONTRACT-COMPATIBILITY-S04 -->
- 适用情形：定义 AI schema 时。每条 AI schema须登记：name、version、schema path、strict、consumers、allowed changes、breaking changes。

<!-- rule-id: TECH-087-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：设计 AI runtime 错误模型时。gRPC error model须区分：用户输入错误、权限错误、budget/capacity 限制、供应商暂时不可用、schema/parse 失败、安全拒绝、approval required、tool denied、内部错误。

<!-- rule-id: TECH-090-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：组织前端代码时。业务页面、局部组件和 API adapter 须放在 feature 目录。

<!-- rule-id: TECH-092-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：触发 integration 工件时。webhook contract 缺省位于 integrations/webhook-contract/<target>.json。

<!-- rule-id: TECH-093-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：建立异步工件时。job contract 缺省位于 async-jobs/job-contract/<target>.json。

<!-- rule-id: TECH-093-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：编写 job contract 时。job contract须包含：target、owner、state_machine、payload_policy、result_policy、idempotency、lease_policy、retry_policy、cancellation_policy、progress_policy、user_visibility、data_retention、human_checkpoint、status。

<!-- rule-id: TECH-093-API-CONTRACT-ERROR-MODEL-S03 -->
- 适用情形：实现异步 API 时。gRPC metadata须传播：actor_id、tenant_id、request_id、idempotency_key、job_id、traceparent。

<!-- rule-id: TECH-093-API-CONTRACT-ERROR-MODEL-S04 -->
- 适用情形：使用 Batch API 时。Batch API须登记：input file id、custom id、status、输出引用、24h 期望、回滚或重跑策略。

<!-- rule-id: TECH-070-API-CONTRACT-ACCESSIBILITY-AI-UX-S01 -->
- 适用情形：适用本专项时。每个关键 surface 须维护 surface map。

<!-- rule-id: TECH-070-API-CONTRACT-ACCESSIBILITY-AI-UX-S02 -->
- 适用情形：维护 surface map 时。surface map须包含：Scope、Users / Context、Views / States、Input Modes、AI Touchpoints、Responsive / Theme、Risks、Linked Artifacts。

<!-- rule-id: TECH-097-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：设计 backend smoke 时。health endpoint 或 gRPC health 可以用于 smoke。

<!-- rule-id: TECH-098-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：实现客户上线 API 时。gRPC API 优先考虑暴露 创建/读取 launch plan；gRPC API 优先考虑暴露 验证 readiness；gRPC API 优先考虑暴露 预检 tenant config；gRPC API 优先考虑暴露 dry-run data import；gRPC API 优先考虑暴露 启停 integration；gRPC API 优先考虑暴露 查询 customer success state。

<!-- rule-id: TECH-099-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：实现 Admin API 时。Admin API 须是显式服务面；Admin API 禁止依靠隐藏 HTTP route 或 Vite 前端按钮保护。

<!-- rule-id: TECH-099-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：实现 Admin API 的 gRPC metadata 传播时。gRPC metadata须传播：actor、tenant、request id、approval id。

<!-- rule-id: TECH-099-API-CONTRACT-ERROR-MODEL-S04 -->
- 适用情形：涉及Go / Kratos / sqlc / gRPC 默认规则时。高风险写操作缺省通过业务 usecase 执行，不直接手写生产 SQL。

<!-- rule-id: TECH-101-API-CONTRACT-ERROR-MODEL-S01 -->
- 适用情形：实现支持相关后台时。支持相关后台缺省在 Go 或 Kratos 服务端执行权限检查。

<!-- rule-id: TECH-101-API-CONTRACT-ERROR-MODEL-S02 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。支持 case 关联 tenant_id 时仅使用最小必要字段。

<!-- rule-id: TECH-101-API-CONTRACT-ERROR-MODEL-S03 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。支持 case 关联 actor_id 时仅使用最小必要字段。

<!-- rule-id: TECH-101-API-CONTRACT-ERROR-MODEL-S04 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。支持 case 关联 request_id 时仅使用最小必要字段。

<!-- rule-id: TECH-101-API-CONTRACT-ERROR-MODEL-S05 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。支持 case 关联 trace_id 时仅使用最小必要字段。

<!-- rule-id: TECH-101-API-CONTRACT-ERROR-MODEL-S06 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。支持 case 关联 release_id 时仅使用最小必要字段。

<!-- rule-id: TECH-101-API-CONTRACT-ERROR-MODEL-S07 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。支持 case 关联 prompt_version 时仅使用最小必要字段。

<!-- rule-id: TECH-101-API-CONTRACT-ERROR-MODEL-S08 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。支持 case 关联 model 时仅使用最小必要字段。
