# AI 工具运行时、外部连接器与沙箱治理规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/00-main.md` 已经判断需要 AI 工具运行时、外部连接器、MCP、沙箱、审批、幂等或审计时，才读取本文件。

如果当前只是判断 AI 行为应该如何定义好坏、失败和降级，先回到 `docs/W3-ai-behavior/00-main.md`。

## 目标

AI 产品真正危险的时刻，不是模型说错一句话，而是模型输出被拿去调用工具：读内部数据、写数据库、发邮件、改权限、触发退款、执行代码、访问 MCP server 或连接第三方 API。本专项定义 AI 工具运行时、外部连接器与沙箱治理规范，让每个 AI capability 都能回答：模型能看到哪些工具，谁批准了调用，工具参数从哪里来，哪些动作有副作用，如何 dry-run，如何幂等和回滚，工具输出是否可信，失败时怎样停止而不是重试到失控。

默认原则：模型可以建议工具调用，执行权属于应用运行时。任何会写数据、花钱、发消息、改变权限、跨租户、读敏感数据、执行代码或访问外部连接器的工具，都必须有显式注册、最小权限、审批、审计、限流、测试和回滚/补偿路径。

## 核心依据

- 《人月神话》：没有一个“强模型 + 全量工具”能消除软件复杂度；概念完整性来自清晰边界、接口和变更控制。
- 小型项目管理：一人公司不能维护大型 agent platform；先保留能防止高损失动作和恢复上下文的五个小工件。
- Saltzer & Schroeder：采用 least privilege、fail-safe defaults、complete mediation 和 economy of mechanism；每次工具调用都要重新校验，而不是信任一次性上下文。
- OpenAI Function Calling / Tools：工具调用是多步流程，模型给出 tool call，应用侧执行代码并把结果再交回模型；函数工具应使用 schema，严格模式能提升参数约束。
- OpenAI Agents SDK / MCP Connectors：当应用拥有编排、工具执行、审批和状态时才使用 agent runtime；远程 MCP/connector 默认应审批并记录要发送的数据。
- OpenAI Safety Best Practices / Developer Mode：高风险输出和代码/工具结果需要 human review；带读写 MCP 能力的开发者模式强大但危险，要防提示注入、错误写操作和恶意 MCP。
- OpenAI Data Controls：远程 MCP server 是第三方服务，发给它的数据受其数据保留和驻留政策约束。
- Model Context Protocol Security Best Practices：MCP 实现要处理 confused deputy、token passthrough、SSRF、session hijacking、本地 MCP server compromise 和 scope minimization。
- OWASP LLM Top 10：prompt injection、insecure output handling、insecure plugin/tool design、excessive agency、sensitive disclosure 和 unbounded consumption 都会在工具调用场景被放大。
- Google SRE Handling Overload / Cascading Failures：工具 fanout、自动重试和无限 agent loop 会制造过载和级联故障；必须有限流、退避、降级、拒绝和恢复。
- Vercel/Geist 设计参考：高风险工具确认 UI 应克制、清晰、可扫描，避免用装饰或模糊文案掩盖动作、目标和后果。

## 范围

适用对象：

- 用户可见 AI chat、agent、RAG、客服助手、后台 operator、代码助手、数据分析助手、自动化 workflow 中的工具调用。
- OpenAI function tools、built-in tools、tool search、remote MCP server、OpenAI managed connector、本地 MCP server、自建 Go tool adapter、第三方 API connector。
- 会读取或写入用户数据、租户数据、计费权益、权限、配置、文件、代码、消息、邮件、webhook、外部系统、生产数据库或 shell/container 的工具。
- Go/Kratos/gRPC 后端中的 tool registry、permission check、approval、idempotency、rate limit、audit、sandbox 和 connector grant。
- Vite 前端中的工具授权、dry-run diff、二次确认、撤销/补偿说明、连接器授权和降级状态。

不适用对象：

