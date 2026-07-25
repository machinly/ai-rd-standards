# product-analytics-experiment-standard Specification

## Purpose

定义一人公司产品分析、事件埋点、隐私友好实验和数据质量复审的最小基线，使产品事件、指标、实验和第三方分析在进入生产前有可审查契约。

## ADDED Requirements

### Requirement: 产品行为采集必须具备 analytics 工件

任何生产 target 只要采集产品行为、用户路径、增长转化、AI 使用行为或运行实验，MUST 具备 analytics artifacts。

#### Scenario: 用户行为事件进入生产

- GIVEN 一个 target 会采集产品行为或用户路径
- WHEN 创建研发 OpenSpec change
- THEN 创建 `analytics/tracking-plans/<target>.json`
- AND 创建 `analytics/metrics-map/<target>.json`
- AND 创建 `analytics/privacy-review/<target>.md`
- AND 在 OpenSpec proposal 或 design 中链接 analytics artifacts

#### Scenario: target 运行实验

- GIVEN 一个 target 会运行 instrumented beta、feature flag rollout、controlled experiment、ab_test 或 holdout
- WHEN 准备对真实用户开放
- THEN 创建 `analytics/experiments/<target>.json`
- AND 创建 `analytics/data-quality-review/<target>.md`

### Requirement: Tracking plan 必须定义事件契约和数据边界

Tracking plan MUST 记录 target、owner、product area、sources、destinations、events、identity policy、schema policy、forbidden properties、implementation links、human checkpoint、review cadence 和 status。

#### Scenario: 定义允许采集的事件

- GIVEN 一个 target 需要采集产品 analytics 事件
- WHEN 创建 `analytics/tracking-plans/<target>.json`
- THEN 每个 event 包含 name、description、trigger、source、purpose、properties、privacy_level、retention、status
- AND `name` 使用 stable snake_case
- AND `name` 不包含用户 ID、资源 ID、时间戳、邮箱、动态 path、UUID、variant 或 UI 文案版本

#### Scenario: 事件属性包含敏感或高基数字段

- GIVEN event properties 包含 forbidden properties、个人识别信息、raw prompt、raw response、free text、URL query、payment、secret 或 token
- WHEN 准备发布
- THEN verifier MUST fail
- OR OpenSpec design MUST 记录显式 privacy/security exception、retention、redaction 和 human approval

### Requirement: Metrics map 必须连接问题、主指标、guardrails 和事件依赖

Metrics map MUST 从少量产品问题出发，定义唯一主指标、支持指标、guardrail 指标、指标定义、dashboard、决策策略、人审点和复审节奏。

#### Scenario: 创建 metrics map

- GIVEN 一个 target 的产品分析将用于决策
- WHEN 创建 `analytics/metrics-map/<target>.json`
- THEN 文件包含 questions、primary_metric、supporting_metrics、guardrail_metrics、metric_definitions、dashboards、decision_policy、human_checkpoint、review_cadence、status
- AND primary_metric 引用至少一个 tracking plan event

#### Scenario: AI 产品分析

- GIVEN target 包含 AI workflow
- WHEN 定义 metrics map
- THEN supporting 或 guardrail metrics 覆盖 task completion、human correction、safety trigger、latency 和 cost 中适用项

### Requirement: Experiment plan 必须定义分流、曝光、停止和可信度检查

Experiment plan MUST 记录 experiment id、linked product bet、hypothesis、method、assignment unit、targeting key policy、variants、exposure event、primary metric、guardrails、sample plan、stop rule、trustworthiness checks、rollback policy、人审点、日期和状态。

#### Scenario: 运行受控实验

- GIVEN method 是 controlled_experiment、ab_test 或 holdout
- WHEN 创建 `analytics/experiments/<target>.json`
- THEN 文件包含 assignment_unit、targeting_key_policy、variants、exposure_event、primary_metric、sample_plan、stop_rule、trustworthiness_checks、rollback_policy
- AND trustworthiness_checks 包含 instrumentation check、sample ratio mismatch check、guardrail check、bot/internal traffic exclusion、missing event check

#### Scenario: 实验可信度异常

- GIVEN SRM、guardrail failure、missing event、assignment drift 或 privacy finding 存在
- WHEN 复审实验结果
- THEN 实验结果 MUST NOT 用于发布、定价、扩大 rollout 或提高 AI 自主性
- UNTIL data quality review 记录解释、修复重跑或人工接受为方向性证据

### Requirement: Privacy review 必须记录个人数据、第三方和保留边界

Privacy review MUST 记录 scope、purpose、data classes、personal data、third-party analytics、consent/notice、retention、deletion/export、AI data boundary、session replay、access control、open risks 和 review cadence。

#### Scenario: 使用第三方 analytics 或 session replay

- GIVEN analytics destinations 包含 analytics_vendor、session_replay、tag_manager、advertising_attribution 或 cross_site_tracking
- WHEN 准备上线
- THEN privacy review 说明处理方、数据类别、目的、保留期、退出/删除路径
- AND human_checkpoint 包含 third_party_analytics 或等价条目

### Requirement: Data quality review 必须在高影响决策前保持新鲜

Data quality review MUST 记录 schema violations、event volume、missing/duplicate events、identity/attribution、experiment trustworthiness、dashboard decisions、privacy findings、open risks 和 one next change。

#### Scenario: dashboard 结果将用于高影响决策

- GIVEN dashboard 结果将用于 release、pricing、AI autonomy、marketing outreach、feature shutdown 或 experiment expansion
- WHEN 做出决策
- THEN `analytics/data-quality-review/<target>.md` 不得过期
- AND 不存在未解释的 schema violation、SRM、missing event、duplicate event、privacy finding 或 guardrail failure
