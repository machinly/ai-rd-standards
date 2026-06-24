# AI 研发工作流规范索引

## 使用规则

这份索引按 AI 研发工作流组织。阶段编号只是历史编号，不是阅读顺序。

默认流程：

1. 先在 `docs/00-start-here.md` 定位 W0-W9。
2. 读取当前 step 的主规范。
3. 只在触发条件出现时读取专项规范。
4. 新增规范必须声明它服务哪个 workflow step。

总入口 skill：`one-person-openspec-rd`。任何研发请求都可以先用它判断 W0-W9，再由对应 step 的专项 skill 接手。

验证命令：

```powershell
python tools\verify_workflow_index.py .
```

## Workflow-To-Standard Map

| Step | 研发问题 | 主规范 | 常用 skill | 主要产出 |
| --- | --- | --- | --- | --- |
| W0 Intake | 现在该不该做？ | `docs/W0-intake/main.md` | `roadmap-prioritization-guard` | work-intake、decision-board |
| W1 Discovery | 要解决的是真问题吗？ | `docs/W1-discovery/main.md` | `product-discovery-learning-loop` | product bet、metrics、feedback |
| W2 OpenSpec / Risk | 行为、边界、风险是什么？ | `docs/W2-openspec-risk/main.md` | `one-person-openspec-rd` | proposal、spec、design、tasks |
| W3 AI Behavior | AI 怎样算好、坏、危险？ | `docs/W3-ai-behavior/main.md` | `ai-prompt-eval-loop` | eval、prompt、route、red-team |
| W4 Build | 如何落到系统？ | `docs/W4-build/main.md` | `go-kratos-sqlc-service` / `vite-geist-frontend` | code、migration、config、batch log |
| W5 Verify | 上线前证据够吗？ | `docs/W5-verify/main.md` | `quality-test-strategy-guard` | test/eval run、risk review |
| W6 Release | 能发布、能回滚、能承诺吗？ | `docs/W6-release/main.md` | `release-pipeline-gates` | release checklist、launch readiness |
| W7 Operate | 线上怎么观察和恢复？ | `docs/W7-operate/main.md` | `sre-lite-ops` | SLO、dashboard、incident、restore |
| W8 Learn | 学到了什么，下一步做什么？ | `docs/W8-learn/main.md` | `ai-quality-regression-guard` | learning decision、quality review |
| W9 Maintain | 下次还能接起来吗？ | `docs/W9-maintain/main.md` | `knowledge-context-recovery-guard` | context pack、freshness、debt review |

## W0：Intake / 当前焦点

核心规范：

- `docs/W0-intake/main.md`

触发专项：

- 超过 30 分钟或影响用户、生产、数据、安全、成本、AI 行为：`docs/W2-openspec-risk/main.md`
- 支持来源进入：`docs/W8-learn/customer-support-trust-ops-standard.md`
- 客户上线来源进入：`docs/W6-release/customer-pilot-onboarding-launch-standard.md`
- 事故来源进入：`docs/W7-operate/security-privacy-incident-vulnerability-standard.md` 或 `docs/W8-learn/ai-quality-regression-incident-standard.md`

人审点：进入 `now` / `expedite`，停车/杀掉高风险请求，超过 appetite。

## W1：Discovery / 问题与证据

核心规范：

- `docs/W1-discovery/main.md`

触发专项：

- 产品赌注、反馈闭环或学习决策需要更细模板：`docs/W1-discovery/product-discovery-feedback-loop-standard.md`
- 产品事件、指标、实验或 analytics：`docs/W1-discovery/product-analytics-experiment-standard.md`
- 支持反馈成为产品证据：`docs/W8-learn/customer-support-trust-ops-standard.md`
- 客户试点：`docs/W6-release/customer-pilot-onboarding-launch-standard.md`
- 商业承诺苗头：`docs/W6-release/commercial-contract-obligation-standard.md`
- 对外声明苗头：`docs/W6-release/external-claim-evidence-release-gate-standard.md`

人审点：目标用户、问题定义、成功指标、不做什么、证据不足是否继续。

## W2：OpenSpec / 风险框定

主规范：

- `docs/W2-openspec-risk/main.md`

触发专项：

- OpenSpec change 操作系统细则：`docs/W2-openspec-risk/one-person-ai-rd-operating-model.md`
- 架构边界：`docs/W2-openspec-risk/architecture-boundary-standard.md`
- API / 契约兼容：`docs/W2-openspec-risk/api-contract-compatibility-standard.md`
- 安全隐私 / 供应链：`docs/W2-openspec-risk/security-privacy-supply-chain-standard.md`
- Auth / tenant：`docs/W2-openspec-risk/auth-tenant-boundary-standard.md`
- 成本 / 容量：`docs/W2-openspec-risk/cost-capacity-vendor-boundary-standard.md`
- 数据生命周期：`docs/W2-openspec-risk/customer-data-portability-lifecycle-standard.md`
- 供应商处理方：`docs/W2-openspec-risk/processor-transfer-vendor-standard.md`
- IP / license：`docs/W2-openspec-risk/ip-license-provenance-standard.md`
- 信任政策：`docs/W2-openspec-risk/trust-policy-compliance-standard.md`