- 纯本地、无外部输入、无生产数据、无网络、无持久化副作用的实验脚本；但一旦进入产品 workflow，仍需登记。
- 已由 W7 完全覆盖的人工 admin action；如果该动作被 AI 调用或建议，本专项仍要求 tool runtime gate。
- 企业级 PAM、SOAR、DLP、SIEM、完整沙箱平台或通用零信任平台；需要时单独开企业安全 change。

## 最小工件

每个可生产调用工具的 AI capability 使用同一个 `<capability>` 文件名：

```text
ai-tools/
  tool-registry/<capability>.json
  permission-policy/<capability>.md
  execution-runbook/<capability>.md
  tool-test-plan/<capability>.json
  tool-review/<capability>.md
```

### `ai-tools/tool-registry/<capability>.json`

工具注册表必须包含：

- `capability`
- `owner`
- `tools`
- `connectors`
- `side_effect_classes`
- `auth`
- `rate_limits`
- `budgets`
- `telemetry`
- `human_checkpoint`
- `review_cadence`

`tools` 每项至少包含：

- `id`
- `name`
- `schema_ref`
- `purpose`
- `side_effect_class`
- `actor_scope`
- `tenant_scope`
- `data_access`
- `requires_approval`
- `supports_dry_run`
- `supports_rollback`
- `idempotency`
- `timeout_ms`
- `retry_policy`
- `rate_limit`
- `audit_events`
- `output_handling`
- `status`

默认副作用分类：

- `read_only`：只读、无敏感数据外发、无持久化副作用。
- `write`：写入业务数据或创建内部记录。
- `destructive`：删除、覆盖、批量修改或难以恢复。
- `external_message`：发送邮件、短信、webhook、support reply、第三方通知。
- `money_movement`：退款、credit、收费、发票、额度、用量结算。
- `entitlement`：改变订阅、权限、配额、feature access。
- `admin`：后台运营、生产配置、break-glass 或支持操作。
- `code_execution`：shell、代码解释器、浏览器自动化、本地 MCP、容器或文件系统写入。

默认：

- 未注册工具不得进入生产 prompt、agent runtime、tool search、MCP allowlist 或 connector grant。
- `read_only` 之外的工具默认必须 `requires_approval=true`、支持 dry-run 或明确补偿方案、记录幂等键，并有审计事件。
- `destructive`、`money_movement`、`entitlement`、`admin`、`external_message`、`code_execution` 默认需要 human checkpoint。
- 工具输出一律视为不可信数据，不得被当作 system/developer instruction、权限声明或已批准状态。
- 不对有副作用工具做盲目自动重试；重试必须基于幂等键、错误分类和 retry budget。

### `ai-tools/permission-policy/<capability>.md`

权限策略必须包含：

- `Scope`
- `Actors`
- `Tool Classes`
- `Allowed Actions`
- `Forbidden Actions`
- `Approval Policy`
- `Tenant Boundary`
- `Data Boundary`
- `Connector / MCP Policy`
- `Tool Output Handling`
- `Secrets`
- `Linked Artifacts`

默认：

- 权限由服务端根据 actor、tenant、capability、tool id、scope、risk、approval id 和 data boundary 判断，不接受模型或前端声称“已授权”。
- 初始 connector/MCP scope 采用最小可用权限；需要写操作或敏感数据时再增量授权。
- token、API key、OAuth refresh token、session cookie、SSH key、数据库连接串和 OpenAI key 不进入模型上下文、工具输出、审计正文或前端日志。
- 外部工具和 MCP server 返回的文本、HTML、Markdown、JSON、代码、文件名、URL、错误消息都按不可信输入处理。

### `ai-tools/execution-runbook/<capability>.md`

执行 runbook 必须包含：

- `Scope`
- `Preflight`
- `Dry Run`
- `Approval`
- `Execution`
- `Idempotency / Retry`
- `Timeout / Rate Limit`
- `Rollback / Compensation`
- `Audit`
- `Degradation / Kill Switch`
- `Incident Actions`
- `Linked Artifacts`

默认执行顺序：

