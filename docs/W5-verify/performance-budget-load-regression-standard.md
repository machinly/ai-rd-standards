# W5 Verify 触发专项：性能预算、负载验证与性能回归治理规范

## W5 触发定位

本文件是 W5 Verify 的触发型专项，不是 W5 主入口。只有当当前验证涉及核心路径性能、负载画像、benchmark、Web Vitals、bundle、DB query、AI latency/token、容量或性能回归时，才需要读取本文件。

普通 W5 验证入口应先回到 `docs/W5-verify/main.md`，由主入口判断是否触发本专项。

## 目标

一人公司的性能问题常常不是“没有优化”，而是**不知道什么时候已经变慢了**。平均延迟看起来正常，p95 或 p99 已经伤害用户；一次依赖升级让 bundle 变大；一个 SQL 查询在小数据上很快，生产数据一多就拖垮核心路径；AI workflow 为了更好答案多走几轮模型调用，用户等待和成本一起上升。

本专项负责回答一个窄问题：**一个变更是否仍在性能预算内，是否能承受目标负载，性能回归能否在发布前被发现或被明确接受。**

默认原则：**没有性能预算、负载画像、benchmark 计划、回归报告和复盘节奏，就不要声称性能可控。** 本专项不追求复杂压测平台，而是把一人公司最容易忽略的性能判断压成少量可检查工件。

## 核心依据

- 《人月神话》：性能优化没有银弹；真正困难的是在需求、接口、数据、运行环境和用户体验之间保持概念完整性。
- 小型项目管理：一人公司不维护完整性能工程团队；只保留能支持 go/no-go 的预算、画像、计划、报告和复盘。
- Google SRE Monitoring / Handling Overload：性能应连接 latency、traffic、errors、saturation；过载时要知道资源上限、优先级、拒绝/降级和 retry budget。
- Brendan Gregg `Systems Performance` / USE Method：性能调查先从资源的 utilization、saturation、errors 出发，避免只看平均 CPU 或单个指标。
- `The Art of Capacity Planning`：容量判断应基于测量、部署和管理真实 web 负载，而不是等流量峰值把系统打穿。
- Go 官方 `testing` / pprof：Go benchmark、parallel benchmark 和 `go tool pprof` 是定位代码级性能回归的低成本入口。
- gRPC Performance Best Practices：长生命周期数据流可用 streaming 减少重复 RPC 开销；高并发和长连接要注意 HTTP/2 stream queueing。
- Web Vitals：LCP、INP、CLS 是前端用户体验的稳定核心指标；lab 数据适合发布前发现回归，field 数据适合持续确认真实用户体验。
- PostgreSQL `EXPLAIN` / `EXPLAIN ANALYZE`：查询性能必须看计划、实际行数和执行时间，同时理解测量开销和网络传输边界。
- Vite Performance：Vite 默认很快，但随着项目增长会出现 server start、page load、build 性能问题，需要持续检查。
- OpenAI Latency Optimization：AI 延迟通常受输出 token、输入 token、请求次数、并行化和是否必须使用 LLM 影响。

## 范围

适用对象：

- 用户可见核心路径、付费路径、后台关键任务、导入/导出、Webhook、RAG/AI workflow、内部管理高频路径。
- Go/Kratos/sqlc/gRPC 服务的 RPC 延迟、吞吐、并发、DB 查询、队列、worker、外部依赖和资源饱和。
- Vite 前端的 Core Web Vitals、bundle、route transition、API 调用延迟和关键交互。
- AI workflow 的模型调用延迟、token、工具调用次数、fallback、timeout、streaming、缓存和供应商速率限制。

不适用对象：

