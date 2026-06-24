# observability-telemetry-standard Specification

## Purpose

定义一人公司观测性、遥测与 AI trace 的最小基线，使生产服务、前端应用和用户可见 AI workflow 在进入生产前明确 metrics、traces、logs、events、trace correlation、AI telemetry、隐私和成本控制。

## Requirements

### Requirement: 生产 target 必须定义观测性工件

生产服务、前端应用或用户可见 AI workflow MUST 在发布前具备观测性 artifacts。

#### Scenario: 新生产 target 进入研发

- GIVEN 一个 target 会进入生产
- WHEN 创建 OpenSpec change
- THEN 创建 `observability/instrumentation/<target>.json`
- AND 创建 `observability/telemetry-schema/<target>.json`
- AND 创建 `observability/dashboards/<target>.md`
- AND 创建 `observability/trace-correlation/<target>.md`
- AND 在 OpenSpec design 或 tasks 中链接 observability artifacts

#### Scenario: AI workflow

- GIVEN target 包含 AI prompt、model、tool、agent workflow、retrieval 或 guardrail
- WHEN 创建 observability artifacts
- THEN 创建 `observability/ai-telemetry/<target>.json`

### Requirement: Instrumentation plan 必须覆盖黄金信号、metrics、traces、logs 和隐私成本

Instrumentation plan MUST 记录 target、owner、stack、SLO links、golden signals、metrics、traces、logs、events、sampling、retention、privacy、cost controls、人审点和复审节奏。

#### Scenario: 创建 instrumentation plan

- GIVEN 一个 target 需要生产观测性
- WHEN 创建 `observability/instrumentation/<target>.json`
- THEN 文件包含 `target`、`owner`、`stack`、`slo_links`、`golden_signals`、`metrics`、`traces`、`logs`、`events`、`sampling`、`retention`、`privacy`、`cost_controls`、`human_checkpoint`、`review_cadence`
- AND golden_signals 覆盖 latency、traffic、errors

### Requirement: Telemetry schema 必须限制命名、基数和敏感字段

Telemetry schema MUST 记录 resource attributes、metric naming、allowed labels、forbidden labels、span attributes、log fields、event names、PII policy、cardinality policy 和 schema version。

#### Scenario: 创建 telemetry schema

- GIVEN 一个 target 定义 telemetry
- WHEN 创建 `observability/telemetry-schema/<target>.json`
- THEN 文件包含 `target`、`resource_attributes`、`metric_naming`、`allowed_labels`、`forbidden_labels`、`span_attributes`、`log_fields`、`event_names`、`pii_policy`、`cardinality_policy`、`schema_version`

#### Scenario: 检查 forbidden labels

- GIVEN telemetry schema 包含 labels 或 attributes
- WHEN 校验 schema
- THEN forbidden_labels 覆盖 user_id、email、phone、full_name、raw_ip、prompt_text、response_text、secret、token、uuid、timestamp、request_body 中适用项

### Requirement: Dashboard spec 必须回答用户影响和排障下一步

Dashboard spec MUST 以人可读方式记录 scope、primary questions、golden signals、user journeys、AI/cost signals、release/config overlays、drilldowns、ownership 和 review cadence。

#### Scenario: 创建 dashboard spec

- GIVEN 一个 target 需要 dashboard
- WHEN 创建 `observability/dashboards/<target>.md`
- THEN 文档包含 Scope、Primary Questions、Golden Signals、User Journeys、AI / Cost Signals、Release / Config Overlays、Drilldowns、Ownership、Review Cadence

### Requirement: Trace correlation 必须定义跨前后端和服务的关联方式

Trace correlation MUST 定义 trace context、request ids、log correlation、frontend-to-backend、gRPC metadata、sampling、debug procedure 和 privacy limits。

#### Scenario: 创建 trace correlation 文档

- GIVEN 一个 target 有跨进程或前后端调用
- WHEN 创建 `observability/trace-correlation/<target>.md`
- THEN 文档包含 Trace Context、Request IDs、Log Correlation、Frontend to Backend、gRPC Metadata、Sampling、Debug Procedure、Privacy Limits
- AND 记录 W3C Trace Context 或等价 propagation

### Requirement: AI telemetry 必须覆盖模型、工具、guardrail、eval、成本和回退

AI telemetry record MUST 记录 workflow、model calls、tool calls、guardrails、eval links、cost metrics、quality signals、trace policy、redaction、fallbacks 和人审点。

#### Scenario: 创建 AI telemetry

- GIVEN target 包含 AI workflow
- WHEN 创建 `observability/ai-telemetry/<target>.json`
- THEN 文件包含 `target`、`owner`、`workflow`、`model_calls`、`tool_calls`、`guardrails`、`eval_links`、`cost_metrics`、`quality_signals`、`trace_policy`、`redaction`、`fallbacks`、`human_checkpoint`
- AND model_calls 覆盖 provider、model、latency、token count、error class、cost bucket
- AND tool_calls 覆盖 tool name、permission result、duration、result class、retry count

### Requirement: 敏感内容和高基数遥测必须人工 checkpoint

采样 prompt/response、记录 payload、加入高基数 label、提高生产 sampling、延长 retention、启用付费 vendor 或 AI 异常继续 rollout MUST 有人工 checkpoint。

#### Scenario: 采样 prompt 内容

- GIVEN trace policy 采样 prompt_text 或 response_text
- WHEN 准备发布
- THEN `human_checkpoint.required_for` 包含 `sample_prompt_content` 或等价条目
- AND privacy/security artifacts 记录 redaction、retention 和 access control

#### Scenario: 高基数 label 例外

- GIVEN telemetry schema 允许 user_id、tenant_id、uuid、timestamp 或 raw request id 作为 metric label
- WHEN 准备发布
- THEN `human_checkpoint.required_for` 包含 `high_cardinality_label`
- AND cost_controls 记录风险、采样和回滚方式
