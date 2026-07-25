# rd-standards-navigation Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义最小默认入口和按需 playbook 导航，使人和 Codex 不需要先加载 W0-W9、角色、OpenSpec 或多 Agent 材料。
## Requirements
### Requirement: 根入口必须指向最小三档路径

README MUST 指向 Quick、Standard、High-risk 快速分流和最小研发内核，说明 Standard/High-risk 实现性变更默认使用 OpenSpec，并明确当前没有无人值守公司 runtime。

#### Scenario: 打开仓库

- GIVEN 用户或 Codex 打开 README
- WHEN 决定先读什么
- THEN README 指向 docs/00-start-here.md
- AND README 指向 docs/01-minimal-rd-kernel.md
- AND 不要求先定位 W0-W9
- AND Quick 不创建 OpenSpec，Standard/High-risk 实现性变更创建或继续 active change

### Requirement: 默认读取集合必须保持小

README、快速分流和最小内核 MUST 合计不超过 350 行，每个文件 MUST 能独立说明自己的用途。

#### Scenario: 新任务冷启动

- GIVEN 一个普通研发请求
- WHEN 读取默认入口
- THEN 不需要读取完整 playbook index、角色文档或来源目录
- AND 只有出现具体缺口时才加载一个 playbook

### Requirement: W0-W9 和角色文档必须是可选 playbook

所有 docs/W* 文档 MUST 在顶部标明可选状态。角色文档 MUST 被描述为专业视角，而不是必设岗位或默认 Agent。

#### Scenario: 选择专项资料

- GIVEN Standard 或 High-risk 工作出现具体专业问题
- WHEN 查看 docs/02-standard-index.md
- THEN 可以选择一个相关 playbook
- AND playbook 与最小内核冲突时以最小内核为准

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

### Requirement: 验证结果必须区分格式、治理和试验

仓库 verifier MUST 分别输出 format_valid、governance_complete 和 pilot_verified，不得用格式 PASS 代表真实任务效果。

#### Scenario: 试验尚未完成

- GIVEN 文件和治理检查通过
- AND 对照任务少于 10 个
- WHEN 运行 python tools/verify_rd_standards.py .
- THEN format_valid 可以 PASS
- AND governance_complete 可以 PASS
- AND pilot_verified 显示 PENDING
