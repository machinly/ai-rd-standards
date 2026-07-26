# 实现

## 项目目的与边界

实现把已确认的产品、体验和技术输入转成代码、配置、schema、migration、生成物、工作区命令和其他技术产物。它负责保持实现批次可审查、可复现并受既定风险边界约束；它不重新决定产品方向、契约边界或上线许可，也不把测试证明、发布执行、生产观测和事故处置复制成实现规则。

## 根本原则

- **ITEM-IMPLEMENTATION-001**：实现需要改变接口、架构、权限、安全、成本、数据、供应商或承诺边界时，应返回技术设计更新相应决定。

## 核心判断

以下问题是非规范性阅读提示，不替代带 rule-id 的规范：

- 当前输入是否已经足以开始实现，还是需要返回定义、体验设计或技术设计？
- 本批次实际触发了哪些后端、前端、数据、配置、AI、异步或外部副作用表面？
- 代码与生成物、配置与 flag、同步与异步、前端与服务端权限是否保持边界？
- schema、路径、命令、字段集合、OR 关系和例外是否完整保留？
- 高风险动作是否停在人工 checkpoint 前，并具有幂等、审计、限流或恢复接口？
- 实现缺口应在何处修复，哪些证据和上线动作必须交给验证或发布项目？

## 重新组织后的规范要求

### 入口、范围与回退

<!-- rule-id: IMPL-MINIMAL-KERNEL-PRECEDENCE -->
- 应用 prompt/eval、Go/Kratos 服务、Vite 前端、数据迁移、配置与 Feature Flag、开发工作区或外部副作用等按需规则时，如其与本规范的正式分类及项目原则冲突，以正式规范为准。

<!-- rule-id: IMPL-OPTIONAL-PLAYBOOK-STATUS -->
- 本实现规范中的 Go/Kratos、Vite、数据迁移、配置、开发工作区和外部副作用专项均是按需 playbook，不得当作每个实现批次的默认流程。

<!-- rule-id: IMPL-W4-MAIN-FIRST -->
- 进入实现时先以本规范判断真实触发条件，再只读取适用主题；普通实现不得绕过本规范直接套用专项。

<!-- rule-id: IMPL-SPECIALTY-TRIGGER-MATRIX -->
- 仅当相应实现面真实存在时，才须加载对应专项：Go/Kratos 服务、Protobuf/gRPC、sqlc、repository 或后端测试进入服务端专项；Vite、React/TypeScript、API adapter、设计 token、可访问交互、构建或预览进入前端专项；schema、query、migration、backfill、数据修复、恢复前置或隐私数据处理进入数据专项；配置注册表、环境差异、flag、kill switch、runtime 参数、前端公开 env 或 AI route 进入配置专项；本地工具链、命令、seed/fixture、one-step verify 或 AI coding 进入工作区专项；收费权益、Webhook、外部 provider、消息通知或对外开发者副作用进入外部副作用专项；长任务、队列、worker、Batch/background、RAG 入库、导入导出、重试、死信或异步状态进入 job 专项。

<!-- rule-id: IMPL-SELECTED-STANDARD-HIGH-RISK-CHANGE -->
- 被选事项进入 Deliver Standard/High-risk 实现时，须创建或继续 OpenSpec change；风险路径和变更性质触发该要求，不能用任务时长、文件数或领域关键词替代判断。轻量 Explore 默认只维护短记录。

<!-- rule-id: IMPL-DISCOVERY-AND-SPEC-BOUNDARY -->
- Explore 可以在 sandbox 中形成不可发布的最小实现：Product Discovery 只实现验证 hypothesis 所需的 shortest slice，UX Prototype 只比较体验，Technical Spike 先关闭 Walking Skeleton。它们不得替代 promote 后的 OpenSpec、稳定契约、AI eval、Deliver 验证或发布门禁；横向框架、恢复矩阵、平台化和完整质量工件延后到出现首个可见产品事实并选定稳定增量之后。

<!-- rule-id: IMPL-USER-VISIBLE-LONG-WORK-ENTRY -->
- 用户可见能力要进入 Deliver 且预计超过 1 个工作日的实现时，必须已有明确目标用户、真实问题、唯一主指标和停止条件。Explore 由 shortest slice、5 个 active tasks 和 showcase cadence 约束，不因预计时长自动转成 Deliver。

<!-- rule-id: IMPL-SPEC-TO-TASKS-HANDOFF -->
- Deliver 行为、边界和风险已经写清时，才进入稳定实现；Standard/High-risk 以 OpenSpec `tasks.md` 作为执行清单。Explore 只使用一份短记录并从实际入口实现 shortest slice。

<!-- rule-id: IMPL-SELECTIVE-TEST-FIRST -->
- 核心领域规则、服务端授权、安全边界、数据一致性、公共契约、bugfix 和危险重构优先测试先行；抛弃式 UI 脚手架、生成代码、简单配置和 UX/Technical Explore 可以先实现后补对 selected behavior 有价值的自动化。Explore promote 前必须为准备稳定的行为补齐与风险相称的回归证据，不追溯要求所有失败探索都采用 TDD。

<!-- rule-id: IMPL-VISUAL-UX-GATE -->
- 用户可见 Standard/High-risk 实现开始前须读取 proposal 的 `visual_ux` 判定；值为 `required` 时，只有计划引用当前 `flow.md`、关键 wireframes 和人类 `approved` review，且项目内组件复用选择已说明，才可开始相关生产性编码。缺失任一输入时返回体验设计或计划，不得用 OpenSpec、文字 brief 或已生成代码代替批准。

<!-- rule-id: IMPL-AI-DEFINITION-BEFORE-BUILD -->
- 用户可见 AI 行为及其输入已由[定义](../02-product-design/03-definition.md)明确、交互感知已由[体验设计](../02-product-design/04-experience-design.md)明确，且 prompt/eval 等技术边界已由[技术设计](05-technical-design.md)明确后，才可把 Go、Vite、worker 或 config 交给实现；缺少哪类输入就返回对应项目。

<!-- rule-id: IMPL-W4-AUTHORITY-BOUNDARY -->
- 实现不得重新决定产品方向、风险边界或上线许可。产品方向、scope 或用户可见行为变化时返回[选题](../01-initiation/01-topic-selection.md)或[定义](../02-product-design/03-definition.md)，交互感知变化时返回[体验设计](../02-product-design/04-experience-design.md)，契约、安全、成本或 AI 技术方案变化时返回[技术设计](05-technical-design.md)，上线许可变化时返回[发布](09-release.md)更新输入。

<!-- rule-id: IMPL-VISUAL-UX-DEVIATION -->
- 实现发现已批准方案中的任务路径、页面结构、状态、权限含义或高风险确认无法成立，或需要产生实质偏差时，须停止受影响路径，先更新可视 UX 并重新取得人类批准；不得只在代码中改变界面，再把线框当作过期附件。

<!-- rule-id: IMPL-LOCAL-CHANGE-ARCHITECTURE-EXCLUSION -->
- 局部实现未改变依赖方向、接口、数据所有权或可见性时，不触发架构专项。

<!-- rule-id: IMPL-WORTH-RETURN-INTAKE -->
- 实现事项不再值得做、需要重新判断优先级或已超过 appetite 时，须返回[选题](../01-initiation/01-topic-selection.md)，不得在实现内继续扩张。

<!-- rule-id: IMPL-BOUNDARY-RETURN-TECH-DESIGN -->
- API、架构、权限、安全、成本、数据、供应商或承诺边界变化时，须返回[技术设计](05-technical-design.md)，不得在实现批次中静默改写。

<!-- rule-id: IMPL-OPEN-SPEC-LINK-OR-RATIONALE -->
- 每个实现批次须链接对应 OpenSpec change；确实不需要 change 时，须明确记录理由。

<!-- rule-id: IMPL-REVIEWABLE-BATCH -->
- 每个实现工作须留下可 review 的实现批次。

<!-- rule-id: IMPL-LOCAL-RUN-COMMAND -->
- 每个实现工作须留下本地可运行命令。

<!-- rule-id: IMPL-VERIFICATION-HANDOFF-RISKS -->
- 移交验证时，须列出失败项、人工接受风险、残余风险和需要补测的路径；这些项的证明由验证项目维护。

<!-- rule-id: IMPL-TRIGGERED-SPECIALTY-MINIMUM -->
- 财务、权限、外部副作用、用户触达、开发者 API 或后台任务被触发时，须产生对应专项的最小工件，或记录明确的不适用理由；只为真实触发面补工件。

