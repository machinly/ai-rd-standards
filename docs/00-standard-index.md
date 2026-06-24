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
| W0 Intake | 现在该不该做？ | `roadmap-prioritization-work-intake-standard` | `roadmap-prioritization-guard` | work-intake、decision-board |
| W1 Discovery | 要解决的是真问题吗？ | `product-discovery-feedback-loop-standard` | `product-discovery-learning-loop` | product bet、metrics、feedback |
| W2 OpenSpec / Risk | 行为、边界、风险是什么？ | `01`、`13`、`18`、`10` | `one-person-openspec-rd` | proposal、spec、design、tasks |
| W3 AI Behavior | AI 怎样算好、坏、危险？ | `04`、`26`、`27`、`30` | `ai-prompt-eval-loop` | eval、prompt、route、red-team |
| W4 Build | 如何落到系统？ | `02`、`03`、`07`、`14`、`20` | `go-kratos-sqlc-service` / `vite-geist-frontend` | code、migration、config、batch log |
| W5 Verify | 上线前证据够吗？ | `12`、`31`、`52`、`53` | `quality-test-strategy-guard` | test/eval run、risk review |
| W6 Release | 能发布、能回滚、能承诺吗？ | `06`、`49`、`46`、`43` | `release-pipeline-gates` | release checklist、launch readiness |
| W7 Operate | 线上怎么观察和恢复？ | `05`、`15`、`21`、`44`、`54` | `sre-lite-ops` | SLO、dashboard、incident、restore |
| W8 Learn | 学到了什么，下一步做什么？ | `11`、`39`、`23`、`48`、`50` | `ai-quality-regression-guard` | learning decision、quality review |
| W9 Maintain | 下次还能接起来吗？ | `16`、`17`、`35`、`47` | `knowledge-context-recovery-guard` | context pack、freshness、debt review |

## W0：Intake / 当前焦点

核心规范：

- `docs/W0-intake/main.md`

触发专项：

- 超过 30 分钟或影响用户/生产/数据/安全/成本/AI 行为：`docs/W2-openspec-risk/one-person-ai-rd-operating-model.md`
- 支持来源进入：`docs/W8-learn/23-customer-support-trust-ops-standard.md`
- 客户上线来源进入：`docs/W6-release/49-customer-pilot-onboarding-launch-standard.md`
- 事故来源进入：`docs/W7-operate/44-security-privacy-incident-vulnerability-standard.md` 或 `docs/W8-learn/48-ai-quality-regression-incident-standard.md`

人审点：进入 `now` / `expedite`，停车/杀掉高风险请求，超过 appetite。

## W1：Discovery / 问题与证据

核心规范：

- `docs/W1-discovery/product-discovery-feedback-loop-standard.md`

触发专项：

- 产品事件、指标、实验或 analytics：`docs/W1-discovery/product-analytics-experiment-standard.md`
- 支持反馈成为产品证据：`docs/W8-learn/23-customer-support-trust-ops-standard.md`
- 客户试点：`docs/W6-release/49-customer-pilot-onboarding-launch-standard.md`
- 商业承诺苗头：`docs/W6-release/43-commercial-contract-obligation-standard.md`
- 对外声明苗头：`docs/W6-release/46-external-claim-evidence-release-gate-standard.md`

人审点：目标用户、问题定义、成功指标、不做什么、证据不足是否继续。

## W2：OpenSpec / 风险框定

主规范：

- `docs/W2-openspec-risk/one-person-ai-rd-operating-model.md`
- `docs/W2-openspec-risk/architecture-boundary-standard.md`
- `docs/W2-openspec-risk/api-contract-compatibility-standard.md`
- `docs/W2-openspec-risk/security-privacy-supply-chain-standard.md`

触发专项：

- Auth / tenant：`docs/W2-openspec-risk/auth-tenant-boundary-standard.md`
- 成本 / 容量：`docs/W2-openspec-risk/cost-capacity-vendor-boundary-standard.md`
- 数据生命周期：`docs/W2-openspec-risk/customer-data-portability-lifecycle-standard.md`
- 供应商处理方：`docs/W2-openspec-risk/processor-transfer-vendor-standard.md`
- IP / license：`docs/W2-openspec-risk/ip-license-provenance-standard.md`
- 信任政策：`docs/W2-openspec-risk/trust-policy-compliance-standard.md`

