# performance-budget-load-regression-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义一人公司性能预算、负载画像、benchmark 计划、性能回归报告和性能复盘的最小规范，使用户可见服务、前端路径、AI workflow、数据库重路径和后台任务能够在发布前发现、阻断或明确接受性能回归。

## Requirements

### Requirement: 高风险性能目标必须定义 performance artifacts

用户可见核心路径、付费路径、AI workflow、数据库重路径、队列/worker、长连接、高并发或外部依赖重路径 MUST 在高风险性能变更前具备 performance artifacts。

#### Scenario: 新目标进入性能门禁

- GIVEN 一个 target 会影响用户可见性能、容量、前端体验、数据库查询、AI 延迟或后台积压
- WHEN 创建 performance artifacts
- THEN 创建 `performance/budget/<target>.json`
- AND 创建 `performance/load-profile/<target>.json`
- AND 创建 `performance/benchmark-plan/<target>.md`
- AND 在 OpenSpec design 或 tasks 中链接 performance artifacts

#### Scenario: 低风险小变更

- GIVEN 一个变更不改变用户可见行为、数据规模、查询、并发、bundle、AI 调用、外部依赖或运行配置
- WHEN 不创建 performance artifacts
- THEN 在 OpenSpec tasks 或变更说明中记录跳过原因

### Requirement: Performance budget 必须覆盖用户路径、预算、测量和降级

Performance budget MUST 记录 target、owner、user journey、surfaces、SLO references、latency、throughput、frontend、database、AI、saturation、degradation、measurement sources、human checkpoint、review cadence 和 status。

#### Scenario: 创建 performance budget

- GIVEN 一个 target 需要性能门禁
- WHEN 创建 `performance/budget/<target>.json`
- THEN 文件包含 `target`、`owner`、`user_journey`、`surfaces`、`slo_refs`、`latency_budget`、`throughput_budget`、`frontend_budget`、`database_budget`、`ai_budget`、`saturation_budget`、`degradation_policy`、`measurement_sources`、`human_checkpoint`、`review_cadence`、`status`
- AND `latency_budget` 至少包含 p95 或 p99
- AND `measurement_sources` 至少包含一个可执行或可观测来源

#### Scenario: 放宽预算

- GIVEN 变更会放宽 p95/p99、Core Web Vitals、bundle、token、timeout、SLO 或 saturation budget
- WHEN 准备发布
- THEN `human_checkpoint.required_for` MUST 记录预算放宽原因
- AND OpenSpec design 或 regression report MUST 说明用户影响、风险接受和后续动作

### Requirement: Load profile 必须定义负载形状、安全边界和停止条件

Load profile MUST 记录 traffic model、workload mix、concurrency、arrival rate、duration、environment、data shape、dependencies、ramp plan、success criteria、stop conditions、safety limits、human checkpoint 和 status。

#### Scenario: 创建 load profile

- GIVEN target 需要负载验证
- WHEN 创建 `performance/load-profile/<target>.json`
- THEN 文件包含 `target`、`owner`、`traffic_model`、`workload_mix`、`concurrency`、`arrival_rate`、`duration`、`test_environment`、`data_shape`、`dependencies`、`ramp_plan`、`success_criteria`、`stop_conditions`、`safety_limits`、`human_checkpoint`、`status`
- AND `success_criteria` 包含预算或 SLO 对照
- AND `stop_conditions` 包含错误率、p95/p99、saturation、queue、cost、rate limit 或用户影响中适用项

#### Scenario: 高风险压测

- GIVEN load profile 会触达 production、真实客户数据、真实付费 AI provider、第三方 API 或共享环境
- WHEN 运行 load、stress 或 soak
- THEN `human_checkpoint.required_for` MUST 记录对应高风险测试
- AND `safety_limits` MUST 包含请求数、并发、费用、速率、时间或回滚/停止动作

### Requirement: Benchmark plan 必须覆盖 baseline、命令、数据、环境和回归阈值

Benchmark plan MUST 记录 scope、critical path、baseline、measurements、tools/commands、test data、environment、load/stress/soak、frontend checks、backend/RPC checks、database checks、AI/external dependency checks、regression thresholds、human checkpoints、linked artifacts 和 review cadence。

#### Scenario: 创建 benchmark plan

- GIVEN target 准备性能验证
- WHEN 创建 `performance/benchmark-plan/<target>.md`
- THEN 文档包含 Scope、Critical Path、Baseline、Measurements、Tools / Commands、Test Data、Environment、Load / Stress / Soak、Frontend Checks、Backend / RPC Checks、Database Checks、AI / External Dependency Checks、Regression Thresholds、Human Checkpoints、Linked Artifacts、Review Cadence
- AND `Regression Thresholds` 明确至少一个阻断条件

