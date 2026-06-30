# W7 Operate 触发专项：观测性、遥测与 AI Trace 规范

## W7 触发定位

本文件是 W7 Operate 的触发型专项，不是 W7 主入口。只有当当前工作涉及 metrics、traces、logs、dashboard、OpenTelemetry、trace correlation、AI telemetry、低基数 schema 或遥测隐私/成本边界时，才需要读取本文件。

普通 W7 运行入口应先回到 `docs/W7-operate/00-main.md`，由主入口判断是否触发本专项。

## 目标

SLO 和 runbook 告诉我们“什么时候该响应”，但代码本身必须先发出可用信号。本专项定义 Go/Kratos/gRPC/sqlc、Vite 前端和 AI workflow 的最小遥测标准，让一人公司在事故、成本异常、AI 行为漂移和用户体验变差时能快速定位，而不是靠回忆和翻日志碰运气。

默认原则：先发少量高价值信号，再扩展 dashboard。metrics 用于健康和趋势，traces 用于定位路径，logs 用于解释具体事件，AI traces 用于理解模型、工具和 guardrail 行为。

## 核心依据

- 《人月神话》：没有银弹。观测性不能弥补混乱设计，但能降低复杂系统中的理解成本。
- 小型项目管理：只采集会支持决策、排障、成本控制和安全审计的信号，不做“为了 dashboard 而 dashboard”。
- Google SRE Monitoring Distributed Systems / Workbook Monitoring：优先关注用户症状和四个黄金信号：latency、traffic、errors、saturation。
- Observability Engineering：可调试性来自高基数上下文、事件关联和快速提问能力，但必须控制成本和隐私。
- OpenTelemetry：vendor-neutral 标准，覆盖 traces、metrics、logs、baggage 和 semantic conventions。
- W3C Trace Context：跨服务传播 trace context，使请求能被端到端关联。
- Prometheus naming：metric 名称和 label 要一致，避免无界高基数 label。
- OpenTelemetry Go / JavaScript：Go 和浏览器/Node 都可以用 OTel SDK/API 发出 traces、metrics、logs。
- OpenTelemetry semantic conventions：HTTP、RPC、DB、messaging、events 和 GenAI 等领域应使用统一属性。
- OpenAI Agents tracing：agent run 应记录模型调用、工具调用、handoff、guardrail 和自定义 spans。

## 范围

适用对象：

- Go/Kratos/gRPC 服务、HTTP endpoint、background worker。
- sqlc/PostgreSQL 数据访问、外部供应商调用、queue/webhook。
- Vite 前端关键用户路径、Web Vitals、API 调用、错误边界。
- AI prompt、model call、tool call、agent workflow、eval、guardrail、cost。
- W7 SLO、W6 release、W2 cost/security、W1 product metrics 和 W5 quality gates 需要的信号。

不适用对象：

- 不进入生产的一次性脚本，除非会访问生产数据或真实供应商。
- 本地实验日志，前提是不处理用户数据、不调用真实模型或生产依赖。
- 个人敏感数据本身。观测性只记录必要上下文，不记录原始 prompt、secret、PII 或完整业务内容。

## 最小工件

每个生产服务、前端应用或 AI workflow 使用同一个 `<target>` 文件名：

```text
observability/
  instrumentation/<target>.json
  telemetry-schema/<target>.json
  dashboards/<target>.md
  trace-correlation/<target>.md
  ai-telemetry/<target>.json
```

### `observability/instrumentation/<target>.json`

用于记录必须发出的信号，必须包含：

- `target`、`owner`、`stack`
- `slo_links`
- `golden_signals`
- `metrics`
- `traces`
- `logs`
- `events`
- `sampling`
- `retention`
- `privacy`
- `cost_controls`
- `human_checkpoint`
- `review_cadence`

默认：生产 target 至少覆盖 latency、traffic、errors；有资源或队列时覆盖 saturation。

### `observability/telemetry-schema/<target>.json`

用于约束名称、label、attribute、PII 和基数，必须包含：

- `target`
- `resource_attributes`
- `metric_naming`
- `allowed_labels`
- `forbidden_labels`
- `span_attributes`
- `log_fields`
- `event_names`
- `pii_policy`
- `cardinality_policy`
- `schema_version`

默认禁止 label/attribute 中出现 user_id、email、phone、full_name、raw_ip、prompt_text、response_text、secret、token、uuid、timestamp、request_body。

### `observability/dashboards/<target>.md`

给人排障使用，必须包含：

- `Scope`
- `Primary Questions`
- `Golden Signals`
- `User Journeys`
- `AI / Cost Signals`
- `Release / Config Overlays`
- `Drilldowns`
- `Ownership`
- `Review Cadence`

默认 dashboard 先回答 3 个问题：用户是否受影响、影响在哪里、下一步查什么。

### `observability/trace-correlation/<target>.md`

用于定义 trace、log、metric、request id 的关联方式，必须包含：

- `Trace Context`
- `Request IDs`
- `Log Correlation`
- `Frontend to Backend`
- `gRPC Metadata`
- `Sampling`
- `Debug Procedure`
- `Privacy Limits`

