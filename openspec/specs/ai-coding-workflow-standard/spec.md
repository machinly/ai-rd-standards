# ai-coding-workflow-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义 AI 辅助编码的最小边界：采用与普通研发相同的 Quick、Standard、High-risk 路径，保留真实验证和人的高影响决策，不为 AI 参与本身强制生成一套平行治理文件。
## Requirements
### Requirement: AI 参与不得自动增加流程工件

AI-assisted work MUST 先执行 R&D applicability；Non-R&D 使用任务自身流程。适用研发工作 MUST 先选择 Explore 或 Deliver，只有 Deliver 再按影响、可逆性和恢复需要选择 Quick、Standard 或 High-risk。AI 参与本身、会话开始、创作性、任务时长或文件数量 MUST NOT 单独触发流程或 Superpowers 升级；Deliver Quick 和轻量 Explore 不创建 OpenSpec，Deliver Standard/High-risk 实现性变更因风险路径默认创建或继续 OpenSpec change。

#### Scenario: 低风险 AI 辅助修改

- **GIVEN** AI 修改低风险、局部、可逆的代码或文档
- **AND** 不影响用户、生产、敏感数据、权限或外部承诺
- **AND** 目标行为已经明确
- **WHEN** 开始实现
- **THEN** 可以走 Deliver Quick
- **AND** 不创建 OpenSpec 或 Superpowers 工件
- **AND** 只需保留 diff、相关验证和剩余风险

#### Scenario: 非研发创作任务

- **GIVEN** AI 执行不改变或决定产品/工程系统的创作任务
- **WHEN** 开始工作
- **THEN** 使用该任务自身流程
- **AND** 不因创作性调用 R&D router 或 Superpowers

### Requirement: 长任务状态必须是事实记录而不是过程表演

跨会话或多批次工作 MUST 保留 changes made、commands run、decisions、assumptions、failures、current status 和 next；同一事实 MUST 有一个权威记录位置。

#### Scenario: 完成一个实现批次

- GIVEN AI 完成一个可独立验证的批次
- WHEN 更新状态记录
- THEN 记录实际变更和真实命令结果
- AND 披露失败、跳过、偏离和残余风险
- AND 不为满足模板复制 proposal、design、tasks 和 batch log 中的相同文本

### Requirement: 生产者自检必须与独立最终审查分离

Producer Self-Check MUST 检查 outcome、acceptance、scope、用户已有修改、真实验证、失败披露和 High-risk 触发。Standard 与 High-risk 的 Independent Final Review MUST 由未参与产出的 reviewer 执行；两个自检镜头 MUST NOT 被称作两轮独立 review。

#### Scenario: AI 实现已经自检

- GIVEN 生产者完成 diff 和 self-check
- WHEN 判断工作是否最终接受
- THEN reviewer 使用目标版本、acceptance、diff 和验证证据重新检查
- AND 记录 accept、changes-requested 或 reject
- AND 生产者不得自行填写独立接受结论

### Requirement: 验证必须匹配实际变更风险

AI-assisted work MUST 运行与变更相关的测试、构建、eval、contract、安全或人工验收；不存在或不适用的检查不得伪造为通过。

#### Scenario: 用户可见 AI 行为变化

- GIVEN prompt、model、tool、route、memory 或 retrieval 变化会影响用户结果
- WHEN 验证工作
- THEN 使用代表、边界和失败/拒绝样例
- AND 记录可复现的 eval 结果与回滚或降级路径

### Requirement: 高影响副作用必须停在人类批准前

Production deploy、real data/secret/vendor access、destructive operation、payment、external communication、auth/tenant boundary、test deletion 或 autonomy increase MUST 触发明确人类 checkpoint。

#### Scenario: AI 准备执行高影响动作

- GIVEN 工作将产生高影响副作用
- WHEN 预检查完成
- THEN 记录目标、影响范围、证据、停止条件和回滚
- AND 在人类批准前不得执行真实副作用

### Requirement: 持久工件不得保存敏感原文

AI coding artifacts MUST NOT 保存真实 secret、真实用户数据、供应商凭据、不必要的 raw prompt/response 或可识别个人信息。

#### Scenario: 保存协作证据

- GIVEN 需要记录上下文和验证
- WHEN 写入仓库
- THEN 保存可信来源链接、行为版本、脱敏 fixture、命令、结果和风险摘要
- AND 对敏感字段删除、脱敏或只保存安全引用

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