<!-- rule-id: IMPL-LOW-RISK-DETAIL-DISCRETION -->
- 包名、普通文件拆分、常规 CRUD 分层、局部 CSS、低风险 copy 与命令目录顺序等低风险细节，缺省由实现者按仓库规范推进，不升级为人工判断点。

<!-- rule-id: IMPL-NEAREST-SIDE-EFFECT-SPECIALTY -->
- 同时触发多个专项时，先读取最靠近副作用边界的专项。

<!-- rule-id: IMPL-AI-LONG-JOB-DUAL-ROUTING -->
- AI 长任务须同时应用异步 job 与相关 AI 行为/runtime 约束。

<!-- rule-id: IMPL-INPUT-INTEGRITY-EXIT -->
- 退出实现前须确认技术设计和 AI 行为输入没有被实现过程暗改。

<!-- rule-id: IMPL-INPUT-CHANGE-RECORDED-RETURN -->
- 实现确实改变上游输入时，须先返回相应项目更新记录，再继续实现。

<!-- rule-id: IMPL-MINIMUM-ARTIFACT-EXIT -->
- 所有已触发的实现专项须产生最小工件，或留下不适用理由。

<!-- rule-id: IMPL-BUILDABLE-OR-CONCRETE-BLOCKER -->
- 移交验证前，本地实现须能够构建；无法运行时，至少给出具体原因。

<!-- rule-id: IMPL-HIGH-RISK-CONTROL-DESCRIPTION -->
- 高风险实现面交给验证前，至少须说明 rollback、幂等、限流、审计或人工 checkpoint 中的一项适用控制。

<!-- rule-id: IMPL-AI-CODING-SMALL-BATCH -->
- AI coding 变更须保留小批次记录。

<!-- rule-id: IMPL-AI-CODING-SELF-REVIEW -->
- AI coding 变更交出前须完成生产者自审。

<!-- rule-id: IMPL-IMPLEMENTATION-FIX-RETURN -->
- 验证、发布、运行或评估中发现代码、配置、migration、worker、billing、Webhook、通知、集成、timeout、retry、数据库、bundle、fallback 或 degraded UI 等实现缺口时，必须返回本实现项目修复，不得在下游项目夹带补实现。

<!-- rule-id: IMPL-VERIFICATION-NEED-HANDOFF -->
- 实现完成后需要质量、安全、性能、可访问性或韧性证明时，转交验证项目；实现只提供可被验证的产物和接口。

<!-- rule-id: IMPL-OPERATIONS-HANDOFF -->
- 线上观测、告警、runbook、事故与凭据轮换转交运行项目；实现不得复制其处置权威。

### 分析事件与承诺连接

<!-- rule-id: IMPL-ANALYTICS-DESTINATIONS -->
- tracking plan 须记录事件目的地；允许值包括 `local_db`、`warehouse`、`analytics_vendor`、`observability`、`none` 等实际选项。

<!-- rule-id: IMPL-ANALYTICS-IMPLEMENTATION-LINKS -->
- tracking plan 须链接适用的 Go/Kratos、Proto、sqlc、Vite、OpenSpec 或 product bet 实现表面。

<!-- rule-id: IMPL-CENTRAL-OUTCOME-EVENT-EMISSION -->
- 生产后端应通过集中 analytics/event service 或明确 usecase hook 发出 outcome 事件，禁止由各 handler 自由拼装。

<!-- rule-id: IMPL-COMMITMENT-TRACEABILITY -->
- 用户或外部承诺须能追溯到实际实现或证据。

### Go/Kratos、gRPC 与生成代码

<!-- rule-id: IMPL-SERVICE-CHANGE-SOURCE -->
- Standard/High-risk 服务端需求须由链接权威产品输入的 OpenSpec change 承载。

<!-- rule-id: IMPL-SQLC-NOT-ORM-DEFAULT -->
- 数据访问缺省使用 sqlc，不默认引入 ORM。

<!-- rule-id: IMPL-NEW-SERVICE-TEMPLATE -->
- 新服务须在空目录使用当前批准的 Kratos CLI 模板生成。

<!-- rule-id: IMPL-SERVICE-DIRECTORY-LAYOUT -->
- 服务缺省目录为：`api/` 放 Protobuf API 与生成代码，`cmd/<service>/` 放程序入口，`configs/` 放本地配置样例，`internal/server/` 放 server 装配，`internal/service/` 放 transport 适配，`internal/biz/` 放 usecase、实体、领域错误和 repository 接口，`internal/data/` 放 repository 实现、事务和 sqlc 调用，`internal/conf/` 放配置结构，`migrations/` 放数据库迁移，`queries/` 放 sqlc 查询，`sqlc.yaml` 放 sqlc 配置。

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

### 前端、语义样式与可访问实现

<!-- rule-id: IMPL-FRONTEND-REQUIREMENT-SOURCE -->
- 前端需求可以由 work brief 或 OpenSpec 承载；实际采用何者须与当前风险路径一致。

<!-- rule-id: IMPL-VANILLA-STATIC-OPTION -->
- 简单静态页或原型可以使用 `vanilla-ts`。

<!-- rule-id: IMPL-PACKAGE-MANAGER-DEFAULT -->
- 包管理器优先沿用仓库已有工具；新项目没有既有选择时，缺省使用 `pnpm`。

<!-- rule-id: IMPL-GEIST-SEMANTIC-STYLE -->
- UI 风格缺省参考 Geist 的语义设计语言。

<!-- rule-id: IMPL-NONDEFAULT-BROWSER-PROTOCOL-DESIGN -->
- 使用 gRPC-Web 或 Connect 等非默认浏览器协议时，须在 `design.md` 说明。

<!-- rule-id: IMPL-STATE-LIBRARY-REAL-NEED -->
- 只有跨页面共享、缓存或协作编辑真实存在时，才引入状态库。

<!-- rule-id: IMPL-COMPONENT-ABSTRACTION-THRESHOLD -->
- 相同交互从第二个调用点起复用已有实现，可在单个 feature 内用 feature-local 组件组合；只有同一项目至少 3 个真实调用点且语义稳定时，才把它泛化或晋升为跨 feature 的 shared component。不得为达到阈值复制实现，也不得用该阈值阻止 feature-local 组合复用。

<!-- rule-id: IMPL-FRONTEND-DIRECTORY-LAYOUT -->
- 前端缺省使用 `index.html`、`package.json`、`src/app/`、`src/components/`、`src/features/`、`src/lib/`、`src/styles/`、`src/main.tsx`、`src/vite-env.d.ts` 与 `public/`；各路径分别承载入口、包清单、应用装配、共享组件、功能代码、通用 client/helper、样式、主入口、Vite env 类型和静态公共资源。

<!-- rule-id: IMPL-SHARED-COMPONENT-SCOPE -->
- `src/components` 只放跨 feature 重复使用的基础组件。

<!-- rule-id: IMPL-FRONTEND-SEMANTIC-TOKENS -->
- 颜色、间距、半径、阴影和字体变量须集中在 `src/styles/tokens.css`；组件只使用少量语义 token，禁止散落 Vercel 或 `gray-700` 一类原始 token 名。

<!-- rule-id: IMPL-FRONTEND-STRUCTURE-YAGNI -->
- 少于 3 个页面时，不拆复杂路由、状态管理、主题包或组件库包；不得为假设需求预建 monorepo、design system package、Storybook 或复杂 mock 平台。

<!-- rule-id: IMPL-CARD-RADIUS-LIMIT -->
- 卡片半径缺省不超过 `8px`。

<!-- rule-id: IMPL-TOOL-PAGE-DENSITY -->
- 工具型页面优先密度、扫描、对齐、表格、筛选和状态，禁止使用营销页式大 hero。

<!-- rule-id: IMPL-ICON-BUTTON-NAME -->
- 图标按钮须提供 `aria-label`，或同时提供 tooltip 与可见文本；所选方式须足以构成可访问名称并符合当前交互语境。

<!-- rule-id: IMPL-NO-DECORATIVE-BOKEH -->
- 产品界面禁止使用离散装饰光斑、渐变球或 bokeh 背景。

<!-- rule-id: IMPL-GRID-CHOICE -->
- Geist Grid 只用于可见 guide 本身属于设计的页面；普通列表和卡片网格使用 CSS grid。

<!-- rule-id: IMPL-NATIVE-HTML-FIRST -->
- 交互控件优先使用原生 HTML；只有原生控件不能满足需求时才使用 ARIA。

