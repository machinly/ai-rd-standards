# W5 Verify 核心规范

## W5 核心入口

本文件是 W5 Verify 的核心入口。进入 `docs/W5-verify/` 时先读它，再按触发条件读取测试质量、可访问性/AI UX、性能回归或韧性演练专项。

W5 只回答一个问题：**W4 做出来的实现，在进入发布或生产运行前，是否有足够证据说明它不会明显伤害用户、数据、成本、可靠性、可访问性、安全或信任？**

W5 不是补写需求、重做实现或临时决定发布承诺的地方。发现规格、风险边界、AI 行为或实现本身需要改变时，分别回退到 W2、W3 或 W4。

## 适用范围

适用：

- 用户可见功能、生产代码、公共 API、数据迁移、配置、后台任务、外部集成、计费、通知和开发者接口的发布前验证。
- Go/Kratos/sqlc/gRPC、Vite 前端、AI workflow、prompt/tool/model/RAG、worker、webhook、migration 的测试与证据整理。
- 可访问性、AI UX、界面信任、性能预算、负载画像、性能回归、韧性演练和降级验证。
- 发布前 test/eval run、accepted risk、flaky、manual exploratory、smoke、benchmark 和 fault-injection 记录。

不适用：

- 当前工作是否值得做，回到 `docs/W0-intake/00-main.md`。
- 用户问题、成功指标或产品证据，回到 `docs/W1-discovery/00-main.md`。
- 契约、安全、权限、成本、供应商和信任边界，回到 `docs/W2-openspec-risk/00-main.md`。
- AI 行为定义、eval 样本、模型路由、工具权限和 RAG 来源，回到 `docs/W3-ai-behavior/00-main.md`。
- 实现修复、迁移、配置或代码批次，回到 `docs/W4-build/00-main.md`。
- 发布、回滚、客户上线和公开承诺，进入 W6。

## W5 最小产出

每个 W5 工作至少留下这些产出：

- 本次变更的验证范围：哪些行为、路径、AI 能力、数据边界或用户体验必须被保护。
- 实际运行证据：test、build、lint、sqlc、eval、smoke、Playwright、accessibility、benchmark、load sample 或 fault-injection 中适用项。
- 跳过项和原因：无法运行、暂不适用、缺少环境、成本过高、需要人工验收或需要后续补齐。
- 风险决策：`pass`、`needs-fix`、`needs-more-tests`、`accepted-risk`、`rollback`、`defer-release` 或等价结论。
- 给 W6/W7/W8 的证据链接：release gate、rollback/mitigation、observability/runbook、用户反馈或质量回归入口。

最小产出不是“所有门禁都跑满”。它要求每个真实风险都有证据、解释或明确的人工接受。

## 人工判断点

默认不问：

- 普通测试文件命名、低风险 fixture、局部断言写法、没有失败的 build/test 记录、低风险文案可访问性微调。

必须人工判断：

- 是否允许带失败测试、跳过关键门禁、已知 flaky、缺少 AI eval 或缺少回滚证据进入发布。
- 是否接受 WCAG 2.2 AA、键盘、焦点、AI disclosure、用户反馈或界面信任的例外。
- 是否接受性能回归、未知基线、放宽 p95/p99、Core Web Vitals、bundle、AI token/latency 或容量预算。
- 是否对生产、真实用户数据、真实客户流量、真实供应商或真实付费 AI provider 做负载/故障/韧性验证。
- 是否接受降级路径未验证、blast radius 扩大、自动 failover、自动供应商切换或弱化 timeout/retry/fallback。
- 是否发布会影响资金、权限、隐私、安全、计费、通知、合同 SLA、公共 API 或高影响 AI 场景的已知质量风险。

## 触发型专项

只在触发条件出现时读取对应文件：

- 通用测试策略、test matrix、test run、flaky、Go/Vite/sqlc/gRPC/AI eval 门禁：`docs/W5-verify/01-testing-quality-standard.md`
- 用户界面、可访问性、AI UX、交互状态、键盘、焦点、AI disclosure、界面信任：`docs/W5-verify/02-accessibility-ai-ux-standard.md`
- 核心路径延迟、负载、Web Vitals、bundle、DB query、AI latency/token、性能回归：`docs/W5-verify/03-performance-budget-load-regression-standard.md`
- 依赖故障、429/5xx/timeout、重试风暴、降级 UI、fault injection、dead letter、blast radius：`docs/W5-verify/04-resilience-fault-injection-degradation-standard.md`

常见跨 W 触发：

- AI 输出质量、安全拒绝、eval 样本失败：回到 `docs/W3-ai-behavior/00-main.md`，必要时再进入 W8 AI 质量回归。
- 安全、权限、隐私、供应链或契约门禁失败：回到 `docs/W2-openspec-risk/00-main.md`。
- 实现缺陷、缺少迁移、缺少配置、缺少 worker/integration 证据：回到 `docs/W4-build/00-main.md`。
- 发布窗口、回滚、客户上线、公开声明：W5 结论明确后进入 W6。

## 进入 W6 的出口

满足以下条件后，W5 才能进入 W6：

- 关键用户路径、数据写入、权限、AI 行为、外部副作用和发布门禁已有证据或人工接受风险。
- 失败项、跳过项、flaky、性能退化、可访问性例外和韧性缺口都写清影响、owner、修复或缓解。
- W2/W3/W4 的输入没有被验证结果推翻；若推翻，已回退。
- 需要上线后的观测、告警、runbook、incident 或 quality review 的项已交给 W7/W8。
- 发布风险能被 W6 的 release checklist、rollback path 和客户沟通承接。

出口选择：

- 验证通过且 release risk 可解释：进入 W6。
- 实现需要修复：回到 W4。
- AI 行为或 eval 定义需要改变：回到 W3。
- 契约、权限、安全、成本或数据边界需要改变：回到 W2。
- 质量结果暴露产品方向或用户问题错误：回到 W1/W0。
- 线上质量回归、用户反馈或事故学习：进入 W8。

## W5 完成检查

- 当前 W5 目录只有一个 `00-main.md` 作为核心入口。
- 所有其它 W5 文件都是触发型专项，并在开头说明不是主入口。
- 入口、索引和 source map 都指向 `docs/W5-verify/00-main.md` 与带目录内顺序编号前缀的语义化专项文件名。
- 没有未编号专项文件、`core-*` wrapper 或只用旧“阶段 NN”作主身份的正文。
- `python tools\verify_workflow_index.py .` 通过。
