# 阶段 7：数据与数据库迁移规范 v0.1

## 目标

为一人公司定义一套可落地的数据变更规范：所有 schema、query、migration、backfill、生产数据修复、备份恢复和隐私数据处理都进入版本控制，并能在发布前被检查。目标不是成为 DBA 团队，而是在一个人维护产品时保护最难恢复的资产：数据。

本阶段默认技术栈：PostgreSQL + sqlc + Go/Kratos。migration 工具不强绑定；新 Go 服务没有既有选择时，默认使用 `golang-migrate/migrate` 风格的 `*.up.sql` / `*.down.sql` 文件。

## 本阶段只解决什么

- 数据变更的最小仓库工件。
- sqlc schema/query/migration 的同步关系。
- 生产迁移的备份、dry-run、验证和回滚要求。
- expand / migrate / contract 的零停机默认路径。
- backfill 和生产数据修复的边界、幂等、限速和观测。
- 隐私数据、删除、匿名化、保留期和导出风险的人工 checkpoint。
- 数据迁移 skill 与本地检查脚本。

不在本阶段展开：完整数据平台、数据仓库、CDC 管道、多主复制、跨区域一致性、企业数据治理委员会、复杂 PII 分类系统。这些需要真实业务规模时再开独立 OpenSpec change。

## 依据转译

- 《人月神话》：数据库工具、迁移框架和 ORM 都不是银弹；真正的风险来自不可见耦合、隐含状态和无法回滚的决策。
- 小型项目管理：一人公司只保留能防止数据丢失、恢复上下文和减少事故损失的工件。
- Designing Data-Intensive Applications：数据系统的核心目标是可靠、可维护、可演进；选择数据库和一致性策略要服务产品事实，而不是追逐流行架构。
- Database Reliability Engineering：数据库可靠性是 SRE 思想在数据层的落地，优先保护数据、自动化重复操作、消除“数据库是特殊雪花”的壁垒。
- Evolutionary Database Design：所有数据库 artifacts 应与应用代码一起版本化；所有数据库变化都应是 migrations；每个变更越小越容易验证和恢复。
- PostgreSQL 官方文档：备份不是一个抽象口号，至少要理解 SQL dump、文件系统备份、连续归档/PITR 的边界；`pg_dump` 是一致快照但不替代 WAL/PITR。
- PostgreSQL DDL 文档：`ALTER TABLE`、默认值、约束、类型变化等会影响现有数据和锁；不可假设所有 DDL 都是轻量操作。
- sqlc 官方文档：sqlc 以 schema 和 queries 生成 Go 代码；`sqlc vet` 可对 queries 做 lint/prepare 检查，但依赖已更新 schema 的数据库或 managed database。
- golang-migrate：迁移按顺序应用到数据库，常见约定是每个 migration 有 up/down 文件。
- OWASP Database Security：数据库需要定期备份，备份需要权限保护，理想情况下加密。
- NIST Privacy Framework / GDPR 原则：个人数据处理需要管理隐私风险，并遵循最小化、保留限制和安全性思路。

## 默认决策

- 默认数据库是 PostgreSQL；没有明确理由不引入多个数据存储。
- 默认使用 SQL migration + sqlc，不使用 ORM 作为数据访问主路径。
- 默认所有数据库变更都进版本控制，禁止生产临时 DDL/DML 后再补文档。
- 默认 schema 先变更、query 后适配、sqlc 再生成、代码再调用。
- 默认生产迁移由 release pipeline 执行或记录；不从开发者本地直接连生产执行。
- 默认小步迁移：一次 migration 只做一个目的清楚的变更。
- 默认高风险数据变更走 expand / migrate / contract，而不是一次性 rename/drop/alter。
- 默认生产数据删除、批量 UPDATE、DROP、TRUNCATE、不可逆 migration、隐私数据导出都需要人工 checkpoint。

## 数据 artifact 目录规范

推荐落点：

