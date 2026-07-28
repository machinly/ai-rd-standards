# 评估：AI 质量、eval 与回归

## 规范要求

<!-- rule-id: EVALUATION-AI-SCOPE-001 -->
AI 质量专项只在出现 AI 质量回归、线上 AI 输出事故、质量信号、回滚 runbook、质量 incident log、quality review 或事故样本回流 eval 时加载，并先经评估核心入口判定。它消费 support review、feedback ledger 与 top contact drivers 的脱敏结论，权威工件则是 quality signal contract、incident log、quality review 和学习决策；该专项不是默认流程。

<!-- rule-id: EVALUATION-AI-SCOPE-002 -->
通用可用性、延迟或容量事故不在 AI 质量评估中重复处理，应回到 SRE-lite、成本容量、可观测性或模型路由的权威规则。

<!-- rule-id: EVALUATION-AI-SCOPE-006 -->
完整在线学习、A/B bandit、自动模型训练平台或企业级 MLOps 只有出现真实规模后才单独开 change；一人公司评估不能以建设平台代替处理当前能力的真实质量问题。

<!-- rule-id: EVALUATION-AI-RUNBOOK-001 -->
先把最高影响 AI capability 的质量事故整理为一人可执行的 runbook；不以“大 MLOps 平台”作为开始评估的前置条件。

<!-- rule-id: EVALUATION-AI-SIGNAL-001 -->
每个生产 AI capability 使用 `ai-quality/signal-contract/<capability>.json`，并包含 `capability`、`owner`、`user_journey`、`quality_dimensions`、`leading_signals`、`lagging_signals`、`thresholds`、`eval_links`、`telemetry_links`、`sampling_policy`、`alert_policy`、`rollback_link`、`human_checkpoint`、`review_cadence` 与 `status`。

<!-- rule-id: EVALUATION-AI-SIGNAL-002 -->
`quality_dimensions` 从用户任务成功、事实/引用正确性、结构化输出成功率、安全/拒答合理性、工具调用成功率中选择适用的 2—3 个；不得用一个模糊“质量分”替代可判断维度。

<!-- rule-id: EVALUATION-AI-SIGNAL-003 -->
`leading_signals` 覆盖能较早暴露问题的 eval failure、schema parse failure、tool failure、fallback rate、guardrail spike、latency/cost spike 与人工抽检失败；`lagging_signals` 覆盖真实用户影响，包括 support complaint、thumbs down、task abandonment、refund/churn、人工修正率和关键业务转化下降。

<!-- rule-id: EVALUATION-AI-SIGNAL-004 -->
每个正式阈值必须绑定一个动作，动作闭集为：继续观察、补 eval、关闭 rollout、切 fallback、回滚 prompt/model/route/retrieval/tool 或升级事故。没有动作的阈值只可作为探索信号，不能写成正式门禁。

<!-- rule-id: EVALUATION-AI-SIGNAL-005 -->
每份 quality signal contract 至少同时包含一个离线 eval 信号和一个线上用户或生产信号；只看 eval 或只看投诉都不足以支持质量结论。

<!-- rule-id: EVALUATION-AI-REVIEW-001 -->
`ai-quality/quality-review/<capability>.md` 以 `<capability> AI Quality Review` 为标题，并包含 `Recent Changes`、`Signal Health`、`Eval / Dataset Drift`、`User Feedback / Support`、`Incidents / Regressions`、`False Positives / Noise`、`Rollback Readiness`、`Open Risks`、`One Next Change` 与 `Review Cadence`。

<!-- rule-id: EVALUATION-AI-REVIEW-002 -->
有活跃用户的核心 AI capability 每两周复盘一次；早期或低风险能力每月复盘一次。

<!-- rule-id: EVALUATION-AI-REVIEW-003 -->
每次 AI quality review 只选一个最高影响改进：新增一个 eval 类别、修一个 top regression、降低一个噪声告警、增加一个 rollback 验证或改一个用户提示。目标是稳定质量定义、检测、止血和学习闭环，而不是追求抽象的“把模型调到最好”。

<!-- rule-id: EVALUATION-AI-STORAGE-001 -->
可选的 `ai_quality_signals`、`ai_quality_incidents`、`ai_quality_actions` 与 `ai_quality_reviews` 表只保存引用和摘要，不保存敏感原文。

<!-- rule-id: EVALUATION-AI-ROLLBACK-001 -->
生产 AI 回滚由 config、feature flag 或 model route 控制；不得在业务代码中临时改 model name 或 prompt 字符串来冒充可审计回滚。

<!-- rule-id: EVALUATION-AI-INCIDENT-001 -->
AI 质量学习既要吸收线上任务失败、事故复盘和用户对输出的投诉，也要吸收 eval、schema、tool、retrieval、fallback 及其他回归信号；实时止血仍归运行，评估只负责把这些事实转成质量结论与下一轮输入。