<!-- rule-id: IMPL-INTERACTIVE-A11Y-BASICS -->
- 所有交互控件须键盘可达、具有可见 `:focus-visible` 和可访问名称；不得移除可见焦点。

<!-- rule-id: IMPL-PAGE-SEMANTIC-STRUCTURE -->
- 页面须具备 `main`、合理层级 heading，以及适用的 `label`、真实 `button`、真实 link 和 `status`/live region 或等价语义。

<!-- rule-id: IMPL-FORM-STATE-AND-PROTECTION -->
- 表单字段须有 label、helper text、error text、提交中状态和重复提交防护。

<!-- rule-id: IMPL-OVERLAY-FOCUS-BEHAVIOR -->
- 弹层、菜单和抽屉须管理或 trap 焦点、处理 `Esc`、定义点击外部行为，并在关闭后把焦点返回触发元素。

<!-- rule-id: IMPL-NOT-COLOR-ONLY -->
- 图标按钮、状态点、加载状态以及危险 replay/cancel/retry 禁止只靠颜色表达含义。

<!-- rule-id: IMPL-REDUCED-MOTION -->
- 动效须尊重 `prefers-reduced-motion`。

<!-- rule-id: IMPL-COMPLEX-UI-STATE-MACHINE -->
- 复杂交互缺省使用受控组件与清晰状态机；本专项前端缺省栈为 Vite、React 和 TypeScript。

<!-- rule-id: IMPL-ASYNC-AI-UI-STATES -->
- 异步 AI 任务须暴露 `pending`、`running`、`succeeded`、`failed`、`cancelled` 与 `degraded`，禁止让前端保持无限 loading。

<!-- rule-id: IMPL-USER-CONTROL-AUDIT-FIELDS -->
- 反馈、纠错、撤销、重新生成和人工处理 API 应记录 `actor`、`tenant`、`surface`、`ai_feature`、request id 与 audit 引用。

<!-- rule-id: IMPL-AI-USER-ACTION-RECOVERY -->
- 生成、重试、取消、编辑、撤销、提交与人工复核都须有明确状态和可恢复路径。

### 数据变更、migration、backfill 与修复

<!-- rule-id: IMPL-DATA-CHANGE-VERSION-CONTROL -->
- schema、query、migration、backfill、数据修复、备份恢复实现与隐私处理产物须进入版本控制。

<!-- rule-id: IMPL-DATA-DEFAULT-STACK -->
- 数据变更缺省栈为 MySQL、sqlc 与 Go/Kratos。

<!-- rule-id: IMPL-MIGRATION-TOOL-DEFAULT -->
- migration 工具不强制绑定；新 Go 服务没有既有选择时，缺省采用可版本化 SQL migration。

<!-- rule-id: IMPL-DOWN-MIGRATION-SAFETY -->
- 只有确实安全时才提供 down migration。

<!-- rule-id: IMPL-HIGH-RISK-MIGRATION-FORWARD-RECOVERY -->
- 涉及已写入数据、审计或身份关系时，优先采用前向恢复、禁用写路径或补偿，不把 down 当作缺省恢复方案。

<!-- rule-id: IMPL-NO-RETROACTIVE-PROD-DDL -->
- 禁止先在生产执行临时 DDL/DML 再补文件或文档。

<!-- rule-id: IMPL-SCHEMA-QUERY-GENERATE-CODE-ORDER -->
- 数据变更顺序须保持为 schema、query、sqlc 生成、代码调用。

<!-- rule-id: IMPL-NO-LOCAL-PROD-MIGRATION -->
- 禁止从开发者本地直接连接生产执行 migration。

<!-- rule-id: IMPL-DATA-ARTIFACT-PATHS -->
- 数据工件缺省路径为：`migrations/`；顺序编号的 `000001_<slug>.up.sql`；确实安全时对应的 `000001_<slug>.down.sql`；`queries/`；`sqlc.yaml`；`data/changes/<change-id>.json`；`data/backfills/<name>.md`；`data/fixes/YYYY-MM-DD-<slug>.md`。

<!-- rule-id: IMPL-EXISTING-DATA-PATH-RECORD -->
- 既有服务须沿用仓库的数据目录模式，并须在 data change JSON 中写清实际路径。

<!-- rule-id: IMPL-DATA-CHANGE-CORE-SCHEMA -->
- data change JSON 须记录 `change_id`、`service`、`owner`、`environment`、`type`、`risk`、`migration_files`、`query_files` 与 `deploy_order`。

<!-- rule-id: IMPL-DATA-CHANGE-SQLC-SCHEMA -->
- data change JSON 的 `sqlc` 块须记录 `config`、`generate` 与 `vet`。

<!-- rule-id: IMPL-DATA-CHANGE-ROLLBACK-SCHEMA -->
- data change JSON 的 `rollback` 块须记录 `strategy` 与 `data_loss_possible`。

<!-- rule-id: IMPL-DATA-CHANGE-VERIFICATION-SCHEMA -->
- data change JSON 的 verification 信息须记录 `dry_run` 与 `post_checks`；验证结论由验证项目维护。

<!-- rule-id: IMPL-DATA-CHANGE-PRIVACY-SCHEMA -->
- data change JSON 的 `privacy` 块须记录 `personal_data`、`retention_change` 与 `export_or_delete`。

<!-- rule-id: IMPL-DATA-CHANGE-HUMAN-CHECKPOINT-SCHEMA -->
- data change JSON 的 `human_checkpoint` 块须记录 `required` 与 `reason`。

<!-- rule-id: IMPL-PRODUCTION-DATA-CHANGE-RECORD -->
- 每个生产数据变更须在 `data/changes/*.json` 下形成记录；具体文件采用 `data/changes/<change-id>.json`，并包含 rollback 说明。

<!-- rule-id: IMPL-FIX-BACKFILL-RECORD -->
- 数据修复与 backfill 须分别记录在 `data/fixes` 或 `data/backfills`。

<!-- rule-id: IMPL-DATA-SYNC-UPDATE-QUERY -->
- schema 改变后须更新 `queries/*.sql`。

<!-- rule-id: IMPL-DATA-SYNC-GENERATE -->
- query 更新后须运行 `sqlc generate`。

<!-- rule-id: IMPL-DATA-SYNC-REPOSITORY-TESTS -->
- sqlc vet 后须更新 Go repository code 与 tests。

<!-- rule-id: IMPL-DATA-SYNC-NO-GENERATED-EDIT -->
- 同步完成后须确认生成代码没有手工修改。

<!-- rule-id: IMPL-PRODUCTION-BACKFILL-CONTROLS -->
- 生产 backfill 须限速、可重试并可暂停。

<!-- rule-id: IMPL-BACKFILL-DESIGN-FIELDS -->
- backfill 须定义输入范围、batch size、rate limit 与 checkpoint。

<!-- rule-id: IMPL-BACKFILL-BATCH-PROGRESS -->
- backfill 每批须记录成功数、失败数、跳过数与最后处理位置。

<!-- rule-id: IMPL-BACKFILL-DRY-OR-SAMPLE -->
- backfill 须提供 dry-run 或 sample mode 二者之一。

<!-- rule-id: IMPL-BACKFILL-STOP-AND-FAILURE -->
- backfill 须定义停止条件与失败动作。

<!-- rule-id: IMPL-BACKFILL-NONPEAK-DEFAULT -->
- backfill 不得把高峰期作为缺省运行时段。

<!-- rule-id: IMPL-PRODUCTION-DATA-FIX-PATH -->
- 生产数据修复须写入 `data/fixes/YYYY-MM-DD-<slug>.md`。

<!-- rule-id: IMPL-DATA-FIX-RECORD-FIELDS -->
- data fix 记录须包含 `Date`、`Service`、`Tables`、`User impact`、`Reason`、`SQL/migration`、`Rollback/compensation` 与 `Owner`。

<!-- rule-id: IMPL-MANUAL-SQL-FILE-REVIEW -->
- 手工 SQL 在执行前须先写成文件并 review。

<!-- rule-id: IMPL-EMERGENCY-SQL-AFTERCARE -->
- 事故止血先执行手工 SQL 时，事后须补文件以及 incident 或 release log。

<!-- rule-id: IMPL-NO-PURPOSELESS-DATA -->
- 禁止收集没有明确产品目的的数据。

<!-- rule-id: IMPL-PERSONAL-FIELD-PURPOSE-RETENTION -->
- 新增个人数据字段须说明用途与保留期。

