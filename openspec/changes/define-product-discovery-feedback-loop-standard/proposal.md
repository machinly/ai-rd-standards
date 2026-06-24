# 提案：定义产品发现、实验与反馈闭环规范

## 意图

为一人公司建立可检查的产品学习闭环，让用户可见能力在进入研发前明确目标用户、真实问题、下注范围、成功指标、反馈证据、实验停止条件和 keep/kill/pivot/iterate 决策，降低“工程正确但产品错误”的返工风险。

## 范围

- 定义 `product/bets`、`product/metrics`、`product/feedback`、`product/experiments`、`product/decisions` 五类最小工件。
- 定义产品 bet、GSM/HEART 指标、事件命名、反馈记录、实验设计、学习决策的字段和门禁。
- 定义 AI 产品能力如何把 eval、成本、延迟、安全和用户任务完成连接到产品指标。
- 定义低流量场景下访谈、原型、concierge、instrumented beta 的默认路径。
- 定义触发人审的产品关键判断。
- 创建产品发现落地 skill 和检查脚本。

## 不做

- 不引入完整产品管理平台或客户数据平台。
- 不要求所有 bug fix、内部重构和事故修复都写 product artifacts。
- 不把 A/B 测试作为早期产品默认动作。
- 不替代 W2-W7 的工程、安全、成本、发布和运维门禁。

## 依据

- 《人月神话》：进度和工程能力不能替代对正确问题的判断。
- 小型项目管理：用轻量工件保留关键上下文和取舍。
- Lean Startup build-measure-learn、Steve Blank Customer Development、The Mom Test。
- Continuous Discovery / Opportunity Solution Tree。
- Shape Up appetite、fixed time variable scope、bets not backlogs。
- Google HEART / GSM、Trustworthy Online Controlled Experiments、Microsoft ExP。
- OpenTelemetry event semantic conventions、产品分析事件命名最佳实践。

## 需要人的判断

建议默认：任何超过 1 个工作日的用户可见能力必须先有 product bet、metrics 和 experiment；大于 1 周的 bet 必须有至少 3 条反馈证据或显式接受无用户证据风险。
