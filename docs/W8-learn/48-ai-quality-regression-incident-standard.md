# 阶段 48：AI 质量回归、线上质量事故与回滚规范

## 目标

AI 产品上线后的失败不总是“服务挂了”。更常见的是：回答变差、格式偶发失败、检索引用跑偏、工具调用变多、拒答风格突变、某类用户任务突然不可用、模型供应商小版本变化带来行为漂移。阶段 4 已要求变更前有 eval，阶段 15 要求生产遥测，阶段 30 要求模型路由和 fallback；阶段 48 负责把这些信号连成一条事故闭环：发现质量回归、分级、止血、回滚、补 eval、复盘。

默认原则：**AI 质量不是主观感觉，而是用户任务成功率、eval 结果、生产信号和人工抽检共同定义的产品可靠性。** 一人公司不追求大 MLOps 平台，先把最重要 AI capability 的质量事故处理成可执行 runbook。

## 核心依据

- 《人月神话》：没有“换模型就会好”的银弹；AI 质量回归往往来自接口、数据、prompt、工具和用户期望的耦合。
- 小型项目管理：一人公司只能维护少量高价值质量信号；每次复盘只选一个最高影响改进。
- Hidden Technical Debt in Machine Learning Systems：ML/AI 系统有隐性依赖、纠缠、反馈环和配置债；质量问题会静默积累。
- The ML Test Score：生产 ML 系统需要数据、模型、基础设施和监控测试；模型要像二进制一样可调试、可回滚、可监控。
- Google Rules of ML：训练/服务偏移、数据变化和系统变化需要显式监控；先保证 pipeline 和基线，再优化复杂模型。
- Google SRE SLO / Alerting / Incident Response / Postmortem：告警要基于用户症状、可行动；事故先止血，再保留时间线和无责复盘。
- OpenAI Evaluation Best Practices / Evals / Agent Evals：eval 要贴近真实任务；agent workflow 应从 traces 调试进入 datasets、graders 和 eval runs。
- OpenAI Agents tracing：LLM generation、tool call、handoff、guardrail 和 custom span 能支持开发和生产质量排查。
- OpenTelemetry GenAI Semantic Conventions：AI 调用、工具、token、finish reason、模型和供应商信号应标准化，便于跨工具排查。
- NIST AI RMF / Generative AI Profile：AI 风险管理需要覆盖设计、评估、使用、监控和持续管理。

## 范围

适用对象：

- 用户可见 AI capability：chat、assistant、agent、RAG、分类、抽取、总结、生成、代码辅助、自动客服、推荐、审核、工具型 workflow。
- prompt、model、route、schema、retrieval、reranker、tool、guardrail、memory、dataset、eval、feature flag 或供应商变化后的质量回归。
- 用户反馈、support ticket、产品指标、人工抽样、eval run、trace、schema parse failure、tool failure、fallback rate 触发的质量事故。

不适用对象：

- 安全/隐私/漏洞事故的通知、证据保全和法律边界；这些走阶段 44。
- prompt/eval fixture 的基础创建；这些走阶段 4 和阶段 26。
- 通用可用性、延迟、容量事故；这些走阶段 5、9、15 和 30。
- 完整在线学习、A/B bandit、自动模型训练平台或企业级 MLOps；这些需要真实规模后单独开 change。

## 最小工件

每个生产 AI capability 使用同一个 `<capability>` 文件名：

```text
ai-quality/
  signal-contract/<capability>.json
  regression-triage/<capability>.md
  rollback-runbook/<capability>.md
  incident-log/<capability>.json
  quality-review/<capability>.md
```

### `ai-quality/signal-contract/<capability>.json`

质量信号契约必须包含：

- `capability`
- `owner`
- `user_journey`
- `quality_dimensions`
- `leading_signals`
- `lagging_signals`
- `thresholds`
- `eval_links`
- `telemetry_links`
- `sampling_policy`
- `alert_policy`
- `rollback_link`
- `human_checkpoint`
- `review_cadence`
- `status`

默认规则：

