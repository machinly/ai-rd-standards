# 发布：数据 migration 与配置

## 执行细则

<!-- rule-id: RELEASE-MIGRATION-001 -->
### 完成 production migration preflight

生产 migration 由 release pipeline 执行或记录，不从开发机直连生产。preflight 确认 OpenSpec、data change JSON、release pipeline 与 SRE-lite release checklist；随后在临时库或 staging 上以同版本 schema dry-run。进入真实迁移前还要具备备份或恢复路径，并给出 dry-run 或可恢复说明。

<!-- rule-id: RELEASE-MIGRATION-002 -->
### 拆开破坏性 schema 与 backfill

不可逆 migration 以及 `DROP`/`TRUNCATE` 必须人工 checkpoint。production backfill 分批执行；不得默认在一个 release 中同时完成 rename/drop/alter type、代码切换、数据回填和旧字段删除。需要这些动作时拆成可观察、可停止的多个 release。

<!-- rule-id: RELEASE-MIGRATION-003 -->
### 记录 migration 运行事实

migration release log 必须记录 migration version、耗时、锁等待、row count、错误与 rollback 状态。字段没有实际测量值时明确标记未知或未发生，不能用空值冒充成功。

<!-- rule-id: RELEASE-CONFIG-001 -->
### 为配置与 flag 建立 rollout 控制

每个 config item 记录 `rollout`，每个 feature flag 记录 `rollout_plan`。production 中是否触发 kill switch、进入降级、执行回滚或继续扩大范围，必须由人结合当前信号判断并留下决定。
