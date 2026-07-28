# 实现：数据变更、migration、backfill 与修复

## 规范要求

<!-- rule-id: IMPL-DATA-CHANGE-VERSION-CONTROL -->
- schema、query、migration、backfill、数据修复、备份恢复实现与隐私处理产物须进入版本控制。

<!-- rule-id: IMPL-DATA-DEFAULT-STACK -->
- 数据变更缺省栈为 MySQL、sqlc 与 Go/Kratos。

<!-- rule-id: IMPL-MIGRATION-TOOL-DEFAULT -->
- migration 工具不强制绑定；新 Go 服务没有既有选择时，缺省采用可版本化 SQL migration。

<!-- rule-id: IMPL-DOWN-MIGRATION-SAFETY -->
- 只有确实安全时才提供 down migration。

<!-- rule-id: IMPL-HIGH-RISK-MIGRATION-FORWARD-RECOVERY -->
- 涉及已写入数据、审计或身份关系时，优先采用前向恢复、禁用写路径或补偿，不把 down 当作缺省恢复方案。

<!-- rule-id: IMPL-NO-RETROACTIVE-PROD-DDL -->
- 禁止先在生产执行临时 DDL/DML 再补文件或文档。

<!-- rule-id: IMPL-SCHEMA-QUERY-GENERATE-CODE-ORDER -->
- 数据变更顺序须保持为 schema、query、sqlc 生成、代码调用。

<!-- rule-id: IMPL-NO-LOCAL-PROD-MIGRATION -->
- 禁止从开发者本地直接连接生产执行 migration。

<!-- rule-id: IMPL-DATA-ARTIFACT-PATHS -->
- 数据工件缺省路径为：`migrations/`；顺序编号的 `000001_<slug>.up.sql`；确实安全时对应的 `000001_<slug>.down.sql`；`queries/`；`sqlc.yaml`；`data/changes/<change-id>.json`；`data/backfills/<name>.md`；`data/fixes/YYYY-MM-DD-<slug>.md`。

<!-- rule-id: IMPL-EXISTING-DATA-PATH-RECORD -->
- 既有服务须沿用仓库的数据目录模式，并须在 data change JSON 中写清实际路径。

<!-- rule-id: IMPL-DATA-CHANGE-CORE-SCHEMA -->
- data change JSON 须记录 `change_id`、`service`、`owner`、`environment`、`type`、`risk`、`migration_files`、`query_files` 与 `deploy_order`。

<!-- rule-id: IMPL-DATA-CHANGE-SQLC-SCHEMA -->
- data change JSON 的 `sqlc` 块须记录 `config`、`generate` 与 `vet`。

<!-- rule-id: IMPL-DATA-CHANGE-ROLLBACK-SCHEMA -->
- data change JSON 的 `rollback` 块须记录 `strategy` 与 `data_loss_possible`。

<!-- rule-id: IMPL-DATA-CHANGE-VERIFICATION-SCHEMA -->
- data change JSON 的 verification 信息须记录 `dry_run` 与 `post_checks`；验证结论由验证项目维护。

<!-- rule-id: IMPL-DATA-CHANGE-PRIVACY-SCHEMA -->
- data change JSON 的 `privacy` 块须记录 `personal_data`、`retention_change` 与 `export_or_delete`。

<!-- rule-id: IMPL-DATA-CHANGE-HUMAN-CHECKPOINT-SCHEMA -->
- data change JSON 的 `human_checkpoint` 块须记录 `required` 与 `reason`。

<!-- rule-id: IMPL-PRODUCTION-DATA-CHANGE-RECORD -->
- 每个生产数据变更须在 `data/changes/*.json` 下形成记录；具体文件采用 `data/changes/<change-id>.json`，并包含 rollback 说明。

<!-- rule-id: IMPL-FIX-BACKFILL-RECORD -->
- 数据修复与 backfill 须分别记录在 `data/fixes` 或 `data/backfills`。

<!-- rule-id: IMPL-DATA-SYNC-UPDATE-QUERY -->
- schema 改变后须更新 `queries/*.sql`。

<!-- rule-id: IMPL-DATA-SYNC-GENERATE -->
- query 更新后须运行 `sqlc generate`。

<!-- rule-id: IMPL-DATA-SYNC-REPOSITORY-TESTS -->
- sqlc vet 后须更新 Go repository code 与 tests。

<!-- rule-id: IMPL-DATA-SYNC-NO-GENERATED-EDIT -->
- 同步完成后须确认生成代码没有手工修改。

<!-- rule-id: IMPL-PRODUCTION-BACKFILL-CONTROLS -->
- 生产 backfill 须限速、可重试并可暂停。

<!-- rule-id: IMPL-BACKFILL-DESIGN-FIELDS -->
- backfill 须定义输入范围、batch size、rate limit 与 checkpoint。

<!-- rule-id: IMPL-BACKFILL-BATCH-PROGRESS -->
- backfill 每批须记录成功数、失败数、跳过数与最后处理位置。

<!-- rule-id: IMPL-BACKFILL-DRY-OR-SAMPLE -->
- backfill 须提供 dry-run 或 sample mode 二者之一。

<!-- rule-id: IMPL-BACKFILL-STOP-AND-FAILURE -->
- backfill 须定义停止条件与失败动作。

<!-- rule-id: IMPL-BACKFILL-NONPEAK-DEFAULT -->
- backfill 不得把高峰期作为缺省运行时段。

<!-- rule-id: IMPL-PRODUCTION-DATA-FIX-PATH -->
- 生产数据修复须写入 `data/fixes/YYYY-MM-DD-<slug>.md`。

<!-- rule-id: IMPL-DATA-FIX-RECORD-FIELDS -->
- data fix 记录须包含 `Date`、`Service`、`Tables`、`User impact`、`Reason`、`SQL/migration`、`Rollback/compensation` 与 `Owner`。

<!-- rule-id: IMPL-MANUAL-SQL-FILE-REVIEW -->
- 手工 SQL 在执行前须先写成文件并 review。

<!-- rule-id: IMPL-EMERGENCY-SQL-AFTERCARE -->
- 事故止血先执行手工 SQL 时，事后须补文件以及 incident 或 release log。

<!-- rule-id: IMPL-NO-PURPOSELESS-DATA -->
- 禁止收集没有明确产品目的的数据。

<!-- rule-id: IMPL-PERSONAL-FIELD-PURPOSE-RETENTION -->
- 新增个人数据字段须说明用途与保留期。

<!-- rule-id: IMPL-BACKUP-DELETION-FOLLOWUP -->
- 备份含个人数据时，删除请求须说明备份保留期与恢复后的再删除流程。

<!-- rule-id: IMPL-DESTRUCTIVE-DATA-HUMAN-GATE -->
- 生产删除、`TRUNCATE`、`DROP`、批量 `DELETE`、不可逆 migration 或个人数据导出任一发生时，须设置人工 checkpoint；是否允许这些高影响动作由人判断。

<!-- rule-id: IMPL-CI-PRODUCTION-MIGRATION-HUMAN-GATE -->
- 是否允许 CI 自动执行 production migration 必须交由人工判断。

<!-- rule-id: IMPL-PERSONAL-DATA-CHANGE-HUMAN-GATE -->
- 新增、导出、删除个人或敏感数据，或改变其用途，须交由人工判断。
