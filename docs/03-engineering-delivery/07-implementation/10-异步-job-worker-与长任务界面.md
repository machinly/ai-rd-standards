# 实现：异步 job、worker 与长任务界面

## 规范要求

<!-- rule-id: IMPL-BACKGROUND-JOB-CONTRACT -->
- 生产后台任务须有显式 job contract，并定义取消策略、观测接口、恢复路径和人工 checkpoint。

<!-- rule-id: IMPL-CLAIM-SQL-ADAPTER-BOUNDARY -->
- 确实需要数据库专有 claim SQL 时，只能隔离在 repository 适配层。

<!-- rule-id: IMPL-USER-VISIBLE-JOB-CONTRACT -->
- 用户可见 job 须提供状态查询、可理解失败原因、结果保留期以及取消与过期策略。

<!-- rule-id: IMPL-SERVER-OWNED-JOB-STATE -->
- job 状态转换须由服务端控制，禁止前端或模型直接写入最终状态。

<!-- rule-id: IMPL-JOB-LEASE-RECOVERY -->
- `leased` 状态须有 `lease_expires_at` 或等价超时；worker 崩溃后，任务须可重新领取或进入 stuck recovery。

<!-- rule-id: IMPL-SKIP-LOCKED-QUEUE-ONLY -->
- `SKIP LOCKED` 只用于 queue-like table 的 worker claim。

<!-- rule-id: IMPL-JOB-EXECUTION-CONTEXT -->
- worker 执行前须绑定 trace id、job id、attempt id、actor、tenant、deadline、cost budget 与 cancellation token。

<!-- rule-id: IMPL-EXPLICIT-ASYNC-SERVICE -->
- 后台异步工作须暴露为明确的服务能力。任何副作用都不得由 prompt 直接发起，也不得借前端轮询写操作、未公开的 cron 或匿名 goroutine 隐式启动。

<!-- rule-id: IMPL-SKIP-LOCKED-NOT-READ-MODEL -->
- 用户状态、统计与审计查询禁止依赖 `SKIP LOCKED` 提供一致视图。

<!-- rule-id: IMPL-WORKER-RUNTIME-CONTROLS -->
- worker 须支持 context deadline、graceful shutdown、lease heartbeat 或短 lease 二者之一、stuck job recovery、bounded concurrency 与 kill switch。

<!-- rule-id: IMPL-LONG-JOB-ID-AND-SURFACE -->
- 用户可见长任务提交后须返回 job id 或 task id，并提供状态页、toast/inline 状态或任务列表中的可见状态表面。

<!-- rule-id: IMPL-LONG-JOB-STATUS-SET -->
- 长任务界面禁止无限 loading，至少显示 `queued`、`running`、`succeeded`、`failed`、`cancelled`、`expired` 与最后更新时间。

<!-- rule-id: IMPL-CANCELLABLE-JOB-ENTRY -->
- 可取消 job 须显示取消入口。

<!-- rule-id: IMPL-NONCANCELLABLE-JOB-EXPLANATION -->
- 不可取消 job 须说明原因、预计影响与结果通知方式。

<!-- rule-id: IMPL-JOB-FAILURE-NEXT-ACTION -->
- 失败状态须给出可执行下一步，例如重试、修改输入、等待、联系客服、下载部分结果或查看审计/错误引用。

<!-- rule-id: IMPL-LONG-AI-WORK-ASYNC-DEFAULT -->
- 长推理、Batch、background、eval、RAG、embedding 与 agent 多步缺省走异步 job。

<!-- rule-id: IMPL-AI-JOB-CONTROL-FIELDS -->
- AI job 须记录 token budget、cost budget、model route、prompt 或 workflow version、eval/safety refs、tool permission refs、result redaction 与用户可见失败状态。

<!-- rule-id: IMPL-AGENT-JOB-BOUNDS -->
- Agent job 缺省限制 iteration、tool fanout、retry 与 wall-clock duration；超限时进入 `failed`、`degraded` 或 `human_review`，禁止继续排队自旋。
