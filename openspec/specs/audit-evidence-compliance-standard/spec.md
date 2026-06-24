# audit-evidence-compliance-standard 规格

## Purpose

Define the minimum one-person-company governance for audit evidence, evidence preservation, audit log policy, retention, redaction, customer/auditor evidence packages, and recurring audit review across Go/Kratos/sqlc/gRPC services, Vite surfaces, and AI workflows.

## Requirements

### Requirement: 生产 target 必须定义 audit-evidence artifacts

Any production target that needs release, incident, trust, security, privacy, billing, support, admin, webhook, AI behavior, model route, eval, red-team, moderation, memory, data-rights, customer due-diligence, or compliance evidence MUST define audit evidence artifacts.

#### Scenario: 新生产 target 需要可证明的信任证据

- GIVEN 一个 target 会产生客户、审计、安全、隐私、AI、运营、计费、支持或后台操作证据
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `audit-evidence/evidence-register/<target>.json`
- AND 创建 `audit-evidence/audit-log-policy/<target>.md`
- AND 创建 `audit-evidence/evidence-retention/<target>.json`
- AND 创建 `audit-evidence/evidence-package/<target>.md`
- AND 创建 `audit-evidence/audit-review/<target>.md`

### Requirement: Evidence register 必须定义 evidence domain、item、control mapping、system of record、collection、integrity、access、privacy 和人工 checkpoint

Evidence register MUST record target、owner、evidence domains、evidence items、control mappings、systems of record、collection policy、integrity policy、access policy、privacy policy、human checkpoint 和 review cadence.

#### Scenario: Reviewer 判断证据是否足够

- GIVEN reviewer 打开 `audit-evidence/evidence-register/<target>.json`
- WHEN 需要理解目标有哪些证据
- THEN 每个 evidence item 包含 id、name、domain、source_artifact、system_of_record、evidence_ref_type、retention_class、sensitivity、freshness_slo、integrity_method、access_scope、owner 和 status
- AND evidence domains 至少覆盖 release、incident、ai_behavior、security_privacy 和 admin_action
- AND AI 证据能追到 prompt/model/eval/trace/human-review/safety 相关引用

### Requirement: Audit log policy 必须定义事件范围、字段、敏感字段、完整性、访问控制、留存、查询导出、告警和关联工件

Audit log policy MUST record scope、events to log、required fields、sensitive fields、integrity/tamper evidence、access control、retention、query/export、alerting 和 linked artifacts.

#### Scenario: 高风险行为被记录为审计事件

- GIVEN 发生登录鉴权、权限变更、admin action、生产数据访问、数据导入导出、release、rollback、feature flag、runtime config、AI route/prompt/tool/eval 变更、webhook replay、billing reconciliation、数据权利请求或安全隐私事件
- WHEN 系统记录 audit event
- THEN audit event 至少包含 event_id、timestamp、actor_id、actor_type、tenant_id、action、resource_type、resource_id、request_id、trace_id、outcome、reason、linked_artifact 和 error_class
- AND 不记录 secret、token、password、private key、session cookie、数据库连接串、原始 prompt/response、完整 tool output、完整 webhook raw payload、完整个人数据或支付数据

### Requirement: Evidence retention 必须定义 retention class、最小化、legal hold、删除、导出、访问、完整性、存储位置和人工 checkpoint

Evidence retention policy MUST record target、owner、retention classes、data minimization、legal hold、deletion policy、export policy、access policy、integrity policy、storage locations、human checkpoint 和 status.

#### Scenario: 证据需要保留、删除或导出

- GIVEN evidence item、audit log、evidence package 或外部请求触发留存/删除/导出
- WHEN 读取 `audit-evidence/evidence-retention/<target>.json`
- THEN retention classes 至少包含 operational、audit、security 和 customer_evidence
- AND 每个 retention class 有 purpose、duration、storage、deletion trigger 和 owner
- AND legal hold、删除例外、外部导出、敏感数据和留存期变化触发人工 checkpoint

### Requirement: Evidence package 必须定义范围、受众、承诺、证据索引、新鲜度、脱敏、风险、复现方式、客户/审计备注和关联工件

Evidence package MUST record scope、audience、claims covered、evidence index、freshness、redactions、open risks、how to reproduce、customer/auditor notes 和 linked artifacts.

#### Scenario: 客户或审计方请求证据

- GIVEN 客户、安全问卷、事故沟通、SOC 2 准备、隐私请求、监管/法律请求或内部复盘需要证据
- WHEN 创建或更新 `audit-evidence/evidence-package/<target>.md`
- THEN 每个 claim 能追到 evidence register 的 evidence item
- AND evidence package 说明截至日期、版本、环境、验证命令、脱敏方式、开放风险和复现路径
- AND 对外证据包不包含其他客户、内部密钥、原始用户内容、攻击样本细节或供应商敏感信息

### Requirement: Audit review 必须复盘近期变更、证据缺口、日志健康、留存删除、访问复核、AI 证据、客户合规请求、事故、风险和下一项改进

Audit review MUST record recent changes、evidence gaps、audit log health、retention/deletion、access review、AI evidence、customer/compliance requests、incidents、open risks 和 next one change.

#### Scenario: 周期性复查审计证据健康

- GIVEN target 有近期 release、incident、AI、security/privacy、billing、support、admin、webhook、customer request 或 retention 变更
- WHEN 更新 `audit-evidence/audit-review/<target>.md`
- THEN 记录证据缺口、audit log health、retention/deletion、access review、AI evidence、customer/compliance requests、incidents 和 open risks
- AND 只选择一个最高影响的 next one change

### Requirement: 高风险审计证据动作必须人工 checkpoint

External evidence sharing, sensitive evidence inclusion, legal hold or deletion exceptions, public trust/compliance claims, AI high-impact evidence, production data/admin evidence, incident or security disclosure, retention period changes, audit-log integrity exceptions, and exporting evidence outside the workspace MUST have human checkpoint coverage.

#### Scenario: 证据动作触发高风险条件

- GIVEN evidence register、audit log policy、retention policy、evidence package、audit review 或 release 触发高风险条件
- WHEN 准备发布、导出、删除、保留、公开或接受例外
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、阻塞、降级、删除计划或专业审阅需求

### Requirement: Audit evidence artifacts 不得保存敏感内容

Audit evidence artifacts MUST NOT store secrets, production tokens, API keys, OAuth refresh tokens, private keys, session cookies, database connection strings, payment data, raw prompts, raw responses, raw tool outputs, raw webhook bodies, raw provider payloads, full user input, unredacted personal data, or executable attack payloads.

#### Scenario: 记录日志、AI、事故、客户请求或证据包内容

- GIVEN 需要保存 release evidence、incident evidence、AI evidence、audit event、customer request、support evidence、admin evidence、webhook evidence 或 security finding
- WHEN 写入 `audit-evidence/` artifacts
- THEN 使用 synthetic example、redacted summary、artifact id、commit、release id、trace id、request id、audit event id、eval run id、hash、finding id、approval id 或 controlled attachment reference
- AND 不保存 secret、production token、API key、OAuth refresh token、private key、session cookie、数据库连接串、支付数据、原始 prompt/response/tool output、完整 webhook raw body、raw provider payload、完整用户输入、未脱敏个人数据或可直接执行的攻击 payload
