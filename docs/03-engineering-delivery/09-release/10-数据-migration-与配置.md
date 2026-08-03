# 发布：数据 migration 与配置

## 执行细则

<!-- rule-id: RELEASE-MIGRATION-001 -->
### 完成 production migration preflight

生产 migration 由唯一 release pipeline 执行或记录，不从开发机直连生产。应用 release contract 声明 migration 路径、顺序、校验和规则、schema 边界与破坏性属性；artifact manifest 只列出本次实际包含的 migration，release plan 只允许执行 manifest 中明确列出的变化。preflight 确认适用的 OpenSpec、data change 记录、release pipeline 与 SRE-lite release checklist；随后在临时库或 staging 上以同版本 schema dry-run。进入真实迁移前还要具备备份或恢复路径，并给出 dry-run 或可恢复说明。

<!-- rule-id: RELEASE-MIGRATION-002 -->
### 拆开破坏性 schema 与 backfill

普通发布以保留数据为默认值，不得根据“空环境”“没有用户”或其他运行时猜测自动选择首次初始化、环境重建、reset、fresh init、`DROP`、`TRUNCATE`、清表或 down migration。首次初始化、环境重建和任何数据清除必须使用与普通 deploy 分离的高风险运维入口，并在真实动作前取得明确人工批准。不可逆 migration 以及 `DROP`/`TRUNCATE` 必须人工 checkpoint；production backfill 分批执行；不得默认在一个 release 中同时完成 rename/drop/alter type、代码切换、数据回填和旧字段删除。需要这些动作时拆成可观察、可停止的多个 release。

<!-- rule-id: RELEASE-MIGRATION-003 -->
### 记录 migration 运行事实

migration release log 必须记录 manifest 中的 migration identity/摘要、from/to schema、实际执行顺序、耗时、锁等待、row count、错误与 rollback/forward-recovery 状态。执行器发现未列入已批准 release plan 的 migration 或 schema 变化时立即停止。字段没有实际测量值时明确标记未知或未发生，不能用空值冒充成功。

<!-- rule-id: RELEASE-CONFIG-001 -->
### 为配置与 flag 建立 rollout 控制

应用 release contract 只记录配置 schema、schema version 和所需 secret key 名称；artifact manifest 记录本次配置 schema 与非敏感 key 的变化；环境 Application 记录非敏感配置和 secret reference，任何一层都不得保存真实 secret 值。每个 config item 记录 `rollout`，每个 feature flag 记录 `rollout_plan`。发布计划必须列出相对当前 release set 的配置 key/schema 变化，实际变化超出计划时停止。production 中是否触发 kill switch、进入降级、执行回滚或继续扩大范围，必须由人结合当前信号判断并留下决定。
