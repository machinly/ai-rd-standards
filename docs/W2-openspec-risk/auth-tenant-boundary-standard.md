# 身份认证、权限与租户边界规范
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/main.md 的场景触发规范命中“认证、授权、租户隔离、support/admin 访问或 AI 代用户操作”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/main.md。
## 目标

为一人公司定义一套可执行的身份、权限和租户隔离规范：每个用户可见服务都明确“谁在请求、代表哪个租户、能对哪些资源做什么、怎么审计、哪些动作必须人工确认”。目标不是搭完整 IAM 平台，而是避免最常见也最致命的安全事故：认证绕过、越权访问、跨租户数据泄露、管理员误用和 AI 工具越权。

本阶段默认技术路径：Go/Kratos middleware 负责认证上下文，gRPC metadata 只传横切信息，业务层做授权判断，sqlc query 必须带租户/owner 条件。浏览器登录可以使用外部 IdP / OIDC / session cookie；服务间调用优先短期 token 或 mTLS/OIDC，由具体部署环境决定。

## 本专项只解决什么

- 身份与权限边界的最小仓库工件。
- authn / authz / tenant context 的默认实现顺序。
- gRPC metadata、Kratos middleware、Go context 和 repository query 的边界。
- RBAC / ABAC 的一人公司裁剪。
- 租户隔离、对象级授权、属性级授权和安全测试。
- session/token/secrets 的最低要求。
- 审计日志、管理员动作和高风险动作的人工 checkpoint。
- 身份权限 skill 与本地检查脚本。

不在本阶段展开：自建 IdP、企业 SSO/SCIM 完整实现、合规认证、复杂策略引擎平台、零信任全栈改造、跨云 IAM。需要时单独开 OpenSpec change。

## 依据转译

- 《人月神话》：安全平台和权限框架不是银弹。权限复杂度来自业务对象、租户边界和例外，而不是缺一个更大的框架。
- 小型项目管理：只保留能阻止高损失事故和恢复上下文的工件：身份边界、权限矩阵、隔离测试、审计说明。
- Saltzer & Schroeder, The Protection of Information in Computer Systems：本专项采用 fail-safe defaults、complete mediation、least privilege、economy of mechanism。默认拒绝、每次访问都检查、权限最小化、机制保持简单。
- OWASP Authorization Cheat Sheet：权限设计阶段要枚举用户、资源、操作；默认拒绝；每个请求都验证权限；权限漂移需要复审。
- OWASP API Security Top 10 2023：BOLA、Broken Authentication、BOPLA、Broken Function Level Authorization 是 API 的核心风险，尤其是用户可改对象 ID 或字段时。
- OWASP Multi-Tenant Security：tenant context 必须早期建立并绑定到 authenticated session，不信任客户端随手传的 tenant id；需要防跨租户数据访问、缓存/会话/存储污染和 tenant context injection。
- OWASP Authentication / Session / Password / Logging Cheat Sheets：认证、会话、密码存储和安全日志要独立设计，不能只靠业务代码顺便实现。
- NIST SP 800-63-4：数字身份应按风险选择 IAL/AAL/FAL；一人公司不需要全量合规，但要用风险思路决定 MFA、federation 和账户恢复强度。
- NIST SP 800-207 Zero Trust：不要因为请求来自内网、后台任务或自家服务就隐式信任；身份和授权是离散函数，访问资源前完成。
- NIST RBAC / ABAC：先用小型 RBAC；当授权需要 subject、object、action、environment 属性组合时再引入 ABAC。
- IETF RFC 9700 / OAuth 2.0 Security BCP：OAuth 不是认证本身；使用 OAuth/OIDC 时要遵循现代安全实践，不使用隐式授权等过时模式。
- OpenID Connect Core：OIDC 通过 ID Token 表达认证结果；不要把 access token、ID token、session cookie 的用途混在一起。
- JWT RFC 7519：JWT 是 claims 表达格式，不等于完整安全方案；必须验证签名、issuer、audience、expiry 和算法。
- gRPC / Kratos 官方文档：gRPC metadata 可传认证凭据等横切信息；Kratos auth middleware 可对 HTTP/gRPC 请求做认证并把 claims 放入 context。

## 默认决策

- 默认使用外部 IdP / OIDC 或托管认证；一人公司不默认自建密码登录和账户恢复系统。
- 如果必须自建密码登录，必须遵循 OWASP/NIST：安全哈希、泄露密码检查、限速、MFA 计划、账户恢复防枚举。
- 默认 `deny by default`，没有明确 allow 的 action 一律拒绝。
- 默认每个用户可见对象访问都做 object-level authorization，不能只验证“已登录”。
- 默认租户上下文从已验证身份/session/claim + membership 派生，不信任客户端 header/query/body 里的 tenant id。
- 默认服务间调用也要认证；内网、同 VPC、同集群不等于可信。
- 默认使用 RBAC + 显式 owner/tenant checks；只有业务真的需要属性组合时再升级 ABAC。
- 默认 admin/superuser 是高风险能力，必须审计、最小化、可撤销，不在普通业务角色里混入。
- 默认 AI tool 或 agent 调用继承同一 actor/tenant/permission 边界，高风险工具仍需 human approval。

