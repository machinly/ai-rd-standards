# API 契约、兼容性与版本演进规范
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/one-person-ai-rd-operating-model.md 的场景触发规范命中“API、Protobuf、错误语义、事件、webhook、AI tool schema 或兼容性变化”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/one-person-ai-rd-operating-model.md。
## 目标

一人公司的 API 风险不只在“接口能不能调通”，更在于未来是否能安全演进。gRPC/Protobuf 字段号、错误语义、前端客户端、AI tool schema、webhook、事件和数据库边界一旦被消费者依赖，破坏性变更会把一个人的注意力拖进迁移泥潭。本触发专项定义最小契约治理规范，让每个生产 target 知道有哪些契约、谁在用、什么变化安全、什么必须人审、怎么验证兼容性。

默认原则：契约先稳定，再扩展。优先 additive change；删除、改语义、重编号、改错误模型、改 AI 工具输入输出都视为高风险。

## 核心依据

- 《人月神话》：概念完整性需要稳定接口和共享语义；接口混乱会放大协调成本。
- 小型项目管理：小项目不能维护厚重 API 流程，但必须记录谁依赖了什么、下一步怎么验证。
- Hyrum's Law：只要有足够使用者，所有可观察行为都会被依赖；一人公司也要把公开、稳定、实验性 surface 分清楚。
- Google AIP-180 Backwards Compatibility：API 兼容性应考虑 source、wire 和 semantic compatibility。
- Protobuf proto3 guide / best practices：已使用字段号不能改；删除字段要 reserve number/name；不要复用 tag；字段类型和 `oneof` 变化可能破坏 wire compatibility。
- Buf breaking change detection：Protobuf 变更应有自动 breaking check，避免靠人工记忆。
- gRPC error handling / status codes：错误状态码和错误详情是 API 契约的一部分，客户端会据此重试、提示或降级。
- SemVer：使用版本号前必须声明 public API；破坏性变更应通过 major 或显式版本边界表达。
- OpenAI function calling / Structured Outputs：AI tool schema 和结构化输出 schema 是行为契约，`strict` schema 会影响模型输出与应用解析。
- Confluent schema evolution：schema 演进要明确 backward、forward、full compatibility 和消费者/生产者读取关系。
- Software Engineering at Google, Deprecation：弃用和移除需要有序迁移，不能靠“没人用了”的猜测。

## 范围

适用对象：

- Protobuf package、message、enum、service、RPC method。
- Go/Kratos/gRPC 服务端与 generated client。
- 浏览器使用的 HTTP/JSON endpoint、BFF、webhook、OpenAPI 或手写 client。
- event/topic payload、job payload、外部 provider callback。
- AI tool schema、structured output schema、prompt/model route 对外返回结构。
- 错误码、错误详情、retry semantics、pagination、idempotency、auth/tenant metadata。
- 数据库 schema 作为外部可依赖契约时的 query/result shape。

不适用对象：

- 未发布、无消费者、可随时删除的本地实验。
- 纯内部实现函数，且没有被 proto、HTTP、event、AI tool、配置、前端或外部系统依赖。
- 已被阶段 7 migration 或阶段 14 config change 覆盖的纯数据/配置变更，除非它改变外部契约。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
contracts/
  surface-map/<target>.json
  compatibility-policy/<target>.md
  protobuf-evolution/<target>.md
  error-model/<target>.md
  contract-tests/<target>.json
  ai-tool-schemas/<target>.json
