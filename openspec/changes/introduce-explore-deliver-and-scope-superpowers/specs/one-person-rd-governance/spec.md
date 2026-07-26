## ADDED Requirements

### Requirement: 研发规范必须先判定适用性

任务 MUST 在读取研发正文、选择研发路径或创建研发工件前判断主要结果是否改变、验证、发布、运行、恢复或处置产品/工程系统，是否直接决定其产品、体验、技术或验收边界，或研究是否直接支持一个已识别产品/工程决定。不符合这些条件的工作 MUST 使用任务自身流程并退出研发规范。

#### Scenario: 摘要非技术材料

- **GIVEN** 用户要求摘要一份不直接支持已识别产品或工程决定的非技术材料
- **WHEN** 开始选择工作流程
- **THEN** 将任务判定为 Non-R&D
- **AND** 不读取研发正文，不创建 OpenSpec 或研发状态工件
- **AND** 不因会话开始而调用 one-person router 或 Superpowers

#### Scenario: 生成营销插图

- **GIVEN** 用户要求生成不改变产品界面或工程系统的营销插图
- **WHEN** 开始选择工作流程
- **THEN** 使用图像任务自身流程
- **AND** 不套用研发规范

#### Scenario: 通用行业研究

- **GIVEN** 研究没有直接支持一个已识别的产品或工程决定
- **WHEN** 判断是否进入研发调研
- **THEN** 将它保留为通用研究
- **AND** 不创建研发治理工件

### Requirement: 研发工作必须区分 Explore 与 Deliver

通过适用性门的研发工作 MUST 先选择 Explore 或 Deliver。关键未知仍主导且目标是用可证伪证据学习时 MUST 选择 Explore，并按最高优先级问题标记 Product Discovery、UX Prototype 或 Technical Spike；行为已经足够明确且目标是稳定交付时 MUST 选择 Deliver。Quick、Standard 和 High-risk MUST 只作为 Deliver 子路由。

#### Scenario: 判断用户问题是否值得建设

- **GIVEN** 已识别一个用户问题但价值或真实性仍是关键未知
- **WHEN** 选择工作模式
- **THEN** 选择 Explore / Product Discovery
- **AND** 不先选择 Quick、Standard 或 High-risk

#### Scenario: 本地合成 auth spike

- **GIVEN** gateway、OIDC 或 service identity 的学习任务只使用本地合成可重建数据和测试凭据
- **AND** 不接触生产、真实客户、真实凭据或外部系统
- **WHEN** 选择工作模式
- **THEN** 选择 Explore / Technical Spike
- **AND** 不因 auth 领域词自动升级为 High-risk

#### Scenario: 已明确行为进入交付

- **GIVEN** 目标行为、边界和验收已经足够明确
- **WHEN** 准备稳定实现
- **THEN** 选择 Deliver
- **AND** 再按影响、可逆性和问责性选择 Quick、Standard 或 High-risk

### Requirement: 轻量 Explore 必须保持在可恢复 sandbox

轻量 Explore MUST 限于本地或隔离 sandbox、合成且可 reset 或 reseed 的数据、无生产或真实客户数据、无真实凭据或未批准外部系统、无付款、外部通信、公开承诺或不可逆操作，并且 MUST NOT 声明稳定 API、production migration、release candidate 或 production-ready。任何边界被突破时 MUST 停止轻量豁免并重新路由。

#### Scenario: Explore 接触真实客户数据

- **GIVEN** 一个轻量 Explore 准备接入真实客户数据
- **WHEN** sandbox boundary 将被突破
- **THEN** 停止轻量 Explore
- **AND** 重新判断 Deliver/High-risk 或其他适用控制
- **AND** 在获得相应批准前不执行真实副作用

### Requirement: Explore 必须以最短可见事实约束投入

Explore MUST 只有一个最高优先级 question、一个可证伪 hypothesis 和一个 shortest slice，同时最多维护 5 个 active tasks。它 MUST 从真实产品入口优先形成可见事实，并在每 120 分钟或每 5 次提交进行 showcase，以先到者为准；连续 2 小时没有新增可见产品事实时 MUST 缩小问题或停止。

#### Scenario: Explore 没有新增可见事实

- **GIVEN** Explore 连续 2 小时只增加横向框架、文档或治理工件
- **AND** 没有从实际产品入口产生新增可见事实
- **WHEN** 到达 showcase 门
- **THEN** 缩小 question 或 shortest slice，或者停止本轮 Explore
- **AND** 不以补流程材料延长同一投入边界

### Requirement: Explore 只有选中的稳定增量可以进入 Deliver

Explore MUST 只在真实 showcase 后由人选择最小稳定增量并 promote。转换 MUST 明确 selected increment 与 excluded exploration，重新判断 Deliver 的 Quick、Standard 或 High-risk；失败尝试、聊天记录和全部探索历史 MUST NOT 被复制为 Deliver 合同。

#### Scenario: Explore 结果被选择进入交付

- **GIVEN** 人在真实 showcase 后选择一个最小稳定行为
- **WHEN** 将该行为 promote
- **THEN** 只把 selected increment 转为 Deliver scope
- **AND** 重新判断 Quick、Standard 或 High-risk
- **AND** 从转换点开始应用相应 OpenSpec、visual UX、质量和审查门禁

### Requirement: Superpowers 必须通过复杂度门按需选择

