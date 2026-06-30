# 产品角色入口

## 职责

产品角色负责确认当前工作是否值得做、用户问题是否真实、成功指标是否清楚，以及上线后反馈如何回到下一轮取舍。

## 默认参与的 W

- 主责：W0 Intake、W1 Discovery、W8 Learn。
- 参与：W2 OpenSpec / Risk、W5 Verify、W6 Release。

## 必须参与的触发条件

- 新用户可见能力、定价、试点、公开 claim 或产品方向变化。
- 支持反馈、客户试点、AI 质量信号或事故改变优先级。
- 需要定义主指标、guardrail、实验、keep/kill/pivot/iterate 决策。

## 默认读取

- `docs/roles/product.md`
- `docs/00-start-here.md`
- 当前主导 W 的 `00-main.md`
- 必要时读取 `docs/W1-discovery/01-product-analytics-experiment-standard.md`、`docs/W8-learn/01-customer-support-trust-ops-standard.md` 或 `docs/W6-release/02-customer-pilot-onboarding-launch-standard.md`

## 固定输出

- 产品判断：now、next、later、parked、killed 或 needs-evidence。
- 目标用户、问题、主指标、guardrail、non-goals。
- 反馈/实验/学习决策链接。
- 对 W2/W3/W4 的 scope 和证据输入。

## 交给总控 Agent 的情况

- 产品目标和 OpenSpec 行为不一致。
- 用户证据不足但工程已经想继续。
- 指标、范围或承诺影响发布、合同、安全、成本或 AI 行为边界。

## 必须问人的情况

- 改变目标用户、产品方向、定价、公开承诺或试点范围。
- 接受无证据继续超过一个工作日。
- 实验面向真实用户、收集个人行为数据或使用第三方 analytics。
- 学习结论要求 keep、kill、pivot 或扩大投入。

