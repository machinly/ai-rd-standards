# 运行

本项目规定生产服务进入持续运行后的最小控制面：可观测性、SLO、告警与事故响应、恢复、人工生产动作、凭据、安全事件、异步任务、支持及 AI 质量与降级。目标是一人可执行、可停止、可回滚并能留下证据；不得以平台化建设代替真实运行准备。

## 项目目的与边界

<!-- rule-id: OPERATION-SCOPE-002 -->
是否开始或继续一项工作，回到[选题](../01-initiation/01-topic-selection.md)判断；涉及新合同、SLA、对外声明或客户上线承诺时，不在运行项继续判定，应转回[发布](../03-engineering-delivery/09-release.md)；风险边界、供应商、权限、安全或承诺发生变化时回到[技术设计](../03-engineering-delivery/05-technical-design.md)。

<!-- rule-id: OPERATION-SCOPE-003 -->
本项目是运行工作的唯一核心入口：进入运行后先读本规范，再按触发条件读取专项。SLO、告警、runbook、incident、observability、IaC drift、基础设施运行准备，以及安全事件、后台动作、凭据等专项均为触发型材料；它们不是默认流程，与本规范的正式分类及项目原则冲突时以正式规范为准。

<!-- rule-id: OPERATION-SCOPE-004 -->
dashboard 名称、低风险 runbook 或 ticket 文案、只读告警、低风险 staging 演练、模板小字段与字段顺序，以及无生产数据访问的本地实验不需要升级决策。企业级 PAM、SIEM、SOAR、ITSM 职责分离、HSM、secret zero、多云 KMS 等能力，仅在合规或客户要求出现后单独开 change。

<!-- rule-id: OPERATION-SCOPE-005 -->
每个运行工作至少留下当前 target 适用的运行事实，包括 SLO/SLI、dashboard、runbook、release watch、alert 或 incident record；第一个真实服务必须建立对应 `ops/` 工件，并由仓库核验命令检查。

<!-- rule-id: OPERATION-SCOPE-006 -->
运行完成后必须选择后续出口：客户反馈、线上信号、事故、支持、AI 质量或使用数据改变下一步时进入[评估](11-evaluation.md)；需要沉淀 runbook、context pack、freshness、dependency/debt 或长期维护时同样由评估决定，形成长期证明时转交[验证](../03-engineering-delivery/08-verification.md)保存证据。

<!-- rule-id: OPERATION-PLATFORM-001 -->
默认采用托管监控和供应商能力，并以 OpenTelemetry 语义接入；具体 backend 可选托管云监控、Grafana/Prometheus、供应商 APM 或日志平台，由真实部署环境决定。多区域高可用、Kubernetes 平台、完整 PagerDuty 排班、复杂容量模型、全量 FinOps 或 SOC 2/ISO 体系，仅在收入、规模或合同义务出现后单独立项。

<!-- rule-id: OPERATION-INFRA-001 -->
IaC、环境拓扑、云资源清单、state、plan/apply、drift、destroy/decommission 与 emergency change 纳入运行准备。`ops/infra/<service>.md` 必须记录环境、region、runtime、state backend、关键云资源、public exposure、`backup_required` 与 drift 处理；production create/replace/destroy、IAM 扩权、public ingress、state 操作、force unlock、资源导入或 decommission 必须进入人工判断。

## 根本原则

- **ITEM-OPERATION-001**：没有付费关键路径或合同 SLA 时，不默认全天候值守；出现合同 SLA、付费关键流程或高损失场景时，必须由人确认更高保障目标。

## 核心判断

<!-- rule-id: OPERATION-HUMAN-001 -->
无法回滚、缺少审计、自动回滚或自动降级/关闭用户功能，以及涉及数据删除、资金、权限、隐私或安全事件的决定，必须由人确认并记录接受、停止、回滚或升级结论。

<!-- rule-id: OPERATION-AVAILABILITY-001 -->
没有付费关键路径或合同 SLA 时，运行基线为外部 uptime 检查、营业时间告警、runbook 与可回滚发布；不默认承诺 24/7、专属支持或更短响应时间，以保护一人公司的注意力和健康。

<!-- rule-id: OPERATION-AVAILABILITY-002 -->
出现合同 SLA、付费关键流程或高损失场景时，必须由人确认更高可用性与响应目标，并明确是否接受为此增加云成本。

## 重新组织后的规范要求

### SLO、可观测性与告警

<!-- rule-id: OPERATION-SLO-001 -->
每个生产服务或关键 workflow 必须先定义并维护用户可见的 SLO/SLI，再补观测；第一版只设 1—2 个可行动 SLO。没有用户路径时，改用最关键后台结果的 freshness 或 correctness SLO。

<!-- rule-id: OPERATION-SLO-002 -->
早期用户可见 MVP 可从 `99.5% monthly availability` 开始讨论，但它不是自动承诺。正式 SLO 必须可计算；暂不可测时只记录采集计划，不得把不可测目标写成正式 SLO。

<!-- rule-id: OPERATION-SLO-003 -->
SLO、SLI 与 error budget policy 的最小仓库工件为 `ops/slo/<service>.json`，并关联 `ops/runbooks/<service>.md`；SLO JSON 应采用来源示例所定义的服务、窗口、指标、目标、数据源、error budget 与行动字段结构。

<!-- rule-id: OPERATION-OBSERVE-001 -->
每个服务必须覆盖四类黄金信号：latency 按 RPC/endpoint 分成功与失败并优先观察 p95 或 p99；traffic 记录请求量、任务量或关键 workflow 次数；errors 覆盖协议错误、业务失败、依赖失败及 parse/schema 失败；saturation 覆盖 CPU、内存、连接池、队列长度、数据库连接或第三方 rate limit。

<!-- rule-id: OPERATION-OBSERVE-002 -->
`ops/observability/<service>.md` 说明 traces、metrics、logs、AI telemetry、dashboard、trace correlation 与低基数 schema。遥测的通用语义和导出协议默认采用 OpenTelemetry；只要求产生可关联信号，不要求自建完整观测平台。

