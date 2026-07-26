# 技术设计

## 项目目的与边界

技术设计把已批准的产品行为、体验契约和风险边界转化为系统结构与可交付接口。它负责架构和依赖方向、API 与数据契约、认证授权、配置和运行时控制、AI runtime、异步与外部集成、观测字段及实际落入本批来源的恢复设计；它不维护工程排期、测试证据、发布动作、生产处置、IaC 环境资源、RPO/RTO 或 restore 演练权威。

## 根本原则

- **ITEM-TECH-DESIGN-001**：技术设计不应为未来假想规模引入复杂架构；影响依赖方向、数据所有权、接口契约、AI 工具边界或供应商锁定的决定必须记录。

## 核心判断

以下内容是阅读技术规则时的非规范性问题清单，不替代带 rule-id 的规范：

- 模块职责、数据所有权、依赖方向与外部边界是否清楚？
- 消费者、版本、兼容窗口、错误和重试语义是否已经辨明？
- 数据权威来源、tenant/owner、事务、幂等、索引与迁移关系是否完整？
- 身份事实、授权裁决点、租户隔离、secret 和副作用边界分别在哪里？
- 配置、flag、kill switch、模型 route、队列与供应商调用由谁拥有和约束？
- AI 方案选择的层级、上下文来源、工具权限、成本和失败路径是什么？
- 异步任务、Webhook 与外部副作用的状态、去重、取消和补偿如何表达？
- 观测与审计结构包含哪些字段，哪些内容属于敏感信息？
- 哪些取舍来自来源中的人工判断点，尚待谁裁决？

## 重新组织后的规范要求

### 架构、模块与依赖边界

<!-- rule-id: TECH-191-FRONTEND-EVENT-SCOPE -->
- 前端事件仅记录 UI 交互与体验路径。

<!-- rule-id: TECH-201-ARCHITECTURE-SPECIALTY-ROUTING -->
- 仅需定义意图、行为、边界、风险和退出条件时，由技术设计总入口继续分流。

<!-- rule-id: TECH-201-ARCHITECTURE-CODE-DATA-BOUNDARY-APPLICABILITY -->
- 架构专项的适用边界限定为所有权发生变化的下列表面：`api/`、`internal/`、`pkg/`、`web/src/features`、AI workflow 与数据库 schema。

<!-- rule-id: TECH-201-ARCHITECTURE-SHARED-COUPLING-APPLICABILITY -->
- 引入框架、跨服务调用或共享公共组件时纳入架构专项。跨服务、数据所有权、权限模型、稳定 API、重大选型或难回退设计存在多个合理方案时，可以按复杂度门只使用 `brainstorming` 比较方案，并把结论写回技术设计或 OpenSpec design；沿用已批准模式的单组件变更默认跳过该 skill。

<!-- rule-id: TECH-201-ARCHITECTURE-EXPERIMENT-EXCLUSION -->
- 一次性 Technical Spike 只有在轻量 Explore sandbox boundary 成立、标有删除或过期边界且不进入生产时，才无需展开完整架构专项；一旦声明稳定接口、跨越真实数据/凭据/外部系统或准备 promote，须重新判断并应用实际命中的架构与风险控制。

<!-- rule-id: TECH-EXPLORE-WALKING-SKELETON -->
- Technical Spike 的第一轮优先形成一条 Walking Skeleton：从一个真实产品入口经过实际所需组件到达一个可见业务结果。多服务 Explore 仍提供一个用户入口，不以分别证明 API、数据库或服务启动代替端到端产品事实；横向加固、平台化和所有异常覆盖延后到该事实出现之后。

<!-- rule-id: TECH-109-ARCHITECTURE-BOUNDARY-S01 -->
- 适用情形：技术设计总入口触发所列架构变化时。只在架构边界、模块职责、数据所有权或依赖方向变化时读取本专项。

<!-- rule-id: TECH-107-ARCHITECTURE-BOUNDARY-S01 -->
- 适用情形：进行架构设计时。不会针对未来假想规模设计复杂架构。

<!-- rule-id: TECH-103-ARCHITECTURE-BOUNDARY-PRINCIPLES-S01 -->
- 适用情形：发生所列结构变化时。本专项覆盖新服务、bounded context、Go module 或服务拆合。

<!-- rule-id: TECH-110-ARCHITECTURE-BOUNDARY-S01 -->
- 适用情形：考虑是否创建 ADR 时。缺省只为架构显著决策写 ADR。

<!-- rule-id: TECH-113-ARCHITECTURE-DIAGRAM-DEPTH-S01 -->
- 适用情形：记录架构图时。缺省不画完整 UML。

<!-- rule-id: TECH-195-FRONTEND-BOUNDARY-S03 -->
- 适用情形：组织 Vite 前端时。禁止用 shared、common 或 utils 收纳未分类业务逻辑。

<!-- rule-id: TECH-195-FRONTEND-BOUNDARY-S04 -->
- 适用情形：组织 Vite 前端时。feature 之间禁止 import 私有文件。

<!-- rule-id: TECH-114-ARCHITECTURE-HUMAN-CHECKPOINTS-S01 -->
- 适用情形：考虑所列架构新增时。新增 bounded context、服务、module 或 shared package 须交由人工判断。

<!-- rule-id: TECH-114-ARCHITECTURE-HUMAN-CHECKPOINTS-S02 -->
- 适用情形：依赖规则需要例外时。接受 dependency rule 例外须交由人工判断。

<!-- rule-id: TECH-114-ARCHITECTURE-HUMAN-CHECKPOINTS-S03 -->
- 适用情形：考虑所列架构动作时。拆合服务或将实验代码转生产须交由人工判断。

<!-- rule-id: TECH-103-ARCHITECTURE-BOUNDARY-PRINCIPLES-S02 -->
- 适用情形：选择总体架构时。缺省单仓库、少服务、强边界且不默认微服务。

<!-- rule-id: TECH-103-ARCHITECTURE-BOUNDARY-PRINCIPLES-S03 -->
- 适用情形：维护架构文档时。架构文档缺省只写能指导下一次改动的内容。

<!-- rule-id: TECH-109-ARCHITECTURE-BOUNDARY-S02 -->
- 适用情形：architecture 专项与本规范的正式分类及项目原则冲突时。冲突时以正式规范为准。

<!-- rule-id: TECH-190-DEPENDENCY-UPDATE-S01 -->
- 适用情形：引入实现依赖时。新增长期依赖须由人工判断。

<!-- rule-id: TECH-208-GOVERNANCE-GO-KRATOS-SQLC-GRPC-SERVICE-S01 -->
- 适用情形：创建新服务时。新服务缺省使用 Go 1.25+；新服务缺省使用 Kratos v3；新服务须保留模板 provenance；新服务禁止手工拼装目录。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S05 -->
- 适用情形：使用数据库专有能力时。数据库专有能力须隔离；数据库专有能力须说明不可移植边界；数据库专有能力须说明替代路径。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S09 -->
- 适用情形：组织 sqlc query 时。query 命名须表达业务意图。

<!-- rule-id: TECH-196-FRONTEND-BOUNDARY-S03 -->
- 适用情形：组织前端代码时。src/lib 禁止放业务流程。

<!-- rule-id: TECH-254-SCHEMA-DATA-VITE-VERCEL-FRONTEND-S01 -->
- 适用情形：配置前端环境时。VITE 变量禁止存 secret、private key、数据库连接或服务端 token。

<!-- rule-id: TECH-216-GOVERNANCE-VITE-VERCEL-FRONTEND-S01 -->
- 适用情形：设计按钮时。文本按钮仅允许用于明确命令。

### API、Protobuf 与错误契约

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

### 数据模型、sqlc 与迁移

<!-- rule-id: TECH-134-SQLC-TENANT-OWNER-CONSTRAINT -->
- 访问租户数据的 sqlc query 须显式约束 tenant 或 owner。

<!-- rule-id: TECH-252-SCHEMA-DATA-PRODUCT-ANALYTICS-EXPERIMENT-S01 -->
- 适用情形：定义事件属性时。事件属性缺省只允许 plan、role、source、status、error_class、latency_bucket、cost_bucket、variant、surface、template_id 这些低基数字段。

<!-- rule-id: TECH-223-MIGRATION-DESIGN-S01 -->
- 适用情形：选择版本迁移策略时。多版本并行或强制迁移须交由人工判断。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S01 -->
- 适用情形：AI 输出供程序消费时。程序消费 AI 输出时缺省使用 Structured Outputs 或 JSON schema，不默认让下游解析自由文本。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S03 -->
- 适用情形：决定是否创建 schema.json 时。仅程序消费结构化输出时 schema.json 必需。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S01 -->
- 适用情形：选择数据存储时。没有明确理由禁止引入多个数据存储。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S02 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时应用逻辑须承担引用完整性。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S05 -->
- 适用情形：实施数据库变更时。所有数据库变更须进入版本控制。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S02 -->
- 适用情形：编写 migration 时。一次 migration 仅允许做一个目的清楚的变更。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S03 -->
- 适用情形：实施高风险生产数据变更时。生产删除、批量更新、破坏性 SQL、不可逆 migration 或隐私导出须设置人工 checkpoint。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S04 -->
- 适用情形：实施数据修复或 backfill 时。数据修复和 backfill 禁止混入普通 schema migration。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S06 -->
- 适用情形：编写 SQL 文件时。SQL 文件禁止存真实生产数据、secret、token、完整导出或隐私样本。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S03 -->
- 适用情形：编写 query 时。query 名称须表达业务意图。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S08 -->
- 适用情形：编写 schema/query 时。schema 和 query 禁止默认使用数据库专有能力或隐式转换。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S05 -->
- 适用情形：设计跨表关系时。无 foreign key 的跨表关系须具备：并发策略、孤儿检测、修复方式。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S11 -->
- 适用情形：执行生产迁移时。生产迁移 code 阶段须兼容新旧 schema。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S07 -->
- 适用情形：设计 backfill 时。backfill 须幂等或有去重键。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S08 -->
- 适用情形：规划生产 migration 时。接受停机窗口或锁表风险须由人工判断。

<!-- rule-id: TECH-248-SCHEMA-DATA-CONFIGURATION-FEATURE-FLAG-S03 -->
- 适用情形：配置 Vite env 时。Vite env 禁止包含 key、token、数据库 URL 或 JWT secret。

<!-- rule-id: TECH-250-SCHEMA-DATA-EXTERNAL-SIDE-EFFECTS-S01 -->
- 适用情形：扩大外部集成时。新 provider、公开 webhook、订阅事件或 breaking schema 须由人工判断。

<!-- rule-id: TECH-218-JOB-CLAIM-TRANSACTION-S01 -->
- 适用情形：实现 worker claim 时。claim job 须在事务中完成。

<!-- rule-id: TECH-217-JOB-CLAIM-SQL-PORTABILITY-S01 -->
- 适用情形：设计队列 claim SQL 时。数据库专有 skip-locked/claim 语法禁止作为默认核心 SQL。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S06 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时事务须承担引用完整性。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S07 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时须按关系需要使用唯一或非空约束承担引用完整性。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S08 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时删除策略须承担引用完整性。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S09 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时补偿任务须承担引用完整性。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S10 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时定期一致性扫描须承担引用完整性。

<!-- rule-id: TECH-183-DATABASE-TABLE-SCHEMA-S02 -->
- 适用情形：持久化客户上线状态时。客户上线 sqlc 表仅允许存引用、状态和脱敏摘要。

### 认证授权、安全、凭据与审计

<!-- rule-id: TECH-002-AI-WRITE-ACTION-SCHEMA -->
- AI 触发写操作时须经过结构化 action schema。

<!-- rule-id: TECH-215-SECURITY-SPECIALTY-APPLICABILITY -->
- 未触发安全专项时，由技术设计总入口继续完成适用性分流。

<!-- rule-id: TECH-256-TECH-DATA-SECURITY-COST-TRUST-SCOPE -->
- 改变技术、数据、安全、成本或信任边界的工作属于技术设计适用范围。

<!-- rule-id: TECH-134-AUTH-SPECIALTY-TRIGGER -->
- 只有 change 涉及安全、数据、Auth、租户、secret、供应链或 AI 工具权限时才启用安全/Auth 专项。

<!-- rule-id: TECH-134-AUTH-DEFAULT-DENY-LEAST-PRIVILEGE -->
- 安全边界缺省拒绝，权限遵循最小权限。

<!-- rule-id: TECH-134-PER-ACCESS-PERMISSION-CHECK -->
- 每次受保护访问都须执行权限检查。

<!-- rule-id: TECH-134-AUTH-THIN-SLICE -->
- 安全/Auth 工件允许从当前单个 target 的最小 thin slice 开始。

<!-- rule-id: TECH-134-OBJECT-TENANT-AUTHORIZATION -->
- 授权须同时覆盖 object-level 与 tenant-level。

<!-- rule-id: TECH-134-AI-AUTH-CONTEXT-INHERITANCE -->
- AI agent/tool 调用须继承 actor、tenant 和 permission。

<!-- rule-id: TECH-134-CI-PRODUCTION-PERMISSION-HUMAN-GATE -->
- CI job 或外部 action 获得生产权限须交由人工判断。

<!-- rule-id: TECH-134-AUTH-MINIMUM-KERNEL-PRECEDENCE -->
- 安全/Auth 专项与本规范的正式分类及项目原则冲突时，以正式规范为准。

<!-- rule-id: TECH-130-AUDIT-LOG-APPEND-ONLY -->
- 高风险动作的审计记录采用 append-only 或其他不可随意覆盖的等价结构。

<!-- rule-id: TECH-130-AUDIT-EVIDENCE-REFERENCE-AND-REDACTION -->
- admin action 审计证据以引用、摘要、hash 或 redacted diff 表示；禁止保存完整 secret、完整 raw prompt、完整 raw response 或不必要个人数据。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S15 -->
- 适用情形：配置前端分析时。VITE_* 禁止存放服务端 secret、管理员 token 或 warehouse credential。

<!-- rule-id: TECH-055-AI-TOOL-PERMISSION-S01 -->
- 适用情形：采集 AI 产品事件时且无明确例外批准。缺省不记录原始 AI 输入输出、工具输出、上传正文或长摘要。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S16 -->
- 适用情形：出现所列实验异常时。可信度或隐私异常后的停止、重跑、回滚或参考用途须交由人工判断。

<!-- rule-id: TECH-131-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：变更涉及所列高影响表面时。技术设计 覆盖用户、生产、数据、权限、供应商或承诺变更。

<!-- rule-id: TECH-131-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：变更涉及所列风险边界时。数据、隐私、安全、Auth、租户或高风险 AI 边界变化须交由人工判断。

<!-- rule-id: TECH-132-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：AI workflow 可能产生高风险副作用时。AI 高风险副作用须经过 auth、cost 和 security 边界。

<!-- rule-id: TECH-056-AI-TOOL-PERMISSION-S01 -->
- 适用情形：考虑引入 agent 时。只在开放式多步且需工具选择和状态管理时引入 agent。

<!-- rule-id: TECH-048-AI-SIDE-EFFECT-AUTHORIZATION-S01 -->
- 适用情形：AI 输出将进入高影响副作用时。高影响输出执行前须经过授权边界。

<!-- rule-id: TECH-133-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：考虑改变所列语义时。错误、重试、权限、幂等或用户失败语义变化须交由人工判断。

<!-- rule-id: TECH-057-AI-TOOL-PERMISSION-S01 -->
- 适用情形：处理 AI/tool 输出时。AI 或 tool 输出禁止直接执行高风险副作用。

<!-- rule-id: TECH-057-AI-TOOL-PERMISSION-S02 -->
- 适用情形：调用高风险 AI 工具时。高风险 AI 工具需要 dry-run、人审或审批。

<!-- rule-id: TECH-057-AI-TOOL-PERMISSION-S03 -->
- 适用情形：外部系统将接收用户数据时。新处理方或工具接收用户数据须交由人工判断。

