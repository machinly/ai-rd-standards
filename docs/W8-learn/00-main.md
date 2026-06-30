# W8 Learn 核心规范

## W8 核心入口

本文件是 W8 Learn 的核心入口。进入 `docs/W8-learn/` 时先读它，再按触发条件读取客户支持/信任运营或 AI 质量回归专项。

W8 只回答一个问题：**发布和运行后的用户反馈、支持请求、质量信号、事故和 AI 行为回归，应该如何转成下一轮产品、工程或运营决策？**

W8 不是无限维护 support backlog，也不是把每条反馈都变成需求。W8 的目标是从真实信号里选出下一步：继续、扩大、回滚、修复、停车、杀掉、回到 W1 重新定义问题，或进入 W9 沉淀维护。

## 适用范围

适用：

- 支持消息、用户投诉、退款/credit 请求、事故反馈、计费/权益困惑、隐私/安全请求和流失信号。
- AI 输出投诉、质量回归、eval 失败、schema/tool/retrieval/fallback 异常、线上用户任务失败和 AI 事故复盘。
- support review、feedback ledger、top contact drivers、quality signal contract、incident log、quality review 和学习决策。
- 发布后发现“做错问题”“质量变差”“用户误解承诺”“支持量重复出现”的回流判断。

不适用：

- 新工作是否进入 now/expedite，回到 `docs/W0-intake/00-main.md`。
- 用户问题、目标用户、成功指标和产品赌注重新定义，回到 `docs/W1-discovery/00-main.md`。
- OpenSpec、风险边界、合同、安全、成本或信任承诺变化，回到 `docs/W2-openspec-risk/00-main.md`。
- AI 行为、prompt/eval、模型路由、RAG、工具权限或记忆策略重新设计，回到 `docs/W3-ai-behavior/00-main.md`。
- 实现修复、配置、迁移、worker、计费、通知或开发者文档改动，回到 `docs/W4-build/00-main.md`。
- 发布、客户上线、对外声明或合同承诺，回到 `docs/W6-release/00-main.md`。

## W8 最小产出

每个 W8 工作至少留下这些产出：

- 信号来源：support、产品指标、AI telemetry、eval、事故、客户上线、社群、GitHub issue 或人工抽样。
- 脱敏事实：影响谁、影响什么任务、频率、严重度、证据引用、关联 release/prompt/model/route/request id。
- 决策：继续观察、补文档、修 UX、补 eval、修实现、回滚、降级、补偿、进入 W0/W1/W2/W3/W4/W6/W7/W9。
- 一个最高影响下一步；不把 W8 输出变成无限 backlog。
- 如果涉及用户信任、AI 伤害、安全/隐私、退款、公开说明或合同风险，记录人工判断。

## 人工判断点

默认不问：

- 普通反馈分类、低风险模板文案、Q-SEV3 eval case、无敏感内容的脱敏样本、低风险文档修正。

必须人工判断：

- 是否公开事故通知、状态页更新、道歉、补偿、退款、credit、合同或权益调整。
- 是否认定 AI 输出造成或可能造成实际伤害、误导、歧视、越权、资金/权限/法律/医疗/安全影响。
- 是否查看或采样原始 prompt/response、客户数据、个人数据、支持工单或受监管内容。
- 是否继续 rollout、回滚、关闭核心 AI 能力、切 fallback、转人工或接受 eval/用户投诉持续存在。
- 是否把支持反馈提升为产品路线、OpenSpec change、公开 bug、安全公告、合同承诺或对外声明修正。
- 是否把客户内容用于长期 eval、demo、训练、文档或公开材料。

## 触发型专项

只在触发条件出现时读取对应文件：

- 支持队列、用户反馈、回复模板、反馈账本、事故沟通、退款/权益/隐私安全请求、top contact drivers：`docs/W8-learn/01-customer-support-trust-ops-standard.md`
- AI 质量回归、线上 AI 质量事故、质量信号、回滚 runbook、质量 incident log、quality review：`docs/W8-learn/02-ai-quality-regression-incident-standard.md`

常见跨 W 触发：

- 信号改变“问题是否值得做”：回到 W0。
- 信号改变目标用户、成功指标、问题定义：回到 W1。
- 信号暴露安全/隐私/合同/成本/信任边界：回到 W2。
- 信号暴露 AI 行为定义或 eval 缺口：回到 W3。
- 信号需要代码、配置、数据或通知修复：回到 W4。
- 信号暴露验证缺口：回到 W5。
- 信号要求发布、回滚、声明更正或客户沟通：回到 W6。
- 信号来自线上事故、凭据或恢复缺口：回到 W7。
- 学到的知识需要长期保存、归档、审计证据或上下文恢复：进入 W9。

## W8 出口

W8 完成时必须选择一个出口：

- `continue`：信号健康，继续观察。
- `improve`：进入 W0/W1/W2/W3/W4/W5/W6/W7 的下一项改进。
- `rollback`：回到 W6/W7 执行回滚或降级。
- `stop`：回到 W0 停车或杀掉方向。
- `maintain`：进入 W9 沉淀文档、证据、依赖或上下文。

## W8 完成检查

- 当前 W8 目录只有一个 `00-main.md` 作为核心入口。
- 所有其它 W8 文件都是触发型专项，并在开头说明不是主入口。
- 入口、索引和 source map 都指向 `docs/W8-learn/00-main.md` 与带目录内顺序编号前缀的语义化专项文件名。
- 没有未编号专项文件、`core-*` wrapper 或只用旧“阶段 NN”作主身份的正文。
- `python tools\verify_workflow_index.py .` 通过。
