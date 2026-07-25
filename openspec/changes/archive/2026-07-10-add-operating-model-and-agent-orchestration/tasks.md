# Tasks

- [x] 新增 `docs/04-operating-model.md`：系统模型、并发隐喻映射、第一性原则、自主性等级、失效模式速查、与 W0-W9 的关系。
- [x] 新增 `docs/05-agent-orchestration.md`：拓扑与角色、任务契约、通信协议、执行循环、并发纪律、失败升级、无人值守门禁、可观测性、采用路径。
- [x] 更新 `README.md`：加入操作模型与编排规范入口，保持规范引用 ≤8 个。
- [x] 更新 `docs/00-start-here.md`：说明 L0/L1 层与 W0-W9 的关系，更新 Codex 接手提示。
- [x] 更新 `docs/02-standard-index.md`：新增"操作模型与编排层"章节并挂接两份新文档。
- [x] 更新 `docs/03-role-index.md`：声明角色 Agent 遵循编排规范的任务契约与升级规则。
- [x] 更新 `knowledge/context-packs/rd-standards.md`：System Shape 与 AI Behavior 补充新层。
- [x] 在 `docs/sources/2026-06-23-source-map.md` 追加 2026-07-03 编排与自主系统依据章节。
- [x] 完成两轮落地 review（Review A 一人可执行性 / Review B 产品工程运维风险），结论见 proposal 交付说明。

## W0-W9 落地扩展

- [x] 更新 `docs/W0-intake/00-main.md`：入口取舍承接目标平面、小项目范围/appetite/non-goals、多 Agent 只定义目标与人审点。
- [x] 更新 `docs/W1-discovery/00-main.md`：发现阶段承接成功标准、证据、范围控制、只读并行发现和原始证据引用。
- [x] 更新 `docs/W2-openspec-risk/00-main.md`：OpenSpec 承接行为边界、风险、计划粒度、WBS/tasks 边界和 side-effect tier。
- [x] 更新 `docs/W3-ai-behavior/00-main.md`：AI 行为承接 eval、验收定义只读、fallback、non-goals 和工具副作用分级。
- [x] 更新 `docs/W4-build/00-main.md`：实现阶段承接小批量、任务契约、write scope、样本先行和返工控制。
- [x] 更新 `docs/W5-verify/00-main.md`：验证阶段承接质量平面、独立验证、证据闭环和 DoD 修订升级。
- [x] 更新 `docs/W6-release/00-main.md`：发布阶段承接 T2/T3 人审、发布候选边界、closeout、对外 claim 证据。
- [x] 更新 `docs/W7-operate/00-main.md`：运行阶段承接责任边界、runbook/alert/audit、升级队列和生产动作限制。
- [x] 更新 `docs/W8-learn/00-main.md`：学习阶段承接 closeout、最高影响下一步、失败分类账和结构性回写。
- [x] 更新 `docs/W9-maintain/00-main.md`：维护阶段承接记忆平面、handoff、source map/context pack、账本可恢复性。
- [x] 更新 `docs/sources/2026-07-08-small-project-management-operating-guide.md`：标注资料已纳入 W0-W9 主入口与触发专项正式规范。
- [x] 更新 `docs/sources/2026-06-23-source-map.md`：补充 2026-07-08 小型项目管理吸收关系和来源。
- [x] 重新运行 `python tools\verify_workflow_index.py .`。
- [x] 重新运行 `openspec validate --all`。
- [x] 检查无人值守生产发布、T2/T3、人审口径和 README 规范引用数量。

## 触发专项落地扩展

