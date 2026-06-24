# backup-recovery-continuity-standard 规格

## ADDED Requirements

### Requirement: 生产 target 必须定义连续性工件

生产服务、前端应用、数据服务或用户可见 AI workflow MUST 在发布前具备 backup recovery continuity artifacts。

#### Scenario: 新生产 target 进入发布准备

- GIVEN 一个 target 存在生产用户路径、不可重建数据、外部供应商依赖或生产运维责任
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `continuity/asset-inventory/<target>.json`
- AND 创建 `continuity/backup-policy/<target>.md`
- AND 创建 `continuity/restore-runbook/<target>.md`
- AND 创建 `continuity/recovery-drill/<target>.json`
- AND 创建 `continuity/continuity-plan/<target>.md`

### Requirement: Asset inventory 必须列出关键资产、依赖和恢复目标

Asset inventory MUST 记录 target、owner、criticality、user journeys、data assets、dependencies、backup sources、restore targets、recovery order、RPO、RTO、人审点和复审节奏。

#### Scenario: 创建资产与依赖清单

- GIVEN 一个 target 有生产资产或外部依赖
- WHEN 创建 `continuity/asset-inventory/<target>.json`
- THEN 文件包含 `target`、`owner`、`criticality`、`user_journeys`、`data_assets`、`dependencies`、`backup_sources`、`restore_targets`、`recovery_order`、`rpo`、`rto`、`human_checkpoint`、`review_cadence`
- AND 每个 data asset 记录 name、type、recoverability、privacy_class、backup_source、restore_validation

### Requirement: Backup policy 必须定义备份来源、频率、保留、权限和恢复测试

Backup policy MUST 记录 scope、business impact、RPO/RTO、backup sources、frequency and retention、encryption and access、offsite/vendor independence、monitoring、restore test、cost boundary 和 human checkpoints。

#### Scenario: 创建备份策略

- GIVEN 一个 target 有 backup_required 或 vendor_managed 数据资产
- WHEN 创建 `continuity/backup-policy/<target>.md`
- THEN 文档包含 Scope、Business Impact、RPO / RTO、Backup Sources、Frequency And Retention、Encryption And Access、Offsite / Vendor Independence、Monitoring、Restore Test、Cost Boundary、Human Checkpoints
- AND 说明备份是否能满足 RPO/RTO

### Requirement: Restore runbook 必须能指导隔离恢复和验证

Restore runbook MUST 记录 scope、prerequisites、access recovery、restore steps、validation、RPO/RTO check、failback、communication 和 abort/escalation。

#### Scenario: 执行恢复演练或事故恢复

- GIVEN 需要从备份、snapshot、PITR、vendor export 或手工重建恢复 target
- WHEN 使用 `continuity/restore-runbook/<target>.md`
- THEN runbook 包含 Scope、Prerequisites、Access Recovery、Restore Steps、Validation、RPO / RTO Check、Failback、Communication、Abort / Escalation
- AND 恢复后验证关键用户路径、数据完整性、权限、服务健康和外部副作用

### Requirement: Recovery drill 必须记录目标、实际结果、缺口和行动项

Recovery drill artifact MUST 记录 target、owner、scenario、drill type、date、RPO/RTO target、RPO/RTO actual、data sources、commands or steps、validation、gaps、actions、status 和 next drill。

#### Scenario: 完成一次恢复演练

- GIVEN target 完成 tabletop、restore test、provider outage simulation、access recovery test 或 live drill
- WHEN 创建 `continuity/recovery-drill/<target>.json`
- THEN 文件包含 `target`、`owner`、`scenario`、`drill_type`、`date`、`rpo_target`、`rto_target`、`rpo_actual`、`rto_actual`、`data_sources`、`commands_or_steps`、`validation`、`gaps`、`actions`、`status`、`next_drill`
- AND status 为 `passed`、`passed_with_gaps`、`failed` 或 `not_run`

### Requirement: Continuity plan 必须定义降级模式、替代操作和沟通路径

Continuity plan MUST 记录 essential user journeys、degraded mode、manual operations、dependency failure、out-of-band communication、access recovery、customer communication、decision log 和 review cadence。

#### Scenario: 关键依赖不可用

- GIVEN 数据库、AI provider、支付、邮件、DNS、云账号、CI/CD 或对象存储出现故障
- WHEN 使用 `continuity/continuity-plan/<target>.md`
- THEN 文档包含 Essential User Journeys、Degraded Mode、Manual Operations、Dependency Failure、Out-Of-Band Communication、Access Recovery、Customer Communication、Decision Log、Review Cadence
- AND 说明在完全恢复前如何降级服务或向用户沟通

### Requirement: 高风险恢复决策必须人工 checkpoint

SLA/24x7 commitment、shorter RPO/RTO、higher DR cost、production overwrite、PITR/data discard、automatic failover、sensitive data restore 或 public customer communication MUST 有人工 checkpoint。

#### Scenario: 恢复动作触发高风险条件

- GIVEN 恢复或连续性策略触发高风险条件
- WHEN 准备执行、合并或发布
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND backup policy、restore runbook 或 continuity plan 记录需要人的判断

### Requirement: Continuity artifacts 不得保存敏感内容

Continuity artifacts MUST NOT 保存真实 secret、生产 DSN、供应商凭据、私钥、真实用户数据、raw prompt、raw response 或可识别个人联系方式。

#### Scenario: 记录备份和恢复证据

- GIVEN 需要记录恢复步骤、数据源、命令或供应商路径
- WHEN 写入 `continuity/` artifacts
- THEN 使用占位符、路径、角色名和 runbook 链接
- AND 不保存真实 secret、生产 DSN、供应商凭据、私钥、真实用户数据、raw prompt 或 raw response
