## ADDED Requirements

### Requirement: 非研发任务必须在读取研发正文前退出

导航 MUST 在加载四分类十一项目、风险路由或 R&D skill 前执行 R&D applicability。Non-R&D 任务 MUST 直接使用自身工作流；混合任务 MUST 只把改变或决定产品/工程系统的部分送入研发规范。

#### Scenario: 普通内容任务打开仓库

- **GIVEN** 任务主要结果是普通写作、翻译、摘要、营销素材或通用查询
- **WHEN** 入口判断需要读取什么
- **THEN** 在读取研发正文前退出
- **AND** 不创建 OpenSpec、研发状态或 Superpowers 工件

### Requirement: Superpowers 运行时必须遵守复杂度作用域

运行时 router 与用户级 Codex instruction MUST 使用同一个 Superpowers complexity scope：只为具体复杂问题选择最小直接相关 skill 集，并明确调用一个 skill 不授权另一个。更近的 repo 或 nested `AGENTS.md` 优先时 MUST 以实际 instruction chain 为准，不得假设用户级默认值机械覆盖项目规则。

#### Scenario: 项目指令与个人默认冲突

- **GIVEN** 用户级 `AGENTS.md` 已部署 scoped Superpowers block
- **AND** 目标仓库存在更近的 `AGENTS.md`
- **WHEN** 在该仓库开始任务
- **THEN** 先读取并应用更近的有效项目指令
- **AND** 冲突会影响试点结论时停止并请求用户决定

## RENAMED Requirements

- FROM: `### Requirement: 根入口必须指向最小三档路径`
- TO: `### Requirement: 根入口必须先判适用性和 Explore / Deliver`
- FROM: `### Requirement: W0-W9 和角色文档必须是可选 playbook`
- TO: `### Requirement: 退役导航不得返回默认入口`
- FROM: `### Requirement: 核心 skill 必须使用三档风险路由`
- TO: `### Requirement: 核心 skill 必须先判适用性并使用 Explore / Deliver`

## MODIFIED Requirements

### Requirement: 根入口必须先判适用性和 Explore / Deliver

README MUST 先提供 R&D applicability，再把适用研发工作分为 Explore 或 Deliver；只有 Deliver 才指向 Quick、Standard、High-risk。入口 MUST 说明 Product Discovery、UX Prototype、Technical Spike 是 Explore 类型，Prototype 是 artifact，Walking Skeleton 是 tactic，并明确当前没有无人值守公司 runtime。

#### Scenario: 打开仓库

- **GIVEN** 用户或 Codex 打开 README
- **WHEN** 决定先读什么
- **THEN** 先判断任务是否适用研发规范
- **AND** 适用时先选择 Explore 或 Deliver
- **AND** 只有 Deliver 再选择 Quick、Standard 或 High-risk
- **AND** Non-R&D 不读取四分类十一项目
- **AND** Deliver Quick 不创建 OpenSpec，Deliver Standard/High-risk 实现性变更创建或继续 active change

### Requirement: 默认读取集合必须保持小

README MUST 独立说明 applicability、Explore / Deliver、Deliver risk routes 和四分类十一项目。任务进入研发后 MUST 只读取一个主要分类入口和一个或少数直接相关项目正文；Non-R&D MUST NOT 为完成适用性判定继续扫描研发正文、完整 playbook、角色文档或来源目录。

#### Scenario: 新任务冷启动

- **GIVEN** 一个新的请求
- **WHEN** 读取默认入口
- **THEN** 先用 README 完成 applicability 和 work-mode 判断
- **AND** Non-R&D 立即退出
- **AND** R&D 只加载一个主要分类和直接相关项目
- **AND** 只有出现具体缺口时才加载一个专项参考

### Requirement: 退役导航不得返回默认入口

已退役的 W0-W9、角色入口、`docs/00-start-here.md` 和 `docs/01-minimal-rd-kernel.md` MUST NOT 重新成为默认或可选操作入口。历史来源只能通过治理账本追溯，不能与四分类十一项目形成第二套 live navigation。

#### Scenario: 查找专项资料

- **GIVEN** Explore 或 Deliver 出现具体专业问题
- **WHEN** 查找补充方法
- **THEN** 从当前正式项目、registered knowledge 或被明确选择的 skill 获取最小相关资料
- **AND** 不恢复 W0-W9、角色文档或已退役最小内核作为操作入口

### Requirement: 核心 skill 必须先判适用性并使用 Explore / Deliver

one-person-openspec-rd skill MUST 先执行 R&D applicability，Non-R&D 立即退出且不读取四分类十一项目。适用研发工作 MUST 先选择 Explore 或 Deliver；只有 Deliver 再选择 Quick、Standard 或 High-risk。skill MUST NOT 默认扫描退役材料、调用 Superpowers 或派生多 Agent；Deliver Standard/High-risk 实现性变更 MUST 默认创建或继续 OpenSpec change。

#### Scenario: 使用核心 skill

- **GIVEN** 用户提出一个请求
- **WHEN** skill 开始路由
- **THEN** 先判断 R&D applicability
- **AND** 适用时选择 Explore 或 Deliver
- **AND** Explore 选择 Product Discovery、UX Prototype 或 Technical Spike 并使用轻量边界
- **AND** Deliver Quick 不创建 OpenSpec
- **AND** Deliver Standard/High-risk 实现性变更创建或继续 active change
- **AND** High-risk 副作用前要求明确人类批准
- **AND** Deliver Standard/High-risk 要求独立最终审查

### Requirement: 知识地图必须反映真实默认入口

docs map、context pack、how-to 和 glossary MUST 将 README、R&D applicability、Explore / Deliver 和四分类十一项目作为 canonical entrypoints；它们 MUST 将 Product Discovery、UX Prototype、Technical Spike 标为 Explore 类型，将 Quick、Standard、High-risk 标为 Deliver 子路由，并将 OpenSpec 标为 Deliver Standard/High-risk 实现性变更的默认 change 载体。退役入口和多 Agent MUST NOT 被描述为默认流程。

#### Scenario: 恢复上下文

- **GIVEN** Codex 读取 `knowledge/docs-map/rd-standards.json`
- **WHEN** 查找默认入口
- **THEN** canonical entrypoints 与 applicability、Explore / Deliver 和四分类十一项目一致
- **AND** 能识别 Explore 的轻量单记录、Deliver Quick 的无 OpenSpec 路径和 Deliver Standard/High-risk 的 active change
- **AND** review、decision、pilot 和历史 archive artifacts 可追溯