```text
migrations/
  000001_create_workspaces.up.sql
  000001_create_workspaces.down.sql
queries/
  workspaces.sql
sqlc.yaml
data/
  changes/<change-id>.json
  backfills/<name>.md
  restore/<service>.md
  fixes/YYYY-MM-DD-<slug>.md
```

如果已有服务使用 `db/migrations`、`internal/data/queries` 或其他目录，沿用仓库模式，但必须在 `data/changes/<change-id>.json` 中写清路径。

`data/changes/<change-id>.json` 是机器可检查的事实来源：

```json
{
  "change_id": "2026-06-add-workspace-plan",
  "service": "billing-api",
  "owner": "founder",
  "environment": "production",
  "type": "schema",
  "risk": "medium",
  "migration_files": [
    "migrations/000018_add_workspace_plan.up.sql",
    "migrations/000018_add_workspace_plan.down.sql"
  ],
  "query_files": ["queries/workspaces.sql"],
  "sqlc": {
    "config": "sqlc.yaml",
    "generate": true,
    "vet": true
  },
  "deploy_order": ["expand", "code", "migrate", "contract"],
  "backup": {
    "required": true,
    "method": "managed snapshot or pg_dump -Fc",
    "restore_tested": false
  },
  "rollback": {
    "strategy": "down migration plus feature flag off",
    "data_loss_possible": false
  },
  "verification": {
    "dry_run": true,
    "post_checks": ["row count unchanged", "new writes populate plan"]
  },
  "privacy": {
    "personal_data": false,
    "retention_change": false,
    "export_or_delete": false
  },
  "human_checkpoint": {
    "required": true,
    "reason": "production schema migration"
  }
}
```

一人公司裁剪规则：

- 低风险本地 schema 变更可以只写 migration/query/sqlc，不写长设计；生产变更必须写 `data/changes/*.json`。
- 每个 production 数据变更必须有 rollback 说明，即使 down migration 只是“不可逆，使用备份/补偿/disable switch”。
- 数据修复和 backfill 不混在普通 schema migration 里；写入 `data/fixes` 或 `data/backfills`。
- SQL 文件不存真实生产数据、密钥、访问 token、完整用户导出或隐私样本。

## sqlc 与 schema/query 同步

默认顺序：

1. 写 migration 或 schema 变化。
2. 更新 `queries/*.sql`。
3. 运行 `sqlc generate`。
4. 运行 `sqlc vet`；需要数据库连接的 rules 先把 migration 应用到临时数据库。
5. 更新 Go repository code 和 tests。
6. 确认生成代码无手改。

规则：

- `sqlc.yaml` 使用 version 2。
- query 名称表达业务意图，不以表操作命名为主。
- 写操作明确事务边界。
- 动态 SQL 必须在 OpenSpec `design.md` 说明原因和测试策略。
- 删除或重命名字段前，先查所有 query、API、后台任务、AI prompt/schema、报表和外部导出。

## Production migration 安全路径

生产迁移默认走：

1. Preflight：确认 OpenSpec、data change JSON、release pipeline、SRE-lite release checklist。
2. Backup：确认最新备份可用；高风险变更需要最近一次 restore drill 或可执行恢复步骤。
3. Dry-run：在临时库或 staging 从同版本 schema 运行 migration。
4. Expand：添加 nullable column、新表、新索引、新兼容字段。
5. Code：应用代码兼容新旧 schema。
6. Migrate/backfill：分批迁移数据，限速、可重试、可暂停。
7. Verify：行数、约束、采样、关键 query、SLO 信号。
8. Contract：确认旧代码不再使用后，删除旧字段/索引/约束。
9. Release log：记录 migration version、耗时、锁等待、row count、错误和 rollback 状态。

默认不在同一个 release 做 `rename/drop/alter type + 代码切换 + 数据回填 + 删除旧字段`。一人公司宁可多一个小 release，也不要一次大爆破。

## Backfill 与数据修复

Backfill 必须可中断：

