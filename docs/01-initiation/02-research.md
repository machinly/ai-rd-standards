# 调研

## 项目目的与边界

调研负责在投入产品定义或实现前理解真实问题、证据和不确定性，并在实验或反馈形成结论后把学习交还给选题。它覆盖产品发现、产品分析和受控实验，但不替代优先级判断、纯运维遥测、事实账本、事故止血、产品定义或后续工程门禁。

## 根本原则

- **ITEM-RESEARCH-001**：实验结果出来后，必须由人选择继续、停止、转向或迭代，不能继续凭感觉推进。

## 核心判断

<!-- rule-id: RESEARCH-PREIMPLEMENTATION-GATE -->
- 用户可见能力进入超过 1 个工作日的实现前，必须完成最小产品判断并给出证据来源。

<!-- rule-id: RESEARCH-REAL-WORLD-EVIDENCE -->
- 问题证据应来自过去真实行为、具体使用场景或可观察阻碍；用户访谈、支持反馈、设计伙伴、内测/灰度、产品事件、AI 质量信号与事故复盘都可作为来源，但没有证据时必须标出风险。

<!-- rule-id: RESEARCH-FOCUSED-OUTCOME -->
- 一轮调研只明确一个主要 outcome。

<!-- rule-id: RESEARCH-VALUE-METRIC-AUTHORITY -->
- 一轮只有一个主指标；该指标是否代表真实用户价值以及是否变更，必须由人判断。

<!-- rule-id: RESEARCH-DISCOVERY-APPLICABILITY -->
- 新的用户可见功能、付费能力、增长实验、AI workflow、关键 UI 流程，以及可能改变激活、留存、转化、成本、信任、安全感或关键任务完成率的改动，均应先评估是否需要调研。

<!-- rule-id: RESEARCH-EVIDENCE-BASED-DECISION -->
- 实验或反馈结束后，以证据形成 keep、kill、pivot 或 iterate 的学习结论并由人确认；不得在结论可用后继续凭直觉推进，结论还需形成可追溯的 product decision。

## 重新组织后的规范要求

### 事故、隐私与真实用户边界

<!-- rule-id: RESEARCH-INCIDENT-SEQUENCING -->
- 紧急事故止血先进入运行/评估；止血后再回到调研和选题形成学习决定。

<!-- rule-id: RESEARCH-REAL-USER-EXPERIMENT-APPROVAL -->
- 是否向真实用户开放实验或 beta，以及 assignment unit 是否会污染结果，必须由人判断。

<!-- rule-id: RESEARCH-PRIVACY-ANALYTICS-APPROVAL -->
- 是否采用第三方分析、session replay、tag manager、广告归因、跨站追踪、稳定用户标识、个人行为分析、延长保留期或跨产品合并数据，必须由人判断。

<!-- rule-id: RESEARCH-HIGH-IMPACT-DASHBOARD-USE -->
- 当分析结果将用于发布、定价、扩大 AI 自主性、营销触达或关闭能力时，dashboard 只能提供证据，最终高影响决定必须由人作出。

### 分析与实验适用范围

<!-- rule-id: RESEARCH-ANALYTICS-APPLICABILITY -->
- 产品分析适用于 Vite 前端的页面、按钮、表单、onboarding、checkout、AI 任务与结果、导出和通知偏好等用户行为，也适用于 Go/Kratos/gRPC 后端的业务 outcome、计费权益、AI workflow 结果和 exposure 事件。范围还包括 feature flag、灰度、A/B、instrumented beta，以及 pricing、onboarding、copy experiments；数据采集既可落在自建事件表，也可借助第三方 analytics、product analytics vendor、warehouse、tag manager 或 session replay。

<!-- rule-id: RESEARCH-ANALYTICS-EXCLUSIONS -->
- 纯 SRE 的 metrics/logs/traces 转到运行观测；产品方向、访谈与 bet 判断使用基础调研；账务/权益、审计日志和支持工单等事实记录由各自权威项目管理；只在本机且不外传的临时调试日志不进入产品分析治理。

<!-- rule-id: RESEARCH-LOW-TRAFFIC-METHOD -->
- 当可用样本不足以支撑有效分流时，不把 A/B 当作默认取证方式；改用 instrumented beta、prototype、concierge 或小范围灰度获取证据。

<!-- rule-id: RESEARCH-ASSIGNMENT-ISOLATION -->
- 先为受控实验选择稳定的分配层级并把 assignment unit 写入记录，可取 user、tenant、workspace 或 session。B2B 与团队协作场景优先按 tenant/workspace 隔离，以免同一组织的成员落入相互干扰的分组。