<!-- rule-id: IMPL-BACKUP-DELETION-FOLLOWUP -->
- 备份含个人数据时，删除请求须说明备份保留期与恢复后的再删除流程。

<!-- rule-id: IMPL-DESTRUCTIVE-DATA-HUMAN-GATE -->
- 生产删除、`TRUNCATE`、`DROP`、批量 `DELETE`、不可逆 migration 或个人数据导出任一发生时，须设置人工 checkpoint；是否允许这些高影响动作由人判断。

<!-- rule-id: IMPL-CI-PRODUCTION-MIGRATION-HUMAN-GATE -->
- 是否允许 CI 自动执行 production migration 必须交由人工判断。

<!-- rule-id: IMPL-PERSONAL-DATA-CHANGE-HUMAN-GATE -->
- 新增、导出、删除个人或敏感数据，或改变其用途，须交由人工判断。

### 配置、Feature Flag 与前端 env

<!-- rule-id: IMPL-CODE-CONFIG-FLAG-SEPARATION -->
- 代码、配置与 Feature Flag 须分开记录：配置只决定部署差异，Feature Flag 只决定运行时行为。

<!-- rule-id: IMPL-CONFIG-ARTIFACT-PATHS -->
- 配置工件缺省位于 `config/environments/<target>.md`、`config/flags/<target>.json` 与 `config/runtime-changes/<target>.jsonl`。

<!-- rule-id: IMPL-CONFIG-ENVIRONMENT-FIELDS -->
- 配置注册表及每个 config item 都须记录适用的 `environments`。

<!-- rule-id: IMPL-ENVIRONMENT-MATRIX-SECTIONS -->
- 环境矩阵须包含 `Scope`、`Environments`、`Config Sources`、`Secrets Sources`、`Differences`、`Promotion Path`、`Validation`、`Rollback` 与 `Human Checkpoints`。

<!-- rule-id: IMPL-PRODUCTION-ENVIRONMENT-SET -->
- 系统进入生产后，环境矩阵至少记录 `local`、`preview` 或 `staging` 二者之一，以及 `production`。

<!-- rule-id: IMPL-FLAG-CATALOG-SCHEMA -->
- Feature Flag 清单须包含 `target`、`flags`、`provider`、`defaults`、`cleanup_policy`、`human_checkpoint` 与 `review_cadence`。

<!-- rule-id: IMPL-FLAG-ITEM-SCHEMA -->
- 每个 flag 须记录 `key`、`type`、`category`、`created_on`、`expires_on` 或 `review_on` 二者之一、`default`、`fail_behavior`、`targeting` 与 `cleanup_plan`。

<!-- rule-id: IMPL-SHORT-LIVED-FLAG-EXPIRY -->
- release 和 experiment flag 须有 `expires_on`。

<!-- rule-id: IMPL-LONG-LIVED-FLAG-REVIEW -->
- ops、permission 与 kill_switch flag 至少须有 `review_on`。

<!-- rule-id: IMPL-ALL-FLAGS-CLEANUP-PLAN -->
- 所有 flag 都须有 cleanup plan。

<!-- rule-id: IMPL-RUNTIME-CHANGE-LOG-SCHEMA -->
- runtime change 日志须包含 `date`、`target`、`environment`、`change_type`、`key`、`actor`、`reason`、`result` 与 `rollback`。

<!-- rule-id: IMPL-GO-TYPED-CONFIG -->
- Go 配置须使用类型化 struct，禁止在业务代码中散落 `os.Getenv`。

<!-- rule-id: IMPL-LOOKUPENV-WHEN-EMPTY-DIFFERS -->
- 需要区分“未设置”和“空值”时，使用 `os.LookupEnv`。

<!-- rule-id: IMPL-KRATOS-CONFIG-BOUNDARY -->
- Kratos config 负责加载、watch 与 decode；业务层只接收已校验的配置对象。

<!-- rule-id: IMPL-CONFIG-FAIL-FAST-EXCEPTION -->
- 关键配置或未明确可降级的配置加载失败时须 fail fast；只有明确可降级的非关键配置例外。

<!-- rule-id: IMPL-RELOADABLE-CONFIG-CONTRACT -->
- reloadable 配置须说明 reload 范围、验证方式与失败回退。

<!-- rule-id: IMPL-VITE-ENV-NONSENSITIVE -->
- 进入浏览器 bundle 的 env 必须是非敏感信息。

<!-- rule-id: IMPL-VITE-ENV-PREFIX -->
- 客户端变量须使用 `VITE_` 前缀，或项目明确配置的 `envPrefix`。

<!-- rule-id: IMPL-RUNTIME-PUBLIC-CONFIG-ENDPOINT -->
- 前端需要运行时动态配置时，须使用后端只读 public config endpoint，并记录缓存和回滚。

<!-- rule-id: IMPL-FRONTEND-FLAG-UI-ONLY -->
- 前端 flag 只能控制 UI exposure，不能作为服务端权限或权益裁决。

<!-- rule-id: IMPL-RELEASE-FLAG-EXPIRY -->
- release toggle 只用于短期隐藏能力，并须有 `expires_on`。

<!-- rule-id: IMPL-EXPERIMENT-FLAG-CRITERIA -->
- experiment toggle 须有 success criteria、stop criteria 与 cleanup。

<!-- rule-id: IMPL-MIGRATION-FLAG-ROUTE -->
- migration toggle 须进入数据迁移规范处理。

<!-- rule-id: IMPL-EXPIRED-FLAG-REMOVAL -->
- 过期 flag 须删除代码路径与配置，禁止以“以后可能用”为由保留。

<!-- rule-id: IMPL-AI-CONFIG-COST-ROLLBACK -->
- AI 配置变更须链接成本 guardrail 与 rollback。

<!-- rule-id: IMPL-AI-ROUTE-FLAG-FIELDS -->
- AI route flag 须记录 `default`、`fallback` 与 `fail behavior`。

<!-- rule-id: IMPL-PRODUCTION-CONFIG-HUMAN-GATE -->
- 生产配置或 Feature Flag 变更须交由人工判断。

<!-- rule-id: IMPL-SENSITIVE-CONFIG-HUMAN-GATE -->
- 敏感配置的新增、迁移或轮换窗口须交由人工判断。

<!-- rule-id: IMPL-LONG-LIVED-FLAG-HUMAN-GATE -->
- 长期保留某个 flag 须交由人工判断。

<!-- rule-id: IMPL-FRONTEND-ENV-HUMAN-GATE -->
- 向前端暴露环境变量须交由人工判断。

<!-- rule-id: IMPL-AI-RUNTIME-SWITCH-HUMAN-GATE -->
- 在运行时切换 AI model、provider 或 prompt route 须交由人工判断。

### 工作区、模板与 AI coding

<!-- rule-id: IMPL-REPRODUCIBLE-WORKSPACE -->
- 本地命令与模板来源须可复现。

<!-- rule-id: IMPL-NEW-APP-APPROVED-TEMPLATE -->
- 所有新应用先在空目录使用当前批准模板生成；禁止覆盖既有非空根目录，也禁止手工仿造目录后声称来自模板。

<!-- rule-id: IMPL-KRATOS-TEMPLATE-PROVENANCE -->
- Go 服务的模板 provenance 须保存 CLI 版本、`kratos new` 命令、模板来源或 revision 与初始文件清单。

<!-- rule-id: IMPL-OWN-TEMPLATE-PROVENANCE -->
- 使用已批准自有应用模板时，须记录模板版本与生成参数。

<!-- rule-id: IMPL-COMPLETE-LOCAL-ENVIRONMENT -->
- 多组件项目须有统一入口，启动产品要求的全部后端、全部前端、MySQL 与必要 mock/provider，并支持日志定位和清理。

<!-- rule-id: IMPL-LOCAL-COMMAND-CATALOG-FIELDS -->
- 本地 command catalog 须记录组件清单、端口、健康条件、启动顺序、失败诊断与一键清理。

<!-- rule-id: IMPL-WORKSPACE-ARTIFACT-PATHS -->
- 工作区工件缺省位于 `dev-workspace/workspace-map/<target>.json`、`dev-workspace/command-catalog/<target>.md`、`dev-workspace/local-environment/<target>.md` 与 `dev-workspace/seed-fixtures/<target>.md`。

<!-- rule-id: IMPL-AI-CODING-ARTIFACT-PATHS -->
- AI coding 工件缺省位于 `ai-coding/implementation-brief/<change-id>.md` 与 `ai-coding/batch-log/<change-id>.md`。

