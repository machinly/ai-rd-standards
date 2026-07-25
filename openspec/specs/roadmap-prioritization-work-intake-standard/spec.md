# roadmap-prioritization-work-intake-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义按需使用的轻量规划与优先级参考。它不得把任务时长、文件数量或 W 阶段当作强制 planning 触发器；产品方向和公开承诺始终由人决定。

## Requirements

### Requirement: 规划重量必须由影响、可逆性和恢复需要决定

Work intake MUST 按用户/生产影响、可逆性、问责性、外部依赖和上下文恢复需要选择 Quick、Standard 或 High-risk。任务时长本身 MUST NOT 强制创建 planning 或 OpenSpec 工件。

#### Scenario: 较长但低风险的局部工作

- GIVEN 工作耗时可能超过半天
- AND 不影响用户、生产、敏感数据、权限、付款或公开承诺
- AND 失败后可以安全撤回并直接验证
- WHEN 选择记录方式
- THEN 可以使用 Quick
- AND 不强制创建 work-intake JSON、roadmap 或 OpenSpec change

#### Scenario: 很短但高风险的动作

- GIVEN 工作只需数分钟
- AND 涉及生产删数、客户数据、凭据、付款或不可逆副作用
- WHEN 选择记录方式
- THEN 使用 High-risk
- AND 在副作用前记录 owner、风险、批准、停止条件和回滚

### Requirement: Planning 工件必须证明净收益并允许合并

Planning artifacts MUST 只在它们能减少优先级重议、跨会话恢复成本或外部承诺歧义时创建。一个 work brief 能承载所需事实时，流程 MUST NOT 强制拆成 strategy map、decision board、roadmap、focus review 和 intake 多份文件。

#### Scenario: 一份记录足够

- GIVEN Standard 工作只有一个 owner 和一个清晰 outcome
- AND 一份 brief 能记录 evidence、scope、non-goals、acceptance、risk、rollback、status 和 next
- WHEN 保存规划状态
- THEN 使用一份 brief
- AND 不重复维护同一事实

### Requirement: 产品取舍和承诺必须由人拥有

AI MUST NOT 自主决定目标用户、产品方向、定价、数据边界、公开日期、客户承诺、SLA 或长期架构锁定。

#### Scenario: 候选工作会改变产品方向

- GIVEN 候选项会改变目标市场、定价、数据用途或客户承诺
- WHEN AI 分析优先级
- THEN 提供证据、选项、代价和不确定性
- AND 由人决定 start、narrow、defer、park 或 reject

### Requirement: Roadmap 必须区分内部预测和外部承诺

如果创建 roadmap，它 MUST 标明 Now/Next/Later 的不确定性、非承诺边界和证据日期；对外版本 MUST 经过人类确认。

#### Scenario: Roadmap 可能被客户看到

- GIVEN roadmap 内容可能进入网站、销售、合同、支持或客户沟通
- WHEN 准备发布或发送
- THEN 明确哪些内容是计划、预测或承诺
- AND 由人确认措辞、日期和责任边界

### Requirement: 无净收益的规划流程必须删除或降级

Planning process MUST 记录其维护成本，并在重复事实、形式通过或维护时间高于决策价值时被合并、降级或删除。

#### Scenario: 规划工件形成重复劳动

- GIVEN 同一事实需要在两个以上 planning 文件重复更新
- OR 连续两次 focus review 没有改变决定、风险或下一步
- WHEN 复查流程成本
- THEN 合并或停止相应工件
- AND 不用新增文档解释原流程为何仍应保留