- `quality_dimensions` 至少写用户任务成功、事实/引用正确性、结构化输出成功率、安全/拒答合理性、工具调用成功率中适用的 2-3 个。
- `leading_signals` 关注能早发现的信号：eval failure、schema parse failure、tool failure、fallback rate、guardrail spike、latency/cost spike、人工抽检失败。
- `lagging_signals` 关注真实用户影响：support complaint、thumbs down、task abandonment、refund/churn、人工修正率、关键业务转化下降。
- 每个正式阈值必须对应动作：继续观察、补 eval、关闭 rollout、切 fallback、回滚 prompt/model/route/retrieval/tool、升级事故。
- 至少一个离线 eval 信号和一个线上用户/生产信号；只看 eval 或只看投诉都不够。

### `ai-quality/regression-triage/<capability>.md`

回归分诊必须包含：

```markdown
# <capability> AI Quality Regression Triage

## Scope

## Severity Levels

## Detection Signals

## First 15 Minutes

## Reproduction

## Scope Check

## Likely Causes

## Decision Matrix

## Evidence To Capture

## Escalation

## Linked Artifacts

## Review Cadence
```

默认严重度：

- `Q-SEV1`：核心任务大面积失败，用户可能受到资金、权限、法律、医疗、隐私、安全或高影响决策伤害；立即止血，人工判断。
- `Q-SEV2`：核心路径明显变差、特定用户群持续失败、回滚或降级当天完成。
- `Q-SEV3`：小范围或可绕过质量问题，进入普通修复，但要补 regression case。

默认分诊顺序：

1. 确认用户影响：谁受影响、从什么时候开始、是否仍在发生。
2. 找最近变化：prompt、model、route、retrieval index、tool、schema、feature flag、数据源、供应商状态。
3. 用 1-3 个真实或脱敏样例复现；不能复现时先保留 trace/eval/user feedback 证据。
4. 先止血：关闭 rollout、切 fallback、降低工具权限、回滚 prompt/model/route、转人工。
5. 再补 eval：把事故样例加入阶段 4/26 的 eval 或 dataset，避免同类问题回归。

### `ai-quality/rollback-runbook/<capability>.md`

回滚 runbook 必须包含：

```markdown
# <capability> AI Quality Rollback Runbook

## Scope

## Disable Switches

## Rollback Paths

## Model / Prompt / Route Rollback

## Retrieval / Tool Rollback

## User Messaging

## Validation

## Data / Safety Checks

## Recovery Criteria

## Post-Rollback Follow Up

## Linked Artifacts

## Review Cadence
```

默认规则：

- AI 能力必须至少有一个止血路径：关闭能力、切基础模式、切旧 prompt/model/route、禁用高风险工具、改为人工处理或异步队列。
- 回滚不只看服务健康；必须验证质量信号恢复：eval pass、schema success、tool success、fallback rate、用户投诉或人工抽样。
- 不能把用户暴露给更低质量的 fallback 而不说明产品影响；核心/付费/高风险路径需要人工 checkpoint。
- 如果回滚不能撤销已经产生的输出、通知、数据写入或外部动作，必须链接 admin/action、audit、support 或 incident 工件。

### `ai-quality/incident-log/<capability>.json`

质量事故日志必须包含：

- `capability`
- `owner`
- `incidents`
- `linked_artifacts`
- `human_checkpoint`
- `review_cadence`
- `status`

`incidents` 可为空；有事故时每项至少包含：

- `id`
- `date`
- `severity`
- `trigger`
- `user_impact`
- `affected_versions`
- `affected_routes`
- `detection`
- `response`
- `rollback_or_mitigation`
- `eval_followup`
- `owner`
- `status`

默认规则：

- 事故日志只记录引用和脱敏摘要，不存原始 prompt/response、客户数据、secret、完整日志或受监管内容。
- Q-SEV1/Q-SEV2 必须记录时间线、止血动作、回滚/降级结果、后续 eval case 和 owner。
- 如果事故实际是安全、隐私、漏洞、资金或权限事故，必须升级到阶段 44/24/35，而不是只留在质量日志。

### `ai-quality/quality-review/<capability>.md`

质量复盘必须包含：

```markdown
# <capability> AI Quality Review

## Recent Changes

## Signal Health

## Eval / Dataset Drift

## User Feedback / Support

## Incidents / Regressions

## False Positives / Noise

## Rollback Readiness

## Open Risks

## One Next Change

## Review Cadence
```

默认规则：