<!-- rule-id: IMPL-TOOLCHAIN-PROVENANCE -->
- 工作区须记录 Go、Node、sqlc、protoc、buf、Vite、OpenSpec 等实际工具链的来源与 install check。

<!-- rule-id: IMPL-APP-TEMPLATE-RECORD -->
- 创建应用时须记录模板名称、版本或 revision、生成命令与初始 diff。

<!-- rule-id: IMPL-LOCAL-ENVIRONMENT-RECORD -->
- 完整本地集成环境须记录组件清单、统一启动命令、就绪命令与清理命令。

<!-- rule-id: IMPL-COMMAND-CATALOG-COVERAGE -->
- command catalog 须覆盖 setup、generate、develop、test、verify、run local、reset、debug 与 release prep 命令。

<!-- rule-id: IMPL-AI-FIXTURE-CASES -->
- AI fixtures 须包含代表样例与失败样例。

<!-- rule-id: IMPL-IMPLEMENTATION-BRIEF-FIELDS -->
- implementation brief 须链接 OpenSpec change、context sources 与 target files，并记录 allowed autonomy、human checkpoints 与 stop conditions。

<!-- rule-id: IMPL-ONE-STEP-LOCAL-VERIFY -->
- 工作区至少须提供一个 one-step local verify 命令。

<!-- rule-id: IMPL-TRIGGERED-VERIFY-COMMANDS -->
- 实现触发 sqlc、Proto 或 AI eval 时，须补对应 verify 命令；验证结论由验证项目维护。

<!-- rule-id: IMPL-REPEATED-AI-ERROR-AUTOMATION -->
- AI 反复犯同类错误时，须更新适用的 skill、script、template 或仓库指令。

<!-- rule-id: IMPL-REAL-EXTERNAL-RESOURCE-HUMAN-GATE -->
- 本地命令会调用真实供应商、真实模型、真实支付、真实邮件或真实生产数据时，须交由人工判断。

<!-- rule-id: IMPL-DESTRUCTIVE-ONE-CLICK-HUMAN-GATE -->
- 把破坏性 reset、migration、backfill、生产发布或 tool commit 暴露成一键命令须交由人工判断。

### 外部副作用、billing 与消息

<!-- rule-id: IMPL-EXTERNAL-SIDE-EFFECT-CONTROLS -->
- 每个外部副作用都须具备审计、重放保护与人工 checkpoint。

<!-- rule-id: IMPL-BILLING-ARTIFACT-PATHS -->
- billing 工件缺省位于 `billing/product-catalog/<target>.json`、`billing/entitlement-policy/<target>.md`、`billing/usage-metering/<target>.json` 与 `billing/reconciliation/<target>.json`。

<!-- rule-id: IMPL-MESSAGING-ARTIFACT-PATHS -->
- messaging 工件缺省位于 `messaging/channel-registry/<target>.json`、`messaging/template-catalog/<target>.json` 与 `messaging/preference-consent/<target>.json`。

<!-- rule-id: IMPL-DEVELOPER-SURFACE-CROSS-STAGE -->
- 发布 public/stable API、SDK、CLI 或示例时，须由技术设计、实现与发布项目共同承接；实现只生产其技术产物。

<!-- rule-id: IMPL-SERVER-ENTITLEMENT-CHECK -->
- entitlement 裁决须由服务端执行。

<!-- rule-id: IMPL-ENTITLEMENT-UI-DISPLAY-ONLY -->
- Vite 只能展示后端返回的权益和用量状态。

<!-- rule-id: IMPL-BILLABLE-EVENT-LOCAL-LEDGER -->
- billable event 须在业务完成的耐久边界写入本地账本。

<!-- rule-id: IMPL-BILLABLE-EVENT-ASYNC-SYNC -->
- 本地记账成功后，再异步同步支付平台。

<!-- rule-id: IMPL-WEBHOOK-SLOW-WORKER -->
- 入站 Webhook 的慢处理须进入 worker。

<!-- rule-id: IMPL-OUTBOX-DISPATCHER-DUTIES -->
- outbox dispatcher 须负责投递、有限重试与死信处理。

<!-- rule-id: IMPL-MESSAGE-CLASSIFY-BEFORE-SEND -->
- 通知发送前须先分类。

<!-- rule-id: IMPL-BILLING-LEDGER-APPEND-ONLY -->
- billing ledger 须为 append-only。

<!-- rule-id: IMPL-REPLAY-SELECTION-SAFETY -->
- 手工 replay 只允许处理失败或明确选择的 delivery，禁止重复处理已成功副作用。

<!-- rule-id: IMPL-MARKETING-TRANSACTIONAL-SEPARATION -->
- 营销消息与事务消息须分流。

<!-- rule-id: IMPL-SMS-PUSH-CONSENT -->
- SMS 或 push 缺省需要 opt-in 或平台授权。

<!-- rule-id: IMPL-AI-EXTERNAL-MESSAGE-DRAFT-ONLY -->
- AI 可以生成消息草稿或 event payload 草案，但不得自动发送或执行外部写入。

<!-- rule-id: IMPL-COMMERCIAL-MODEL-HUMAN-GATE -->
- 定价模型、套餐、价格、价值计量单位、超额策略、退款或补偿的发布或改变须交由人工判断。

<!-- rule-id: IMPL-OUTBOUND-SENSITIVE-DATA-HUMAN-GATE -->
- 出站事件会发送敏感数据、用户内容、AI 输出、支付或计费状态、跨租户信息任一项时，须交由人工判断。

<!-- rule-id: IMPL-MESSAGING-EXPANSION-HUMAN-GATE -->
- 新增 channel、provider、sender domain、SMS number、push app，或启用高量、事故、安全、账单、法律通知时，须交由人工判断。

<!-- rule-id: IMPL-EXTERNAL-EFFECT-IDEMPOTENCY-AUDIT -->
- 每个外部副作用须能追溯到 idempotency key 与 audit/ref。

### 异步 job、worker 与长任务界面

<!-- rule-id: IMPL-BACKGROUND-JOB-CONTRACT -->
- 生产后台任务须有显式 job contract，并定义取消策略、观测接口、恢复路径和人工 checkpoint。

<!-- rule-id: IMPL-CLAIM-SQL-ADAPTER-BOUNDARY -->
- 确实需要数据库专有 claim SQL 时，只能隔离在 repository 适配层。

<!-- rule-id: IMPL-USER-VISIBLE-JOB-CONTRACT -->
- 用户可见 job 须提供状态查询、可理解失败原因、结果保留期以及取消与过期策略。

<!-- rule-id: IMPL-SERVER-OWNED-JOB-STATE -->
- job 状态转换须由服务端控制，禁止前端或模型直接写入最终状态。

<!-- rule-id: IMPL-JOB-LEASE-RECOVERY -->
- `leased` 状态须有 `lease_expires_at` 或等价超时；worker 崩溃后，任务须可重新领取或进入 stuck recovery。

<!-- rule-id: IMPL-SKIP-LOCKED-QUEUE-ONLY -->
- `SKIP LOCKED` 只用于 queue-like table 的 worker claim。

<!-- rule-id: IMPL-JOB-EXECUTION-CONTEXT -->
- worker 执行前须绑定 trace id、job id、attempt id、actor、tenant、deadline、cost budget 与 cancellation token。

<!-- rule-id: IMPL-EXPLICIT-ASYNC-SERVICE -->
- 后台异步工作须暴露为明确的服务能力。任何副作用都不得由 prompt 直接发起，也不得借前端轮询写操作、未公开的 cron 或匿名 goroutine 隐式启动。

<!-- rule-id: IMPL-SKIP-LOCKED-NOT-READ-MODEL -->
- 用户状态、统计与审计查询禁止依赖 `SKIP LOCKED` 提供一致视图。

<!-- rule-id: IMPL-WORKER-RUNTIME-CONTROLS -->
- worker 须支持 context deadline、graceful shutdown、lease heartbeat 或短 lease 二者之一、stuck job recovery、bounded concurrency 与 kill switch。

<!-- rule-id: IMPL-LONG-JOB-ID-AND-SURFACE -->
- 用户可见长任务提交后须返回 job id 或 task id，并提供状态页、toast/inline 状态或任务列表中的可见状态表面。

<!-- rule-id: IMPL-LONG-JOB-STATUS-SET -->
- 长任务界面禁止无限 loading，至少显示 `queued`、`running`、`succeeded`、`failed`、`cancelled`、`expired` 与最后更新时间。

