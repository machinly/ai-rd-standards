# W6 Release 核心规范

## W6 核心入口

本文件是 W6 Release 的核心入口。进入 `docs/W6-release/` 时先读它，再按触发条件读取发布流水线、客户上线、对外声明证据或商业承诺专项。

W6 只回答一个问题：**W5 的验证证据已经足够后，这次变更能不能发布、如何发布、对谁上线、对外能承诺什么、失败时如何回滚或更正？**

W6 不是补测试、补实现或临时改产品边界的地方。发现验证证据不足回 W5；发现实现缺口回 W4；发现风险边界、合同义务或公开声明不成立回 W2；发现 AI 行为证据不足回 W3。

## 适用范围

适用：

- 生产部署、preview/staging/production promote、CI gates、artifact、smoke、rollback、release log 和 post-deploy watch。
- 客户试点、design partner、private beta、paid pilot、production go-live、租户 provision、launch readiness 和 customer handoff。
- 官网、pricing、docs、developer portal、release notes、AI disclosure、trust/security/privacy、support macro、sales email 等对外 claim。
- 客户合同、订单、SLA、DPA、安全附件、商业承诺、服务积分、非标准条款和红线判断。

不适用：

- 工作优先级和是否值得做，回到 `docs/W0-intake/00-main.md`。
- 用户问题、试点成功指标或学习假设，回到 `docs/W1-discovery/00-main.md`。
- 契约、安全、供应商、数据、成本、信任政策和客户数据生命周期，回到 `docs/W2-openspec-risk/00-main.md`。
- AI 行为、eval、红队、模型路由、工具权限和 RAG 证据，回到 `docs/W3-ai-behavior/00-main.md`。
- 代码、配置、迁移、计费、通知、worker 或集成实现，回到 `docs/W4-build/00-main.md`。
- 上线前验证、性能、可访问性或韧性证据，回到 `docs/W5-verify/00-main.md`。

## W6 最小产出

每个 W6 工作至少留下这些产出：

- 发布决策：发布、不发布、延后、回滚、灰度、仅 preview、仅客户试点或仅内部上线。
- Release evidence：release id、commit/artifact、gates、smoke、rollback、post-deploy watch、残余风险。
- 如果涉及客户上线：pilot charter、tenant provisioning、launch readiness、success plan 或 handoff review 中适用项。
- 如果涉及对外声明：claim inventory、evidence map、release gate、correction runbook 或 claim review 中适用项。
- 如果涉及合同或商业承诺：obligation register、agreement map、SLA/service credit、redline playbook 或 contract review 中适用项。
- 下一步去向：进入 W7 运行观察、W8 学习反馈、回 W5 补证据、回 W4 修实现，或回 W2/W3 修边界。

## 人工判断点

默认不问：

- release 文件命名、低风险 release note、preview/staging 自动部署、没有强承诺的 typo、标准合同字段顺序。

必须人工判断：

- 是否发布到 production，是否自动 production deploy，是否自动回滚或自动关闭功能。
- 是否允许 CI 自动执行 migration、生产数据操作、真实付款、真实通知、真实 webhook 或真实客户上线。
- 是否发布或保留高风险对外声明：AI 能力、准确性、不训练、数据驻留、删除、SLA、安全、隐私、合规、费用、退款、API 稳定性。
- 是否接受非标准合同条款、SLA、服务积分、24/7、P1 响应、数据/AI/安全强承诺、uncapped liability 或供应商能力之外的义务。
- 是否把 design partner/private beta 转 paid pilot 或 production。
- 是否带着 W5 的失败门禁、accepted risk、未验证 rollback、未验证 support path 或客户未验收继续发布。
- 是否需要律师、隐私/安全顾问、客户通知、开发者通知、公开更正或合同变更。

## 触发型专项

只在触发条件出现时读取对应文件：

- CI/CD、release artifact、smoke、rollback、production deploy、post-deploy watch、provenance/SBOM：`docs/W6-release/01-release-pipeline-standard.md`
- 客户试点、租户导入、客户上线、launch readiness、success plan、handoff/offboarding：`docs/W6-release/02-customer-pilot-onboarding-launch-standard.md`
- 官网、docs、pricing、AI disclosure、trust/security/privacy、developer docs、support/sales claim：`docs/W6-release/03-external-claim-evidence-release-gate-standard.md`
- 客户合同、订单、SLA、服务积分、红线、DPA、安全附件、商业承诺：默认由本文件的人审点、W2 `docs/W2-openspec-risk/04-cost-data-vendor-trust-boundary-standard.md` 和 W6 对外声明证据门禁承接；非标准条款或正式合同需要单独 OpenSpec change。

常见跨 W 触发：

- Billing launch、entitlement、Webhook 或通知执行：回到 `docs/W4-build/06-external-side-effects-standard.md` 补实现证据。
- Audit evidence package：进入 `docs/W9-maintain/00-main.md`，由 W9 主入口判断是否需要证据索引或单独 change。
- Trust/data/vendor claim 证据不足：回到 `docs/W2-openspec-risk/00-main.md`。
- 发布后观测、告警、事故或凭据轮换：进入 W7。

## 进入 W7 的出口

满足以下条件后，W6 才能进入 W7：

- Release decision、release id、artifact、环境、smoke、rollback 和 watch plan 已明确。
- W5 失败项、accepted risk 和跳过项已经被发布决策承接。
- 客户上线有 readiness、support path、rollback/offboarding 和客户验收或明确不可转生产说明。
- 对外 claim 有证据、范围、owner、更新时间和更正路径；不支持的强声明未发布。
- 商业承诺有义务登记、证据链接、SLA/服务积分处理方式和人工接受记录。
- post-deploy 需要看的 SLO、dashboard、alert、support channel、billing/entitlement、AI quality 或 claim correction 已交给 W7/W8/W9。

出口选择：

- 发布完成或客户上线完成：进入 W7 运行、观测与事故准备。
- 发布结果产生用户/客户/支持/质量反馈：进入 W8。
- 门禁失败或证据不足：回到 W5。
- 需要实现修复：回到 W4。
- 需要调整边界、承诺、合同、供应商或信任声明：回到 W2。
- 需要调整 AI 行为、eval 或模型路径：回到 W3。

## W6 完成检查

- 当前 W6 目录只有一个 `00-main.md` 作为核心入口。
- 所有其它 W6 文件都是触发型专项，并在开头说明不是主入口。
- 入口、索引和 source map 都指向 `docs/W6-release/00-main.md` 与带目录内顺序编号前缀的语义化专项文件名。
- 没有未编号专项文件、`core-*` wrapper 或只用旧“阶段 NN”作主身份的正文。
- `python tools\verify_workflow_index.py .` 通过。
