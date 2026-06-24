# 任务

## 1. 来源与约束

- [x] 1.1 查证 PostgreSQL backup/restore、PITR、DDL 官方文档。
- [x] 1.2 查证 sqlc schema/query/generate/vet 官方文档和 golang-migrate 文件约定。
- [x] 1.3 查证 Evolutionary Database Design、DDIA、Database Reliability Engineering、OWASP/NIST/GDPR 数据安全与隐私依据。
- [x] 1.4 补充阶段 7 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 数据迁移规范

- [x] 2.1 编写阶段 7 规范正文。
- [x] 2.2 定义 `data/changes`、migrations、queries、backfills、restore、fixes artifacts。
- [x] 2.3 定义 sqlc 同步、production migration、backfill、隐私、备份恢复规则。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 7 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `data-migration-guard` skill。
- [x] 4.2 添加 data change artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 data migration 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实数据库迁移，因此不运行真实 migration 或 restore。

验证说明：本仓库是规范仓库，不包含真实数据库 migration，也不应在规范阶段连接生产数据库或执行 restore。已通过 `verify_data_migration.py` 的临时 `billing-api` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `data/changes`。
