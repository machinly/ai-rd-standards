# AI 模型、供应商路由与降级治理规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/main.md` 已经判断需要改变默认模型、供应商、route、fallback、成本/延迟边界或 provider review 时，才读取本文件。

如果当前只是判断 AI 行为应该如何定义好坏、失败和降级，先回到 `docs/W3-ai-behavior/main.md`。

## 目标

AI 产品的模型选择很容易从“临时改一个 model name”变成不可复盘的行为变化：质量、延迟、成本、拒答风格、工具调用、上下文窗口、数据保留和供应商可用性都会一起变。本专项定义 AI 模型、供应商路由与降级治理规范，让每个用户可见 AI capability 都能回答：默认走哪条模型路线、为什么选它、什么时候降级、如何评测候选模型、失败时用户看到什么、哪些数据能发给哪个供应商、何时需要人判断。

默认原则：模型不是配置字符串，而是产品行为契约。任何生产默认模型、供应商、fallback、reasoning effort、工具能力或数据边界变化，都必须有路由工件、eval gate 和回滚路径。

## 核心依据

- 《人月神话》：没有“换模型就解决”的银弹；真正困难的是概念完整性、接口边界和变更控制。
- 小型项目管理：一人公司不能维护复杂 AI gateway 平台；只保留 model registry、route policy、fallback runbook、eval gate、provider review 五个可执行工件。
- Google Rules of ML：先保证端到端 pipeline、指标和简单基线，再增加模型复杂度；早期模型不必花哨，但基础设施必须可信。
- Hidden Technical Debt in ML Systems：ML/AI 系统容易因为 glue code、配置、隐式依赖、纠缠和反馈环积累隐性债务；模型路由必须显式化。
- OpenAI Model Selection：先优化准确性并建立 eval dataset，再在达到质量目标后优化成本和延迟。
- OpenAI Models / GPT-5.5 migration：最新模型能力、推荐和迁移方式会变化；新模型族不能当成 drop-in replacement，需要 fresh baseline、代表样例和 prompt/route 调整。
- OpenAI Latency / Cost / Rate Limits / Error Codes：生产 AI 调用需要管理 token、输出长度、模型大小、Batch/Flex/Priority、rate limit、timeout、retry 和 5xx/503/429 等错误。
- Google SRE Handling Overload / Cascading Failures：过载不可避免；可靠服务要提前设计 degraded response、限流、拒绝和恢复，避免供应商故障放大为级联故障。
- OpenTelemetry GenAI Semantic Conventions：模型、供应商、prompt、token、stream、finish reason、tool call、retrieval 和 latency 应进入标准化遥测，而不是散落日志。

## 范围

适用对象：

- 用户可见 AI capability 的默认模型、候选模型、reasoning effort、temperature、output token、streaming、tool use、structured output、batch/flex/priority processing。
- OpenAI、Azure OpenAI、Anthropic、Google、开源模型、embedding、reranker、moderation、image/audio/realtime 模型等供应商或模型路线。
- Go/Kratos/sqlc/gRPC 后端里的模型路由、provider adapter、timeout、retry、fallback、budget、telemetry、audit 和 config/feature flag。
- Vite 前端里的降级提示、排队/异步状态、低置信或受限能力提示、重试入口和高成本能力开关。

不适用对象：

- W3 prompt/eval 细节；本专项关注模型路线和供应商执行边界。
- W2 的整体成本预算；本专项只要求 route 级成本/延迟限制并链接成本工件。
- W4 Feature Flag 平台；本专项只定义模型路由必须如何被配置和回滚。
- 自建训练平台、复杂多云 AI gateway、自动模型竞价、企业采购流程；这些需要单独 OpenSpec change。

## 最小工件

每个有生产 AI 调用的 capability 使用同一个 `<capability>` 文件名：

```text
ai-routing/
  model-registry/<capability>.json
  route-policy/<capability>.md
  fallback-runbook/<capability>.md
  eval-gate/<capability>.json
  provider-review/<capability>.md
```

### `ai-routing/model-registry/<capability>.json`

Model registry 必须包含：

- `capability`
- `owner`
- `providers`
- `routes`
- `default_route`
- `budgets`
- `latency_slo`
- `quality_gate`
- `safety_gate`
- `telemetry`
- `human_checkpoint`
- `review_cadence`

`providers` 每项至少包含：

- `id`
- `name`
- `kind`
- `data_boundary`
- `retention`
- `auth_ref`
- `status`

`routes` 每项至少包含：

- `id`
- `purpose`
- `provider`
- `model`
- `model_family`
- `input_modalities`
- `output_modalities`
- `reasoning_effort`
- `max_input_tokens`
- `max_output_tokens`
- `timeout_ms`
- `retries`
- `stream`
- `cache_policy`
- `cost_tier`
- `latency_target_ms`
- `fallback_chain`
- `eval_refs`
- `safety_refs`
- `status`

