# 阶段 54：凭据、密钥与服务账号生命周期规范

## 目标

一人公司的密钥问题通常不是“不知道不能泄露”，而是：到底有哪些凭据、谁在用、在哪里注入、多久没轮换、泄露后先撤哪个、旧版本是否还活着，没有一个可恢复的事实来源。阶段 54 只解决这个窄问题：让生产凭据、API key、service account、webhook secret、TLS/private key、数据库凭据、OpenAI/project key、CI/OIDC identity 和本地开发凭据都有 inventory、访问边界、轮换计划、轮换证据和泄露复盘。

默认原则：**记录 metadata，不记录 secret value**。仓库只保存引用、用途、scope、owner、轮换证据和风险判断；真实 secret 值只存在 secret manager、CI secrets、云平台、开发者本机受保护存储或短期环境变量中。

## 核心依据

- 《人月神话》：凭据治理不能靠工具银弹。真正要降低的是概念复杂度：一个凭据只有一个用途、一个 owner、一个 revocation path、一个可验证的轮换故事。
- 小型项目管理：一人公司不维护完整 PAM/KMS/GRC 平台；阶段 54 只保留五个工件，把人的注意力留给生产凭据、真实泄露和无法自动轮换的高风险项。
- OWASP Secrets Management：secrets 需要集中存储、访问控制、审计、轮换、撤销、过期和 incident response；metadata 必须能回答创建、使用、轮换、删除、联系人、用途和类型。
- NIST SP 800-57 Part 1：cryptographic key management 覆盖 key material 的保护、用途、生命周期、backup、compromise、inventory 和 policy；阶段 54 只取一人公司能执行的 key inventory 与 lifecycle 片段。
- Twelve-Factor App Config：配置应与代码分离；一个代码库应能随时公开而不暴露凭据。
- GitHub Secret Scanning / Push Protection：secret scanning 用于发现已进入仓库历史、PR、issue、discussion 的凭据；push protection 把泄露挡在进入仓库之前。
- OpenAI API Key Safety / Production Best Practices：OpenAI key 不应共享、不应在浏览器或移动端暴露、不应提交到仓库；生产应使用环境变量或 secret management service，并可按 project 隔离 staging/production。
- Google Cloud Secret Manager Best Practices：周期性轮换能限制泄露影响、移除不再需要访问的人，并降低事故风险；secret inventory、访问日志和组织级策略能发现不符合要求的 secret。
- Building Secure and Reliable Systems：安全和可靠性都受益于简单、可理解的设计；凭据边界越复杂，事故时越难止血。
- Kratos Config / gRPC Auth / Vite Env：Go/Kratos 可从文件、env 或配置中心加载配置；gRPC credentials 应与 TLS/channel 边界配合；Vite `VITE_*` 会进入浏览器 bundle，不能放敏感值。

## 范围

适用对象：

- OpenAI、模型供应商、支付、邮件、短信、对象存储、数据库、Webhook、OAuth client、analytics、monitoring、CI/CD、cloud IAM、deploy token、TLS/private key、JWT signing key、encryption key、RAG/vector store、MCP/connector token。
- Go/Kratos/sqlc/gRPC 服务、Vite 前端、AI workflow、worker、webhook endpoint、admin/support 工具、本地开发环境、preview/staging/production。
- 人工创建的长期 key、自动生成的短期 token、service account、OIDC federated identity、mTLS cert、webhook signing secret 和 break-glass credential。

不适用对象：

- 阶段 10 的整体 security/privacy/supply-chain 基线；阶段 54 只负责 credential lifecycle。
- 阶段 14 的普通配置项、feature flag 和 runtime change；只有敏感凭据及其引用进入本阶段。
- 阶段 44 的完整安全事故响应；本阶段只定义 credential exposure 的撤销、轮换和预防复盘。
- 企业级 HSM、PAM、secret zero、多云 KMS 架构、正式密码学政策；有客户或监管要求时单独开 change。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
credentials/
  inventory/<target>.json
  access-policy/<target>.md
  rotation-plan/<target>.md
  rotation-run/<target>.json
  exposure-review/<target>.md
```

### `credentials/inventory/<target>.json`

凭据清单是事实来源，不保存真实值。必须包含：

- `target`
- `owner`
- `environments`
- `credentials`
- `storage_locations`
- `injection_paths`
- `detection_controls`
- `rotation_defaults`
- `linked_artifacts`
- `human_checkpoint`
- `review_cadence`
- `status`

`credentials` 每项至少包含：

- `id`
- `type`：`api_key`、`database_password`、`service_account`、`oauth_client_secret`、`webhook_signing_secret`、`tls_private_key`、`jwt_signing_key`、`encryption_key`、`ci_token`、`mcp_connector_token`、`other`
- `purpose`
- `issuer`
- `environment`
- `consumer`
- `scope`
- `storage_ref`
- `injection_method`
- `rotation_interval`
- `expires_on`
- `last_rotated`
- `revocation_path`
- `blast_radius`
- `status`

默认规则：

- `storage_ref` 只写 secret manager path、CI secret name、cloud resource id、key id、version id 或本地占位说明，不写 secret value。
- `scope` 应尽量是最小权限、单环境、单用途。production 和 staging 默认分开 key/project。
- `last_rotated` 未知时写 `unknown`，并在 `rotation-plan` 中列为第一优先级。
- `revocation_path` 必须能让一个疲惫的人在事故时知道去哪撤销：dashboard、CLI、API、runbook 或 vendor support。
- OpenAI/API provider key 应记录 project、rate/spend guard、owner、usage monitoring 和是否暴露到前端。

### `credentials/access-policy/<target>.md`

访问策略给人读，必须包含：

```markdown
# <target> Credential Access Policy

