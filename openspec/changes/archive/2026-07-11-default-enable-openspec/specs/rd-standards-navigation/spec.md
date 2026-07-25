# rd-standards-navigation 的变更规格

## MODIFIED Requirements

### Requirement: 根入口必须指向最小三档路径

README MUST 指向 Quick、Standard、High-risk 快速分流和最小研发内核，说明 Standard/High-risk 实现性变更默认使用 OpenSpec，并明确当前没有无人值守公司 runtime。

#### Scenario: 打开仓库

- GIVEN 用户或 Codex 打开 README
- WHEN 决定先读什么
- THEN README 指向 docs/00-start-here.md
- AND README 指向 docs/01-minimal-rd-kernel.md
- AND 不要求先定位 W0-W9
- AND Quick 不创建 OpenSpec，Standard/High-risk 实现性变更创建或继续 active change

### Requirement: 核心 skill 必须使用三档风险路由

one-person-openspec-rd skill MUST 先选择 Quick、Standard 或 High-risk，不得默认扫描 W0-W9 或派生多 Agent；选择 Standard/High-risk 实现性变更后 MUST 默认创建或继续 OpenSpec change。

#### Scenario: 使用核心 skill

- GIVEN 用户提出研发任务
- WHEN skill 开始工作
- THEN 按影响、可逆性和问责性分流
- AND Quick 不创建 OpenSpec
- AND Standard/High-risk 实现性变更创建或继续 active change
- AND High-risk 副作用前要求明确人类批准
- AND Standard/High-risk 要求独立最终审查

### Requirement: 知识地图必须反映真实默认入口

docs map 和 context pack MUST 将 README、快速分流、最小内核和 context pack 作为 canonical entrypoints，将 W0-W9 和多 Agent 标为可选，并将 OpenSpec 标为 Standard/High-risk 实现性变更的默认 change 载体。

#### Scenario: 恢复上下文

- GIVEN Codex 读取 knowledge/docs-map/rd-standards.json
- WHEN 查找默认入口
- THEN canonical entrypoints 与最小三档路径一致
- AND 能识别 Quick 的无 OpenSpec 路径和 Standard/High-risk 的 active change
- AND review、decision 和 experiment artifacts 可追溯