- [x] 阅读并更新 `docs/W1-discovery/01-product-analytics-experiment-standard.md`：数据证据、实验可信度、隐私边界和只读并行核查。
- [x] 阅读并更新 `docs/W2-openspec-risk/01-architecture-boundary-standard.md`：架构边界、ADR、write scope 和高影响架构人审点。
- [x] 阅读并更新 `docs/W2-openspec-risk/02-api-contract-compatibility-standard.md`：契约 DoD、breaking change、AI tool schema 和串行裁决。
- [x] 阅读并更新 `docs/W2-openspec-risk/03-security-auth-supply-chain-standard.md`：权限/租户/secret/供应链边界和升级队列。
- [x] 阅读并更新 `docs/W2-openspec-risk/04-cost-data-vendor-trust-boundary-standard.md`：成本、客户数据、供应商、IP、信任 claim 和 T3 边界。
- [x] 阅读并更新 `docs/W3-ai-behavior/01-prompt-eval-agent-workflow-standard.md`：prompt/eval 四件套、agent 升级和工具副作用分级。
- [x] 阅读并更新 `docs/W3-ai-behavior/02-ai-eval-safety-standard.md`：AI safety gate、红队样例、threshold 和 release decision。
- [x] 阅读并更新 `docs/W3-ai-behavior/03-ai-context-memory-retrieval-standard.md`：RAG/记忆来源、删除路径、untrusted context 和跨租户人审。
- [x] 阅读并更新 `docs/W3-ai-behavior/04-ai-runtime-routing-tools-standard.md`：模型路由、工具权限、预算背压、T2/T3 工具边界。
- [x] 阅读并更新 `docs/W4-build/01-go-kratos-sqlc-grpc-service-standard.md`：后端小批量、生成链、write scope 和生产副作用边界。
- [x] 阅读并更新 `docs/W4-build/02-vite-vercel-frontend-standard.md`：前端 surface 小批量、授权状态承接和 UI 不放大权限。
- [x] 阅读并更新 `docs/W4-build/03-data-migration-standard.md`：数据变更账本、expand/migrate/contract、T2/T3 数据动作。
- [x] 阅读并更新 `docs/W4-build/04-configuration-feature-flag-standard.md`：配置事实源、flag 清理、生产配置 T2 人审。
- [x] 阅读并更新 `docs/W4-build/05-dev-workspace-ai-coding-standard.md`：AI coding 任务契约、批次日志、write scope 和真实副作用禁止。
- [x] 阅读并更新 `docs/W4-build/06-external-side-effects-standard.md`：计费/webhook/通知幂等审计和外部副作用人审。
- [x] 阅读并更新 `docs/W4-build/07-async-job-worker-standard.md`：job contract、状态机、背压、死信回放和 AI Batch 隐私边界。
- [x] 阅读并更新 `docs/W5-verify/01-testing-quality-standard.md`：独立质量证据、DoD 修订、flaky/accepted risk 人审。
- [x] 阅读并更新 `docs/W5-verify/02-accessibility-ai-ux-standard.md`：AI UX、可访问性、关键任务、不可逆交互边界。
- [x] 阅读并更新 `docs/W5-verify/03-operational-risk-verification-standard.md`：性能/韧性 go-no-go、生产演练限制和降级证据。
- [x] 阅读并更新 `docs/W6-release/01-release-pipeline-standard.md`：release gate、发布候选边界、无人窗口不生产发布。
- [x] 阅读并更新 `docs/W6-release/02-customer-pilot-onboarding-launch-standard.md`：客户上线小项目、readiness gates、真实客户数据和 offboarding。
- [x] 阅读并更新 `docs/W6-release/03-external-claim-evidence-release-gate-standard.md`：claim evidence、公开承诺、AI 草稿不自动发布。
- [x] 阅读并更新 `docs/W7-operate/01-sre-lite-operations-standard.md`：SLO/runbook/incident、自动恢复限制和 24/7 人审。
- [x] 阅读并更新 `docs/W7-operate/02-admin-ops-action-standard.md`：admin action registry、R2/R3/R4、T3 永不 AI 自主执行。
- [x] 阅读并更新 `docs/W7-operate/03-security-privacy-incident-vulnerability-standard.md`：安全事故 first hour、通知判断和敏感证据边界。
- [x] 阅读并更新 `docs/W7-operate/04-credential-secret-lifecycle-standard.md`：credential metadata、轮换计划、AI 不接触真实 secret。
- [x] 阅读并更新 `docs/W8-learn/01-customer-support-trust-ops-standard.md`：支持闭环、最高影响下一步、退款/通知/数据请求人审。
- [x] 阅读并更新 `docs/W8-learn/02-ai-quality-regression-incident-standard.md`：AI 质量事故、失败分类回写、Q-SEV 人审。
- [x] 阅读并更新 `docs/W9-maintain/01-knowledge-context-recovery-standard.md`：context pack/docs map、账本可恢复、canonical source 人审。
- [x] 阅读并更新 `docs/W9-maintain/02-maintenance-dependency-debt-standard.md`：依赖/债务/弃用小批量、major upgrade 和自动 PR 边界。
- [x] 检查 30 个触发专项均存在 `## 专项承接 L0/L1 与小型项目管理` 段落。
- [x] 重新运行 `python tools\verify_workflow_index.py .`。
- [x] 重新运行 `openspec validate --all`。
- [x] 复查 README 引用数量、source map/context pack 引用关系和无人生产发布安全口径。