1. 校验 tool id、schema version、actor、tenant、permission、data boundary、budget 和 rate limit。
2. 对非只读工具先 dry-run 或生成影响摘要：目标对象、租户、数量、金额、外部收件人、文件路径、权限变化和不可逆后果。
3. 需要批准时，批准对象必须包含工具名、参数摘要、目标、风险级别、dry-run 结果和有效期。
4. 执行时绑定 request id、tool run id、approval id、idempotency key、deadline 和 retry budget。
5. 成功后记录审计、用户可见状态和可验证结果；失败后按错误分类停止、补偿、降级或转人工。
6. 出现 prompt injection、越权参数、跨租户、敏感数据外发、成本异常、循环调用、sandbox escape 或 connector 异常时，立即禁用相关 tool/route 或 kill switch。

### `ai-tools/tool-test-plan/<capability>.json`

工具测试计划必须包含：

- `capability`
- `owner`
- `environments`
- `cases`
- `required_checks`
- `evidence_refs`
- `human_checkpoint`
- `status`

`required_checks` 默认至少覆盖：

- `schema_validation`
- `auth_denial`
- `tenant_denial`
- `approval_required`
- `dry_run`
- `idempotency`
- `rollback_or_compensation`
- `timeout`
- `rate_limit`
- `prompt_injection_tool_args`
- `tool_output_untrusted`
- `audit_event`
- `cost_limit`

默认：

- 每个工具至少有成功路径、权限拒绝、租户拒绝、schema 错误、超时/限流、工具输出注入和审计断言。
- 有副作用工具必须覆盖 dry-run、approval、幂等、rollback/compensation 和重复提交。
- 外部 connector/MCP 必须覆盖 scope 最小化、连接失败、第三方错误、数据外发摘要和撤销授权。

### `ai-tools/tool-review/<capability>.md`

工具复盘必须包含：

- `Recent Changes`
- `Tool Calls / Denials`
- `Approval Quality`
- `Injection / Output Risks`
- `Side Effects / Rollback`
- `Cost / Rate Limits`
- `Connector / MCP Grants`
- `Incidents`
- `Open Risks`
- `Next One Change`

默认：

- pre-revenue 或低流量：每月复盘一次，或任何新写工具/新 connector 上线前复盘。
- 有活跃用户：每两周复盘一次，或事故、越权拒绝、成本异常、第三方权限变化、MCP server 变更后复盘。
- 每次只选一个最高影响改进：收紧 scope、补 dry-run、补幂等、删除危险工具、加强审计、改确认 UI、增加 kill switch 或降低自治级别。

## Go / Kratos / sqlc / gRPC 默认规则

- 工具运行时必须是显式后端能力，不由前端或 prompt 直接拼接第三方 API、SQL、shell 或内部 admin endpoint。
- Go/Kratos middleware 必须在每次工具调用前校验 actor、tenant、capability、tool id、permission、approval、budget、rate limit、idempotency key 和 deadline。
- gRPC metadata 传播 `actor_id`、`tenant_id`、`request_id`、`tool_run_id`、`approval_id`、`idempotency_key`、`capability` 和 `risk_class`；服务端重新计算授权。
- Protobuf 定义工具调用请求/响应、dry-run 结果、approval request、tool run status 和错误模型；浏览器用 HTTP/BFF 时也不得绕过 gRPC usecase。
- sqlc 表默认包含：`ai_tool_definitions`、`ai_tool_runs`、`ai_tool_approvals`、`ai_tool_audit_events`、`ai_connector_grants`、`ai_tool_idempotency_keys`、`ai_tool_denials`。
- 外部 MCP/connector adapter 暴露稳定内部接口，不把供应商 SDK 类型、access token 或 raw tool output 泄漏到业务层。
- sandbox/code execution 工具默认网络、文件系统、环境变量、进程、时间、CPU、内存和输出大小受限；敏感目录和 secret 默认不可读。

## Vite 前端默认规则

