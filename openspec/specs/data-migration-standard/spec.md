# data-migration-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义一人公司数据与数据库迁移的最小规范，使 schema、query、migration、backfill、生产数据修复、备份恢复和隐私数据变更都可版本化、可检查、可恢复。

## Requirements

### Requirement: 生产数据变更必须有结构化 data change artifact

生产数据库 schema、query、migration、backfill、数据修复或隐私数据变更 MUST 在发布前具备 `data/changes/<change-id>.json`。

#### Scenario: 新增生产 migration

- GIVEN 一个变更会修改生产数据库
- WHEN 创建数据变更 artifacts
- THEN 创建 `data/changes/<change-id>.json`
- AND 文件包含 `change_id`、`service`、`owner`、`environment`、`type`、`risk`、`migration_files`、`backup`、`rollback`、`verification`

#### Scenario: 仅本地实验

- GIVEN 数据变更只用于本地一次性实验
- WHEN 不创建 data change artifact
- THEN 在 OpenSpec tasks 或 design 中记录豁免原因
- AND 不得把该变更用于 production

### Requirement: sqlc schema/query/code 必须同步

使用 sqlc 的服务 MUST 在 schema 或 query 变化后重新生成代码并执行 sqlc 验证或明确记录跳过原因。

#### Scenario: 修改 schema 或 query

- GIVEN `migrations/`、schema 文件或 `queries/` 发生变化
- WHEN 准备合并或发布
- THEN 运行 `sqlc generate`
- AND 运行 `sqlc vet` 或记录无法运行的原因、风险和补救
- AND 生成代码不得手工修改

#### Scenario: 需要动态 SQL

- GIVEN 变更需要动态 SQL 或无法由 sqlc 静态生成
- WHEN 设计数据访问层
- THEN 在 OpenSpec design 中说明原因
- AND 添加测试和输入边界

### Requirement: 生产迁移必须有备份、dry-run、验证和回滚

生产 migration MUST 在执行前具备备份策略、dry-run 或 staging 验证、post-check 和 rollback/compensation 说明。

#### Scenario: 生产迁移发布前

- GIVEN production data change artifact
- WHEN 评审发布门禁
- THEN `backup.required` 为 true 或记录明确豁免
- AND `verification.dry_run` 为 true 或记录无法 dry-run 的原因
- AND `verification.post_checks` 非空
- AND `rollback.strategy` 非空

#### Scenario: 高价值生产数据

- GIVEN 服务包含付费、权限、隐私或核心业务数据
- WHEN 准备高风险迁移
- THEN 确认 `data/restore/<service>.md` 存在
- AND 记录最近 restore drill 或人工接受风险

### Requirement: 破坏性或不可逆数据操作必须人工 checkpoint

DROP、TRUNCATE、批量 DELETE、不可逆 migration、隐私数据导出或删除 MUST 有人工 checkpoint。

#### Scenario: destructive SQL

- GIVEN migration 或 data fix 包含 DROP、TRUNCATE、DELETE、CASCADE、ALTER TYPE、SET NOT NULL 等高风险操作
- WHEN 准备 production release
- THEN `human_checkpoint.required` 为 true
- AND `rollback.data_loss_possible` 明确为 true 或 false
- AND 记录原因和恢复/补偿方案

#### Scenario: 隐私数据处理

- GIVEN 变更新增、导出、删除、匿名化或改变个人数据用途
- WHEN 创建 data change artifact
- THEN `privacy.personal_data` 或 `privacy.export_or_delete` 标记为 true
- AND `human_checkpoint.required` 为 true
- AND 记录用途、保留期或删除策略

### Requirement: Backfill 必须幂等、可暂停并可观测

生产 backfill MUST 具备批处理边界、幂等策略、checkpoint、限速、dry-run 或 sample mode、停止条件和观测信号。

#### Scenario: 创建 backfill

- GIVEN 需要迁移或补齐现有生产数据
- WHEN 创建 `data/backfills/<name>.md`
- THEN 文档包含 input scope、batch size、rate limit、checkpoint、idempotency、dry-run、stop condition、metrics
- AND data change artifact 引用该 backfill 文件

### Requirement: 数据恢复能力必须被记录

生产数据服务 MUST 记录备份来源、恢复步骤、验证方式、RPO/RTO 和最近演练状态。

#### Scenario: 新生产数据服务

- GIVEN 服务写入生产数据库
- WHEN 定义运维 artifacts
- THEN 创建 `data/restore/<service>.md`
- AND 文档包含 backup sources、restore steps、validation、RPO/RTO、last drill

#### Scenario: 尚未演练恢复

- GIVEN restore drill 尚未执行
- WHEN 准备发布
- THEN 在 data change artifact 或 release log 中记录风险
- AND 为付费或关键数据创建后续 task