默认使用 W3C Trace Context 或等价 propagation；gRPC 通过 metadata 传播。

### `observability/ai-telemetry/<target>.json`

只有 target 包含 AI workflow 时必须创建，必须包含：

- `target`、`owner`
- `workflow`
- `model_calls`
- `tool_calls`
- `guardrails`
- `eval_links`
- `cost_metrics`
- `quality_signals`
- `trace_policy`
- `redaction`
- `fallbacks`
- `human_checkpoint`

默认记录 token、latency、model/provider、tool name、tool result class、guardrail action、fallback、cost bucket、eval version，不记录原始 prompt/response，除非有显式 privacy/security 审查。

## Go / Kratos / gRPC / sqlc 默认规则

- 使用 OpenTelemetry Go 或等价接口发出 metrics、traces、logs。
- Kratos middleware 应覆盖 server latency、request count、error count、panic/recovery、trace id。
- gRPC span 记录 service、method、status_code、deadline、retry、peer service，不记录 payload。
- 数据库 span 记录 operation、table/query name、rows count bucket、error class、latency，不记录 SQL 参数或用户数据。
- background worker 记录 job type、attempt、duration、result、queue depth 或 backlog。
- 所有外部供应商调用记录 vendor、operation、status、latency、rate_limit、retry count、cost bucket。

## Vite 前端默认规则

- 记录 Web Vitals、route transition、API latency/error、关键用户行为事件和错误边界。
- 前端 trace 应能关联到后端 trace 或 request id。
- 前端 event 只记录稳定、低基数属性，不记录输入框内容、prompt、邮箱、手机号或完整 URL query。
- 关键路径包括登录、创建、保存、导出、支付前确认、AI 任务提交和结果查看。
- release version、feature flag variant、environment 作为低基数属性加入。

## AI workflow 默认规则

- 每次 AI workflow 至少关联一个 trace/span。
- model call 记录 provider、model、operation、latency、input/output token count、cache hit、error class、cost bucket。
- tool call 记录 tool name、permission result、dry-run/commit、duration、result class、retry count。
- guardrail 记录 action、reason class、blocked/allowed、human review required。
- agent workflow 记录 handoff、iteration count、stop reason、max iteration hit、fallback path。
- eval run 和 production trace 之间至少共享 prompt version、workflow version、model route 和 dataset/eval version。
- 高风险工具副作用必须能从 trace 追到 actor、tenant、approval、audit log，但不在 trace 中记录 secret 或完整私有内容。

## Cardinality 和隐私规则

- 不把 user_id、tenant_id、request_id、trace_id、email、uuid、timestamp 当 metric label。需要定位时放 trace/log 字段或抽样事件。
- label 值必须低基数，例如 route、method、status_class、error_class、feature_flag_variant、model_route。
- 日志可以包含 request_id/trace_id，但不得包含 secret、token、password、原始 prompt/response、完整 payload。
- prompt/response 内容默认不进遥测；需要采样时必须有 privacy/security record、retention 和 redaction。
- 高基数或高成本信号必须有 sampling 和 retention 策略。

## 需要人判断的关键点

只把这些观测性判断交给人：

- 是否允许采样 prompt/response 或用户内容。
- 是否允许增加高基数 label 或长保留期。
- 是否启用额外付费 observability vendor。
- 是否在生产临时提高 trace/log sampling。
- AI 行为异常时是回滚、降级、继续 rollout 还是人工审核。

其他仪表、字段、schema 和脚本检查由 Codex 默认创建。

## Review 1：一人公司注意力审查

- 保留：五类工件分别服务“发什么、叫什么、怎么看、怎么关联、AI 怎么追踪”，职责清楚。
- 保留：不要求完整 observability 平台，JSON/Markdown 先表达最低可用信号。
- 调整：不强制所有服务都有复杂 dashboard，先回答 3 个排障问题。
- 调整：AI 原始内容默认不采样，降低隐私和成本风险。
- 风险：instrumentation 容易被写成愿望清单。缓解：脚本检查 latency/traffic/errors、trace/log correlation、低基数和 AI 成本/质量字段。

结论：可落地。一个人可以在 30 到 60 分钟内为一个 target 写出最小观测性基线，并把后续仪表扩展留给真实事故和产品需求。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户旅程和产品事件要能解释用户是否受影响，不只看服务内部健康。
- 工程角度：Go/Kratos/gRPC/sqlc、Vite、AI workflow 都有默认信号，不需要每次重新设计。
- 运维角度：四个黄金信号、trace correlation 和 dashboard drilldown 能支持 W7 SRE-lite incident/runbook。
- 安全隐私角度：默认不采样 prompt/response、secret、PII，采样必须人审。
- 成本角度：高基数、高采样率、AI trace 和长期保留都有 cost_controls 和 checkpoint。

结论：可落地。本专项把“上线后看不见”的风险前移到研发阶段，和 SLO、release、AI eval、成本规范衔接。
