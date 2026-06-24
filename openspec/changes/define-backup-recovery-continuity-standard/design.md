# Design

## 工件形态

每个生产 target 使用轻量 continuity 工件：

- `continuity/asset-inventory/<target>.json`
- `continuity/backup-policy/<target>.md`
- `continuity/restore-runbook/<target>.md`
- `continuity/recovery-drill/<target>.json`
- `continuity/continuity-plan/<target>.md`

JSON 用于机器检查和演练事实，Markdown 用于人审恢复步骤和沟通策略。工件记录恢复能力，不保存 secret、真实用户数据、生产 DSN、raw prompt 或 raw response。

## 验证策略

`backup-recovery-continuity-guard` 提供 `verify_continuity.py`：

- 检查 asset inventory 必填字段、data asset 类型、recoverability、RPO/RTO、人审点。
- 检查 backup policy、restore runbook、continuity plan 必要章节。
- 检查 recovery drill JSON 的 scenario、drill type、RPO/RTO 目标与实际值、验证、缺口、行动项和下一次演练。
- 对 PostgreSQL asset 要求备份策略或 runbook 提及 pg_dump、snapshot、WAL、PITR 或 managed backup。
- 对 AI/provider 依赖要求 continuity plan 提及 fallback、disable、queue 或 manual operation。
- 检查 secret、PII、raw prompt/response 不进入 continuity 工件。

## 裁剪原则

- pre-revenue 可以从 tabletop 和托管自动备份开始。
- 有付费用户、不可重建用户数据或合同义务时，必须做 restore test。
- verifier 不判断云架构是否真的满足 RPO/RTO，只检查是否有证据、演练和人审边界。
- 跨区域、多供应商和自动 failover 只有在业务影响证明后才升级。