- 工具授权和确认 UI 是工作台，不是营销页：动作名、目标、影响、权限 scope、dry-run、批准状态、撤销/补偿和风险必须清楚可扫描。
- 高风险确认不能只写“确定吗”；必须显示工具名、目标对象、数量/金额/外部收件人/权限变化和不可逆后果。
- 用户授权 connector/MCP 时要显示要发送的数据摘要、第三方名称、scope、有效期、撤销入口和数据边界。
- 对工具失败、等待批准、降级、取消、rollback/compensation、rate limit 和 kill switch 状态提供明确界面。
- 避免暗色/浅色主题中危险状态只靠颜色表达；使用明确文案、焦点可见、键盘可达和可读错误。

## AI workflow 默认规则

- Prompt 只能请求工具；不能自己决定权限、审批、幂等、租户边界、成本上限或重试策略。
- 生产工具 schema 使用严格结构，参数必须在服务端校验、规范化和最小化；不把用户输入原文无过滤地转成高权限参数。
- RAG 文档、网页、邮件、support ticket、工具输出和 MCP 描述都视为不可信上下文，不得覆盖系统策略或打开新工具。
- autonomous loop 默认有限步数、有限工具 fanout、有限 token/cost、有限重试；超限后降级为说明、转人工或排队任务。
- 新工具、新 connector、新写权限、新代码执行能力或工具自治等级提升前，必须跑 W3 相关 eval 或对抗样本。

## 需要人判断的关键点

只把这些判断交给人：

- 是否引入新的外部 connector、MCP server、本地 MCP server、代码执行工具或浏览器/电脑控制工具。
- 是否允许 AI 调用写操作、删除、退款/credit、权益/权限、外部通知、生产配置、后台操作或跨租户工具。
- 是否接受没有 dry-run、没有 rollback/compensation、没有幂等、没有审计或没有测试的有副作用工具。
- 是否扩大 OAuth/API scope、把敏感数据发给第三方、改变数据保留/驻留边界或使用供应商托管 connector。
- 是否让工具输出进入 SQL、shell、HTML、Markdown、email、webhook、代码执行或另一个高权限工具。
- 是否提高 agent 自治等级、扩大 loop/fanout/retry/budget、关闭 kill switch 或绕过审批。
- 是否处理 prompt injection、tool output injection、sandbox escape、越权拒绝、异常成本或第三方 connector incident。

其他字段完整性、章节、JSON 枚举、schema 引用、human checkpoint 覆盖、敏感内容扫描、OpenSpec linkage、positive/negative fixture 和基础验证由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“有哪些工具、谁能用、怎么执行、怎么测、怎么复盘”。
- 保留：人只判断新 connector/MCP、写/删/钱/权限/外部通知/代码执行、敏感数据外发、无 dry-run/回滚/幂等/审计的例外和自治等级提升。
- 调整：不要求完整 agent platform 或企业审批系统；先用注册表、服务端 gate、approval id、审计和 kill switch。
- 调整：只读低风险工具不强制每次人工审批，但仍要限流、租户校验、输出不可信和审计。
- 风险：工具登记可能变成文档负担。缓解：只登记生产可被 AI 调用的工具；纯内部手工动作继续走 W7 后台运营动作。

结论：可落地。一个人可以先为最重要 AI capability 列出 3 到 8 个真实工具，把所有有副作用的工具改成 dry-run + approval + audit，再逐步补齐 sandbox 和 connector scope。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户能看清 AI 即将做什么、影响谁、能否撤销，减少“AI 悄悄替我做了事”的信任损失。
- 工程角度：工具 schema、权限、幂等、审计和错误模型进入 Go/Kratos/sqlc/gRPC 结构，不散落在 prompt 和前端按钮里。
- 运维角度：timeout、rate limit、retry budget、kill switch、降级和 incident action 防止工具循环导致级联故障。
- 安全隐私角度：覆盖 prompt injection、tool output injection、MCP scope、第三方数据边界、secret 泄漏、sandbox 和跨租户风险。
- 成本角度：限制 loop、fanout、工具调用、第三方 API、代码执行和重试，避免 agent 把账单或外部副作用放大。

结论：可落地。本专项把“agent 能调用工具”压成一个可审查的运行时契约：模型建议，应用执行，权限最小，副作用可见，失败可停。