人审点：数据边界、安全隐私例外、架构锁定、供应商锁定、显著成本。

## W3：AI Behavior / AI 行为设计

主规范：

- `docs/W3-ai-behavior/main.md`

触发专项：

- Prompt / eval / agent workflow：`docs/W3-ai-behavior/prompt-eval-agent-workflow-standard.md`
- AI 数据集与 eval 数据：`docs/W3-ai-behavior/ai-dataset-eval-data-standard.md`
- AI 红队与滥用场景：`docs/W3-ai-behavior/ai-red-team-abuse-standard.md`
- 内容安全：`docs/W3-ai-behavior/content-safety-moderation-standard.md`
- AI 记忆：`docs/W3-ai-behavior/ai-memory-context-standard.md`
- 工具运行时：`docs/W3-ai-behavior/ai-tool-runtime-standard.md`
- 异步 AI 任务：`docs/W4-build/async-job-worker-standard.md`
- RAG：`docs/W3-ai-behavior/rag-retrieval-source-standard.md`
- 模型优化：`docs/W3-ai-behavior/ai-model-optimization-training-standard.md`
- 多语言 AI：`docs/W3-ai-behavior/localization-locale-time-ai-standard.md`

人审点：无 eval 变更、模型供应商变化、工具权限、RAG 来源、记忆策略、安全拒绝策略。

## W4：Build / 产品与系统实现

主规范：

- `docs/W4-build/main.md`

触发专项：

- Go/Kratos/sqlc/gRPC 服务端：`docs/W4-build/go-kratos-sqlc-grpc-service-standard.md`
- Vite 前端：`docs/W4-build/vite-vercel-frontend-standard.md`
- 数据迁移与 sqlc 同步：`docs/W4-build/data-migration-standard.md`
- 配置、环境与 Feature Flag：`docs/W4-build/configuration-feature-flag-standard.md`
- 本地开发与命令自动化：`docs/W4-build/dev-workspace-automation-standard.md`
- AI 协作编码：`docs/W4-build/ai-coding-workflow-standard.md`
- Billing / entitlement：`docs/W4-build/billing-entitlement-metering-standard.md`
- Async job / worker：`docs/W4-build/async-job-worker-standard.md`
- Webhook / event：`docs/W4-build/event-webhook-integration-standard.md`
- Notification / messaging：`docs/W4-build/user-notification-messaging-standard.md`
- API docs / SDK：`docs/W4-build/developer-experience-api-docs-sdk-standard.md`
- Admin action：`docs/W7-operate/admin-ops-action-standard.md`

人审点：不可逆数据迁移、生产配置默认值、用户可见 API/UI 行为、权限、计费、通知或外部副作用变化。

## W5：Verify / 验证与安全门禁

主规范：

- `docs/W5-verify/main.md`

触发专项：

- 测试策略、test matrix、flaky、test/eval run：`docs/W5-verify/testing-quality-standard.md`
- 可访问性、AI UX 与界面信任：`docs/W5-verify/accessibility-ai-ux-standard.md`
- 性能预算、负载验证与回归报告：`docs/W5-verify/performance-budget-load-regression-standard.md`
- 韧性演练、故障注入与降级验证：`docs/W5-verify/resilience-fault-injection-degradation-standard.md`
- AI 质量回归：`docs/W8-learn/ai-quality-regression-incident-standard.md`
- 安全供应链扫描：`docs/W2-openspec-risk/security-privacy-supply-chain-standard.md`
- 内容安全审核：`docs/W3-ai-behavior/content-safety-moderation-standard.md`
- 本地化验证：`docs/W3-ai-behavior/localization-locale-time-ai-standard.md`

人审点：失败门禁、accepted risk、性能回归、AI 质量回归、安全/隐私例外。

## W6：Release / 发布、上线与承诺

主规范：

- `docs/W6-release/main.md`

触发专项：

