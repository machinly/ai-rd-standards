# one-person-rd-governance 的变更规格

## ADDED Requirements

### Requirement: 默认工作单元必须是 OpenSpec change

研发流程 MUST 将预计超过 30 分钟的开发工作表示为一个 OpenSpec change，并在实现前完成基本 artifacts。

#### Scenario: 标准功能工作

- GIVEN 一个新的功能、服务、界面、数据、运维或 AI 行为请求
- WHEN 预计工作量超过 30 分钟
- THEN 创建或更新一个 OpenSpec change 目录
- AND 包含 `proposal.md`、`design.md`、`tasks.md` 和至少一个 delta spec

#### Scenario: 低风险小修复

- GIVEN 修复预计 30 分钟以内完成
- AND 回滚、数据、安全和产品风险都很低
- WHEN 直接完成修复
- THEN 在最接近的相关 spec、change 或规范文档中记录变更

### Requirement: 人的注意力必须受预算约束

研发流程 MUST 只把具有明显产品、成本、数据、安全、合规或架构后果的决策交给人判断。

#### Scenario: 低风险局部实现细节

- GIVEN 某个选择很容易回滚
- AND 仓库或规范已经暗示默认值
- WHEN agent 需要选择实现细节
- THEN 使用默认值继续
- AND 只有在影响后续工作时才在总结中说明

#### Scenario: 高影响决策

- GIVEN 某个选择影响产品方向、用户数据、架构锁定、成本、合规或多日工作量
- WHEN agent 无法推断安全默认值
- THEN 用最多三个选项询问人
- AND 标注推荐默认值

### Requirement: 每段内容必须有两轮一人公司 review

每个完成的规范段落 MUST 在进入下一段前包含两轮 review。

#### Scenario: 一人可执行性 review

- GIVEN 一个规范段落已起草
- WHEN 执行 Review A
- THEN 评估一个人是否能执行、是否能中断后恢复、是否有完成条件、是否避免流程负担

#### Scenario: 产品工程运维风险 review

- GIVEN 一个规范段落已起草
- WHEN 执行 Review B
- THEN 评估过早复杂化、测试或 eval、观测、数据安全、回滚和运维影响

### Requirement: AI 行为必须可评估

研发流程 MUST 在改变用户可见 AI prompt、模型、工具 workflow 或自主行为前定义最小 eval。

#### Scenario: 用户可见 AI 行为变更

- GIVEN 一个功能会改变用户或业务流程依赖的 AI 输出
- WHEN 规划变更
- THEN 定义代表性 eval 输入、验收标准和至少一个边界或对抗样例
- AND 将 prompt 或 instruction 源版本化到代码或配置中

