# ai-tool-runtime-standard 规格

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

Define the minimum one-person-company governance for AI tool execution, external connectors, MCP servers, sandbox/code execution, approvals, idempotency, retry limits, audit trails, tool output trust, and recovery paths.

## Requirements

### Requirement: 生产 AI 工具 capability 必须定义 ai-tools artifacts

Any production AI capability that can call tools, external connectors, MCP servers, third-party APIs, local MCP, code execution, browser/computer-use, or backend actions MUST define AI tool runtime artifacts.

#### Scenario: 新工具能力准备进入生产

- GIVEN 一个 AI capability 能调用只读、写入、删除、外部通知、计费、权限、后台、代码执行、MCP 或第三方 API 工具
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `ai-tools/tool-registry/<capability>.json`
- AND 创建 `ai-tools/permission-policy/<capability>.md`
- AND 创建 `ai-tools/execution-runbook/<capability>.md`
- AND 创建 `ai-tools/tool-test-plan/<capability>.json`
- AND 创建 `ai-tools/tool-review/<capability>.md`

### Requirement: Tool registry 必须定义工具、连接器、副作用、权限、预算、遥测和人工 checkpoint

Tool registry MUST record capability、owner、tools、connectors、side effect classes、auth、rate limits、budgets、telemetry、human checkpoint 和 review cadence.

#### Scenario: Reviewer 判断工具是否可进入运行时

- GIVEN reviewer 打开 `ai-tools/tool-registry/<capability>.json`
- WHEN 需要理解模型可调用哪些工具
- THEN 每个 tool 包含 id、name、schema_ref、purpose、side_effect_class、actor_scope、tenant_scope、data_access、requires_approval、supports_dry_run、supports_rollback、idempotency、timeout_ms、retry_policy、rate_limit、audit_events、output_handling 和 status
- AND `side_effect_class` 使用 `read_only`、`write`、`destructive`、`external_message`、`money_movement`、`entitlement`、`admin` 或 `code_execution`
- AND 非 `read_only` 工具必须有 approval、dry-run 或补偿路径、幂等和审计

### Requirement: Permission policy 必须定义 actor、工具类别、允许/禁止动作、审批、租户、数据、连接器、工具输出和 secret 边界

Permission policy MUST record scope、actors、tool classes、allowed actions、forbidden actions、approval policy、tenant boundary、data boundary、connector/MCP policy、tool output handling、secrets 和 linked artifacts.

#### Scenario: 服务端判断一次工具调用是否允许

- GIVEN 模型请求调用某个工具
- WHEN 后端执行 permission check
- THEN 服务端基于 actor、tenant、capability、tool id、scope、risk、approval id 和 data boundary 重新判断权限
- AND 不信任模型、前端、MCP server 或工具输出声称的授权状态
- AND secret、token、cookie、私钥和连接串不得进入模型上下文、工具输出、审计正文或前端日志

### Requirement: Execution runbook 必须定义 preflight、dry-run、approval、execution、idempotency、retry、timeout、rollback、audit、degradation 和 incident actions

Execution runbook MUST record preflight、dry-run、approval、execution、idempotency/retry、timeout/rate limit、rollback/compensation、audit、degradation/kill switch、incident actions 和 linked artifacts.

#### Scenario: 有副作用工具被调用

- GIVEN tool registry 标记工具存在副作用
- WHEN AI workflow 请求执行该工具
- THEN 后端先校验 tool id、schema version、actor、tenant、permission、budget、rate limit、approval 和 idempotency key
- AND 执行前产生 dry-run 或影响摘要
- AND 执行时绑定 request id、tool run id、approval id、deadline 和 retry budget
- AND 失败时按错误分类停止、补偿、降级、转人工或触发 kill switch

### Requirement: Tool test plan 必须覆盖 schema、auth、tenant、approval、dry-run、idempotency、rollback、timeout、rate limit、prompt injection、tool output、audit 和 cost

Tool test plan MUST record capability、owner、environments、cases、required checks、evidence refs、human checkpoint 和 status.

#### Scenario: 发布前验证工具运行时

- GIVEN AI tool capability 准备发布
- WHEN 读取 `ai-tools/tool-test-plan/<capability>.json`
- THEN `required_checks` 至少包含 `schema_validation`、`auth_denial`、`tenant_denial`、`approval_required`、`dry_run`、`idempotency`、`rollback_or_compensation`、`timeout`、`rate_limit`、`prompt_injection_tool_args`、`tool_output_untrusted`、`audit_event` 和 `cost_limit`
- AND 每个有副作用工具覆盖 dry-run、approval、幂等、rollback/compensation 和重复提交
- AND 外部 connector 或 MCP 工具覆盖 scope 最小化、连接失败、第三方错误、数据外发摘要和撤销授权

### Requirement: Tool review 必须复盘工具调用、拒绝、审批质量、注入风险、副作用、成本、连接器和下一项改进

Tool review MUST record recent changes、tool calls/denials、approval quality、injection/output risks、side effects/rollback、cost/rate limits、connector/MCP grants、incidents、open risks 和 next one change.

#### Scenario: 周期性复查 AI 工具运行时

- GIVEN capability 有近期工具、connector、MCP、schema、权限、prompt、model route 或 sandbox 变更
- WHEN 更新 `ai-tools/tool-review/<capability>.md`
- THEN 记录近期工具调用和拒绝、审批质量、注入/输出风险、副作用与回滚、成本/限流、connector/MCP grant、事故和开放风险
- AND 只选择一个最高影响的 next one change

### Requirement: 高风险工具、连接器、沙箱和自治变更必须人工 checkpoint

New connectors/MCP servers, write/destructive/money/entitlement/admin/external-message/code-execution tools, sensitive third-party data sharing, missing dry-run/rollback/idempotency/audit/tests, tool-output-to-execution paths, autonomy expansion, and tool incidents MUST have human checkpoint coverage.

#### Scenario: Tool runtime 触发高风险条件

- GIVEN registry、permission policy、runbook、test plan、review 或 release 触发高风险条件
- WHEN 准备发布或接受例外
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、阻塞或降级状态

### Requirement: AI tool artifacts 不得保存敏感内容

AI tool runtime artifacts MUST NOT store secrets, production tokens, API keys, OAuth refresh tokens, private keys, session cookies, database connection strings, payment data, raw prompts, raw responses, raw tool outputs, unredacted personal data, connector credentials, or executable attack payloads.

#### Scenario: 记录工具参数、输出、事故或测试证据

- GIVEN 需要保存 tool run、connector consent、prompt-injection case、sandbox incident、approval evidence 或 third-party error
- WHEN 写入 `ai-tools/` artifacts
- THEN 使用 synthetic example、redacted summary、trace id、request id、tool run id、hash、finding id 或 controlled attachment reference
- AND 不保存 secret、生产 token、API key、OAuth refresh token、私钥、session cookie、数据库连接串、支付数据、完整 raw prompt/response/tool output、未脱敏个人数据、connector credential 或可直接执行的攻击 payload
