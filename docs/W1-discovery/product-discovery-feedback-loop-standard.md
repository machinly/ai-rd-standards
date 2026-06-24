# 产品发现、实验与反馈闭环规范

## W1 触发定位

本文件是 W1 Discovery 的触发型专项规范，不是 W1 主入口。只有当 `docs/W1-discovery/main.md` 已经判断需要更细地组织产品赌注、用户证据、反馈、实验和学习决策时，才读取本文件。

如果当前问题只是“这件事是否值得进入产品发现”或 W1 应该先读哪个文件，先回到 `docs/W1-discovery/main.md`。普通入口问题不要从本文件开始。

## 场景触发规范

- 需要采集产品事件、分析漏斗、做 A/B、灰度或 instrumented beta：进入 `docs/W1-discovery/product-analytics-experiment-standard.md`。
- 支持反馈、投诉、退款、信任请求构成产品证据：参考 `docs/W8-learn/customer-support-trust-ops-standard.md`。
- 客户试点或设计伙伴反馈影响产品方向：参考 `docs/W6-release/customer-pilot-onboarding-launch-standard.md`。
- 商业承诺、合同、SLA 或销售邮件正在影响产品 scope：参考 `docs/W6-release/commercial-contract-obligation-standard.md`。
- 官网、文档、销售材料或 AI disclosure 里出现强承诺：参考 `docs/W6-release/external-claim-evidence-release-gate-standard.md`。
- 用户可见 AI 能力进入设计：下一步进入 `docs/W3-ai-behavior/prompt-eval-agent-workflow-standard.md`。

## 目标

一人公司最危险的浪费不是代码写慢，而是把技术正确地做在错误问题上。本规范把产品发现压缩成一个可执行闭环：先写清用户、问题、赌注、指标、证据和停止条件，再进入研发。

默认原则：没有明确用户、问题、成功指标和学习目标的用户可见能力，不进入超过 1 个工作日的实现。

## 核心依据

- 《人月神话》：不要用排期乐观掩盖认知不确定性；真正困难的部分常在概念完整性和需求判断。
- 小型项目管理：一人公司只保留能减少返工、恢复上下文、支持取舍的最小工件。
- Lean Startup：研发循环应服务于 build-measure-learn，而不是只累积功能。
- Steve Blank Customer Development：建筑物内没有事实，假设要用实验和客户接触验证。
- The Mom Test：客户访谈要从过去真实行为和具体问题中学习，避免诱导性赞美。
- Continuous Discovery / Opportunity Solution Tree：持续以小步触点、机会、方案和假设测试连接产品结果。
- Shape Up：用 appetite 限制时间，用可变 scope 控制风险，避免无尽 backlog。
- Google HEART / GSM：产品指标从目标、信号、度量映射，避免只看虚荣指标。
- Trustworthy Online Controlled Experiments / Microsoft ExP：受控实验可以建立因果证据，但可信数字比拿到数字更难。
- OpenTelemetry / 产品分析事件规范：事件名稳定、低基数、无动态值，才能长期比较。

## 范围

适用对象：

- 新用户可见功能、付费能力、增长实验、AI workflow、重要 UI 流程。
- 会改变激活、留存、转化、成本、信任、安全感或用户关键任务完成率的改动。
- 从原型、内测、灰度到生产发布的产品学习过程。

不适用对象：

- 纯内部重构，且不改变用户体验、成本、安全、权限或数据处理。
- 小于 1 个工作日的 bug fix，前提是已经有明确复现和验收。
- 紧急事故修复。事故后应补充 decision 记录。

## 最小工件

每个用户可见能力用同一个 `<capability>` 文件名贯穿：

```text
product/
  bets/<capability>.md
  metrics/<capability>.json
  feedback/<capability>.jsonl
  experiments/<capability>.json
  decisions/<capability>.md
```

### `product/bets/<capability>.md`

用于决定是否值得下注，必须包含：

- `Target User`：谁会因为这个能力更成功。
- `Problem`：过去真实行为里出现的问题，不写泛泛愿景。
- `Appetite`：愿意投入的时间上限。默认 1 到 2 周；高风险能力最多 6 周。
- `Scope`：这次做什么。
- `Out of Scope`：这次明确不做什么。
- `Risks`：desirability、viability、feasibility、usability、ethics 五类风险中相关项。
- `Learning Goal`：这次要学到什么，和继续/停止相关。
- `OpenSpec Link`：关联 change id。
- `Decision Date`：什么时候必须做 keep / kill / pivot / iterate 判断。

### `product/metrics/<capability>.json`

用于让学习可度量，必须包含：

- `outcome`：一个产品结果，不超过一句话。
- `goal`、`signals`、`metrics`：采用 GSM 映射。
- `guardrails`：不能为了主指标牺牲的体验、成本、安全、隐私或可靠性指标。
- `events`：稳定事件名、触发条件、来源、属性和隐私说明。
- `human_checkpoint`：哪些指标变化需要人判断。

默认只允许一个主指标。多指标并列会让一人公司难以判断。

### `product/feedback/<capability>.jsonl`

用于保存用户证据，每行一条观察：

```json
{"id":"fb-001","date":"2026-06-23","source":"interview","persona":"solo founder","problem":"手工整理研发流程时丢上下文","evidence":"描述了上周重复写 release checklist 的经历","tags":["workflow","toil"]}
```

