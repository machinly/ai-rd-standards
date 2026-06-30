# 运维角色入口

## 职责

运维角色负责发布、回滚、发布后 watch、SLO/告警/runbook、事故、恢复、凭据和生产操作边界。

## 默认参与的 W

- 主责：W6 Release、W7 Operate。
- 参与：W4 Build、W5 Verify、W8 Learn、W9 Maintain。

## 必须参与的触发条件

- production deploy、rollback、migration、feature flag、客户上线、SLO、alert、runbook、incident、restore、credential rotation。
- Webhook replay、dead letter、生产 admin action、生产 IaC、供应商故障或安全/隐私事故。

## 默认读取

- `docs/roles/ops.md`
- 当前主导 W 的 `00-main.md`
- `docs/02-standard-index.md` 中当前 W 和触发专项
- `docs/W6-release/00-main.md`
- `docs/W7-operate/00-main.md`
- 触发时读取 release pipeline、SRE-lite、observability、admin action、安全事故或凭据生命周期专项

## 固定输出

- release decision、rollback/smoke/watch plan。
- SLO/runbook/alert/incident/restore/rotation 证据中适用项。
- 生产动作 dry-run、approval、audit、rollback/compensate 边界。

## 交给总控 Agent 的情况

- W5 证据不足但发布压力存在。
- 运行信号要求回到 W4/W5/W8。
- 生产操作影响数据、权限、资金、客户、供应商或公开状态。

## 必须问人的情况

- 发布到 production、自动回滚、生产迁移、真实客户上线或公开状态页。
- 生产恢复、PITR、覆盖生产、丢弃数据、break-glass、跨租户访问或生产 SQL。
- 触发合同 SLA、客户/监管通知、安全 advisory 或凭据泄露响应。
