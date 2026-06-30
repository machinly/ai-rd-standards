# W4 Build 触发专项：AI 异步任务、队列与后台 Worker 治理规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及长任务、队列、后台 worker、Batch/background、RAG 入库、导出导入、webhook retry、backfill、取消、重试、死信或异步用户状态时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/00-main.md`，由主入口判断是否触发本专项。

## 目标

AI 产品一旦进入真实使用，很多工作都不该绑在一次 HTTP/gRPC 请求里：长推理、批量评测、文件处理、导出、索引刷新、RAG 入库、视频/图片生成、后台补偿、webhook 重试、定时同步、批量数据修复、AI agent 多步任务。本专项定义 AI 异步任务、队列与后台 Worker 治理规范，让每个后台 workflow 都能回答：任务怎样入队，状态怎样变化，谁能取消，worker 怎样抢占和续租，失败怎样重试，何时进入死信，能否安全回放，用户如何查看进度，部署和宕机时怎样不丢任务、不重复副作用、不无限烧钱。

默认原则：长任务是产品契约，不是隐藏线程。任何超过一次交互可承受时间、会重试、会批处理、会定时运行、会调用 AI 模型/工具或会产生用户可见结果的后台任务，都必须有显式 job contract、有限重试、幂等、取消、观测、恢复和人工 checkpoint。

## 核心依据

- 《人月神话》：没有“加一个队列”就解决复杂度的银弹；后台任务的本质复杂度在状态、失败、重复、恢复和用户预期。
- 小型项目管理：一人公司不能维护大型调度平台；先保留能避免丢任务、重复副作用和恢复上下文的五个小工件。
- Enterprise Integration Patterns：异步消息模式提供稳定词汇，如 Competing Consumers、Idempotent Receiver、Message Store、Message History；队列能削峰，但也需要流控。
- Designing Data-Intensive Applications：数据系统设计要权衡可靠性、可扩展性、可维护性、批处理/流处理、消息 broker 和工具复杂度；一人公司不能为未发生的规模提前平台化。
- Google SRE Distributed Periodic Scheduling with Cron：定时任务在分布式环境里需要处理单点、重复触发、一致状态和依赖边界。
- Google SRE Data Processing Pipelines：后台管道可能业务关键；延迟或错误会造成用户可见问题，因此要定义 pipeline 需求、健康信号和运行生命周期。
- Google SRE Handling Overload / Cascading Failures：队列、worker fanout、自动重试和批处理会放大过载；必须有背压、限流、退避、降级和停止条件。
- Twelve-Factor App Concurrency / Disposability：长任务应由 worker process 承担；worker 要能快速启动、优雅停止，并在停止时把当前 job 归还或安全释放。
- PostgreSQL `FOR UPDATE SKIP LOCKED`：Postgres 可用于多个消费者访问 queue-like table，但它给的是不一致视图，只适合队列式抢占，不适合作为通用一致性读取。
- OpenAI Background Mode / Batch API：长推理和离线大批量 AI 请求应异步处理并轮询状态；background mode 有数据保留边界，Batch 适合不要求即时响应的任务。
- OpenTelemetry Messaging Semantic Conventions：消息/队列跨度、指标和日志应使用可迁移语义，而不是每个 worker 自造字段。

## 范围

适用对象：

- AI long-running task、agent run、eval run、Batch API job、background response、RAG ingestion、embedding、rerank、file processing、export/import、webhook retry、scheduled sync、backfill、data repair、notification retry。
- Go/Kratos/gRPC 后端里的 `SubmitJob`、`GetJob`、`CancelJob`、`RetryJob`、worker process、queue table、lease/lock、dead letter、outbox、scheduler。
- sqlc/PostgreSQL 队列表、job attempt、job event、job result、job schedule、job cancellation、dead-letter 和幂等键。
- Vite 前端里的排队状态、进度、取消、重试、结果下载、失败解释、部分成功和降级提示。
- W3 AI eval、W7 observability、W7 admin ops、W3 model routing、W3 tool runtime 中任何需要异步执行的 workflow。

不适用对象：

