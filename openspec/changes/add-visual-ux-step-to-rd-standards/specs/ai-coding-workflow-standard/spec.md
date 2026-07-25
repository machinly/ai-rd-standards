## ADDED Requirements

### Requirement: AI 实现必须消费已批准的可视 UX 输入

AI-assisted Standard/High-risk implementation MUST 读取 proposal 的 `visual_ux` 判定。值为 `required` 时，生产性实现前 MUST 链接当前 `flow.md`、关键 wireframes 和人类 `approved` review；AI MUST NOT 用 OpenSpec、文字 brief、一般授权或已生成代码代替该批准。

#### Scenario: Required UX 未批准

- **WHEN** AI 准备开始用户可见生产性实现
- **AND** `visual_ux` 为 `required` 但没有当前人类 `approved`
- **THEN** AI 停止该生产性实现路径
- **AND** 返回体验设计或请求明确决定

#### Scenario: 实现发现已批准方案不成立

- **WHEN** 实现发现任务路径、状态、权限含义或高风险确认需要实质改变
- **THEN** 先更新体验设计并重新取得人类批准
- **AND** 不在代码中静默改变后把 wireframe 标为过期附件