默认：

- `default_route` 必须指向 `routes[].id`。
- 生产 route 不允许只写 `latest`、`auto`、`default`、`best` 这类不可复盘模型名；可以使用官方 latest guide 做选择依据，但落地工件必须记录当时的模型族、route id、eval 日期和回滚路线。
- `fallback_chain` 至少包含一个用户可见降级策略：较小模型、缓存答案、异步队列、只返回检索摘要、人工处理、关闭非核心 AI 能力或明确失败。
- `timeout_ms` 和 `retries` 必须有限；默认不对有副作用工具调用做自动重试。
- route 的 `eval_refs` 和 `safety_refs` 必须指向 W3 prompt/eval、数据集、红队或内容安全相关工件，或说明为什么暂不适用。

### `ai-routing/route-policy/<capability>.md`

Route policy 必须包含：

- `Scope`
- `Decision Matrix`
- `Default Route`
- `Model Selection`
- `Reasoning / Tool Use`
- `Fallback / Degradation`
- `Timeouts / Retries`
- `Cost / Latency`
- `Data Boundary`
- `Safety / Privacy`
- `Telemetry`
- `Human Checkpoints`
- `Linked Artifacts`

默认：

- 先定义任务类型，再选模型：简单分类、结构化抽取、摘要、代码/推理、长上下文、工具代理、低延迟聊天、后台批处理要走不同 route。
- 先用最能达标的模型建立准确率 baseline，再用较小、较快、较便宜的路线挑战 baseline。
- reasoning effort、tool use、long context、image/audio、web/file search 不是“越多越好”；默认只给当前任务必要能力。
- 用户可见核心路径要有 fallback；非核心 AI enhancement 可以 fail closed 或关闭。
- 任何不可信输入、RAG 文档、用户上传文件、网页内容、support ticket 和工具输出，不得改变 developer/system 指令。

### `ai-routing/fallback-runbook/<capability>.md`

Fallback runbook 必须包含：

- `Scope`
- `Failure Modes`
- `Detection Signals`
- `Immediate Actions`
- `Degradation Modes`
- `Rollback`
- `User Messaging`
- `Provider Escalation`
- `Recovery Check`
- `Post-Incident Review`
- `Linked Artifacts`

默认：

- failure modes 至少覆盖：rate limit、timeout、provider 5xx/503、模型输出不合 schema、safety block、成本阈值、延迟超 SLO、质量 eval 失败、供应商状态异常。
- degradation modes 默认从低风险开始：减少输出 token、降低检索数量、切小模型、关闭工具、转异步、使用缓存、只返回可验证来源、人工处理。
- retry 必须有上限、backoff 和错误分类；429/503/timeout 可重试，400/401/403、schema 错误、权限错误和安全拒绝默认不盲目重试。
- 用户提示要诚实但短：说明功能暂时降级、可重试或已转入后台，不暴露供应商内部错误和敏感路由细节。

### `ai-routing/eval-gate/<capability>.json`

Eval gate 必须包含：

- `capability`
- `owner`
- `baseline_route`
- `candidate_route`
- `datasets`
- `metrics`
- `thresholds`
- `cost_latency_limits`
- `safety_checks`
- `rollout`
- `rollback`
- `evidence_refs`
- `human_checkpoint`
- `status`

默认：

- 默认模型、供应商、reasoning effort、工具能力、structured output schema、fallback chain 或 context window 变化前，必须跑相关 eval。
- 至少比较 baseline 与 candidate：质量、拒答/安全、schema 成功率、tool call 成功率、p95 latency、token/cost、超时率、fallback 触发率。
- 不能只看主观“感觉更聪明”；必须有代表样例、边界样例、失败样例和至少一个用户影响指标。
- rollout 默认 staged：local eval、shadow 或 small cohort、监控、扩大、保留 rollback route。

### `ai-routing/provider-review/<capability>.md`

Provider review 必须包含：

- `Recent Changes`
- `Quality Results`
- `Cost / Latency`
- `Reliability`
- `Safety / Privacy`
- `Provider Terms / Data Boundary`
- `Incidents`
- `Open Risks`
- `Next One Change`

默认：

