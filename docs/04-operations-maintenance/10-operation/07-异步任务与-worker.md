# 运行：异步任务与 worker

## 执行细则

<!-- rule-id: OPERATION-JOB-001 -->
只有 job type 完成生产登记后，异步任务才可投入运行；prompt、tool、admin action、webhook 与 cron 均不得启动未登记类型。

<!-- rule-id: OPERATION-JOB-002 -->
worker runbook 默认位于 `async-jobs/worker-runbook/<target>.md`，必须包含 Scope、Start/Shutdown、Enqueue、Dequeue/Lease、Execute、Cancellation、Dead Letter/Replay、Incident Actions 与 Linked Artifacts。

<!-- rule-id: OPERATION-JOB-003 -->
`max_attempts` 必须有限；job contract 包含 `dead_letter_policy`，默认状态机包含 `dead_lettered`。重试耗尽、不可重试或风险错误进入 dead letter，并经明确 replay 审查；高风险 job 必须有死信路径。每次尝试记录 retry decision；副作用自动重试、回放、backfill、定时写或跨租户批处理必须人审。

<!-- rule-id: OPERATION-JOB-004 -->
worker 抢占 job 必须在事务中按 deterministic order 使用 lease 或 lock。

<!-- rule-id: OPERATION-JOB-005 -->
每次尝试必须记录 attempt、开始与结束时间、错误分类、queue age、duration、worker id 与结果引用。

<!-- rule-id: OPERATION-JOB-006 -->
收到 shutdown 后停止领取新 job；当前 job 必须完成或释放/等待 lease 过期，进程退出不得丢失隐式内存状态。

<!-- rule-id: OPERATION-JOB-007 -->
job registry 必须包含 telemetry；每个 queue 定义 `backlog_slo` 与 `oldest_age_slo`；高风险 job 具有观测字段，worker runbook 包含 Observability。

<!-- rule-id: OPERATION-JOB-008 -->
删除或回放死信、修复 stuck job、补偿重复副作用或公开事故必须人工判断。