Superpowers skill MUST 只在存在实质产品歧义、多种高返工方案、跨组件或难回退架构、复杂跨会话依赖、未知或首次修复失败的故障，或重大合并、发布、完成结论时，选择一个或少数直接相关 skills。会话开始、AI 参与、创作性、时长或文件数量 MUST NOT 单独触发；调用一个 skill MUST NOT 授权或自动串联其他 skills。

#### Scenario: 已有 OpenSpec tasks 足够

- **GIVEN** Deliver Standard change 已有足够清晰的 OpenSpec `tasks.md`
- **WHEN** 准备执行工作
- **THEN** 不再创建 Superpowers plan 或 work brief
- **AND** 状态只更新在现有 `tasks.md`

#### Scenario: 调用一个 Superpowers skill

- **GIVEN** 一个具体复杂问题命中单一 skill 的触发条件
- **WHEN** 调用该 skill
- **THEN** 只取得该 skill 所需的权限和方法
- **AND** 不自动调用 brainstorming、writing-plans、worktree、subagents、review、verification 或 branch finishing

## RENAMED Requirements

- FROM: `### Requirement: 默认流程必须按影响、可逆性和问责性分流`
- TO: `### Requirement: Deliver 必须按影响、可逆性和问责性分流`
- FROM: `### Requirement: Standard 和 High-risk 实现性变更必须默认使用 OpenSpec`
- TO: `### Requirement: Deliver Standard 和 High-risk 实现性变更必须默认使用 OpenSpec`

## MODIFIED Requirements

### Requirement: Deliver 必须按影响、可逆性和问责性分流

只有 Deliver MUST 按影响、可逆性和问责性分为 Quick、Standard 或 High-risk，不得只按任务时长、文件数量或领域关键词决定流程重量。Explore MUST 在 work-mode 层处理，不得被当作第四个风险路径。

#### Scenario: 低风险可逆修改

- **GIVEN** Deliver 工作不影响用户、生产、敏感数据、权限、付款或外部承诺
- **AND** 失败后可以安全撤回
- **WHEN** 开始工作
- **THEN** 可以选择 Quick
- **AND** 不强制创建 OpenSpec 或治理文件
- **AND** 交付时提供产物、验证和剩余风险

#### Scenario: 高影响副作用

- **GIVEN** Deliver 工作涉及生产、删数、客户数据、安全、凭据、付款、公开承诺或不可逆操作
- **WHEN** 准备执行真实副作用
- **THEN** 选择 High-risk
- **AND** 在副作用前记录风险、停止条件和回滚
- **AND** 取得明确人类批准

### Requirement: Deliver Standard 和 High-risk 实现性变更必须默认使用 OpenSpec

研发流程 MUST 在 Deliver Standard 和 High-risk 的代码、配置、schema、API、AI 行为、数据、基础设施或发布设计进入实现前创建或继续一个 OpenSpec change。Deliver Quick 和轻量 Explore MUST NOT 被强制创建 OpenSpec。跳过默认规则 MUST 有明确的人类批准、理由、适用范围和恢复方式。

#### Scenario: 开始 Deliver Standard 用户可见变更

- **GIVEN** Deliver 工作会改变用户可见行为并需要独立验收
- **WHEN** 准备进入实现
- **THEN** 创建或继续一个 OpenSpec change
- **AND** proposal/specs/design/tasks 只承载本次 change 的增量
- **AND** `tasks.md` 成为执行状态的权威来源

#### Scenario: 执行 Deliver Quick 局部修复

- **GIVEN** Deliver 工作低风险、局部、可逆且不影响用户、生产、敏感数据或权限
- **WHEN** 开始实现
- **THEN** 不要求创建 OpenSpec
- **AND** 交付时提供 diff、相关验证和剩余风险

#### Scenario: 轻量 Explore 开始学习

- **GIVEN** 工作符合轻量 Explore sandbox 且目标是降低关键未知
- **WHEN** 开始 shortest slice
- **THEN** 默认不创建 OpenSpec
- **AND** 只维护一份 Explore 短记录

#### Scenario: 用户批准跳过 OpenSpec

- **GIVEN** Deliver Standard/High-risk 实现性变更有特殊原因不使用 OpenSpec
- **WHEN** 用户明确批准豁免
- **THEN** 记录 decision owner、理由、适用范围和恢复方式
- **AND** 执行者不能仅以“已有文档足够”自行豁免

### Requirement: 治理工件必须有预算和可观察用途

每个新增治理域 MUST 记录触发原因、权威入口、改变的决策或门禁以及保留策略。轻量 Explore MUST 只维护一份包含 question、hypothesis、sandbox boundary、shortest slice、active tasks、showcase、evidence/limits、decision 和 next 的短记录；只有命中真实风险、promote 或进入 Deliver 时，才按对应门禁增加治理工件。

#### Scenario: guard 准备创建新治理域

- **GIVEN** 某个专项 guard 被触发
- **WHEN** 准备新增治理文件
- **THEN** 在 project map 登记 domain、trigger、owner、decision_or_gate 和 retention
- **AND** 不为 verifier 或目录完整性创建没有决策或验收价值的文件

#### Scenario: Explore 准备扩展治理工件

- **GIVEN** Explore 已有一份权威短记录
- **WHEN** 准备创建额外 plan、work brief、质量矩阵或状态文件
- **THEN** 只有实际风险门禁或 promote 后的 Deliver 要求可以触发新增
- **AND** 不以工件数量代替可见产品事实
