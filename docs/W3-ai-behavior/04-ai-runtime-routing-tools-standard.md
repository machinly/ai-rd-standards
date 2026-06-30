# AI 运行时、模型路由与工具治理规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/00-main.md` 已经判断需要改变模型、供应商、route、fallback、工具运行时、外部连接器、MCP、沙箱、审批、幂等或审计时，才读取本文件。

如果当前只是判断 AI 行为应该如何定义好坏、失败和降级，先回到 `docs/W3-ai-behavior/00-main.md`。

## 目标

AI 产品的运行时风险通常同时来自两件事：模型 route 影响质量、成本、延迟和数据边界；工具 route 影响读写权限、外部副作用、审计和恢复。把它们拆成两个默认入口会让一人公司和 Agent 重复判断同一组能力边界。

本专项把模型路由、供应商选择、fallback、工具注册、权限、审批、幂等、沙箱和审计放在同一个 AI runtime 契约里，让每个用户可见 AI capability 都能回答：默认走哪条模型和工具路线，坏了怎么降级，哪些数据能发给哪个供应商，哪些工具能被调用，谁批准副作用，如何测试、审计和回滚。

默认原则：模型可以生成建议，应用运行时才拥有执行权。任何生产默认模型、供应商、fallback、reasoning effort、工具能力、connector scope 或数据边界变化，都必须有 eval gate、权限 gate、降级路径和回滚/补偿方式。

## 范围

适用对象：

- 用户可见 AI capability 的默认模型、候选模型、reasoning effort、temperature、output token、streaming、structured output、tool use、batch/flex/priority processing。
- OpenAI、Azure OpenAI、Anthropic、Google、开源模型、embedding、reranker、moderation、image/audio/realtime 模型等供应商或模型路线。
- OpenAI function tools、built-in tools、remote MCP server、本地 MCP server、自建 Go tool adapter、第三方 API connector。
- 会读取或写入用户数据、租户数据、计费权益、权限、配置、文件、代码、消息、邮件、webhook、外部系统、生产数据库或 shell/container 的工具。

不适用对象：

- W3 prompt/eval 细节；本专项只引用 eval gate，不替代 `docs/W3-ai-behavior/01-prompt-eval-agent-workflow-standard.md`。
- W2 的整体成本、供应商、客户数据和信任边界；本专项只要求 AI runtime 级别的约束并链接 W2。
- W4 的配置、feature flag、worker 和实现细节；本专项定义运行时契约，落地实现仍走 W4。
- 自建训练平台、复杂多云 AI gateway、自动模型竞价、企业 PAM/SOAR/DLP/SIEM；这些需要单独 OpenSpec change。

## 最小工件

每个有生产 AI 调用的 capability 使用同一个 `<capability>` 文件名：

```text
ai-runtime/
  route-policy/<capability>.md
  model-registry/<capability>.json
  tool-registry/<capability>.json
  permission-policy/<capability>.md
  eval-gate/<capability>.json
  fallback-runbook/<capability>.md
  runtime-review/<capability>.md
```

### `ai-runtime/route-policy/<capability>.md`

必须包含：

- `Scope`
- `Decision Matrix`
- `Default Model Route`
- `Tool / Connector Routes`
- `Fallback / Degradation`
- `Timeouts / Retries`
- `Cost / Latency`
- `Data Boundary`
- `Safety / Privacy`
- `Telemetry`
- `Human Checkpoints`
- `Linked Artifacts`

默认规则：

- 先定义任务类型，再选模型和工具：分类、结构化抽取、摘要、代码/推理、长上下文、工具代理、低延迟聊天、后台批处理要走不同 route。
- 生产 route 不允许只写 `latest`、`auto`、`default`、`best` 这类不可复盘模型名；必须记录模型族、route id、eval 日期和回滚路线。
- 用户可见核心路径要有 fallback；非核心 AI enhancement 可以 fail closed 或关闭。
- retry 必须有上限、backoff 和错误分类；有副作用工具默认不自动重试。
- 不可信输入、RAG 文档、用户上传文件、网页内容、support ticket、工具输出和 MCP 描述，不得改变 developer/system 指令或权限判断。

### `ai-runtime/model-registry/<capability>.json`

必须包含：

- `capability`
- `owner`
- `providers`
- `routes`
- `default_route`
- `budgets`
- `latency_slo`
- `quality_gate`
- `safety_gate`
- `telemetry`
- `human_checkpoint`
- `review_cadence`

每条 route 至少包含模型、供应商、数据边界、timeout、retry、max token、reasoning/tool capability、cost tier、latency target、fallback chain、eval refs、safety refs 和状态。

默认规则：