<!-- rule-id: OPERATION-OBSERVE-003 -->
新服务至少提供 health check；依赖数据库、外部 API 或关键配置时还要表达 readiness。服务必须为 latency、traffic、errors、saturation 指定信号落点，error model 记录 Observability，启动日志包含服务名。

<!-- rule-id: OPERATION-OBSERVE-004 -->
上线 AI 能力必须记录身份与版本维度：model、`ai_feature`、prompt version 与 schema version；同时记录 latency、traffic、errors、saturation、tool failure rate、structured output parse failure rate、fallback、rollback、human review rate，以及 token/cost 估计或采集计划。AI telemetry 至少持续保留这些版本、失败率与成本字段。

<!-- rule-id: OPERATION-OBSERVE-005 -->
模型 route policy 必须包含 Telemetry；model registry 必须包含 `latency_slo` 与 telemetry。延迟超 SLO 属于 failure mode；Feature Flag 清单、每个 flag 及 AI route flag 都必须记录 observability。

<!-- rule-id: OPERATION-ALERT-001 -->
告警分为 `page` 与 `ticket`：`page` 只用于用户可见、正在发生且人能立即处置的问题；非紧急、用户不可见或不能立即行动的信号进入 `ticket`。每条告警必须回答“现在能做什么”；连续两次误报或无法行动的 page 必须降级或修改条件，接受不可行动告警须由人决定。

<!-- rule-id: OPERATION-ALERT-002 -->
`page` 必须写明 condition、impact、runbook 与 rollback，并关联含诊断、缓解和回滚步骤的 runbook；没有 runbook 的告警默认不得升级为 page。

<!-- rule-id: OPERATION-RUNBOOK-001 -->
成本专项、integration delivery 与 messaging delivery 均必须有可执行 runbook；后两者默认分别位于 `integrations/delivery-runbook/<target>.md` 与 `messaging/delivery-runbook/<target>.md`。

<!-- rule-id: OPERATION-HANDOFF-001 -->
发布流水线必须包含 observability 动作并引用 `ops/slo/<service>.json`、`ops/runbooks/<service>.md` 与 `release/<service>-checklist.md`；post-deploy 适用的 SLO、alert 与生产服务运行工件必须移交运行和评估持续维护。

### 事故、恢复与备份

<!-- rule-id: OPERATION-INCIDENT-001 -->
事故响应采用一人可执行的轻量顺序：先宣告并写明时间、影响、响应入口和当前假设；随后在工作记录中逐项记录关键动作及结果；止血后再说明用户影响并复盘。紧急止血本身不需要先创建 OpenSpec change。

<!-- rule-id: OPERATION-INCIDENT-002 -->
默认等级为：大量用户不可用、数据损坏、资金/权限/隐私风险或合同 SLA 风险为 `SEV1`；核心路径部分失败或明显性能退化为 `SEV2`，必须当天处理；小范围影响或内部工具失败为 `SEV3`，可进入普通修复。

<!-- rule-id: OPERATION-INCIDENT-003 -->
事故索引与记录分别放在 `incidents/README.md` 和 `incidents/YYYY-MM-DD-<slug>.md`。记录以 `Incident: <title>` 开始，包含 `Timeline`，并至少填写 Date、Severity、Service、User impact、Detection 与 Resolution。

<!-- rule-id: OPERATION-INCIDENT-004 -->
事故下一步必须明确修复、回滚、客户/供应商通知、评估中的质量与学习回路，或验证中的 evidence package。24/7、合同 SLA、客户或监管通知、公开状态页、安全 advisory 与事后说明均不得隐含承诺，必须单独判断。

<!-- rule-id: OPERATION-INCIDENT-005 -->
AI fallback runbook 必须包含 `Post-Incident Review`，将降级原因、用户影响、恢复验证与后续改进闭环。

<!-- rule-id: OPERATION-RECOVERY-001 -->
每条关键路径必须选择可用的止血或恢复方式：rollback、feature flag、kill switch、credential revoke、tenant isolation、restore runbook、admin action 或 provider escalation。涉及 schema migration、权限、资金或 AI 自动副作用时，必须有 rollback 或 disable switch；处置优先按回滚、关 flag、降级、限流或切换依赖缩小影响。

<!-- rule-id: OPERATION-RECOVERY-002 -->
`ops/recovery/<service>.md` 是备份、恢复、RPO/RTO、灾难演练、业务连续性与供应商故障的最小记录，必须列出关键资产、RPO/RTO、备份来源、restore steps、验证命令及下一次演练日期。

<!-- rule-id: OPERATION-RECOVERY-003 -->
生产恢复、PITR、覆盖生产、丢弃数据，以及恢复含个人、资金、权限、审计或 AI trace 的数据必须人审；destroy/decommission、IAM 扩权、public ingress 与 state 操作同样不得自动放行。

<!-- rule-id: OPERATION-BACKUP-001 -->
生产数据服务默认启用托管自动备份和 snapshot；高价值数据另保留手动 snapshot 或 dump。备份文件与 restore 权限必须最小化，备份文件必须加密。

<!-- rule-id: OPERATION-BACKUP-002 -->
data change JSON 的 `backup` 配置块必须记录 `required`、`method`、`restore_tested`。生产迁移前确认最新备份可用；高风险变更只有在近期存在恢复演练证据，或恢复步骤当场可执行时才能继续；data fix 记录必须包含 `Backup`。

<!-- rule-id: OPERATION-BACKUP-003 -->
每个生产数据服务维护 `data/restore/<service>.md`，包含 `Backup Sources`、`Restore Steps`、`Validation` 与 `Last Drill`。有付费用户或关键数据后，每月或每季度执行一次 restore drill。

### 安全事件、漏洞与审计

<!-- rule-id: OPERATION-SECURITY-001 -->
安全事故专项仅在攻击、数据、隐私、漏洞披露、合同通知或生产安全影响出现时触发；普通可用性事故留在通用事故流程。每个 target 至少维护 `security-incidents/response-plan/<target>.md`、`incident-register/<target>.json` 和 `vulnerability-disclosure/<target>.md`。不默认建设 24/7 SOC、SIEM、SOAR、bug bounty 或 CNA/PSIRT，但密钥泄露、正在利用、跨租户、个人数据、客户生产影响及支付/权限/删除动作必须能叫醒负责人。

