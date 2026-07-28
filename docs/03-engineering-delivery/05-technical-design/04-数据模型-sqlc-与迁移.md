# 技术设计：数据模型、sqlc 与迁移

## 规范要求

<!-- rule-id: TECH-134-SQLC-TENANT-OWNER-CONSTRAINT -->
- 访问租户数据的 sqlc query 须显式约束 tenant 或 owner。

<!-- rule-id: TECH-252-SCHEMA-DATA-PRODUCT-ANALYTICS-EXPERIMENT-S01 -->
- 适用情形：定义事件属性时。事件属性缺省只允许 plan、role、source、status、error_class、latency_bucket、cost_bucket、variant、surface、template_id 这些低基数字段。

<!-- rule-id: TECH-223-MIGRATION-DESIGN-S01 -->
- 适用情形：选择版本迁移策略时。多版本并行或强制迁移须交由人工判断。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S01 -->
- 适用情形：AI 输出供程序消费时。程序消费 AI 输出时缺省使用 Structured Outputs 或 JSON schema，不默认让下游解析自由文本。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S03 -->
- 适用情形：决定是否创建 schema.json 时。仅程序消费结构化输出时 schema.json 必需。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S01 -->
- 适用情形：选择数据存储时。没有明确理由禁止引入多个数据存储。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S02 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时应用逻辑须承担引用完整性。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S05 -->
- 适用情形：实施数据库变更时。所有数据库变更须进入版本控制。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S02 -->
- 适用情形：编写 migration 时。一次 migration 仅允许做一个目的清楚的变更。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S03 -->
- 适用情形：实施高风险生产数据变更时。生产删除、批量更新、破坏性 SQL、不可逆 migration 或隐私导出须设置人工 checkpoint。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S04 -->
- 适用情形：实施数据修复或 backfill 时。数据修复和 backfill 禁止混入普通 schema migration。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S06 -->
- 适用情形：编写 SQL 文件时。SQL 文件禁止存真实生产数据、secret、token、完整导出或隐私样本。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S03 -->
- 适用情形：编写 query 时。query 名称须表达业务意图。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S08 -->
- 适用情形：编写 schema/query 时。schema 和 query 禁止默认使用数据库专有能力或隐式转换。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S05 -->
- 适用情形：设计跨表关系时。无 foreign key 的跨表关系须具备：并发策略、孤儿检测、修复方式。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S11 -->
- 适用情形：执行生产迁移时。生产迁移 code 阶段须兼容新旧 schema。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S07 -->
- 适用情形：设计 backfill 时。backfill 须幂等或有去重键。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S08 -->
- 适用情形：规划生产 migration 时。接受停机窗口或锁表风险须由人工判断。

<!-- rule-id: TECH-248-SCHEMA-DATA-CONFIGURATION-FEATURE-FLAG-S03 -->
- 适用情形：配置 Vite env 时。Vite env 禁止包含 key、token、数据库 URL 或 JWT secret。

<!-- rule-id: TECH-250-SCHEMA-DATA-EXTERNAL-SIDE-EFFECTS-S01 -->
- 适用情形：扩大外部集成时。新 provider、公开 webhook、订阅事件或 breaking schema 须由人工判断。

<!-- rule-id: TECH-218-JOB-CLAIM-TRANSACTION-S01 -->
- 适用情形：实现 worker claim 时。claim job 须在事务中完成。

<!-- rule-id: TECH-217-JOB-CLAIM-SQL-PORTABILITY-S01 -->
- 适用情形：设计队列 claim SQL 时。数据库专有 skip-locked/claim 语法禁止作为默认核心 SQL。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S06 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时事务须承担引用完整性。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S07 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时须按关系需要使用唯一或非空约束承担引用完整性。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S08 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时删除策略须承担引用完整性。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S09 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时补偿任务须承担引用完整性。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S10 -->
- 适用情形：设计无 FK 关系时。不使用 foreign key 时定期一致性扫描须承担引用完整性。

<!-- rule-id: TECH-183-DATABASE-TABLE-SCHEMA-S02 -->
- 适用情形：持久化客户上线状态时。客户上线 sqlc 表仅允许存引用、状态和脱敏摘要。


## 执行细则

<!-- rule-id: TECH-252-SCHEMA-DATA-PRODUCT-ANALYTICS-EXPERIMENT-S02 -->
- 适用情形：创建 tracking plan 时。schema policy须登记：命名规则、属性类型、低基数要求、版本策略、弃用方式。

<!-- rule-id: TECH-180-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：存储产品事件且该状态适用时。sqlc 表须区分：适用的 raw ingestion、适用的 schema violation、适用的 experiment assignment、适用的 exposure、适用的 suppression/deletion state。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S02 -->
- 适用情形：建立 AI artifact 时。结构化输出 schema 缺省位于 ai/schemas/<capability>.schema.json。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S04 -->
- 适用情形：输出为纯展示文本时。纯展示文本可在 design 中说明无需 schema。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S05 -->
- 适用情形：按默认顺序推进 AI change 时。需要结构化输出时须写 JSON Schema。

<!-- rule-id: TECH-253-SCHEMA-DATA-PROMPT-EVAL-AGENT-WORKFLOW-S06 -->
- 适用情形：设计结构化输出 schema 时。结构化输出 schema 须设置必要字段；结构化输出 schema 须设置 additionalProperties false。

<!-- rule-id: TECH-245-SCHEMA-DATA-AI-CONTEXT-MEMORY-RETRIEVAL-S01 -->
- 适用情形：触发上下文治理工件时。preference schema 缺省位于 ai-context/preference-schema/<capability>.json。

