# 阶段 35：AI 产品审计、证据保全与合规证据包治理规范

## 目标

一人公司的信任问题常常不是“没有做事”，而是半年后说不清当时做了什么、为什么这么做、谁批准、证据在哪里、能不能给客户或审计方看。第 35 阶段定义 AI 产品审计、证据保全与合规证据包治理规范，让每个生产 target 能回答：哪些行为需要审计证据，证据来自哪里，如何防篡改，保留多久，能否对外，怎样脱敏，什么时候必须人工判断。

默认原则：证据是可追溯的索引，不是敏感内容仓库。优先保存 artifact ref、commit、release id、trace id、request id、audit event id、hash、版本号、审批记录和脱敏摘要；不把 secret、原始 prompt/response、完整用户数据、支付数据或供应商 raw payload 复制进证据包。

## 核心依据

- 《人月神话》：大型系统的主要成本来自沟通、概念完整性和长期维护；证据治理要减少未来的解释成本，而不是制造仪式。
- 小型项目管理：一人公司不能维护企业级 GRC 平台；先用五个小工件覆盖证据清单、日志策略、留存策略、对外证据包和周期复盘。
- Google SRE Incident Response / Postmortem Culture：事故处理需要边处理边记录，复盘需要可读、及时、无责、可行动的证据。
- OWASP Logging Cheat Sheet：应用日志应记录安全和运营事件，但应按风险决定日志内容，排除或脱敏 token、PII、支付数据、密钥和敏感内容，并保护日志免受篡改和未授权访问。
- NIST SP 800-53：Audit and Accountability、Assessment/Authorization/Monitoring、Incident Response、PII Processing and Transparency 等控制族提供审计、问责、控制证据和隐私保护的通用词汇。
- NIST AI RMF / Generative AI Profile：AI 风险管理要纳入设计、开发、使用和评估；生成式 AI 需要可追踪的风险、评估、治理和管理证据。
- AICPA Trust Services Criteria / SOC 2：安全、可用性、处理完整性、机密性和隐私是客户最容易理解的信任维度；早期证据包可以按这些维度组织。
- OpenTelemetry semantic conventions：统一 trace、metric、log、event 属性，减少未来跨服务、跨供应商证据关联成本。
- OpenAI Evaluation Best Practices / Data Controls：AI 行为证据应连接 eval、日志、人工判断和数据保留边界；默认不要把客户内容复制到本地长期证据中。

## 范围

适用对象：

- release、incident、SLO、backup/restore、migration、billing、support、admin action、webhook、tool runtime、async job、AI model route、prompt/eval、red team、moderation、memory、data rights、trust policy、security/privacy 变更。
- Go/Kratos/gRPC 服务里的 audit event、admin action、data access、security event、AI workflow event、release evidence、incident evidence。
- sqlc/PostgreSQL 表中的 audit log、evidence index、approval、retention、export、access review 和 evidence package metadata。
- Vite 前端中的 trust center、安全页、合规请求、管理员审计视图、人工操作确认和证据导出 UI。
- 客户安全问卷、SOC 2 准备、供应商尽调、事故沟通、监管/法律请求、企业客户审查。

不适用对象：

- 正式法律意见、eDiscovery、诉讼保全、监管申报、SOC 2 审计执行、法证镜像和企业 GRC 平台；这些需要专业服务或单独 change。
- 原始日志、生产数据库、对象存储、SIEM、trace backend 的完整替代；本阶段只定义“如何索引和打包证据”。
- 临时本地实验，前提是不处理真实用户数据、不影响生产、不产生对外承诺。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
audit-evidence/
  evidence-register/<target>.json
  audit-log-policy/<target>.md
  evidence-retention/<target>.json
  evidence-package/<target>.md
  audit-review/<target>.md
