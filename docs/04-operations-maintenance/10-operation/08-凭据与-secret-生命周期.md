# 运行：凭据与 secret 生命周期

## 执行细则

<!-- rule-id: OPERATION-CREDENTIAL-001 -->
API key、service account、webhook secret、TLS/private key、OpenAI/provider key、CI/OIDC identity、短期 token、mTLS cert、AI connector/MCP token 与 break-glass credential 都进入 credential lifecycle。适用范围包括 Go/Kratos/sqlc/gRPC 服务、Vite 前端、AI workflow、worker、webhook、admin/support 工具及 local/preview/staging/production。每个生产 target 至少维护 `credentials/inventory/<target>.json`；普通配置和 flag 仍归配置专项，整体安全基线仍归[技术设计](../../03-engineering-delivery/05-technical-design.md)。

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