<!-- rule-id: OPERATION-SECURITY-002 -->
`security-incidents/response-plan/<target>.md` 必须以 `<target> Security Incident Response Plan` 为标题，并包含 Scope、Severity Model、Intake Channels、First Hour、Containment、Evidence Preservation、Investigation、Customer / Vendor / Regulator Notification、Recovery、Communications、AI-Specific Incidents、Linked Artifacts 与 Review Cadence。

<!-- rule-id: OPERATION-SECURITY-003 -->
安全事故 First Hour 依次确认范围、冻结易变或可能丢失的证据、关闭或限流可阻断的攻击入口、限制受影响权限并创建事故记录。

<!-- rule-id: OPERATION-SECURITY-004 -->
Containment 应选择能安全缩小暴露面的最小措施：kill switch、关闭 feature flag、限流、租户隔离、禁用 connector、冻结 webhook、回滚部署或关闭高风险 AI tool。

<!-- rule-id: OPERATION-SECURITY-005 -->
Evidence Preservation 只保留足以调查的引用或脱敏证据，不保存 secrets、原始个人数据、完整 prompt/response、攻击 payload 或支付数据。

<!-- rule-id: OPERATION-SECURITY-006 -->
`security-incidents/incident-register/<target>.json` 顶层必须包含 `target`、`owner`、`intake_channels`、`severity_model`、`incidents`、`dependencies`、`evidence_policy`、`human_checkpoint`、`review_cadence` 与 `status`；每个 `incidents[]` 元素还必须有 `owner` 和 `status`。

<!-- rule-id: OPERATION-SECURITY-007 -->
每个安全事故条目还必须包含 `id`、`detected_at`、`source`、`category`、`severity`、`summary`、`affected_assets`、`affected_data`、`tenant_scope`、`containment`、`evidence_refs` 与 `notification_refs`。

<!-- rule-id: OPERATION-SECURITY-008 -->
`incidents[].category` 默认允许：`credential_exposure`、`unauthorized_access`、`tenant_isolation`、`personal_data_breach`、`sensitive_data_disclosure`、`dependency_vulnerability`、`supply_chain_compromise`、`ai_prompt_injection`、`ai_tool_misuse`、`rag_data_leak`、`model_or_provider_incident`、`admin_action_error`、`webhook_or_integration_abuse`、`payment_or_billing_security`、`availability_attack`。

<!-- rule-id: OPERATION-SECURITY-009 -->
安全事故登记的 `incidents[].severity` 使用闭集 `sev0`、`sev1`、`sev2`、`sev3`。

<!-- rule-id: OPERATION-SECURITY-010 -->
正在被利用、跨租户或大量个人数据、生产凭证外泄、资金/删除/权限高风险动作归为 `sev0`；单租户或有限数据暴露、可复现高危漏洞、影响生产的供应商事故、暴露公网的 critical CVE 归为 `sev1`；中等漏洞、可控敏感日志泄露或无利用证据但有明确攻击路径归为 `sev2`；低风险报告、误报、已隔离非生产问题或 defense-in-depth 缺口归为 `sev3`。

<!-- rule-id: OPERATION-SECURITY-011 -->
`security-incidents/notification-matrix/<target>.json` 必须包含 `target`、`owner`、`jurisdictions_or_contracts`、`notification_triggers`、`notification_deadlines`、`recipient_classes`、`message_templates`、`vendor_processor_contacts`、`customer_contacts_policy`、`regulator_contacts_policy`、`legal_review`、`human_checkpoint` 与 `status`。

<!-- rule-id: OPERATION-SECURITY-012 -->
不得把“72 小时”“30 天”“60 天”或“4 个工作日”等写成通用通知承诺；期限必须按适用法域、合同、客户类型及组织角色分别判断。

<!-- rule-id: OPERATION-SECURITY-013 -->
通知只陈述事实：发生了什么、何时发现、影响范围、已采取措施、用户需要做什么及下一次更新时间；不得猜测、淡化或过度承诺。客户、监管、供应商与公开状态页消息分别登记，不得混为一份。

<!-- rule-id: OPERATION-SECURITY-014 -->
涉及个人或敏感数据、儿童/健康/金融/支付数据、供应商处理方、企业 SLA/DPA/安全附件、监管或公开披露义务时必须人审；First Hour 要判断是否需要客户、供应商、平台、执法、律师、保险或取证协助。接受高危漏洞暂不修复、延迟通知、继续运行受影响功能或公开漏洞细节也必须人审；可能触发法律、监管或客户重大通知的事件按 `sev0` 处理。

<!-- rule-id: OPERATION-SECURITY-015 -->
统一安全 audit event 必须包含 `event_id`、`timestamp`、`actor_id`、`tenant_id`、`request_id`、`trace_id`、`source_ip_hash`、`action`、`resource`、`outcome` 与 `reason`。可选表 `security_incidents`、`incident_events`、`vulnerability_reports`、`containment_actions`、`notification_decisions`、`incident_evidence_refs` 使用 sqlc 生成类型安全查询。

<!-- rule-id: OPERATION-SECURITY-016 -->
AI 安全事故按风险入口处置：高风险工具先禁用，模型/路由先降级，污染或泄露的 RAG source 先关闭，memory 写入先冻结，connector 先限制；无法安全自动处置时启用人工审核。

<!-- rule-id: OPERATION-SECURITY-017 -->
分级前必须检查个人数据、客户内容、生产凭证、支付/健康/儿童/金融数据、跨租户、AI agent 越权、RAG/记忆泄露与供应商数据事件，并检查是否正在利用、进入 CISA KEV、存在公开 PoC、影响公网入口或可触发权限/资金/删除动作。

