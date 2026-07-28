# 技术设计：异步任务、Webhook 与韧性

## 规范要求

<!-- rule-id: TECH-241-ROUTE-RETRY-POLICY -->
- route retry 须定义上限、backoff 和错误分类。

<!-- rule-id: TECH-241-SIDE-EFFECT-TOOL-RETRY-DEFAULT -->
- 有副作用工具缺省禁止自动重试。

<!-- rule-id: TECH-241-AUTOMATIC-RETRY-ELIGIBILITY -->
- 自动 retry 仅用于无副作用、可幂等且属于瞬时错误的调用。

<!-- rule-id: TECH-241-NO-BLIND-SIDE-EFFECT-RETRY -->
- 模型 route 层禁止盲目重试工具调用、支付、写数据或发通知。

<!-- rule-id: TECH-241-RETRY-LIMIT-EXPANSION-HUMAN-GATE -->
- 扩大 retry 上限须交由人工判断。

<!-- rule-id: TECH-238-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：分析调用失败时且事件不是合规或计费事实。分析失败禁止阻断核心业务流程。

<!-- rule-id: TECH-240-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：工作涉及所列表面时。对外 claim、供应商数据流或高成本 AI workflow 须有降级路径。

<!-- rule-id: TECH-238-RETRY-FALLBACK-RESILIENCE-S02 -->
- 适用情形：调用外部分析 provider 时。分析 provider client须具备：timeout、retry、backoff、drop policy、本地 fallback。

<!-- rule-id: TECH-240-RETRY-FALLBACK-RESILIENCE-S02 -->
- 适用情形：设计 AI 成本容量时。重试须有上限。

<!-- rule-id: TECH-123-ASYNC-JOB-WORKER-S02 -->
- 适用情形：执行客户数据删除、导出或同步时。数据作业须具备：dry-run、幂等、audit、状态、例外解释。

<!-- rule-id: TECH-240-RETRY-FALLBACK-RESILIENCE-S03 -->
- 适用情形：调用供应商时。供应商调用须具备：timeout、retry budget。

<!-- rule-id: TECH-124-ASYNC-JOB-WORKER-S01 -->
- 适用情形：引入基础设施时。新增队列须由人工判断。

<!-- rule-id: TECH-124-ASYNC-JOB-WORKER-S02 -->
- 适用情形：引入基础设施时。新增事件 broker 须由人工判断。

<!-- rule-id: TECH-225-NOTIFICATION-MESSAGING-S01 -->
- 适用情形：引入外部供应商时。新增支付、通知或开发者平台供应商须由人工判断。

<!-- rule-id: TECH-242-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：决定 实现交接边界时。接受没有取消能力或重试上限的实现进入下一步须由人工判断。

<!-- rule-id: TECH-125-ASYNC-JOB-WORKER-S01 -->
- 适用情形：设计管理入口时。高风险不可逆 worker 可保留进程隔离。

<!-- rule-id: TECH-118-ASYNC-JOB-CONTRACT-S01 -->
- 适用情形：不使用 foreign key 时。无 foreign key 时应用层须实现幂等控制。

<!-- rule-id: TECH-226-NOTIFICATION-MESSAGING-S01 -->
- 适用情形：扩大服务架构时。引入异步消息、事件溯源或分布式事务须由人工判断。

<!-- rule-id: TECH-119-ASYNC-JOB-CONTRACT-S01 -->
- 适用情形：实现前端写操作时。写操作须至少使用 disabled 状态或幂等 key 之一防止重复提交。

<!-- rule-id: TECH-121-ASYNC-JOB-CONTRACT-S01 -->
- 适用情形：实现外部副作用时。所有外部副作用须有幂等。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S02 -->
- 适用情形：处理入站 Webhook 时。入站 Webhook 须先验签；入站 Webhook 须去重；入站 Webhook 须持久化 inbox；入站 Webhook 须快速 ack。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S03 -->
- 适用情形：产生出站事件时。出站事件须与业务状态同事务写 outbox。

<!-- rule-id: TECH-227-NOTIFICATION-MESSAGING-S01 -->
- 适用情形：构建用户消息时。邮件、SMS 和 push 禁止包含 secret、完整 AI/用户内容或敏感数据。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S04 -->
- 适用情形：处理 Webhook 时。Webhook 处理禁止依赖顺序。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S01 -->
- 适用情形：应用异步 job 专项时。与本规范的正式分类及项目原则冲突时，以正式规范为准。

<!-- rule-id: TECH-243-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：实现生产后台任务时。后台任务须有限重试。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S02 -->
- 适用情形：实现生产后台任务时。后台任务须幂等。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S03 -->
- 适用情形：登记高风险 job 时。高风险 job须具备：幂等键、人工 checkpoint。

