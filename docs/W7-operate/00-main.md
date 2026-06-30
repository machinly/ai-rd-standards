# W7 Operate 核心规范

## W7 核心入口

本文件是 W7 Operate 的核心入口。进入 `docs/W7-operate/` 时先读它，再按触发条件读取 SRE-lite、观测性、备份恢复、后台运营、基础设施、事故响应或凭据生命周期专项。

W7 只回答一个问题：**发布或上线后，如何知道系统是否正常、坏了如何止血和恢复、哪些生产动作能被安全执行、哪些事故或凭据风险必须升级？**

W7 不是重做发布、补实现或重新定义承诺的地方。发布决策回 W6；验证证据回 W5；实现修复回 W4；契约、安全、成本、供应商或信任边界回 W2。

## 适用范围

适用：

- 生产 SLO、SLI、告警、runbook、incident、postmortem、toil 和运维复盘。
- traces、metrics、logs、AI telemetry、dashboard、trace correlation 和低基数遥测 schema。
- 备份、恢复、RPO/RTO、灾难演练、业务连续性、供应商故障和访问恢复。
- Admin console、support console、one-off command、break-glass、人工生产操作和审计日志。
- IaC、云环境、resource inventory、state、plan/apply、drift、destroy/decommission 和基础设施 emergency change。
- 安全/隐私事故、漏洞披露、供应商事件、AI 安全事故、客户/监管/供应商通知。
- API key、service account、webhook secret、TLS/private key、OpenAI/provider key、CI/OIDC identity 的 inventory、轮换和泄露复盘。

不适用：

- 是否开始或继续做某件事，回到 `docs/W0-intake/00-main.md`。
- 客户反馈和产品学习，进入 W8。
- 发布、上线、公开承诺和合同义务，回到 `docs/W6-release/00-main.md`。
- 测试、性能、可访问性和韧性门禁，回到 `docs/W5-verify/00-main.md`。
- 代码、配置、迁移、worker、billing、webhook、通知或开发者接口实现，回到 `docs/W4-build/00-main.md`。

## W7 最小产出

每个 W7 工作至少留下这些产出：

- 当前 target 的运行事实：SLO/SLI、dashboard、runbook、release watch、alert 或 incident record 中适用项。
- 可定位证据：trace/log/metric/request id/audit event/rotation run/recovery drill 的引用，不保存 secret、完整个人数据或 raw prompt/response。
- 恢复或止血路径：rollback、feature flag、kill switch、credential revoke、tenant isolation、restore runbook、admin action 或 provider escalation。
- 人工生产动作的边界：action registry、dry-run、approval、audit、rollback/compensate。
- 事故或异常的下一步：修复、回滚、客户通知、供应商通知、W8 质量/学习回路、W9 evidence package。

## 人工判断点

默认不问：

- dashboard 名称、低风险 runbook 文案、只读告警、低风险 staging 演练、普通字段顺序。

必须人工判断：

- 是否承诺或触发 24/7、合同 SLA、客户通知、监管通知、公开状态页或安全 advisory。
- 是否执行生产恢复、PITR、覆盖生产、丢弃数据、恢复含个人/资金/权限/审计/AI trace 的数据。
- 是否允许 break-glass、跨租户访问、用户 impersonation、R2/R3/R4 admin action、生产 SQL、退款/credit、删除或批量修复。
- 是否对 production IaC 执行 create/replace/destroy、IAM 扩权、public ingress、state 操作、force unlock、资源导入或 decommission。
- 是否接受未验证备份、不可行动告警、无法回滚、缺少审计、无法撤销旧凭据、疑似 secret 泄露或高危漏洞暂不处理。
- 是否涉及个人数据、客户内容、生产凭证、支付/健康/儿童/金融数据、跨租户、AI agent 越权、RAG/记忆泄露或供应商数据事件。

## 触发型专项

只在触发条件出现时读取对应文件：

- SLO、告警、runbook、incident、postmortem、toil、发布后 watch：`docs/W7-operate/01-sre-lite-operations-standard.md`
- metrics、traces、logs、dashboard、OpenTelemetry、AI trace、低基数 schema：`docs/W7-operate/02-observability-telemetry-standard.md`
- 备份、恢复、RPO/RTO、restore drill、业务连续性、供应商故障：`docs/W7-operate/03-backup-recovery-continuity-standard.md`
- Admin/support console、人工生产动作、dry-run、break-glass、审计日志：`docs/W7-operate/04-admin-ops-action-standard.md`
- IaC、环境拓扑、云资源、state、plan/apply、drift、destroy/decommission：`docs/W7-operate/07-infra-iac-environment-standard.md`
- 安全/隐私事故、漏洞披露、通知矩阵、AI 安全事故、advisory：`docs/W7-operate/05-security-privacy-incident-vulnerability-standard.md`
- 凭据、密钥、服务账号、rotation、exposure review、OpenAI/provider key：`docs/W7-operate/06-credential-secret-lifecycle-standard.md`

常见跨 W 触发：

- 用户或客户反馈进入产品决策：进入 W8。
- AI 质量回归或线上输出事故：进入 `docs/W8-learn/02-ai-quality-regression-incident-standard.md`。
- 审计证据包、长期证据保全或 trust center 证据：进入 `docs/W9-maintain/03-audit-evidence-compliance-standard.md`。
- 新合同/SLA/公开声明或客户上线承诺：回到 `docs/W6-release/00-main.md`。

## 进入 W8 或 W9 的出口

W7 完成后通常不直接结束，而是选择一个出口：

- 线上信号、事故、支持、客户反馈、AI 质量或使用数据改变下一步：进入 W8。
- 需要沉淀 runbook、context pack、freshness、audit evidence、dependency/debt 或长期维护：进入 W9。
- 需要发布修复：回到 W6。
- 需要补验证：回到 W5。
- 需要实现修复：回到 W4。
- 需要改变风险边界、供应商、权限、安全或承诺：回到 W2。

## W7 完成检查

- 当前 W7 目录只有一个 `00-main.md` 作为核心入口。
- 所有其它 W7 文件都是触发型专项，并在开头说明不是主入口。
- 入口、索引和 source map 都指向 `docs/W7-operate/00-main.md` 与带目录内顺序编号前缀的语义化专项文件名。
- 没有未编号专项文件、`core-*` wrapper 或只用旧“阶段 NN”作主身份的正文。
- `python tools\verify_workflow_index.py .` 通过。