<!-- rule-id: OPERATION-VULN-001 -->
`security-incidents/vulnerability-disclosure/<target>.md` 必须以 `<target> Vulnerability Disclosure` 为标题，并包含 Scope、Contact、Safe Harbor / Authorization Boundary、In Scope、Out of Scope、Report Requirements、Triage And Acknowledgement、Remediation And Disclosure Timeline、CVE / Advisory Policy、Researcher Communication 与 Review Cadence。

<!-- rule-id: OPERATION-VULN-002 -->
应先让外部报告者能通过最小安全渠道联系，再评估是否运营 bug bounty；没有预算与 triage 能力时不得承诺奖励。授权边界必须排除会破坏服务或侵害他人的测试，包括社工、物理攻击、数据外传、隐私侵犯、DoS、大规模扫描、绕过付费和访问他人数据。

<!-- rule-id: OPERATION-VULN-003 -->
有效报告必须确认收到、完成复现与分级，并给出修复计划和披露窗口；无法修复时记录风险接受。公共产品漏洞必要时考虑 CVE/advisory；接受高危漏洞暂不处理必须由人决定。

<!-- rule-id: OPERATION-AUDIT-001 -->
跨租户、support/admin 与 break-glass 访问必须审计；最小 schema 工件为 `admin-ops/audit-log-schema/<target>.json`。

<!-- rule-id: OPERATION-BREAKGLASS-001 -->
`admin-ops/break-glass/<target>.md` 是 admin/support console、one-off command 与人工紧急生产访问的最小工件，必须包含 Scope、Triggers、Access Grant、Time Limit、Allowed Actions、Forbidden Actions、Logging、Communication 与 Review。

<!-- rule-id: OPERATION-BREAKGLASS-002 -->
break-glass 只用于 SEV、数据恢复、安全事件、账号锁定、供应商故障或无法经常规权限恢复用户的情形，不得作为日常操作捷径。

<!-- rule-id: OPERATION-BREAKGLASS-003 -->
break-glass 必须限时，并在文档中包含 Revoke；访问结束立即撤销。每次使用后执行 review，并补齐暴露出的 action registry 或 runbook 缺口。

## 按主题整理的执行细则

### 人工生产动作与 break-glass

<!-- rule-id: OPERATION-ADMIN-001 -->
后台操作视为产品代码管理。内部 admin/support console、运营脚本、one-off command、后台 job 与数据修复工具，只要会改变用户数据、权限、租户、计费权益、退款/credit、feature flag、配置、AI workflow、生产依赖或外部通知，就必须使用同一 `<target>` 维护 `admin-ops/action-registry/<target>.json`、`operator-playbook/<target>.md` 与 `ops-review/<target>.md`，覆盖 dry-run、approval、audit、rollback/compensate。正式 migration/backfill 的执行规范另管，但其人工审批仍在本项目内。

<!-- rule-id: OPERATION-ADMIN-002 -->
任何未注册动作不得进入生产 admin UI、support tool、agent tool 或运营脚本；执行前必须确认该动作已在 action registry 登记。

<!-- rule-id: OPERATION-ADMIN-003 -->
动作风险使用闭集：`R0-readonly` 为不涉及敏感数据和跨租户的只读；`R1-low` 为单用户低风险状态变更；`R2-sensitive` 涉及付费、权益、个人数据、AI 输出补救或生产配置；`R3-destructive` 涉及删除、批量修复、跨租户、退款/credit、权限、外部通知或直接写生产数据；`R4-break-glass` 为绕过常规权限或紧急生产访问。

<!-- rule-id: OPERATION-ADMIN-004 -->
`R1-low` 可自动化但必须审计；`R2-sensitive` 必须 human checkpoint；`R3-destructive` 必须先 dry-run、获批准并具备回滚或补偿计划；`R4-break-glass` 只授予限时访问并全量审计。

<!-- rule-id: OPERATION-ADMIN-005 -->
`admin-ops/operator-playbook/<target>.md` 必须包含 Scope、When To Use、Preconditions、Dry Run、Execute、Verify、Rollback / Compensate、Abort / Escalation、Communication 与 Linked Artifacts。

<!-- rule-id: OPERATION-ADMIN-006 -->
执行任何 admin action 前必须确认当前 actor 对目标、租户与动作均有权限。

<!-- rule-id: OPERATION-ADMIN-007 -->
能够 dry-run 的后台动作不得直接执行；dry-run 或 precheck 必须列出影响对象、数量、受影响租户、金额、权限影响与外部副作用。

<!-- rule-id: OPERATION-ADMIN-008 -->
实际执行必须从最小范围开始：单租户、单用户、单批次，并保持可停止。

<!-- rule-id: OPERATION-ADMIN-009 -->
执行后必须验证用户影响、数据一致性、审计事件、告警与回滚点。

<!-- rule-id: OPERATION-ADMIN-010 -->
关闭或补偿动作时，必须记录结果、失败、回滚、credit、用户沟通及后续 action。

<!-- rule-id: OPERATION-ADMIN-011 -->
批量生产数据修复、真实生产 backfill、生产数据或跨租户访问、impersonation、break-glass、R2/R3/R4 动作、生产 SQL/脚本/REPL/一次性 job，以及让 AI 或 agent 获得生产写权限，均必须人工判断。

<!-- rule-id: OPERATION-ADMIN-012 -->
AI 可以协助调查、归类、生成 dry-run plan、解释风险和草拟记录，但不得自主退款、删除、改权限、跨租户访问、发外部通知、改生产配置或执行 break-glass；AI 触发的任何写操作必须产生 audit event。

<!-- rule-id: OPERATION-ADMIN-013 -->
租户上线涉及 admin action 时，必须经过本运行项目中后台运营专项的审批、dry-run、rollback 与 audit log 控制。

### 配置、纠正与受控副作用

<!-- rule-id: OPERATION-CONFIG-001 -->
配置 runbook 必须包含 Scope、Change Procedure、Validation、Rollback、Drift Detection 与 Human Checkpoints。

