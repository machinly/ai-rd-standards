# 提案：定义身份认证、权限与租户边界规范

## 意图

为一人公司建立可检查的身份、权限和租户隔离规范，让每个用户可见服务明确 actor、tenant、resource、action、decision、audit 和 human checkpoint，降低认证绕过、越权访问、跨租户数据泄露和 AI 工具越权风险。

## 范围

- 定义 auth artifacts 目录和最小文件。
- 定义 authn/authz/tenant context 的默认实现顺序。
- 定义 gRPC metadata、Kratos middleware、Go context、sqlc query 的边界。
- 定义 RBAC/ABAC 裁剪、object/property-level authorization、租户隔离测试。
- 定义 session/token/secrets、审计日志、高风险动作和人工 checkpoint。
- 创建身份权限落地 skill 和检查脚本。

## 不做

- 不实现真实 IdP、SSO、SCIM 或策略引擎。
- 不定义法律合规结论。
- 不默认自建密码登录。
- 不建立复杂零信任平台。

## 依据

- 《人月神话》：权限框架不是银弹，复杂度来自业务对象、租户和例外。
- 小型项目管理：只保留阻止高损失安全事故和恢复上下文的最小工件。
- Saltzer & Schroeder：fail-safe defaults、complete mediation、least privilege、economy of mechanism。
- OWASP Authorization、Authentication、Session、Logging、Multi-Tenant Security、API Security Top 10。
- NIST SP 800-63-4、SP 800-207、RBAC、ABAC。
- IETF RFC 9700、RFC 7519、OpenID Connect Core。
- gRPC metadata/auth 和 Kratos auth middleware 官方文档。

## 需要人的判断

建议默认：所有用户可见服务必须有 `auth/boundaries/<service>.json`、`auth/policies/<service>.json`、`auth/tests/<service>.jsonl`、`auth/audit/<service>.md`；没有明确 allow 的动作默认 deny。
