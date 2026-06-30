# AI 研发工作流规范索引

## 使用规则

这份索引按 W0-W9 AI 研发工作流组织。文件名前缀只表示所在 W 目录内的阅读顺序。

默认流程：

1. 先在 `docs/00-start-here.md` 定位 W0-W9。
2. 读取当前 step 的 `00-main.md`。
3. 只在触发条件出现时读取专项规范。
4. 需要角色视角时，再读 `docs/03-role-index.md` 和对应 `docs/roles/*.md`。
5. 新增规范必须声明它服务哪个 workflow step 和哪个角色消费者。

总入口 skill：`one-person-openspec-rd`。总控 Agent 先定位 W0-W9，再按角色泳道调度产品、Tech Lead、后端、前端、测试、运维、运营、安全合规。

验证命令：

```powershell
python tools\verify_workflow_index.py .
```

## Workflow-To-Standard Map

| Step | 研发问题 | 主规范 | 常用 skill | 主要产出 |
| --- | --- | --- | --- | --- |
| W0 Intake | 现在该不该做？ | `docs/W0-intake/00-main.md` | `roadmap-prioritization-guard` | work-intake、decision-board |
| W1 Discovery | 要解决的是真问题吗？ | `docs/W1-discovery/00-main.md` | `product-discovery-learning-loop` | product bet、metrics、feedback |
| W2 OpenSpec / Risk | 行为、边界、风险是什么？ | `docs/W2-openspec-risk/00-main.md` | `one-person-openspec-rd` | proposal、spec、design、tasks |
| W3 AI Behavior | AI 怎样算好、坏、危险？ | `docs/W3-ai-behavior/00-main.md` | `ai-prompt-eval-loop` | eval、prompt、route、safety |
| W4 Build | 如何落到系统？ | `docs/W4-build/00-main.md` | `go-kratos-sqlc-service` / `vite-geist-frontend` | code、migration、config、batch log |
| W5 Verify | 上线前证据够吗？ | `docs/W5-verify/00-main.md` | `quality-test-strategy-guard` | test/eval run、risk review |
| W6 Release | 能发布、能回滚、能承诺吗？ | `docs/W6-release/00-main.md` | `release-pipeline-gates` | release checklist、launch readiness |
| W7 Operate | 线上怎么观察和恢复？ | `docs/W7-operate/00-main.md` | `sre-lite-ops` | SLO、dashboard、incident、restore |
| W8 Learn | 学到了什么，下一步做什么？ | `docs/W8-learn/00-main.md` | `ai-quality-regression-guard` | learning decision、quality review |
| W9 Maintain | 下次还能接起来吗？ | `docs/W9-maintain/00-main.md` | `knowledge-context-recovery-guard` | context pack、freshness、debt review |

## W0：Intake / 当前焦点

核心规范：

- `docs/W0-intake/00-main.md`

触发方向：

- 超过 30 分钟，或影响用户、生产、数据、安全、成本、AI 行为、公开承诺：进入 W2。
- 支持/客户/事故信号作为入口：先记录来源，再按 W8/W7/W6 回流到 W0。

人审点：进入 `now` / `expedite`，停车/杀掉高风险请求，超过 appetite。

## W1：Discovery / 问题与证据

核心规范：

- `docs/W1-discovery/00-main.md`

触发专项：

- 产品事件、指标、实验、analytics、隐私友好 tracking、数据质量：`docs/W1-discovery/01-product-analytics-experiment-standard.md`
- 支持反馈成为产品证据：`docs/W8-learn/01-customer-support-trust-ops-standard.md`
- 客户试点影响方向：`docs/W6-release/02-customer-pilot-onboarding-launch-standard.md`
- 对外声明或商业承诺苗头：`docs/W6-release/03-external-claim-evidence-release-gate-standard.md` 或 W2 `docs/W2-openspec-risk/04-cost-data-vendor-trust-boundary-standard.md`

降级说明：原产品发现闭环专项已并入 W1 主入口；访谈、product bet、feedback、experiment、decision 默认在 `docs/W1-discovery/00-main.md` 的最小产出中完成。