<!-- rule-id: TECH-135-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：license gate 失败时。license gate 失败时仅允许替换、授权或经人审接受风险。

<!-- rule-id: TECH-135-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：考虑所列 IP 风险时。高风险许可、无授权素材、客户内容复用或 AI-only 权利声明须交由人工判断。

<!-- rule-id: TECH-257-SECURITY-PRIVACY-S07 -->
- 适用情形：change 涉及 AI 工具或输入输出时。AI 安全须覆盖不安全输出处理；AI 安全须覆盖工具越权。

<!-- rule-id: TECH-136-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：定义 AI capability 时。须确认权限边界可接受。

<!-- rule-id: TECH-136-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：决定 AI 工具权限时。上线高权限工具须由人工判断。

<!-- rule-id: TECH-259-SECURITY-PRIVACY-S01 -->
- 适用情形：改变内容安全策略时。改变 policy boundary 须由人工判断。

<!-- rule-id: TECH-137-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：执行授权判断时。长期记忆和 RAG context 禁止作为授权事实。

<!-- rule-id: TECH-137-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：默认注入长期上下文时。缺少权限控制的内容禁止默认注入模型。

<!-- rule-id: TECH-137-AUTH-TENANT-PERMISSION-S03 -->
- 适用情形：执行权限判断时。记忆禁止作为授权事实，权限必须由后端 Auth/tenant boundary 判定。

<!-- rule-id: TECH-137-AUTH-TENANT-PERMISSION-S04 -->
- 适用情形：扩大上下文共享范围时。跨用户、tenant、workspace 或 project 共享上下文资产须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：改变生产模型、工具或数据边界时。生产 AI runtime 默认变化须有权限 gate。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：处理 runtime 外部输入时。不可信输入和外部上下文禁止改变 developer/system 指令或权限判断。

<!-- rule-id: TECH-059-AI-TOOL-PERMISSION-S01 -->
- 适用情形：将工具用于生产时。未注册工具禁止进入任何生产 AI 工具表面。

<!-- rule-id: TECH-059-AI-TOOL-PERMISSION-S02 -->
- 适用情形：注册有副作用工具时。非 read_only 工具缺省 requires_approval true；非 read_only 工具须支持 dry-run 或明确补偿方案；非 read_only 工具须记录幂等键；非 read_only 工具须有审计事件。

<!-- rule-id: TECH-059-AI-TOOL-PERMISSION-S03 -->
- 适用情形：运行高风险工具时。destructive 工具缺省需要 human checkpoint。

<!-- rule-id: TECH-059-AI-TOOL-PERMISSION-S04 -->
- 适用情形：运行高风险工具时。money_movement 工具缺省需要 human checkpoint。

<!-- rule-id: TECH-059-AI-TOOL-PERMISSION-S05 -->
- 适用情形：运行高风险工具时。admin 工具缺省需要 human checkpoint。

<!-- rule-id: TECH-059-AI-TOOL-PERMISSION-S06 -->
- 适用情形：运行高风险工具时。external_message 工具缺省需要 human checkpoint。

<!-- rule-id: TECH-059-AI-TOOL-PERMISSION-S07 -->
- 适用情形：运行高风险工具时。code_execution 工具缺省需要 human checkpoint。

<!-- rule-id: TECH-059-AI-TOOL-PERMISSION-S08 -->
- 适用情形：处理工具输出时。工具输出须视为不可信数据；工具输出禁止作为 system/developer instruction；工具输出禁止作为已批准状态。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S03 -->
- 适用情形：处理工具输出时。工具输出禁止作为权限声明。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S04 -->
- 适用情形：判断 AI 工具权限时。服务端禁止接受模型声称已授权；服务端禁止接受前端声称已授权。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S05 -->
- 适用情形：授权 connector 或 MCP 时。初始 connector/MCP scope 须采用最小可用权限。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S06 -->
- 适用情形：扩大 connector 或 MCP scope 时。需要写操作或敏感数据时才增量授权。

<!-- rule-id: TECH-261-SECURITY-PRIVACY-S01 -->
- 适用情形：处理 runtime secret 时。token、key、cookie 和连接串禁止进入工具输出；token、key、cookie 和连接串禁止进入审计正文；token、key、cookie 和连接串禁止进入前端日志。

<!-- rule-id: TECH-059-AI-TOOL-PERMISSION-S09 -->
- 适用情形：处理 connector 或 MCP 返回时。外部工具和 MCP server 返回内容须按不可信输入处理。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S07 -->
- 适用情形：设计 AI runtime retry 时。模型 route 层禁止盲目重试权限变更。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S08 -->
- 适用情形：改变模型时。更换模型禁止扩大工具权限。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S09 -->
- 适用情形：授权 AI 工具时。允许 AI 调用写操作须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S10 -->
- 适用情形：授权 AI 工具时。允许 AI 调用删除须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S11 -->
- 适用情形：授权 AI 工具时。允许 AI 调用退款须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S12 -->
- 适用情形：授权 AI 工具时。允许 AI 调用 credit 须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S13 -->
- 适用情形：授权 AI 工具时。允许 AI 改变权益须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S14 -->
- 适用情形：授权 AI 工具时。允许 AI 改变权限须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S15 -->
- 适用情形：授权 AI 工具时。允许 AI 发送外部通知须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S16 -->
- 适用情形：授权 AI 工具时。允许 AI 改变生产配置须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S17 -->
- 适用情形：授权 AI 工具时。允许 AI 执行后台操作须由人工判断。

<!-- rule-id: TECH-140-AUTH-TENANT-PERMISSION-S18 -->
- 适用情形：授权 AI 工具时。允许 AI 调用跨租户工具须由人工判断。

<!-- rule-id: TECH-141-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：实现项目发生相应变化时。改变权限须由人工判断。

<!-- rule-id: TECH-141-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：授权 AI coding 时。允许 AI agent 执行有副作用命令须由人工判断。

<!-- rule-id: TECH-141-AUTH-TENANT-PERMISSION-S03 -->
- 适用情形：授权 AI coding 时。允许 AI agent 访问真实数据须由人工判断。

<!-- rule-id: TECH-141-AUTH-TENANT-PERMISSION-S04 -->
- 适用情形：授权 AI coding 时。允许 AI agent 调用真实供应商须由人工判断。

<!-- rule-id: TECH-142-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：扩大服务边界时。引入认证、多租户、计费或第三方登录须由人工判断。

<!-- rule-id: TECH-143-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：处理用户数据时。删除、导出、匿名化、合并账号或修改权限数据须设置人工 checkpoint。

<!-- rule-id: TECH-262-SECURITY-PRIVACY-S01 -->
- 适用情形：设计配置时。配置禁止作为 secret 仓库。

<!-- rule-id: TECH-262-SECURITY-PRIVACY-S02 -->
- 适用情形：管理 secret 配置时。secret 配置仅允许记录引用；secret 配置仅允许记录来源；secret 配置禁止记录真实值。

<!-- rule-id: TECH-262-SECURITY-PRIVACY-S03 -->
- 适用情形：编写配置注册表时。配置注册表禁止存真实 secret 值。

<!-- rule-id: TECH-144-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：登记 permission flag 时。permission toggle 须进入 auth boundary。

<!-- rule-id: TECH-145-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：使用 AI coding 时。AI coding 禁止替代权威产品输入、体验设计和人工高影响判断。

<!-- rule-id: TECH-060-AI-TOOL-PERMISSION-S01 -->
- 适用情形：扩大开发工作区时。新增长期工具、容器栈、付费工具或并行 agent 同边界须由人工判断。

<!-- rule-id: TECH-145-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：授权 AI coding 时。让 AI 扩大副作用、真实数据、自主权或 scope 须由人工判断。

<!-- rule-id: TECH-146-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：实现副作用 job 时。retry 禁止导致重复邮件、扣费或权限修改。

<!-- rule-id: TECH-264-SECURITY-PRIVACY-S01 -->
- 适用情形：使用 background mode 时。background mode 用于 ZDR 或强隐私路径须人工确认。

<!-- rule-id: TECH-264-SECURITY-PRIVACY-S02 -->
- 适用情形：改变 AI background 数据边界时。background mode 用于强隐私或改变结果保留须由人工判断。

<!-- rule-id: TECH-144-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：管理 secret 配置时。secret 配置仅允许记录权限。

<!-- rule-id: TECH-177-CREDENTIAL-ROTATION-REVOCATION-S01 -->
- 适用情形：管理 secret 配置时。secret 配置仅允许记录轮换信息。

<!-- rule-id: TECH-265-SECURITY-PRIVACY-S01 -->
- 适用情形：配置发布 secret 时。secrets 默认禁止写入 workflow、Dockerfile、build args 或仓库文件。

<!-- rule-id: TECH-265-SECURITY-PRIVACY-S02 -->
- 适用情形：构建 production image 时。runtime image 禁止包含 secret。

<!-- rule-id: TECH-147-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：配置 GitHub Actions 时。GitHub Actions 缺省 permissions 为 contents:read。

<!-- rule-id: TECH-147-AUTH-TENANT-PERMISSION-S03 -->
- 适用情形：配置 GitHub Actions 时。仅有 deploy job 可以提升到必要权限。

<!-- rule-id: TECH-265-SECURITY-PRIVACY-S03 -->
- 适用情形：构建 container artifact 时。禁止通过 Docker build args 传 secret。

<!-- rule-id: TECH-266-SECURITY-PRIVACY-S01 -->
- 适用情形：创建客户 account 别名时。account 别名禁止使用客户 secret。

<!-- rule-id: TECH-148-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：维护 tenant provisioning 时。tenant_id_ref 仅允许写系统引用。

<!-- rule-id: TECH-148-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：维护 tenant_id_ref 时。tenant_id_ref 禁止写入真实 tenant secret；tenant_id_ref 禁止写入真实 session；tenant_id_ref 禁止写入真实 JWT；tenant_id_ref 禁止写入真实 客户邮箱。

<!-- rule-id: TECH-148-AUTH-TENANT-PERMISSION-S03 -->
- 适用情形：维护 tenant identity 时。真实 IdP secret 禁止进入 tenant provisioning 文件。

<!-- rule-id: TECH-148-AUTH-TENANT-PERMISSION-S05 -->
- 适用情形：实现客户专属配置时。客户专属配置必须经 config、feature flag、entitlement 或 tenant config 管理，禁止在 Go 代码写客户特例。

<!-- rule-id: TECH-179-CREDENTIAL-SCOPE-EXPANSION-CHECKPOINT-S01 -->
- 适用情形：决定扩大 credential scope 时。扩大 credential scope 须设置人工 checkpoint。

<!-- rule-id: TECH-178-CREDENTIAL-ROTATION-REVOCATION-S01 -->
- 适用情形：定义credentials/rotation-run/<target>.json工件时。rotation run 的 steps 禁止记录 secret value。

### 配置、成本、供应商与其他技术边界

<!-- rule-id: TECH-088-PUBLIC-API-HUMAN-GATE -->
- 改变公共 API 须由人工判断。

<!-- rule-id: TECH-215-SENSITIVE-DATA-HUMAN-GATE -->
- 处理敏感、高影响或受监管数据须交由人工判断。

<!-- rule-id: TECH-234-PLATFORM-CAPABILITY-SEPARATE-CHANGE -->
- 自建训练平台、复杂多云 gateway、自动竞价或企业安全平台不属于默认建设范围，须由单独的 OpenSpec change 承载。

<!-- rule-id: TECH-089-INCOMPATIBLE-CHANGE-HUMAN-GATE -->
- 接受破坏既有 API 或数据兼容须交由人工判断。

<!-- rule-id: TECH-134-SELF-HOSTED-PASSWORD-LOGIN-REVIEW -->
- 自建密码登录须接受单独人工审查。

<!-- rule-id: TECH-134-TENANT-CONTEXT-ORIGIN -->
- 只有身份和 membership 均已验证后才派生 tenant context；调用端直接提供的 tenant id 禁止被当作可信事实。

<!-- rule-id: TECH-134-IDENTITY-CAPABILITY-HUMAN-GATE -->
- 自建登录、企业身份、高权限或 impersonation 须交由人工判断。

<!-- rule-id: TECH-134-HIGH-PRIVILEGE-WRITE-HUMAN-GATE -->
- 跨租户管理员访问、service token 写生产或 AI 代写须交由人工判断。

<!-- rule-id: TECH-191-TRACKING-PLAN-PRODUCTION-GATE -->
- 没有 tracking plan 的事件禁止进入生产。

<!-- rule-id: TECH-191-EVENT-NAMING -->
- 产品事件名采用稳定 snake_case，禁止包含用户 ID、资源 ID、时间戳、邮箱、动态 path、UUID、实验 variant 或 UI 文案版本。

<!-- rule-id: TECH-191-EVENT-PROPERTY-SENSITIVITY -->
- 事件属性不得接收敏感标识、凭据或原始内容；禁入集合按类别固定如下：
  - 身份、联系与位置：`full_name`、`email`、`phone`、`address`、`precise_location`、`raw_ip`、`ssn`。
  - 认证与支付：`password`、`secret`、`token`、`session_cookie`、`payment_card`、`cvv`。
  - 原始交互内容：`raw_prompt`、`raw_response`、`raw_user_input`、`message_body`、`free_text`、`url_query`。

<!-- rule-id: TECH-191-TRUSTED-OUTCOME-EVENT-SOURCE -->
- 关键 outcome 事件优先考虑由后端或可信边界产生。

<!-- rule-id: TECH-191-EVENT-PURPOSE -->
- 每个产品事件须回答一个产品或运营问题；无法解释用途的事件禁止采集。

<!-- rule-id: TECH-201-SERVICE-BOUNDARY-DEFAULT -->
- 服务边界缺省不为每个 feature 单拆微服务，优先考虑 modular monolith 或少量服务。

<!-- rule-id: TECH-201-CODE-HYGIENE -->
- 代码维护缺省删除 dead code，并禁止长期保留关闭的 flag 或 commented code。

<!-- rule-id: TECH-203-COST-DATA-VENDOR-TRUST-ROUTING -->
- 未触发成本、数据、供应商或信任专项时，由技术设计总入口继续分流。

<!-- rule-id: TECH-203-CUSTOMER-DATA-LIFECYCLE -->
- 客户数据须具有生命周期定义。

<!-- rule-id: TECH-203-EXTERNAL-MATERIAL-SOURCE -->
- 外部材料须具有来源记录。

<!-- rule-id: TECH-203-MINIMUM-ARTIFACT-SELECTION -->
- 专项工件按真实触发选择最小集合。

<!-- rule-id: TECH-203-TRIGGER-ONLY-ARTIFACT-SELECTION -->
- 每次只补充与触发条件对应的最小工件。

<!-- rule-id: TECH-203-DATA-CHANGE-HUMAN-GATE -->
- 新增敏感或跨边界数据处理、批量删除或例外须交由人工判断。

<!-- rule-id: TECH-241-CORE-ROUTE-FALLBACK -->
- 用户可见核心路径须具有 fallback。

<!-- rule-id: TECH-241-CENTRALIZED-RUNTIME-TIMEOUT -->
- 后端 AI runtime 的 timeout 禁止散落硬编码在业务代码中。

<!-- rule-id: TECH-241-MISSING-FALLBACK-HUMAN-GATE -->
- 接受没有 fallback 的用户可见 AI 能力须交由人工判断。

<!-- rule-id: TECH-157-BILLING-ENTITLEMENT-PRICING-S01 -->
- 适用情形：涉及所列高影响取舍时。now/expedite、定价、数据边界和长期架构锁定须由人决定。

<!-- rule-id: TECH-173-COST-VENDOR-S01 -->
- 适用情形：设计产品事件时。产品分析仅采集支持决策、排障、成本控制或体验改进的事件。

<!-- rule-id: TECH-214-GOVERNANCE-PRODUCT-ANALYTICS-EXPERIMENT-S04 -->
- 适用情形：采集或发送产品分析数据时。原始内容、直接标识、支付信息和精确位置禁止发给 analytics。

