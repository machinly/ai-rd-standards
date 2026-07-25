# 设计：数据与数据库迁移规范

## 设计决策

### 1. 结构化 data change JSON

迁移 SQL 只能说明“做什么”，不能完整表达备份、回滚、验证、隐私和人工 checkpoint。`data/changes/<change-id>.json` 用于记录这些发布前必须检查的事实。

### 2. 迁移工具不锁定，文件约定可检查

真实项目可能已有 goose、golang-migrate、Atlas 或云厂商工具。规范只要求迁移文件可排序、可追踪、可在 CI/staging 执行。新 Go 服务默认用 golang-migrate 的 up/down SQL 文件，便于简单检查和回滚说明。

### 3. sqlc 是 schema/query/code 的门禁

sqlc 从 schema 和 queries 生成 Go 代码。数据规范必须要求 `sqlc generate` 和 `sqlc vet`，否则 schema 变了但 repository code 未同步会进入生产。

### 4. 生产迁移默认 expand/migrate/contract

rename、drop、type change、set not null 和批量更新可能带来锁、不可逆数据损失或旧代码不兼容。默认拆成 expand、代码兼容、backfill、verify、contract。

### 5. 备份以恢复能力为准

“有备份”不足以证明安全。高价值数据需要 restore 文档和周期性 drill；高风险迁移需要确认最近备份可恢复，或明确接受风险。

### 6. 隐私数据进入人工 checkpoint

一人公司不能用复杂治理系统替代判断。新增、导出、删除、匿名化、AI eval 使用真实用户数据等行为必须显式确认。

## 取舍

- JSON 增加少量书写成本，但换来机器检查。
- 不锁定 migration 工具降低一致性，但避免与真实项目冲突。
- expand/migrate/contract 让某些变更跨多个 release，但降低不可逆风险。
- 不要求第一天 PITR，但要求知道备份/恢复边界。