<!-- rule-id: TECH-243-RETRY-FALLBACK-RESILIENCE-S03 -->
- 适用情形：登记高风险 job 时。高风险 job 须有重试上限。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S04 -->
- 适用情形：存储 job payload 时。payload 缺省只能保存 schema 化输入；payload 禁止保存 raw AI/tool 内容、secret 或未脱敏个人数据；payload 缺省只能保存最小化输入；payload 缺省只能保存可重放输入。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S05 -->
- 适用情形：存储 job result 时。job row 禁止保存大文件、敏感正文或供应商原始响应。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S06 -->
- 适用情形：实现副作用 job 时。外部副作用须使用 outbox、幂等、补偿或 AI tool gate。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S07 -->
- 适用情形：扩大异步架构时。引入新队列、引擎、调度、Batch 或后台供应商须由人工判断。

<!-- rule-id: TECH-129-ASYNC-JOB-WORKER-S08 -->
- 适用情形：改变 job 数据保留时。job payload/result 保留 raw 或敏感内容须由人工判断。

<!-- rule-id: TECH-243-RETRY-FALLBACK-RESILIENCE-S04 -->
- 适用情形：扩大 job 容量时。提高 job 并发、速率、重试、规模、预算或频率须由人工判断。

<!-- rule-id: TECH-128-ASYNC-JOB-WORKER-S01 -->
- 适用情形：决定是否采用该专项时。异步 job 与 worker 专项是可选 playbook，不是缺省流程。

<!-- rule-id: TECH-120-ASYNC-JOB-CONTRACT-S01 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时幂等控制须承担引用完整性。

<!-- rule-id: TECH-244-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：设计 retry 时。retry须具备：上限、backoff、retry budget。

<!-- rule-id: TECH-228-NOTIFICATION-MESSAGING-S01 -->
- 适用情形：决定是否外部通知时。普通文案更正可以不通知；若错误涉及数据、安全、隐私、SLA、计费、AI 能力或合同承诺，通知决定须接受人工审查。


## 执行细则

<!-- rule-id: TECH-094-JOB-DEFAULT-STATE-MACHINE -->
- job contract 的缺省状态机须包含 `queued`、`leased`、`running`、`succeeded`、`failed`、`cancel_requested`、`cancelled` 和 `expired`。

<!-- rule-id: TECH-123-ASYNC-JOB-WORKER-S01 -->
- 适用情形：执行客户数据删除、导出或同步时。删除、导出和同步缺省使用异步 job。

<!-- rule-id: TECH-239-RETRY-FALLBACK-RESILIENCE-S01 -->
- 适用情形：定义 AI schema 时。每条 AI schema 须记录 fallback。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S01 -->
- 适用情形：触发 integration 工件时。event catalog 缺省位于 integrations/event-catalog/<target>.json。

<!-- rule-id: TECH-192-EVENT-WEBHOOK-S05 -->
- 适用情形：处理 Webhook 时。Webhook 状态不确定时须拉取 provider 当前对象状态。

<!-- rule-id: TECH-126-ASYNC-JOB-WORKER-S01 -->
- 适用情形：建立异步工件时。job registry 缺省位于 async-jobs/job-registry/<target>.json。

<!-- rule-id: TECH-126-ASYNC-JOB-WORKER-S02 -->
- 适用情形：编写 job registry 时。job registry须包含：target、owner、queues、job_types、schedules、storage、workers、rate_limits、retention、human_checkpoint、review_cadence。

<!-- rule-id: TECH-126-ASYNC-JOB-WORKER-S03 -->
- 适用情形：登记 queue 时。每个 queue须包含：id、purpose、priority、max_concurrency、dispatch_rate_per_minute、status。

<!-- rule-id: TECH-126-ASYNC-JOB-WORKER-S04 -->
- 适用情形：登记 job type 时。每个 job type须包含：id、name、queue、payload_schema_ref、result_schema_ref、trigger、side_effect_class、idempotency、dedupe_key、max_attempts、cancellation、progress、user_visible、data_policy、status。

<!-- rule-id: TECH-243-RETRY-FALLBACK-RESILIENCE-S02 -->
- 适用情形：登记 job type 时。每个 job type须包含：timeout_seconds、retry_policy。

<!-- rule-id: TECH-127-ASYNC-JOB-WORKER-S01 -->
- 适用情形：存储 job result 时。result 缺省保存引用、摘要、artifact id 或受控对象。

<!-- rule-id: TECH-122-ASYNC-JOB-QUEUE-INDEXES-S01 -->
- 适用情形：设计 Postgres 队列表时。Postgres 队列表缺省按 status 建索引；Postgres 队列表缺省按 priority 建索引；Postgres 队列表缺省按 run_after 建索引；Postgres 队列表缺省按 lease_expires_at 建索引；Postgres 队列表缺省按 attempt_count 建索引；Postgres 队列表缺省按 tenant_id 建索引；Postgres 队列表缺省按 dedupe_key 建索引。

<!-- rule-id: TECH-202-GOVERNANCE-ASYNC-JOB-WORKER-S01 -->
- 适用情形：使用 background mode 时。background mode须登记：provider response id、polling 状态、terminal state、超时、数据保留边界。