- 纯同步、低风险、几百毫秒内完成且不重试的普通请求。
- 只在本地运行、不访问生产数据、不调用真实供应商、不进入产品路径的一次性脚本。
- 企业级工作流编排平台、全量数据平台、复杂 DAG 调度、跨区域 exactly-once 系统；需要时单独开 architecture change。

## 最小工件

每个生产异步 workflow 使用同一个 `<target>` 文件名：

```text
async-jobs/
  job-registry/<target>.json
  job-contract/<target>.json
  worker-runbook/<target>.md
  job-test-plan/<target>.json
  operations-review/<target>.md
```

### `async-jobs/job-registry/<target>.json`

Job registry 必须包含：

- `target`
- `owner`
- `queues`
- `job_types`
- `schedules`
- `storage`
- `workers`
- `rate_limits`
- `retention`
- `telemetry`
- `human_checkpoint`
- `review_cadence`

`queues` 每项至少包含：

- `id`
- `purpose`
- `priority`
- `max_concurrency`
- `dispatch_rate_per_minute`
- `backlog_slo`
- `oldest_age_slo`
- `status`

`job_types` 每项至少包含：

- `id`
- `name`
- `queue`
- `payload_schema_ref`
- `result_schema_ref`
- `trigger`
- `side_effect_class`
- `idempotency`
- `dedupe_key`
- `timeout_seconds`
- `max_attempts`
- `retry_policy`
- `cancellation`
- `progress`
- `user_visible`
- `data_policy`
- `status`

默认：

- 生产异步任务必须先登记 job type；未登记 job 不得由 prompt、tool、admin action、webhook 或 cron 启动。
- `max_attempts` 必须有限；不允许无限重试。
- 有副作用、AI cost、外部调用、批量数据、后台修复或定时写操作的 job 必须有幂等键、重试上限、死信路径、观测字段和人工 checkpoint。
- 用户可见 job 必须有状态查询、可理解失败原因、结果保留期和取消/过期策略。

### `async-jobs/job-contract/<target>.json`

Job contract 必须包含：

- `target`
- `owner`
- `state_machine`
- `payload_policy`
- `result_policy`
- `idempotency`
- `lease_policy`
- `retry_policy`
- `dead_letter_policy`
- `cancellation_policy`
- `progress_policy`
- `user_visibility`
- `data_retention`
- `human_checkpoint`
- `status`

默认状态：

- `queued`
- `leased`
- `running`
- `succeeded`
- `failed`
- `cancel_requested`
- `cancelled`
- `expired`
- `dead_lettered`

默认：

- 状态转换必须由服务端控制，不接受前端或模型直接写入最终状态。
- `leased` 必须有 `lease_expires_at` 或等价超时；worker 崩溃后任务能被重新领取或进入 stuck recovery。
- payload 默认只存 schema 化、最小化、可重放输入；不保存完整 raw prompt、raw response、raw tool output、secret 或未脱敏个人数据。
- result 默认保存引用、摘要、artifact id 或受控对象，不把大文件、敏感正文或供应商原始响应塞进 job row。

### `async-jobs/worker-runbook/<target>.md`

Worker runbook 必须包含：

- `Scope`
- `Start / Shutdown`
- `Enqueue`
- `Dequeue / Lease`
- `Execute`
- `Retry / Backoff`
- `Cancellation`
- `Dead Letter / Replay`
- `Observability`
- `Degradation / Kill Switch`
- `Incident Actions`
- `Linked Artifacts`

默认执行顺序：

1. 入队前校验 actor、tenant、job type、payload schema、dedupe key、budget、rate limit 和用户可见状态。
2. Worker 抢占 job 时使用事务、lease/lock 和 deterministic order；Postgres 队列表可用 `FOR UPDATE SKIP LOCKED`，但只用于 queue-like table。
3. Worker 执行前绑定 trace id、job id、attempt id、actor、tenant、deadline、cost budget 和 cancellation token。
4. 每次尝试记录 attempt、开始/结束、错误分类、retry decision、queue age、duration、worker id 和结果引用。
5. 收到 shutdown 时停止领取新 job，当前 job 要么完成，要么释放/过期 lease；不在进程退出时丢失隐式内存状态。
6. 重试耗尽、不可重试错误、payload 风险、外部供应商异常、工具越权或数据风险进入 dead letter，并要求明确 replay 审查。