- route 的 `eval_refs` 和 `safety_refs` 必须指向 W3 prompt/eval、安全样本或内容安全工件，或说明为什么暂不适用。
- request context 必须有 deadline；provider 调用必须记录 route id、provider、model、workflow version、eval version、latency、token、cost bucket 和 fallback reason。
- 对后台、低优先级、大批量任务，优先 Batch/Flex/异步队列；对高价值低延迟路径，才考虑 priority 或更强模型。

### `ai-runtime/tool-registry/<capability>.json`

必须包含：

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

工具副作用分类：

- `read_only`：只读、无敏感数据外发、无持久化副作用。
- `write`：写入业务数据或创建内部记录。
- `destructive`：删除、覆盖、批量修改或难以恢复。
- `external_message`：发送邮件、短信、webhook、support reply、第三方通知。
- `money_movement`：退款、credit、收费、发票、额度、用量结算。
- `entitlement`：改变订阅、权限、配额、feature access。
- `admin`：后台运营、生产配置、break-glass 或支持操作。
- `code_execution`：shell、代码解释器、浏览器自动化、本地 MCP、容器或文件系统写入。

默认规则：

- 未注册工具不得进入生产 prompt、agent runtime、tool search、MCP allowlist 或 connector grant。
- `read_only` 之外的工具默认必须 `requires_approval=true`、支持 dry-run 或明确补偿方案、记录幂等键，并有审计事件。
- `destructive`、`money_movement`、`entitlement`、`admin`、`external_message`、`code_execution` 默认需要 human checkpoint。
- 工具输出一律视为不可信数据，不得被当作 system/developer instruction、权限声明或已批准状态。

### `ai-runtime/permission-policy/<capability>.md`

必须包含：

- `Scope`
- `Actors`
- `Allowed / Forbidden Actions`
- `Approval Policy`
- `Tenant Boundary`
- `Data Boundary`
- `Connector / MCP Policy`
- `Tool Output Handling`
- `Secrets`
- `Audit`
- `Linked Artifacts`

默认规则：

- 权限由服务端根据 actor、tenant、capability、tool id、scope、risk、approval id 和 data boundary 判断，不接受模型或前端声称“已授权”。
- 初始 connector/MCP scope 采用最小可用权限；需要写操作或敏感数据时再增量授权。
- token、API key、OAuth refresh token、session cookie、SSH key、数据库连接串和 OpenAI key 不进入模型上下文、工具输出、审计正文或前端日志。
- 外部工具和 MCP server 返回的文本、HTML、Markdown、JSON、代码、文件名、URL、错误消息都按不可信输入处理。

### `ai-runtime/eval-gate/<capability>.json`

必须包含：

- `capability`
- `owner`
- `baseline_route`
- `candidate_route`
- `datasets`
- `metrics`
- `thresholds`
- `tool_checks`
- `cost_latency_limits`
- `safety_checks`
- `rollout`
- `rollback`
- `evidence_refs`
- `human_checkpoint`
- `status`

默认规则：

- 默认模型、供应商、reasoning effort、工具能力、structured output schema、fallback chain、context window 或 connector scope 变化前，必须跑相关 eval。
- 至少比较 baseline 与 candidate：质量、拒答/安全、schema 成功率、tool call 成功率、p95 latency、token/cost、超时率、fallback 触发率。
- 有副作用工具必须覆盖 dry-run、approval、幂等、rollback/compensation、重复提交、权限拒绝、租户拒绝和审计断言。
- rollout 默认 staged：local eval、shadow 或 small cohort、监控、扩大、保留 rollback route。

### `ai-runtime/fallback-runbook/<capability>.md`

必须包含：

- `Scope`
- `Failure Modes`
- `Detection Signals`
- `Immediate Actions`
- `Degradation Modes`
- `Rollback / Compensation`
- `User Messaging`
- `Provider / Connector Escalation`
- `Recovery Check`
- `Post-Incident Review`
- `Linked Artifacts`

默认规则：

- failure modes 至少覆盖：rate limit、timeout、provider 5xx/503、模型输出不合 schema、tool call 失败、approval 失败、安全拒绝、成本阈值、延迟超 SLO、供应商或 connector 状态异常。
- degradation modes 默认从低风险开始：减少输出 token、降低检索数量、切小模型、关闭工具、转异步、使用缓存、只返回可验证来源、人工处理。
- 出现 prompt injection、越权参数、跨租户、敏感数据外发、成本异常、循环调用、sandbox escape 或 connector 异常时，立即禁用相关 tool/route 或 kill switch。
- 用户提示要诚实但短：说明功能暂时降级、可重试或已转入后台，不暴露供应商内部错误和敏感路由细节。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端使用显式 `AIRuntime`、`ModelRouter`、`ToolRegistry` 或等价 usecase，输入 capability、task type、actor、tenant、risk tier、latency class、budget class、required tools 和 data boundary，输出 route id、request options 和 allowed tool set。
- 不在业务代码散落硬编码 model name、provider URL、timeout、max token、reasoning effort、temperature、tool allowlist 或 connector scope。
- Provider adapter 和 tool adapter 暴露稳定内部接口，不把供应商 SDK 类型、access token 或 raw tool output 泄漏到业务层。
- gRPC error model 必须区分：用户输入错误、权限错误、budget/capacity 限制、供应商暂时不可用、schema/parse 失败、安全拒绝、approval required、tool denied 和内部错误。
- 自动 retry 只用于无副作用、可幂等、瞬时错误；工具调用、支付、写数据、发通知、权限变更前后都不得由模型 route 层盲目重试。

