# customer-data-portability-lifecycle-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

Define the minimum one-person-company governance for customer data import, export, sync, portability, deletion, third-party propagation, backup implications, AI/vector/cache residue, and data-rights lifecycle operations.

## Requirements

### Requirement: 客户数据搬运必须具备 lifecycle 工件

任何生产 target 只要导入、导出、同步、删除或响应客户数据权利请求，MUST 具备 customer-data artifacts。

#### Scenario: 新增客户数据导入导出能力

- GIVEN 一个 target 会导入、导出或同步客户数据
- WHEN 创建研发 OpenSpec change
- THEN 创建 `customer-data/data-map/<target>.json`
- AND 创建 `customer-data/transfer-contract/<target>.json`
- AND 创建 `customer-data/sync-runbook/<target>.md`
- AND 在 OpenSpec proposal 或 design 中链接 customer-data artifacts

#### Scenario: 新增删除或数据权利请求能力

- GIVEN 一个 target 会响应 access、export、rectification、deletion、restriction 或 stop_sync 请求
- WHEN 准备对真实用户开放
- THEN 创建 `customer-data/rights-deletion-policy/<target>.json`
- AND 创建 `customer-data/lifecycle-review/<target>.md`

### Requirement: Data map 必须定位主数据、派生数据、AI 数据、第三方和备份

Data map MUST 记录 systems of record、data sets、derived stores、external processors、AI stores、backup locations、identity keys、tenant boundary、retention classes、exportability、deletion classes、audit refs、人审点、复审节奏和状态。

#### Scenario: 创建 data map

- GIVEN 一个 target 处理客户数据
- WHEN 创建 `customer-data/data-map/<target>.json`
- THEN 每个 data set 包含 id、name、system_of_record、data_classification、contains_personal_data、contains_sensitive_data、tenant_scope、source、purpose、retention、export_policy、delete_policy、sync_targets、status
- AND derived_stores 覆盖 analytics、search、cache、RAG、embedding、AI memory、exports、logs、support summary 中适用项
- AND backup_locations 说明保留期和恢复后的再删除流程

### Requirement: Transfer contract 必须定义安全导入、导出和交换格式

Transfer contract MUST 记录 formats、import contracts、export contracts、schema policy、validation policy、security policy、privacy policy、limits、idempotency、error policy、audit policy、人审点和状态。

#### Scenario: 定义导入契约

- GIVEN 一个 target 允许客户导入数据
- WHEN 创建 transfer contract
- THEN 每个 import contract 包含 format、source、allowed_data_classes、schema_ref、field_mapping、validation、staging、dedupe_key、idempotency_key、dry_run_required、rollback_or_compensation、status
- AND 导入默认先进入 staging 或等价隔离状态
- AND 文件导入覆盖格式白名单、大小限制、内容验证和权限检查

#### Scenario: 定义导出契约

- GIVEN 一个 target 允许客户导出数据
- WHEN 创建 transfer contract
- THEN 每个 export contract 包含 format、audience、included_data_sets、excluded_data_sets、redaction、csv_injection_protection、delivery_method、expiry、access_control、status
- AND 导出默认排除 secret、token、password、session cookie、其他租户数据、第三方受限数据、raw prompt/response 和内部安全日志

### Requirement: Sync runbook 必须定义 source of truth、幂等、冲突和删除传播

Sync runbook MUST 说明系统、主权来源、身份映射、同步方向、初始导入、增量同步、冲突解决、幂等去重、回放、删除传播、限流背压、观测、事故动作和链接工件。

#### Scenario: 外部系统同步客户数据

- GIVEN 一个 target 与外部系统同步客户数据
- WHEN 创建 `customer-data/sync-runbook/<target>.md`
- THEN runbook 包含 Source Of Truth、Identity Mapping、Sync Direction、Incremental Sync、Conflict Resolution、Idempotency / Dedupe、Deletion / Tombstone Propagation、Rate Limits / Backpressure、Observability、Incident Actions
- AND 双向同步、跨租户匹配或静默覆盖需要 human_checkpoint

### Requirement: Rights deletion policy 必须覆盖请求、验证、范围、删除目标、第三方和备份

Rights deletion policy MUST 记录 request types、identity verification、scope resolution、workflow、deletion targets、export targets、third-party propagation、backup policy、exceptions、SLA、audit policy、人审点和状态。

#### Scenario: 处理删除请求

- GIVEN 一个用户或客户请求删除数据
- WHEN 创建或执行 deletion job
- THEN deletion_targets 覆盖主库、对象存储、cache、search index、RAG chunks、embedding/vector store、AI memory、conversation/application state、analytics join key、support summaries、exports 和第三方同步目标中适用项
- AND 每个 target 包含 system、data_sets、method、mode、verification、retention_exception、status

#### Scenario: 存在删除例外

- GIVEN 数据因 billing/tax、security/audit、fraud、legal hold、contract obligation、backup retention 或 supplier limitation 不能立即删除
- WHEN 响应删除请求
- THEN policy 记录例外原因、保留期、访问限制、复审日期和用户可解释文本
- AND human_checkpoint 包含 deletion_exception 或等价条目

### Requirement: Lifecycle review 必须定期验证搬运与删除链路

Lifecycle review MUST 记录 recent changes、imports、exports、sync health、deletion/rights requests、third-party propagation、AI/vector/cache coverage、backup/restore implications、security/privacy findings、incidents、open risks、one next change 和 review cadence。

#### Scenario: 高影响数据动作前复盘

- GIVEN 即将执行租户级导出、批量导入、双向同步、不可逆删除、第三方迁出或 AI/vector 删除
- WHEN 做出执行决策
- THEN `customer-data/lifecycle-review/<target>.md` 不得过期
- AND 不存在未解释的导入失败、错误导出、同步错配、删除失败、第三方传播失败、AI 残留、备份恢复再删除缺口或隐私发现