### `async-jobs/job-test-plan/<target>.json`

Job test plan 必须包含：

- `target`
- `owner`
- `environments`
- `cases`
- `required_checks`
- `evidence_refs`
- `human_checkpoint`
- `status`

`required_checks` 默认至少覆盖：

- `enqueue_schema`
- `idempotency_duplicate`
- `dequeue_lock_or_lease`
- `graceful_shutdown`
- `retry_backoff`
- `max_attempts`
- `dead_letter`
- `replay_guard`
- `cancellation`
- `timeout`
- `rate_limit_concurrency`
- `stuck_job_recovery`
- `status_polling`
- `telemetry`
- `sensitive_payload_redaction`
- `ai_cost_limit`

默认：

- 每个 job type 至少覆盖成功、重复提交、worker 崩溃/lease 过期、超时、取消、可重试错误、不可重试错误、死信和回放保护。
- AI job 必须覆盖 cost/token limit、model/provider timeout、background/batch status polling、fallback 或用户可见失败状态。
- 有副作用 job 必须覆盖幂等、重复尝试、补偿/回滚、审计和外部调用失败。

### `async-jobs/operations-review/<target>.md`

Operations review 必须包含：

- `Recent Changes`
- `Backlog / Latency`
- `Failures / Retries`
- `Dead Letters / Replays`
- `Cancellation / Expiry`
- `Cost / Capacity`
- `User Impact`
- `Incidents`
- `Open Risks`
- `Next One Change`

默认：

- pre-revenue 或低流量：每月复盘一次，或新 job type、新 schedule、新 worker、新供应商批处理上线前复盘。
- 有活跃用户：每两周复盘一次，或 backlog SLO 破坏、死信、批量失败、重复副作用、成本异常、用户投诉后复盘。
- 每次只选一个最高影响改进：缩短队列延迟、补取消、收紧重试、加 dead letter、修幂等、降并发、拆大 job、改用户状态 UI 或迁移托管队列。

## Go / Kratos / sqlc / gRPC 默认规则

- 异步任务必须是显式服务能力，不用匿名 goroutine、隐藏 cron、前端轮询触发写操作或 prompt 直接启动后台副作用。
- gRPC 默认定义：`SubmitJob`、`GetJob`、`CancelJob`、`ListJobs`、`RetryDeadLetterJob` 或等价 API；HTTP/BFF 只包装这些 usecase。
- gRPC metadata 传播 `actor_id`、`tenant_id`、`request_id`、`idempotency_key`、`job_id`、`traceparent`；服务端重新计算权限和租户。
- sqlc 默认表可包含：`async_job_types`、`async_jobs`、`async_job_attempts`、`async_job_events`、`async_job_results`、`async_job_dead_letters`、`async_job_schedules`、`async_job_cancellations`、`async_job_idempotency_keys`。
- Postgres 队列表默认用 status、priority、run_after、lease_expires_at、attempt_count、tenant_id、dedupe_key 建索引；claim job 必须在事务中完成。
- `FOR UPDATE SKIP LOCKED` 只用于 worker claim；读用户状态、统计和审计不要依赖它的一致视图。
- Worker 必须支持 context deadline、graceful shutdown、lease heartbeat 或短 lease、stuck job recovery、bounded concurrency 和 kill switch。
- 对外部副作用使用 outbox、幂等 key、补偿 action 或 W3 tool runtime gate；不能让 retry 重复发邮件、重复扣费、重复改权限。

## Vite 前端默认规则

