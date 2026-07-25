# one-person-rd-governance 的变更规格

## REMOVED Requirements

### Requirement: OpenSpec 必须是可选工具

**Reason**：用户决定将 OpenSpec 设为 Standard/High-risk 实现性变更的默认载体；原规则导致复杂项目可以在早期一次跳过后永久不再评估。

**Migration**：Quick 和非实现性工作继续不默认创建；Standard/High-risk 实现性变更创建或继续 active change，只有用户明确批准并记录理由时才跳过。

## ADDED Requirements

### Requirement: Standard 和 High-risk 实现性变更必须默认使用 OpenSpec

研发流程 MUST 在 Standard 和 High-risk 的代码、配置、schema、API、AI 行为、数据、基础设施或发布设计进入实现前创建或继续一个 OpenSpec change。Quick MUST NOT 被强制创建 OpenSpec。跳过默认规则 MUST 有明确的人类批准、理由、适用范围和恢复方式。

#### Scenario: 开始 Standard 用户可见变更

- GIVEN 工作会改变用户可见行为并需要独立验收
- WHEN 准备进入实现
- THEN 创建或继续一个 OpenSpec change
- AND proposal/specs/design/tasks 只承载本次 change 的增量
- AND `tasks.md` 成为执行状态的权威来源

#### Scenario: 执行 Quick 局部修复

- GIVEN 工作低风险、局部、可逆且不影响用户、生产、敏感数据或权限
- WHEN 开始实现
- THEN 不要求创建 OpenSpec
- AND 交付时提供 diff、相关验证和剩余风险

#### Scenario: 用户批准跳过 OpenSpec

- GIVEN Standard/High-risk 实现性变更有特殊原因不使用 OpenSpec
- WHEN 用户明确批准豁免
- THEN 记录 decision owner、理由、适用范围和恢复方式
- AND 执行者不能仅以“已有文档足够”自行豁免

### Requirement: OpenSpec 不得复制权威输入或替代完成证据

OpenSpec MUST 链接经人确认的产品输入、体验设计、验收映射、review 和验证证据，不得复制为第二权威来源。OpenSpec validation MUST NOT 被解释为产品完成、浏览器 E2E、独立审查或发布批准。

#### Scenario: 新用户能力建立 change

- GIVEN 产品输入和体验设计已经由人确认
- WHEN 编写 OpenSpec proposal 和 delta spec
- THEN change 链接权威输入并只描述本次行为增量
- AND acceptance 映射继续由真实 API、数据、自动化、浏览器或人工证据证明
- AND 不用格式校验替代独立验收