<!-- rule-id: OPERATION-CONFIG-002 -->
配置 runbook 默认位于 `config/runbooks/<target>.md`。所有生产配置变更必须有 rollback；高风险开关必须有 kill switch 或不适用说明；ops toggle、kill switch 及 worker degradation/kill switch 均必须写入 runbook。

<!-- rule-id: OPERATION-CLAIM-001 -->
每个 production target 必须维护 correction runbook，包含 title、Scope、Trigger Conditions、Triage、Surfaces To Update、Customer / Developer Notice、Contract / Support Handling、Evidence Preservation、Rollback / Mitigation、Owner And Timeline 与 Review Cadence。

<!-- rule-id: OPERATION-CONTENT-001 -->
内容审核必须有执行手册，默认位于 `content-safety/enforcement-runbook/<surface>.md`。

<!-- rule-id: OPERATION-EXPERIMENT-001 -->
实验必须发送 exposure event；仅处于 eligible group 不等于已 exposure。

<!-- rule-id: OPERATION-EXTERNAL-001 -->
执行真实外部副作用或绕过消息保护控制必须人工判断。

<!-- rule-id: OPERATION-CUSTOMER-001 -->
客户上线工件的 `rollback_or_offboarding` 必须说明如何撤销 flag。

### 异步任务与 worker

<!-- rule-id: OPERATION-JOB-001 -->
只有 job type 完成生产登记后，异步任务才可投入运行；prompt、tool、admin action、webhook 与 cron 均不得启动未登记类型。

<!-- rule-id: OPERATION-JOB-002 -->
worker runbook 默认位于 `async-jobs/worker-runbook/<target>.md`，必须包含 Scope、Start/Shutdown、Enqueue、Dequeue/Lease、Execute、Cancellation、Dead Letter/Replay、Incident Actions 与 Linked Artifacts。

<!-- rule-id: OPERATION-JOB-003 -->
`max_attempts` 必须有限；job contract 包含 `dead_letter_policy`，默认状态机包含 `dead_lettered`。重试耗尽、不可重试或风险错误进入 dead letter，并经明确 replay 审查；高风险 job 必须有死信路径。每次尝试记录 retry decision；副作用自动重试、回放、backfill、定时写或跨租户批处理必须人审。

<!-- rule-id: OPERATION-JOB-004 -->
worker 抢占 job 必须在事务中按 deterministic order 使用 lease 或 lock。

<!-- rule-id: OPERATION-JOB-005 -->
每次尝试必须记录 attempt、开始与结束时间、错误分类、queue age、duration、worker id 与结果引用。

<!-- rule-id: OPERATION-JOB-006 -->
收到 shutdown 后停止领取新 job；当前 job 必须完成或释放/等待 lease 过期，进程退出不得丢失隐式内存状态。

<!-- rule-id: OPERATION-JOB-007 -->
job registry 必须包含 telemetry；每个 queue 定义 `backlog_slo` 与 `oldest_age_slo`；高风险 job 具有观测字段，worker runbook 包含 Observability。

<!-- rule-id: OPERATION-JOB-008 -->
删除或回放死信、修复 stuck job、补偿重复副作用或公开事故必须人工判断。

### 凭据与 secret 生命周期

<!-- rule-id: OPERATION-CREDENTIAL-001 -->
API key、service account、webhook secret、TLS/private key、OpenAI/provider key、CI/OIDC identity、短期 token、mTLS cert、AI connector/MCP token 与 break-glass credential 都进入 credential lifecycle。适用范围包括 Go/Kratos/sqlc/gRPC 服务、Vite 前端、AI workflow、worker、webhook、admin/support 工具及 local/preview/staging/production。每个生产 target 至少维护 `credentials/inventory/<target>.json`；普通配置和 flag 仍归配置专项，整体安全基线仍归[技术设计](../03-engineering-delivery/05-technical-design.md)。

<!-- rule-id: OPERATION-CREDENTIAL-002 -->
凭据工件只记录 metadata，不记录 secret value。

<!-- rule-id: OPERATION-CREDENTIAL-003 -->
`credentials/inventory/<target>.json` 顶层必须包含 `target`、`owner`、`environments`、`credentials`、`storage_locations`、`injection_paths`、`detection_controls`、`linked_artifacts`、`human_checkpoint`、`review_cadence` 与 `status`。

<!-- rule-id: OPERATION-CREDENTIAL-004 -->
inventory 顶层还必须有 `rotation_defaults`；每个 `credentials[]` 元素必须包含 `id`、`type`、`purpose`、`issuer`、`environment`、`consumer`、`scope`、`storage_ref`、`injection_method`、`rotation_interval`、`expires_on`、`last_rotated`、`revocation_path`、`blast_radius` 与 `status`。

<!-- rule-id: OPERATION-CREDENTIAL-005 -->
`credentials[].type` 只能从闭集中取值；按字典序列出为 `api_key`、`ci_token`、`database_password`、`encryption_key`、`jwt_signing_key`、`mcp_connector_token`、`oauth_client_secret`、`other`、`service_account`、`tls_private_key`、`webhook_signing_secret`。

<!-- rule-id: OPERATION-CREDENTIAL-006 -->
凭据 `scope` 应保持最小权限、单环境、单用途；production 与 staging 默认使用不同 key/project。

<!-- rule-id: OPERATION-CREDENTIAL-007 -->
OpenAI/API provider key 必须记录 project、rate/spend guard、owner、usage monitoring 及是否暴露到前端。内部 service account/token/mTLS、AI connector/MCP token、tool runtime token、provider key 与 sandbox credential 均进入 inventory，并记录 scope、approval、revocation path 与 data boundary。

<!-- rule-id: OPERATION-CREDENTIAL-008 -->
无法确定 `last_rotated` 时必须显式写 `unknown`。

<!-- rule-id: OPERATION-CREDENTIAL-009 -->
API key、service account、webhook secret、TLS/private key、OpenAI/provider key 与 CI/OIDC identity 都必须有轮换路径；`revocation_path` 必须让事故中的操作者能直接找到 dashboard、CLI、API、runbook 或 vendor support 撤销入口。

