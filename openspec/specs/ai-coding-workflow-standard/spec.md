# ai-coding-workflow-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义 AI 辅助编码的最小边界：采用与普通研发相同的 Quick、Standard、High-risk 路径，保留真实验证和人的高影响决策，不为 AI 参与本身强制生成一套平行治理文件。
## Requirements
### Requirement: AI 参与不得自动增加流程工件

AI-assisted work MUST 按影响、可逆性和恢复需要选择路径。AI 参与本身、任务时长或文件数量 MUST NOT 单独触发流程升级；Quick 不创建 OpenSpec，Standard/High-risk 实现性变更则因风险路径默认创建或继续 OpenSpec change。

#### Scenario: 低风险 AI 辅助修改

- GIVEN AI 修改低风险、局部、可逆的代码或文档
- AND 不影响用户、生产、敏感数据、权限或外部承诺
- WHEN 开始实现
- THEN 可以走 Quick
- AND 不创建 OpenSpec
- AND 只需保留 diff、相关验证和剩余风险

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

### Requirement: Standard 工作只维护一份可恢复状态

需要跨会话恢复、用户可见行为或独立验收的 AI-assisted implementation MUST 在 OpenSpec change 中记录 outcome、non-goals、scope、acceptance、context sources、risks、verification、rollback、decisions needed、status 和 next。同一事实 MUST NOT 再复制到平行 work brief。

#### Scenario: AI 协作跨越一个会话

- GIVEN 工作属于 Standard implementation
- WHEN 建立持久状态
- THEN 创建或继续 OpenSpec change
- AND 使用 `tasks.md` 记录当前状态和下一步
- AND 链接产品输入、测试、review 和设计证据
- AND 不创建内容重复的 work brief
