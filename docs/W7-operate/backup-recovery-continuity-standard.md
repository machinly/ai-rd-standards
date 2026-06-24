# W7 Operate 触发专项：备份、恢复、灾难演练与业务连续性规范

## W7 触发定位

本文件是 W7 Operate 的触发型专项，不是 W7 主入口。只有当当前工作涉及备份、恢复、RPO/RTO、restore drill、业务连续性、供应商故障、访问恢复或灾难演练时，才需要读取本文件。

普通 W7 运行入口应先回到 `docs/W7-operate/main.md`，由主入口判断是否触发本专项。

## 目标

一人公司最怕的不是服务短暂不可用，而是数据丢了、凭据进不去、供应商挂了、恢复步骤没人记得、用户不知道发生了什么。本专项定义备份、恢复、灾难演练与业务连续性规范，让每个生产 target 都能回答：什么最重要，最多能丢多少数据，多久要恢复，靠什么恢复，演练是否真的通过。

默认原则：备份不是目标，恢复才是目标。没有演练过的备份只能算希望；没有 RPO/RTO 的恢复计划只是愿望清单。

## 核心依据

- 《人月神话》：工具不是银弹；真正困难来自隐藏依赖、概念不一致和事故时无法协调的复杂性。
- 小型项目管理：一人公司的连续性计划必须短、可执行、可演练，不能依赖厚重组织流程。
- Google SRE, Data Integrity：备份和归档不是一回事；真正有价值的是能在服务可用性需求内恢复的数据。
- Google SRE, Lessons Learned / DiRT：灾难恢复能力需要模拟和演练；只读文档无法形成事故时的记忆。
- Google SRE, Emergency Response：事故中需要 out-of-band communication、替代访问方式、rollback 能力和历史记录。
- Google Cloud Disaster Recovery / RTO / RPO：RTO 表示最大可接受中断时间，RPO 表示最大可接受数据恢复点年龄；DR 设计要由业务影响驱动。
- AWS Well-Architected Reliability：每个 workload 应定义 RTO/RPO，并通过周期性恢复测试验证备份完整性和恢复流程。
- NIST SP 800-34：contingency planning 要围绕业务影响、恢复优先级、恢复策略、测试和维护形成计划。
- PostgreSQL Backup and Restore：PostgreSQL 有 SQL dump、文件系统备份、连续归档/PITR 三类方式；每种都有边界和假设。
- PostgreSQL `pg_dump` / `pg_restore`：`pg_dump` 可做一致导出，但通常不是生产数据库常规备份的唯一选择；`pg_restore` 能从 archive 重建数据库，也有安全注意事项。

## 范围

适用对象：

- PostgreSQL、对象存储、文件、向量库、队列、缓存中可重建与不可重建数据。
- Go/Kratos/gRPC 服务、Vite 前端、AI workflow、prompt/eval artifacts、配置、feature flag、secret、CI/CD、DNS、域名、支付、邮件、模型供应商。
- 源代码、OpenSpec、docs、skills、部署配置和运维 runbook。
- 生产事故、供应商故障、误删数据、配置错误、账号锁定、凭据泄漏、区域故障、AI provider outage。

不适用对象：

- 完全可重建且无用户影响的本地缓存。
- 不进入生产、不保存用户数据、不依赖外部服务的实验。
- 已由W7 SRE-lite 事故响应 或W4 数据迁移专项 覆盖的单次发布/迁移动作；本专项关注跨事故的恢复能力。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
continuity/
  asset-inventory/<target>.json
  backup-policy/<target>.md
  restore-runbook/<target>.md
  recovery-drill/<target>.json
  continuity-plan/<target>.md