<!-- rule-id: OPERATION-CREDENTIAL-010 -->
`credentials/access-policy/<target>.md` 必须以 `<target> Credential Access Policy` 为标题，并包含 Scope、Identities And Roles、Least Privilege、Storage And Injection、CI / CD、Local Development、Frontend Boundary、Audit And Monitoring、Human Checkpoints 与 Review Cadence。本地开发使用 `.env.local` 或开发 secret manager，且不得复用 production secret；访问日志至少回答哪个人或 workload 在何时读取了哪个 secret reference。

<!-- rule-id: OPERATION-CREDENTIAL-011 -->
没有 OIDC 时，长期 secret 必须可轮换；production secret 默认只允许 runtime identity、deploy identity 与 break-glass owner 访问。

<!-- rule-id: OPERATION-CREDENTIAL-013 -->
所有 `VITE_*` 值都视为公开信息；前端构建日志、preview 环境变量、错误上报与 analytics event 不得含 token、key、cookie、Authorization header 或 connection string。

<!-- rule-id: OPERATION-CREDENTIAL-014 -->
凭据轮换至少维护 `credentials/rotation-plan/<target>.md` 与 `credentials/rotation-run/<target>.json`。rotation plan 以 `<target> Credential Rotation Plan` 为标题，并包含 Scope、Credentials、Preconditions、Dual-Key Or Version Strategy、Steps、Validation、Rollback、Revocation、Communication、Evidence、Human Checkpoints 与 Review Cadence。

<!-- rule-id: OPERATION-CREDENTIAL-015 -->
长期 deploy token 必须有 owner 与轮换计划。无法双 key 的凭据安排低流量窗口并准备 rollback path；JWT signing key、webhook signing secret 与 encryption key 必须定义 old/new overlap 及 `kid` 或 version。

<!-- rule-id: OPERATION-CREDENTIAL-016 -->
轮换计划不要求每月轮完所有 key；优先处理 blast radius 最大、最久未轮换、owner 不明、疑似泄露或涉及离职/权限变化的凭据，`last_rotated: unknown` 必须列为第一优先级。

<!-- rule-id: OPERATION-CREDENTIAL-017 -->
production key 的轮换或撤销、暂停旧版本、临时共享 secret、允许旧 key 继续有效，以及无法轮换、无法撤销、无法确认泄露、owner 不明或 staging/production 不可区分，均必须 human checkpoint；OpenAI/provider key、支付、数据库、JWT/encryption key、TLS/private key、CI deploy token 与 break-glass credential 一律纳入该判断。

<!-- rule-id: OPERATION-CREDENTIAL-018 -->
`credentials/rotation-run/<target>.json` 必须包含 `target`、`owner`、`date`、`environment`、`credential_refs`、`reason`、`steps`、`validation`、`downtime`、`user_impact`、`revoked_old_versions`、`evidence_refs`、`decision`、`gaps`、`actions`、`human_checkpoint` 与 `status`。

<!-- rule-id: OPERATION-CREDENTIAL-019 -->
rotation run 的 `decision` 只能取 `pass`、`pass_with_notes`、`needs_fix`、`abort`、`accepted_risk`、`defer`。

<!-- rule-id: OPERATION-CREDENTIAL-020 -->
旧版本未撤销，或 `decision` 为 `accepted_risk`、`defer`、`abort`、`needs_fix` 时，必须记录 `human_checkpoint`、`gaps` 与 `actions`。

<!-- rule-id: OPERATION-CREDENTIAL-021 -->
rotation run 的每个 `steps` 项必须同时记录动作摘要与动作结果。

<!-- rule-id: OPERATION-CREDENTIAL-022 -->
疑似 secret 泄露必须人工判断；credential exposure 的 First Hour 优先撤销并轮换受影响凭据。

<!-- rule-id: OPERATION-CREDENTIAL-023 -->
`credentials/exposure-review/<target>.md` 必须以 `<target> Credential Exposure Review` 为标题，并包含 Scope、Detection Sources、Findings、Active Exposure、Revocation Actions、User / Customer Impact、Evidence、Preventive Controls、Action Items、Human Checkpoints 与 Review Cadence。

<!-- rule-id: OPERATION-CREDENTIAL-024 -->
`Findings` 只能保存 alert id、commit hash、file path、line reference、provider key id、secret fingerprint 或 redacted summary，不得保存完整 secret。`Preventive Controls` 至少回答 secret scanning、push protection、pre-commit scan、CI scan、日志脱敏、Vite env guard 与 prompt/tool output redaction 是否启用。

<!-- rule-id: OPERATION-CREDENTIAL-025 -->
exposure review 必须包含 `Incident Link`。事件涉及 production、客户数据、费用、跨租户、供应商通知，或无法确认凭据是否被使用时，必须链接本运行项目的安全/隐私事故工件，并判断客户/供应商通知或律师/取证帮助。

<!-- rule-id: OPERATION-CREDENTIAL-026 -->
Codex 或 AI agent 可按模板生成 inventory、access policy、rotation plan、exposure review、runbook 与风险摘要；除非用户显式进入受外部安全控制的 break-glass，它不得读取、打印、复制、发送、保存或轮换真实 production secret。

<!-- rule-id: OPERATION-CREDENTIAL-028 -->
sqlc/MySQL 凭据必须按环境分离；connection string 不得进入日志、migration、fixtures、OpenSpec artifacts 或 support 工单。

### 支持与信任运营

<!-- rule-id: OPERATION-SUPPORT-001 -->
支持专项是运行项目的触发型 playbook：覆盖邮件、表单、聊天、社区、GitHub issue、Linear、社交媒体与内嵌反馈，但不替代本规范的核心入口，也不扩展到无外部用户或无生产支持承诺的实验、呼叫中心排班与大型客服 QA 平台。每个 target 使用同名的 `support/intake/<target>.json`、`playbooks/<target>.md`、`templates/<target>.md` 与 `reviews/<target>.md`；目标是减少下一次支持需求。