<!-- rule-id: TECH-230-PLANNING-GOVERNANCE-ROUTING-S01 -->
- 适用情形：计划采用所列高隐私影响能力时。第三方分析、回放、跨站追踪、广告归因、数据出口和画像缺省需要人工 checkpoint。

<!-- rule-id: TECH-214-GOVERNANCE-PRODUCT-ANALYTICS-EXPERIMENT-S05 -->
- 适用情形：分析必须使用用户标识时。须使用用户标识时优先使用不可反推的内部 surrogate key。

<!-- rule-id: TECH-214-GOVERNANCE-PRODUCT-ANALYTICS-EXPERIMENT-S06 -->
- 适用情形：保留产品分析数据时。产品分析数据缺省短期保留。

<!-- rule-id: TECH-230-PLANNING-GOVERNANCE-ROUTING-S02 -->
- 适用情形：计划进行所列高影响数据使用时。超过 13 个月、跨产品合并、第三方导出或训练个性化需人工 checkpoint。

<!-- rule-id: TECH-168-CONFIG-FLAGS-S02 -->
- 适用情形：配置前端分析时。缺省关闭 autocapture、session replay 和 DOM/text capture。

<!-- rule-id: TECH-209-GOVERNANCE-MAIN-S01 -->
- 适用情形：使用 技术设计 时。技术设计 不代替产品发现。

<!-- rule-id: TECH-209-GOVERNANCE-MAIN-S02 -->
- 适用情形：使用 技术设计 时。技术设计 不承担上线证明。

<!-- rule-id: TECH-231-PLANNING-GOVERNANCE-ROUTING-S01 -->
- 适用情形：Standard/High-risk 变更进入实现前。技术设计 将工作压成可审查 OpenSpec change 并在实现前确认高影响边界。

<!-- rule-id: TECH-209-GOVERNANCE-MAIN-S03 -->
- 适用情形：修复满足全部低风险条件时。低风险可回滚且无需详细规格的修复无需应用 技术设计。

<!-- rule-id: TECH-209-GOVERNANCE-MAIN-S07 -->
- 适用情形：变更涉及所列数据风险时。敏感数据、高影响领域、删除例外、不可逆数据或权利履行缺口须交由人工判断。

<!-- rule-id: TECH-219-LIVE-INCIDENT-RESPONSE-S01 -->
- 适用情形：考虑接受所列供应链风险时。接受高危漏洞、未签名 release 或无 provenance 交付物须交由人工判断。

<!-- rule-id: TECH-174-COST-VENDOR-S01 -->
- 适用情形：设计成本边界时。成本须有硬限制。

<!-- rule-id: TECH-174-COST-VENDOR-S02 -->
- 适用情形：考虑所列成本风险时。上调预算、取消 hard cap、无限循环或高成本真实运行须交由人工判断。

<!-- rule-id: TECH-174-COST-VENDOR-S03 -->
- 适用情形：cost/data/vendor/trust 专项与本规范的正式分类及项目原则冲突时。冲突时以正式规范为准。

<!-- rule-id: TECH-174-COST-VENDOR-S06 -->
- 适用情形：设计 AI 成本容量时。AI token须有上限。

<!-- rule-id: TECH-174-COST-VENDOR-S07 -->
- 适用情形：设计 AI 成本容量时。请求须有上限。

<!-- rule-id: TECH-174-COST-VENDOR-S08 -->
- 适用情形：设计 AI 成本容量时。工具循环须有上限。

<!-- rule-id: TECH-174-COST-VENDOR-S09 -->
- 适用情形：设计 AI 成本容量时。batch须有上限。

<!-- rule-id: TECH-174-COST-VENDOR-S10 -->
- 适用情形：设计 AI 成本容量时。导出须有上限。

<!-- rule-id: TECH-210-GOVERNANCE-MAIN-S01 -->
- 适用情形：定义 AI capability 时。须确认用户数据边界可接受。

<!-- rule-id: TECH-210-GOVERNANCE-MAIN-S02 -->
- 适用情形：推进用户可见 AI 能力时。没有回滚或降级路径禁止进入实现或发布。

<!-- rule-id: TECH-210-GOVERNANCE-MAIN-S03 -->
- 适用情形：判断 AI 技术设计 适用范围时。结构化输出变化纳入 AI 技术设计。

<!-- rule-id: TECH-210-GOVERNANCE-MAIN-S04 -->
- 适用情形：判断 AI 技术设计 是否适用时。数据边界未明确时回到 技术设计。

<!-- rule-id: TECH-175-COST-VENDOR-S01 -->
- 适用情形：升级 AI workflow 时。升级 workflow 的成本和延迟须在产品可接受范围。

<!-- rule-id: TECH-233-PLANNING-GOVERNANCE-ROUTING-S01 -->
- 适用情形：选择 AI 技术设计专项时。普通 AI 技术设计 工作须先回主入口。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S01 -->
- 适用情形：设计 AI route 时。须先定义任务类型再选择模型和工具。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S10 -->
- 适用情形：设计非核心 AI route 时。非核心 AI enhancement 可 fail closed 或关闭。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S12 -->
- 适用情形：选择高成本 AI route 时。仅高价值低延迟路径考虑 priority 或更强模型。

<!-- rule-id: TECH-158-BILLING-ENTITLEMENT-PRICING-S01 -->
- 适用情形：运行高风险工具时。entitlement 工具缺省需要 human checkpoint。

<!-- rule-id: TECH-155-BACKUP-RESTORE-RECOVERY-S01 -->
- 适用情形：能力未提供 rollback 或 compensation 方式时。接受既没有 rollback 也没有 compensation 的用户可见 AI 能力须由人工判断。

<!-- rule-id: TECH-269-USER-CONTROL-S01 -->
- 适用情形：扩大 AI runtime 资源时。取消 AI 硬限制须由人工判断。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S13 -->
- 适用情形：改变 AI runtime 安全控制时。关闭 kill switch 须由人工判断。

<!-- rule-id: TECH-211-GOVERNANCE-MAIN-S01 -->
- 适用情形：实现项目发生相应变化时。改变错误语义须由人工判断。

<!-- rule-id: TECH-211-GOVERNANCE-MAIN-S02 -->
- 适用情形：实现项目发生相应变化时。改变租户边界须由人工判断。

<!-- rule-id: TECH-212-GOVERNANCE-MAIN-S01 -->
- 适用情形：引入开发工具时。新增付费工具链须由人工判断。

<!-- rule-id: TECH-165-CONFIG-FLAG-RUNTIME-ROUTING-S01 -->
- 适用情形：改变运行时控制时。允许生产配置运行时切换须由人工判断。

<!-- rule-id: TECH-165-CONFIG-FLAG-RUNTIME-ROUTING-S02 -->
- 适用情形：改变运行时控制时。允许 Feature Flag 运行时切换须由人工判断。

<!-- rule-id: TECH-165-CONFIG-FLAG-RUNTIME-ROUTING-S03 -->
- 适用情形：改变运行时控制时。允许 kill switch 运行时切换须由人工判断。

<!-- rule-id: TECH-165-CONFIG-FLAG-RUNTIME-ROUTING-S04 -->
- 适用情形：改变运行时控制时。允许 AI route 运行时切换须由人工判断。

<!-- rule-id: TECH-165-CONFIG-FLAG-RUNTIME-ROUTING-S05 -->
- 适用情形：改变运行时控制时。允许高成本能力运行时切换须由人工判断。

<!-- rule-id: TECH-212-GOVERNANCE-MAIN-S02 -->
- 适用情形：决定 实现交接边界时。接受没有幂等的实现进入下一步须由人工判断。

<!-- rule-id: TECH-213-GOVERNANCE-MAIN-S01 -->
- 适用情形：决定 实现交接边界时。接受没有回滚的实现进入下一步须由人工判断。

<!-- rule-id: TECH-156-BACKUP-RESTORE-RECOVERY-S01 -->
- 适用情形：实现可取消的写操作时。写操作须有幂等或事务策略。

<!-- rule-id: TECH-170-CONFIG-FLAGS-S01 -->
- 适用情形：配置前端环境时。VITE 变量须视为公开信息。

<!-- rule-id: TECH-167-CONFIG-FLAG-RUNTIME-ROUTING-S01 -->
- 适用情形：设计 Feature Flag 时。flag 禁止作为永久产品策略。

<!-- rule-id: TECH-167-CONFIG-FLAG-RUNTIME-ROUTING-S05 -->
- 适用情形：登记生产配置时。生产配置须具备：validation、rollback。

<!-- rule-id: TECH-171-CONFIG-FLAGS-S01 -->
- 适用情形：登记敏感配置时。敏感配置禁止记录真实值。

<!-- rule-id: TECH-171-CONFIG-FLAGS-S02 -->
- 适用情形：登记前端配置时。client exposed 配置禁止敏感。

<!-- rule-id: TECH-167-CONFIG-FLAG-RUNTIME-ROUTING-S07 -->
- 适用情形：记录 runtime change 时。runtime change 日志禁止记录 secret、token、password、连接串、邮箱或手机号。

<!-- rule-id: TECH-167-CONFIG-FLAG-RUNTIME-ROUTING-S08 -->
- 适用情形：处理 AI runtime 输入时。运行时禁止把用户输入拼成未校验 prompt 或 config key。

<!-- rule-id: TECH-159-BILLING-ENTITLEMENT-PRICING-S01 -->
- 适用情形：修正账本时。账本修正须使用 compensating event、credit 或 adjustment。

<!-- rule-id: TECH-159-BILLING-ENTITLEMENT-PRICING-S02 -->
- 适用情形：操作生产副作用时。生产 replay、批量账权、credit、退款或重复副作用处理须由人工判断。

<!-- rule-id: TECH-167-CONFIG-FLAG-RUNTIME-ROUTING-S09 -->
- 适用情形：登记 AI route flag 时。AI model route flag 须进入成本边界；AI model route flag 须进入安全边界。

<!-- rule-id: TECH-237-PLANNING-GOVERNANCE-ROUTING-S01 -->
- 适用情形：计划扩张或转付费时。Expansion / Conversion 须受 商业承诺专项约束。

<!-- rule-id: TECH-205-GOVERNANCE-CUSTOMER-PILOT-ONBOARDING-LAUNCH-S06 -->
- 适用情形：启用客户数据进入 AI 前。客户数据进入 AI 前须有 provider boundary。

<!-- rule-id: TECH-194-EXTERNAL-CLAIM-COMMITMENT-S01 -->
- 适用情形：claim substantiation 为 unsupported 时。unsupported claim 只能处于 draft 或 blocked，禁止进入 approved 或 published。

<!-- rule-id: TECH-194-EXTERNAL-CLAIM-COMMITMENT-S02 -->
- 适用情形：claim 证据过期时。expires_at 过期后 claim 必须进入 needs_review 且禁止继续发布强声明。

<!-- rule-id: TECH-194-EXTERNAL-CLAIM-COMMITMENT-S03 -->
- 适用情形：保全 claim correction 证据时。claim correction 证据禁止复制 secret。

<!-- rule-id: TECH-194-EXTERNAL-CLAIM-COMMITMENT-S04 -->
- 适用情形：记录 claim gate 事件时。claim gate 日志禁止保存敏感内容。

<!-- rule-id: TECH-194-EXTERNAL-CLAIM-COMMITMENT-S05 -->
- 适用情形：设计 claim surface 时。禁止用营销视觉削弱限制说明。

### AI runtime、模型、上下文与工具

<!-- rule-id: TECH-258-USER-VISIBLE-AI-SAFETY-GATE -->
- 缺少安全边界的用户可见 AI 能力禁止进入实现或发布。

<!-- rule-id: TECH-149-AI-EXTERNAL-CLAIM-BOUNDARY -->
- AI 处理外部文案时，禁止自行发布、扩写或强化 external claim。

<!-- rule-id: TECH-149-AI-CLAIM-CORRECTION-PUBLISH-BOUNDARY -->
- AI 发现 claim 冲突时，禁止自动发布 claim correction。

<!-- rule-id: TECH-234-AI-QUALITY-ROUTING-BOUNDARY -->
- 仅定义 AI 好坏、失败或降级时，由 AI 技术设计总入口继续分流。

<!-- rule-id: TECH-201-DETERMINISTIC-AI-WORKFLOW -->
- AI workflow 优先考虑确定性编排。

<!-- rule-id: TECH-026-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：采集前端事件时。表单、prompt、自由文本、URL、文件名和直接标识禁止进入事件属性。

<!-- rule-id: TECH-014-AI-MODEL-ROUTING-S01 -->
- 适用情形：变更引入所列长期义务时。长期架构、关键供应商、出境、DPA、训练保留或显著成本须交由人工判断。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S01 -->
- 适用情形：组织 Go/Kratos 服务时。internal/biz 禁止 import data、transport、SQL driver 或 model vendor SDK。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S02 -->
- 适用情形：考虑拆分服务时。只在数据、发布、可靠性或供应商安全边界明确时拆服务。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S03 -->
- 适用情形：组织 AI 依赖时。AI model/vendor SDK 不纳入 domain/biz 层。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S05 -->
- 适用情形：考虑所列依赖时。引入新框架、供应商 SDK、agent runtime 或公共组件库须交由人工判断。

<!-- rule-id: TECH-028-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：处理 secret 时。secret 禁止进入仓库、日志或 prompt。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S01 -->
- 适用情形：当前 change 命中所列风险时。只在 change 涉及成本、客户数据、供应商、出境、IP、AI 内容或承诺时读取本专项。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S03 -->
- 适用情形：供应商缺少所列保障时。接受缺少关键条款或数据边界的供应商须交由人工判断。

<!-- rule-id: TECH-028-AI-PROMPT-ARTIFACT-S02 -->
- 适用情形：change 涉及 AI 工具或输入输出时。AI 安全须覆盖AI prompt injection。

<!-- rule-id: TECH-047-AI-SENSITIVE-DISCLOSURE-SAFETY-S01 -->
- 适用情形：change 涉及 AI 工具或输入输出时。AI 安全须覆盖敏感信息泄露。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S07 -->
- 适用情形：设计 AI 成本容量时。供应商调用须有上限。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S09 -->
- 适用情形：调用供应商时。供应商调用须具备：disable switch、数据最小化。

<!-- rule-id: TECH-018-AI-MODEL-ROUTING-S01 -->
- 适用情形：判断 AI 技术设计 适用范围时。模型路由变化纳入 AI 技术设计。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S01 -->
- 适用情形：决定 AI 自治等级时。上线 autonomous agent 须由人工判断。

<!-- rule-id: TECH-018-AI-MODEL-ROUTING-S03 -->
- 适用情形：规划模型优化时。模型优化前先确认数据边界。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S02 -->
- 适用情形：实现新 AI 能力时。新 AI 能力缺省使用 deterministic workflow 或单次 Responses API 调用，不默认采用 autonomous agent。

<!-- rule-id: TECH-051-AI-TOOL-LEAST-PRIVILEGE-S01 -->
- 适用情形：定义 AI 工具调用时。工具调用缺省最小权限。

<!-- rule-id: TECH-052-AI-TOOL-NECESSITY-S01 -->
- 适用情形：接入 AI 工具时。仅真实需要外部数据或副作用时添加工具。

<!-- rule-id: TECH-003-AI-AGENT-USE-CASE-S01 -->
- 适用情形：决定是否升级 agent 时。仅有固定 workflow 不足时才考虑升级 agent。

<!-- rule-id: TECH-009-AI-INSTRUCTION-TRUST-BOUNDARY-S01 -->
- 适用情形：处理用户输入时。不可信用户输入只能进入 user/input 数据区，禁止拼入 developer/system 高优先级指令。

<!-- rule-id: TECH-019-AI-MODEL-ROUTING-S01 -->
- 适用情形：选择 AI workflow 层级时。规则或传统代码能解决时不用模型。

