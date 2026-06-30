# W1 Discovery 核心入口

## W1 定位

本文件是 W1 Discovery 的核心入口，也是进入 `docs/W1-discovery/` 后默认先读的唯一主规范。W1 只回答一个问题：**我们要解决的是真问题，还是只是想做一个功能？**

W1 不负责排研发优先级，也不替代 OpenSpec、AI eval、实现、验证或发布门禁。W0 已经决定这件事值得进入发现；W1 负责把用户、问题、证据、指标、实验和学习决策写清楚，再决定是否进入 W2/W3/W4，或者回到 W0 停车。

## 核心问题

W1 要让一人公司在写代码前完成最小产品判断：

- 谁因为这件事更成功？
- 过去真实行为里出现了什么问题？
- 本轮只押注哪个 outcome？
- 哪个指标能代表真实价值，哪些 guardrail 不能被伤害？
- 证据、实验和停止条件是否足够支撑继续投入？

默认原则：没有明确目标用户、真实问题、唯一主指标、证据来源和停止条件的用户可见能力，不进入超过 1 个工作日的实现。

## 适用范围

适用：

- 新用户可见功能、付费能力、增长实验、AI workflow、关键 UI 流程。
- 会改变激活、留存、转化、成本、信任、安全感或用户关键任务完成率的改动。
- 从用户访谈、支持反馈、设计伙伴、内测、灰度、产品事件、AI 质量信号或事故复盘进入的产品学习。

不适用：

- 已经明确复现和验收的小 bug fix，且不改变用户体验、成本、安全、权限或数据处理。
- 纯内部重构、基础设施修复或文档维护；分别回到 W0、进入 W2/W4/W9。
- 紧急事故止血；先走 W7/W8，事后再回到 W0/W1 做学习决策。

## 最小产出

每个用户可见能力使用同一个 `<capability>` 贯穿：

```text
product/
  bets/<capability>.md
  metrics/<capability>.json
  feedback/<capability>.jsonl
  experiments/<capability>.json
  decisions/<capability>.md
```

最小可接受版本：

- `product/bets`：目标用户、问题、appetite、scope、non-goals、风险、学习目标、OpenSpec 链接和决策日期。
- `product/metrics`：一个主 outcome、GSM 映射、guardrails、事件依赖和人工判断点。
- `product/feedback`：来自过去行为、具体场景或真实阻碍的证据；无证据继续必须显式记风险。
- `product/experiments`：假设、方法、样本、成功阈值、失败阈值、停止规则和回滚/降级条件。
- `product/decisions`：基于证据做 keep、kill、pivot 或 iterate，禁止实验结束后继续凭感觉推进。

## 人工判断点

默认不问人的事项：字段补齐、模板初稿、低风险证据整理、普通事件命名、缺失链接、review cadence。

必须人工判断：

- 目标用户和痛点是否足够具体。
- 本轮唯一主指标是否代表真实价值。
- 是否向真实用户开放实验或 beta。
- 是否接受证据不足但继续投入。
- 是否收集个人行为分析、使用第三方 analytics、做 session replay、延长保留期或跨产品合并数据。
- 实验结果出来后是 keep、kill、pivot 还是 iterate。

## 触发型专项

- 需要采集产品事件、分析漏斗、做 A/B、灰度、instrumented beta、第三方 analytics、隐私 review 或数据质量复盘：读 `docs/W1-discovery/01-product-analytics-experiment-standard.md`。
- 需要更细地组织访谈、产品赌注、反馈证据、实验和学习决策：先在本文件的最小产出里补齐，不再单独打开产品发现专项。
- 支持反馈、投诉、退款或信任请求成为产品证据：读 `docs/W8-learn/01-customer-support-trust-ops-standard.md`。
- 客户试点或设计伙伴反馈影响产品方向：读 `docs/W6-release/02-customer-pilot-onboarding-launch-standard.md`。
- 商业承诺、合同、SLA 或销售邮件影响 scope：回到 W2 的 `docs/W2-openspec-risk/04-cost-data-vendor-trust-boundary-standard.md` 和 W6 的对外声明门禁判断。
- 官网、文档、销售材料或 AI disclosure 出现强承诺：读 `docs/W6-release/03-external-claim-evidence-release-gate-standard.md`。
- 用户可见 AI 行为、prompt、工具、模型、RAG、记忆或安全边界进入设计：进入 W3。

## 出口

- 证据不足：回到 W0，把 work item 标成 `needs-evidence`、`parked` 或缩小 appetite。
- 需要定义行为、边界、风险和退出条件：进入 W2，并链接 W1 的 bet、metrics、feedback 和 experiment。
- 用户可见 AI 行为变化：进入 W3，先补 eval、失败样例、安全边界和 fallback。
- 只需要最小实现来验证假设：进入 W4，但 scope 必须受 experiment 和 appetite 限制。
- 需要证明不会伤害质量、成本、可靠性或信任：进入 W5。
- 实验或反馈已经形成结论：写 `product/decisions/<capability>.md`，再回到 W0 决定继续、停车、杀掉或扩大。

## Review 1：一人公司注意力审查

- 保留：W1 只回答“是否是真问题”，不扩展成完整产品管理系统。
- 保留：默认先用 Markdown、JSON 和 JSONL 承接，不强迫引入数据平台。
- 调整：产品发现和 analytics 都作为 W1 的触发专项，由本入口统一决定何时读取。
- 风险：证据工件可能形式化。缓解：人工只看痛点、主指标、实验开放和最终决策。

结论：可落地。W1 主入口能在进入 OpenSpec 和实现前，把产品学习压缩成一个可停止、可回退的判断。

## Review 2：产品、工程、运维、安全、成本审查

- 产品角度：用户、问题、outcome、证据和 decision 连在一起，避免功能清单替代学习。
- 工程角度：W1 输出为 W2 OpenSpec、W3 AI 行为和 W4 实现提供输入，但不替代工程门禁。
- 运维角度：guardrails 要覆盖延迟、错误、可靠性、支持投诉或回滚信号。
- 安全隐私角度：第三方 analytics、个人行为分析、session replay 和长保留明确触发人审。
- 成本角度：appetite、实验方法和 AI 成本 guardrail 防止早期产品探索变成多周工程投入。

结论：可落地。W1 的完成标志不是“想清楚一个功能”，而是能基于证据决定继续、停止、转向或回到 W0。