<!-- rule-id: OPERATION-SUPPORT-002 -->
`support/intake/<target>.json` 必须包含 `target`、`owner`、`channels`、`categories`、`severity_levels`、`first_response_targets`、`data_handling`、`routing`、`linked_artifacts`、`metrics`、`human_checkpoint` 与 `review_cadence`。

<!-- rule-id: OPERATION-SUPPORT-003 -->
support category 默认包括 `bug / defect`、`billing / entitlement / account access`、`incident / outage`、`privacy / security request`、`feature request / product feedback`、`docs / usability confusion`。

<!-- rule-id: OPERATION-SUPPORT-004 -->
support metrics 至少记录未处理 backlog、first response time、time to resolution、reopen rate、top contact drivers，以及 customer effort 或“是否一次解决”的轻量替代指标。

<!-- rule-id: OPERATION-SUPPORT-005 -->
`support/playbooks/<target>.md` 必须包含 Scope、Triage、Severity、First Response、Reproduction、Workaround、AI Output Complaints 与 Close Criteria。

<!-- rule-id: OPERATION-SUPPORT-006 -->
triage 先判断是否影响多个用户、资金、权限、隐私、安全或造成 AI 伤害；随后优先恢复用户，可采用 workaround、降级、撤销错误权益、补发 credit、关闭高风险 workflow 或转入 incident。

<!-- rule-id: OPERATION-SUPPORT-007 -->
复现信息以最小化为准：保留发生时间和 request id，并标注环境、版本、当时的 feature flag 与错误类别；完整 raw prompt 和用户私密内容默认排除。

<!-- rule-id: OPERATION-SUPPORT-008 -->
`support/templates/<target>.md` 必须提供 Bug / Defect、AI Output Concern、Feature Request 与 Closure 模板。

<!-- rule-id: OPERATION-SUPPORT-009 -->
同一 production target 的支持工件使用同一个 `<target>` 文件名；回复先承认事实和影响，再说明正在做什么，且所有渠道必须使用同一事实版本。

<!-- rule-id: OPERATION-SUPPORT-010 -->
support playbook 必须包含 Billing / Access，模板必须包含 Billing / Access 与 Refund / Credit；case 应链接 bug、OpenSpec change、eval case、security incident、billing reconciliation 或 docs issue。不得承诺未经验证的修复时间、退款、法律结论、删除完成或 24/7 支持；退款、credit、合同承诺、权益或手工账号覆盖必须人审。

<!-- rule-id: OPERATION-SUPPORT-011 -->
support playbook 必须包含 Escalation 与 Privacy / Security Requests，模板包含 Privacy / Security Request。法律通知、监管问询、合规审计与合同谈判转专业服务或单独 OpenSpec；公开事故通知、状态页、道歉、补偿、事后说明及法律/隐私/安全/数据权利请求必须人审。

<!-- rule-id: OPERATION-SUPPORT-012 -->
support playbook 必须包含 Incident Handoff，模板包含 Incident Update；所有事故更新使用同一事实来源。

<!-- rule-id: OPERATION-SUPPORT-013 -->
AI 输出投诉回复要说明已记录并将按安全或质量流程检查，不得把模型输出表述为公司立场。记录 model、prompt/workflow version、tool path、request id 与安全类别；有害内容或越权工具行为，以及影响资金、权限、法律、医疗或安全的幻觉必须 human checkpoint。转为 eval fixture 候选前必须脱敏和裁剪。

<!-- rule-id: OPERATION-SUPPORT-014 -->
可由产品、文档、默认配置、监控、eval 或 runbook 消除的联系原因不得长期依赖人工回复。`support/feedback-ledger/<target>.jsonl` 只记录可行动事实；重复反馈进入 top contact drivers。反馈进入 eval 前必须脱敏、最小化并连接[技术设计](../03-engineering-delivery/05-technical-design.md)中的 prompt/eval 方案与[验证](../03-engineering-delivery/08-verification.md)中的证据要求；账本不得保存邮箱、电话、真实姓名、支付信息、密钥、完整 raw prompt/response 或隐私数据。

<!-- rule-id: OPERATION-SUPPORT-015 -->
客户支持、投诉与信任运营走本运行项目；Support Path 必须链接本规范中的客户支持路径，不得口头承诺 24/7 support。

<!-- rule-id: OPERATION-SUPPORT-016 -->
support 或 founder 访问用户数据必须审计；生产数据 access、impersonation 与手工修复必须 human checkpoint；改变计费、权益、数据删除、权限或外部通知的支持动作必须转对应阶段规范。

<!-- rule-id: OPERATION-SUPPORT-017 -->
把支持信号纳入 roadmap、形成 OpenSpec change、对外确认 bug 或发布安全公告，属于需要人工作出的升级决定。

<!-- rule-id: OPERATION-SUPPORT-018 -->
后台动作必须链接其原因，如 support case、incident、billing reconciliation、OpenSpec change、security/privacy request 或 data migration；break-glass 不得常态化处理普通客服、产品试验、功能开关或批量数据修正。

### AI 质量事故与运行时降级

<!-- rule-id: OPERATION-AI-QUALITY-001 -->
`ai-quality/regression-triage/<capability>.md` 是最小质量回归工件，以 `<capability> AI Quality Regression Triage` 为标题，并包含 Scope、Severity Levels、Detection Signals、First 15 Minutes、Reproduction、Scope Check、Likely Causes、Decision Matrix、Evidence To Capture、Escalation、Linked Artifacts 与 Review Cadence；等级允许 `Q-SEV1`、`Q-SEV2`、`Q-SEV3`。

<!-- rule-id: OPERATION-AI-QUALITY-002 -->
核心任务大面积失败，或可能造成资金、权限、法律、医疗、隐私、安全或高影响决策伤害，定为 `Q-SEV1`，立即止血并由人处置；核心路径明显变差或特定用户群持续失败定为 `Q-SEV2`，当天回滚或降级；小范围、可绕过问题定为 `Q-SEV3`，进入普通修复。

<!-- rule-id: OPERATION-AI-QUALITY-003 -->
质量回归 triage 必须确认谁受影响、从何时开始及是否仍在发生，并用 1—3 个真实或脱敏样例复现；不能复现时先保存 trace、eval 与 user feedback 的引用证据。