```

### `audit-evidence/evidence-register/<target>.json`

证据注册表必须包含：

- `target`
- `owner`
- `evidence_domains`
- `evidence_items`
- `control_mappings`
- `systems_of_record`
- `collection_policy`
- `integrity_policy`
- `access_policy`
- `privacy_policy`
- `human_checkpoint`
- `review_cadence`

`evidence_items` 每项至少包含：

- `id`
- `name`
- `domain`
- `source_artifact`
- `system_of_record`
- `evidence_ref_type`
- `retention_class`
- `sensitivity`
- `freshness_slo`
- `integrity_method`
- `access_scope`
- `owner`
- `status`

默认 evidence domains 至少覆盖：

- `release`
- `incident`
- `ai_behavior`
- `security_privacy`
- `admin_action`

默认：

- 证据项优先引用已有阶段工件，不复制内容：`openspec/changes/...`、`docs/...`、`slo/`、`release/`、`trust/`、`observability/`、`integrations/`、`async-jobs/`、`ai-*`。
- AI 行为证据必须能追到 prompt version、model route、eval run、red-team/safety finding、trace id 或人工审核记录。
- 对外承诺证据必须连接阶段 25 commitment register；发布证据连接阶段 6 release；事故证据连接阶段 5 SRE-lite。
- 没有 owner、来源、留存、敏感级别和完整性方法的 evidence item 只能是 draft。

### `audit-evidence/audit-log-policy/<target>.md`

审计日志策略必须包含：

- `Scope`
- `Events To Log`
- `Required Fields`
- `Sensitive Fields`
- `Integrity / Tamper Evidence`
- `Access Control`
- `Retention`
- `Query / Export`
- `Alerting`
- `Linked Artifacts`

默认必须审计：

- 登录、鉴权失败、权限变更、租户切换、service token 使用。
- admin action、break-glass、生产数据访问、数据导入/导出、数据删除/恢复、migration/backfill。
- billing/entitlement/usage reconciliation、refund、quota override。
- release、rollback、feature flag、runtime config、secret/key rotation。
- AI prompt/model/tool/route 变更、eval gate、human review、safety block、moderation action、memory create/update/delete。
- webhook replay、dead letter 处理、外部事件补发、手工重试。
- 用户数据权利请求、隐私/安全事件、客户合规请求。

默认 required fields：

- `event_id`
- `timestamp`
- `actor_id`
- `actor_type`
- `tenant_id`
- `action`
- `resource_type`
- `resource_id`
- `request_id`
- `trace_id`
- `outcome`
- `reason`
- `linked_artifact`
- `error_class`

默认不记录：

- secret、token、password、private key、session cookie、数据库连接串。
- 原始 prompt、原始 response、完整 tool output、完整 webhook raw payload、完整用户输入、支付卡号、身份证号、健康/金融等敏感个人数据。
- 需要排障时使用短期、受控、脱敏的 attachment 或专用日志存储，并记录审批与删除日期。

### `audit-evidence/evidence-retention/<target>.json`

证据留存策略必须包含：

- `target`
- `owner`
- `retention_classes`
- `data_minimization`
- `legal_hold`
- `deletion_policy`
- `export_policy`
- `access_policy`
- `integrity_policy`
- `storage_locations`
- `human_checkpoint`
- `status`

默认 retention classes：

- `operational`：短期排障证据，默认 30 到 90 天。
- `audit`：发布、审批、变更、访问、客户请求等审计证据，默认 1 年。
- `security`：安全事件、访问异常、break-glass、密钥轮换证据，默认 2 年或按合同/法规。
- `customer_evidence`：客户尽调、问卷、trust center export、合规说明，默认 1 年或合同周期。

默认：

- 留存期不能只写“永久”；必须有目的、删除路径和例外条件。
- legal hold、客户合同、监管、诉讼、隐私删除请求之间冲突时必须人工 checkpoint。
- 证据导出给客户、供应商、律师、审计方或外部系统前必须记录范围、脱敏方式、接收方和过期日期。

### `audit-evidence/evidence-package/<target>.md`

证据包必须包含：

- `Scope`
- `Audience`
- `Claims Covered`
- `Evidence Index`
- `Freshness`
- `Redactions`
- `Open Risks`
- `How To Reproduce`
- `Customer / Auditor Notes`
- `Linked Artifacts`

默认：

- 证据包按受众生成：内部复盘、客户安全问卷、企业采购、事故沟通、SOC 2 准备、隐私请求、监管/法律请求。
- 对外证据包只包含必要证据的引用、摘要、截图或导出，不包含其他客户、内部密钥、原始用户内容、攻击样本细节或供应商敏感信息。
- 每个 claim 必须能追到 evidence register 的 evidence item。
- Freshness 说明证据截至日期、版本、环境和最近验证命令。

### `audit-evidence/audit-review/<target>.md`

审计复盘必须包含：

- `Recent Changes`
- `Evidence Gaps`
- `Audit Log Health`
- `Retention / Deletion`
- `Access Review`
- `AI Evidence`
- `Customer / Compliance Requests`
- `Incidents`
- `Open Risks`
- `Next One Change`

默认节奏：

- pre-revenue：每月一次，或发布客户可见 AI/安全/隐私/计费承诺前。
- 有付费客户：每两周一次，或客户尽调、事故、安全事件、数据权利请求、AI 行为重大变更前后。
- 每次只选一个最高影响改进：补 audit log 字段、补 evidence item、缩短留存、补导出脱敏、补 eval 证据、补访问复核或关闭过期证据包。

## Go / Kratos / sqlc / gRPC 默认规则

- Go/Kratos 服务使用 middleware 或 usecase hook 记录审计事件；业务代码不得散落临时字符串日志作为唯一证据。
- gRPC metadata 传播 actor、tenant、request id、trace id、service account、idempotency key；审计事件记录 metadata 摘要，不记录 payload。
- sqlc 默认表可包含：`audit_events`、`audit_event_links`、`evidence_items`、`evidence_packages`、`evidence_exports`、`evidence_access_reviews`、`retention_policies`、`legal_holds`。
- `audit_events` 默认字段：event_id、occurred_at、actor_id、actor_type、tenant_id、action、resource_type、resource_id、request_id、trace_id、outcome、reason、linked_artifact、integrity_hash、retention_class。
- 高风险 action 连接阶段 24 admin action；AI tool side effect 连接阶段 32；async side effect 连接阶段 33；webhook replay 连接阶段 34。
- 审计日志写入失败不能静默吞掉：低风险事件可降级告警，高风险事件必须阻断或进入 fail-closed/queued 状态，并记录运维事件。

## Vite 前端默认规则

- 管理员审计页面优先显示过滤、时间线、actor、tenant、action、outcome、linked artifact、trace id 和导出状态。
- 证据包导出 UI 必须有范围、受众、敏感级别、脱敏摘要、过期日期和确认步骤。
- 不显示 secret、完整 raw payload、完整 prompt/response、完整个人数据、支付数据或其他租户证据。
- 客户可见 trust center 保持 Vercel/Geist 风格：密集但清晰，按 Security、Availability、Processing Integrity、Confidentiality、Privacy 和 AI Safety 分组，不用营销文案替代证据。
- 对外下载、分享链接、客户问卷附件必须有访问日志和过期策略。

## AI workflow 默认规则

- AI 相关证据默认保存版本和指标：prompt version、model route、eval dataset/run、red-team case id、safety decision、moderation policy version、trace id、human review id、cost bucket。
- 不把原始 prompt/response 长期保存在 `audit-evidence/`；需要留存时使用专门受控存储、脱敏、短保留、访问审批和删除计划。
- 模型或供应商变更的证据必须连接阶段 30 model routing；prompt/eval 变更连接阶段 4/26；安全红队连接阶段 27；内容安全连接阶段 28；工具运行时连接阶段 32。
- AI 自动生成证据包、合规回答或安全问卷答案时，输出只能作为 draft；对外发送前必须人工 checkpoint。
- AI agent 不得自行扩大证据导出范围、解除脱敏、修改留存策略、删除证据或创建 legal hold。

## 需要人判断的关键点

只把这些判断交给人：

- 是否对客户、审计方、监管方、律师、供应商或公众导出/分享证据包。
- 是否让证据包含敏感数据、生产数据、用户内容、原始 prompt/response、日志摘录、事故细节或供应商材料。
- 是否创建、解除或覆盖 legal hold、删除例外、合同/法规留存例外。
- 是否公开新的安全、隐私、可用性、AI safety、SOC 2、合规或客户承诺。
- 是否接受缺少 audit log、证据 item、完整性校验、访问控制、脱敏、freshness 或复现步骤的证据包。
- 是否允许生产数据访问、break-glass、admin action、webhook replay、AI 高影响决策作为合规证据。
- 是否修改证据留存期、导出范围、外部接收方、访问权限或 evidence package audience。
- 是否需要律师、安全顾问、隐私顾问、审计师或客户安全团队参与。

其他字段完整性、章节、JSON 枚举、敏感内容扫描、required fields、positive/negative fixture、OpenSpec linkage 和基础验证由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“有哪些证据、日志怎么记、证据留多久、如何对外打包、如何复盘”。
- 保留：人只判断导出、敏感内容、legal hold、对外承诺、证据缺口接受和专业意见；字段和格式交给脚本。
- 调整：不引入 GRC/SIEM 平台作为默认要求；先用 Markdown/JSON 建立证据索引。
- 调整：不复制原始日志和用户内容，只保留 ref/hash/trace/version/审批。
- 风险：证据治理容易变成“每件事都截图”。缓解：evidence register 只收高影响域，audit review 每次只选一个 next one change。

结论：可落地。一个人可以先为最可能被客户问到的 target 写五个文件，覆盖发布、事故、AI 行为、安全隐私和后台操作证据。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：客户安全问卷和 trust center 能从证据包恢复上下文，不再靠临时翻聊天记录。
- 工程角度：Go/Kratos/sqlc/gRPC 有明确 audit event 表、metadata、linked artifact 和 fail-closed 规则。
- 运维角度：SRE incident、postmortem、release、rollback、backup drill 都能被索引到一个 evidence register。
- 安全隐私角度：默认不保存 secret、原始 prompt/response、完整个人数据和支付数据；外部导出需要脱敏和人审。
- 成本角度：不要求长期保存所有日志，只按 retention class 和 evidence item 保留真正有用的证据。

结论：可落地。第 35 阶段把“将来怎么证明”前移到研发规范里，同时避免把证据目录变成新的敏感数据仓库。
