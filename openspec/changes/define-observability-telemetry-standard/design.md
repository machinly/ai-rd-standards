# 设计：观测性、遥测与 AI Trace 规范

## 设计决策

### 1. 观测性工件和 SLO 工件分离

阶段 5 定义 SLO、alert 和 runbook。阶段 15 只定义代码和系统必须发出的信号、字段和关联方式。这样避免把 dashboard 当成可靠性策略，也避免 SLO 没有数据来源。

### 2. 用 OpenTelemetry 作为默认语义

OpenTelemetry 是 vendor-neutral 标准，能覆盖 traces、metrics、logs 和 semantic conventions。规范不要求特定后端，但要求命名、resource attribute、span attribute、log field 和 context propagation 可迁移。

### 3. 低基数优先，定位信息放 trace/log

metric labels 用于聚合和告警，必须低基数。request_id、trace_id、user_id、uuid 等高基数字段不进入 metric label，放 trace/log 或采样事件中。

### 4. AI trace 默认记录结构，不记录原文

AI 排障需要 model、token、cost、tool、guardrail、fallback 和 eval version，但原始 prompt/response 会带来隐私和数据保留风险。默认只记录结构化元数据，需要原文采样时触发 privacy/security checkpoint。

### 5. Dashboard 先回答问题，不追求图表数量

一人公司 dashboard 只需先回答：用户是否受影响、影响在哪里、下一步查什么。图表数量随真实 incident 和 product decisions 增加。

### 6. 人只判断高风险观测性扩展

模板和脚本负责默认信号、字段、PII、高基数和 AI telemetry 检查。人只判断内容采样、付费 vendor、高采样率、长期保留和 AI 异常处理。

## 取舍

- 增加少量观测性工件，但减少上线后排障成本。
- 不默认 vendor，降低早期成本和锁定。
- 不把所有业务事件都变成 metrics，避免高基数和成本爆炸。
- 简单脚本无法证明 instrumentation 已在代码中实现，但能阻止没有观测性计划的生产变更。
