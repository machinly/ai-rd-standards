# 提案：定义观测性、遥测与 AI Trace 规范

## 意图

为一人公司建立最小可用观测性基线，让 Go/Kratos/gRPC/sqlc 服务、Vite 前端和 AI workflow 在进入生产前明确 metrics、traces、logs、events、trace correlation、AI telemetry、隐私和成本控制，降低上线后无法定位用户影响、AI 行为异常和成本异常的风险。

## 范围

- 定义 `observability/instrumentation`、`observability/telemetry-schema`、`observability/dashboards`、`observability/trace-correlation`、`observability/ai-telemetry` artifacts。
- 定义 Go/Kratos/gRPC/sqlc、Vite、AI workflow 的默认 metrics/logs/traces/events。
- 定义 telemetry naming、label/attribute、cardinality、PII、sampling、retention 和 cost controls。
- 定义 AI model call、tool call、guardrail、eval、cost 和 fallback trace 字段。
- 创建观测性落地 skill 和检查脚本。

## 不做

- 不采购或绑定商业 observability 平台。
- 不替代阶段 5 SLO/alert/runbook，而是补充 instrumentation 标准。
- 不默认采样原始 prompt、response、payload 或用户内容。
- 不要求所有服务一开始拥有复杂 dashboard。

## 依据

- 《人月神话》：观测性不是银弹，必须服务系统理解和概念完整性。
- 小型项目管理：只采集能支持决策、排障和恢复上下文的信号。
- Google SRE Monitoring Distributed Systems / Workbook Monitoring。
- Observability Engineering。
- OpenTelemetry signals、Go、JavaScript、logs、semantic conventions。
- W3C Trace Context。
- Prometheus metric naming。
- OpenAI Agents tracing / integrations and observability。

## 需要人的判断

建议默认：任何生产 target 必须有 instrumentation、telemetry schema、dashboard 和 trace correlation artifacts；AI workflow 还必须有 ai telemetry artifact。采样用户内容、高基数 label、提高生产采样率、付费 vendor 或 AI 行为异常处理必须有人审。