## Scope

## Identities And Roles

## Least Privilege

## Storage And Injection

## CI / CD

## Local Development

## Frontend Boundary

## Audit And Monitoring

## Human Checkpoints

## Review Cadence
```

默认规则：

- 生产 secret 访问默认只给运行时 identity、deploy identity 和 break-glass owner；Codex/AI agent 不能读取真实 secret。
- CI 默认使用 OIDC/federated identity 或短期 token；长期 deploy token 需要轮换计划和 owner。
- 本地开发使用 `.env.local` 或开发 secret manager，且不复用 production secret。
- Vite 前端不得包含 API key、OpenAI key、数据库 URL、service token、JWT secret 或任何可代替后端身份的凭据。
- 访问日志至少能回答：谁/哪个 workload 在何时读取了哪个 secret reference。

### `credentials/rotation-plan/<target>.md`

轮换计划必须包含：

```markdown
# <target> Credential Rotation Plan

## Scope

## Credentials

## Preconditions

## Dual-Key Or Version Strategy

## Steps

## Validation

## Rollback

## Revocation

## Communication

## Evidence

## Human Checkpoints

## Review Cadence
```

默认规则：

- 能双 key 或版本化的供应商，优先先创建新 key、部署新引用、验证流量、再撤旧 key。
- 不能双 key 的凭据必须安排低流量窗口、rollback path 和健康检查。
- 数据库密码、JWT signing key、webhook signing secret、TLS/private key、OpenAI key、CI deploy identity 都必须有明确验证步骤。
- 轮换计划不要求每月轮所有 key；先轮换最高 blast radius、最长未动、无法确定 owner、疑似泄露或离职/权限变更相关的凭据。
- 任何生产 key 轮换、无法撤旧 key、扩大 scope、临时共享 secret、跳过验证或接受旧 key 继续有效都需要人工 checkpoint。

### `credentials/rotation-run/<target>.json`

轮换运行记录必须包含：

- `target`
- `owner`
- `date`
- `environment`
- `credential_refs`
- `reason`
- `steps`
- `validation`
- `downtime`
- `user_impact`
- `revoked_old_versions`
- `evidence_refs`
- `decision`
- `gaps`
- `actions`
- `human_checkpoint`
- `status`

`decision` 只能是：

- `pass`
- `pass_with_notes`
- `needs_fix`
- `abort`
- `accepted_risk`
- `defer`

默认规则：

- `steps` 记录动作摘要和结果，不记录 secret value。
- `validation` 记录 smoke、health、synthetic call、provider usage、logs/metrics、failed auth rate 或 gRPC/API request 成功证据。
- `revoked_old_versions=false` 或 `decision=accepted_risk/defer/abort/needs_fix` 时，必须有 `human_checkpoint`、`gaps` 和 `actions`。
- `actions` 最多 3 个，避免一人公司把轮换复盘变成无法关闭的长清单。

### `credentials/exposure-review/<target>.md`

泄露复盘用于 secret scanning 告警、误提交、日志泄露、AI/tool 输出泄露、供应商提醒或人工发现。必须包含：

```markdown
# <target> Credential Exposure Review

## Scope

## Detection Sources

## Findings

## Active Exposure

## Revocation Actions

## User / Customer Impact

## Evidence

## Incident Link

## Preventive Controls

## Action Items

## Human Checkpoints