```

`ai-tool-schemas` 仅在 target 包含 AI tool、structured output 或 agent tool contract 时必须创建。

### `contracts/surface-map/<target>.json`

契约地图必须包含：

- `target`
- `owner`
- `audiences`
- `surfaces`
- `consumers`
- `versioning`
- `protobuf_roots`
- `generated_clients`
- `ai_tool_schemas`
- `human_checkpoint`
- `review_cadence`

`surfaces` 每条至少包含：

- `name`
- `type`：`grpc_service`、`http_endpoint`、`webhook`、`event`、`db_contract`、`ai_tool_schema`、`frontend_route`、`config_contract`
- `path`
- `stability`：`experimental`、`internal`、`stable`、`deprecated`
- `version`
- `consumers`
- `owner`
- `compatibility`
- `deprecation`

默认：任何 `stable` 或外部消费者使用的 surface 都要有 contract tests 和兼容性策略。

### `contracts/compatibility-policy/<target>.md`

兼容性策略必须包含：

- `Scope`
- `Compatibility Definition`
- `Allowed Changes`
- `Breaking Changes`
- `Versioning`
- `Deprecation`
- `Consumer Communication`
- `Human Checkpoints`

默认兼容性定义：

- source compatibility：旧客户端代码能用新 client library 或 schema 编译。
- wire compatibility：旧/新客户端和服务端能在序列化层互通。
- semantic compatibility：同一输入的业务含义、错误语义、权限语义、重试语义不被悄悄改变。

### `contracts/protobuf-evolution/<target>.md`

Protobuf 演进计划必须包含：

- `Scope`
- `Proto Sources`
- `Safe Changes`
- `Reserved Fields`
- `Enum Rules`
- `Breaking Change Checks`
- `Generated Code`
- `Rollback`

默认安全变更：

- 新增 optional 字段或新 RPC 时不改变旧字段含义。
- 删除字段前先 deprecated，再 reserve number/name。
- enum 必须保留 unspecified/zero value；删除 enum value 要 reserve。
- 不改已发布字段号；不复用 tag；不把已有字段移入 `oneof`。
- 生成代码 diff 必须可 review，不和业务逻辑混在一起。

### `contracts/error-model/<target>.md`

错误模型必须包含：

- `Scope`
- `gRPC Status Codes`
- `Validation Errors`
- `Retry Semantics`
- `Auth / Permission Errors`
- `User-Facing Messages`
- `Observability`
- `Compatibility`

默认：客户端可观察的错误码、错误详情字段、retryable/non-retryable 语义、权限失败语义和用户提示都属于契约。

### `contracts/contract-tests/<target>.json`

契约测试计划必须包含：

- `target`
- `owner`
- `compatibility_baseline`
- `test_suites`
- `consumer_fixtures`
- `generated_clients`
- `ci_gates`
- `release_gates`
- `ai_eval_links`
- `human_checkpoint`

默认 gate：

- Protobuf 变更运行 `buf breaking` 或等价检查。
- gRPC handler 运行 contract tests，覆盖成功、验证错误、权限错误、not found、retryable dependency failure。
- 前端 client 或 BFF 运行 generated client / schema fixture tests。
- AI tool schema 变化运行 eval 和 tool-call fixture tests。

### `contracts/ai-tool-schemas/<target>.json`

AI tool / structured output 契约必须包含：

- `target`
- `owner`
- `schemas`
- `eval_links`
- `compatibility_policy`
- `rollback`
- `human_checkpoint`

`schemas` 每条至少包含：

- `name`
- `version`
- `schema_path`
- `strict`
- `consumers`
- `allowed_changes`
- `breaking_changes`
- `fallback`

默认：改 required 字段、删除字段、改字段含义、改 enum 值、改 tool side effect、改 structured output 根结构，都视为 AI 行为契约变更。

## Go / Kratos / gRPC / Protobuf 默认规则

- `.proto` 是服务契约 source of truth；Kratos/gRPC handler 不得定义与 proto 不一致的隐藏输入输出语义。
- proto package/version 命名保持稳定；需要破坏性版本时新增版本边界，而不是改旧包语义。
- 所有删除字段、删除 enum value、删除 RPC method 必须进入 deprecation plan，并 reserve 已删除字段号/名称。
- `buf lint` / `buf breaking` 或等价检查进入 CI/release gate。
- gRPC metadata 中的 auth、tenant、trace、idempotency key 也是契约，必须在 surface-map 或 error-model 中记录。
- 错误状态码用标准 gRPC status；业务错误详情字段必须稳定、低敏感、可观测。

## HTTP / Vite client 默认规则

- 浏览器调用的 HTTP/BFF endpoint 要么由 proto/gateway/OpenAPI 生成，要么在 surface-map 中记录手写契约。
- 前端不依赖未记录的错误 message 字符串、字段顺序、空值表现或偶然响应结构。
- Vite 前端升级 client schema 后至少运行 build、typecheck、Vitest 和关键 Playwright smoke。
- UI 文案变化不是 API 契约；但错误类别、权限类别、空状态类别会影响用户路径，应纳入 contract tests。

## AI workflow 默认规则

- tool schema、structured output schema、function name、required fields、side-effect flag、permission result 都是契约。
- prompt 可以内部演进，但如果改变 tool 调用分布、输出 schema、错误类别或 fallback 路径，必须跑 eval。
- schema 变化前保留旧 fixture；schema 变化后记录新旧 schema 的兼容性结论。
- structured output 默认使用严格 schema；不支持的 JSON Schema 特性不得默默进入生产。
- 高风险工具必须把 dry-run/commit、approval、tenant、actor、rollback 作为稳定契约字段或上下文。

## 需要人判断的关键点

只把这些契约判断交给人：

- 是否把 experimental/internal surface 升级为 stable/public。
- 是否接受 breaking API / protobuf / schema / AI tool contract change。
- 是否删除或重命名字段、RPC、event、tool、route、config。
- 是否改变错误码、retry、权限、idempotency 或用户可见失败语义。
- 是否支持多版本并行，还是强制迁移。
- 是否在有消费者未知时继续移除 deprecated surface。

其他字段完整性、路径存在性、章节、CI gate、AI schema 链接、敏感内容和 contract test 结构由 Codex 和 verifier 检查。

## Review 1：一人公司注意力审查

- 保留：五类核心工件分别回答“有哪些契约、什么变化安全、proto 怎么演进、错误如何稳定、怎么测”。
- 保留：AI tool schema 单独建文件，但仅 AI target 必须创建。
- 调整：不要求完整 API 平台或 schema registry；先用 JSON/Markdown 和 CI gate。
- 调整：stable/public 才强制 contract tests；experimental/internal 可以轻量记录。
- 风险：契约治理可能拖慢迭代。缓解：默认 additive change 可快速推进，只有破坏性或语义变化才人审。

结论：可落地。一个人可以在设计接口时写出 surface map 和兼容性策略，在改 proto/AI schema 时用 verifier 和 contract tests 护住未来演进。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：错误语义、权限失败、AI 输出结构和前端空状态会影响用户路径，必须稳定。
- 工程角度：Protobuf 字段号、reserved、buf breaking、generated client 和 schema fixture 形成可执行边界。
- 运维角度：错误模型、retry semantics、observability 和 release gate 能降低发布后排障成本。
- 安全隐私角度：auth/tenant metadata、permission errors、AI tool side effects 和敏感内容都进入契约边界。
- 成本角度：兼容性检查比事故后迁移便宜；只对 stable/public 和高风险变化加门禁，避免过度流程。

结论：可落地。第 18 阶段把“接口会被依赖”这件事前移到研发阶段，并与阶段 6 release、阶段 12 testing、阶段 17 deprecation 衔接。


