# credential-secret-lifecycle-standard Specification

## Purpose

Define the minimum credential, secret, service-account, API-key, signing-key, and connector-token lifecycle standard for a one-person AI company so production systems can inventory credentials, control access, rotate safely, prove old versions were revoked, and respond to exposure without storing real secret values in the repository.

## Requirements

### Requirement: 高风险 target 必须定义 credential lifecycle artifacts

Production services, user-visible AI workflows, CI/CD deploy flows, webhook integrations, admin/support tools, and systems using provider API keys, database credentials, signing keys, encryption keys, service accounts, or connector tokens MUST define credential lifecycle artifacts before production release or high-risk credential change.

#### Scenario: 创建 credential lifecycle artifacts

- GIVEN 一个 target 使用 production credential、provider API key、service account、database password、webhook signing secret、JWT/encryption key、TLS/private key、CI token 或 connector token
- WHEN 创建 credential lifecycle artifacts
- THEN 创建 `credentials/inventory/<target>.json`
- AND 创建 `credentials/access-policy/<target>.md`
- AND 创建 `credentials/rotation-plan/<target>.md`
- AND 创建 `credentials/rotation-run/<target>.json`
- AND 创建 `credentials/exposure-review/<target>.md`
- AND 在 OpenSpec design 或 tasks 中链接 credential artifacts

### Requirement: Credential inventory 必须记录 metadata 而不保存 secret value

Credential inventory MUST record target, owner, environments, credentials, storage locations, injection paths, detection controls, rotation defaults, linked artifacts, human checkpoint, review cadence, and status without storing real secret values.

#### Scenario: 创建 credential inventory

- GIVEN reviewer 打开 `credentials/inventory/<target>.json`
- WHEN 检查凭据清单
- THEN 文件包含 `target`、`owner`、`environments`、`credentials`、`storage_locations`、`injection_paths`、`detection_controls`、`rotation_defaults`、`linked_artifacts`、`human_checkpoint`、`review_cadence`、`status`
- AND 每个 credential 包含 `id`、`type`、`purpose`、`issuer`、`environment`、`consumer`、`scope`、`storage_ref`、`injection_method`、`rotation_interval`、`expires_on`、`last_rotated`、`revocation_path`、`blast_radius`、`status`
- AND `storage_ref` 不包含真实 secret value

### Requirement: Access policy 必须定义最小权限、注入边界、前端边界和审计

Access policy MUST define identities and roles, least privilege, storage and injection, CI/CD, local development, frontend boundary, audit and monitoring, human checkpoints, and review cadence.

#### Scenario: 创建 access policy

- GIVEN reviewer 打开 `credentials/access-policy/<target>.md`
- WHEN 检查访问策略
- THEN 文档包含 Scope、Identities And Roles、Least Privilege、Storage And Injection、CI / CD、Local Development、Frontend Boundary、Audit And Monitoring、Human Checkpoints、Review Cadence
- AND 生产 secret 访问边界不授予浏览器、Vite bundle、普通日志、prompt、eval fixture、RAG source 或 AI agent 默认读取权限

### Requirement: Rotation plan 必须定义双钥或版本策略、验证、回滚和撤旧

Rotation plan MUST define scope, credentials, preconditions, dual-key or version strategy, steps, validation, rollback, revocation, communication, evidence, human checkpoints, and review cadence.

#### Scenario: 创建 rotation plan

- GIVEN reviewer 打开 `credentials/rotation-plan/<target>.md`
- WHEN 检查轮换计划
- THEN 文档包含 Scope、Credentials、Preconditions、Dual-Key Or Version Strategy、Steps、Validation、Rollback、Revocation、Communication、Evidence、Human Checkpoints、Review Cadence
- AND 计划说明如何验证新凭据可用
- AND 计划说明如何撤销旧凭据或记录不能撤销的原因

### Requirement: Rotation run 必须记录验证、撤旧、决策、缺口和行动

Rotation run MUST record target, owner, date, environment, credential refs, reason, steps, validation, downtime, user impact, revoked old versions, evidence refs, decision, gaps, actions, human checkpoint, and status.

#### Scenario: 创建 rotation run

- GIVEN reviewer 打开 `credentials/rotation-run/<target>.json`
- WHEN 检查轮换记录
- THEN 文件包含 `target`、`owner`、`date`、`environment`、`credential_refs`、`reason`、`steps`、`validation`、`downtime`、`user_impact`、`revoked_old_versions`、`evidence_refs`、`decision`、`gaps`、`actions`、`human_checkpoint`、`status`
- AND `decision` 是 `pass`、`pass_with_notes`、`needs_fix`、`abort`、`accepted_risk` 或 `defer`

#### Scenario: 高风险 rotation run 需要人工 checkpoint

- GIVEN `revoked_old_versions=false` 或 `decision` 是 `needs_fix`、`abort`、`accepted_risk`、`defer`
- WHEN 写入 rotation run
- THEN `human_checkpoint` MUST 记录风险接受或下一步判断
- AND `gaps` 与 `actions` MUST 非空

### Requirement: Exposure review 必须把发现、撤销、影响、证据和预防控制串起来

Exposure review MUST record scope, detection sources, findings, active exposure, revocation actions, user/customer impact, evidence, incident link, preventive controls, action items, human checkpoints, and review cadence.

#### Scenario: 创建 exposure review

- GIVEN reviewer 打开 `credentials/exposure-review/<target>.md`
- WHEN 检查泄露复盘
- THEN 文档包含 Scope、Detection Sources、Findings、Active Exposure、Revocation Actions、User / Customer Impact、Evidence、Incident Link、Preventive Controls、Action Items、Human Checkpoints、Review Cadence
- AND Findings 或 Active Exposure 非空时，Revocation Actions 与 Human Checkpoints MUST 非空

### Requirement: Frontend、AI 和文档工件不得保存真实 secret

Credential lifecycle artifacts MUST NOT store secrets, production tokens, API keys, OAuth refresh tokens, private keys, session cookies, database connection strings, webhook signing secrets, JWT signing keys, payment data, raw prompts, raw responses, raw tool outputs, raw provider payloads, unredacted personal data, or executable attack payloads.

#### Scenario: 写入 credential artifacts

- GIVEN Codex 或 reviewer 要记录凭据证据、泄露发现、日志、prompt、工具输出、provider response 或配置片段
- WHEN 写入 `credentials/` artifacts
- THEN 使用 secret reference、key id、version id、fingerprint、hash、redacted summary、trace id、request id、alert id、commit id 或 controlled attachment reference
- AND 不保存真实 secret value、完整 Authorization header、private key、production DSN、OpenAI/provider key、raw prompt/response/tool output 或未脱敏个人数据

### Requirement: Go/Kratos/sqlc/gRPC、Vite 和 AI workflow 必须落实 credential 边界

Backend, frontend, and AI workflow implementations MUST align credential handling with the credential lifecycle artifacts.

#### Scenario: 实现 credential 边界

- GIVEN target 使用 Go/Kratos/sqlc/gRPC、Vite 或 AI workflow
- WHEN 实现或 review credential handling
- THEN Go/Kratos 服务通过 typed config 或 runtime injection 获取 secret reference/value
- AND sqlc/PostgreSQL connection strings 不进入日志、migration、fixtures 或 docs
- AND gRPC call credentials 不在未保护 channel 上发送
- AND Vite `VITE_*` 与浏览器 bundle 不包含 secret
- AND AI prompt、eval、trace、RAG source、memory 和 tool output 不包含真实 secret