## Review Cadence
```

默认规则：

- 发现真实 production credential、OpenAI key、database URL、private key、webhook secret、CI token、OAuth refresh token 或 session cookie 时，先撤销/轮换，再清理历史。
- Git 历史清理不是第一止血动作；如果旧 key 已撤销，重点转为防止再泄露和评估影响。
- `Findings` 使用 alert id、commit hash、file path、line reference、provider key id、secret fingerprint 或 redacted summary，不保存完整 secret。
- `Preventive Controls` 至少回答是否启用 secret scanning、push protection、pre-commit scan、CI scan、日志脱敏、Vite env guard 和 prompt/tool output redaction。
- 涉及生产、客户数据、费用、跨租户、供应商通知或无法确认是否被使用时，必须链接阶段 44 security incident artifact。

## Go / Kratos / sqlc / gRPC 默认规则

- Kratos config struct 只接收 secret reference 或运行时注入后的配置对象；业务代码不得散落读取 `os.Getenv("OPENAI_API_KEY")`。
- 服务启动时校验必需 secret 是否存在、格式是否合理、权限是否能完成最小 smoke；失败默认 fail fast。
- sqlc/PostgreSQL 凭据按环境分离，连接串不进入日志、migration、fixtures、OpenSpec artifacts 或 support 工单。
- gRPC call credentials 不得在未加密 channel 上发送；内部 service account/token/mTLS 证书必须进入 inventory。
- JWT signing key、webhook signing secret 和 encryption key 轮换必须定义 old/new overlap、kid/version、验证和旧版本撤销。

## Vite 前端默认规则

- `VITE_*` 值视为公开信息。任何以 `VITE_` 暴露的值都不得是 secret，也不能作为后端授权依据。
- 前端需要调用 OpenAI、支付、对象存储、数据库或私有 API 时，必须通过后端/BFF/serverless function 代理，并由后端持有 secret。
- 前端构建日志、preview 环境变量、错误上报和 analytics event 不得包含 token、key、cookie、Authorization header 或 connection string。
- 密钥泄露防护界面或内部控制台采用 Vercel/Geist 风格：表格、状态、动作按钮清楚；危险动作需要确认和 evidence，而不是用营销文案掩盖风险。

## AI workflow 默认规则

- AI prompt、tool output、eval fixture、trace、memory、RAG source 和 support transcript 默认不得包含真实 secret。
- AI agent 可以生成 rotation plan、runbook 和风险摘要，但不能读取、打印、复制、发送、保存或轮换真实 production secret，除非用户显式进行 break-glass 且有外部安全控制。
- AI connector/MCP token、tool runtime token、provider API key、sandbox credential 必须进入 inventory，并记录 scope、approval、revocation path 和 data boundary。
- 发现 prompt injection 诱导模型泄露 secret、工具返回 secret、RAG/source 含 secret 时，按 exposure review 处理，并补阶段 27 red-team case 或阶段 32 tool runtime guard。

## 需要人判断的关键点

默认不问：

- 普通字段顺序、Markdown 小节文案、低风险开发 key 命名、无生产访问的测试 fixture。
- Codex 可先按模板生成 inventory、access policy、rotation plan、exposure review。

必须问：

- 是否允许 production secret 轮换、撤销、暂停旧版本或接受旧版本继续有效。
- 是否新增长期生产 key、跨环境共享 key、跨租户共享 credential、第三方可读 secret 或外部 action/deploy identity。
- 是否把任何值暴露到 Vite/browser/mobile、公开 docs、support transcript、logs、prompt、eval 或 RAG source。
- 是否无法轮换、无法撤销、无法确认是否泄露、无法定位 owner 或无法区分 staging/production。
- 是否涉及 OpenAI/provider key、支付、数据库、JWT/encryption key、TLS/private key、CI deploy token、break-glass credential。
- 是否需要触发阶段 44 安全/隐私事故、客户/供应商通知或律师/取证帮助。

## 执行顺序

1. 为最关键 target 写 `credentials/inventory/<target>.json`，先列 production 和 OpenAI/provider key。
2. 写 `access-policy`，明确谁/哪个 workload 能读，哪里注入，哪里绝不允许出现。
3. 写 `rotation-plan`，先覆盖最高 blast radius 的 1 到 3 个凭据。
4. 执行一次低风险 rotation run：开发或 staging key 优先，记录验证和撤旧证据。
5. 写 `exposure-review`，即使没有泄露，也记录 detection controls 和下一项预防动作。
6. 把 verifier 接入 release/security checklist；真实项目中每月只处理一个最高风险 credential 改进。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“有哪些凭据、谁能读、怎么轮、轮过没有、泄露怎么办”。
- 保留：人只判断生产凭据、前端暴露、真实泄露、无法轮换/撤销和风险接受。
- 调整：不默认引入 Vault、PAM、HSM 或多云 secret 平台；早期用托管 secret manager、CI secrets、环境变量和清晰 metadata 足够。
- 调整：不要求一次性轮换所有 secret；先处理最高 blast radius、最长未轮换、owner 不清楚和 OpenAI/provider key。
- 风险：文档可能变成“凭据清单但没人轮”。缓解：`rotation-run` 和 `exposure-review` 必须留下验证和下一项行动。

结论：可落地。一个人可以在一个专注块内为最关键服务建立凭据事实来源，并先演练一次低风险轮换。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：凭据泄露会直接导致费用、数据、可用性和客户信任损失；本阶段把止血路径前置。
- 工程角度：Go/Kratos/sqlc/gRPC、Vite 和 AI workflow 的 secret 边界明确，避免凭据散落在代码、前端和 prompt 中。
- 运维角度：轮换有验证、回滚、撤旧和 evidence，不把 production key rotation 变成临场手术。
- 安全隐私角度：只记录引用和 redacted evidence，不保存真实值；泄露复盘连接阶段 44。
- 成本角度：OpenAI/API provider key 有 project、usage monitoring、rate/spend guard 和 revocation path，能降低盗用费用风险。

结论：可落地。阶段 54 把“别泄露 secret”变成可检查的 credential lifecycle 闭环。
