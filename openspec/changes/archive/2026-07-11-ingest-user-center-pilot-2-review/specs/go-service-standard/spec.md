# go-service-standard 的变更规格

## ADDED Requirements

### Requirement: 多个 Go 可执行入口必须有命令注册表

存在多个 `cmd/<name>` 的 Go target MUST 在 `governance/architecture/command-registry.json` 登记每个入口的 path、purpose、kind、environment、lifecycle、starter、dependencies、privileges、data_writes、failure_recovery 和 retirement。

#### Scenario: 服务包含 API、worker、管理 CLI 和测试工具

- GIVEN Go target 有两个以上 cmd 入口
- WHEN 进行结构或发布审查
- THEN 每个实际 cmd 路径都在 command registry 中恰好出现一次
- AND 生产、开发和测试入口可区分
- AND 一次性高权限操作记录权限、数据写入和恢复方式

### Requirement: 高风险实现必须保留代码内设计意图

状态转换、权限拒绝、事务/并发、关键 SQL、前端按钮状态、异常恢复和临时限制等非显然高风险逻辑 MUST 在代码附近解释业务/安全意图、失败风险或不变量。注释 MUST NOT 只复述语法，也 MUST NOT 以覆盖率作为完成指标。

#### Scenario: 实现 CAS 状态转换

- GIVEN 代码使用版本或 CAS 防止并发覆盖
- WHEN reviewer 阅读实现
- THEN 代码附近说明保护的不变量和冲突处理原因
- AND reviewer 无需只靠外部治理文档重新推导意图

