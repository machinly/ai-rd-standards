## ADDED Requirements

### Requirement: 已退役执行资产必须退出当前执行面

正式替换完成后，仓库 MUST 把被替换的 active change 归档，并移除没有当前消费者的一次性执行工具、重复计划和已退役 live 文档；仓库 MUST 保留正式规则追溯、人工批准、来源基线和历史审查证据。未完成任务被后续事实覆盖时 MUST 记录 `superseded` 或 `terminated` 结论，不得伪造为完成。

#### Scenario: 正式替换完成后的清理

- **WHEN** 当前状态已经声明正式替换完成，且旧执行资产没有当前入口或消费者
- **THEN** 旧 change 从 active 区归档
- **AND** 一次性工具与重复 live 文档从当前工作树移除
- **AND** 历史治理和规则追溯证据继续可读

#### Scenario: 清理不得扩大范围

- **WHEN** 仓库同时存在其他 active change、试点或用户未提交工作
- **THEN** 清理只作用于明确 allowlist
- **AND** 当前 change、试点和本地受保护运行态内容保持不变

### Requirement: 本地运行态资产不得进入版本控制

仓库 MUST 忽略可重建的 Agent/预览服务运行态目录和语言缓存；清理已有运行态内容前 MUST 确认相关进程与保留决定，且不得读取或输出 token、secret 或其他敏感值。

#### Scenario: 本地运行态目录存在

- **WHEN** `.agents/`、`.superpowers/` 或 Python cache 出现在工作区
- **THEN** Git 不把这些目录作为待提交正式资产
- **AND** 可重建 cache 可以安全删除
- **AND** 受保护或可能含敏感内容的目录只在明确授权后处置
