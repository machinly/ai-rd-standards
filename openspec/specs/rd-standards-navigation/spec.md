# rd-standards-navigation Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义最小默认入口和按需 playbook 导航，使人和 Codex 不需要先加载 W0-W9、角色、OpenSpec 或多 Agent 材料。
## Requirements
### Requirement: 默认读取集合必须保持小

README MUST 独立说明 applicability、Explore / Deliver、Deliver risk routes 和四分类十一项目。任务进入研发后 MUST 只读取一个主要分类原则和一个或少数直接相关项目原则；只有需要落地规则时，才通过 `docs/execution-details.md` 读取一个或少数命中的第三级主题文件。Non-R&D MUST NOT 为完成适用性判定继续扫描研发正文、完整 playbook、角色文档或来源目录。

#### Scenario: 新任务冷启动

- **GIVEN** 一个新的请求
- **WHEN** 读取默认入口
- **THEN** 先用 README 完成 applicability 和 work-mode 判断
- **AND** Non-R&D 立即退出
- **AND** R&D 只加载一个主要分类原则和直接相关项目原则
- **AND** 需要落地规则时只从执行细节总索引加载命中的主题文件
- **AND** 只有出现具体缺口时才加载一个专项参考

### Requirement: 知识地图必须反映真实默认入口

docs map、context pack、how-to 和 glossary MUST 将 README、R&D applicability、Explore / Deliver、四分类十一项目和 `docs/execution-details.md` 作为 canonical entrypoints；它们 MUST 将 Product Discovery、UX Prototype、Technical Spike 标为 Explore 类型，将 Quick、Standard、High-risk 标为 Deliver 子路由，并将 OpenSpec 标为 Deliver Standard/High-risk 实现性变更的默认 change 载体。退役入口和多 Agent MUST NOT 被描述为默认流程。

#### Scenario: 恢复上下文

- **GIVEN** Codex 读取 `knowledge/docs-map/rd-standards.json`
- **WHEN** 查找默认入口
- **THEN** canonical entrypoints 与 applicability、Explore / Deliver、四分类十一项目和第三级执行细节总索引一致
- **AND** 能识别 Explore 的轻量单记录、Deliver Quick 的无 OpenSpec 路径和 Deliver Standard/High-risk 的 active change
- **AND** review、decision、pilot 和历史 archive artifacts 可追溯

### Requirement: 验证结果必须区分格式、治理和试验

仓库 verifier MUST 分别输出 format_valid、governance_complete 和 pilot_verified，不得用格式 PASS 代表真实任务效果。

#### Scenario: 试验尚未完成

- GIVEN 文件和治理检查通过
- AND 对照任务少于 10 个
- WHEN 运行 python tools/verify_rd_standards.py .
- THEN format_valid 可以 PASS
- AND governance_complete 可以 PASS
- AND pilot_verified 显示 PENDING

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

### Requirement: 退役导航不得返回默认入口

已退役的 W0-W9、角色入口、`docs/00-start-here.md` 和 `docs/01-minimal-rd-kernel.md` MUST NOT 重新成为默认或可选操作入口。历史来源只能通过治理账本追溯，不能与四分类十一项目形成第二套 live navigation。

#### Scenario: 查找专项资料

- **GIVEN** Explore 或 Deliver 出现具体专业问题
- **WHEN** 查找补充方法
- **THEN** 从当前正式项目、registered knowledge 或被明确选择的 skill 获取最小相关资料
- **AND** 不恢复 W0-W9、角色文档或已退役最小内核作为操作入口

### Requirement: 正式正文必须保持三级边界

四个分类 `README.md` MUST 只包含分类标题和分类根本原则；十一个项目 `.md` MUST 只包含项目标题和项目根本原则。全部稳定 `rule-id`、目的边界、核心判断、输入产物、退出条件和主题规则 MUST 位于对应项目的同名第三级目录。`docs/execution-details.md` MUST 逐文件记录分类、项目、内容层和执行细节类型，并且 MUST 覆盖全部第三级文件且不复制规则正文。

#### Scenario: 读取正式正文

- **GIVEN** 四分类十一项目及其执行细节已经发布
- **WHEN** 验证三级结构
- **THEN** 四个分类文件只出现分类原则
- **AND** 十一个项目文件只出现项目原则
- **AND** 2,337 个稳定 rule-id 只出现在第三级细节文件
- **AND** 每个第三级文件在执行细节总索引中恰好映射一次

### Requirement: 核心 skill 必须先判适用性并使用 Explore / Deliver

one-person-openspec-rd skill MUST 先执行 R&D applicability，Non-R&D 立即退出且不读取四分类十一项目。适用研发工作 MUST 先选择 Explore 或 Deliver；只有 Deliver 再选择 Quick、Standard 或 High-risk。skill MUST NOT 默认扫描退役材料、调用 Superpowers 或派生多 Agent；Deliver Standard/High-risk 实现性变更 MUST 默认创建或继续 OpenSpec change。

#### Scenario: 使用核心 skill

- **GIVEN** 用户提出一个请求
- **WHEN** skill 开始路由
- **THEN** 先判断 R&D applicability
- **AND** 适用时选择 Explore 或 Deliver
- **AND** Explore 选择 Product Discovery、UX Prototype 或 Technical Spike 并使用轻量边界
- **AND** 先读取分类原则和项目原则，需要落地时再由执行细节总索引选择命中的主题文件
- **AND** Deliver Quick 不创建 OpenSpec
- **AND** Deliver Standard/High-risk 实现性变更创建或继续 active change
- **AND** High-risk 副作用前要求明确人类批准
- **AND** Deliver Standard/High-risk 要求独立最终审查

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

### Requirement: 已退役执行资产必须退出当前执行面

正式替换完成后，仓库 MUST 把被替换的 active change 归档，并移除没有当前消费者的一次性执行工具、重复计划和已退役 live 文档；仓库 MUST 保留正式规则追溯、人工批准、来源基线和历史审查证据。未完成任务被后续事实覆盖时 MUST 记录 `superseded` 或 `terminated` 结论，不得伪造为完成。

#### Scenario: 正式替换完成后的清理

- **WHEN** 当前状态已经声明正式替换完成，且旧执行资产没有当前入口或消费者
- **THEN** 旧 change 从 active 区归档
- **AND** 一次性工具与重复 live 文档从当前工作树移除
- **AND** 历史治理和规则追溯证据继续可读

#### Scenario: 清理不得扩大范围

- **WHEN** 仓库同时存在其他 active change、试点或用户未提交工作
- **THEN** 清理只作用于明确 allowlist
- **AND** 当前 change、试点和本地受保护运行态内容保持不变

### Requirement: 本地运行态资产不得进入版本控制

仓库 MUST 忽略可重建的 Agent/预览服务运行态目录和语言缓存；清理已有运行态内容前 MUST 确认相关进程与保留决定，且不得读取或输出 token、secret 或其他敏感值。

#### Scenario: 本地运行态目录存在

- **WHEN** `.agents/`、`.superpowers/` 或 Python cache 出现在工作区
- **THEN** Git 不把这些目录作为待提交正式资产
- **AND** 可重建 cache 可以安全删除
- **AND** 受保护或可能含敏感内容的目录只在明确授权后处置
