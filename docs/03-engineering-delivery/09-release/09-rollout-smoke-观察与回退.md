# 发布：Rollout、smoke、观察与回退

## 执行细则

<!-- rule-id: RELEASE-ROLLOUT-001 -->
### 按可观测流量选择部署策略

发布默认小批量并保持可回退，高风险变更要进一步拆小。有足够流量时可用 canary 或 progressive rollout，也可按环境能力选择 blue/green 或受控 promote；没有足够流量时，用 staging smoke、production 只读检查与外部 uptime 检查补偿，不能假装执行了 canary。

<!-- rule-id: RELEASE-ROLLOUT-002 -->
### AI runtime 分阶段扩大

AI runtime change 的默认次序是先做 local eval，再进入 shadow 或 small cohort，持续监控后才扩大范围；整个过程必须保留 rollback route。任一阶段缺少证据时停在当前范围，不直接跳到全量。

<!-- rule-id: RELEASE-WATCH-001 -->
### 定义 production smoke 覆盖

smoke 按变更影响覆盖关键用户路径、health、gRPC/HTTP endpoint、前端关键页面和 AI fallback 中的适用项。每项必须有实际结果；只访问首页或只看进程存活，不能代表其他路径通过。

<!-- rule-id: RELEASE-WATCH-002 -->
### 执行发布后 watch

production deploy 后执行 smoke，并连续观察关键 SLI 15–30 分钟；必须覆盖 SLO 四黄金信号。watch plan 在部署前必须链接本次适用的 `stop_conditions`，执行记录按 condition id 保存实际窗口、观测值、触发结果与动作。SLO、dashboard、日志字段和 alert 必须能识别本次 release 的影响，watch 结果进入发布证据。无法形成有效流量时，使用已声明的只读与外部检查，不把“无数据”记成稳定。

<!-- rule-id: RELEASE-WATCH-003 -->
### 用错误预算触发停止动作

`error_budget_policy` 必须预先写明触发后的暂停发布、回滚、人工复核或最高影响问题修复动作。引用错误预算时，`stop_conditions` 必须链接可解析的 policy 工件与具体条目，并能从该条目确定阈值、观察窗口、信号来源和动作；只写“快速消耗”不构成可检查条件。观察期命中预授权的快速消耗条件时先自动停止扩大，并按合同回滚或关闭开关，再排查。是否恢复或继续 rollout、切 fallback、转人工或接受持续的 eval/投诉风险，必须由指定的人依据当前证据决定。

<!-- rule-id: RELEASE-WATCH-004 -->
### 维护可判定的 stop conditions

每个 `stop_conditions[]` 条目至少记录 `id`、`threshold`、`observation_window`、`signal_source`、`action`、`decision_owner` 与 `execution_mode`。`signal_source` 必须能定位 metric/query、dashboard panel、log/eval 查询或外部检查；`execution_mode` 只能为 `automatic` 或 `human`。`automatic` 只执行事先批准且可逆的停止扩大、回滚或 disable 动作，并记录执行结果；扩大范围、恢复发布、接受风险或改变客户/数据边界始终由 `decision_owner` 人工决定。缺少任一判定字段时，条件不得被声称为自动 gate，命中不明信号时先停止扩大并转人工。

<!-- rule-id: RELEASE-ROLLBACK-001 -->
### 让 rollback runbook 可直接执行

rollback runbook 必须写明回到哪个已验证且兼容的 release set，或在单应用场景回到哪个 artifact；同时写明各应用切换顺序、migration 是否可逆、不可逆时的停机/降级/补偿、可用的 feature flag 或 disable switch、回退后的 smoke、谁能执行以及唯一执行入口。数据库默认不隐式执行 down migration；上一代码/配置组合与当前 schema 不兼容时，先停止或降级并进入独立恢复决定，不能把链接切回称为完整回滚。pipeline 的 `rollback` 必须指向该可读文件；runbook 和 smoke 步骤要在发布前写好，而不是故障后临时补写。