### Requirement: Regression report 必须比较 baseline 和 candidate 并给出发布决策

Regression report MUST 记录 change ref、baseline、candidate、results、budget comparison、regressions、root cause、decision、rollback/mitigation、human checkpoint 和 status。

#### Scenario: 创建 regression report

- GIVEN 完成性能验证
- WHEN 创建 `performance/regression-report/<target>.json`
- THEN 文件包含 `target`、`owner`、`change_ref`、`baseline_ref`、`candidate_ref`、`results`、`budget_comparison`、`regressions`、`root_cause`、`decision`、`rollback_or_mitigation`、`human_checkpoint`、`status`
- AND `decision` 是 `pass`、`pass_with_notes`、`needs_fix`、`accepted_risk`、`rollback` 或 `defer_release`
- AND `budget_comparison` 至少比较一个预算项

#### Scenario: 带性能退化发布

- GIVEN `decision` 是 `accepted_risk`、`rollback`、`defer_release`
- OR report 包含核心路径性能退化、弱基线、未知基线或预算放宽
- WHEN 准备发布
- THEN `human_checkpoint.required_for` MUST 记录对应风险
- AND `rollback_or_mitigation` MUST 记录可执行动作

### Requirement: Performance review 必须只保留一个下一步

Performance review MUST 记录近期变化、预算健康、用户/SLO 影响、benchmark 结果、前端、后端、数据库、AI/外部依赖、饱和、回归/事故、开放风险、一个下一步和复审节奏。

#### Scenario: 创建 performance review

- GIVEN target 已有预算或经历性能相关发布
- WHEN 创建 `performance/performance-review/<target>.md`
- THEN 文档包含 Recent Changes、Budget Health、User / SLO Impact、Load / Benchmark Results、Frontend / Web Vitals、Backend / RPC、Database / Queries、AI / External Dependencies、Saturation / Capacity、Regressions / Incidents、Open Risks、One Next Change、Review Cadence
- AND `One Next Change` 为空时必须明确 `no action`

### Requirement: Go/Kratos/sqlc/gRPC 目标必须有后端性能证据

Go/Kratos/sqlc/gRPC target MUST 记录 RPC 延迟、deadline、retry/backpressure、Go benchmark/pprof 或 DB explain 中适用证据。

#### Scenario: Go/Kratos/gRPC 服务

- GIVEN benchmark plan 涉及 Go、Kratos、gRPC 或 RPC
- WHEN 定义 Tools / Commands
- THEN 包含 `go test -bench`、`go test`、pprof、RPC benchmark、staging load 或明确跳过原因中至少一项
- AND Backend / RPC Checks 覆盖 deadline、retry budget、streaming/queueing/backpressure 中适用项

#### Scenario: sqlc 或 MySQL 查询风险

- GIVEN target 涉及 sqlc、MySQL、schema、index、pagination、join、N+1 或数据规模变化
- WHEN 定义 Database Checks
- THEN 包含 `EXPLAIN`、`EXPLAIN ANALYZE`、query plan evidence 或明确跳过原因

### Requirement: Vite 前端目标必须记录 Web Vitals 和 bundle 风险

Vite frontend target MUST 记录 build/preview、Core Web Vitals、bundle 或 route/API latency 中适用证据。

#### Scenario: Vite frontend

- GIVEN benchmark plan 涉及 Vite、frontend、route、form、dashboard、bundle 或 interaction
- WHEN 定义 Frontend Checks
- THEN 包含 build、preview、lab Web Vitals、bundle check、route transition 或 API latency check 中适用项
- AND budget 记录 LCP、INP、CLS、JS bundle 或 route transition 中至少一项

### Requirement: AI workflow 目标必须记录延迟、token、工具循环和供应商边界

AI workflow target MUST 记录 model/provider latency、token、tool iterations、fallback、timeout、rate limit 和 cost boundary 中适用证据。

#### Scenario: AI workflow

- GIVEN target 涉及 prompt、model、RAG、tool、agent、model route、provider 或 AI workflow
- WHEN 创建 performance budget 和 regression report
- THEN `ai_budget` 包含 p95 latency、timeout、token budget、tool iteration、fallback 或 provider rate limit 中适用项
- AND report 的 results 或 budget_comparison 覆盖 AI latency、token/cost、timeout、fallback 或 provider error 中适用项
