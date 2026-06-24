# 产品分析、事件埋点与隐私友好实验规范

## W1 触发定位

本文件是 W1 Discovery 的触发型专项规范，不是 W1 主入口。只有当 `docs/W1-discovery/main.md` 已经说明需要产品事件、指标地图、实验分流、第三方 analytics、隐私 review 或数据质量复盘时，才读取本文件。

如果当前问题只是用户、痛点、产品 bet、成功指标或学习决策不清，先回到 `docs/W1-discovery/main.md`，不要从本文件开始。

## 目标

`docs/W1-discovery/main.md` 已经要求每个 product bet 说明用户、问题、指标、反馈和实验。本专项解决更具体的落地问题：当产品真的开始采集事件、看漏斗、做 A/B 或灰度实验时，如何让数据可用、可信、可删除、可解释，并且不把一人公司拖进复杂的数据平台。

默认原则：产品分析只采集能支持决策、排障、成本控制或用户体验改进的事件。没有 tracking plan 的事件不进生产；没有隐私边界和可信度检查的实验不用于发布决策。

## 核心依据

- 《人月神话》：复杂度会从命名、边界和概念不一致里长出来；事件名、属性和指标定义不统一，会让后续所有分析变成猜谜。
- 小型项目管理：一人公司只保留能恢复上下文和支持取舍的最小工件，不为“看起来数据驱动”而增加仪式。
- Lean Startup / Lean Analytics：分析服务于 build-measure-learn；早期优先一个真正代表价值的主指标，避免虚荣指标。
- Google HEART / GSM：先写目标，再找信号，再定义度量；用户体验指标要能连接 happiness、engagement、adoption、retention、task success 中适用维度。
- Trustworthy Online Controlled Experiments：拿到数字很容易，拿到可信数字很难；受控实验必须关注 assignment unit、exposure、stop rule、guardrails、SRM 和数据质量。
- Diagnosing Sample Ratio Mismatch：SRM 是实验数据质量异常的高价值信号，不能在未解释根因时继续把实验结果当真。
- OpenTelemetry semantic conventions：事件是有名称的、有意义时间点上的发生；名称、属性和语义要稳定，才能跨代码、仪表盘和供应商比较。
- Segment / Snowplow / Amplitude tracking plan：产品事件需要先计划事件、属性、来源、用途和所有权，再进入实现。
- W3C Privacy Principles / FTC Protecting Personal Information：数据最小化适用于个人数据；没有业务需要的敏感个人信息不要收集，更不要长期保存。
- Google Analytics PII policy：第三方分析默认不得接收能直接识别、联系或定位个人的信息。
- Vite env 官方文档：`VITE_*` 会进入客户端 bundle，不能放分析供应商 secret 或其他敏感配置。
- OpenFeature evaluation context：实验分流和 feature flag 需要稳定 targeting key，但上下文字段也要控制数据最小化。

## 范围

适用对象：

- Vite 前端的页面、按钮、表单、onboarding、checkout、AI 任务提交、结果查看、导出、通知偏好等用户行为事件。
- Go/Kratos/gRPC 后端的业务 outcome 事件、计费/权益事件、AI workflow 结果事件、实验 exposure 事件。
- 产品漏斗、激活、留存、转化、AI 质量、成本、延迟和错误 guardrail 指标。
- feature flag、灰度、A/B、instrumented beta、pricing/onboarding/copy 实验。
- 第三方 analytics、warehouse、session replay、tag manager、product analytics vendor 或自建事件表。

不适用对象：

- 纯 SRE metrics、logs、traces；这些归 W7 的观测性规范管。
- 产品方向、用户访谈和 bet 判断；这些先回到 `docs/W1-discovery/main.md`。
- 支付账务、权益、审计日志、支持工单的事实记录；这些分别归 W4 计费、W9 审计证据和 W8 支持信任运营管。
- 只在本地开发使用且不离开本机的临时调试日志。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
analytics/
  tracking-plans/<target>.json
  metrics-map/<target>.json
  experiments/<target>.json
  privacy-review/<target>.md
  data-quality-review/<target>.md