<!-- rule-id: IMPL-CANCELLABLE-JOB-ENTRY -->
- 可取消 job 须显示取消入口。

<!-- rule-id: IMPL-NONCANCELLABLE-JOB-EXPLANATION -->
- 不可取消 job 须说明原因、预计影响与结果通知方式。

<!-- rule-id: IMPL-JOB-FAILURE-NEXT-ACTION -->
- 失败状态须给出可执行下一步，例如重试、修改输入、等待、联系客服、下载部分结果或查看审计/错误引用。

<!-- rule-id: IMPL-LONG-AI-WORK-ASYNC-DEFAULT -->
- 长推理、Batch、background、eval、RAG、embedding 与 agent 多步缺省走异步 job。

<!-- rule-id: IMPL-AI-JOB-CONTROL-FIELDS -->
- AI job 须记录 token budget、cost budget、model route、prompt 或 workflow version、eval/safety refs、tool permission refs、result redaction 与用户可见失败状态。

<!-- rule-id: IMPL-AGENT-JOB-BOUNDS -->
- Agent job 缺省限制 iteration、tool fanout、retry 与 wall-clock duration；超限时进入 `failed`、`degraded` 或 `human_review`，禁止继续排队自旋。

### AI prompt、上下文与 runtime

<!-- rule-id: IMPL-EVAL-JSON-FIELD-ORDER-DISCRETION -->
- 编写 eval 数据时，JSON/JSONL 字段顺序缺省无需人工判断。

<!-- rule-id: IMPL-PROMPT-EVAL-SPECIALTY-TRIGGER -->
- 只有[技术设计](05-technical-design.md)要求进一步定义 prompt、eval、结构化输出、workflow/agent 升级或最小质量门禁时，才使用 prompt/eval 专项。

<!-- rule-id: IMPL-PROMPT-VERSION-REPOSITORY -->
- 每个 prompt 都须纳入仓库版本管理；个人笔记、聊天记录、Dashboard 与 Playground 可以作为辅助工作面，但不能成为其唯一保存位置。

<!-- rule-id: IMPL-MODEL-DEFAULT-CENTRAL-CONFIG -->
- 模型默认值须集中配置，禁止散落硬编码。

<!-- rule-id: IMPL-PROMPT-ARTIFACT-PATH -->
- prompt 工件缺省位于 `ai/prompts/<capability>/prompt.md`。

<!-- rule-id: IMPL-AI-TRACE-DIRECTORY -->
- trace 目录缺省位于 `ai/traces/<capability>/`。

<!-- rule-id: IMPL-PROMPT-REQUIRED-SECTIONS -->
- `prompt.md` 须记录目标、输入、输出、拒绝或降级策略、示例与版本记录。

<!-- rule-id: IMPL-MINIMAL-MODEL-CALL-SHAPE -->
- 最小模型调用优先单次调用或固定 workflow。

<!-- rule-id: IMPL-PROMPT-METADATA -->
- 版本化 prompt 须记录 `version`、`owner`、`last_reviewed` 与 `model_default`。

<!-- rule-id: IMPL-PROMPT-INSTRUCTION-QUALITY -->
- prompt 指令须短、具体、可验证，且不得堆积历史原因。

<!-- rule-id: IMPL-PROMPT-EXAMPLE-COVERAGE -->
- prompt 示例须覆盖常见、拒绝和降级情况。

<!-- rule-id: IMPL-PROMPT-SENSITIVE-CONTENT-BAN -->
- prompt 禁止包含 secret、API key、内部不可泄露策略或用户隐私样例。

<!-- rule-id: IMPL-PROMPT-CHANGE-EXPECTED-BEHAVIOR -->
- prompt 改动须说明预期行为变化。

<!-- rule-id: IMPL-PROMPT-FILENAME-DISCRETION -->
- 低风险 AI change 的 prompt 文件命名缺省无需人工判断。

<!-- rule-id: IMPL-EVAL-CASE-ID-DISCRETION -->
- 低风险 AI change 的 case id 缺省无需人工判断。

<!-- rule-id: IMPL-LOCAL-JSONL-FIXTURE-DISCRETION -->
- 低风险 AI change 是否用本地 JSONL 存 fixture，缺省无需人工判断。

<!-- rule-id: IMPL-MEMORY-WORKSPACE-CONTEXT-TYPE -->
- memory policy 的 memory type 须覆盖 workspace context。

<!-- rule-id: IMPL-CONTEXT-DELETION-SURFACES -->
- 上下文删除路径须覆盖 memory item、vector store、embedding、cache、conversation state、application state 与 source index。

<!-- rule-id: IMPL-AI-RUNTIME-W4-LANDING -->
- AI runtime 的配置、flag 与 worker 落地须进入实现项目。

<!-- rule-id: IMPL-AI-RUNTIME-EXPLICIT-USECASE -->
- 后端处理 AI runtime 时，须先经过职责明确的内部 usecase；该入口可以是 `ToolRegistry`、`AIRuntime`、`ModelRouter`，也可以采用职责等价的实现。

<!-- rule-id: IMPL-AI-RUNTIME-INPUT-SCHEMA -->
- AI runtime usecase 输入须包含 capability、task type、actor、tenant、risk tier、latency class、budget class、required tools 与 data boundary。

<!-- rule-id: IMPL-AI-RUNTIME-OUTPUT-SCHEMA -->
- AI runtime usecase 输出须包含 route id、request options 与 allowed tool set。

<!-- rule-id: IMPL-AI-RUNTIME-NO-SCATTERED-HARDCODE -->
- 业务代码禁止散落硬编码 model name、provider URL、max token、reasoning effort、temperature、tool allowlist 或 connector scope。

<!-- rule-id: IMPL-AI-ADAPTER-STABLE-INTERFACE -->
- provider adapter 与 tool adapter 须暴露稳定内部接口。

<!-- rule-id: IMPL-AI-ADAPTER-NO-LEAKAGE -->
- adapter 禁止把供应商 SDK 类型、access token 或 raw tool output 泄漏到业务层。

<!-- rule-id: IMPL-CODE-EXECUTION-TOOL-HUMAN-GATE -->
- 扩大 runtime 能力并引入新代码执行工具时，须交由人工判断。

## 按主题整理的执行细则

### 客户上线与管理界面

<!-- rule-id: IMPL-ONBOARDING-BACKEND-USECASE -->
- 客户上线状态应由后端的统一 usecase 管理；实现可采用职责等价的入口，也可命名为 `CustomerLaunchService` 或 `TenantOnboardingService`。

<!-- rule-id: IMPL-ONBOARDING-ADMIN-CONTENTS -->
- 客户上线管理台应展示试点目标、租户配置、readiness gates、支持路径、风险与下一步。

<!-- rule-id: IMPL-ONBOARDING-ADMIN-DENSITY -->
- 密集管理界面应使用清晰层级、语义色、紧凑表格与可扫描状态，禁止营销式 hero。

<!-- rule-id: IMPL-CUSTOMER-ONBOARDING-VISIBLE-CONTENTS -->
- 客户可见 onboarding UI 只展示需要完成的任务、状态与下一步。

<!-- rule-id: IMPL-CUSTOMER-ONBOARDING-INTERNAL-REDACTION -->
- 客户可见 onboarding UI 禁止暴露内部 route、prompt、trace、供应商错误或 secret 引用。

<!-- rule-id: IMPL-HIGH-RISK-ONBOARDING-ACTION -->
- 高风险 onboarding 按钮须提供图标、tooltip、confirm 与 dry-run/result preview。

<!-- rule-id: IMPL-ONBOARDING-EMPTY-STATE -->
- onboarding 空状态须给出下一步动作，禁止用大段说明文字占据操作界面。

<!-- rule-id: IMPL-CLAIM-CONTROL-API-BOUNDARY -->
- 内部 gRPC API 可以提供 claim 查询与记录能力，但浏览器不得自行决定 claim 是否可发布。

### 运行准备、后台动作与安全响应接口

<!-- rule-id: IMPL-BUSINESS-HOURS-ALERTING-DEFAULT -->
- 除非已有付费用户、合同义务、真实收入风险或外部依赖要求，缺省不实现 24/7 值班，只准备营业时间告警与关键黑盒 uptime 检查。

<!-- rule-id: IMPL-SERVICE-OBSERVABILITY-SURFACE -->
- 每个 Go/Kratos/gRPC 服务至少须提供运行项目规定的最小观测暴露面；具体 SLO、告警和证据由运行项目维护。