人审点：数据边界、安全隐私例外、架构锁定、供应商锁定、显著成本。

## W3：AI Behavior / AI 行为设计

主规范：

- `docs/W3-ai-behavior/04-ai-prompt-eval-agent-workflow-standard.md`
- `docs/W3-ai-behavior/26-ai-dataset-eval-data-standard.md`
- `docs/W3-ai-behavior/27-ai-red-team-abuse-standard.md`
- `docs/W3-ai-behavior/30-ai-model-routing-provider-standard.md`

触发专项：

- 内容安全：`docs/W3-ai-behavior/28-content-safety-moderation-standard.md`
- AI 记忆：`docs/W3-ai-behavior/29-ai-memory-context-standard.md`
- 工具运行时：`docs/W3-ai-behavior/32-ai-tool-runtime-standard.md`
- 异步 AI 任务：`docs/W4-build/33-async-job-worker-standard.md`
- RAG：`docs/W3-ai-behavior/36-rag-retrieval-source-standard.md`
- 模型优化：`docs/W3-ai-behavior/51-ai-model-optimization-training-standard.md`
- 多语言 AI：`docs/W3-ai-behavior/55-localization-locale-time-ai-standard.md`

人审点：无 eval 变更、模型供应商变化、工具权限、RAG 来源、记忆策略、安全拒绝策略。

## W4：Build / 产品与系统实现

主规范：

- `docs/W4-build/02-go-kratos-sqlc-grpc-service-standard.md`
- `docs/W4-build/03-vite-vercel-frontend-standard.md`
- `docs/W4-build/07-data-migration-standard.md`
- `docs/W4-build/14-configuration-feature-flag-standard.md`
- `docs/W4-build/19-dev-workspace-automation-standard.md`
- `docs/W4-build/20-ai-coding-workflow-standard.md`

触发专项：

- API docs / SDK：`docs/W4-build/45-developer-experience-api-docs-sdk-standard.md`
- Webhook / event：`docs/W4-build/34-event-webhook-integration-standard.md`
- Admin action：`docs/W7-operate/24-admin-ops-action-standard.md`
- Billing / entitlement：`docs/W4-build/22-billing-entitlement-metering-standard.md`
- Notification：`docs/W4-build/38-user-notification-messaging-standard.md`

人审点：不可逆数据迁移、生产配置默认值、用户可见 API/UI 行为变化。

## W5：Verify / 验证与安全门禁

主规范：

- `docs/W5-verify/12-testing-quality-standard.md`
- `docs/W5-verify/31-accessibility-ai-ux-standard.md`
- `docs/W5-verify/52-performance-budget-load-regression-standard.md`
- `docs/W5-verify/53-resilience-fault-injection-degradation-standard.md`

触发专项：

- AI 质量回归：`docs/W8-learn/48-ai-quality-regression-incident-standard.md`
- 安全供应链扫描：`docs/W2-openspec-risk/security-privacy-supply-chain-standard.md`
- 内容安全审核：`docs/W3-ai-behavior/28-content-safety-moderation-standard.md`
- 本地化验证：`docs/W3-ai-behavior/55-localization-locale-time-ai-standard.md`

人审点：失败门禁、accepted risk、性能回归、AI 质量回归、安全/隐私例外。

## W6：Release / 发布、上线与承诺

主规范：

- `docs/W6-release/06-release-pipeline-standard.md`
- `docs/W6-release/49-customer-pilot-onboarding-launch-standard.md`
- `docs/W6-release/46-external-claim-evidence-release-gate-standard.md`
- `docs/W6-release/43-commercial-contract-obligation-standard.md`

触发专项：

- Trust policy：`docs/W2-openspec-risk/trust-policy-compliance-standard.md`
- Audit evidence：`docs/W9-maintain/35-audit-evidence-compliance-standard.md`
- Billing launch：`docs/W4-build/22-billing-entitlement-metering-standard.md`
- Open source release：`docs/W9-maintain/47-open-source-release-community-maintenance-standard.md`

人审点：生产发布、回滚、公开声明、合同/SLA、客户定制、证据不足仍发布。