## Auth artifact 目录规范

推荐落点：

```text
auth/
  boundaries/<service>.json
  policies/<service>.json
  tests/<service>.jsonl
  audit/<service>.md
```

`auth/boundaries/<service>.json` 是机器可检查的身份边界事实来源：

```json
{
  "service": "workspace-api",
  "owner": "founder",
  "identity_provider": "managed-oidc",
  "authn": {
    "methods": ["oidc"],
    "mfa_required_for": ["owner", "admin"],
    "session_or_token": "httpOnly secure session cookie for browser; bearer token for gRPC service calls"
  },
  "transport": {
    "browser": "HTTPS",
    "service_to_service": "gRPC metadata authorization bearer token",
    "metadata_keys": ["authorization", "x-request-id", "x-tenant-context"]
  },
  "tenant": {
    "model": "shared database with tenant_id column",
    "context_source": "derived from verified membership, not trusted from client",
    "required_on_resources": ["workspace", "project", "invoice"]
  },
  "authorization": {
    "policy_file": "auth/policies/workspace-api.json",
    "default": "deny",
    "object_level": true,
    "property_level": true
  },
  "audit": {
    "file": "auth/audit/workspace-api.md",
    "events": ["login_failed", "permission_denied", "tenant_switch", "admin_action", "api_token_created"]
  },
  "tests": "auth/tests/workspace-api.jsonl",
  "human_checkpoint": {
    "required_for": ["new admin role", "cross-tenant support access", "service token with write permission", "AI tool with side effects"]
  }
}
```

`auth/policies/<service>.json` 是权限矩阵：

```json
{
  "service": "workspace-api",
  "default": "deny",
  "roles": ["owner", "admin", "member", "viewer"],
  "resources": ["workspace", "project", "invoice"],
  "permissions": [
    {
      "role": "owner",
      "resource": "workspace",
      "actions": ["read", "update", "delete"],
      "tenant_scope": "current_tenant",
      "conditions": ["membership_active", "mfa_for_delete"]
    },
    {
      "role": "viewer",
      "resource": "project",
      "actions": ["read"],
      "tenant_scope": "current_tenant",
      "conditions": ["membership_active"]
    }
  ],
  "high_risk_actions": ["delete_workspace", "export_user_data", "grant_admin", "create_service_token"],
  "admin_model": "break-glass admin requires audit event and reason"
}
```

`auth/tests/<service>.jsonl` 至少覆盖：

```json
{"id":"unauthenticated-read-denied","actor":"anonymous","tenant":"none","action":"read","resource":"workspace","expected":"deny","tags":["unauthenticated"]}
{"id":"viewer-cross-tenant-denied","actor":"viewer","tenant":"tenant-a","target_tenant":"tenant-b","action":"read","resource":"project","expected":"deny","tags":["cross_tenant","bola"]}
{"id":"viewer-delete-denied","actor":"viewer","tenant":"tenant-a","action":"delete","resource":"workspace","expected":"deny","tags":["forbidden_action"]}
{"id":"owner-delete-mfa-required","actor":"owner","tenant":"tenant-a","action":"delete_workspace","resource":"workspace","expected":"step_up_or_deny","tags":["high_risk"]}
```

一人公司裁剪规则：

- 第一版只定义当前服务真实角色，不预建企业角色树。
- 少于 5 个角色时不用引入外部 policy engine；在 Go 代码中集中实现 policy function，并用 JSON/测试守住矩阵。
- `super_admin` 不作为默认角色；需要时写成 break-glass 能力。
- 权限测试可以先是 JSONL + 手动/单元测试映射，后续再生成自动化测试。

## 实现顺序

1. 写 OpenSpec：用户、租户、资源、动作、不可做什么。
2. 写 `auth/boundaries/<service>.json`：身份来源、token/session、tenant context、audit、human checkpoint。
3. 写 `auth/policies/<service>.json`：角色、资源、动作、条件、默认拒绝。
4. 写 `auth/tests/<service>.jsonl`：至少未登录、同租户允许、跨租户拒绝、低权限拒绝、高风险 step-up。
5. 更新 `.proto`：不要把用户/租户权限作为业务字段随便传，除非它是业务对象本身。
6. 实现 Kratos auth middleware：验证 token/session，提取 subject、tenant memberships、roles、request id。
7. 在 biz/usecase 层做授权；repository 层 query 必须带 tenant/owner 条件。
8. 记录安全审计：失败登录、权限拒绝、租户切换、管理员动作、token 创建/撤销、AI 工具高风险调用。
9. 加 release gates：auth artifacts 检查、权限测试、SRE-lite/observability。

