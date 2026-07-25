# product-discovery-feedback-loop-standard 的变更规格

## ADDED Requirements

### Requirement: 用户可见能力必须定义产品学习工件

超过 1 个工作日的用户可见能力、付费能力、增长实验或 AI workflow MUST 在进入实质研发前具备产品学习 artifacts。

#### Scenario: 新用户可见能力进入研发

- GIVEN 一个能力会改变用户体验、转化、留存、成本、信任或关键任务完成率
- WHEN 创建研发 OpenSpec change
- THEN 创建 `product/bets/<capability>.md`
- AND 创建 `product/metrics/<capability>.json`
- AND 创建 `product/experiments/<capability>.json`
- AND 在 OpenSpec proposal 或 design 中链接 product bet

#### Scenario: 小 bug fix 或纯内部重构

- GIVEN 一个改动不改变用户体验、成本、安全、权限、数据处理或产品指标
- WHEN 不创建 product artifacts
- THEN 在 OpenSpec tasks 或变更说明中记录不适用原因

### Requirement: Product bet 必须定义用户、问题、范围和学习目标

Product bet MUST 记录目标用户、真实问题、投入上限、范围、非范围、风险、学习目标、OpenSpec 链接和决策日期。

#### Scenario: 创建 product bet

- GIVEN 一个能力准备进入超过 1 个工作日的研发
- WHEN 创建 `product/bets/<capability>.md`
- THEN 文档包含 Target User、Problem、Appetite、Scope、Out of Scope、Risks、Learning Goal、OpenSpec Link、Decision Date

#### Scenario: 大于 1 周的 bet

- GIVEN `Appetite` 大于 1 周
- WHEN 创建 product bet
- THEN `product/feedback/<capability>.jsonl` 至少包含 3 条反馈记录
- OR 在 bet 中显式记录无用户证据风险和人工接受

### Requirement: Metrics 必须连接 outcome、GSM、guardrails 和事件

产品指标定义 MUST 从一个 outcome 出发，映射 goal、signals、metrics、guardrails 和可采集事件。

#### Scenario: 创建 metrics record

- GIVEN 一个能力准备进入实验
- WHEN 创建 `product/metrics/<capability>.json`
- THEN 文件包含 `capability`、`owner`、`outcome`、`goal`、`signals`、`metrics`、`guardrails`、`events`、`privacy`、`review_cadence`、`human_checkpoint`

#### Scenario: AI 产品能力

- GIVEN 能力包含 AI prompt、model、tool 或 agent workflow
- WHEN 定义 metrics
- THEN metrics 或 guardrails 覆盖任务完成、人工修正、拒答/误答、安全触发、成本和延迟中适用项

### Requirement: 产品事件必须稳定、低基数且隐私安全

产品 analytics 事件 MUST 使用稳定事件名、低基数字段和最小个人数据。

#### Scenario: 定义事件

- GIVEN metrics record 包含 events
- WHEN 校验事件
- THEN 每个 event 包含 name、trigger、source、properties
- AND `name` 使用 snake_case
- AND `name` 不包含用户 ID、资源 ID、时间戳、邮箱、动态 path 或 UUID

#### Scenario: 事件包含个人行为分析

- GIVEN 事件会采集个人行为、session replay、跨站追踪或第三方 analytics
- WHEN 准备发布
- THEN `privacy` 记录数据类别和处理方
- AND `human_checkpoint.required_for` 包含 `personal_behavior_analytics` 或等价条目

### Requirement: Experiment 必须定义假设、方法、阈值、guardrails 和决策规则

产品实验 MUST 在实现前定义假设、方法、样本、成功阈值、guardrails、开始日期、复审日期、人审点和决策规则。

#### Scenario: 创建 experiment record

- GIVEN 一个能力准备进入实验
- WHEN 创建 `product/experiments/<capability>.json`
- THEN 文件包含 `capability`、`owner`、`hypothesis`、`method`、`sample`、`success_threshold`、`guardrails`、`decision_rule`、`start_date`、`review_date`、`human_checkpoint`

#### Scenario: 使用受控实验

- GIVEN `method` 是 controlled_experiment、ab_test 或等价方式
- WHEN 创建 experiment record
- THEN 文件包含 `assignment_unit`、`primary_metric`、`stop_rule`、`trustworthiness_checks`
- AND guardrails 覆盖错误、延迟、成本或用户伤害中适用项

### Requirement: Feedback 必须记录具体用户证据

产品反馈 MUST 记录来自访谈、支持、销售、beta、可用性测试或产品事件的具体证据，且避免不必要个人数据。

#### Scenario: 创建 feedback record

- GIVEN 一个能力准备复审
- WHEN 写入 `product/feedback/<capability>.jsonl`
- THEN 每行 JSON 包含 `id`、`date`、`source`、`persona`、`problem`、`evidence`、`tags`
- AND 不包含密钥、密码、token、完整邮箱、手机号或支付信息

### Requirement: Decision 必须关闭学习闭环

实验复审后 MUST 写出 keep、kill、pivot 或 iterate 决策，并定义下一步。

#### Scenario: 到达 decision date

- GIVEN 到达 product bet 的 Decision Date 或 experiment review_date
- WHEN 复审证据
- THEN 创建或更新 `product/decisions/<capability>.md`
- AND 文档包含 Evidence Summary、Decision、Why、Next Step、Review Cadence
- AND Decision 是 keep、kill、pivot 或 iterate 之一

#### Scenario: 决策后继续研发

- GIVEN Decision 是 keep、pivot 或 iterate
- WHEN 进入下一轮研发
- THEN 创建或更新 OpenSpec change
- AND 链接上一轮 decision