```

### `analytics/tracking-plans/<target>.json`

用于定义允许采集什么事件，必须包含：

- `target`、`owner`、`product_area`
- `sources`：frontend、backend、worker、ai_workflow、webhook 中适用项。
- `destinations`：local_db、warehouse、analytics_vendor、observability、none 等。
- `events`：每个事件的名称、触发条件、来源、用途、属性、隐私等级、保留期和状态。
- `identity_policy`：匿名、登录用户、tenant、session、experiment assignment 的处理方式。
- `schema_policy`：命名、属性类型、低基数、版本、弃用方式。
- `forbidden_properties`：禁止进入事件的字段。
- `implementation_links`：Go/Kratos、proto、sqlc、Vite、OpenSpec 或 product bet 链接。
- `human_checkpoint`
- `review_cadence`
- `status`

事件默认规则：

- 事件名使用稳定 snake_case，例如 `report_exported`、`ai_task_result_viewed`。
- 事件名不得包含用户 ID、资源 ID、时间戳、邮箱、动态 path、UUID、实验 variant 或 UI 文案版本。
- 属性默认只允许低基数字段：plan、role、source、status、error_class、latency_bucket、cost_bucket、variant、surface、template_id。
- 禁止属性：email、phone、full_name、raw_ip、precise_location、address、password、secret、token、session_cookie、payment_card、cvv、ssn、raw_prompt、raw_response、raw_user_input、message_body、free_text、url_query。
- 关键 outcome 事件优先由后端或可信边界产生；前端事件只记录 UI 交互和体验路径。
- 每个事件必须能回答一个产品或运营问题；不能解释用途的事件不采集。

### `analytics/metrics-map/<target>.json`

用于把产品问题连接到指标，必须包含：

- `target`、`owner`
- `questions`：当前最重要的产品/增长/AI 行为问题。
- `primary_metric`：唯一主指标。
- `supporting_metrics`
- `guardrail_metrics`
- `metric_definitions`：分子、分母、过滤、时间窗口、去重、归因和查询位置。
- `dashboards`
- `decision_policy`
- `human_checkpoint`
- `review_cadence`
- `status`

默认规则：

- 一次实验或一个产品 bet 默认只有一个主指标。
- 每个指标必须有 event dependency；没有事件依赖的指标不能用于发布判断。
- guardrail 至少覆盖适用的 latency、error、cost、privacy、support complaint、unsubscribe/opt-out、AI safety trigger。
- 归因窗口必须写清楚，例如 24 小时、7 天或 billing cycle；不能用“近期”“活跃用户”等模糊定义。
- dashboard 只回答少数问题：用户是否完成关键任务、哪里掉队、是否伤害 guardrail、下一步该看什么。

### `analytics/experiments/<target>.json`

用于定义实验分流和可信度，必须包含：

- `target`、`owner`
- `experiment_id`
- `linked_product_bet`
- `hypothesis`
- `method`：instrumented_beta、feature_flag_rollout、controlled_experiment、ab_test、holdout 中适用项。
- `assignment_unit`
- `targeting_key_policy`
- `variants`
- `exposure_event`
- `primary_metric`
- `guardrails`
- `sample_plan`
- `stop_rule`
- `trustworthiness_checks`
- `rollback_policy`
- `human_checkpoint`
- `start_date`
- `review_date`
- `status`

默认规则：

- 流量不足时不默认 A/B；优先 instrumented beta、prototype、concierge 或灰度观察。
- 受控实验必须记录 assignment unit，例如 user、tenant、workspace、session；B2B/团队协作产品优先 tenant/workspace，避免同一组织互相污染。
- 必须有 exposure event，且 exposure 不能只等同于“用户在 eligible group 里”。
- trustworthiness checks 至少包含 instrumentation check、sample ratio mismatch check、guardrail check、bot/internal traffic exclusion、missing event check。
- 不能在看到早期漂亮数字后随意提前停止；提前停止必须人工 checkpoint。
- SRM、关键 guardrail 失败、埋点缺失或 assignment 漂移时，实验结果不得用于发布判断，直到写出解释或重跑。

### `analytics/privacy-review/<target>.md`

用于说明为什么可以采集这些产品行为数据，必须包含：

- `Scope`
- `Purpose`
- `Data Classes`
- `Personal Data`
- `Third Party Analytics`
- `Consent / Notice`
- `Retention`
- `Deletion / Export`
- `AI Data Boundary`
- `Session Replay / Recording`
- `Access Control`
- `Open Risks`
- `Review Cadence`

默认规则：

- 不把原始 prompt、response、用户输入、消息正文、完整 URL query、邮箱、手机号、姓名、支付信息或精确位置发给 analytics。
- 第三方 analytics、session replay、跨站追踪、广告归因、数据出口、个人行为画像默认需要人工 checkpoint。
- 如果必须使用 user identifier，优先使用不可反推的内部 surrogate key，并记录用途、保留期和删除路径。
- 产品分析数据默认短保留；超过 13 个月、跨产品合并、导出给第三方或用于训练/个性化，需要人工 checkpoint。

### `analytics/data-quality-review/<target>.md`

用于定期检查数据还能不能信，必须包含：

- `Scope`
- `Recent Changes`
- `Schema Violations`
- `Event Volume`
- `Missing / Duplicate Events`
- `Attribution / Identity`
- `Experiment Trustworthiness`
- `Dashboard Decisions`
- `Privacy Findings`
- `Open Risks`
- `One Next Change`
- `Review Cadence`

默认规则：

- 有付费用户或真实实验：每周检查一次；只有内测：每两周一次。
- 每次改事件名、属性、来源、destination、主指标、分流逻辑或隐私策略后必须复查。
- 任何 dashboard 用于发布、定价、关闭功能、加大触达、提高 AI 自主性或扩大实验范围前，必须确认数据质量 review 不是过期状态。

## Go / Kratos / sqlc / gRPC 默认规则

- 生产后端默认通过一个 analytics/event service 或明确的 usecase hook 发出业务 outcome 事件，不让每个 handler 自由拼事件。
- Protobuf 定义稳定事件 envelope：event_name、occurred_at、source、actor_scope、tenant_scope、request_id、trace_id、experiment_id、variant、properties、schema_version。
- gRPC metadata 只传播 request_id、traceparent、tenant/workspace context、feature flag variant 和实验 assignment；不传播个人敏感值。
- sqlc 表至少区分 raw ingestion、schema violation、experiment assignment、exposure、suppression/deletion state 中适用项。
- 业务 outcome 事件优先在数据库事务成功后或 outbox 中产生，避免前端乐观状态导致漏斗失真。
- provider/vendor client 必须有 timeout、retry、backoff、drop policy 和本地 fallback；分析失败不得阻断核心业务流程，除非是合规或计费事实事件。

## Vite 前端默认规则

- 前端只通过一个 typed analytics client 发事件，不在组件里散落 vendor SDK 调用。
- `VITE_*` 只放公开、可暴露的配置，例如 public write key 或环境名；不得放 server secret、admin token、warehouse credential。
- 默认关闭 autocapture、session replay、DOM/text capture；开启前必须过 privacy review。
- 表单字段、prompt、自由文本、URL query、文件名、邮箱、手机号和真实姓名不进入事件属性。
- 关键 UI 事件连接 Vercel Geist 风格的清晰界面：设置、同意、退出、实验状态和错误提示应克制、可扫描、支持深色模式。
- 前端事件至少能关联 release version、route pattern、feature flag variant、latency bucket 和 error class 中适用项。

## AI workflow 默认规则

- AI 产品事件默认记录 workflow、prompt_version、model_route、tool_names、latency_bucket、token_bucket、cost_bucket、result_class、safety_action、human_correction_required。
- 不记录 raw_prompt、raw_response、raw_tool_output、用户上传文件正文或长文本摘要，除非 W2 安全隐私、W9 审计证据或 W3 AI 数据规范已明确允许保留和访问控制。
- AI 质量指标必须连接 eval 版本和产品事件，不能只看 token 用量或用户点击。
- AI 自动生成分析结论只能作为 draft；发布、定价、提高自主性、扩大触达、改默认模型或删功能的决策必须有人看数据质量 review。

## 需要人判断的关键点

只把这些问题交给人：

- 是否允许第三方 analytics、session replay、tag manager、广告归因或跨站追踪。
- 是否允许采集个人行为分析、稳定用户标识、长保留期或跨产品合并。
- 本轮唯一主指标是否代表真实价值，是否要变更主指标。
- 实验是否可以暴露给真实用户，以及 assignment unit 是否会污染结果。
- SRM、guardrail 失败、埋点缺失或隐私异常后，是停止、修复重跑、回滚还是仅作方向性参考。
- 是否把 dashboard 结果用于发布、定价、扩大 AI 自主性、营销触达或关闭功能。

其他字段完整性、命名、低基数、敏感字段、OpenSpec 链接、review cadence 和 expected-fail 行为交给 Codex 与 verifier。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“采什么、怎么算、怎么实验、是否合规、数据能不能信”，一个人可以按 target 填。
- 保留：只把隐私、主指标、真实用户实验、可信度异常和高影响决策交给人。
- 调整：不强制上仓库/数据平台/BI 工具，JSON 与 Markdown 先形成可审查契约。
- 调整：早期不默认 A/B，防止低流量下制造伪精确。
- 风险：tracking plan 可能写得比实现多。缓解：data quality review 必须看 schema violation、missing/duplicate 和 dashboard decisions。

结论：可落地。一个人可以先为一个 onboarding、AI 任务或 checkout target 写五个文件，用 30 到 60 分钟把数据边界定住，再决定是否接入 vendor。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：主指标、GSM 和 dashboard decision policy 防止只追点击或 PV。
- 工程角度：Go/Kratos event service、Protobuf envelope、sqlc event/assignment 表和 Vite typed client 让埋点可测试。
- 运维角度：分析 vendor 失败不阻断核心路径；关键 outcome 可用 outbox/retry；实验异常有回滚策略。
- 安全隐私角度：数据最小化、PII 禁止字段、第三方 analytics checkpoint 和删除/导出路径降低泄露风险。
- 成本角度：默认不买大平台；高事件量、长保留、session replay、warehouse 导出和 AI telemetry 才触发人审。

结论：可落地。本触发专项把“数据驱动”从口号变成一个小而硬的契约：事件、指标、实验和隐私都能被本地文件和脚本检查。


