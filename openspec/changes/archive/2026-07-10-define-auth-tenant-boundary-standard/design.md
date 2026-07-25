# 设计：身份认证、权限与租户边界规范

## 设计决策

### 1. 用四个工件表达 auth 边界

`auth/boundaries` 记录身份来源、tenant context、token/session 和 audit；`auth/policies` 记录权限矩阵；`auth/tests` 记录最小越权测试；`auth/audit` 记录审计事件。这样一个人可以恢复上下文，脚本也能检查缺项。

### 2. 默认托管身份，不默认自建密码

自建密码登录、账户恢复、MFA 和风控成本高且容易出错。一人公司默认使用托管 IdP/OIDC；只有产品明确需要时才自建。

### 3. 授权在业务层集中实现

Kratos middleware 认证身份并把 claims/context 放入 Go context；`internal/biz` 执行授权；`internal/data` 强制 tenant/owner query 条件。避免权限散落在 handler 或前端。

### 4. 租户上下文必须绑定已验证身份

客户端可传 tenant id 用于 UX 或路由，但不能直接信任。服务端必须从已认证 subject 的 membership 派生当前 tenant context。

### 5. 小型 RBAC 优先，ABAC 按需升级

少量角色和资源时，JSON 权限矩阵 + Go policy function 最可维护。需要 subject/object/action/environment 属性组合时，再引入 ABAC 或策略引擎。

### 6. 高风险能力必须审计和 checkpoint

support impersonation、break-glass admin、service token 写权限、AI tool 写操作、跨租户查询都需要 audit reason 和人工确认。

## 取舍

- JSON 工件增加少量书写成本，但能被脚本检查。
- 不强制 policy engine 降低早期复杂度，但要求权限测试补足信心。
- 不锁定 IdP，避免供应商选择提前固化。
- 不把租户隔离只放在数据库层，要求 API、cache、storage、job、AI traces 同步考虑。
