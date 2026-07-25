# ai-coding-workflow-standard 的变更规格

## MODIFIED Requirements

### Requirement: AI 参与不得自动增加流程工件

AI-assisted work MUST 按影响、可逆性和恢复需要选择路径。AI 参与本身、任务时长或文件数量 MUST NOT 单独触发流程升级；Quick 不创建 OpenSpec，Standard/High-risk 实现性变更则因风险路径默认创建或继续 OpenSpec change。

#### Scenario: 低风险 AI 辅助修改

- GIVEN AI 修改低风险、局部、可逆的代码或文档
- AND 不影响用户、生产、敏感数据、权限或外部承诺
- WHEN 开始实现
- THEN 可以走 Quick
- AND 不创建 OpenSpec
- AND 只需保留 diff、相关验证和剩余风险

## REMOVED Requirements

### Requirement: Standard 工作只维护一份可恢复 brief

**Reason**：Standard/High-risk implementation 现在默认使用 OpenSpec，平行 work brief 会重复维护相同状态。

**Migration**：使用 active change 的 `tasks.md` 保存状态和下一步，并链接外部产品、review 与验证证据。

## ADDED Requirements

### Requirement: Standard 工作只维护一份可恢复状态

需要跨会话恢复、用户可见行为或独立验收的 AI-assisted implementation MUST 在 OpenSpec change 中记录 outcome、non-goals、scope、acceptance、context sources、risks、verification、rollback、decisions needed、status 和 next。同一事实 MUST NOT 再复制到平行 work brief。

#### Scenario: AI 协作跨越一个会话

- GIVEN 工作属于 Standard implementation
- WHEN 建立持久状态
- THEN 创建或继续 OpenSpec change
- AND 使用 `tasks.md` 记录当前状态和下一步
- AND 链接产品输入、测试、review 和设计证据
- AND 不创建内容重复的 work brief