<!-- rule-id: OPERATION-AI-QUALITY-004 -->
triage 必须检查最近的 prompt、model、route、retrieval index、tool、schema、feature flag、数据源与供应商状态变化。

<!-- rule-id: OPERATION-AI-QUALITY-005 -->
先限制暴露面：暂停 rollout；再从 fallback、收紧 tool 权限、恢复上一 prompt/model/route 或人工接管中选择最小可行止血措施。

<!-- rule-id: OPERATION-AI-QUALITY-006 -->
`ai-quality/rollback-runbook/<capability>.md` 以 `<capability> AI Quality Rollback Runbook` 为标题，并包含 Scope、Disable Switches、Rollback Paths、Model / Prompt / Route Rollback、Retrieval / Tool Rollback、User Messaging、Validation、Data / Safety Checks、Recovery Criteria、Post-Rollback Follow Up、Linked Artifacts 与 Review Cadence。

<!-- rule-id: OPERATION-AI-QUALITY-007 -->
每项 AI 能力至少有一个止血路径：关闭能力、切基础模式、切旧 prompt/model/route、禁用高风险工具、转人工或异步队列。恢复不能只看服务健康，还要验证 eval pass、schema success、tool success、fallback rate、用户投诉或人工抽样；低质量 fallback 必须说明产品影响。核心、付费或高风险路径需要 human checkpoint；已发生且不可撤销的输出、通知、数据写入或外部动作必须链接 admin/action、audit、support 或 incident 工件。

<!-- rule-id: OPERATION-AI-QUALITY-008 -->
`ai-quality/incident-log/<capability>.json` 顶层必须包含 `capability`、`owner`、`incidents`、`linked_artifacts`、`human_checkpoint`、`review_cadence` 与 `status`；`incidents` 可为空。存在事故时，每项必须包含 `id`、`date`、`severity`、`trigger`、`user_impact`、`affected_versions`、`affected_routes`、`detection`、`response`、`rollback_or_mitigation`、`eval_followup`、`owner` 与 `status`。日志只保存引用和脱敏摘要。

<!-- rule-id: OPERATION-AI-QUALITY-009 -->
`Q-SEV1`/`Q-SEV2` 必须记录时间线、止血动作、回滚或降级结果、后续 eval case 与 owner。若实质属于安全、隐私、漏洞、资金或权限事故，必须升级到本运行项目的安全/隐私或后台运营专项；需要长期审计证明时转交[验证](../03-engineering-delivery/08-verification.md)，不得只留在质量日志。

<!-- rule-id: OPERATION-AI-QUALITY-010 -->
实现 AI 能力前必须先写 `runbook.md`。

<!-- rule-id: OPERATION-AI-RUNTIME-001 -->
fallback runbook 默认位于 `ai-runtime/fallback-runbook/<capability>.md`，包含 Scope、Detection Signals、Immediate Actions、Degradation Modes、Rollback/Compensation、User Messaging、Provider/Connector Escalation、Recovery Check 与 Linked Artifacts。

<!-- rule-id: OPERATION-AI-RUNTIME-002 -->
failure modes 至少覆盖 rate limit、timeout、provider 5xx/503、schema 不合格、tool call 失败、approval 失败、安全拒绝、成本阈值及供应商或 connector 状态异常。

<!-- rule-id: OPERATION-AI-RUNTIME-003 -->
降级可减少输出 token、降低检索数量、切换小模型、关闭工具、转异步、使用缓存或转人工。用户提示必须如实说明功能暂时降级、可重试或已转后台之一，不得暴露供应商内部错误或敏感路由细节。

<!-- rule-id: OPERATION-AI-RUNTIME-004 -->
出现注入、越权、跨租户、数据外发、成本失控、循环、逃逸或 connector 异常时，立即禁用相关 tool/route 或启用 kill switch。

<!-- rule-id: OPERATION-AI-RUNTIME-005 -->
每次 AI 工具调用都要留下可追查的运行记录，使审计者能够还原所用工具、批准状态、输入契约版本、租户与发起者、请求链路、副作用和最终结果；对应字段至少包括 `tool name`、`approval`、`input schema version`、`tenant`、`actor`、`request id`、`trace id`、`side effect`、`outcome`。完整的原始 prompt 或 response 不得落盘，只有完成脱敏的内容才可进入日志。

## 输入与产物

输入是已发布服务与关键 workflow、发布和变更记录、真实运行遥测、合同与支持边界，以及适用的数据、凭据、AI 和第三方依赖事实。产物按本项目规定落入 `ops/`、`incidents/`、`security-incidents/`、`admin-ops/`、`credentials/`、`async-jobs/`、`support/`、`ai-quality/` 与 `ai-runtime/`；只创建真实 target 需要且能持续维护的工件。

## 完成、停止或退出条件

完成要求是：适用的 SLO/SLI 可测，page 可行动且有 runbook，回滚/降级/恢复路径可执行，高风险动作与 secret 有人审和审计，事故与支持有统一事实来源，关键 AI 路径可止血并验证质量恢复。任何真实影响超出授权、无法回滚或撤销、证据不足、租户/权限/数据边界不明，或需要新增合同、法律、监管、客户通知与 24/7 承诺时，必须停止并升级。

## 相关项目引用

- [选题](../01-initiation/01-topic-selection.md)：工作是否开始或继续。
- [技术设计](../03-engineering-delivery/05-technical-design.md)：风险、安全、供应商、权限与承诺边界，以及 prompt/eval 与 AI tool 方案。
- [实现](../03-engineering-delivery/07-implementation.md)：代码、配置、数据变更、异步任务与可观测性落点。
- [验证](../03-engineering-delivery/08-verification.md)：质量样本、核验结果与审计证据。
- [发布](../03-engineering-delivery/09-release.md)：发布、客户上线、SLA 与公开声明。
- [评估](11-evaluation.md)：支持反馈、AI 质量、产品学习、长期维护与知识恢复。