- 有明确输入范围、batch size、rate limit、checkpoint。
- 幂等或有去重键，重复执行不会破坏数据。
- 每批记录成功、失败、跳过和最后处理位置。
- 有 dry-run 或 sample mode。
- 有停止条件和失败动作。
- 不默认在高峰期运行。

生产数据修复必须写 `data/fixes/YYYY-MM-DD-<slug>.md`：

```markdown
# Data Fix: <title>

- Date:
- Service:
- Tables:
- User impact:
- Reason:
- SQL/migration:
- Backup:
- Verification:
- Rollback/compensation:
- Owner:
```

任何手工 SQL 都必须先变成文件并 review；紧急事故中可以先止血，但事后必须补文件和 incident/release log。

## 隐私、删除与保留

默认原则：

- 不收集没有明确产品目的的数据。
- 新增个人数据字段时，说明用途、保留期、访问边界和是否进入日志/备份/AI eval。
- 删除用户数据、导出用户数据、匿名化、合并账号、修改权限数据都需要人工 checkpoint。
- 备份包含个人数据时，删除请求需要说明备份保留期和恢复后的再删除流程。
- AI eval fixtures 不使用真实用户隐私样本，除非经过脱敏并记录依据。

## 备份与恢复

一人公司默认：

- 使用托管数据库的自动备份和 snapshot；对高价值数据保留手动 snapshot 或 `pg_dump -Fc`。
- 备份文件和 restore 权限比生产读权限更敏感，必须最小权限和加密。
- 至少为每个生产数据服务写 `data/restore/<service>.md`。
- 有付费用户或关键数据后，每月或每季度做一次 restore drill。
- 备份没有恢复演练不算真正可用。

`data/restore/<service>.md` 最少写：

```markdown
# <service> Restore Drill

## Backup Sources

## Restore Steps

## Validation

## RPO / RTO

## Last Drill
```

## 只问人的关键判断

默认不问：migration 文件编号、query 文件拆分、字段命名小调整、backfill 文档小节顺序、是否用 `migrations/` 还是既有目录。

必须问：

- 是否允许生产数据删除、TRUNCATE、DROP、不可逆 migration。
- 是否允许 CI 自动执行 production migration。
- 是否接受停机窗口或锁表风险。
- 是否新增、导出、删除或改变个人/敏感数据用途。
- 是否用更高成本换 PITR、跨区备份、加密密钥管理或更短 RPO/RTO。
- 是否让 AI 训练/eval 使用真实用户数据。

当前建议默认接受：生产数据变更必须有 `data/changes/<change-id>.json`；包含 DROP/TRUNCATE/批量 DELETE/不可逆 migration/个人数据导出时，默认需要人工 checkpoint。

## 本阶段 Review A：一人公司可落地性

结论：可落地，关键是把数据风险压成一个 JSON 和少量 SQL/Markdown 文件。

- `data/changes/*.json` 让一个人能快速恢复“这次数据变更为什么安全”。
- 继续复用 sqlc、release pipeline、SRE-lite，不额外引入数据治理平台。
- expand / migrate / contract 比一次大迁移多一点步骤，但更适合单人产品的可恢复性。
- 最大摩擦是写 backup/rollback/verification；脚本会强制生产变更补齐这些字段。
- 下一步应在第一个真实 schema change 上用 `data-migration-guard` 生成 artifacts。

## 本阶段 Review B：产品/工程/运维风险

结论：阶段 7 主要保护“最难恢复”的生产数据。

- 已把 destructive SQL、不可逆 migration、隐私数据、生产数据修复列为人工 checkpoint。
- 已要求 dry-run、备份、restore 文档和 post-check，降低迁移事故风险。
- 已把 sqlc generate/vet 放入默认顺序，降低 schema/query/code 不一致。
- 已要求 backfill 幂等、限速、可暂停，避免后台修复压垮生产。
- 仍不锁定具体 migration 工具；真实项目可沿用既有工具，新 Go 服务默认使用 golang-migrate 风格。