- 发布流水线、smoke、rollback、post-deploy watch：`docs/W6-release/release-pipeline-standard.md`
- 客户试点、租户上线与交付：`docs/W6-release/customer-pilot-onboarding-launch-standard.md`
- 对外声明、claim 与证据发布门禁：`docs/W6-release/external-claim-evidence-release-gate-standard.md`
- 客户合同、SLA 与商业承诺：`docs/W6-release/commercial-contract-obligation-standard.md`
- Trust policy：`docs/W2-openspec-risk/trust-policy-compliance-standard.md`
- Audit evidence：`docs/W9-maintain/audit-evidence-compliance-standard.md`
- Billing launch：`docs/W4-build/billing-entitlement-metering-standard.md`
- Open source release：`docs/W9-maintain/open-source-release-community-maintenance-standard.md`

人审点：生产发布、回滚、公开声明、合同/SLA、客户定制、证据不足仍发布。

## W7：Operate / 运行、观测与事故

主规范：

- `docs/W7-operate/main.md`

触发专项：

- SRE-lite、SLO、告警、runbook、incident：`docs/W7-operate/sre-lite-operations-standard.md`
- 观测性、遥测与 AI Trace：`docs/W7-operate/observability-telemetry-standard.md`
- 备份、恢复与业务连续性：`docs/W7-operate/backup-recovery-continuity-standard.md`
- 后台运营、人工操作与高风险动作：`docs/W7-operate/admin-ops-action-standard.md`
- 安全/隐私事故与漏洞披露：`docs/W7-operate/security-privacy-incident-vulnerability-standard.md`
- 凭据、密钥与服务账号生命周期：`docs/W7-operate/credential-secret-lifecycle-standard.md`
- Infra / IaC：`docs/W7-operate/infra-iac-environment-standard.md`
- Event / webhook delivery：`docs/W4-build/event-webhook-integration-standard.md`
- Async worker ops：`docs/W4-build/async-job-worker-standard.md`

人审点：事故升级、客户/监管通知、生产恢复、凭据轮换、break-glass。

## W8：Learn / 反馈、质量回归与下一轮

主规范：

- `docs/W8-learn/main.md`

触发专项：

- 支持反馈、投诉、信任运营：`docs/W8-learn/customer-support-trust-ops-standard.md`
- AI 质量回归、线上质量事故与回滚：`docs/W8-learn/ai-quality-regression-incident-standard.md`
- 学习结果改变产品问题或成功指标：`docs/W1-discovery/main.md`
- 需要事件、指标或实验复盘：`docs/W1-discovery/product-analytics-experiment-standard.md`
- 学习结果改变当前优先级：`docs/W0-intake/main.md`
- Customer onboarding signal：`docs/W6-release/customer-pilot-onboarding-launch-standard.md`
- Notification feedback：`docs/W4-build/user-notification-messaging-standard.md`
- Cost review：`docs/W2-openspec-risk/cost-capacity-vendor-boundary-standard.md`

人审点：继续、扩大、停车、杀掉、回滚、重新定义产品方向。

## W9：Maintain / 维护、知识与长期演进

主规范：

- `docs/W9-maintain/main.md`

触发专项：

- 知识管理、文档与上下文恢复：`docs/W9-maintain/knowledge-context-recovery-standard.md`
- 维护、依赖升级、技术债与弃用：`docs/W9-maintain/maintenance-dependency-debt-standard.md`
- 审计、证据保全与合规证据包：`docs/W9-maintain/audit-evidence-compliance-standard.md`
- 开源发布、社区贡献与维护边界：`docs/W9-maintain/open-source-release-community-maintenance-standard.md`
- Processor watch：`docs/W2-openspec-risk/processor-transfer-vendor-standard.md`
- License / provenance：`docs/W2-openspec-risk/ip-license-provenance-standard.md`
- Developer docs freshness：`docs/W4-build/developer-experience-api-docs-sdk-standard.md`

人审点：canonical source、术语变化、删除/归档、接受过期文档、长期维护边界。

## 阶段到 Workflow 的主归属

