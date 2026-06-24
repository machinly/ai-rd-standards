# 提案：定义数据与数据库迁移规范

## 意图

为一人公司建立可检查的数据变更流程，让 schema、query、migration、backfill、生产数据修复、备份恢复和隐私数据处理进入版本控制，并与 Go/sqlc、release pipeline、SRE-lite 门禁衔接。

## 范围

- 定义数据变更最小仓库 artifacts。
- 定义 sqlc schema/query/migration 同步流程。
- 定义 production migration 的备份、dry-run、验证、回滚要求。
- 定义 expand / migrate / contract 和 backfill 默认规则。
- 定义隐私数据、删除、导出、保留期和 restore drill 的人工 checkpoint。
- 创建数据迁移落地 skill 和检查脚本。

## 不做

- 不实现真实数据库迁移。
- 不锁定云厂商数据库或 migration 工具。
- 不建立完整数据治理平台、数据仓库或 CDC 架构。
- 不定义法律合规结论；只建立工程层的隐私/安全 checkpoint。

## 依据

- 《人月神话》：数据工具不是银弹，必须显性化不可逆决策。
- 小型项目管理：只保留能避免数据丢失和恢复上下文的最小工件。
- Designing Data-Intensive Applications / Database Reliability Engineering：数据系统应可靠、可维护、可恢复，数据库不应成为特殊雪花。
- Evolutionary Database Design：数据库 artifacts 版本化，所有数据库变化都用 migrations，变更越小越容易验证。
- PostgreSQL backup/restore、DDL、PITR 官方文档。
- sqlc schema/query/generate/vet 官方文档。
- golang-migrate migration 文件约定。
- OWASP Database Security、NIST Privacy Framework / GDPR 数据最小化原则。

## 需要人的判断

建议默认：生产数据变更必须有 `data/changes/<change-id>.json`；DROP、TRUNCATE、批量 DELETE、不可逆 migration、个人数据导出或删除都需要人工 checkpoint。
