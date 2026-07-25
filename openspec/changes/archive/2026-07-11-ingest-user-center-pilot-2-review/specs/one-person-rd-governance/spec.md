# one-person-rd-governance 的变更规格

## ADDED Requirements

### Requirement: 用户可见工作必须先证明最小产品闭环

用户可见 Standard/High-risk implementation MUST 在扩展大量专项治理工件前定义关键用户旅程，并尽早从完整本地环境证明至少一条真实页面闭环。High-risk 实现前独立审查 MUST 保持不变。

#### Scenario: 新用户能力开始实现

- GIVEN 产品输入和体验设计已经确认
- WHEN 准备实现用户可见能力
- THEN 先定义少量关键用户/管理员旅程
- AND 把旅程映射到真实页面动作、结果和证据层级
- AND 在扩大治理域前跑通至少一条代表性 Browser E2E 或保持状态为 in_progress/changes_requested

### Requirement: 项目必须只有一个权威当前状态

Standard/High-risk 项目 MUST 维护一个绑定目标 revision 和最新独立 review 的权威当前状态。较新的 `changes_requested`、失败关键旅程或失效 manifest MUST 使较早完成摘要失效。

#### Scenario: 最新独立审查要求修改

- GIVEN 早期验证摘要写过 pass 或 complete local integration
- WHEN 最新冻结输入的独立 review 为 changes_requested
- THEN 项目当前状态为 changes_requested
- AND 早期验证只保留为历史运行事实
- AND 不再支持完成或 accepted 声明

### Requirement: 治理工件必须有预算和可观察用途

每个新增治理域 MUST 记录触发原因、权威入口、改变的决策或门禁以及保留策略。实验 MUST 先建立产品输入、最小旅程、完整本地环境和一条浏览器闭环，再按命中风险增加治理工件。

#### Scenario: guard 准备创建新治理域

- GIVEN 某个专项 guard 被触发
- WHEN 准备新增治理文件
- THEN 在 project map 登记 domain、trigger、owner、decision_or_gate 和 retention
- AND 不为 verifier 或目录完整性创建没有决策/验收价值的文件

### Requirement: 试点记录必须显式记录 OpenSpec 使用状态

每条研发规范试点记录 MUST 记录 `openspec.used`、`change_id`、跳过批准和原因。Standard/High-risk 未使用 OpenSpec 时 MUST 有用户事前明确批准的例外依据，否则记录 MUST 视为格式失败且不得计入效果样本。

#### Scenario: High-risk 试点遗漏 OpenSpec

- GIVEN 一项 High-risk 实现没有创建或继续 OpenSpec change
- WHEN 汇总试点记录
- THEN `openspec.used` 为 false
- AND 记录真实遗漏原因，不追溯性伪造 change id
- AND 没有用户批准例外时该记录不计入 eligible 样本