- 通用 SLO、告警、事故响应；走 W7 SRE-lite 专项。
- 成本预算、供应商退出、容量限额和过载 runbook；走 W2 成本容量专项。
- 通用测试矩阵、flaky 测试和发布前 test run；走 W5 测试质量专项。
- 指标、日志、trace schema 和 dashboard；走 W7 观测性专项。
- AI 模型路由、fallback、provider gate；走 W3 model routing。
- AI 质量回归和线上质量事故；走 W8 AI quality regression。
- 企业级性能实验室、全链路压测平台、容量预测模型或持续 profiler 平台；真实规模证明需要后再单独开 change。

## 最小工件

每个性能目标使用同一个 `<target>` 文件名：

```text
performance/
  budget/<target>.json
  load-profile/<target>.json
  benchmark-plan/<target>.md
  regression-report/<target>.json
  performance-review/<target>.md
```

`<target>` 可以是服务、RPC、前端路径、AI capability、后台 job 或关键用户旅程，例如 `checkout-rpc`、`assistant-answer`、`dashboard-home`。

### `performance/budget/<target>.json`

性能预算必须包含：

- `target`
- `owner`
- `user_journey`
- `surfaces`
- `slo_refs`
- `latency_budget`
- `throughput_budget`
- `frontend_budget`
- `database_budget`
- `ai_budget`
- `saturation_budget`
- `degradation_policy`
- `measurement_sources`
- `human_checkpoint`
- `review_cadence`
- `status`

默认规则：

- `latency_budget` 至少记录 p95 或 p99；不要只用平均值。
- `frontend_budget` 记录适用的 LCP、INP、CLS、JS bundle、route transition 或关键 API 延迟。
- `database_budget` 记录慢查询阈值、最大扫描行数或 `EXPLAIN ANALYZE` 触发条件。
- `ai_budget` 记录 p95、timeout、token、工具调用次数、fallback 或 streaming 目标中适用项。
- `saturation_budget` 记录 CPU、memory、DB connection、queue depth、worker concurrency、provider quota 中适用项。
- 放宽 p95/p99、Core Web Vitals、bundle、token、timeout、SLO 或饱和阈值时必须有人工 checkpoint。

### `performance/load-profile/<target>.json`

负载画像必须包含：

- `target`
- `owner`
- `traffic_model`
- `workload_mix`
- `concurrency`
- `arrival_rate`
- `duration`
- `test_environment`
- `data_shape`
- `dependencies`
- `ramp_plan`
- `success_criteria`
- `stop_conditions`
- `safety_limits`
- `human_checkpoint`
- `status`

默认规则：

- `traffic_model` 记录正常、峰值、突发、后台批处理、长连接、AI streaming 或导入导出中适用模式。
- `workload_mix` 不只写 QPS；要记录请求类型、数据规模、缓存命中、租户/用户分布和重试比例。
- `test_environment` 默认是本地、preview、staging、sandbox 或 isolated environment。
- 生产压测、真实供应商压测、真实付费 AI 调用、使用真实客户数据或可能影响他人的测试，必须有人审。
- `stop_conditions` 必须能让一个人知道何时停止测试：错误率、p95/p99、饱和、队列、费用、供应商限流或用户影响。

### `performance/benchmark-plan/<target>.md`

benchmark 计划必须包含：

```markdown
# <target> Performance Benchmark Plan

## Scope

## Critical Path

## Baseline

## Measurements

## Tools / Commands

## Test Data

## Environment

## Load / Stress / Soak

## Frontend Checks

## Backend / RPC Checks

## Database Checks

## AI / External Dependency Checks

## Regression Thresholds

## Human Checkpoints

## Linked Artifacts

## Review Cadence
```

默认规则：