## W7：Operate / 运行、观测与事故

主规范：

- `docs/W7-operate/05-sre-lite-operations-standard.md`
- `docs/W7-operate/15-observability-telemetry-standard.md`
- `docs/W7-operate/21-backup-recovery-continuity-standard.md`
- `docs/W7-operate/44-security-privacy-incident-vulnerability-standard.md`
- `docs/W7-operate/54-credential-secret-lifecycle-standard.md`

触发专项：

- Infra / IaC：`docs/W7-operate/37-infra-iac-environment-standard.md`
- Event / webhook delivery：`docs/W4-build/34-event-webhook-integration-standard.md`
- Async worker ops：`docs/W4-build/33-async-job-worker-standard.md`
- Admin ops：`docs/W7-operate/24-admin-ops-action-standard.md`

人审点：事故升级、客户/监管通知、生产恢复、凭据轮换、break-glass。

## W8：Learn / 反馈、质量回归与下一轮

主规范：

- `docs/W1-discovery/product-discovery-feedback-loop-standard.md`
- `docs/W1-discovery/product-analytics-experiment-standard.md`
- `docs/W8-learn/23-customer-support-trust-ops-standard.md`
- `docs/W8-learn/48-ai-quality-regression-incident-standard.md`
- `docs/W0-intake/main.md`

触发专项：

- Customer onboarding signal：`docs/W6-release/49-customer-pilot-onboarding-launch-standard.md`
- Notification feedback：`docs/W4-build/38-user-notification-messaging-standard.md`
- Cost review：`docs/W2-openspec-risk/cost-capacity-vendor-boundary-standard.md`

人审点：继续、扩大、停车、杀掉、回滚、重新定义产品方向。

## W9：Maintain / 维护、知识与长期演进

主规范：

- `docs/W9-maintain/16-knowledge-context-recovery-standard.md`
- `docs/W9-maintain/17-maintenance-dependency-debt-standard.md`
- `docs/W9-maintain/35-audit-evidence-compliance-standard.md`
- `docs/W9-maintain/47-open-source-release-community-maintenance-standard.md`

触发专项：

- Processor watch：`docs/W2-openspec-risk/processor-transfer-vendor-standard.md`
- License / provenance：`docs/W2-openspec-risk/ip-license-provenance-standard.md`
- Developer docs freshness：`docs/W4-build/45-developer-experience-api-docs-sdk-standard.md`

人审点：canonical source、术语变化、删除/归档、接受过期文档、长期维护边界。

## 阶段到 Workflow 的主归属