| 阶段 | 主归属 | 规范 |
| --- | --- | --- |
| 01 | W2 | `docs/W2-openspec-risk/one-person-ai-rd-operating-model.md` |
| 02 | W4 | `docs/W4-build/go-kratos-sqlc-grpc-service-standard.md` |
| 03 | W4 | `docs/W4-build/vite-vercel-frontend-standard.md` |
| 04 | W3 | `docs/W3-ai-behavior/prompt-eval-agent-workflow-standard.md` |
| 05 | W7 | `docs/W7-operate/sre-lite-operations-standard.md` |
| 06 | W6 | `docs/W6-release/release-pipeline-standard.md` |
| 07 | W4 | `docs/W4-build/data-migration-standard.md` |
| 08 | W2 | `docs/W2-openspec-risk/auth-tenant-boundary-standard.md` |
| 09 | W2 | `docs/W2-openspec-risk/cost-capacity-vendor-boundary-standard.md` |
| 10 | W2 | `docs/W2-openspec-risk/security-privacy-supply-chain-standard.md` |
| 11 | W1 | `docs/W1-discovery/product-discovery-feedback-loop-standard.md` |
| 12 | W5 | `docs/W5-verify/testing-quality-standard.md` |
| 13 | W2 | `docs/W2-openspec-risk/architecture-boundary-standard.md` |
| 14 | W4 | `docs/W4-build/configuration-feature-flag-standard.md` |
| 15 | W7 | `docs/W7-operate/observability-telemetry-standard.md` |
| 16 | W9 | `docs/W9-maintain/knowledge-context-recovery-standard.md` |
| 17 | W9 | `docs/W9-maintain/maintenance-dependency-debt-standard.md` |
| 18 | W2 | `docs/W2-openspec-risk/api-contract-compatibility-standard.md` |
| 19 | W4 | `docs/W4-build/dev-workspace-automation-standard.md` |
| 20 | W4 | `docs/W4-build/ai-coding-workflow-standard.md` |
| 21 | W7 | `docs/W7-operate/backup-recovery-continuity-standard.md` |
| 22 | W4 | `docs/W4-build/billing-entitlement-metering-standard.md` |
| 23 | W8 | `docs/W8-learn/customer-support-trust-ops-standard.md` |
| 24 | W7 | `docs/W7-operate/admin-ops-action-standard.md` |
| 25 | W2 | `docs/W2-openspec-risk/trust-policy-compliance-standard.md` |
| 26 | W3 | `docs/W3-ai-behavior/ai-dataset-eval-data-standard.md` |
| 27 | W3 | `docs/W3-ai-behavior/ai-red-team-abuse-standard.md` |
| 28 | W3 | `docs/W3-ai-behavior/content-safety-moderation-standard.md` |
| 29 | W3 | `docs/W3-ai-behavior/ai-memory-context-standard.md` |
| 30 | W3 | `docs/W3-ai-behavior/ai-model-routing-provider-standard.md` |
| 31 | W5 | `docs/W5-verify/accessibility-ai-ux-standard.md` |
| 32 | W3 | `docs/W3-ai-behavior/ai-tool-runtime-standard.md` |
| 33 | W4 | `docs/W4-build/async-job-worker-standard.md` |
| 34 | W4 | `docs/W4-build/event-webhook-integration-standard.md` |
| 35 | W9 | `docs/W9-maintain/audit-evidence-compliance-standard.md` |
| 36 | W3 | `docs/W3-ai-behavior/rag-retrieval-source-standard.md` |
| 37 | W7 | `docs/W7-operate/infra-iac-environment-standard.md` |
| 38 | W4 | `docs/W4-build/user-notification-messaging-standard.md` |
| 39 | W1 | `docs/W1-discovery/product-analytics-experiment-standard.md` |
| 40 | W2 | `docs/W2-openspec-risk/customer-data-portability-lifecycle-standard.md` |
| 41 | W2 | `docs/W2-openspec-risk/processor-transfer-vendor-standard.md` |
| 42 | W2 | `docs/W2-openspec-risk/ip-license-provenance-standard.md` |
| 43 | W6 | `docs/W6-release/commercial-contract-obligation-standard.md` |
| 44 | W7 | `docs/W7-operate/security-privacy-incident-vulnerability-standard.md` |
| 45 | W4 | `docs/W4-build/developer-experience-api-docs-sdk-standard.md` |
| 46 | W6 | `docs/W6-release/external-claim-evidence-release-gate-standard.md` |
| 47 | W9 | `docs/W9-maintain/open-source-release-community-maintenance-standard.md` |
| 48 | W8 | `docs/W8-learn/ai-quality-regression-incident-standard.md` |
| 49 | W6 | `docs/W6-release/customer-pilot-onboarding-launch-standard.md` |
| 50 | W0 | `docs/W0-intake/main.md` |
| 51 | W3 | `docs/W3-ai-behavior/ai-model-optimization-training-standard.md` |
| 52 | W5 | `docs/W5-verify/performance-budget-load-regression-standard.md` |
| 53 | W5 | `docs/W5-verify/resilience-fault-injection-degradation-standard.md` |
| 54 | W7 | `docs/W7-operate/credential-secret-lifecycle-standard.md` |
| 55 | W3 | `docs/W3-ai-behavior/localization-locale-time-ai-standard.md` |

## 新增规范准入规则

新增规范必须先回答：

- 它服务 W0-W9 哪一步？
- 它是否补的是已有 step 的缺口，而不是另起一摊？
- 它的最小 artifact 是什么？
- 它替人减少了哪个判断或重复劳动？
- 它需要哪个 skill 或 verifier 承接？

答不清时，不新增规范；先更新当前 workflow step 的索引或 context pack。







