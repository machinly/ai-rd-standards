## ADDED Requirements

### Requirement: Required 可视 UX 必须以浏览器证据核对已批准方案

`visual_ux: required` change MUST 用可重复 Browser E2E 证明关键旅程，并用 desktop screenshot 核对已批准 wireframes；只有布局实质不同时才要求 mobile screenshot。验证 MUST 覆盖适用的 loading、empty、error、success、keyboard-only、visible focus 和 focus order，并记录实质差异及重新 review 证据。Screenshot MUST NOT 替代 Browser E2E。

#### Scenario: 实现与已批准 UX 一致

- **WHEN** 在干净完整本地环境验证 required 可视 UX change
- **THEN** Browser E2E 从页面入口完成真实用户动作并断言最终状态
- **AND** desktop screenshot 可与当前批准 wireframe 核对
- **AND** 布局实质不同时有 mobile screenshot

#### Scenario: 浏览器实现存在实质偏差

- **WHEN** 任务路径、结构、状态、权限含义或高风险确认与批准 UX 不一致
- **THEN** 验证不得把该路径标为 accepted
- **AND** 返回体验设计更新并重新 review
