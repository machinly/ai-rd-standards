# Design

## 工件形态

每个生产 target 使用轻量 admin-ops artifacts：

- `admin-ops/action-registry/<target>.json`
- `admin-ops/operator-playbook/<target>.md`
- `admin-ops/audit-log-schema/<target>.json`
- `admin-ops/break-glass/<target>.md`
- `admin-ops/ops-review/<target>.md`

JSON 记录机器可检查的动作、权限、审批、dry-run、回滚、AI 自治级别和审计字段。Markdown 记录人执行时需要的操作步骤、紧急访问和定期复盘。工件不得保存真实 secret、生产 DSN、完整 raw prompt、完整 raw response、真实用户数据或不必要个人信息。

## 验证策略

`admin-ops-action-guard` 提供 `verify_admin_ops.py`：

- 检查 action registry 必填字段、动作清单、风险级别、权限、dry-run、rollback、audit event 和 human checkpoints。
- 检查 operator playbook 必要章节和执行顺序。
- 检查 audit log schema 必填字段、append-only/integrity、retention、alerts 和敏感字段策略。
- 检查 break-glass 必要章节、限时访问、撤销、记录和 review。
- 检查 ops review 的高风险动作、失败/中止、审计缺口、权限漂移、toil 和 next one change。
- 检查 AI autonomy 不能把 R2/R3/R4 写操作默认交给 AI 自动执行。

## 裁剪原则

- pre-revenue 可以先登记最常用的少数 admin actions，不做复杂后台平台。
- 有付费用户、生产数据、跨租户、退款/credit、权限、删除或外部通知时，必须补齐审计、dry-run 和 rollback/compensate。
- verifier 不判断业务动作是否正确，只检查是否有边界、证据、回滚路径和人审点。
- 允许脚本和 one-off processes，但必须随 release/code/config 管理，而不是散落在个人机器。