默认规则：

- 大于 1 周的产品 bet 至少需要 3 条反馈证据，或在 bet 中显式接受“无用户证据”风险。
- 反馈优先记录过去行为、具体场景和阻碍，不记录“你会不会用”式承诺。
- 不记录邮箱、手机号、真实姓名、完整 IP、支付信息、密钥或其他不必要个人数据。

### `product/experiments/<capability>.json`

用于把假设变成可停止的实验，必须包含：

- `hypothesis`：如果做 X，目标用户会因为 Y 产生 Z 行为。
- `method`：interview、prototype、concierge、wizard_of_oz、instrumented_beta、controlled_experiment 等。
- `sample`：样本来源和数量预期。
- `success_threshold`：继续的阈值。
- `guardrails`：失败或伤害阈值。
- `decision_rule`：何时 keep / kill / pivot / iterate。
- `human_checkpoint`：哪些动作必须人审。

流量不足时不默认 A/B 测试。优先用访谈、原型、concierge 或 instrumented beta 获得方向性证据。

### `product/decisions/<capability>.md`

用于防止“实验结束后继续凭感觉写代码”，必须包含：

- `Evidence Summary`
- `Decision`：只能是 keep、kill、pivot、iterate 中一个。
- `Why`
- `Next Step`
- `Review Cadence`

## 研发接入顺序

1. 写 `product/bets` 和 `product/metrics`。
2. 写 OpenSpec proposal/design/tasks，链接 product bet。
3. 补最小 `feedback` 或显式记录无用户证据风险。
4. 定义 `experiments`。
5. 只实现支持本次实验的最小 backend/frontend/AI 变更。
6. 采集反馈和事件。
7. 写 `decisions`，再决定下一轮 OpenSpec。

## 产品事件规范

- 事件名使用 snake_case，例如 `assistant_report_exported`。
- 事件名不得包含用户 ID、资源 ID、时间戳、邮箱、动态 path 或 UUID。
- 关键业务事件优先由后端或可信边界产生，前端事件只用于 UI 交互和体验分析。
- 事件属性只记录分组、状态、数量、耗时、错误类别等低基数字段。
- 涉及个人行为分析、session replay、第三方 analytics 或跨站追踪时，必须进入 security/privacy review。

## AI 产品特殊规则

- AI 能力的成功指标不能只看“回答看起来不错”，必须连接用户任务完成、人工修正率、拒答/误答、安全触发、成本和延迟。
- prompt、工具、模型或 agent workflow 的变化需要连接 eval 结果和产品指标。
- 当用户可见输出会影响钱、权限、医疗、法律、生产数据或外部通知时，实验前必须定义人工审批或 dry-run。
- AI 实验失败后，不默认加大模型或工具复杂度；先检查任务定义、上下文、eval 样本和用户路径。

## 需要人判断的关键点

只把这些问题交给人：

- 目标用户和痛点是否足够具体。
- 本轮唯一主指标是否代表真实价值。
- 是否可以向真实用户开放。
- 是否可以收集个人行为分析或使用第三方 analytics。
- 证据出来后是 keep、kill、pivot 还是 iterate。

其他字段由 Codex 按模板先填，除非触发安全、隐私、成本、权限或发布阶段的 checkpoint。

## 默认取舍

- 默认小赌注：1 到 2 周固定 appetite，可变 scope。
- 默认先学习再扩建：先原型、访谈、concierge 或窄 MVP，再做平台化能力。
- 默认证据优先：反馈、事件和实验结论比路线图意见更高优先级。
- 默认停止机制：到 `Decision Date` 必须写 decision，不允许无限延期。
- 默认低工具负担：不强制购买产品分析平台；JSON/JSONL/Markdown 可先满足一人公司落地。

## Review 1：一人公司注意力审查

- 保留：只要求 5 个工件，并且每个工件只服务一个判断。
- 保留：只把 5 类关键判断交给人，其他由模板和脚本先做。
- 调整：不要求每个小 bug 都写产品 bet，避免流程压过交付。
- 调整：A/B 测试降级为高流量条件下的选项，早期默认不用。
- 风险：`feedback` 可能被形式化填写。缓解：脚本检查最低字段，review 要看是否来自具体行为。

结论：可落地。该流程适合一人公司在进入实现前做 20 到 40 分钟判断，适合较大 bet 做半天产品发现。

## Review 2：研发、运维、安全、成本交叉审查

- 研发角度：OpenSpec 先链接 product bet，能防止需求漂移；但不得让产品工件替代 proto/API/eval/spec。
- 运维角度：guardrails 必须包含延迟、错误、成本或可靠性，否则产品实验可能牺牲生产健康。
- 安全隐私角度：事件属性和第三方 analytics 是主要风险点，已纳入 human checkpoint。
- 成本角度：AI 产品指标必须包含 token、工具调用或单位成本 guardrail，避免好用但不可负担。
- 数据角度：事件命名和属性要稳定，后续 schema 变动走数据迁移规范。

结论：可落地。W1 产品发现应作为 W2 OpenSpec、W3 AI 行为、W4 实现、W5 验证和 W6 发布的入口门，而不是替代工程门禁。