- 用户可见长任务提交后必须返回 job id 或 task id，并提供状态页、toast/inline 状态或任务列表。
- 不使用无限 loading 代替后台任务状态；至少显示 queued/running/succeeded/failed/cancelled/expired 和最后更新时间。
- 能取消的 job 显示取消入口；不能取消的 job 说明原因、预计影响和结果通知方式。
- 失败状态给出用户可做的下一步：重试、修改输入、等待、联系客服、下载部分结果或查看审计/错误引用。
- 参考 Vercel/Geist 风格：后台任务 UI 应克制、状态清晰、错误明确、按钮少而精确，危险 replay/cancel/retry 不只靠颜色表达。

## AI workflow 默认规则

- 长推理、Batch API、background response、eval、RAG ingestion、embedding、agent 多步执行默认走异步 job。
- OpenAI background mode 需要记录 provider response id、polling 状态、terminal state、超时、取消策略和数据保留边界；ZDR 或强隐私路径必须人工确认。
- Batch API 只用于不要求即时响应的离线任务，例如 eval、分类、embedding、内容仓库处理；要记录 input file id、custom id、status、输出引用、24h 期望和回滚/重跑策略。
- AI job 必须有 token/cost budget、model route、prompt/workflow version、eval/safety refs、tool permission refs、result redaction 和用户可见失败状态。
- Agent job 默认有限 iteration、有限 tool fanout、有限 retry、有限 wall-clock duration；超限进入 failed/degraded/human_review，不继续排队自旋。

## 需要人判断的关键点

只把这些判断交给人：

- 是否引入新的 durable queue、workflow engine、cloud scheduler、Batch API 路线或后台供应商。
- 是否把用户可见核心路径改成异步，或上线没有状态查询/取消/失败解释的长任务。
- 是否允许有副作用 job 自动重试、回放 dead letter、批量 backfill、定时生产写操作或跨租户批处理。
- 是否接受无幂等、无 lease、无 max attempts、无 dead letter、无 graceful shutdown 或无 stuck recovery 的 worker。
- 是否在 job payload/result 中保留 raw prompt、raw response、raw tool output、未脱敏个人数据、文件正文或供应商原始响应。
- 是否提高并发、dispatch rate、retry 上限、Batch 规模、AI token/cost budget 或调度频率。
- 是否删除/重放 dead letter、修复 stuck job、补偿重复副作用或公开任务事故说明。
- 是否使用 OpenAI background mode 于 ZDR/强隐私路径，或改变 background/batch 结果保留策略。

其他字段完整性、状态机、JSON 枚举、测试覆盖、敏感内容扫描、OpenSpec linkage、positive/negative fixture 和基础验证由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“有哪些任务、状态契约是什么、worker 怎么跑、怎么测、怎么复盘”。
- 保留：人只判断新队列/供应商、核心路径异步化、副作用重试/回放、缺失幂等/租约/死信、敏感 payload、并发成本和隐私保留。
- 调整：不默认引入 Temporal/Kafka/Celery/云任务；先用 Postgres/sqlc job table 和清晰 contract，真实压力出现再迁移。
- 调整：不要求完整 DAG；一人公司先处理单阶段 job，复杂 pipeline 只在产品需要时拆成多个 job type。
- 风险：后台任务 UI 容易被低估。缓解：用户可见 job 必须有状态、失败解释、结果保留和取消/过期策略。

结论：可落地。一个人可以先为最重要的 AI 长任务写 3 到 5 个 job type，用 Postgres + worker 跑通幂等、取消、重试和死信，再用真实 backlog 决定是否换队列。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：长任务从“卡住的 loading”变成可查询、可取消、可恢复的用户体验。
- 工程角度：Go/Kratos/gRPC/sqlc 有清晰 job API、状态机、lease、attempt、idempotency 和表结构路径。
- 运维角度：backlog age、queue latency、retry、dead letter、stuck job、graceful shutdown 和 kill switch 支撑 SRE-lite。
- 安全隐私角度：payload/result 最小化，raw prompt/response/tool output 默认不存，dead-letter/replay 需要 checkpoint。
- 成本角度：AI job 的 token/cost、Batch 规模、worker concurrency 和 retry fanout 都有硬上限与复盘。

结论：可落地。本专项把后台任务从“代码里悄悄跑”变成可审查的产品/运维契约：能排队、能停止、能重试、能解释、能恢复。