<!-- rule-id: RESEARCH-EARLY-STOP-CHECKPOINT -->
- 不得因为早期正向数字任意提前结束实验；提前停止必须经过人工 checkpoint。

<!-- rule-id: RESEARCH-EXTERNAL-INCIDENT-COLLABORATION -->
- 安全/隐私事故、漏洞披露与应急响应规范适用于涉及外部安全研究人员、客户安全团队、供应商、平台、监管方、客户支持或公开 advisory 的协作。

## 按主题整理的执行细则

### 连续标识与最小治理

<!-- rule-id: RESEARCH-CAPABILITY-IDENTITY -->
- 同一用户可见能力的 bet、metrics、feedback、experiment 与 decision 使用一致的 `<capability>` 标识。

<!-- rule-id: RESEARCH-ANALYTICS-TARGET-IDENTITY -->
- 同一 production target 的全部分析工件使用相同的 `<target>` 命名，包括 tracking plan、metrics map、experiment、privacy review 和 data-quality review。

<!-- rule-id: RESEARCH-TRACKING-IDENTITY-POLICY -->
- tracking plan 必须记录匿名用户、登录用户、tenant、session 与 experiment assignment 的身份处理策略。

<!-- rule-id: RESEARCH-PROPORTIONAL-ARTIFACTS -->
- 需要更细地组织访谈、产品赌注、反馈证据、实验或学习决定时，先在本项目的最小产出中补齐，不再单独打开产品发现专项。

<!-- rule-id: RESEARCH-LOW-RISK-AUTOMATION -->
- 字段补齐、模板初稿、低风险证据整理、普通事件命名、缺失链接和 review cadence 等事项默认不需要人工判断。

### 指标与实验记录

<!-- rule-id: RESEARCH-METRICS-RECORD -->
- `product/metrics` 或等价指标记录应包含唯一主 outcome、GSM 映射、guardrails、依赖的事件，以及必须由人判断的节点。

<!-- rule-id: RESEARCH-PRODUCT-EXPERIMENT-SUMMARY -->
- 最小 product experiment 记录应写明假设、所选方法与样本、成功和失败阈值、停止规则，以及触发回滚或降级的条件。

<!-- rule-id: RESEARCH-EXPERIMENT-RECORD -->
- 需要可重复分流和可信度审查时，experiment 工件至少记录：`target`、`owner`、`experiment_id`、关联的 product bet、假设、方法（从 instrumented beta、feature-flag rollout、controlled experiment、A/B、holdout 中选择适用项）、assignment unit、targeting-key policy、variants、exposure event、primary metric、guardrails、sample plan、stop rule、trustworthiness checks、rollback policy、human checkpoint、start date、review date 与 status。

### 分析界面

<!-- rule-id: RESEARCH-ANALYTICS-INTERFACE-QUALITY -->
- 采用 Vercel Geist 风格的分析设置、同意/退出、实验状态与错误提示界面应克制、便于扫描并支持深色模式。

## 输入与产物

输入包括候选问题、过去行为、访谈或支持材料、产品/运行事件、事故事实、已有指标、风险和可用流量。

<!-- rule-id: RESEARCH-DECISION-HANDOFF -->
- 一轮调研完成时应有明确决定、理由、人类负责人和复查日期。

产物按实际需要包括 problem evidence、bet、metrics、feedback、tracking plan、experiment 和 product decision；不要求为低风险问题创建全套工件。

## 完成、停止或退出条件

调研在问题证据、单一 outcome、主指标、关键 guardrails、剩余不确定性和下一步决定均可追溯时完成。证据无法支持继续时，返回选题补证据、缩小投入或停车；涉及真实用户、隐私数据或高影响 dashboard 使用而未获批准时停止。

<!-- rule-id: RESEARCH-DEFINITION-HANDOFF -->
- 当需要确定行为、范围、风险或退出条件时进入定义，并链接本轮 bet、metrics、feedback 和 experiment。

## 相关项目引用

<!-- rule-id: RESEARCH-INTERNAL-WORK-EXCLUSION -->
- 纯内部重构、基础设施修复或文档维护不适用产品调研，分别转入选题、技术设计/实现或评估处理。

- 选题决定是否投入以及优先级；调研只提供证据、实验与不确定性。
- 定义和体验设计消费调研结论；验证负责证明已实现结果，不替代实验设计或产品学习。
- 运行提供 SRE 遥测与事故事实，评估汇总发布后信号并在需要时再次触发调研。
