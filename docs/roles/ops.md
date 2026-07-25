# 运维视角

> 状态：可选角色视角，不是必设岗位或默认 Agent。仅在任务涉及发布、运行或恢复时读取。

## 关注问题

- 用户影响如何观察？
- 发布、配置和迁移是否可回滚？
- 告警是否指向可执行动作？
- 外部依赖失败时如何降级？
- 恢复、备份和凭据路径是否实际可用？

## 最小输出

- deploy and rollback plan；
- health signals；
- smoke/post-action watch；
- runbook or recovery gap；
- incident trigger。

## 必须交给人

- 生产发布和恢复；
- 数据丢失风险；
- break-glass；
- 客户/监管通知；
- 凭据操作。
