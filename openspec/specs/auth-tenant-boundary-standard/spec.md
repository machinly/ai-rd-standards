# auth-tenant-boundary-standard Specification

## Purpose

定义一人公司身份认证、授权和租户隔离的最小规范，使用户可见服务能明确 actor、tenant、resource、action、decision、audit 和 high-risk checkpoint，降低越权访问和跨租户数据泄露风险。

## Requirements

### Requirement: 用户可见服务必须定义身份与租户边界

用户可见服务 MUST 在实现认证、权限或租户相关功能前具备身份与租户边界 artifact。

#### Scenario: 新服务需要认证

- GIVEN 一个用户可见服务需要认证或租户隔离
- WHEN 创建 auth artifacts
- THEN 创建 `auth/boundaries/<service>.json`
- AND 文件包含 `service`、`owner`、`identity_provider`、`authn`、`transport`、`tenant`、`authorization`、`audit`、`tests`

#### Scenario: 服务无登录用户

- GIVEN 服务只被内部 worker 或服务间调用使用
- WHEN 不定义浏览器用户身份
- THEN 仍需记录 service identity、token/credential 来源、权限 scope 和审计事件

### Requirement: 授权必须默认拒绝并每次请求检查

服务授权 MUST 使用 deny-by-default，并在每个受保护请求上验证 actor、tenant、resource、action。

#### Scenario: 创建权限矩阵

- GIVEN 一个服务定义权限
- WHEN 创建 `auth/policies/<service>.json`
- THEN `default` 为 `deny`
- AND 文件包含 roles、resources、permissions
- AND 每条 permission 包含 role、resource、actions、tenant_scope

#### Scenario: 未匹配权限

- GIVEN 一个请求没有匹配的 allow rule
- WHEN 进行授权判断
- THEN 拒绝请求
- AND 记录 permission denied 审计事件或指标

### Requirement: 租户上下文不得直接信任客户端输入

服务 MUST 从已验证身份和 membership 派生 tenant context，不得直接信任客户端传入的 tenant id。

#### Scenario: 请求包含 tenant id

- GIVEN 请求 header、metadata、query 或 body 中包含 tenant id
- WHEN 服务建立 tenant context
- THEN 验证该 tenant id 属于已认证 subject 的 membership
- AND 将验证后的 tenant context 注入业务 context

#### Scenario: 按对象 id 访问资源

- GIVEN 请求通过 id 读取、更新或删除资源
- WHEN 查询数据库或下游服务
- THEN 同时验证 tenant/owner 条件
- AND 不得只依赖全局 id

### Requirement: 权限测试必须覆盖越权与跨租户场景

服务 MUST 维护最小 auth 测试 fixtures，覆盖未登录、低权限、跨租户和高风险动作。

#### Scenario: 创建 auth tests

- GIVEN 一个用户可见服务
- WHEN 创建 `auth/tests/<service>.jsonl`
- THEN 至少包含 4 条 case
- AND 覆盖 `unauthenticated`、`cross_tenant`、`forbidden_action`、`high_risk` 标签
- AND 每条 case 包含 `id`、`actor`、`action`、`resource`、`expected`

#### Scenario: 修改权限

- GIVEN 修改 role、permission、tenant model 或 admin behavior
- WHEN 准备发布
- THEN 更新 auth tests
- AND 在 release 或 OpenSpec tasks 中记录预期行为变化

### Requirement: 高风险身份和权限动作必须审计并人工 checkpoint

Admin、break-glass、impersonation、service token 写权限、AI 写操作和跨租户访问 MUST 具备审计记录和人工 checkpoint。

#### Scenario: 创建高风险能力

- GIVEN 新增高风险权限能力
- WHEN 更新 auth artifacts
- THEN `human_checkpoint.required_for` 记录该能力
- AND `auth/audit/<service>.md` 记录事件、字段、保留期、隐私和告警

#### Scenario: AI tool 代表用户写入

- GIVEN AI workflow 或 agent 会代表用户执行写操作
- WHEN 定义工具权限
- THEN 继承 actor、tenant、permission 边界
- AND 高风险写操作需要 human approval 或 dry-run

### Requirement: Token、session 和 secret 必须用途清晰

服务 MUST 区分 session cookie、access token、ID token、service token 和 secret 的用途，并禁止泄漏到日志或仓库。

#### Scenario: 使用 JWT/OIDC

- GIVEN 服务使用 JWT 或 OIDC
- WHEN 验证请求
- THEN 验证 signature、issuer、audience、expiry 和算法
- AND 不把 ID token 当作 API access token 使用

#### Scenario: 日志记录请求

- GIVEN 请求包含 password、secret、session id 或 token
- WHEN 写日志或审计事件
- THEN 不记录完整敏感值
- AND 至多记录可关联的安全摘要或 token id

### Requirement: 安全审计必须覆盖身份和权限事件

服务 MUST 记录关键身份、权限和租户隔离事件，且日志字段最小化。

#### Scenario: 创建 audit 文档

- GIVEN 服务进入生产
- WHEN 创建 `auth/audit/<service>.md`
- THEN 文档包含 Events、Fields、Retention、Privacy、Alerts、Review Cadence
- AND 至少覆盖 login failure、permission denied、role change、admin action、service token lifecycle
