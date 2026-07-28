# 运行：SLO、可观测性与告警

## 规范要求

<!-- rule-id: OPERATION-SLO-001 -->
每个生产服务或关键 workflow 必须先定义并维护用户可见的 SLO/SLI，再补观测；第一版只设 1—2 个可行动 SLO。没有用户路径时，改用最关键后台结果的 freshness 或 correctness SLO。

<!-- rule-id: OPERATION-SLO-002 -->
早期用户可见 MVP 可从 `99.5% monthly availability` 开始讨论，但它不是自动承诺。正式 SLO 必须可计算；暂不可测时只记录采集计划，不得把不可测目标写成正式 SLO。

<!-- rule-id: OPERATION-SLO-003 -->
SLO、SLI 与 error budget policy 的最小仓库工件为 `ops/slo/<service>.json`，并关联 `ops/runbooks/<service>.md`；SLO JSON 应采用来源示例所定义的服务、窗口、指标、目标、数据源、error budget 与行动字段结构。

<!-- rule-id: OPERATION-OBSERVE-001 -->
每个服务必须覆盖四类黄金信号：latency 按 RPC/endpoint 分成功与失败并优先观察 p95 或 p99；traffic 记录请求量、任务量或关键 workflow 次数；errors 覆盖协议错误、业务失败、依赖失败及 parse/schema 失败；saturation 覆盖 CPU、内存、连接池、队列长度、数据库连接或第三方 rate limit。

<!-- rule-id: OPERATION-OBSERVE-002 -->
`ops/observability/<service>.md` 说明 traces、metrics、logs、AI telemetry、dashboard、trace correlation 与低基数 schema。遥测的通用语义和导出协议默认采用 OpenTelemetry；只要求产生可关联信号，不要求自建完整观测平台。

<!-- rule-id: OPERATION-OBSERVE-003 -->
新服务至少提供 health check；依赖数据库、外部 API 或关键配置时还要表达 readiness。服务必须为 latency、traffic、errors、saturation 指定信号落点，error model 记录 Observability，启动日志包含服务名。

<!-- rule-id: OPERATION-OBSERVE-004 -->
上线 AI 能力必须记录身份与版本维度：model、`ai_feature`、prompt version 与 schema version；同时记录 latency、traffic、errors、saturation、tool failure rate、structured output parse failure rate、fallback、rollback、human review rate，以及 token/cost 估计或采集计划。AI telemetry 至少持续保留这些版本、失败率与成本字段。

<!-- rule-id: OPERATION-OBSERVE-005 -->
模型 route policy 必须包含 Telemetry；model registry 必须包含 `latency_slo` 与 telemetry。延迟超 SLO 属于 failure mode；Feature Flag 清单、每个 flag 及 AI route flag 都必须记录 observability。

<!-- rule-id: OPERATION-ALERT-001 -->
告警分为 `page` 与 `ticket`：`page` 只用于用户可见、正在发生且人能立即处置的问题；非紧急、用户不可见或不能立即行动的信号进入 `ticket`。每条告警必须回答“现在能做什么”；连续两次误报或无法行动的 page 必须降级或修改条件，接受不可行动告警须由人决定。

<!-- rule-id: OPERATION-ALERT-002 -->
`page` 必须写明 condition、impact、runbook 与 rollback，并关联含诊断、缓解和回滚步骤的 runbook；没有 runbook 的告警默认不得升级为 page。

<!-- rule-id: OPERATION-RUNBOOK-001 -->
成本专项、integration delivery 与 messaging delivery 均必须有可执行 runbook；后两者默认分别位于 `integrations/delivery-runbook/<target>.md` 与 `messaging/delivery-runbook/<target>.md`。

<!-- rule-id: OPERATION-HANDOFF-001 -->
发布流水线必须包含 observability 动作并引用 `ops/slo/<service>.json`、`ops/runbooks/<service>.md` 与 `release/<service>-checklist.md`；post-deploy 适用的 SLO、alert 与生产服务运行工件必须移交运行和评估持续维护。