- `Baseline` 记录对比基线：上一版 release、main branch、最近稳定 build、生产 field 数据或 synthetic baseline。
- `Measurements` 明确 p50/p95/p99、error rate、throughput、CPU/memory、DB query time、bundle、Web Vitals、token/cost 中适用项。
- `Tools / Commands` 使用仓库已有命令优先；Go 目标优先 `go test -bench`、`go test -run`、pprof；前端目标优先 build、preview、Web Vitals/lab 工具；DB 目标优先 `EXPLAIN` / `EXPLAIN ANALYZE` 的安全副本。
- `Regression Thresholds` 写清楚阻断条件，例如 p95 +10%、bundle +20KB、LCP 超 2.5s、INP 超 200ms、DB query 超 200ms、AI p95 超预算。
- 不要求每个目标都做 stress/soak；只有并发、队列、长连接、外部依赖、缓存或内存泄漏风险时才做。

### `performance/regression-report/<target>.json`

性能回归报告必须包含：

- `target`
- `owner`
- `change_ref`
- `baseline_ref`
- `candidate_ref`
- `results`
- `budget_comparison`
- `regressions`
- `root_cause`
- `decision`
- `rollback_or_mitigation`
- `human_checkpoint`
- `status`

`decision` 只允许：

- `pass`
- `pass_with_notes`
- `needs_fix`
- `accepted_risk`
- `rollback`
- `defer_release`

默认规则：

- `results` 必须包含本轮实际数据，不只写“通过”。
- `budget_comparison` 至少比较一个预算项；没有基线时 decision 不能是 `pass`，只能是 `pass_with_notes` 或 `needs_fix`。
- `regressions` 必须列出退化指标、幅度、用户影响和是否可恢复。
- `accepted_risk`、`rollback`、`defer_release`、放宽预算或带性能退化发布，都必须有人工 checkpoint。
- 如果回归来自 DB、AI provider、缓存、队列、bundle、重试或并发，报告必须链接相应 mitigation 或后续 work item。

### `performance/performance-review/<target>.md`

性能复盘必须包含：

```markdown
# <target> Performance Review

## Recent Changes

## Budget Health

## User / SLO Impact

## Load / Benchmark Results

## Frontend / Web Vitals

## Backend / RPC

## Database / Queries

## AI / External Dependencies

## Saturation / Capacity

## Regressions / Incidents

## Open Risks

## One Next Change

## Review Cadence
```

默认规则：

- 复盘只选一个下一步，不把性能债变成长清单。
- 如果预算健康、没有回归、没有用户影响，可以记录 `no action`。
- 如果出现同类回归第二次，必须把 threshold、测试数据或基线纳入 release gate。

## 默认流程

1. 选一个 `<target>`：只选本次变更会影响的核心路径。
2. 写 `budget`：把用户可感知目标、SLO、前端/后端/DB/AI/饱和预算写成 JSON。
3. 写 `load-profile`：描述正常、峰值、突发和测试安全边界。
4. 写 `benchmark-plan`：写 baseline、命令、测试数据、阈值和人审点。
5. 跑最小验证：本地 benchmark、preview/lab、staging load、DB explain、AI latency sample 中适用的最小组合。
6. 写 `regression-report`：用实际数据做 go/no-go。
7. 定期写 `performance-review`：只保留一个最高影响改进。

## Go / Kratos / sqlc / gRPC 默认规则

- Kratos middleware 记录 RPC method、status、deadline/cancel、p95/p99、payload bucket、error class 和 trace id；不要记录 payload 原文。
- gRPC 服务默认设置 deadline/timeout；retry 必须有上限、backoff 和 retry budget，不允许无限重试。
- 高并发或长生命周期流程优先评估 streaming、连接复用、并发队列、backpressure 和 graceful degradation。
- Go 代码级热点用 `go test -bench` 或 pprof 先证明瓶颈，再优化；不要凭直觉改复杂缓存。
- sqlc 查询必须有可读 query name；慢查询、分页、N+1、JOIN 或索引变化必须记录 `EXPLAIN` / `EXPLAIN ANALYZE` 证据或跳过原因。
- 后端性能预算不替代 W2 容量边界；它只定义“此路径应该多快、退化多少算失败”。

## Vite 前端默认规则

