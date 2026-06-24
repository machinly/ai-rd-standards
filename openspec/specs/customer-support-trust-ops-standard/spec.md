# customer-support-trust-ops-standard 规格

## Purpose

定义一人公司生产产品的客户支持、反馈分流与信任运营规则，确保用户问题能被低成本接收、分类、回复、升级、脱敏记录并反哺产品、工程、AI eval、安全隐私、计费权益和事故沟通。

## Requirements

### Requirement: 生产 target 必须定义 support trust ops artifacts

有外部用户、公开 beta、付费用户、AI 输出或支持承诺的 target MUST 在发布前具备 customer support trust ops artifacts。

#### Scenario: 新生产 target 准备开放用户

- GIVEN 一个 target 有外部用户、付费用户、公开 beta、用户可见 AI workflow 或支持入口
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `support/intake/<target>.json`
- AND 创建 `support/playbooks/<target>.md`
- AND 创建 `support/templates/<target>.md`
- AND 创建 `support/feedback-ledger/<target>.jsonl`
- AND 创建 `support/reviews/<target>.md`

### Requirement: Intake 必须定义入口、分类、严重性、响应目标和数据处理

Support intake MUST 记录 target、owner、channels、categories、severity levels、first response targets、data handling、routing、linked artifacts、metrics、人审点和复审节奏。

#### Scenario: 用户提交支持请求

- GIVEN 用户通过邮件、表单、聊天、社区、GitHub issue、Linear 或产品内入口提交问题
- WHEN support intake 捕获请求
- THEN 请求被分类为 bug、billing/access、incident、privacy/security、AI output concern、feature feedback 或 docs/usability
- AND 系统记录最小必要上下文与响应目标
- AND 不要求用户提交 secret、支付信息、完整 raw prompt 或完整 raw response

### Requirement: Playbook 必须指导一人完成分流、恢复、升级和关闭

Support playbook MUST 记录 scope、triage、severity、first response、reproduction、workaround、escalation、billing/access、AI output complaints、privacy/security requests、incident handoff 和 close criteria。

#### Scenario: 支持请求触发高影响类别

- GIVEN 支持请求涉及多个用户、资金、权限、隐私、安全、AI 输出伤害或服务事故
- WHEN 使用 `support/playbooks/<target>.md`
- THEN playbook 指导先恢复用户或降低影响
- AND 指导链接 OpenSpec、bug、eval、security incident、billing reconciliation 或 docs issue
- AND 高风险动作进入人工 checkpoint

### Requirement: Response templates 必须事实清晰且避免未经验证承诺

Support templates MUST 覆盖 bug/defect、billing/access、AI output concern、privacy/security request、incident update、refund/credit、feature request 和 closure。

#### Scenario: 回复用户支持请求

- GIVEN 需要回复用户
- WHEN 使用 `support/templates/<target>.md`
- THEN 回复承认事实、说明影响、当前动作和下一步
- AND 不承诺未经验证的修复时间、退款、法律结论、数据删除完成、事故恢复时间或 24/7 支持

### Requirement: Feedback ledger 必须把支持事实连接到研发改进

Support feedback ledger MUST 使用脱敏 JSONL 记录 id、date、source、category、severity、summary、evidence、customer impact、linked artifact、next action 和 redacted。

#### Scenario: 支持反馈暴露产品或 AI 行为问题

- GIVEN 一条支持反馈可复现 bug、文档缺口、UX 困惑、计费权益问题、AI eval 缺口或安全隐私风险
- WHEN 写入 `support/feedback-ledger/<target>.jsonl`
- THEN 记录脱敏事实、用户影响和下一步
- AND 链接 OpenSpec change、bug、eval fixture、security record、billing reconciliation 或 docs issue

### Requirement: Support review 必须减少重复联系原因

Support review MUST 记录 queue health、top contact drivers、root cause fixes、product feedback、docs/self-service、AI trust and safety、risks/escalations 和 next one change。

#### Scenario: 完成一次支持复盘

- GIVEN 到达每周或双周支持 review 节奏
- WHEN 更新 `support/reviews/<target>.md`
- THEN 记录 backlog、响应/解决信号、最高频联系原因和风险
- AND 只选择一个最高影响改进作为 next one change

### Requirement: AI 输出投诉必须进入安全、eval 和产品闭环

AI output concern、unsafe output、tool misuse、hallucination affecting money/rights/safety 或 policy risk MUST 记录 model/prompt/workflow/version/request context 并连接 eval、安全或产品修复。

#### Scenario: 用户报告 AI 输出有害或误导

- GIVEN 用户报告 AI 输出包含有害内容、误导、歧视、越权工具动作、账单/权限错误或政策风险
- WHEN 支持流程处理该反馈
- THEN 记录脱敏 request id、model、prompt/workflow version、tool path 和安全类别
- AND 创建或链接 eval case、safety review、product docs fix 或 OpenSpec change
- AND 涉及真实伤害、钱、权限、医疗、法律、安全或隐私时进入人工 checkpoint

### Requirement: Support artifacts 不得保存敏感内容

Support artifacts MUST NOT 保存真实邮箱、电话、姓名、支付信息、secret、生产 token、完整 raw prompt、完整 raw response、完整日志或不必要个人数据。

#### Scenario: 记录支持证据和复现信息

- GIVEN 需要保存用户反馈、复现步骤、截图说明或 AI 输出投诉
- WHEN 写入 `support/` artifacts
- THEN 使用 request id、trace id、feature、错误类别、脱敏摘要和 linked artifact
- AND 不保存真实联系方式、支付信息、secret、完整 raw prompt、完整 raw response 或不必要个人数据
