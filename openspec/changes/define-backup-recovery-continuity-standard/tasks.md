# 任务

## 1. 来源与约束

- [x] 1.1 查证 Google SRE Data Integrity / Disaster Recovery Testing / Emergency Response。
- [x] 1.2 查证 Google Cloud / AWS RPO、RTO、DR planning 和恢复测试。
- [x] 1.3 查证 NIST SP 800-34 contingency planning。
- [x] 1.4 查证 PostgreSQL Backup and Restore、PITR、pg_dump、pg_restore。
- [x] 1.5 补充阶段 21 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 备份恢复连续性规范

- [x] 2.1 编写阶段 21 规范正文。
- [x] 2.2 定义 asset inventory、backup policy、restore runbook、recovery drill、continuity plan artifacts。
- [x] 2.3 定义 Go/Kratos/sqlc/gRPC、Vite、AI workflow 默认恢复规则和人审点。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 21 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `backup-recovery-continuity-guard` skill。
- [x] 4.2 添加 continuity artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 continuity 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实 target 的 `continuity` artifacts，因此不连接真实数据库、云账号、供应商或生产环境。

验证说明：本仓库是研发规范仓库，不包含真实产品 target 的 `continuity` artifacts，也不应在规范阶段连接真实数据库、云账号、备份系统、供应商或生产环境。已通过 `verify_continuity.py` 的临时 `assistant-app` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `continuity/asset-inventory`。
