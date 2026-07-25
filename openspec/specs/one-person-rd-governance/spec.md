# one-person-rd-governance Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义一个轻量、可证伪的一人公司 AI 辅助研发内核。默认目标是减少总注意力、恢复和返工成本，同时保留人的产品判断与高影响问责。
## Requirements
### Requirement: 默认流程必须按影响、可逆性和问责性分流

研发入口 MUST 将工作分为 Quick、Standard 或 High-risk，不得只按任务时长或文件数量决定流程重量。

#### Scenario: 低风险可逆修改

- GIVEN 工作不影响用户、生产、敏感数据、权限、付款或外部承诺
- AND 失败后可以安全撤回
- WHEN 开始工作
- THEN 可以选择 Quick
- AND 不强制创建 OpenSpec 或治理文件
- AND 交付时提供产物、验证和剩余风险

#### Scenario: 高影响副作用

- GIVEN 工作涉及生产、删数、客户数据、安全、凭据、付款、公开承诺或不可逆操作
- WHEN 准备执行真实副作用
- THEN 选择 High-risk
- AND 在副作用前记录风险、停止条件和回滚
- AND 取得明确人类批准

### Requirement: 人必须持续拥有产品方向和最终问责

AI 辅助研发 MUST 将产品方向、用户价值、伦理边界、高影响风险和最终问责保留给人，而不是只让人输入目标和处理例外。

#### Scenario: 产品方向变化

- GIVEN 工作会改变目标用户、定价、数据边界或公开承诺
- WHEN AI 识别到该变化
- THEN 停止把它当作普通实现细节
- AND 将证据、选项和影响交给人决定

### Requirement: 新用户能力必须有权威产品输入

新用户能力、新服务或重大体验变化在进入生产性代码、migration 或稳定 API 前，MUST 有经人确认的产品输入、体验设计和验收映射。work brief MUST NOT 替代这些输入。

#### Scenario: 只有执行 brief

- GIVEN 仓库只有实现批次 work brief
- AND 缺少目标用户、产品范围、用户/管理员流程、错误状态或验收设计
- WHEN AI 准备开始生产性实现
- THEN 只允许需求澄清或不可发布原型
- AND 不创建稳定 API、生产 migration 或完成声明

### Requirement: 新应用必须由批准模板生成

新应用 MUST 在空目录由当前批准、可版本化的模板生成并保留 provenance。当前 Go 服务模板是 Kratos CLI 官方脚手架；未来可以由自有应用模板取代。手工目录相似 MUST NOT 被描述为模板同源。

#### Scenario: 创建新 Go 服务

- GIVEN 当前批准的 Go 应用模板来源是 Kratos CLI
- WHEN 初始化新服务
- THEN 记录 CLI 版本、生成命令、模板来源/revision 和首次构建
- AND 不在非空项目根目录手工仿造或覆盖生成

### Requirement: 最终审查必须与生产者自检分离

Standard 和 High-risk 工作 MUST 区分 producer self-check 与 independent final review。

#### Scenario: Standard 工作完成

- GIVEN 执行者已完成产出和自检
- WHEN 进行最终审查
- THEN reviewer 未参与该产出
- AND reviewer 检查目标、acceptance、产物和验证证据
- AND 记录 accept、changes-requested 或 reject

### Requirement: 多组件项目必须有完整本地集成环境

多组件项目 MUST 提供统一、可重复的本地集成入口，实际启动产品要求的全部后端、前端、数据库和必要 mock/provider，并支持 readiness、smoke 和清理。前端 MAY 运行在宿主机，不强制容器化。

#### Scenario: 只有依赖容器和宿主 integration 不足

- GIVEN MySQL、mock provider 或测试工具运行在 Docker
- AND 后端或任一前端没有由统一入口实际启动
- WHEN 汇报验证结果
- THEN 可以声明 dependency-container 和 host integration 通过
- AND MUST NOT 声明 complete local integration 或 browser E2E 已完成

### Requirement: 完成证据必须准确命名覆盖层级

验证证据 MUST 区分 unit、host integration、dependency-container、complete local integration、browser E2E、provider sandbox 和 production observation。

#### Scenario: 完整本地环境通过但没有浏览器路径

- GIVEN 全部后端、前端、MySQL 和必要 mock/provider 已由统一入口启动并完成 smoke
- AND 没有运行真实浏览器用户路径
- WHEN 汇报验证结果
- THEN 可以声明 complete local integration 通过
- AND MUST NOT 声明 browser E2E 已完成

### Requirement: 默认数据栈必须遵循已确认偏好

新 Go 服务 SHOULD 优先 MySQL + sqlc，SQL SHOULD 尽量采用 MySQL/PostgreSQL 通用语法，且默认 MUST NOT 创建 foreign key。例外必须记录原因、不可移植边界和验证方式。

#### Scenario: 无 foreign key 的跨表关系

- GIVEN schema 存在跨表引用且不创建 foreign key
- WHEN 实现创建、更新或删除路径
- THEN 应用层验证引用存在性并定义事务、幂等和删除策略
- AND 使用唯一/非空约束、孤儿数据扫描、修复路径和并发测试证明完整性责任没有丢失

### Requirement: 终止必须保留真实状态

用户停止 Standard 或 High-risk 工作时，执行者 MUST 停止扩大改动，保留已知证据与未完成范围，并在没有额外授权时不提交、推送、重置或删除工作。

#### Scenario: 用户终止未完成批次

- GIVEN 批次存在未提交实现和未解决审查问题
- WHEN 用户要求停止
- THEN 状态记录为 stopped 或 terminated
- AND 记录禁止结论、恢复前置条件和工作区处置边界

### Requirement: AI 行为必须可评估

用户可见 AI 行为变更 MUST 定义代表、边界和失败/拒绝样例，并在高风险场景提供降级或回滚路径。

#### Scenario: 用户可见 AI 行为变化

- GIVEN prompt、model、tool、route、memory 或 retrieval 变化会影响用户结果
- WHEN 规划验证
- THEN 定义最小 eval 和验收标准
- AND 记录至少一个失败或拒绝样例

### Requirement: 更复杂的自主性必须由真实数据证明

多 Agent、无人值守和目标级委托 MUST 保持为实验能力，直到真实任务数据证明净收益且没有增加高风险漏检。

#### Scenario: 试图升级自主性

- GIVEN 仓库没有足够对照任务或独立审查证据
- WHEN 提议扩大自主性
- THEN 保持人主导、AI 辅助
- AND 将试验状态标为 pending

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

每条研发规范试点记录 MUST 记录 `openspec.used`、`change_id`、跳过批准和原因。Standard/High-risk 未使用 OpenSpec 且没有用户事前明确批准时，记录 MAY 作为结构合法的负面证据保留，但 MUST 标记为不合规且不得计入效果样本；只有 `openspec` 对象本身缺失或结构错误时才是格式失败。

#### Scenario: High-risk 试点遗漏 OpenSpec

- GIVEN 一项 High-risk 实现没有创建或继续 OpenSpec change
- WHEN 汇总试点记录
- THEN `openspec.used` 为 false
- AND 记录真实遗漏原因，不追溯性伪造 change id
- AND 没有用户批准例外时该记录保留为 negative evidence 且不计入 eligible 样本