- pre-revenue：每月一次，或任何生产默认 route / provider change 前。
- 有活跃用户：每两周一次，或重大模型发布、供应商价格/限制/数据政策变化、AI incident 后。
- 每次只选一个最高影响改进，避免一个人陷入“持续调模型”的黑洞。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端使用一个显式 `ModelRouter` 或等价 usecase，输入 capability、task type、tenant/user、risk tier、latency class、budget class、required tools、data boundary，输出 route id 和 request options。
- 不在业务代码散落硬编码 model name、provider URL、timeout、max token、reasoning effort、temperature；这些必须来自 route registry、配置或 feature flag，并可审计。
- Provider adapter 只暴露稳定内部接口：`Generate`、`GenerateStructured`、`Embed`、`Moderate`、`Rerank`、`Stream` 等；不要让上游业务直接依赖供应商 SDK 结构。
- gRPC error model 必须区分：用户输入错误、权限错误、budget/capacity 限制、供应商暂时不可用、供应商永久错误、schema/parse 失败、安全拒绝、内部错误。
- sqlc 默认表可包含：`ai_model_routes`、`ai_model_route_versions`、`ai_provider_events`、`ai_route_eval_runs`、`ai_route_fallback_events`。
- request context 必须有 deadline；provider 调用必须记录 route id、provider、model、prompt/workflow version、eval version、timeout、retry count、latency、token、cost bucket、fallback reason。
- 自动 retry 只用于无副作用、可幂等、瞬时错误；工具调用、支付、写数据、发通知、权限变更前后都不得由模型 route 层盲目重试。

## Vite 前端默认规则

- 用户可见 AI 能力降级时，界面应提供简短状态：生成较慢、功能暂时受限、已转后台、可重试或已使用基础模式。
- 高成本/慢速模式使用明确按钮或切换；不要把“更贵更慢的模型”藏成默认体验。
- 如果结果来自 fallback、缓存、较小模型或受限上下文，界面可以提示能力受限，但不要展示供应商内部错误。
- 需要等待的 AI 任务用进度、取消、后台通知或任务列表；避免让用户盯着无限 loading。
- 对 paid/high-risk flow，fallback 到低质量 route 前需要产品上可接受的文案和人工 checkpoint。

## AI workflow 默认规则

- Prompt builder 必须读取 route id 和 route policy，不允许 prompt 自己决定供应商或越权启用工具。
- 结构化输出优先使用 schema；不同模型的 schema adherence 需在 eval gate 中单独记录。
- 工具路由必须与 auth、tenant boundary、admin action guard 和 red-team 工件相连；模型更换不得扩大工具权限。
- 模型迁移优先从“最小 prompt + 代表样例”开始，不把旧 prompt stack 全量搬到新模型族。
- 对后台、低优先级、大批量任务，优先 Batch/Flex/异步队列；对高价值低延迟路径，才考虑 priority 或更强模型。

## 需要人判断的关键点

只把这些判断交给人：

- 是否改变用户可见生产默认模型、供应商或 route。
- 是否引入新的外部模型供应商、区域、数据保留或供应商条款边界。
- 是否让 sensitive/regulatory/high-impact 数据进入某条 route。
- 是否改变 refusal/safety behavior、moderation route 或安全阈值。
- 是否启用 tool-heavy、agentic、computer-use、write-action 或高权限 route。
- 是否对付费、高风险或核心用户路径 fallback 到低质量 route。
- 是否提高预算、取消硬限制、扩大 context window 或默认高 reasoning effort。
- 是否允许没有 fallback 的用户可见 AI 能力上线。
- 是否移除、弃用或迁移当前生产模型快照。

其他字段完整性、章节、JSON 枚举、route 引用、fallback 链、timeout/retry、eval evidence、telemetry、敏感内容扫描和 OpenSpec linkage 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“有哪些 route、怎么选、坏了怎么办、能不能发布、供应商是否还合适”。
- 保留：人只判断默认模型、新供应商、敏感数据、高权限工具、核心路径降级、高成本默认、无 fallback 和模型弃用。
- 调整：不要求 AI gateway、多供应商自动竞价或复杂 bandit；默认一个主 route、一个安全 fallback、一个关闭开关。
- 调整：不要求每次小 prompt 调整都开完整路由评审；只有 route/model/provider/tool/data boundary 变化触发 eval gate。
- 风险：模型更新太快，文档过期。缓解：registry 记录的是内部 route 决策和证据，不把外部价格/能力表硬编码为长期事实。

结论：可落地。一个人可以先为最重要 AI capability 建一个小 registry 和 fallback runbook，再用 eval gate 控制模型升级。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户不会被模型故障或降级吓到；核心体验有明确 fallback 和文案。
- 工程角度：model name、provider、timeout、retry、reasoning effort、fallback 不再散落代码，route change 可 review。
- 运维角度：rate limit、timeout、5xx、schema 失败、安全拒绝和成本阈值都有检测与动作。
- 安全隐私角度：新供应商、敏感数据、数据保留、工具权限和安全行为变化都需要 checkpoint。
- 成本角度：先质量达标，再缩小模型、减少 token、缓存、批处理或异步；避免“默认最强模型解决一切”的账单黑洞。

结论：可落地。本专项把模型选择从“临时调参”变成可评测、可降级、可回滚的产品行为契约。