## Vite 前端默认规则

- 用户可见 AI 能力降级时，界面应提供简短状态：生成较慢、功能暂时受限、已转后台、可重试或已使用基础模式。
- 高成本/慢速模式使用明确按钮或切换；不要把“更贵更慢的模型”藏成默认体验。
- 工具授权和确认 UI 必须显示动作名、目标、影响、权限 scope、dry-run、批准状态、撤销/补偿和风险。
- 高风险确认不能只写“确定吗”；必须显示工具名、目标对象、数量/金额/外部收件人/权限变化和不可逆后果。
- 对工具失败、等待批准、降级、取消、rollback/compensation、rate limit 和 kill switch 状态提供明确界面。

## AI workflow 默认规则

- Prompt builder 必须读取 route id、route policy 和 allowed tool set，不允许 prompt 自己决定供应商、权限、审批、幂等、租户边界、成本上限或重试策略。
- 结构化输出优先使用 schema；不同模型的 schema adherence 需在 eval gate 中单独记录。
- 工具路由必须与 auth、tenant boundary、admin action guard 和 red-team 工件相连；模型更换不得扩大工具权限。
- autonomous loop 默认有限步数、有限工具 fanout、有限 token/cost、有限重试；超限后降级为说明、转人工或排队任务。
- 新工具、新 connector、新写权限、新代码执行能力或工具自治等级提升前，必须跑 W3 相关 eval 或对抗样本。

## 需要人判断的关键点

只把这些判断交给人：

- 是否改变用户可见生产默认模型、供应商或 route。
- 是否引入新的外部模型供应商、connector、MCP server、本地 MCP server、代码执行工具或浏览器/电脑控制工具。
- 是否让 sensitive/regulatory/high-impact 数据进入某条 route，或扩大供应商/connector 的数据保留、驻留、训练或 scope 边界。
- 是否改变 refusal/safety behavior、moderation route、安全阈值、tool-heavy route 或 agent 自治等级。
- 是否允许 AI 调用写操作、删除、退款/credit、权益/权限、外部通知、生产配置、后台操作或跨租户工具。
- 是否接受没有 fallback、dry-run、rollback/compensation、幂等、审计或测试的用户可见 AI 能力。
- 是否提高预算、取消硬限制、扩大 context window、默认高 reasoning effort、扩大 loop/fanout/retry/budget 或关闭 kill switch。

其他字段完整性、章节、JSON 枚举、schema 引用、route 引用、human checkpoint 覆盖、敏感内容扫描、OpenSpec linkage、eval fixture 和基础验证由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：七个工件分别回答“怎么路由模型、有哪些模型、有哪些工具、谁能用、怎么验证、坏了怎么办、怎么复盘”。
- 保留：人只判断默认模型/供应商、新 connector/MCP、敏感数据、高权限工具、高成本默认、无 fallback/无 dry-run/无审计例外和自治等级提升。
- 调整：不要求完整 AI gateway、agent platform 或企业审批系统；先用 route policy、registry、eval gate、approval id、审计和 kill switch。
- 风险：合并后单个专项更宽。缓解：只有 AI runtime 边界变化才读；普通 prompt/eval 仍回到 W3 主入口和 prompt/eval 专项。

结论：可落地。一个人可以先为最重要 AI capability 建一个小 AI runtime 契约，再用 eval gate 和 permission gate 控制模型升级与工具副作用。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户不会被模型故障、工具副作用或降级吓到；核心体验有明确 fallback、确认和文案。
- 工程角度：model name、provider、timeout、retry、tool schema、权限、幂等、审计和错误模型进入结构化运行时，不散落在 prompt 和前端按钮里。
- 运维角度：rate limit、timeout、5xx、schema 失败、tool failure、approval failure、kill switch 和 incident action 都有检测与动作。
- 安全隐私角度：覆盖供应商数据边界、prompt injection、tool output injection、MCP scope、secret 泄漏、sandbox 和跨租户风险。
- 成本角度：限制强模型默认、context window、token、loop、fanout、工具调用、第三方 API、代码执行和重试。

结论：可落地。本专项把“模型怎么跑”和“工具怎么执行”压成同一个可审查运行时契约：模型建议，应用执行，权限最小，副作用可见，失败可停。