<!-- rule-id: TECH-019-AI-MODEL-ROUTING-S02 -->
- 适用情形：选择 AI workflow 层级时。单次模型调用能解决时不用 workflow。

<!-- rule-id: TECH-067-AI-WORKFLOW-PATTERN-SELECTION-S01 -->
- 适用情形：选择 AI workflow 层级时。固定步骤能提升质量时采用 deterministic workflow。

<!-- rule-id: TECH-067-AI-WORKFLOW-PATTERN-SELECTION-S02 -->
- 适用情形：选择 AI workflow 层级时。需要分类分流时采用 routing。

<!-- rule-id: TECH-067-AI-WORKFLOW-PATTERN-SELECTION-S03 -->
- 适用情形：选择 AI workflow 层级时。需要多个独立视角时采用 parallelization。

<!-- rule-id: TECH-003-AI-AGENT-USE-CASE-S02 -->
- 适用情形：选择 AI workflow 层级时。仅步数不可预知且需工具探索恢复时采用 agent。

<!-- rule-id: TECH-069-AI-WORKFLOW-STOP-CHECKPOINT-S01 -->
- 适用情形：升级 AI workflow 时。升级 workflow 须至少有明确停止条件、最大迭代次数或人工 checkpoint 之一。

<!-- rule-id: TECH-068-AI-WORKFLOW-SIDE-EFFECT-CONTROL-S01 -->
- 适用情形：升级 AI workflow 时。升级 workflow 的工具权限和副作用须可审计；升级 workflow 的工具权限和副作用须可回滚或可人工确认。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S01 -->
- 适用情形：定义 AI 工具时。工具名称须清楚。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S02 -->
- 适用情形：定义 AI 工具时。工具参数须清楚。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S03 -->
- 适用情形：定义 AI 工具时。工具描述须清楚。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S05 -->
- 适用情形：定义 AI 工具时。工具参数应避免用自由文本承载指令。

<!-- rule-id: TECH-063-AI-TOOL-SIDE-EFFECT-CONTROL-S01 -->
- 适用情形：定义高风险 AI 工具时。高风险工具缺省 dry-run 或人工批准。

<!-- rule-id: TECH-063-AI-TOOL-SIDE-EFFECT-CONTROL-S02 -->
- 适用情形：定义写操作 AI 工具时。写操作工具须具备：幂等键、审计日志。

<!-- rule-id: TECH-051-AI-TOOL-LEAST-PRIVILEGE-S02 -->
- 适用情形：定义写操作 AI 工具时。写操作工具须有权限检查。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S01 -->
- 适用情形：处理外部工具数据时。外部检索内容须视为不可信输入。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S02 -->
- 适用情形：处理外部工具数据时。网页内容须视为不可信输入。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S03 -->
- 适用情形：处理外部工具数据时。邮件内容须视为不可信输入。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S04 -->
- 适用情形：处理外部工具数据时。用户文件须视为不可信输入。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S05 -->
- 适用情形：处理工具返回数据时。工具返回数据禁止直接升级为高优先级指令。

<!-- rule-id: TECH-036-AI-QUALITY-COST-LATENCY-TRADEOFF-S01 -->
- 适用情形：决定 AI 质量取舍时。接受更高成本换质量须由人工判断。

<!-- rule-id: TECH-036-AI-QUALITY-COST-LATENCY-TRADEOFF-S02 -->
- 适用情形：决定 AI 质量取舍时。接受更高延迟换质量须由人工判断。

<!-- rule-id: TECH-199-GOVERNANCE-AI-EVAL-SAFETY-S01 -->
- 适用情形：设计内容审核时。禁止把内容审核缩减为单次分类器调用。

<!-- rule-id: TECH-198-GOVERNANCE-AI-CONTEXT-MEMORY-RETRIEVAL-S01 -->
- 适用情形：应用 AI context 专项时。与本规范的正式分类及项目原则冲突时，以正式规范为准。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S01 -->
- 适用情形：构建 AI 上下文时。长期记忆和 RAG context 须视为不可信外部上下文。

<!-- rule-id: TECH-029-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：构建 AI prompt 时。长期记忆和 RAG context 禁止作为 system/developer 指令。

<!-- rule-id: TECH-020-AI-MODEL-ROUTING-S01 -->
- 适用情形：默认注入长期上下文时。缺少来源的内容禁止默认注入模型。

<!-- rule-id: TECH-020-AI-MODEL-ROUTING-S02 -->
- 适用情形：默认注入长期上下文时。缺少 TTL 的内容禁止默认注入模型。

<!-- rule-id: TECH-020-AI-MODEL-ROUTING-S03 -->
- 适用情形：默认注入长期上下文时。缺少删除路径的内容禁止默认注入模型。

<!-- rule-id: TECH-029-AI-PROMPT-ARTIFACT-S03 -->
- 适用情形：注入 RAG context 时。RAG context 进入 prompt 时须标记 untrusted context。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S04 -->
- 适用情形：注入 RAG context 时。检索文本中的指令禁止提升为模型指令。

<!-- rule-id: TECH-010-AI-MEMORY-CONTEXT-DEFAULTS-S01 -->
- 适用情形：改变 memory 默认时。默认开启长期记忆须由人工判断；默认引用 chat history 须由人工判断；默认启用 workspace memory 须由人工判断。

<!-- rule-id: TECH-010-AI-MEMORY-CONTEXT-DEFAULTS-S02 -->
- 适用情形：改变 retrieval 默认时。默认检索须由人工判断。

<!-- rule-id: TECH-010-AI-MEMORY-CONTEXT-DEFAULTS-S03 -->
- 适用情形：改变 context injection 默认时。default context injection 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S05 -->
- 适用情形：处理敏感上下文时。保存 sensitive/restricted memory 或客户机密来源须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S06 -->
- 适用情形：处理敏感上下文时。推断 sensitive/restricted memory 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S07 -->
- 适用情形：处理敏感上下文时。默认注入 sensitive/restricted memory 或客户机密来源须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S08 -->
- 适用情形：选择 RAG 来源时。使用权利或政策不清的内容须由人工判断。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S03 -->
- 适用情形：处理上下文删除失败时。接受删除失败须由人工判断。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S04 -->
- 适用情形：处理上下文删除失败时。接受 reindex 失败须由人工判断。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S05 -->
- 适用情形：处理上下文删除失败时。接受 vector store retention 清理失败须由人工判断。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S06 -->
- 适用情形：处理上下文删除失败时。接受 cache 清理失败须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S09 -->
- 适用情形：使用高影响上下文时。在医疗领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S10 -->
- 适用情形：使用高影响上下文时。在法律领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S11 -->
- 适用情形：使用高影响上下文时。在金融领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S12 -->
- 适用情形：使用高影响上下文时。在身份领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S13 -->
- 适用情形：使用高影响上下文时。在就业领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S14 -->
- 适用情形：使用高影响上下文时。在教育领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S15 -->
- 适用情形：使用高影响上下文时。在公共安全领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：应用 AI runtime 专项时。与本规范的正式分类及项目原则冲突时，以正式规范为准。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S01 -->
- 适用情形：决定是否使用 AI runtime 专项时。仅有 AI 技术设计总入口触发模型或工具运行时变化时才使用本专项。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S02 -->
- 适用情形：设计 AI runtime 时。仅有应用运行时拥有执行权。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S02 -->
- 适用情形：改变生产模型、工具或数据边界时。生产 AI runtime 默认变化须有降级路径。

<!-- rule-id: TECH-044-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：生产 AI runtime 默认变化时。生产 AI runtime 默认变化须有回滚或补偿方式。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S03 -->
- 适用情形：调用模型供应商时。request context 须有 deadline。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S04 -->
- 适用情形：处理 runtime secret 时。token、key、cookie 和连接串禁止进入模型上下文。

<!-- rule-id: TECH-033-AI-PROMPT-RUNTIME-CONTRACT-S02 -->
- 适用情形：构建 AI prompt 时。prompt 禁止自行决定供应商；prompt 禁止自行决定权限；prompt 禁止自行决定审批；prompt 禁止自行决定幂等策略；prompt 禁止自行决定租户边界；prompt 禁止自行决定成本上限；prompt 禁止自行决定重试策略。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S03 -->
- 适用情形：实现 autonomous loop 时。autonomous loop须具备：有限步数、有限工具 fanout、有限 token、有限 cost、有限重试。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S04 -->
- 适用情形：loop 超限时。autonomous loop 超限后须降级、转人工或排队。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S05 -->
- 适用情形：改变生产 route 时。改变用户可见生产默认模型须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S06 -->
- 适用情形：改变生产 route 时。改变用户可见生产供应商须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S07 -->
- 适用情形：改变生产 route 时。改变用户可见生产 route 须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S08 -->
- 适用情形：扩大 runtime 供应商时。引入新外部模型供应商须由人工判断。

<!-- rule-id: TECH-043-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：扩大 runtime 集成时。引入新 connector 须由人工判断。

<!-- rule-id: TECH-043-AI-RUNTIME-ROUTING-S02 -->
- 适用情形：扩大 runtime 集成时。引入新 remote MCP server 须由人工判断。

<!-- rule-id: TECH-043-AI-RUNTIME-ROUTING-S03 -->
- 适用情形：扩大 runtime 集成时。引入新本地 MCP server 须由人工判断。

<!-- rule-id: TECH-043-AI-RUNTIME-ROUTING-S04 -->
- 适用情形：扩大 runtime 工具能力时。引入浏览器或电脑控制工具须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S09 -->
- 适用情形：改变 route 数据时。让敏感、监管或高影响数据进入 route 须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S10 -->
- 适用情形：改变供应商数据边界时。扩大供应商或 connector 数据保留边界须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S11 -->
- 适用情形：改变供应商数据边界时。扩大供应商或 connector 数据驻留边界须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S12 -->
- 适用情形：改变供应商数据边界时。扩大供应商或 connector 数据训练边界须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S13 -->
- 适用情形：改变供应商数据边界时。扩大供应商或 connector scope 边界须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S14 -->
- 适用情形：改变 AI 安全 route 时。改变 refusal 或 safety behavior 须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S15 -->
- 适用情形：改变 AI 安全 route 时。改变 moderation route 须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S16 -->
- 适用情形：改变 AI 安全 route 时。改变安全阈值须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S17 -->
- 适用情形：改变 AI 工具 route 时。改变 tool-heavy route 须由人工判断。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S05 -->
- 适用情形：改变 AI 自治等级时。改变 agent 自治等级须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S05 -->
- 适用情形：接受 runtime 控制缺口时。接受没有 dry-run 的用户可见 AI 能力须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S06 -->
- 适用情形：接受 runtime 控制缺口时。接受没有幂等的用户可见 AI 能力须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S07 -->
- 适用情形：接受 runtime 控制缺口时。接受没有审计的用户可见 AI 能力须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S08 -->
- 适用情形：扩大 AI runtime 资源时。提高 AI 预算须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S09 -->
- 适用情形：扩大 AI runtime 资源时。扩大 context window 须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S10 -->
- 适用情形：扩大 AI runtime 资源时。默认高 reasoning effort 须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S11 -->
- 适用情形：扩大 AI runtime 资源时。扩大 loop 上限须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S12 -->
- 适用情形：扩大 AI runtime 资源时。扩大 fanout 须由人工判断。

<!-- rule-id: TECH-022-AI-MODEL-ROUTING-S01 -->
- 适用情形：引入外部供应商时。新增模型供应商须由人工判断。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S06 -->
- 适用情形：授权 AI coding 时。扩大 AI agent 自主权限须由人工判断。

<!-- rule-id: TECH-046-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：设计 runtime 行为时。代码须决定能力边界。

<!-- rule-id: TECH-207-GOVERNANCE-DEV-WORKSPACE-AI-CODING-S01 -->
- 适用情形：使用 AI coding 时。work brief 仅允许承载执行状态。

<!-- rule-id: TECH-023-AI-MODEL-ROUTING-S01 -->
- 适用情形：运行本地 AI workflow 时。本地 AI workflow 缺省使用 dry-run、mock provider 或低成本 sandbox，不默认调用真实模型和真实工具。

<!-- rule-id: TECH-023-AI-MODEL-ROUTING-S02 -->
- 适用情形：使用 AI coding 时。未经人审 AI 禁止访问真实 secret、用户数据、生产数据或真实供应商。

<!-- rule-id: TECH-198-GOVERNANCE-AI-CONTEXT-MEMORY-RETRIEVAL-S02 -->
- 适用情形：决定是否采用该专项时。AI context 专项是可选 playbook，不是缺省流程。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S13 -->
- 适用情形：决定是否采用该专项时。AI runtime 专项是可选 playbook，不是缺省流程。

<!-- rule-id: TECH-030-AI-PROMPT-ARTIFACT-S02 -->
- 适用情形：启用客户数据进入 AI 前。客户数据进入 prompt/RAG/memory/tool action 前须有 data boundary。

### 异步任务、Webhook 与韧性

<!-- rule-id: TECH-241-ROUTE-RETRY-POLICY -->
- route retry 须定义上限、backoff 和错误分类。

<!-- rule-id: TECH-241-SIDE-EFFECT-TOOL-RETRY-DEFAULT -->
- 有副作用工具缺省禁止自动重试。

<!-- rule-id: TECH-241-AUTOMATIC-RETRY-ELIGIBILITY -->
- 自动 retry 仅用于无副作用、可幂等且属于瞬时错误的调用。

<!-- rule-id: TECH-241-NO-BLIND-SIDE-EFFECT-RETRY -->
- 模型 route 层禁止盲目重试工具调用、支付、写数据或发通知。

<!-- rule-id: TECH-241-RETRY-LIMIT-EXPANSION-HUMAN-GATE -->
- 扩大 retry 上限须交由人工判断。

<!-- rule-id: TECH-238-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：分析调用失败时且事件不是合规或计费事实。分析失败禁止阻断核心业务流程。

<!-- rule-id: TECH-240-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：工作涉及所列表面时。对外 claim、供应商数据流或高成本 AI workflow 须有降级路径。

<!-- rule-id: TECH-238-RETRY-FALLBACK-RESILIENCE-S02 -->
- 适用情形：调用外部分析 provider 时。分析 provider client须具备：timeout、retry、backoff、drop policy、本地 fallback。

<!-- rule-id: TECH-240-RETRY-FALLBACK-RESILIENCE-S02 -->
- 适用情形：设计 AI 成本容量时。重试须有上限。

<!-- rule-id: TECH-123-ASYNC-JOB-WORKER-S02 -->
- 适用情形：执行客户数据删除、导出或同步时。数据作业须具备：dry-run、幂等、audit、状态、例外解释。

<!-- rule-id: TECH-240-RETRY-FALLBACK-RESILIENCE-S03 -->
- 适用情形：调用供应商时。供应商调用须具备：timeout、retry budget。

<!-- rule-id: TECH-124-ASYNC-JOB-WORKER-S01 -->
- 适用情形：引入基础设施时。新增队列须由人工判断。

<!-- rule-id: TECH-124-ASYNC-JOB-WORKER-S02 -->
- 适用情形：引入基础设施时。新增事件 broker 须由人工判断。

<!-- rule-id: TECH-225-NOTIFICATION-MESSAGING-S01 -->
- 适用情形：引入外部供应商时。新增支付、通知或开发者平台供应商须由人工判断。

<!-- rule-id: TECH-242-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：决定 实现交接边界时。接受没有取消能力或重试上限的实现进入下一步须由人工判断。

<!-- rule-id: TECH-125-ASYNC-JOB-WORKER-S01 -->
- 适用情形：设计管理入口时。高风险不可逆 worker 可保留进程隔离。

<!-- rule-id: TECH-118-ASYNC-JOB-CONTRACT-S01 -->
- 适用情形：不使用 foreign key 时。无 foreign key 时应用层须实现幂等控制。