<!-- rule-id: IMPL-BACKUP-INFRA-NONDEFAULT-SPECIALTY -->
- 备份、恢复与基础设施不作为缺省独立实现专项。

<!-- rule-id: IMPL-BACKUP-INFRA-HIGH-RISK-ROUTE -->
- 真实合同、付费关键数据、生产 IaC apply、跨区域恢复、客户证据或高风险资源销毁任一触发计划性实现变更时，须走 High-risk、使用 OpenSpec，并保留决策与回滚证据；验证证据由验证项目维护。

<!-- rule-id: IMPL-RELEASE-TEST-HANDOFF -->
- 发布前须引用已运行的 Go、frontend、AI eval 与 migration 相关测试；实现不得把“已写代码”当作测试已通过。

<!-- rule-id: IMPL-ADMIN-CONTROLLED-ACTION -->
- 能写成受控动作的后台操作不得依赖临场 SQL；能够 dry-run 的动作不得直接执行，AI 建议也不等于 AI 可以写生产。

<!-- rule-id: IMPL-ADMIN-SURFACE-APPLICABILITY -->
- Go/Kratos/gRPC admin API、sqlc 数据修正、Vite 后台页面，以及 AI operator、support assistant 或 admin agent 属于后台动作实现面。

<!-- rule-id: IMPL-ADMIN-MIDDLEWARE-CHECKS -->
- Go/Kratos middleware 须完成六项检查：request id 与 approval、风险级别与权限，以及租户和身份。

<!-- rule-id: IMPL-ADMIN-SQL-DATA-FIX-ROUTE -->
- 后台动作确需 SQL 时，须进入 data migration 或 data fix 工件。

<!-- rule-id: IMPL-AI-ADMIN-READONLY-DEFAULT -->
- AI 后台 workflow 缺省只允许只读调查或提出建议，由人执行动作。

<!-- rule-id: IMPL-NO-UNVERIFIED-AUTONOMY-LABELS -->
- 实现权限不得依赖 L0/L1 等未经验证的自治等级命名。

<!-- rule-id: IMPL-SECURITY-RESPONSE-SURFACES -->
- 安全响应实现面可包括 Go/Kratos/sqlc/gRPC 服务、Vite 前端、AI workflow、RAG、外部 connector、后台工具、数据管道、Webhook、CI/CD、基础设施与供应商集成；适用的事故和 advisory 处置由[运行](../04-operations-maintenance/10-operation.md)负责，超出当前边界时应建立独立升级项。

<!-- rule-id: IMPL-POST-INCIDENT-REVIEW-TRIGGERS -->
- SEV0/SEV1、个人数据、客户通知、供应商事故、公开漏洞或 AI 安全事故任一发生时，须为运行项目提供复盘所需实现引用。

<!-- rule-id: IMPL-SECURITY-INTERNAL-APIS -->
- 内部 gRPC API 可以暴露 `ReportSecurityEvent`、`ListIncidentTimeline`、`RecordContainmentAction` 与 `RecordNotificationDecision`。

<!-- rule-id: IMPL-SECURITY-DECISION-NOT-FRONTEND -->
- 事故分级与通知决定禁止由前端单独作出。

<!-- rule-id: IMPL-SECURITY-AUDIT-PATHS -->
- Kratos middleware 应写入最小安全审计字段，覆盖外部或管理路径（connector、Webhook、AI tool call、admin action）以及身份或数据路径（rate limit、租户解析、授权、认证、data delete 和 data export）。

<!-- rule-id: IMPL-CREDENTIAL-EXPOSURE-CONTROLS -->
- credential exposure 的实现须支持四类控制：强制重新认证，停用 connector 或 Webhook，轮换 secret，以及撤销 session、key 或 token。

<!-- rule-id: IMPL-INCIDENT-UI-SENSITIVE-REDACTION -->
- 事故界面的前端展示须排除六类内容：监管判断、尚未公开的漏洞细节、内部 trace、其他租户信息、攻击 payload 和敏感事故细节。

<!-- rule-id: IMPL-AI-INCIDENT-TYPE-SET -->
- AI 事故分类的最低集合由九类组成：agent 误执行、越权记忆、eval 数据泄露、供应商的数据或模型事件、模型拒绝服务、工具越权、RAG 跨租户、敏感信息泄露和 prompt injection。

### 凭据与 secret 实现边界

<!-- rule-id: IMPL-SECRET-ALLOWED-STORAGE -->
- 对真实 secret 值实行存储白名单：允许的载体仅为短期环境变量、开发者本机的受保护存储、云平台、CI secrets 与 secret manager。

<!-- rule-id: IMPL-CREDENTIAL-SCOPE-SET -->
- 凭据治理的实现范围是一个封闭集合，按用途包括：MCP/connector token 与 RAG/vector store；encryption key、JWT signing key、TLS/private key、deploy token 与 cloud IAM；CI/CD、monitoring、analytics、OAuth client 与 Webhook；数据库、对象存储、短信、邮件、支付，以及 OpenAI 或其他模型供应商。

<!-- rule-id: IMPL-CREDENTIAL-STORAGE-REF -->
- `storage_ref` 禁止保存 secret value。该字段的允许值只表示位置或标识，可写本地占位说明、version id、key id、cloud resource id、CI secret name 或 secret manager path。

<!-- rule-id: IMPL-AI-NO-REAL-SECRET-ACCESS -->
- Codex 或其他 AI agent 禁止读取真实 secret。

<!-- rule-id: IMPL-CI-SHORT-LIVED-IDENTITY -->
- CI 缺省使用 OIDC/federated identity 或短期 token。

<!-- rule-id: IMPL-FRONTEND-CREDENTIAL-BAN -->
- Vite 前端不得承载任何能够替代后端身份的凭据，明确包括 JWT secret、service token、数据库 URL、OpenAI key 与 API key。

<!-- rule-id: IMPL-EXPOSED-CREDENTIAL-REVOKE-FIRST -->
- 一旦发现真实值属于 session cookie、OAuth refresh token、CI token、Webhook secret、private key、database URL、OpenAI key 或 production credential 中任一类，处理顺序必须先撤销或轮换，随后才清理历史。

<!-- rule-id: IMPL-KRATOS-SECRET-REFERENCE-ONLY -->
- 交给 Kratos config struct 的内容仅可采用两种形态：secret reference，或已经在运行时完成注入的配置对象。

<!-- rule-id: IMPL-NO-BUSINESS-OPENAI-GETENV -->
- 业务代码禁止散落读取 `os.Getenv("OPENAI_API_KEY")`。

<!-- rule-id: IMPL-GRPC-CREDENTIAL-ENCRYPTED-CHANNEL -->
- gRPC call credentials 禁止在未加密 channel 上传输。

<!-- rule-id: IMPL-FRONTEND-PRIVATE-SERVICE-PROXY -->
- 浏览器需要访问私有 API、数据库、对象存储、支付或 OpenAI 时，secret 须留在后端；请求必须通过 serverless function、BFF 或后端中的一种代理边界。

<!-- rule-id: IMPL-AI-ARTIFACT-SECRET-BAN -->
- 真实 secret 缺省禁止进入任何 AI 内容载体；受约束的表面依次为 support transcript、RAG source、memory、trace、eval fixture、tool output 与 AI prompt。

### 支持、AI 质量与维护实现

<!-- rule-id: IMPL-EVALUATION-DECISION-CONSUMPTION -->
- 发布和运行后的用户反馈、支持请求、质量信号、事故与 AI 回归由评估项目转成下一轮决定；实现只消费其中明确的工程修复项。

<!-- rule-id: IMPL-AI-GAP-RETURN-BEHAVIOR-DESIGN -->
- 信号暴露用户可见 AI 行为或输入定义缺口时返回[定义](../02-product-design/03-definition.md)，交互感知缺口返回[体验设计](../02-product-design/04-experience-design.md)，eval 方案缺口返回[技术设计](05-technical-design.md)，只有证明不足时返回[验证](08-verification.md)；不得仅用实现补丁掩盖。

<!-- rule-id: IMPL-SUPPORT-SURFACE-APPLICABILITY -->
- 生产 SaaS、付费 AI 产品、公开 beta、用户可见 AI workflow、计费/权益/账号支持，以及 AI 输出错误、有害输出、越权工具调用、隐私请求、账号删除、退款、服务事故或重大流失风险，属于支持实现表面。

