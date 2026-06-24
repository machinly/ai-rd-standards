# trust-policy-compliance-standard 规格

## ADDED Requirements

### Requirement: 生产 target 必须定义 trust policy artifacts

有外部用户、付费用户、AI 输出、用户数据处理或对外政策/承诺的 target MUST 在发布前具备 trust policy compliance artifacts。

#### Scenario: 新生产 target 准备公开发布

- GIVEN 一个 target 有外部用户、付费用户、AI 输出、用户数据处理、官网承诺、隐私/条款/退款/安全声明或 AI disclosure
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `trust/commitment-register/<target>.json`
- AND 创建 `trust/policy-surfaces/<target>.md`
- AND 创建 `trust/ai-disclosure/<target>.md`
- AND 创建 `trust/data-rights/<target>.md`
- AND 创建 `trust/compliance-review/<target>.md`

### Requirement: Commitment register 必须把对外 claim 连接到证据

Commitment register MUST 记录 target、owner、audiences、claims、evidence、policy dependencies、supplier dependencies、regulated domains、人审点和复审节奏。

#### Scenario: 发布或修改对外承诺

- GIVEN 官网、产品内、帮助文档、隐私页、条款、AI disclosure、销售材料或客服模板出现对外 claim
- WHEN 写入 `trust/commitment-register/<target>.json`
- THEN 每个 claim 包含 id、surface、claim_text、claim_type、risk_level、evidence_ref、owner、last_verified 和 status
- AND 没有 evidence_ref 的 claim 不得标为 production-ready

### Requirement: Policy surfaces 必须列出用户能找到的政策入口

Policy surfaces MUST 记录 scope、user-facing surfaces、required policies、privacy/data use、terms/AUP、security claims、billing/refund claims、change notice、owner/review cadence 和 linked artifacts。

#### Scenario: 用户查找产品政策

- GIVEN 用户需要了解隐私、条款、AI 限制、安全联系、账单/退款或数据权利
- WHEN 查看产品或官网
- THEN policy surfaces 记录对应入口和 owner
- AND 入口连接到真实政策页面、帮助页、产品内说明或 runbook

### Requirement: AI disclosure 必须说明 AI 使用、能力、限制、人审、数据和反馈

AI disclosure MUST 记录 where AI is used、what AI can do、known limitations、human oversight、user controls、data sent to models、safety/abuse handling、high impact boundaries、feedback/appeal 和 version/review。

#### Scenario: 用户使用 AI 功能

- GIVEN 用户进入用户可见 AI workflow
- WHEN 产品展示 AI 功能或说明
- THEN 用户能知道何处使用 AI、AI 的能力与限制、数据是否发送到模型、如何反馈/申诉
- AND 高影响领域说明人工流程、专业边界或不适用范围

### Requirement: Data rights runbook 必须定义删除、导出、更正、opt-out 和处理方协作

Data rights runbook MUST 记录 scope、data inventory link、request types、identity verification、response targets、deletion/export/correction、opt-out/consent、processor/supplier handling、exceptions、audit trail 和 human checkpoints。

#### Scenario: 用户提交数据权利请求

- GIVEN 用户请求删除、导出、更正、停止使用、撤回同意或了解数据用途
- WHEN 使用 `trust/data-rights/<target>.md`
- THEN runbook 指导身份验证、响应目标、应用数据处理、供应商处理和审计记录
- AND 不为验证身份收集过量数据

### Requirement: Compliance review 必须复查 claim、数据用途、供应商政策和用户权利变化

Compliance review MUST 记录 recent changes、claim changes、data use changes、AI policy/provider changes、user rights requests、regulated domain check、open risks 和 next one change。

#### Scenario: 发布前或周期性信任复盘

- GIVEN target 有近期页面、政策、AI workflow、数据流、供应商或用户权利流程变化
- WHEN 更新 `trust/compliance-review/<target>.md`
- THEN 记录变化、风险、人审状态和下一步
- AND 只选择一个最高影响改进作为 next one change

### Requirement: 高风险信任和合规决策必须人工 checkpoint

New legal/policy/AI/billing/security claim、professional-grade AI claim、sensitive data、minor data、high-impact domain、data use/training/retention change、new supplier/data flow、unproven claim、policy-implementation mismatch 或 legal/professional review need MUST 有人工 checkpoint。

#### Scenario: 对外承诺触发高风险条件

- GIVEN OpenSpec change、release、页面文案、隐私/条款、AI disclosure、供应商设置或数据流程触发高风险条件
- WHEN 准备合并、发布或执行
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND commitment register、policy surface、AI disclosure、data rights 或 compliance review 记录需要人的判断

### Requirement: Trust artifacts 不得保存敏感内容

Trust artifacts MUST NOT 保存真实用户数据、secret、生产 token、供应商凭据、合同原文、完整 raw prompt、完整 raw response、银行卡数据或不必要个人联系方式。

#### Scenario: 记录承诺证据和政策依赖

- GIVEN 需要保存 claim 证据、供应商条款、数据权利请求或 AI disclosure 依据
- WHEN 写入 `trust/` artifacts
- THEN 使用引用、摘要、policy version、redacted example、eval id、配置路径或 runbook 链接
- AND 不保存真实用户数据、secret、生产 token、供应商凭据、合同原文、完整 raw prompt、完整 raw response、银行卡数据或不必要个人联系方式