<!-- rule-id: TECH-226-NOTIFICATION-MESSAGING-S01 -->
- 适用情形：扩大服务架构时。引入异步消息、事件溯源或分布式事务须由人工判断。

<!-- rule-id: TECH-119-ASYNC-JOB-CONTRACT-S01 -->
- 适用情形：实现前端写操作时。写操作须至少使用 disabled 状态或幂等 key 之一防止重复提交。

<!-- rule-id: TECH-121-ASYNC-JOB-CONTRACT-S01 -->
- 适用情形：实现外部副作用时。所有外部副作用须有幂等。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S02 -->
- 适用情形：处理入站 Webhook 时。入站 Webhook 须先验签；入站 Webhook 须去重；入站 Webhook 须持久化 inbox；入站 Webhook 须快速 ack。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S03 -->
- 适用情形：产生出站事件时。出站事件须与业务状态同事务写 outbox。

<!-- rule-id: TECH-227-NOTIFICATION-MESSAGING-S01 -->
- 适用情形：构建用户消息时。邮件、SMS 和 push 禁止包含 secret、完整 AI/用户内容或敏感数据。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S04 -->
- 适用情形：处理 Webhook 时。Webhook 处理禁止依赖顺序。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S01 -->
- 适用情形：应用异步 job 专项时。与本规范的正式分类及项目原则冲突时，以正式规范为准。

<!-- rule-id: TECH-243-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：实现生产后台任务时。后台任务须有限重试。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S02 -->
- 适用情形：实现生产后台任务时。后台任务须幂等。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S03 -->
- 适用情形：登记高风险 job 时。高风险 job须具备：幂等键、人工 checkpoint。

<!-- rule-id: TECH-243-RETRY-FALLBACK-RESILIENCE-S03 -->
- 适用情形：登记高风险 job 时。高风险 job 须有重试上限。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S04 -->
- 适用情形：存储 job payload 时。payload 缺省只能保存 schema 化输入；payload 禁止保存 raw AI/tool 内容、secret 或未脱敏个人数据；payload 缺省只能保存最小化输入；payload 缺省只能保存可重放输入。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S05 -->
- 适用情形：存储 job result 时。job row 禁止保存大文件、敏感正文或供应商原始响应。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S06 -->
- 适用情形：实现副作用 job 时。外部副作用须使用 outbox、幂等、补偿或 AI tool gate。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S07 -->
- 适用情形：扩大异步架构时。引入新队列、引擎、调度、Batch 或后台供应商须由人工判断。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S08 -->
- 适用情形：改变 job 数据保留时。job payload/result 保留 raw 或敏感内容须由人工判断。

<!-- rule-id: TECH-243-RETRY-FALLBACK-RESILIENCE-S04 -->
- 适用情形：扩大 job 容量时。提高 job 并发、速率、重试、规模、预算或频率须由人工判断。

<!-- rule-id: TECH-128-ASYNC-JOB-WORKER-S01 -->
- 适用情形：决定是否采用该专项时。异步 job 与 worker 专项是可选 playbook，不是缺省流程。

<!-- rule-id: TECH-120-ASYNC-JOB-CONTRACT-S01 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时幂等控制须承担引用完整性。

<!-- rule-id: TECH-244-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：设计 retry 时。retry须具备：上限、backoff、retry budget。

<!-- rule-id: TECH-228-NOTIFICATION-MESSAGING-S01 -->
- 适用情形：决定是否外部通知时。普通文案更正可以不通知；若错误涉及数据、安全、隐私、SLA、计费、AI 能力或合同承诺，通知决定须接受人工审查。

## 按主题整理的执行细则

### 架构、模块与依赖边界

<!-- rule-id: TECH-002-ACTION-FRONTEND-SECURITY-BOUNDARY -->
- 隐藏路由、禁用按钮和前端角色判断都不构成后台动作的安全边界。

<!-- rule-id: TECH-089-PROTO-DEPENDENCY-LOCATION -->
- 服务目录中的 Proto 依赖缺省位于 `third_party/`。

<!-- rule-id: TECH-191-BACKEND-EVENT-CONSTRUCTION -->
- 后端 handler 禁止自由拼装生产业务事件。

<!-- rule-id: TECH-191-FRONTEND-EVENT-CORRELATION -->
- 适用时，前端事件须关联 release version、latency bucket 和 error class。

<!-- rule-id: TECH-201-GO-KRATOS-LAYERING -->
- `internal/service` 适配 transport 并调用 biz/usecase；`internal/biz` 持有领域规则、usecase 和 port interface。

<!-- rule-id: TECH-201-KRATOS-LAYOUT-DEFAULT -->
- 后端缺省采用 Kratos layout，不另造新的后端结构。

<!-- rule-id: TECH-201-GO-KRATOS-DEFAULT-DIRECTORIES -->
- Go/Kratos 缺省目录包含服务启动入口、`internal/conf`、`internal/biz`、`internal/data`、`internal/service`、`internal/server`、`internal/ai` 和 `internal/pkg`。

<!-- rule-id: TECH-105-ARCHITECTURE-BOUNDARY-S01 -->
- 适用情形：变更触发架构专项时。架构触发时补充 ADR、boundary、module map 和 dependency rules。

<!-- rule-id: TECH-113-ARCHITECTURE-DIAGRAM-DEPTH-S02 -->
- 适用情形：需要架构图时。架构图优先考虑 context/container 级别。

<!-- rule-id: TECH-113-ARCHITECTURE-DIAGRAM-DEPTH-S03 -->
- 适用情形：考虑详细架构图时。只在调试复杂边界时展开 component/code 级别。

<!-- rule-id: TECH-153-BACKEND-CODE-ARCHITECTURE-BOUNDARY-S01 -->
- 适用情形：组织 Go/Kratos 服务时。internal/data 实现 repository port 并掌握数据 adapter。

<!-- rule-id: TECH-195-FRONTEND-BOUNDARY-S01 -->
- 适用情形：组织 Vite 前端时。shared/ui 仅存放跨 feature 真实复用且稳定的 UI 原语。

<!-- rule-id: TECH-195-FRONTEND-BOUNDARY-S02 -->
- 适用情形：组织 Vite 前端时。shared/lib 仅存放无业务语义的纯函数。

<!-- rule-id: TECH-195-FRONTEND-BOUNDARY-S05 -->
- 适用情形：组织 Vite 前端设计系统时。设计 token 与决策纳入 design system 工件且不散落在 feature 中。

<!-- rule-id: TECH-106-ARCHITECTURE-BOUNDARY-S01 -->
- 适用情形：创建架构最小工件时。同一 target 的架构工件采用同一文件名。

<!-- rule-id: TECH-109-ARCHITECTURE-BOUNDARY-S03 -->
- 适用情形：change 触发架构专项时。最小架构工件纳入日期化 ADR。

<!-- rule-id: TECH-115-ARCHITECTURE-MINIMUM-ARTIFACTS-S01 -->
- 适用情形：change 触发架构专项时。最小架构工件纳入 target boundary JSON。

<!-- rule-id: TECH-115-ARCHITECTURE-MINIMUM-ARTIFACTS-S02 -->
- 适用情形：change 触发架构专项时。最小架构工件纳入 target module map。

<!-- rule-id: TECH-115-ARCHITECTURE-MINIMUM-ARTIFACTS-S03 -->
- 适用情形：change 触发架构专项时。最小架构工件纳入 target dependency rules。

<!-- rule-id: TECH-195-FRONTEND-BOUNDARY-S06 -->
- 适用情形：组织 Vite 前端时。Vite 缺省目录包含 web 根目录；Vite 缺省目录包含 index.html 入口；Vite 缺省目录包含 src；Vite 缺省目录包含 app；Vite 缺省目录包含 feature 目录；Vite 缺省目录包含 shared/ui；Vite 缺省目录包含 shared/lib；Vite 缺省目录包含 styles。

<!-- rule-id: TECH-109-ARCHITECTURE-BOUNDARY-S04 -->
- 适用情形：记录架构显著决策时。ADR须登记：Status、触发事实和约束、采用的决定、决定后果、至少一个被拒方案、复查日期。

<!-- rule-id: TECH-109-ARCHITECTURE-BOUNDARY-S05 -->
- 适用情形：记录架构显著决策时。替代旧决策时 ADR 须记录被替代 ADR。

<!-- rule-id: TECH-109-ARCHITECTURE-BOUNDARY-S06 -->
- 适用情形：创建 architecture boundary 时。boundary JSON须登记：target、owner、status、bounded_context、data ownership。

<!-- rule-id: TECH-104-ARCHITECTURE-BOUNDARY-SCHEMA-S01 -->
- 适用情形：创建 architecture boundary 时。boundary JSON须登记：modules、dependency direction、allowed dependencies、forbidden dependencies、external interfaces、source roots、ADR links、review cadence。

<!-- rule-id: TECH-106-ARCHITECTURE-BOUNDARY-S02 -->
- 适用情形：创建 architecture boundary 时。boundary JSON 须记录 AI boundaries。

<!-- rule-id: TECH-108-ARCHITECTURE-BOUNDARY-S01 -->
- 适用情形：创建 architecture boundary 时。boundary JSON 须记录 human checkpoint。

<!-- rule-id: TECH-116-ARCHITECTURE-MODULE-ENTRY-SCHEMA-S01 -->
- 适用情形：定义 boundary module 时。每个 module须登记：name、path、owns、may depend on、must not depend on。

<!-- rule-id: TECH-111-ARCHITECTURE-BOUNDARY-S01 -->
- 适用情形：定义 boundary module 时。每个 module 须记录 type，且 type 只能取 domain、usecase、service、data、transport、frontend_feature、ai_workflow、shared、config、cmd。

<!-- rule-id: TECH-117-ARCHITECTURE-MODULE-MAP-S01 -->
- 适用情形：创建 module map 时。module map须登记：Context、Containers、Modules、Dependency Direction、Operational Boundaries。

<!-- rule-id: TECH-109-ARCHITECTURE-BOUNDARY-S07 -->
- 适用情形：创建 module map 时。module map须登记：Data Ownership、Open Decisions。

<!-- rule-id: TECH-106-ARCHITECTURE-BOUNDARY-S03 -->
- 适用情形：创建 module map 时。module map 须记录 AI Boundaries。

<!-- rule-id: TECH-189-DEPENDENCY-RULES-ARTIFACT-S01 -->
- 适用情形：创建 dependency rules 工件时。dependency rules 工件须登记：target、source roots、rules、exceptions。

<!-- rule-id: TECH-108-ARCHITECTURE-BOUNDARY-S02 -->
- 适用情形：创建 dependency rules 工件时。dependency rules 工件须记录 human checkpoint。

<!-- rule-id: TECH-188-DEPENDENCY-RULE-SCHEMA-S01 -->
- 适用情形：定义 dependency rule 时。每条 dependency rule须登记：name、applies_to、forbidden imports、reason、severity。

<!-- rule-id: TECH-112-ARCHITECTURE-BOUNDARY-S01 -->
- 适用情形：change 涉及依赖或构建时。供应链专项须覆盖依赖扫描。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S01 -->
- 适用情形：创建新服务时。数据库缺省使用 MySQL。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S02 -->
- 适用情形：选择数据库时。项目须固定数据库版本。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S03 -->
- 适用情形：选择非 MySQL 数据库时。选择非默认数据库时须记录原因。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S04 -->
- 适用情形：编写 SQL 时。SQL 优先考虑采用 MySQL/PostgreSQL 通用语法。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S06 -->
- 适用情形：设计数据库 schema 时。缺省不创建 foreign key。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S07 -->
- 适用情形：配置 sqlc 时。sqlc.yaml 须使用 version 2；sqlc.yaml 须明确 engine；sqlc.yaml 须明确 schema；sqlc.yaml 须明确 queries；sqlc.yaml 须明确 gen.go.package；sqlc.yaml 须明确 gen.go.out。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S08 -->
- 适用情形：组织 sqlc query 时。查询文件须按聚合或 usecase 分组。

<!-- rule-id: TECH-208-GOVERNANCE-GO-KRATOS-SQLC-GRPC-SERVICE-S02 -->
- 适用情形：实现 repository 时。写操作须说明事务边界。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S10 -->
- 适用情形：确实需要动态 SQL 时。使用动态 SQL 时须记录在 design.md；使用动态 SQL 时须说明静态查询不足原因。

<!-- rule-id: TECH-196-FRONTEND-BOUNDARY-S01 -->
- 适用情形：设计前端状态时。缺省不引入全局状态库。

<!-- rule-id: TECH-196-FRONTEND-BOUNDARY-S02 -->
- 适用情形：设计前端组件时。缺省不引入大型 UI 组件库。

<!-- rule-id: TECH-254-SCHEMA-DATA-VITE-VERCEL-FRONTEND-S02 -->
- 适用情形：配置前端环境时。环境变量须在 vite-env.d.ts 或等价 schema 类型化。

<!-- rule-id: TECH-251-SCHEMA-DATA-GO-KRATOS-SQLC-GRPC-SERVICE-S11 -->
- 适用情形：偏离已确认的服务数据默认时。偏离已确认的 MySQL、sqlc、无 ORM、通用 SQL 或无 foreign key 默认时须登记：原因、影响。

### API、Protobuf 与错误契约

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

### 数据模型、sqlc 与迁移

<!-- rule-id: TECH-252-SCHEMA-DATA-PRODUCT-ANALYTICS-EXPERIMENT-S02 -->
- 适用情形：创建 tracking plan 时。schema policy须登记：命名规则、属性类型、低基数要求、版本策略、弃用方式。

<!-- rule-id: TECH-180-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：存储产品事件且该状态适用时。sqlc 表须区分：适用的 raw ingestion、适用的 schema violation、适用的 experiment assignment、适用的 exposure、适用的 suppression/deletion state。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S02 -->
- 适用情形：建立 AI artifact 时。结构化输出 schema 缺省位于 ai/schemas/<capability>.schema.json。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S04 -->
- 适用情形：输出为纯展示文本时。纯展示文本可在 design 中说明无需 schema。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S05 -->
- 适用情形：按默认顺序推进 AI change 时。需要结构化输出时须写 JSON Schema。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S06 -->
- 适用情形：设计结构化输出 schema 时。结构化输出 schema 须设置必要字段；结构化输出 schema 须设置 additionalProperties false。

<!-- rule-id: TECH-245-SCHEMA-DATA-AI-CONTEXT-MEMORY-RETRIEVAL-S01 -->
- 适用情形：触发上下文治理工件时。preference schema 缺省位于 ai-context/preference-schema/<capability>.json。

<!-- rule-id: TECH-245-SCHEMA-DATA-AI-CONTEXT-MEMORY-RETRIEVAL-S02 -->
- 适用情形：登记上下文来源时。source registry须登记：owner、scope、system of record、access check、license 或 rights、data classification、deletion policy。

<!-- rule-id: TECH-246-SCHEMA-DATA-AI-RUNTIME-ROUTING-TOOLS-S01 -->
- 适用情形：实现 AI workflow 时。结构化输出应优先考虑使用 schema。

<!-- rule-id: TECH-221-MIGRATION-BACKFILL-DATA-FIX-S01 -->
- 适用情形：实现数据访问时。schema 和 migration 须先于 query。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S01 -->
- 适用情形：选择数据存储时。缺省数据库为 MySQL。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S01 -->
- 适用情形：实施数据变更时。数据变更缺省使用 SQL migration 和 sqlc，不以 ORM 作为数据访问主路径。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S02 -->
- 适用情形：编写 SQL 时。缺省优先使用 MySQL/PostgreSQL 通用 SQL。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S03 -->
- 适用情形：使用数据库专有能力时。专有 SQL 须隔离；专有 SQL 须标注；专有 SQL 须提供替代路径或锁定理由之一。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S05 -->
- 适用情形：同步 schema/query/code 时。sqlc 同步第一步须写 migration 或 schema 变化。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S06 -->
- 适用情形：运行 sqlc vet 时。需要数据库连接的 vet rule 须先在临时库应用 migration。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S07 -->
- 适用情形：配置 sqlc 时。sqlc.yaml 须使用 version 2。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S04 -->
- 适用情形：编写 query 时。写操作须明确事务边界。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S09 -->
- 适用情形：编写 schema/query 时。使用数据库专有能力时须登记：engine lock-in、替代路径。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S10 -->
- 适用情形：执行生产迁移时。生产迁移 expand 阶段添加兼容 schema。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S12 -->
- 适用情形：新增个人数据字段时。新增个人数据字段须说明访问边界。

