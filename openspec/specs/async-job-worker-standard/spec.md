# async-job-worker-standard 规格

## Purpose

Define the minimum one-person-company governance for long-running AI tasks, queues, background workers, scheduled jobs, leases, retries, dead letters, cancellation, status polling, user-visible progress, worker shutdown, and asynchronous AI provider boundaries.

## Requirements

### Requirement: 生产异步 workflow 必须定义 async-jobs artifacts

Any production workflow that uses long-running AI tasks, queues, background workers, scheduled jobs, retries, batch processing, webhook retry, backfill, RAG ingestion, exports/imports, or user-visible async results MUST define async job artifacts.

#### Scenario: 新异步 workflow 准备进入生产

- GIVEN 一个 workflow 会入队、后台执行、定时运行、重试、批处理、调用 AI 模型/工具或产生用户可见异步结果
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `async-jobs/job-registry/<target>.json`
- AND 创建 `async-jobs/job-contract/<target>.json`
- AND 创建 `async-jobs/worker-runbook/<target>.md`
- AND 创建 `async-jobs/job-test-plan/<target>.json`
- AND 创建 `async-jobs/operations-review/<target>.md`

### Requirement: Job registry 必须定义队列、job type、schedule、storage、worker、限流、保留、遥测和人工 checkpoint

Job registry MUST record target、owner、queues、job types、schedules、storage、workers、rate limits、retention、telemetry、human checkpoint 和 review cadence.

#### Scenario: Reviewer 判断后台任务是否可运行

- GIVEN reviewer 打开 `async-jobs/job-registry/<target>.json`
- WHEN 需要理解有哪些异步任务
- THEN 每个 queue 包含 id、purpose、priority、max_concurrency、dispatch_rate_per_minute、backlog_slo、oldest_age_slo 和 status
- AND 每个 job type 包含 id、name、queue、payload_schema_ref、result_schema_ref、trigger、side_effect_class、idempotency、dedupe_key、timeout_seconds、max_attempts、retry_policy、cancellation、progress、user_visible、data_policy 和 status
- AND `max_attempts` 有有限正整数
- AND 有副作用、AI cost、外部调用、批量数据或定时写操作的 job type 有幂等键、死信路径和人工 checkpoint

### Requirement: Job contract 必须定义状态机、payload/result、幂等、租约、重试、死信、取消、进度、用户可见性和数据保留

Job contract MUST record target、owner、state machine、payload policy、result policy、idempotency、lease policy、retry policy、dead letter policy、cancellation policy、progress policy、user visibility、data retention、human checkpoint 和 status.

#### Scenario: Worker 或前端读取 job 状态契约

- GIVEN job contract 存在
- WHEN worker 更新状态或前端显示 job
- THEN 状态机至少包含 `queued`、`leased`、`running`、`succeeded`、`failed`、`cancel_requested`、`cancelled`、`expired` 和 `dead_lettered`
- AND `leased` 状态有 lease expiry 或等价恢复机制
- AND payload/result policy 不保存 secret、raw prompt、raw response、raw tool output 或未脱敏个人数据

### Requirement: Worker runbook 必须定义启动关闭、入队、抢占租约、执行、重试、取消、死信、观测、降级和事故动作

Worker runbook MUST record scope、start/shutdown、enqueue、dequeue/lease、execute、retry/backoff、cancellation、dead letter/replay、observability、degradation/kill switch、incident actions 和 linked artifacts.

#### Scenario: Worker 部署、宕机或队列积压

- GIVEN worker 进程需要启动、停止、升级或恢复
- WHEN operator 读取 `async-jobs/worker-runbook/<target>.md`
- THEN 能看到如何停止领取新 job、如何完成或释放当前 job、如何处理 lease 过期、如何识别 stuck job、如何降并发或关闭队列
- AND dead-letter replay 必须要求审查、幂等和影响摘要

### Requirement: Job test plan 必须覆盖入队 schema、重复幂等、租约、优雅关闭、重试、死信、回放、取消、超时、限流、stuck recovery、状态轮询、遥测、脱敏和 AI 成本

Job test plan MUST record target、owner、environments、cases、required checks、evidence refs、human checkpoint 和 status.

#### Scenario: 发布前验证异步 workflow

- GIVEN 异步 workflow 准备发布
- WHEN 读取 `async-jobs/job-test-plan/<target>.json`
- THEN `required_checks` 至少包含 `enqueue_schema`、`idempotency_duplicate`、`dequeue_lock_or_lease`、`graceful_shutdown`、`retry_backoff`、`max_attempts`、`dead_letter`、`replay_guard`、`cancellation`、`timeout`、`rate_limit_concurrency`、`stuck_job_recovery`、`status_polling`、`telemetry`、`sensitive_payload_redaction` 和 `ai_cost_limit`
- AND cases 覆盖每个 required check
- AND AI job 覆盖 cost/token limit、provider timeout、background/batch status polling 和用户可见失败状态

### Requirement: Operations review 必须复盘 backlog、延迟、失败、重试、死信、取消、成本、用户影响、事故和下一项改进

Operations review MUST record recent changes、backlog/latency、failures/retries、dead letters/replays、cancellation/expiry、cost/capacity、user impact、incidents、open risks 和 next one change.

#### Scenario: 周期性复查后台任务健康

- GIVEN target 有近期 job type、worker、schedule、queue、AI route、tool、retry 或 provider 变更
- WHEN 更新 `async-jobs/operations-review/<target>.md`
- THEN 记录 backlog/latency、失败/重试、dead letter/replay、取消/过期、成本/容量、用户影响、事故和开放风险
- AND 只选择一个最高影响的 next one change

### Requirement: 高风险异步任务变更必须人工 checkpoint

New durable queues/providers, user-visible core async paths, side-effect retry/replay, missing idempotency/lease/max-attempts/dead-letter/graceful-shutdown/stuck-recovery, sensitive payload/result retention, concurrency/cost expansion, dead-letter deletion/replay, and OpenAI background/batch privacy boundary changes MUST have human checkpoint coverage.

#### Scenario: Async workflow 触发高风险条件

- GIVEN registry、contract、runbook、test plan、review 或 release 触发高风险条件
- WHEN 准备发布或接受例外
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、阻塞、降级或补偿动作

### Requirement: Async job artifacts 不得保存敏感内容

Async job artifacts MUST NOT store secrets, production tokens, API keys, OAuth refresh tokens, private keys, session cookies, database connection strings, payment data, raw prompts, raw responses, raw tool outputs, unredacted personal data, connector credentials, provider raw outputs, or executable attack payloads.

#### Scenario: 记录 payload、结果、dead letter、事故或测试证据

- GIVEN 需要保存 job payload example、result example、dead-letter note、worker incident、AI background/batch status 或 replay evidence
- WHEN 写入 `async-jobs/` artifacts
- THEN 使用 synthetic example、redacted summary、job id、attempt id、trace id、artifact id、hash、finding id 或 controlled attachment reference
- AND 不保存 secret、生产 token、API key、OAuth refresh token、私钥、session cookie、数据库连接串、支付数据、完整 raw prompt/response/tool output、未脱敏个人数据、connector credential、provider raw output 或可直接执行的攻击 payload