```

### `continuity/asset-inventory/<target>.json`

资产与依赖清单必须包含：

- `target`
- `owner`
- `criticality`
- `user_journeys`
- `data_assets`
- `dependencies`
- `backup_sources`
- `restore_targets`
- `recovery_order`
- `rpo`
- `rto`
- `human_checkpoint`
- `review_cadence`

`data_assets` 每条至少包含：

- `name`
- `type`：`postgres`、`object_storage`、`vector_store`、`queue`、`cache`、`repo`、`secret`、`config`、`ai_artifact`、`third_party`
- `recoverability`：`rebuildable`、`backup_required`、`manual_export`、`vendor_managed`
- `privacy_class`
- `backup_source`
- `restore_validation`

默认：任何 `backup_required` 或含个人/付费/业务关键数据的 asset 都必须有 backup policy、restore runbook 和 recovery drill。

### `continuity/backup-policy/<target>.md`

备份策略必须包含：

- `Scope`
- `Business Impact`
- `RPO / RTO`
- `Backup Sources`
- `Frequency And Retention`
- `Encryption And Access`
- `Offsite / Vendor Independence`
- `Monitoring`
- `Restore Test`
- `Cost Boundary`
- `Human Checkpoints`

默认策略：

- 早期产品默认先使用托管数据库自动备份和 snapshot。
- 有付费用户、不可重建用户数据、关键交易或合同义务时，必须确认 PITR、跨区域、离线导出或更短 RPO/RTO 是否值得成本。
- 备份访问权限高于普通读权限，必须最小权限、加密、审计。
- 源代码、OpenSpec、迁移、runbook、skills、配置模板和 CI 定义也属于恢复资产。

### `continuity/restore-runbook/<target>.md`

恢复 runbook 必须包含：

- `Scope`
- `Prerequisites`
- `Access Recovery`
- `Restore Steps`
- `Validation`
- `RPO / RTO Check`
- `Failback`
- `Communication`
- `Abort / Escalation`

默认恢复顺序：

1. 确认事故类型：数据损坏、误删、供应商故障、区域故障、账号锁定、凭据泄漏、代码/配置事故。
2. 冻结进一步破坏：关闭写入、关闭 feature flag、禁用 AI side effect、撤销凭据或暂停发布。
3. 选择恢复点：按 RPO、数据完整性和用户影响选择 snapshot、PITR、dump、导出或手工重建。
4. 在隔离环境恢复：验证数据、权限、schema、应用启动、关键用户路径。
5. 切流或替换生产：记录风险、回滚点和用户沟通。
6. 验证并复盘：记录实际 RPO/RTO、缺口和行动项。

### `continuity/recovery-drill/<target>.json`

恢复演练记录必须包含：

- `target`
- `owner`
- `scenario`
- `drill_type`
- `date`
- `rpo_target`
- `rto_target`
- `rpo_actual`
- `rto_actual`
- `data_sources`
- `commands_or_steps`
- `validation`
- `gaps`
- `actions`
- `status`
- `next_drill`

`drill_type` 允许：

- `tabletop`
- `restore_test`
- `provider_outage_simulation`
- `access_recovery_test`
- `live_drill`

默认频率：

- pre-revenue：至少每季度 tabletop，关键数据每半年 restore test。
- 有付费用户：每季度 restore test 或 provider outage simulation。
- 有合同 SLA/合规义务：按合同、RPO/RTO 和数据风险单独定义，不默认一人承诺 24/7。

### `continuity/continuity-plan/<target>.md`

业务连续计划必须包含：

- `Essential User Journeys`
- `Degraded Mode`
- `Manual Operations`
- `Dependency Failure`
- `Out-Of-Band Communication`
- `Access Recovery`
- `Customer Communication`
- `Decision Log`
- `Review Cadence`

默认：

- 为每个关键用户路径定义“完全恢复前还能怎么服务用户”。
- AI provider 故障必须有 fallback、disable switch、排队、降级文案或人工处理策略。
- 支付、邮件、DNS、域名、OAuth、云账号、OpenAI/API provider 都要记录替代访问或供应商支持路径。
- 客户沟通模板只写事实、影响、缓解、下一次更新时间；不承诺未经验证的恢复时间。

## Go / Kratos / sqlc / gRPC 默认规则

- 数据恢复后必须运行 schema/version 检查、sqlc query smoke、关键 gRPC health/read/write smoke。
- 备份或恢复脚本不得硬编码生产 DSN、token、私钥或个人数据。
- 对高风险恢复动作提供 dry-run 或隔离环境验证命令。
- gRPC 服务应有只读健康检查和关键业务 smoke，用于恢复后验证。
- 恢复后必须检查 idempotency、队列重复消费、定时任务重放和外部副作用。

## Vite 前端默认规则

- 前端静态资源通常可重建，但构建配置、环境变量模板、域名/DNS/CDN 配置属于连续性资产。
- continuity plan 必须记录前端降级模式：只读页、维护页、状态页链接、功能关闭文案。
- 恢复后至少运行 build、preview smoke 或关键路径 Playwright smoke。

## AI workflow 默认规则

- prompt、eval fixtures、tool schemas、model routing、safety policy、cost limit 和 fallback 配置属于恢复资产。
- AI provider outage 默认先降级或排队，不让 agent 自动切到未验证模型处理高风险任务。
- eval 数据和 trace 不保存真实用户 raw prompt/raw response；恢复和导出时遵守隐私边界。
- 恢复后必须运行最小 eval 或 dry-run，确认 schema parse、tool permission、fallback 和 cost guard 仍有效。

## 需要人判断的关键点

只把这些判断交给人：

- 是否承诺合同 SLA、24/7 响应、更短 RTO/RPO 或跨区域容灾。
- 是否接受更高云成本换更短恢复时间或更少数据丢失。
- 是否从备份覆盖生产、执行 PITR、丢弃部分数据或通知用户数据可能丢失。
- 是否启用自动 failover、自动关闭功能、自动切供应商或自动回滚。
- 是否恢复包含个人数据、权限、资金、审计日志、AI eval/trace 的数据集。
- 是否公开状态页、客户通知或事后说明。

其他资产字段、章节完整性、演练记录、路径链接、验证命令、敏感内容检查由 Codex 和 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“什么重要、怎么备份、怎么恢复、是否演练、怎么连续服务”。
- 保留：人只判断 RPO/RTO 成本、覆盖生产、用户通知、自动 failover 和敏感数据恢复。
- 调整：不要求一开始多区域 HA；先从托管备份、restore runbook、季度演练开始。
- 调整：演练允许 tabletop 起步，但有付费关键数据后必须做真实 restore test。
- 风险：恢复计划容易写完就忘。缓解：`recovery-drill.json` 强制记录下次演练和行动项。

结论：可落地。一个人可以用半天补齐第一个 target 的连续性工件，再用每季度一次低风险演练把“希望能恢复”变成“知道怎么恢复”。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：关键用户路径和降级模式让恢复期间仍能解释用户影响。
- 工程角度：PostgreSQL、sqlc、gRPC、Vite、AI workflow 都有恢复后验证路径。
- 运维角度：RPO/RTO、恢复顺序、out-of-band communication 和演练记录降低事故时的慌乱。
- 安全隐私角度：备份权限、加密、个人数据、AI traces、凭据恢复都进入人审边界。
- 成本角度：不默认昂贵跨区容灾；只有付费、合同或数据价值证明后才升级策略。

结论：可落地。本专项把 W7 SRE、W4 数据恢复、W2 安全和 W4 本地可复现连接成真正能执行的业务连续性能力。
