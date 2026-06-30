# W4 Build 核心规范

## W4 核心入口

本文件是 W4 Build 的核心入口。进入 `docs/W4-build/` 时先读它，再按触发条件读取后端、前端、数据、配置、异步任务、集成、计费、通知或开发者体验专项。

W4 只回答一个问题：**如何把 W2 已定义的行为、边界和风险，以及 W3 已定义的 AI 行为，落成可运行、可验证、可交付的系统构件？**

W4 不是重新决定产品方向、风险边界或上线许可的地方。发现 scope、契约、安全、成本、AI 行为或用户承诺变化时，先回退到 W2 或 W3。

## 适用范围

适用：

- Go/Kratos/sqlc/gRPC 服务、Vite 前端、API/BFF、数据库迁移、配置和 Feature Flag。
- AI coding 会话、生成代码、prompt/tool/eval 相关实现、后台 worker、异步 job、RAG 入库或批处理。
- 计费、权益、用量、webhook、事件、通知、开发者 API 文档、SDK 示例等会进入产品运行面的构件。
- 本地开发环境、命令目录、seed/fixtures、one-step verify、实现批次日志。

不适用：

- “要不要做”和优先级判断，回到 `docs/W0-intake/00-main.md`。
- 用户问题、成功指标、实验设计，回到 `docs/W1-discovery/00-main.md`。
- OpenSpec、架构、契约、安全、成本、权限、供应商和信任边界，回到 `docs/W2-openspec-risk/00-main.md`。
- AI 行为定义、eval、红队、模型路由、工具权限、RAG 来源和记忆策略，回到 `docs/W3-ai-behavior/00-main.md`。
- 上线前验收、性能、可访问性、韧性和安全门禁，进入 W5。

## W4 最小产出

每个 W4 工作至少留下这些产出：

- 已链接的 OpenSpec change，或明确说明该实现不需要 change。
- 可 review 的实现批次：代码、迁移、配置、前端状态、worker、集成或文档构件。
- 本地可运行命令和最小验证结果，例如 build、test、generate、sqlc、preview、smoke、eval fixture。
- 对 W5 有用的证据：测试输出、失败项、人工接受风险、残余风险、需要补测的路径。
- 如果触发财务、权限、外部副作用、用户触达、开发者 API 或后台任务，必须有对应专项的最小工件或明确不适用理由。

最小产出不等于“所有专项都写一遍”。只为真实触发的实现面补工件。

## 人工判断点

默认不把包名、文件拆分、普通 CRUD 分层、局部 CSS、低风险 copy、命令目录顺序交给人判断。Codex 或工程实现者按本仓库默认规范推进。

必须人工判断：

- 是否改变用户可见行为、公共 API、错误语义、权限、租户、计费、套餐、通知或外部承诺。
- 是否执行不可逆 migration、DROP/TRUNCATE、批量生产数据修复、真实生产 backfill 或真实外部副作用。
- 是否新增长期依赖、队列、事件 broker、支付/通知/开发者平台供应商、模型供应商或付费工具链。
- 是否允许生产配置、Feature Flag、kill switch、AI route 或高成本能力在运行时切换。
- 是否让 AI agent 执行有副作用命令、访问真实数据、调用真实供应商、删除/跳过失败测试或扩大自主权限。
- 是否接受没有本地验证、没有幂等、没有回滚、没有取消/重试上限或没有 W5 门禁证据的实现进入下一步。

## 触发型专项

只在触发条件出现时读取对应文件：

- Go/Kratos/sqlc/gRPC 服务、proto、repository、service 层或后端质量门禁：`docs/W4-build/01-go-kratos-sqlc-grpc-service-standard.md`
- Vite、React/TypeScript、前端状态、设计 token、可访问交互或 preview：`docs/W4-build/02-vite-vercel-frontend-standard.md`
- schema、migration、sqlc、backfill、数据修复、备份/恢复前置检查：`docs/W4-build/03-data-migration-standard.md`
- 配置、环境变量、Feature Flag、kill switch、AI route/runtime change：`docs/W4-build/04-configuration-feature-flag-standard.md`
- 本地命令、工具链、devcontainer/compose、seed fixtures、one-step verify：`docs/W4-build/05-dev-workspace-automation-standard.md`
- AI 协作编码、变更批次、自审、verification JSON、agent stop condition：`docs/W4-build/06-ai-coding-workflow-standard.md`
- 付费、套餐、权益、用量计量、Stripe、账本、对账：`docs/W4-build/07-billing-entitlement-metering-standard.md`
- 异步 job、worker、队列、Batch/background、取消、重试、死信：`docs/W4-build/08-async-job-worker-standard.md`
- 入站 webhook、出站事件、inbox/outbox、验签、重放和集成 schema：`docs/W4-build/09-event-webhook-integration-standard.md`
- 邮件、SMS、push、通知模板、退订、偏好、送达事件：`docs/W4-build/10-user-notification-messaging-standard.md`
- 对外 API 文档、SDK、示例、developer changelog、文档站：`docs/W4-build/11-developer-experience-api-docs-sdk-standard.md`

如果一个实现同时触发多个专项，先读最靠近副作用边界的专项。例如支付 webhook 同时读计费和事件；AI 长任务同时读异步 job 和 W3 相关专项。

## 进入 W5 的出口

满足以下条件后，W4 才能进入 W5：

- W2/W3 的输入没有被实现过程悄悄改变；若改变，已回退更新。
- 触发的 W4 专项已产出最小工件，或记录了为什么不适用。
- 本地实现能构建或至少给出无法运行的具体原因。
- migration、config、flag、worker、webhook、billing、notification 等高风险面已有 rollback、幂等、限流、审计或人工 checkpoint 说明。
- AI coding 变更有小批次记录、自审和验证命令结果。
- 残余风险已经写给 W5，而不是藏在实现说明里。

出口选择：

- 证据不足、测试缺口或安全/性能/UX 风险未验证：进入 W5。
- 需要发布、客户上线、公开承诺或 rollback 计划：W5 通过后进入 W6。
- 需要线上观测、告警、runbook、事故或凭据轮换：进入 W7。
- 用户反馈、质量回归、支持信号改变了下一步：进入 W8，再回到 W0/W1。

## 回退规则

- 产品目标、成功指标或用户问题变化：回到 W1。
- 工作不再值得做或超过 appetite：回到 W0。
- API、架构、权限、安全、成本、数据边界、供应商或信任承诺变化：回到 W2。
- Prompt、eval、模型、工具、RAG、记忆或 AI 安全行为变化：回到 W3。
- 验证失败但实现方向仍对：留在 W4 修复或进入 W5 做门禁判断。