<!-- rule-id: TECH-248-SCHEMA-DATA-CONFIGURATION-FEATURE-FLAG-S01 -->
- 适用情形：编写配置注册表时。配置注册表须包含：target、owner、stack、secrets_policy、validation、startup_checks、reload_policy、drift_detection、human_checkpoint、review_cadence。

<!-- rule-id: TECH-248-SCHEMA-DATA-CONFIGURATION-FEATURE-FLAG-S02 -->
- 适用情形：登记 flag 时。每个 flag 须包含 owner。

<!-- rule-id: TECH-181-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：设计 sqlc 异步存储时。可按职责选建下列九张表，均非必需：
  - 类型与主记录：`async_job_types`、`async_jobs`。
  - 执行历史：`async_job_attempts`、`async_job_events`、`async_job_results`。
  - 失败与调度：`async_job_dead_letters`、`async_job_schedules`。
  - 取消与幂等：`async_job_cancellations`、`async_job_idempotency_keys`。

<!-- rule-id: TECH-217-JOB-CLAIM-SQL-PORTABILITY-S02 -->
- 适用情形：使用数据库专有 claim SQL 时。使用专有 claim SQL 时须登记：MySQL/PostgreSQL 差异、替代路径。

<!-- rule-id: TECH-224-MIGRATION-DESIGN-S01 -->
- 适用情形：使用自有应用模板时。批准自有模板后须记录迁移边界。

<!-- rule-id: TECH-182-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：需要持久化 UX 证据时。sqlc 允许按需包含 ux_feedback_events 表；sqlc 允许按需包含 ai_output_feedback 表；sqlc 允许按需包含 accessibility_exceptions 表；sqlc 允许按需包含 ui_incident_reports 表。

<!-- rule-id: TECH-183-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：需要持久化客户上线状态时。sqlc 允许按需选择包含 customer_launches 表；sqlc 允许按需选择包含 tenant_provisioning_events 表；sqlc 允许按需选择包含 tenant_entitlements 表；sqlc 允许按需选择包含 customer_readiness_gates 表；sqlc 允许按需选择包含 customer_success_reviews 表。