### Requirement: Deliver Standard 工作只维护一份可恢复状态

需要跨会话恢复、用户可见行为或独立验收的 Deliver Standard AI-assisted implementation MUST 在 OpenSpec change 中记录 outcome、non-goals、scope、acceptance、context sources、risks、verification、rollback、decisions needed、status 和 next。同一事实 MUST NOT 再复制到平行 work brief、Superpowers spec 或 plan。Explore MUST 使用单一短记录而不是预建 Deliver 状态体系。

#### Scenario: AI 协作跨越一个会话

- **GIVEN** 工作属于 Deliver Standard implementation
- **WHEN** 建立持久状态
- **THEN** 创建或继续 OpenSpec change
- **AND** 使用 `tasks.md` 记录当前状态和下一步
- **AND** 链接产品输入、测试、review 和设计证据
- **AND** 不创建内容重复的 work brief 或 Superpowers plan

#### Scenario: Explore 跨越一个会话

- **GIVEN** 轻量 Explore 需要在下一会话恢复
- **WHEN** 保存当前事实
- **THEN** 只更新包含 question、hypothesis、sandbox boundary、shortest slice、active tasks、showcase、evidence/limits、decision 和 next 的单一短记录
- **AND** 不因此自动创建 OpenSpec

### Requirement: Explore AI 实现必须优先最短可见切片

AI-assisted Explore MUST 优先从一个实际产品入口经过必要组件形成一个可见业务结果，再扩展横向框架、恢复矩阵、平台化或完整质量工件。它 MAY 实现不可发布的最小代码，但 MUST 保持 sandbox boundary，且不得把可运行探索声明为生产就绪。

#### Scenario: Technical Spike 准备横向建设

- **GIVEN** Technical Spike 尚未形成一条从实际产品入口到可见结果的 Walking Skeleton
- **WHEN** AI 准备增加通用框架、完整异常矩阵或平台抽象
- **THEN** 先关闭 shortest visible slice
- **AND** 延后与该可见事实无关的横向建设

### Requirement: 测试先行必须按行为风险选择

AI-assisted work MUST 对核心领域规则、服务端授权、安全边界、数据一致性、公共契约、bugfix 和危险重构优先测试先行。抛弃式 UI 脚手架、生成代码、简单配置和 UX/Technical Explore MAY 先实现后补只对 selected behavior 有价值的自动化；Explore promote 前 MUST 为准备稳定的行为补齐与风险相称的回归证据。

#### Scenario: 抛弃式 UX Prototype

- **GIVEN** UX Prototype 只在本地 sandbox 比较流程且不会 promote 当前实现
- **WHEN** AI 生成抛弃式界面脚手架
- **THEN** 不强制为全部失败探索先写自动化测试
- **AND** showcase 仍使用实际入口、可理解 fixture 并准确记录证据限制

#### Scenario: 授权规则进入稳定实现

- **GIVEN** selected increment 包含服务端授权行为
- **WHEN** 它准备 promote 或进入 Deliver
- **THEN** 优先用失败测试锁定授权边界
- **AND** 不以探索期豁免跳过稳定行为回归证据

### Requirement: Superpowers 调用不得自动串联或复制权威工件

AI MUST 只为具体复杂度触发选择最小直接相关 Superpowers skill 集。调用一个 skill MUST NOT 自动授权另一个；当产品文档、技术设计、Explore iteration record 或 OpenSpec 已拥有事实和状态时，AI MUST 链接或更新该权威工件，不得创建重复 Superpowers spec、plan、work brief 或状态文件。

#### Scenario: OpenSpec tasks 已拥有状态

- **GIVEN** Deliver Standard change 已有足够的 proposal、design 和 `tasks.md`
- **WHEN** AI 开始执行多步骤实现
- **THEN** 更新现有 `tasks.md`
- **AND** 不自动调用 writing-plans 或创建平行计划

#### Scenario: 一个复杂故障命中 debugging

- **GIVEN** 跨服务偶发失败且首次修复无效
- **WHEN** AI 选择 systematic-debugging
- **THEN** 只使用该 skill 处理当前未知故障
- **AND** 不因此自动调用 brainstorming、subagents、code review 或 branch finishing