<!-- rule-id: TECH-245-SCHEMA-DATA-AI-CONTEXT-MEMORY-RETRIEVAL-S02 -->
- 适用情形：登记上下文来源时。source registry须登记：owner、scope、system of record、access check、license 或 rights、data classification、deletion policy。

<!-- rule-id: TECH-246-SCHEMA-DATA-AI-RUNTIME-ROUTING-TOOLS-S01 -->
- 适用情形：实现 AI workflow 时。结构化输出应优先考虑使用 schema。

<!-- rule-id: TECH-221-MIGRATION-BACKFILL-DATA-FIX-S01 -->
- 适用情形：实现数据访问时。schema 和 migration 须先于 query。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S01 -->
- 适用情形：选择数据存储时。缺省数据库为 MySQL。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S01 -->
- 适用情形：实施数据变更时。数据变更缺省使用 SQL migration 和 sqlc，不以 ORM 作为数据访问主路径。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S02 -->
- 适用情形：编写 SQL 时。缺省优先使用 MySQL/PostgreSQL 通用 SQL。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S03 -->
- 适用情形：使用数据库专有能力时。专有 SQL 须隔离；专有 SQL 须标注；专有 SQL 须提供替代路径或锁定理由之一。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S05 -->
- 适用情形：同步 schema/query/code 时。sqlc 同步第一步须写 migration 或 schema 变化。

<!-- rule-id: TECH-222-MIGRATION-BACKFILL-DATA-FIX-S06 -->
- 适用情形：运行 sqlc vet 时。需要数据库连接的 vet rule 须先在临时库应用 migration。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S07 -->
- 适用情形：配置 sqlc 时。sqlc.yaml 须使用 version 2。

<!-- rule-id: TECH-206-GOVERNANCE-DATA-MIGRATION-S04 -->
- 适用情形：编写 query 时。写操作须明确事务边界。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S09 -->
- 适用情形：编写 schema/query 时。使用数据库专有能力时须登记：engine lock-in、替代路径。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S10 -->
- 适用情形：执行生产迁移时。生产迁移 expand 阶段添加兼容 schema。

<!-- rule-id: TECH-249-SCHEMA-DATA-DATA-MIGRATION-S12 -->
- 适用情形：新增个人数据字段时。新增个人数据字段须说明访问边界。

<!-- rule-id: TECH-248-SCHEMA-DATA-CONFIGURATION-FEATURE-FLAG-S01 -->
- 适用情形：编写配置注册表时。配置注册表须包含：target、owner、stack、secrets_policy、validation、startup_checks、reload_policy、drift_detection、human_checkpoint、review_cadence。

<!-- rule-id: TECH-248-SCHEMA-DATA-CONFIGURATION-FEATURE-FLAG-S02 -->
- 适用情形：登记 flag 时。每个 flag 须包含 owner。

<!-- rule-id: TECH-181-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：设计 sqlc 异步存储时。可按职责选建下列九张表，均非必需：
  - 类型与主记录：`async_job_types`、`async_jobs`。
  - 执行历史：`async_job_attempts`、`async_job_events`、`async_job_results`。
  - 失败与调度：`async_job_dead_letters`、`async_job_schedules`。
  - 取消与幂等：`async_job_cancellations`、`async_job_idempotency_keys`。

<!-- rule-id: TECH-217-JOB-CLAIM-SQL-PORTABILITY-S02 -->
- 适用情形：使用数据库专有 claim SQL 时。使用专有 claim SQL 时须登记：MySQL/PostgreSQL 差异、替代路径。

<!-- rule-id: TECH-224-MIGRATION-DESIGN-S01 -->
- 适用情形：使用自有应用模板时。批准自有模板后须记录迁移边界。

<!-- rule-id: TECH-182-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：需要持久化 UX 证据时。sqlc 允许按需包含 ux_feedback_events 表；sqlc 允许按需包含 ai_output_feedback 表；sqlc 允许按需包含 accessibility_exceptions 表；sqlc 允许按需包含 ui_incident_reports 表。

<!-- rule-id: TECH-183-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：需要持久化客户上线状态时。sqlc 允许按需选择包含 customer_launches 表；sqlc 允许按需选择包含 tenant_provisioning_events 表；sqlc 允许按需选择包含 tenant_entitlements 表；sqlc 允许按需选择包含 customer_readiness_gates 表；sqlc 允许按需选择包含 customer_success_reviews 表。

<!-- rule-id: TECH-184-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：需要持久化 claim control 时。sqlc 允许按需选择包含 external_claims 表；sqlc 允许按需选择包含 claim_surfaces 表；sqlc 允许按需选择包含 claim_evidence_links 表；sqlc 允许按需选择包含 claim_release_gates 表；sqlc 允许按需选择包含 claim_correction_events 表；sqlc 允许按需选择包含 claim_reviews 表。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`admin_actions` 表缺省存在。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S02 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`admin_action_runs` 表缺省存在。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S03 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`admin_approvals` 表缺省存在。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S04 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`audit_events` 表缺省存在。

<!-- rule-id: TECH-185-DATABASE-TABLE-SCHEMA-S05 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`break_glass_sessions` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_cases` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S02 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_events` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S03 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_feedback_links` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S04 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_template_versions` 表缺省存在。

<!-- rule-id: TECH-186-DATABASE-TABLE-SCHEMA-S05 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。`support_review_items` 表缺省存在。

<!-- rule-id: TECH-187-DATABASE-TABLE-SCHEMA-S01 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。sqlc 允许按需选择表：`ai_quality_signals`、`ai_quality_incidents`、`ai_quality_actions`、`ai_quality_reviews`。