- 新前端目标使用 Vite build/preview 作为基础门禁；关键路径记录 bundle、route transition、API latency 和 Core Web Vitals。
- LCP、INP、CLS 默认采用 Web Vitals 推荐阈值作为起点；业务可更严，但放宽需要人工 checkpoint。
- 使用 Vercel Geist 风格时保持界面克制、密集、低噪声；性能报告 UI 优先显示 pass/fail、delta、阻断项和证据链接。
- 不为早期项目强制完整 RUM 平台；先用 lab/preview 检查阻断明显回归，生产有用户后再接 field 数据。

## AI workflow 默认规则

- AI 目标至少记录 p95 latency、timeout、input/output token、tool iteration、fallback、provider error/rate limit 中适用项。
- 先减少不必要请求、输出 token、输入 token 或工具轮次，再考虑更复杂的模型路由或缓存平台。
- 真实 OpenAI/LLM 供应商负载测试必须设置请求数、token、费用和速率上限；默认使用 mock、recorded response 或小样本 capped run。
- Streaming 可改善用户感知等待，但仍要记录整体完成时间、首 token 时间和失败/中断路径。
- 性能不能单独战胜质量和安全：AI p95 变好但质量、安全、隐私或工具正确性退化，走 W8 quality regression 或 W3 model routing，不在本专项直接放行。

## 需要人判断的关键点

默认不问：

- 文件命名、字段完整性、普通 baseline 选择、低风险本地 benchmark、没有退化的 `pass` 报告、复盘中的 `no action`。

必须问：

- 是否放宽 p95/p99、Core Web Vitals、bundle、token、timeout、SLO 或饱和预算。
- 是否对 production、真实客户数据、真实付费 AI provider、第三方 API 或共享环境运行 load/stress/soak。
- 是否接受性能回归、发布 `accepted_risk`、`pass_with_notes` 中的核心路径退化或未知基线。
- 是否增加显著云资源、数据库索引/缓存/CDN/队列、供应商优先级或模型服务成本。
- 是否删除或弱化 benchmark、load test、trace、timeout、rate limit、fallback、backpressure 或性能 release gate。
- 是否在付费客户、合同 SLA、核心转化路径或高风险 AI workflow 中带性能未知发布。

其他字段、敏感信息、状态枚举、正反 fixture、OpenSpec 链接和报告结构由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“预算是多少、负载是什么、怎么测、是否退化、下次改什么”。
- 保留：人只判断放宽预算、真实压测、接受回归、显著花钱、弱化门禁和核心路径未知性能发布。
- 调整：不要求完整性能平台；用文件、命令和少量样本先挡住明显回归。
- 调整：允许没有 field 数据的早期项目用 lab/staging baseline 起步，但报告必须承认基线弱。
- 风险：性能规范可能变成每个小改动都要填表。缓解：只对用户可见核心路径、高风险变更、容量/并发/AI/DB/前端 bundle 风险触发。

结论：可落地。本专项把性能从“感觉还行”变成少量能复查的预算和证据，不会要求一人公司先搭平台。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：预算连接用户路径和 SLO，不为技术指标本身优化。
- 工程角度：Go benchmark、gRPC deadline、sqlc query、Vite build 和 AI latency 都有各自证据入口。
- 运维角度：负载画像、stop conditions、saturation 和降级策略连接 W7 SRE-lite、W2 成本容量和 W7 观测性，避免压测本身造成事故。
- 安全隐私角度：性能工件不保存 raw payload、客户数据、secret、prompt/response 原文或生产日志。
- 成本角度：性能改进先定位瓶颈，再决定缓存、索引、CDN、队列、供应商优先级或扩容，避免用钱掩盖设计问题。

结论：可落地。它补上 W7 SRE-lite、W2 成本容量、W5 测试质量、W7 观测性、W3 模型路由和 W8 AI 质量之间的性能回归门禁：先定义预算，再测负载；先比较基线，再决定发布。