<!-- rule-id: TECH-184-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：需要持久化 claim control 时。sqlc 允许按需选择包含 external_claims 表；sqlc 允许按需选择包含 claim_surfaces 表；sqlc 允许按需选择包含 claim_evidence_links 表；sqlc 允许按需选择包含 claim_release_gates 表；sqlc 允许按需选择包含 claim_correction_events 表；sqlc 允许按需选择包含 claim_reviews 表。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`admin_actions` 表缺省存在。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S02 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`admin_action_runs` 表缺省存在。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S03 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`admin_approvals` 表缺省存在。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S04 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`audit_events` 表缺省存在。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S05 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`break_glass_sessions` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_cases` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S02 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_events` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S03 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_feedback_links` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S04 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_template_versions` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S05 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_review_items` 表缺省存在。

<!-- rule-id: TECH-187-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。sqlc 允许按需选择表：`ai_quality_signals`、`ai_quality_incidents`、`ai_quality_actions`、`ai_quality_reviews`。

### 认证授权、安全、凭据与审计

<!-- rule-id: TECH-002-ACTION-REGISTRY-TOP-LEVEL-SCHEMA -->
- `admin-ops/action-registry/<target>.json` 的顶层须具备 13 个字段：`target`、`owner`、`actions`、`risk_levels`、`permission_model`、`approval_policy`、`dry_run_policy`、`rollback_policy`、`rate_limits`、`observability`、`ai_autonomy`、`human_checkpoint`、`review_cadence`。

<!-- rule-id: TECH-002-ACTION-REGISTRY-ACTION-ITEM-SCHEMA -->
- `admin-ops/action-registry/<target>.json` 的每个 `actions[]` 元素须具备 14 个字段：`id`、`name`、`category`、`scope`、`risk_level`、`actor`、`authorization`、`input_schema`、`prechecks`、`dry_run`、`execution_path`、`rollback`、`audit_event`、`status`。

<!-- rule-id: TECH-002-ACTION-UI-DATA-MINIMIZATION -->
- 后台页面禁止展示完成当前任务不需要的个人数据、secret、完整 prompt/response 或支付敏感信息。

<!-- rule-id: TECH-151-SECURITY-THREAT-SCOPE -->
- 威胁范围须纳入 prompt injection 引起的数据或动作风险、RAG 泄露、AI 工具越权、供应链漏洞、日志/trace 泄露、个人数据泄露、租户隔离失败、权限绕过、密钥泄露、疑似入侵和安全漏洞。

<!-- rule-id: TECH-204-CREDENTIAL-ACCESS-POLICY-MINIMUM-ARTIFACT -->
- 凭据治理的最小工件须包含 `access-policy/<target>.md`。

<!-- rule-id: TECH-152-VITE-SECRET-AUTH-BOUNDARY -->
- 通过 `VITE_` 暴露的值禁止是 secret，也不可作为后端授权依据。

<!-- rule-id: TECH-256-SECURITY-PRIVACY-ARTIFACT-TRIGGERS -->
- 触发安全隐私专项时，须补充威胁、隐私、供应链和 secret 工件。

<!-- rule-id: TECH-134-AUTH-ENFORCEMENT-LAYERS -->
- Go/Kratos 的认证与 context 注入落在 middleware，授权裁决落在 biz/usecase。

<!-- rule-id: TECH-134-HIGH-IMPACT-AUTH-ARTIFACT-LINK -->
- 高影响 OpenSpec change 须链接安全/Auth 工件，或写明不适用原因。

<!-- rule-id: TECH-134-AUTH-IDENTITY-BOUNDARY-ARTIFACT -->
- change 涉及 Auth 时，最小工件须包含 `identity boundary`。

<!-- rule-id: TECH-134-AUTHORIZATION-POLICY-TEST-ARTIFACTS -->
- change 涉及授权时，最小工件须包含 `policy matrix` 和 `authorization tests`；测试执行证据由验证项目负责。

<!-- rule-id: TECH-134-HIGH-PRIVILEGE-AUDIT-NOTES -->
- Auth change 涉及高权限访问时，最小工件须包含 `audit notes`。

<!-- rule-id: TECH-134-AUTH-COVERAGE -->
- Auth 专项须把五类约束纳入覆盖范围：缺省拒绝、角色/资源/action、tenant context、session/token 和身份来源。

<!-- rule-id: TECH-134-SUPPLY-CHAIN-CI-MINIMUM-PERMISSION -->
- 涉及依赖或构建时，供应链专项须覆盖 CI 最小权限。

<!-- rule-id: TECH-130-AUDIT-LOG-TOP-LEVEL-SCHEMA -->
- `admin-ops/audit-log-schema/<target>.json` 顶层须具备 `target`、`owner`、`event_name`、`required_fields`、`sensitive_fields`、`retention`、`storage`、`integrity`、`alerts`、`query_examples` 和 `human_checkpoint`。

<!-- rule-id: TECH-130-AUDIT-LOG-REQUIRED-FIELDS -->
- `admin-ops/audit-log-schema/<target>.json` 的 `required_fields` 集合须纳入 `event_id`、`timestamp`、`actor_id`、`actor_type`、`tenant_id`、`action_id`、`action_version`、`reason`、`linked_artifact`、`request_id`、`dry_run`、`approval_id`、`target_resource`、`before_ref`、`after_ref`、`status` 和 `error_class`。

<!-- rule-id: TECH-130-AUDIT-LOG-SENSITIVE-ASSET -->
- audit log 本身属于敏感资产，对它的访问也须被记录。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S01 -->
- 适用情形：采集产品行为数据前。privacy review 用于说明产品行为数据为何可以采集。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S02 -->
- 适用情形：创建 privacy review 时。privacy review 登记 scope。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S03 -->
- 适用情形：创建 privacy review 时。privacy review 登记 purpose。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S04 -->
- 适用情形：创建 privacy review 时。privacy review 登记 data classes。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S05 -->
- 适用情形：创建 privacy review 时。privacy review 登记 personal data。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S06 -->
- 适用情形：创建 privacy review 时。privacy review 登记 third-party analytics。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S07 -->
- 适用情形：创建 privacy review 时。privacy review 登记 consent 或 notice。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S08 -->
- 适用情形：创建 privacy review 时。privacy review 登记 retention。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S09 -->
- 适用情形：创建 privacy review 时。privacy review 登记 deletion 和 export。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S10 -->
- 适用情形：创建 privacy review 时。privacy review 登记 AI data boundary。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S11 -->
- 适用情形：创建 privacy review 时。privacy review 登记 session replay 或 recording。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S12 -->
- 适用情形：创建 privacy review 时。privacy review 登记 access control。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S13 -->
- 适用情形：创建 privacy review 时。privacy review 登记 open risks。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S14 -->
- 适用情形：创建 privacy review 时。privacy review 登记 review cadence。

<!-- rule-id: TECH-133-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：评估 semantic compatibility 时。semantic compatibility 要求业务、错误、权限与重试语义不被静默改变。

<!-- rule-id: TECH-257-SECURITY-PRIVACY-S01 -->
- 适用情形：change 处理数据时。最小安全工件纳入 privacy record。

<!-- rule-id: TECH-257-SECURITY-PRIVACY-S02 -->
- 适用情形：change 涉及依赖或构建时。最小安全工件纳入 supply-chain record。

<!-- rule-id: TECH-257-SECURITY-PRIVACY-S03 -->
- 适用情形：change 处理 secret 时。最小安全工件纳入 secrets record。

<!-- rule-id: TECH-255-SECURITY-PRIVACY-S17 -->
- 适用情形：定义 tracking plan 事件时。每个事件须记录隐私等级。

<!-- rule-id: TECH-055-AI-TOOL-PERMISSION-S02 -->
- 适用情形：采集 AI 产品事件时。AI 产品事件缺省记录 tool_names。

<!-- rule-id: TECH-053-AI-TOOL-PERMISSION-S01 -->
- 适用情形：定义 AI tool port 时。tool port 须明确输入 schema；tool port 须明确成本限制；tool port 须明确dry-run；tool port 须明确审批要求；tool port 须明确审计日志。

<!-- rule-id: TECH-132-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：定义 AI tool port 时。tool port 须明确权限；tool port 须明确tenant。

<!-- rule-id: TECH-054-AI-TOOL-PERMISSION-S01 -->
- 适用情形：创建 surface map 时。surface map 须记录 AI tool schemas。

<!-- rule-id: TECH-257-SECURITY-PRIVACY-S04 -->
- 适用情形：change 触发安全专项时。安全专项须覆盖信任边界；安全专项须覆盖滥用场景；安全专项须覆盖控制；安全专项须覆盖未决风险。

<!-- rule-id: TECH-257-SECURITY-PRIVACY-S05 -->
- 适用情形：change 处理数据时。安全专项须覆盖数据分类；安全专项须覆盖处理目的；安全专项须覆盖外部处理方；安全专项须覆盖保留；安全专项须覆盖日志；安全专项须覆盖删除/导出；安全专项须覆盖AI 数据使用。

<!-- rule-id: TECH-257-SECURITY-PRIVACY-S06 -->
- 适用情形：change 涉及依赖或构建时。供应链专项须覆盖secret scanning。

<!-- rule-id: TECH-058-AI-TOOL-PERMISSION-S01 -->
- 适用情形：需要 AI 工具治理时。触发工具运行时治理时补充 ai-tools 工件。

<!-- rule-id: TECH-049-AI-TOOL-CONTRACT-AUDITABILITY-S01 -->
- 适用情形：定义 AI 工具调用时。工具调用缺省使用显式参数；工具调用缺省使用结构化返回；工具调用缺省记录可审计日志。

<!-- rule-id: TECH-260-SECURITY-PRIVACY-S01 -->
- 适用情形：执行最小安全下一步时。每个默认注入的上下文须写清来源；每个默认注入的上下文须写清删除路径。

<!-- rule-id: TECH-137-AUTH-TENANT-PERMISSION-S05 -->
- 适用情形：执行最小安全下一步时。每个默认注入的上下文须写清权限。

<!-- rule-id: TECH-138-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：生产 AI capability 建立 runtime 工件时。permission policy 缺省位于 ai-runtime/permission-policy/<capability>.md。

<!-- rule-id: TECH-138-AUTH-TENANT-PERMISSION-S02 -->
- 适用情形：编写 permission policy 时。permission policy须包含：Scope、Actors、Allowed/Forbidden Actions、Approval Policy、Tenant Boundary、Data Boundary、Connector/MCP Policy、Tool Output Handling、Secrets、Audit、Linked Artifacts。

<!-- rule-id: TECH-139-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：判断 AI 工具权限时。服务端权限判断须使用 actor；服务端权限判断须使用 tenant；服务端权限判断须使用 capability；服务端权限判断须使用 tool id；服务端权限判断须使用 scope；服务端权限判断须使用 risk；服务端权限判断须使用 approval id；服务端权限判断须使用 data boundary。

<!-- rule-id: TECH-138-AUTH-TENANT-PERMISSION-S03 -->
- 适用情形：实现工具路由时。工具路由须与 auth 相连；工具路由须与 tenant boundary 相连。

<!-- rule-id: TECH-001-ADMIN-ACTION-CONTROL-S01 -->
- 适用情形：实现工具路由时。工具路由须与 admin action guard 相连。

<!-- rule-id: TECH-142-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：设计管理入口时。同类高权限一次性操作优先考虑合并为统一管理 CLI。

<!-- rule-id: TECH-263-SECURITY-PRIVACY-S01 -->
- 适用情形：执行最小安全下一步时。每个外部副作用须追溯到 event id。

<!-- rule-id: TECH-147-AUTH-TENANT-PERMISSION-S01 -->
- 适用情形：设计 release pipeline schema 时。pipeline.ci 建议包含 permissions。

<!-- rule-id: TECH-061-AI-TOOL-PERMISSION-S01 -->
- 适用情形：定义试点 AI 边界时。AI Boundary 须说明客户数据是否用于tool action。

<!-- rule-id: TECH-148-AUTH-TENANT-PERMISSION-S04 -->
- 适用情形：创建客户租户前。建租户前须完成 tenant provisioning。

<!-- rule-id: TECH-176-CREDENTIAL-ACCESS-POLICY-S01 -->
- 适用情形：编写凭据 access-policy 时。access-policy需要明确：谁或哪个 workload 能读取凭据、凭据在哪里注入、凭据绝不允许出现的位置。

<!-- rule-id: TECH-267-SECURITY-PRIVACY-S01 -->
- 适用情形：实现或维护“AI workflow 默认规则”时。对可能违反 OpenAI 采用政策或产品安全边界的请求，使用 moderation/safety check、账户级 safety identifier 或等价机制帮助定位和处理。

### 配置、成本、供应商与其他技术边界

<!-- rule-id: TECH-150-HIGH-PRIVILEGE-INSTRUCTION-BOUNDARY -->
- 用户输入、客服消息或网页内容禁止直接拼入高优先级 developer/system 指令后再调用高权限工具。

<!-- rule-id: TECH-100-KEY-ROTATION-OLD-VERSION-REVOCATION -->
- 轮换 JWT signing key、Webhook signing secret 或 encryption key 时，方案须说明旧版本如何撤销。

<!-- rule-id: TECH-193-EXTERNAL-CLAIM-EVIDENCE-REFERENCE -->
- 对外 claim 在发布时须带有 evidence ref。

<!-- rule-id: TECH-079-CONTRACT-ARTIFACT-FILE-NAMING -->
- 同一 target 的契约工件采用同一文件名。

<!-- rule-id: TECH-079-COMPATIBILITY-POLICY-MINIMUM-ARTIFACT -->
- 契约专项的最小工件须包含 compatibility policy。

<!-- rule-id: TECH-089-API-REQUEST-CONSTRAINTS -->
- API 请求字段须表达必填、长度、范围、分页、排序和 filter 允许范围。

<!-- rule-id: TECH-089-API-ERROR-CATEGORIES -->
- API error model 须区分业务、参数、权限、依赖和内部错误。

<!-- rule-id: TECH-134-BROWSER-LOGIN-DEFAULT -->
- 浏览器登录缺省优先托管 IdP/OIDC。

<!-- rule-id: TECH-191-TRACKING-PLAN-BOUNDARY -->
- tracking plan 用于界定允许采集的事件与禁止进入事件的属性；`sources` 只可从 `frontend`、`backend`、`worker`、`ai_workflow`、`webhook` 中选择适用来源。

<!-- rule-id: TECH-191-BUSINESS-OUTCOME-EMISSION -->
- 业务 outcome 事件优先考虑在事务成功后或 outbox 中产生。

<!-- rule-id: TECH-191-TYPED-ANALYTICS-CLIENT -->
- 前端仅通过一个 typed analytics client 发送产品事件。

<!-- rule-id: TECH-191-TRACKING-PLAN-EVENT-SCHEMA -->
- tracking plan 中的每个事件须登记名称、触发条件、来源、用途、属性、保留期和状态。

<!-- rule-id: TECH-201-GO-PKG-DEFAULT -->
- Go 包布局缺省不使用 `pkg`。

<!-- rule-id: TECH-201-VITE-FEATURE-COLOCATION -->
- Vite feature 内部 co-locate 组件、hook、测试、adapter 和类型；测试执行与证据仍归验证项目。

<!-- rule-id: TECH-203-CUSTOMER-DATA-MAP-ARTIFACT -->
- change 处理客户数据时，最小工件须包含 `data map`。

<!-- rule-id: TECH-203-CUSTOMER-DATA-RIGHTS-DELETION-ARTIFACT -->
- change 处理客户数据权利时，最小工件须包含 `rights/deletion policy`。

<!-- rule-id: TECH-203-IP-SOURCE-REGISTER-ARTIFACT -->
- IP 专项处理外部或生成内容时，最小工件须包含 `source register`。

<!-- rule-id: TECH-203-IP-LICENSE-POLICY-ARTIFACT -->
- IP 专项处理第三方内容时，最小工件须包含 `license policy`。

<!-- rule-id: TECH-203-IP-NOTICE-ATTRIBUTION-ARTIFACT -->
- IP 专项处理需 attribution 内容时，最小工件须包含 `notice/attribution`。

<!-- rule-id: TECH-203-TRUST-COMMITMENT-REGISTER-ARTIFACT -->
- change 涉及用户承诺时，信任专项最小工件须包含 `commitment register`。

<!-- rule-id: TECH-203-TRUST-DATA-RIGHTS-ARTIFACT -->
- change 涉及用户数据权利时，信任专项最小工件须包含 `data rights` 文档。

<!-- rule-id: TECH-203-CUSTOMER-DATA-RECORD-FIELDS -->
- 客户数据记录须说明第三方传播、删除如何传播、导入与导出的格式，以及作为权威来源的 system of record。

<!-- rule-id: TECH-203-CONTENT-PROVENANCE-FIELDS -->
- 外部或生成内容须具有来源、license/rights basis 和 NOTICE/attribution。

<!-- rule-id: TECH-241-ROUTE-POLICY-RESILIENCE-FIELDS -->
- route policy 须包含 `Fallback/Degradation` 与 `Timeouts/Retries`。

<!-- rule-id: TECH-076-STABLE-EVENT-ENVELOPE-SCHEMA -->
- 稳定事件 envelope 须按 schema_version、properties、variant、experiment_id、trace_id、request_id、tenant_scope、actor_scope、source、occurred_at、event_name 的顺序完整表达这些字段。

<!-- rule-id: TECH-214-GOVERNANCE-PRODUCT-ANALYTICS-EXPERIMENT-S01 -->
- 适用情形：创建 tracking plan 时。tracking plan 登记人工 checkpoint。

<!-- rule-id: TECH-214-GOVERNANCE-PRODUCT-ANALYTICS-EXPERIMENT-S02 -->
- 适用情形：创建 tracking plan 时。tracking plan 登记 review cadence。

<!-- rule-id: TECH-214-GOVERNANCE-PRODUCT-ANALYTICS-EXPERIMENT-S03 -->
- 适用情形：创建 tracking plan 时。tracking plan 登记状态。

<!-- rule-id: TECH-173-COST-VENDOR-S02 -->
- 适用情形：前端发送产品事件时。组件中禁止散落 vendor SDK 调用。

<!-- rule-id: TECH-168-CONFIG-FLAGS-S01 -->
- 适用情形：配置前端分析时。VITE_* 仅存放公开可暴露配置。

<!-- rule-id: TECH-209-GOVERNANCE-MAIN-S04 -->
- 适用情形：存在实现前必须锁定的决策时。design 只记录实现前须锁定的高影响决策。

<!-- rule-id: TECH-209-GOVERNANCE-MAIN-S05 -->
- 适用情形：变更触发客户数据专项时。客户数据触发时补充数据地图、传输、同步和权利删除工件。

<!-- rule-id: TECH-209-GOVERNANCE-MAIN-S06 -->
- 适用情形：变更触发信任承诺专项时。信任承诺触发时补充承诺、政策表面、AI disclosure 和数据权利工件。

<!-- rule-id: TECH-169-CONFIG-FLAGS-S01 -->
- 适用情形：组织 Go/Kratos 服务时。cmd 仅负责启动、配置、wire 和 shutdown。

<!-- rule-id: TECH-229-OBSERVABILITY-SLO-ALERT-S01 -->
- 适用情形：组织 Go/Kratos 服务时。internal/server 组装 server、middleware、health 和 observability。

<!-- rule-id: TECH-197-GOVERNANCE-S01 -->
- 适用情形：组织 Vite 前端时。feature 间通过明确公共边界交互。

<!-- rule-id: TECH-163-CONFIG-FLAG-RUNTIME-ROUTING-S01 -->
- 适用情形：组织 Go/Kratos 服务时。Go/Kratos 缺省目录包含 configs。

<!-- rule-id: TECH-174-COST-VENDOR-S04 -->
- 适用情形：change 触发成本风险时。成本专项最小工件纳入 budget。

<!-- rule-id: TECH-174-COST-VENDOR-S05 -->
- 适用情形：change 触发成本风险时。成本专项最小工件纳入 vendor boundary。

<!-- rule-id: TECH-214-GOVERNANCE-PRODUCT-ANALYTICS-EXPERIMENT-S07 -->
- 适用情形：创建 tracking plan 时。tracking plan须登记：target、owner、product_area。

<!-- rule-id: TECH-214-GOVERNANCE-PRODUCT-ANALYTICS-EXPERIMENT-S08 -->
- 适用情形：分析必须使用 user identifier 时。用户标识须登记：用途、保留期、删除路径。

<!-- rule-id: TECH-162-CONFIG-FLAG-RUNTIME-ROUTING-S01 -->
- 适用情形：采集前端事件且该关联项适用时。前端事件须关联适用的 feature flag variant。

<!-- rule-id: TECH-173-COST-VENDOR-S03 -->
- 适用情形：采集 AI 产品事件时。AI 产品事件缺省记录 cost_bucket。

<!-- rule-id: TECH-232-PLANNING-GOVERNANCE-ROUTING-S01 -->
- 适用情形：change 涉及依赖或构建时。供应链专项须覆盖SBOM/provenance 计划。

<!-- rule-id: TECH-154-BACKUP-RESTORE-RECOVERY-S01 -->
- 适用情形：处理客户数据时。客户数据须记录备份例外。

<!-- rule-id: TECH-174-COST-VENDOR-S11 -->
- 适用情形：定义成本预算时。cost budget须登记：50% 阈值、80% 阈值、100% 阈值、hard cap、degradation。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S02 -->
- 适用情形：设计 AI route 时。分类任务须有适配 route。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S03 -->
- 适用情形：设计 AI route 时。结构化抽取任务须有适配 route。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S04 -->
- 适用情形：设计 AI route 时。摘要任务须有适配 route。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S05 -->
- 适用情形：设计 AI route 时。代码或推理任务须有适配 route。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S06 -->
- 适用情形：设计 AI route 时。长上下文任务须有适配 route。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S07 -->
- 适用情形：设计 AI route 时。工具代理任务须有适配 route。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S08 -->
- 适用情形：设计 AI route 时。低延迟聊天任务须有适配 route。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S09 -->
- 适用情形：设计 AI route 时。后台批处理任务须有适配 route。

<!-- rule-id: TECH-164-CONFIG-FLAG-RUNTIME-ROUTING-S11 -->
- 适用情形：选择后台 AI route 时。后台、低优先级或大批量任务优先 Batch、Flex 或异步队列。

<!-- rule-id: TECH-268-STRUCTURED-LOG-FIELD-CONTRACT-S01 -->
- 适用情形：创建新服务时。结构化日志须包含：service、version、env、request_id、trace_id、关键业务 id。

<!-- rule-id: TECH-166-CONFIG-FLAG-RUNTIME-ROUTING-S01 -->
- 适用情形：建立前端目录时。Vite 配置缺省位于 vite.config.ts。

<!-- rule-id: TECH-166-CONFIG-FLAG-RUNTIME-ROUTING-S02 -->
- 适用情形：建立前端目录时。TypeScript 配置缺省位于 tsconfig.json。

<!-- rule-id: TECH-235-PLANNING-GOVERNANCE-ROUTING-S01 -->
- 适用情形：使用动态 SQL 时。动态 SQL 须在 OpenSpec design.md 说明原因。

<!-- rule-id: TECH-167-CONFIG-FLAG-RUNTIME-ROUTING-S02 -->
- 适用情形：建立配置工件时。配置注册表缺省位于 config/registry/<target>.json。

<!-- rule-id: TECH-167-CONFIG-FLAG-RUNTIME-ROUTING-S03 -->
- 适用情形：编写配置注册表时。配置注册表须包含 config_items。

<!-- rule-id: TECH-167-CONFIG-FLAG-RUNTIME-ROUTING-S04 -->
- 适用情形：登记配置项时。每个 config item须包含：key、type、owner、source、required、default、validation、sensitive、client_exposed、restart_required、rollback。

<!-- rule-id: TECH-167-CONFIG-FLAG-RUNTIME-ROUTING-S06 -->
- 适用情形：编写 flag 清单时。Feature Flag 清单须包含 owner。

<!-- rule-id: TECH-270-USER-CONTROL-S01 -->
- 适用情形：执行最小安全下一步时。每个外部副作用须追溯到回放或撤销策略。

<!-- rule-id: TECH-236-PLANNING-GOVERNANCE-ROUTING-S01 -->
- 适用情形：维护 surface map 时。surface map 须包含 Critical Tasks。

<!-- rule-id: TECH-205-GOVERNANCE-CUSTOMER-PILOT-ONBOARDING-LAUNCH-S01 -->
- 适用情形：维护 pilot charter 时。pilot charter须包含：Data Boundary、AI Boundary、Integration Boundary。

<!-- rule-id: TECH-205-GOVERNANCE-CUSTOMER-PILOT-ONBOARDING-LAUNCH-S02 -->
- 适用情形：定义试点数据边界时。Data Boundary 须说明是否接触真实客户数据；Data Boundary 须说明是否接触个人数据；Data Boundary 须说明是否接触导入数据；Data Boundary 须说明是否接触日志；Data Boundary 须说明是否接触附件。

<!-- rule-id: TECH-205-GOVERNANCE-CUSTOMER-PILOT-ONBOARDING-LAUNCH-S03 -->
- 适用情形：定义试点 AI 边界时。AI Boundary 须说明客户数据是否用于人工审核；AI Boundary 须说明客户数据是否用于日志。

<!-- rule-id: TECH-205-GOVERNANCE-CUSTOMER-PILOT-ONBOARDING-LAUNCH-S04 -->
- 适用情形：维护 integrations[] 时。integrations[] 须包含 data_boundary。

<!-- rule-id: TECH-160-BILLING-ENTITLEMENT-PRICING-S01 -->
- 适用情形：维护 billing 时。billing 须包含 invoice/payment boundary。

<!-- rule-id: TECH-205-GOVERNANCE-CUSTOMER-PILOT-ONBOARDING-LAUNCH-S05 -->
- 适用情形：维护 ai_settings 时。ai_settings 须包含 provider data boundary。

<!-- rule-id: TECH-220-LIVE-INCIDENT-RESPONSE-S01 -->
- 适用情形：涉及范围时。通用可用性、延迟或容量事故须进入 运行项目 SRE-lite、技术设计成本容量、运行项目观测性和 AI 模型路由专项。

<!-- rule-id: TECH-220-LIVE-INCIDENT-RESPONSE-S02 -->
- 适用情形：创建或维护 ai-quality incident log 时。AI 质量事故日志禁止保存原始 prompt/response、客户数据、secret、完整日志或受监管内容。

### AI runtime、模型、上下文与工具

<!-- rule-id: TECH-102-AI-QUALITY-ERROR-CATEGORIES -->
- AI quality 的 gRPC status/error model 须分别表达 `temporarily degraded`、`fallback active`、`safety block`、`retrieval miss`、`tool failure`、`schema/parse failure` 与质量退化。

<!-- rule-id: TECH-086-PROMPT-INPUT-OUTPUT-CONTRACT -->
- 按默认顺序编写 prompt 时，`prompt.md` 须同时写明输入契约和输出契约。

<!-- rule-id: TECH-215-SUPPLY-CHAIN-LOCKFILE-COVERAGE -->
- 涉及依赖或构建时，供应链专项须覆盖 lockfile。

<!-- rule-id: TECH-079-AI-CONTRACT-SCHEMA-TRIGGER -->
- 仅当 target 含 AI tool、structured output 或 agent tool contract 时，须形成 `ai-tool-schemas`。

<!-- rule-id: TECH-079-AI-CONTRACT-MINIMUM-ARTIFACT -->
- target 含 AI 契约时，其最小工件须包含 AI tool schemas。

<!-- rule-id: TECH-079-AI-CONTRACT-SCHEMA -->
- AI contract（包括 AI tool 或 structured output）须登记 `target`、`owner`、`schemas`、`compatibility policy`、`rollback` 和 `human checkpoint`。

<!-- rule-id: TECH-191-AI-PRODUCT-EVENT-DEFAULTS -->
- AI 产品事件缺省记录 workflow、latency_bucket、token_bucket、result_class、safety_action 和 human_correction_required。

<!-- rule-id: TECH-241-MODEL-ROUTE-RESILIENCE-FIELDS -->
- 每条 model route 至少登记 timeout、retry 和 fallback chain。

<!-- rule-id: TECH-027-PROMPT-BUILDER-PLACEMENT -->
- prompt builder 的技术位置靠近所属 feature。

<!-- rule-id: TECH-006-AI-EVAL-FIXTURE-S01 -->
- 适用情形：组织 AI 服务代码时。internal/ai 存放 prompt、tool port、workflow 和 eval fixtures。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S04 -->
- 适用情形：组织 AI 依赖时。AI model/vendor SDK 仅在 adapter 或 workflow boundary 使用。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S06 -->
- 适用情形：组织前端时。缺省按 feature/route 组织 Vite 前端且不过度技术分层。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S02 -->
- 适用情形：调用供应商时。供应商调用收口到 client boundary。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S07 -->
- 适用情形：组织 Vite 前端时。Vite 缺省目录包含 routes。

<!-- rule-id: TECH-016-AI-MODEL-ROUTING-S01 -->
- 适用情形：change 触发安全专项时。最小安全工件纳入 threat model。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S04 -->
- 适用情形：change 引入数据处理方时。供应商专项最小工件纳入 processor register。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S05 -->
- 适用情形：change 引入数据处理方时。供应商专项最小工件纳入 DPA checklist。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S06 -->
- 适用情形：change 涉及数据出境时。供应商专项最小工件纳入 transfer impact。

<!-- rule-id: TECH-013-AI-MODEL-ROUTING-S01 -->
- 适用情形：采集前端事件且该关联项适用时。前端事件须关联适用的 route pattern。

<!-- rule-id: TECH-026-AI-PROMPT-ARTIFACT-S02 -->
- 适用情形：采集 AI 产品事件时。AI 产品事件缺省记录 prompt_version。

<!-- rule-id: TECH-013-AI-MODEL-ROUTING-S02 -->
- 适用情形：采集 AI 产品事件时。AI 产品事件缺省记录 model_route。

<!-- rule-id: TECH-016-AI-MODEL-ROUTING-S02 -->
- 适用情形：change 触发安全专项时。安全专项须覆盖资产；安全专项须覆盖入口。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S08 -->
- 适用情形：引入新供应商时。新供应商须登记：role、purpose、data classes、DPA/terms、retention、region、training/use 政策、删除协助。

<!-- rule-id: TECH-018-AI-MODEL-ROUTING-S02 -->
- 适用情形：需要模型路由治理时。触发模型路由或供应商治理时补充 ai-routing 工件。

<!-- rule-id: TECH-032-AI-PROMPT-DEGRADATION-STRATEGY-S01 -->
- 适用情形：编写 prompt.md 时。prompt.md 须记录降级策略。

<!-- rule-id: TECH-034-AI-PROMPT-SAFETY-BOUNDARY-S01 -->
- 适用情形：按默认顺序编写 prompt 时。prompt.md 须包含安全边界。

<!-- rule-id: TECH-065-AI-TRACE-LOG-CONTRACT-S01 -->
- 适用情形：记录 AI 调用证据时。trace/log须登记：prompt 版本、model、case id、latency、token、cost、tool calls、结果。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S04 -->
- 适用情形：定义 AI 工具时。工具参数应尽量结构化。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S02 -->
- 适用情形：触发上下文治理工件时。memory policy 缺省位于 ai-context/memory-policy/<capability>.md。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S01 -->
- 适用情形：触发上下文治理工件时。source registry 缺省位于 ai-context/source-registry/<capability>.json。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S02 -->
- 适用情形：触发上下文治理工件时。context review 缺省位于 ai-context/context-review/<capability>.md。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S03 -->
- 适用情形：定义 memory policy 时。memory type 须覆盖 session；memory type 须覆盖 saved preference；memory type 须覆盖 inferred preference；memory type 须覆盖 retrieved knowledge；memory type 须覆盖 support summary；memory type 须覆盖 safety context。

<!-- rule-id: TECH-029-AI-PROMPT-ARTIFACT-S02 -->
- 适用情形：构建 AI prompt 时。Prompt builder 须分区 system/developer 指令；Prompt builder 须分区用户输入；Prompt builder 须分区 memory；Prompt builder 须分区 RAG context；Prompt builder 须分区 tool output。

<!-- rule-id: TECH-041-AI-RUNTIME-GOVERNANCE-LINK-S01 -->
- 适用情形：处理成本、供应商或客户数据时。AI runtime 约束须链接 技术设计整体边界。

<!-- rule-id: TECH-040-AI-ROUTE-POLICY-ARTIFACT-S01 -->
- 适用情形：生产 AI capability 建立 runtime 工件时。route policy 缺省位于 ai-runtime/route-policy/<capability>.md。

<!-- rule-id: TECH-011-AI-MODEL-REGISTRY-S01 -->
- 适用情形：生产 AI capability 建立 runtime 工件时。model registry 缺省位于 ai-runtime/model-registry/<capability>.json。

<!-- rule-id: TECH-045-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：生产 AI capability 建立 runtime 工件时。tool registry 缺省位于 ai-runtime/tool-registry/<capability>.json。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S03 -->
- 适用情形：生产 AI capability 建立 runtime 工件时。runtime review 缺省位于 ai-runtime/runtime-review/<capability>.md。

<!-- rule-id: TECH-040-AI-ROUTE-POLICY-ARTIFACT-S02 -->
- 适用情形：编写 route policy 时。route policy须包含：Scope、Decision Matrix、Default Model Route、Tool/Connector Routes、Cost/Latency、Data Boundary、Safety/Privacy、Human Checkpoints、Linked Artifacts。

<!-- rule-id: TECH-025-AI-PRODUCTION-ROUTE-RECORD-S01 -->
- 适用情形：定义生产 route 时。生产 route须登记：模型族、route id、回滚路线。

<!-- rule-id: TECH-011-AI-MODEL-REGISTRY-S02 -->
- 适用情形：编写 model registry 时。model registry须包含：capability、owner、providers、routes、default_route、budgets、safety_gate、human_checkpoint、review_cadence。

<!-- rule-id: TECH-012-AI-MODEL-ROUTE-CONTRACT-S01 -->
- 适用情形：登记 model route 时。每条 route至少登记：模型、供应商、数据边界、max token、reasoning capability、tool capability、cost tier、latency target、safety refs、状态。

<!-- rule-id: TECH-035-AI-PROVIDER-CALL-TELEMETRY-S01 -->
- 适用情形：调用模型供应商时。provider 调用须登记：route id、provider、model、workflow version、eval version、latency、token、cost bucket、fallback reason。

<!-- rule-id: TECH-062-AI-TOOL-REGISTRY-SCHEMA-S01 -->
- 适用情形：编写 tool registry 时。tool registry须包含：capability、owner、tools、connectors、side_effect_classes、auth、rate_limits、budgets、telemetry、human_checkpoint、review_cadence。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S01 -->
- 适用情形：分类工具副作用时。只读且无敏感数据外发和持久副作用的工具划入 read_only。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S02 -->
- 适用情形：分类工具副作用时。写业务数据或创建内部记录的工具划入 write。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S03 -->
- 适用情形：分类工具副作用时。删除、覆盖、批量修改或难恢复工具划入 destructive。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S04 -->
- 适用情形：分类工具副作用时。发送外部消息或通知的工具划入 external_message。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S05 -->
- 适用情形：分类工具副作用时。退款、credit、收费、发票、额度或结算工具划入 money_movement。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S06 -->
- 适用情形：分类工具副作用时。改变订阅、权限、配额或 feature access 的工具划入 entitlement。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S07 -->
- 适用情形：分类工具副作用时。后台运营、生产配置、break-glass 或支持工具划入 admin。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S08 -->
- 适用情形：分类工具副作用时。shell、解释器、浏览器自动化、本地 MCP、容器或文件写入工具划入 code_execution。

<!-- rule-id: TECH-033-AI-PROMPT-RUNTIME-CONTRACT-S01 -->
- 适用情形：构建 AI prompt 时。Prompt builder 须读取 route id；Prompt builder 须读取 route policy；Prompt builder 须读取 allowed tool set。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S04 -->
- 适用情形：实现工具路由时。工具路由须与 red-team 工件相连。

<!-- rule-id: TECH-207-GOVERNANCE-DEV-WORKSPACE-AI-CODING-S02 -->
- 适用情形：使用自有应用模板时。批准自有模板后须记录回退边界。

<!-- rule-id: TECH-007-AI-EVAL-FIXTURE-S01 -->
- 适用情形：建立 AI fixtures 时。AI fixtures 须包含边界样例。

<!-- rule-id: TECH-039-AI-RAG-MEMORY-S01 -->
- 适用情形：定义试点数据边界时。Data Boundary 须说明是否接触RAG source。

<!-- rule-id: TECH-008-AI-EVAL-FIXTURE-S01 -->
- 适用情形：定义试点数据边界时。Data Boundary 须说明是否接触训练/eval 材料。

<!-- rule-id: TECH-030-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：定义试点 AI 边界时。AI Boundary 须说明客户数据是否用于prompt。

<!-- rule-id: TECH-039-AI-RAG-MEMORY-S02 -->
- 适用情形：定义试点 AI 边界时。AI Boundary 须说明客户数据是否用于RAG；AI Boundary 须说明客户数据是否用于memory。

<!-- rule-id: TECH-024-AI-MODEL-ROUTING-S01 -->
- 适用情形：定义试点 AI 边界时。AI Boundary 须说明客户数据是否用于供应商处理。

<!-- rule-id: TECH-024-AI-MODEL-ROUTING-S02 -->
- 适用情形：启用客户专属 AI 配置时。客户专属 AI 配置须链接相应的 模型路由 工件。

<!-- rule-id: TECH-031-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：发现 AI prompt、tool 或 RAG source 的 secret exposure 时。发现 prompt injection 诱导模型泄露 secret、工具返回 secret、RAG/source 含 secret 时，按 exposure review 处理，并补充 AI red-team case 或 AI tool runtime guard。

<!-- rule-id: TECH-037-AI-QUALITY-TELEMETRY-CONTRACT-S01 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。Kratos middleware/handler 须记录 capability；Kratos middleware/handler 须记录 workflow version；Kratos middleware/handler 须记录 prompt version；Kratos middleware/handler 须记录 route id；Kratos middleware/handler 须记录 eval version；Kratos middleware/handler 须记录 trace id；Kratos middleware/handler 须记录 fallback reason；Kratos middleware/handler 须记录 quality severity；Kratos middleware/handler 禁止记录原始内容。

### 异步任务、Webhook 与韧性

<!-- rule-id: TECH-094-JOB-DEFAULT-STATE-MACHINE -->
- job contract 的缺省状态机须包含 `queued`、`leased`、`running`、`succeeded`、`failed`、`cancel_requested`、`cancelled` 和 `expired`。

<!-- rule-id: TECH-123-ASYNC-JOB-WORKER-S01 -->
- 适用情形：执行客户数据删除、导出或同步时。删除、导出和同步缺省使用异步 job。

<!-- rule-id: TECH-239-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：定义 AI schema 时。每条 AI schema 须记录 fallback。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S01 -->
- 适用情形：触发 integration 工件时。event catalog 缺省位于 integrations/event-catalog/<target>.json。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S05 -->
- 适用情形：处理 Webhook 时。Webhook 状态不确定时须拉取 provider 当前对象状态。

<!-- rule-id: TECH-126-ASYNC-JOB-WORKER-S01 -->
- 适用情形：建立异步工件时。job registry 缺省位于 async-jobs/job-registry/<target>.json。

<!-- rule-id: TECH-126-ASYNC-JOB-WORKER-S02 -->
- 适用情形：编写 job registry 时。job registry须包含：target、owner、queues、job_types、schedules、storage、workers、rate_limits、retention、human_checkpoint、review_cadence。

<!-- rule-id: TECH-126-ASYNC-JOB-WORKER-S03 -->
- 适用情形：登记 queue 时。每个 queue须包含：id、purpose、priority、max_concurrency、dispatch_rate_per_minute、status。

<!-- rule-id: TECH-126-ASYNC-JOB-WORKER-S04 -->
- 适用情形：登记 job type 时。每个 job type须包含：id、name、queue、payload_schema_ref、result_schema_ref、trigger、side_effect_class、idempotency、dedupe_key、max_attempts、cancellation、progress、user_visible、data_policy、status。

<!-- rule-id: TECH-243-RETRY-FALLBACK-RESILIENCE-S02 -->
- 适用情形：登记 job type 时。每个 job type须包含：timeout_seconds、retry_policy。

<!-- rule-id: TECH-127-ASYNC-JOB-WORKER-S01 -->
- 适用情形：存储 job result 时。result 缺省保存引用、摘要、artifact id 或受控对象。

<!-- rule-id: TECH-122-ASYNC-JOB-QUEUE-INDEXES-S01 -->
- 适用情形：设计 Postgres 队列表时。Postgres 队列表缺省按 status 建索引；Postgres 队列表缺省按 priority 建索引；Postgres 队列表缺省按 run_after 建索引；Postgres 队列表缺省按 lease_expires_at 建索引；Postgres 队列表缺省按 attempt_count 建索引；Postgres 队列表缺省按 tenant_id 建索引；Postgres 队列表缺省按 dedupe_key 建索引。

<!-- rule-id: TECH-202-GOVERNANCE-ASYNC-JOB-WORKER-S01 -->
- 适用情形：使用 background mode 时。background mode须登记：provider response id、polling 状态、terminal state、超时、数据保留边界。

## 输入与产物

输入包括已批准的产品行为和体验契约、现有系统与数据边界、流量和容量假设、供应商及合规约束，以及来源明确要求保留的人工判断点。产物只按真实触发形成 ADR、boundary/module/dependency 工件、契约与 schema、权限和配置策略、AI route/tool/context 工件、job/webhook contract、观测与审计结构，以及本批来源实际要求的 rollback、幂等或客户数据备份例外。

## 完成、停止或退出条件

适用的带 rule-id 技术决定有唯一权威落点，条件、字段集合、OR 关系和人工判断点可追溯时，技术设计可以交给后续项目消费。存在未裁决冲突、高影响人工判断缺失、数据或权限边界不清，或契约破坏没有迁移路径时停止；需要改变产品行为或用户交互时返回定义或体验设计。

## 相关项目引用

- 定义提供产品行为、范围、商业与 AI 风险边界；技术设计不改写这些含义。
- 体验设计提供用户任务、状态、错误、授权和控制合同；技术设计只定义支撑接口。
- 计划负责拆分和排序；实现负责代码、schema、migration、IaC 与环境资源。
- 验证负责评审、测试、完整环境证据、restore 验证及其他证明材料；技术设计只提供可被验证的结构与接口。
- 发布负责 build、smoke、部署、开放、迁移、回滚和确认动作；技术设计只提供被发布流程消费的契约。
- 运行负责生产处置、告警响应、备份运行、restore 操作以及 RPO/RTO 的运行权威；评估负责相应恢复效果与学习结论。
- 本项目不宣称覆盖通用 IaC、环境资源、RPO/RTO 或 restore 规则，只保留本批来源中的 AI rollback/compensation、写操作幂等/事务和客户数据备份例外。

<!-- rule-id: TECH-079-SCHEMA-OLD-FIXTURE-HANDOFF -->
- schema 设计须提供旧 fixture 的引用接口；旧 fixture 的保留证据由验证项目负责。

<!-- rule-id: TECH-079-SCHEMA-COMPATIBILITY-CONCLUSION-HANDOFF -->
- schema 变化须提供新旧兼容性结论的引用接口；兼容性验证证据由验证项目负责。

<!-- rule-id: TECH-027-PROMPT-LIFECYCLE-HANDOFF -->
- prompt builder 须纳入验证项目的评审与测试范围，并纳入发布项目的部署范围；这些证据和动作不由技术设计维护。

<!-- rule-id: TECH-161-RELEASE-PIPELINE-SECTIONS -->
- 发布项目的 pipeline schema 建议包含 `build` 与 `smoke_test`；技术设计只提供被它们引用的 artifact、health/smoke 和 rollback 接口。

<!-- rule-id: TECH-161-RELEASE-BUILD-SCHEMA -->
- 发布项目的 `pipeline.build` 建议登记 `kind`、`commands` 和 `artifact`；这些发布配置不在技术设计中复制。

<!-- rule-id: TECH-161-RELEASE-SMOKE-ROLLBACK-SPECIFICITY -->
- 发布项目须让 `smoke_test` 指向可读文件，且 smoke 与 rollback 禁止只写“看情况”；技术设计只定义可供其调用的接口。

<!-- rule-id: TECH-172-COMPLETE-ENVIRONMENT-EVIDENCE-HANDOFF -->
- 完整环境证据由实现与验证项目维护；不完整的组件集合禁止被宣称为完整项目环境。
