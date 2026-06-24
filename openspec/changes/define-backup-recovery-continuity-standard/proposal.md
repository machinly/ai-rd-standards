# Proposal: define backup recovery continuity standard

## 意图

建立一人公司备份、恢复、灾难演练与业务连续性规范，覆盖关键资产、RPO/RTO、备份策略、恢复 runbook、恢复演练和降级/沟通计划，避免数据丢失或供应商事故时只能靠记忆处理。

## 范围

- 新增 `backup-recovery-continuity-standard` spec。
- 新增阶段 21 规范文档。
- 创建 `backup-recovery-continuity-guard` skill 和 verifier。
- 补充来源索引与 README。

## 不做什么

- 不替代阶段 5 SRE-lite incident response。
- 不替代阶段 7 数据 migration / restore 文档；本阶段把跨资产连续性补齐。
- 不要求一开始多区域 HA、复杂 DR 平台或 24/7 值班。
- 不连接真实云账号、数据库、备份系统、供应商或生产环境。

## 依据

- 《人月神话》。
- Google SRE Data Integrity、Lessons Learned、Emergency Response、DiRT。
- Google Cloud Disaster Recovery / RTO / RPO。
- AWS Well-Architected Reliability backup recovery testing 和 recovery objectives。
- NIST SP 800-34 contingency planning。
- PostgreSQL Backup and Restore、PITR、pg_dump、pg_restore。

## 需要人的判断

只有这些需要人工 checkpoint：合同 SLA/24x7/更短 RTO/RPO、更高云成本、从备份覆盖生产、PITR 或丢弃数据、自动 failover/供应商切换/自动回滚、包含个人数据/权限/资金/审计/AI trace 的恢复、公开状态页或客户通知。