- 有活跃用户的核心 AI capability 每两周复盘一次；早期或低风险能力每月一次。
- 每次只选一个最高影响改进：补一个 eval 类别、修一个 top regression、降一个噪声告警、加一个 rollback 验证或改一个用户提示。
- 复盘不追求“模型调到最好”；目标是让质量定义、检测、止血和学习闭环更稳。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端使用显式 `AIQualityService` 或等价 usecase 记录 quality signal、incident、rollback decision 和 eval follow-up。
- gRPC status/error model 区分：质量降级、schema/parse 失败、tool failure、retrieval miss、safety block、fallback active、temporarily degraded。
- Kratos middleware/handler 记录 capability、workflow version、prompt version、route id、eval version、trace id、fallback reason、quality severity，不记录原始内容。
- sqlc 可选表：`ai_quality_signals`、`ai_quality_incidents`、`ai_quality_actions`、`ai_quality_reviews`；表里存引用和摘要，不存敏感原文。
- 生产回滚由 config/feature flag/model route 控制，不在业务代码里临时改 model name 或 prompt 字符串。

## Vite 前端默认规则

- AI 降级时 UI 只给用户可行动状态：结果可能受限、已切基础模式、可重试、已转人工或稍后通知。
- 不暴露供应商内部错误、模型名细节、prompt、trace 原文或安全绕过信息。
- 用户反馈入口需要可关联 capability、版本、route、trace/request id；不要要求用户提交 secret、完整日志或个人数据。
- 质量事故中的用户提示必须和阶段 38 notification、阶段 23 support、阶段 46 external claim gate 对齐。

## AI workflow 默认规则

- 每次 prompt/model/route/retrieval/tool/schema 变化前后，至少比较基线样例、事故样例和当前线上高频任务样例。
- RAG 质量回归要同时检查：索引版本、chunking、embedding/reranker、source freshness、tenant filter、citation accuracy。
- 工具型 agent 质量回归要同时检查：工具选择、参数、权限拒绝、重试、部分失败、人工审批和审计日志。
- 如果质量异常来自安全/abuse/content policy，先走安全/内容规范，不为了“提高通过率”降低 guardrail。

## 需要人判断的关键点

默认不问：

- signal 字段命名、普通 Q-SEV3 triage、低风险 eval case 添加、复盘文案、非核心能力的小阈值调整。

必须问：

- 是否将质量问题定为 Q-SEV1/Q-SEV2，是否触发用户通知、公开说明、退款/补偿或合同 SLA 风险。
- 是否继续 rollout、回滚、关闭核心 AI 能力、切低质量 fallback、转人工或暂停发布。
- 是否采样或查看原始 prompt/response、客户数据、支持工单、个人数据或受监管内容。
- 是否接受 eval 失败、人工抽检失败、用户投诉持续存在仍然发布。
- 是否降低 safety/refusal/guardrail 阈值以提升通过率。
- 是否把事故样例加入长期 eval/dataset，尤其包含客户内容、敏感数据或授权不清材料。

其他字段完整性、章节、阈值、信号类型、敏感内容扫描、OpenSpec linkage、positive/negative fixture 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答发现、分诊、止血、留证和复盘；一个人可以在一次事故后补齐。
- 保留：人只判断严重度、用户通知、回滚/继续、原始内容采样、安全阈值和接受风险。
- 调整：不要求在线训练、复杂 drift 平台或全天候 on-call；先用 eval、trace、support、用户反馈和少量指标。
- 调整：incident log 可以没有事故；先把结构建好，等第一次真实质量回归时能写。
- 风险：质量信号容易变成噪声。缓解：quality review 必须检查 false positives，并且每次只选一个下一步。

结论：可落地。阶段 48 把“AI 变差了”从感觉变成一条可执行事故路径，同时保护一人公司的注意力。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：质量回归按用户任务影响分级，不只看模型输出好不好看。
- 工程角度：prompt/model/route/retrieval/tool/schema 都有 rollback path 和版本引用。
- 运维角度：SRE 的用户症状、止血、时间线和复盘被移植到 AI 行为质量上。
- 安全隐私角度：原始 prompt/response 和客户数据默认不进入工件；安全类问题升级到安全事故。
- 成本角度：不因质量焦虑默认切最强模型；先定位回归、回滚，再评估一个最高影响改进。

结论：可落地。它补上了阶段 4、15、30 之间的运行闭环：上线前有 eval，上线中有信号，出问题时有止血和学习。