人审点：目标用户、问题定义、唯一主指标、不做什么、证据不足是否继续。

## W2：OpenSpec / 风险框定

主规范：

- `docs/W2-openspec-risk/00-main.md`

触发专项：

- 架构边界、模块职责、数据所有权、依赖方向、ADR：`docs/W2-openspec-risk/01-architecture-boundary-standard.md`
- API、Protobuf、错误语义、事件、webhook、AI tool schema、兼容性：`docs/W2-openspec-risk/02-api-contract-compatibility-standard.md`
- 威胁模型、数据处理、认证授权、租户隔离、secret、供应链、AI 工具权限：`docs/W2-openspec-risk/03-security-auth-supply-chain-standard.md`
- 成本、客户数据生命周期、供应商处理方、数据出境、IP/license、信任政策、公开承诺：`docs/W2-openspec-risk/04-cost-data-vendor-trust-boundary-standard.md`

降级说明：原 W2 操作系统专项已由 W2 主入口、OpenSpec change 和 `one-person-openspec-rd` skill 承接。

人审点：数据边界、安全隐私例外、架构锁定、供应商锁定、显著成本、公开承诺。

## W3：AI Behavior / AI 行为设计

主规范：

- `docs/W3-ai-behavior/00-main.md`

触发专项：

- Prompt、eval、结构化输出、workflow/agent 升级：`docs/W3-ai-behavior/01-prompt-eval-agent-workflow-standard.md`
- AI eval 数据、红队、滥用样本、内容安全、moderation、safety release：`docs/W3-ai-behavior/02-ai-eval-safety-standard.md`
- AI 记忆、用户偏好、长期上下文、RAG 来源、检索、引用、删除：`docs/W3-ai-behavior/03-ai-context-memory-retrieval-standard.md`
- 模型选择、供应商路由、fallback、工具运行时、外部连接器、MCP、沙箱、审批、幂等和审计：`docs/W3-ai-behavior/04-ai-runtime-routing-tools-standard.md`

降级说明：模型优化/微调/蒸馏、本地化/多语言 AI 默认只在 W3 主入口保留触发提醒；真实训练、正式 locale、多币种或高风险翻译再单独开 OpenSpec change。

人审点：无 eval 变更、模型供应商变化、工具权限、RAG 来源、记忆默认开启、安全拒绝策略。

## W4：Build / 产品与系统实现

主规范：

- `docs/W4-build/00-main.md`

触发专项：

- Go/Kratos/sqlc/gRPC 服务端：`docs/W4-build/01-go-kratos-sqlc-grpc-service-standard.md`
- Vite 前端：`docs/W4-build/02-vite-vercel-frontend-standard.md`
- 数据迁移与 sqlc 同步：`docs/W4-build/03-data-migration-standard.md`
- 配置、环境与 Feature Flag：`docs/W4-build/04-configuration-feature-flag-standard.md`
- 本地开发、命令自动化、AI 协作编码、批次、自审和 verification：`docs/W4-build/05-dev-workspace-ai-coding-standard.md`
- 计费、Webhook、事件、外部 provider、用户通知、送达、退订和开发者可依赖副作用：`docs/W4-build/06-external-side-effects-standard.md`
- Async job、worker、队列、Batch/background、取消、重试、死信：`docs/W4-build/07-async-job-worker-standard.md`

降级说明：开发者 API 文档、SDK、示例和 changelog 默认由 W2 API 契约、W4 主入口、W6 对外声明和 W9 知识恢复承接；public/stable surface 再单独开 change。

人审点：不可逆数据迁移、生产配置默认值、用户可见 API/UI 行为、权限、计费、通知或外部副作用变化。

## W5：Verify / 验证与安全门禁

主规范：

- `docs/W5-verify/00-main.md`

触发专项：

- 测试策略、test matrix、flaky、Go/Vite/sqlc/gRPC/AI eval 门禁：`docs/W5-verify/01-testing-quality-standard.md`
- 可访问性、AI UX 与界面信任：`docs/W5-verify/02-accessibility-ai-ux-standard.md`
- 性能、容量、负载、Web Vitals、AI latency/token、依赖失败、降级、fault injection、dead letter：`docs/W5-verify/03-operational-risk-verification-standard.md`

