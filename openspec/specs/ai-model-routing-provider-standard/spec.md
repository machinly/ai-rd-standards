# ai-model-routing-provider-standard 规格

## Purpose

Define the minimum one-person-company governance for AI model/provider routing, fallback, eval gates, route-level telemetry, provider review, and production model migration.

## Requirements

### Requirement: 生产 AI capability 必须定义 ai-routing artifacts

Any production AI capability that calls a model, embedding, reranker, moderation, image/audio/realtime, or tool-using AI provider MUST define AI routing artifacts.

#### Scenario: 新 AI capability 调用生产模型

- GIVEN 一个 AI capability 会调用生产模型或外部 AI provider
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `ai-routing/model-registry/<capability>.json`
- AND 创建 `ai-routing/route-policy/<capability>.md`
- AND 创建 `ai-routing/fallback-runbook/<capability>.md`
- AND 创建 `ai-routing/eval-gate/<capability>.json`
- AND 创建 `ai-routing/provider-review/<capability>.md`

### Requirement: Model registry 必须定义 providers、routes、default route、预算、SLO、gate 和 telemetry

Model registry MUST record capability、owner、providers、routes、default_route、budgets、latency_slo、quality_gate、safety_gate、telemetry、human_checkpoint 和 review_cadence。

#### Scenario: Reviewer 判断当前默认模型路线

- GIVEN reviewer 打开 `ai-routing/model-registry/<capability>.json`
- WHEN 需要理解生产 AI 调用
- THEN 能看到 providers、routes、default_route、budgets、latency_slo、quality_gate、safety_gate 和 telemetry
- AND default_route 指向一个 route id
- AND 每个 route 记录 provider、model、reasoning_effort、token limits、timeout、retries、stream、cache_policy、cost_tier、latency target、fallback_chain、eval_refs、safety_refs 和 status

### Requirement: Route policy 必须定义模型选择、工具使用、fallback、timeout/retry、成本延迟、数据边界和人审点

Route policy MUST record scope、decision matrix、default route、model selection、reasoning/tool use、fallback/degradation、timeouts/retries、cost/latency、data boundary、safety/privacy、telemetry、human checkpoints 和 linked artifacts。

#### Scenario: Prompt builder 或 ModelRouter 选择 route

- GIVEN ModelRouter 准备为某个 task type 选择 route
- WHEN 查看 `ai-routing/route-policy/<capability>.md`
- THEN 能确认任务类型、默认 route、候选 route、fallback、timeout/retry、成本/延迟、数据边界、安全隐私和遥测要求
- AND route policy 不允许 prompt 自行越权选择供应商或工具

### Requirement: Fallback runbook 必须覆盖供应商、容量、schema、安全、成本和质量失败

Fallback runbook MUST record scope、failure modes、detection signals、immediate actions、degradation modes、rollback、user messaging、provider escalation、recovery check、post-incident review 和 linked artifacts。

#### Scenario: 模型调用失败或降级

- GIVEN route 遇到 rate limit、timeout、provider 5xx/503、schema failure、safety block、cost threshold、latency SLO breach 或 quality regression
- WHEN operator 或 automation 读取 `ai-routing/fallback-runbook/<capability>.md`
- THEN 能执行 immediate action、degradation mode、rollback、user messaging 和 recovery check
- AND retry 有上限、backoff 和错误分类

### Requirement: Eval gate 必须比较 baseline 与 candidate route

Eval gate MUST record capability、owner、baseline_route、candidate_route、datasets、metrics、thresholds、cost_latency_limits、safety_checks、rollout、rollback、evidence_refs、human_checkpoint 和 status。

#### Scenario: 准备替换默认模型或供应商

- GIVEN candidate route 会改变默认模型、供应商、reasoning effort、工具能力、structured output schema、fallback chain 或 context window
- WHEN 准备发布
- THEN `ai-routing/eval-gate/<capability>.json` 比较 baseline_route 与 candidate_route
- AND 包含质量、安全、schema/tool 成功率、p95 latency、token/cost、timeout rate、fallback rate 和 rollout/rollback evidence

### Requirement: Provider review 必须复盘质量、成本、可靠性、安全隐私、条款边界和事故

Provider review MUST record recent changes、quality results、cost/latency、reliability、safety/privacy、provider terms/data boundary、incidents、open risks 和 next one change。

#### Scenario: 周期性复查模型供应商

- GIVEN capability 有活跃用户、生产模型 route、供应商事件、价格/限制/数据政策变化或 AI incident
- WHEN 更新 `ai-routing/provider-review/<capability>.md`
- THEN 记录质量、成本/延迟、可靠性、安全/隐私、供应商条款/数据边界、事故、开放风险
- AND 只选择一个最高影响的 next one change

### Requirement: 高风险 route 变化必须人工 checkpoint

Production default route changes, new external providers, cross-region or new retention boundaries, sensitive/regulatory data routes, safety/refusal behavior changes, tool-enabled or agentic routes, lower-quality fallback for paid/high-risk flows, budget/cap increases, no-fallback user-visible launches, large-context/high-reasoning defaults, and model deprecations MUST have human checkpoint coverage.

#### Scenario: Route change 触发高风险条件

- GIVEN registry、route policy、eval gate、release 或 incident action 触发高风险条件
- WHEN 准备发布或执行
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、升级或阻塞状态

### Requirement: AI routing artifacts 不得保存敏感内容

AI routing artifacts MUST NOT store secrets, production tokens, provider credentials, private keys, payment data, raw prompts, raw responses, raw tool outputs, unredacted user data, or sensitive provider incident details.

#### Scenario: 记录 route、eval evidence 或 provider event

- GIVEN 需要保存 route sample、eval evidence、provider event 或 incident note
- WHEN 写入 `ai-routing/` artifacts
- THEN 使用 route id、provider id、redacted summary、synthetic prompt、trace id、request id、hash 或 controlled attachment reference
- AND 不保存 secrets、生产 token、供应商凭据、私钥、支付数据、完整 raw prompt/response/tool output 或未脱敏个人数据