<!-- rule-id: IMPL-SUPPORT-AI-CONCERN-CATEGORY -->
- `support/intake/<target>.json` 的允许或默认项须包含 AI output concern、safety 与 abuse 类别。

<!-- rule-id: IMPL-SUPPORT-URGENT-REVIEW-TIMING -->
- 出现 SEV1/SEV2、退款潮、AI 伤害投诉或安全隐私请求时，支持 review 应在当天或次日发起。

<!-- rule-id: IMPL-SUPPORT-SERVER-TENANT-CHECK -->
- 支持后台须由 Go/Kratos 服务端执行权限检查，禁止前端直接读取跨租户支持数据。

<!-- rule-id: IMPL-AI-CAPABILITY-SCOPE -->
- 用户可见 AI capability 的实现范围包括三组表面：工具型 workflow、审核、推荐、自动客服和代码辅助；生成、总结、抽取与分类；RAG、agent、assistant 与 chat。

<!-- rule-id: IMPL-AI-CAPABILITY-FILENAME-CONSISTENCY -->
- 同一生产 AI capability 的相关工件须使用一致的 `<capability>` 文件名。

<!-- rule-id: IMPL-AI-QUALITY-USECASE -->
- 后端须通过职责明确的质量 usecase 落下四类记录：eval follow-up、rollback decision、incident 与 quality signal；该入口可以命名为 `AIQualityService`，也可以采用等价实现。

<!-- rule-id: IMPL-MAINTENANCE-EVIDENCE-CLOSEOUT -->
- release、incident、AI 行为、安全/隐私、客户上线、合同、支持、运营与数据变更完成后，实现须提供长期证据和知识收尾的引用；证明与留存策略由[验证](08-verification.md)承接，知识入口和后续维护决定由[评估](../04-operations-maintenance/11-evaluation.md)承接。

<!-- rule-id: IMPL-MAINTENANCE-WORK-ROUTING -->
- 维护信号需要改代码时留在实现，需要补证明时返回[验证](08-verification.md)，暴露用户可见 AI 行为或交互缺口时分别返回[定义](../02-product-design/03-definition.md)或[体验设计](../02-product-design/04-experience-design.md)，暴露 prompt/eval 等 AI 技术方案缺口时返回[技术设计](05-technical-design.md)；产品学习与支持反馈交给[评估](../04-operations-maintenance/11-evaluation.md)承接。

<!-- rule-id: IMPL-MAINTENANCE-FACTS -->
- 维护实现须记录关键依赖、升级策略、技术债利息、弃用计划与下次复审日期。

<!-- rule-id: IMPL-MAINTENANCE-EVIDENCE-INDEX -->
- 维护证据索引须引用 release、incident、AI 行为、安全隐私、admin action、audit log 与 evidence package，并记录留存策略。

<!-- rule-id: IMPL-DEPENDENCY-SPECIALTY-ROUTE -->
- 以下任一事项均须从[评估](../04-operations-maintenance/11-evaluation.md)进入维护与依赖专项：deprecation、Dependabot、AI SDK/framework/runtime 维护、弃用、技术债和依赖升级。后续需要改代码时返回实现，需要形成证明时转交验证。

<!-- rule-id: IMPL-MAINTENANCE-NEXT-REVIEW-QUESTION -->
- 完成维护实现时，须指出哪些依赖、债务、证据或开源承诺需要下一次复审。

<!-- rule-id: IMPL-CONSISTENT-TARGET-FILENAME -->
- 同一产品、服务、前端应用或 AI workflow 的维护工件须使用一致的 `<target>` 文件名。

<!-- rule-id: IMPL-HOWTO-EXECUTABLE-STYLE -->
- how-to 每个任务只写最短可执行步骤和链接，不写长篇背景。

<!-- rule-id: IMPL-DOCUMENT-ACTION-STYLE -->
- 实现文档使用主动语态、祈使句与可执行步骤。

<!-- rule-id: IMPL-MAINTENANCE-NO-CHASE-NO-FREEZE -->
- 依赖维护既不得无目的追新，也不得长期冻结；一人执行时应显式记录依赖或技术债利息，分批处理，并把高风险决定留给人。

<!-- rule-id: IMPL-MAINTENANCE-STACK-SCOPE -->
- 维护实现面包括 Go/Kratos/gRPC/sqlc 服务、shared Go module、generated code、Vite 前端、Node/npm 依赖、构建工具与浏览器 SDK。

<!-- rule-id: IMPL-SMALL-PATCH-EXCLUSION -->
- 单次小 patch 只有在不改变 runtime、framework、API、数据、auth、安全或 AI 行为契约时，才可按小范围维护处理。

<!-- rule-id: IMPL-DEBT-REGISTER-SCOPE -->
- `maintenance/debt-register/<target>.jsonl` 只登记会影响未来修改、可靠性、安全、成本或 AI 行为的债务。

<!-- rule-id: IMPL-GO-MODULE-MANIFESTS -->
- `go.mod` 与 `go.sum` 必须入库。

<!-- rule-id: IMPL-GO-VULNERABILITY-SCAN -->
- Go 依赖安全扫描使用 `govulncheck ./...` 或等价 gate。

<!-- rule-id: IMPL-GO-DEPENDENCY-UPGRADE-REGEN -->
- Kratos、grpc-go、protobuf、sqlc 或 migration 工具升级后须重新生成代码。

<!-- rule-id: IMPL-GO-DEPENDENCY-UPGRADE-CHECKS -->
- 上述 Go 工具链升级后须运行 Go tests、sqlc vet/verify 与 gRPC contract tests；结果由验证项目维护。

<!-- rule-id: IMPL-BREAKING-PROTO-SEPARATE-ROUTE -->
- gRPC/protobuf breaking change 须进入技术设计的 architecture/API compatibility 与发布 gate，禁止借依赖升级顺手改变协议契约。

<!-- rule-id: IMPL-NPM-CI-COMMAND -->
- Vite/npm 项目的 CI 须使用 `npm ci`。

<!-- rule-id: IMPL-FRONTEND-MAJOR-UPGRADE-GUIDE -->
- 前端发生大版本升级时，必须先查阅官方 migration guide；这一要求适用于 Playwright、test runner、state、router、React 与 Vite。

<!-- rule-id: IMPL-UI-THEME-SEPARATE-FROM-UPGRADE -->
- UI token、Vercel Geist 风格或 dark/light 主题变化禁止混入无关依赖升级 change。

<!-- rule-id: IMPL-DEPENDABOT-ECOSYSTEM-GROUPING -->
- 自动化依赖更新缺省按 ecosystem 分组以减少 PR 噪音。

<!-- rule-id: IMPL-DEPENDENCY-PR-CONCURRENCY-LIMIT -->
- 一人执行时缺省限制同时打开的依赖 PR 数量，避免维护噪音淹没产品工作。

## 输入与产物

输入包括已经批准的产品和体验要求、适用的 `visual_ux` 判定与当前人类 review、技术设计、OpenSpec change 与 `tasks.md`、现有仓库模式、数据与权限边界、实际触发的专项工件和人工判断结果。产物包括可 review 的代码批次、配置与 flag、schema/migration/query、生成代码、前端与后端实现、AI runtime 与 job、可复现工作区命令、残余风险和交接引用。

## 完成、停止或退出条件

当实际触发表面均有对应实现、上游输入和已批准可视 UX 未被暗改、生成物来自权威源、本地能够构建或已有具体阻塞说明、高风险控制与人工 checkpoint 清楚、残余风险已移交时，实现可以进入验证。出现产品方向或契约边界变化、required UX 缺少批准或发生未复审的实质偏差、生产副作用即将发生、数据或权限边界不清，或无法保持可回滚与可审查批次时停止；不得用下游验证或发布阶段掩盖实现缺口。

## 相关项目引用

- 定义和体验设计提供产品行为、状态与用户控制；实现不得改写这些含义。
- 技术设计提供架构、API、数据、权限、AI route 与风险边界；实现只生产其技术产物。
- 计划负责拆分、顺序、状态与恢复；实现须把进度写回权威任务记录。
- 验证负责测试、评审、环境、生成一致性、迁移检查和其他证明；实现只提供命令与可验证接口。
- 发布负责 build、smoke、部署、migration 执行、开放、回滚与结果确认；实现不得执行或宣称这些动作。
- 运行负责生产观测、告警、事故、凭据轮换和恢复操作；评估负责把反馈与质量信号转成下一轮决定。