人审点：失败门禁、accepted risk、性能回归、降级缺口、AI 质量回归、安全/隐私例外。

## W6：Release / 发布、上线与承诺

主规范：

- `docs/W6-release/00-main.md`

触发专项：

- 发布流水线、smoke、rollback、post-deploy watch：`docs/W6-release/01-release-pipeline-standard.md`
- 客户试点、租户上线与交付：`docs/W6-release/02-customer-pilot-onboarding-launch-standard.md`
- 对外声明、claim 与证据发布门禁：`docs/W6-release/03-external-claim-evidence-release-gate-standard.md`

降级说明：商业合同、SLA、服务积分和非标准承诺默认由 W6 主入口、W2 成本/数据/供应商/信任边界和对外声明证据门禁承接；正式合同或非标准条款单独开 change。

人审点：生产发布、回滚、公开声明、合同/SLA、客户定制、证据不足仍发布。

## W7：Operate / 运行、观测与事故

主规范：

- `docs/W7-operate/00-main.md`

触发专项：

- SRE-lite、SLO、告警、runbook、observability、restore drill、infra/drift、incident：`docs/W7-operate/01-sre-lite-operations-standard.md`
- 后台运营、人工操作、break-glass、dry-run、审计日志：`docs/W7-operate/02-admin-ops-action-standard.md`
- 安全/隐私事故、漏洞披露、AI 安全事故、advisory：`docs/W7-operate/03-security-privacy-incident-vulnerability-standard.md`
- 凭据、密钥、服务账号、rotation、exposure review、OpenAI/provider key：`docs/W7-operate/04-credential-secret-lifecycle-standard.md`

降级说明：观测性、备份恢复和 IaC 已并入 SRE-lite 的运行准备提醒；真实生产恢复、跨区域容灾、生产 IaC apply/destroy 或客户证据再单独开 change。

人审点：事故升级、客户/监管通知、生产恢复、凭据轮换、break-glass、生产 IaC。

## W8：Learn / 反馈、质量回归与下一轮

主规范：

- `docs/W8-learn/00-main.md`

触发专项：

- 支持反馈、投诉、信任运营：`docs/W8-learn/01-customer-support-trust-ops-standard.md`
- AI 质量回归、线上质量事故与回滚：`docs/W8-learn/02-ai-quality-regression-incident-standard.md`

人审点：继续、扩大、停车、杀掉、回滚、重新定义产品方向。

## W9：Maintain / 维护、知识与长期演进

主规范：

- `docs/W9-maintain/00-main.md`

触发专项：

- 知识管理、文档与上下文恢复：`docs/W9-maintain/01-knowledge-context-recovery-standard.md`
- 维护、依赖升级、技术债与弃用：`docs/W9-maintain/02-maintenance-dependency-debt-standard.md`

降级说明：审计证据包和开源社区维护默认在 W9 主入口的证据索引、维护事实和对外维护边界中登记；真实客户/审计导出、公开仓库或官方 SDK 发布再单独开 change。

人审点：canonical source、术语变化、删除/归档、接受过期文档、长期维护边界。

## 角色泳道

角色入口不复制规范正文，只负责调度和输出契约：

- 产品：`docs/roles/product.md`
- Tech Lead：`docs/roles/tech-lead.md`
- 后端：`docs/roles/backend.md`
- 前端：`docs/roles/frontend.md`
- 测试：`docs/roles/qa.md`
- 运维：`docs/roles/ops.md`
- 运营：`docs/roles/support-ops.md`
- 安全合规：`docs/roles/security-compliance.md`

## 新增规范准入规则

新增规范必须先回答：

- 它服务 W0-W9 哪一步？
- 它服务哪个角色消费者？
- 它是否补的是已有 step 的缺口，而不是另起一摊？
- 它的最小 artifact 是什么？
- 它替人减少了哪个判断或重复劳动？
- 它需要哪个 skill 或 verifier 承接？

答不清时，不新增规范；先更新当前 workflow step 的 `00-main.md`、角色入口或 context pack。