## gRPC / Kratos / Go 边界

- gRPC metadata 只作为传输层横切信息：`authorization`、`x-request-id`、trace、可信内部 context。
- `tenant_id` 可以出现在 metadata 中用于路由或 UX，但必须由服务端根据已验证身份和 membership 验证后才进入业务 context。
- Kratos middleware 负责认证和 context 注入；业务权限不要散落在每个 handler 的 if 里。
- `internal/service` 只做协议适配和参数校验；`internal/biz` 做授权和业务判断；`internal/data` 强制 tenant/owner query 条件。
- 不把完整 token、密码、secret、session id 写日志。

## 租户隔离规则

- 每个租户资源表默认有 `tenant_id` 或更强隔离模型；没有租户概念的资源必须在 design 中说明。
- 所有按 id 读取、更新、删除的 query 必须包含 tenant/owner 条件，避免只靠全局 id。
- cache key、object storage path、queue topic、background job、AI trace/eval 数据都必须带 tenant partition 或说明不需要。
- tenant switch、support impersonation、cross-tenant admin query 都是高风险动作，需要 audit reason。
- API 返回字段也要授权；不能因为对象级允许就返回所有敏感属性。

## Token / Session / Secret 规则

- Browser 默认使用 httpOnly、Secure、SameSite 合理配置的 session cookie；SPA/OIDC access token 存储策略必须在 design 中说明。
- JWT 必须验证 signature、issuer、audience、expiry、算法；不接受 `alg=none` 或未预期算法。
- Access token 默认短期；refresh token 或 session 可撤销。
- Service token 默认最小 scope、可轮换、可撤销，不与用户 token 混用。
- OAuth access token 用于授权访问资源；OIDC ID token 用于表达认证结果；不要混用。
- Secrets 存 CI/secret manager，不写入 `auth/*.json`、日志、migration、prompt 或测试样例。

## 审计与监控

`auth/audit/<service>.md` 最少写：

```markdown
# <service> Auth Audit
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/main.md 的场景触发规范命中“认证、授权、租户隔离、support/admin 访问或 AI 代用户操作”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/main.md。
## Events

## Fields

## Retention

## Privacy

## Alerts

## Review Cadence
```

默认审计事件：

- login success/failure、MFA challenge/failure。
- permission denied、cross-tenant denied。
- role/permission change。
- admin/break-glass action。
- service token created/revoked。
- API key created/revoked。
- AI tool high-risk call approved/denied。

审计日志必须有 actor、tenant、resource、action、decision、reason/request id、timestamp。隐私字段要最小化，避免把 secret、token、完整 PII 写进日志。

## 只问人的关键判断

默认不问：JSON 字段顺序、角色名小修正、测试 case id、audit 文档小节顺序、middleware 文件放哪里。

必须问：

- 是否自建密码登录，而不是托管 IdP/OIDC。
- 是否允许 support/admin 跨租户访问。
- 是否允许 service token 写生产数据。
- 是否允许 AI agent/tool 代表用户执行写操作。
- 是否新增 super admin、break-glass、impersonation。
- 是否处理医疗、金融、法律、未成年人、政府身份等高风险身份或敏感数据。
- 是否需要企业 SSO、SCIM、审计导出或合同安全承诺。

当前建议默认接受：所有用户可见服务必须有 `auth/boundaries/<service>.json`、`auth/policies/<service>.json`、`auth/tests/<service>.jsonl`、`auth/audit/<service>.md`；没有明确 allow 的动作默认 deny。

## 本专项 Review A：一人公司可落地性

结论：可落地，但必须避免一开始搭完整 IAM 平台。

- 四个 auth 工件足以让一个人恢复身份、租户、权限和审计上下文。
- 默认托管 IdP/OIDC，减少自建密码、MFA、恢复流程的高风险维护。
- 小型 RBAC + owner/tenant checks 比一开始引入复杂 policy engine 更适合单人产品。
- 最大摩擦是写权限测试；因此要求至少 4 条 JSONL case，并让 skill 脚本检查。
- 下一步应在第一个真实服务上用 `auth-boundary-guard` 生成 artifacts。

## 本专项 Review B：产品/工程/运维风险

结论：本专项主要降低越权和跨租户泄露风险。

- 已把 deny-by-default、每次请求授权、tenant context 不信任客户端、object/property-level authorization 写成硬约束。
- 已把 admin、support impersonation、service token、AI 写操作列为人工 checkpoint。
- 已要求审计事件和权限拒绝日志，连接 SRE/incident 后续处理。
- 已把 sqlc query 的 tenant/owner 条件纳入实现规则，连接 W4 数据迁移与数据访问规范。
- 仍不锁定具体 IdP 或 policy engine；真实项目可按成本和客户需求选择。


