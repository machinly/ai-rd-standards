# 任务

## 1. 来源与约束

- [x] 1.1 查证 OWASP Authorization、Authentication、Session、Logging、Multi-Tenant、API Security Top 10。
- [x] 1.2 查证 NIST SP 800-63-4、SP 800-207、RBAC、ABAC。
- [x] 1.3 查证 IETF OAuth Security BCP、JWT、OpenID Connect、gRPC/Kratos auth 官方文档。
- [x] 1.4 补充 W2 auth/tenant 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 身份权限规范

- [x] 2.1 编写 W2 auth/tenant 规范正文。
- [x] 2.2 定义 `auth/boundaries`、`auth/policies`、`auth/tests`、`auth/audit` artifacts。
- [x] 2.3 定义 authn/authz/tenant context、token/session、审计和人工 checkpoint 规则。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建 W2 auth/tenant change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `auth-boundary-guard` skill。
- [x] 4.2 添加 auth artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 auth boundary 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实服务 auth artifacts，因此不运行真实身份系统测试。

验证说明：本仓库是规范仓库，不包含真实服务 auth artifacts，也不应在规范阶段连接真实 IdP 或执行真实登录/权限测试。已通过 `verify_auth_boundary.py` 的临时 `workspace-api` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `auth/boundaries`。