| 阶段 | 主归属 | 规范 |
| --- | --- | --- |
| 01 | W2 | `docs/W2-openspec-risk/one-person-ai-rd-operating-model.md` |
| 02 | W4 | `docs/W4-build/02-go-kratos-sqlc-grpc-service-standard.md` |
| 03 | W4 | `docs/W4-build/03-vite-vercel-frontend-standard.md` |
| 04 | W3 | `docs/W3-ai-behavior/04-ai-prompt-eval-agent-workflow-standard.md` |
| 05 | W7 | `docs/W7-operate/05-sre-lite-operations-standard.md` |
| 06 | W6 | `docs/W6-release/06-release-pipeline-standard.md` |
| 07 | W4 | `docs/W4-build/07-data-migration-standard.md` |
| 08 | W2 | `docs/W2-openspec-risk/auth-tenant-boundary-standard.md` |
| 09 | W2 | `docs/W2-openspec-risk/cost-capacity-vendor-boundary-standard.md` |
| 10 | W2 | `docs/W2-openspec-risk/security-privacy-supply-chain-standard.md` |
| 11 | W1 | `docs/W1-discovery/product-discovery-feedback-loop-standard.md` |
| 12 | W5 | `docs/W5-verify/12-testing-quality-standard.md` |
| 13 | W2 | `docs/W2-openspec-risk/architecture-boundary-standard.md` |
| 14 | W4 | `docs/W4-build/14-configuration-feature-flag-standard.md` |
| 15 | W7 | `docs/W7-operate/15-observability-telemetry-standard.md` |
| 16 | W9 | `docs/W9-maintain/16-knowledge-context-recovery-standard.md` |
| 17 | W9 | `docs/W9-maintain/17-maintenance-dependency-debt-standard.md` |
| 18 | W2 | `docs/W2-openspec-risk/api-contract-compatibility-standard.md` |
| 19 | W4 | `docs/W4-build/19-dev-workspace-automation-standard.md` |
| 20 | W4 | `docs/W4-build/20-ai-coding-workflow-standard.md` |
| 21 | W7 | `docs/W7-operate/21-backup-recovery-continuity-standard.md` |
| 22 | W4 | `docs/W4-build/22-billing-entitlement-metering-standard.md` |
| 23 | W8 | `docs/W8-learn/23-customer-support-trust-ops-standard.md` |
| 24 | W7 | `docs/W7-operate/24-admin-ops-action-standard.md` |
| 25 | W2 | `docs/W2-openspec-risk/trust-policy-compliance-standard.md` |
| 26 | W3 | `docs/W3-ai-behavior/26-ai-dataset-eval-data-standard.md` |
| 27 | W3 | `docs/W3-ai-behavior/27-ai-red-team-abuse-standard.md` |
| 28 | W3 | `docs/W3-ai-behavior/28-content-safety-moderation-standard.md` |
| 29 | W3 | `docs/W3-ai-behavior/29-ai-memory-context-standard.md` |
| 30 | W3 | `docs/W3-ai-behavior/30-ai-model-routing-provider-standard.md` |
| 31 | W5 | `docs/W5-verify/31-accessibility-ai-ux-standard.md` |
| 32 | W3 | `docs/W3-ai-behavior/32-ai-tool-runtime-standard.md` |
| 33 | W4 | `docs/W4-build/33-async-job-worker-standard.md` |
| 34 | W4 | `docs/W4-build/34-event-webhook-integration-standard.md` |
| 35 | W9 | `docs/W9-maintain/35-audit-evidence-compliance-standard.md` |
| 36 | W3 | `docs/W3-ai-behavior/36-rag-retrieval-source-standard.md` |
| 37 | W7 | `docs/W7-operate/37-infra-iac-environment-standard.md` |
| 38 | W4 | `docs/W4-build/38-user-notification-messaging-standard.md` |
| 39 | W1 | `docs/W1-discovery/product-analytics-experiment-standard.md` |
| 40 | W2 | `docs/W2-openspec-risk/customer-data-portability-lifecycle-standard.md` |
| 41 | W2 | `docs/W2-openspec-risk/processor-transfer-vendor-standard.md` |
| 42 | W2 | `docs/W2-openspec-risk/ip-license-provenance-standard.md` |
| 43 | W6 | `docs/W6-release/43-commercial-contract-obligation-standard.md` |
| 44 | W7 | `docs/W7-operate/44-security-privacy-incident-vulnerability-standard.md` |
| 45 | W4 | `docs/W4-build/45-developer-experience-api-docs-sdk-standard.md` |
| 46 | W6 | `docs/W6-release/46-external-claim-evidence-release-gate-standard.md` |
| 47 | W9 | `docs/W9-maintain/47-open-source-release-community-maintenance-standard.md` |
| 48 | W8 | `docs/W8-learn/48-ai-quality-regression-incident-standard.md` |
| 49 | W6 | `docs/W6-release/49-customer-pilot-onboarding-launch-standard.md` |
| 50 | W0 | `docs/W0-intake/main.md` |
| 51 | W3 | `docs/W3-ai-behavior/51-ai-model-optimization-training-standard.md` |
| 52 | W5 | `docs/W5-verify/52-performance-budget-load-regression-standard.md` |
| 53 | W5 | `docs/W5-verify/53-resilience-fault-injection-degradation-standard.md` |
| 54 | W7 | `docs/W7-operate/54-credential-secret-lifecycle-standard.md` |
| 55 | W3 | `docs/W3-ai-behavior/55-localization-locale-time-ai-standard.md` |

## 新增规范准入规则

新增规范必须先回答：

- 它服务 W0-W9 哪一步？
- 它是否补的是已有 step 的缺口，而不是另起一摊？
- 它的最小 artifact 是什么？
- 它替人减少了哪个判断或重复劳动？
- 它需要哪个 skill 或 verifier 承接？

答不清时，不新增规范；先更新当前 workflow step 的索引或 context pack。







