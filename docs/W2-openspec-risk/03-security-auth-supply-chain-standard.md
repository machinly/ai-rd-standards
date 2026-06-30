# W2 触发专项：安全、隐私、Auth 与供应链边界规范

## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项，不是 W2 主入口。只有当当前 change 涉及威胁模型、数据处理、认证授权、租户隔离、support/admin 访问、secret、依赖供应链、构建来源或 AI 工具权限时，才读取本文件。

普通 W2 工作先回到 `docs/W2-openspec-risk/00-main.md`。

## 目标

把原先分散的安全隐私基线和 Auth/tenant 边界合并成一个实现前门禁：谁在请求、代表哪个租户、能访问什么数据，哪些外部输入和依赖可信，哪些 secret、构建、AI 工具或管理员能力必须被限制、审计和验证。

默认原则：默认拒绝、最小权限、每次访问都检查、secret 不进仓库/日志/prompt、AI/tool 输出不直接执行高风险副作用。

## 主要角色消费者

- Tech Lead：在 W2 锁定安全和权限边界。
- 后端：在 W4 实现 middleware、policy、query scope、audit 和供应链检查。
- 安全合规：在 W2/W5/W7 判断例外、事故和证据。

## 最小工件

```text
security/
  threat-models/<target>.md
  privacy/<target>.json
  supply-chain/<target>.json
  secrets/<target>.md

auth/
  boundaries/<target>.json
  policies/<target>.json
  tests/<target>.jsonl
  audit/<target>.md
```

可以先从一个 target 的最小版本开始，不要求一次覆盖全产品。

## 必须覆盖

- 资产、入口、信任边界、滥用场景、控制和未决风险。
- 数据分类、处理目的、外部处理方、保留、日志、删除/导出、AI 数据使用。
- 身份来源、session/token、tenant context、角色/资源/action、默认拒绝。
- object-level 和 tenant-level authorization；跨租户、support/admin、break-glass 必须审计。
- lockfile、依赖扫描、secret scanning、SBOM/provenance 计划、CI 最小权限。
- AI prompt injection、敏感信息泄露、不安全输出处理、工具越权。

## 默认实现规则

- 浏览器登录默认优先托管 IdP/OIDC；自建密码登录需要单独人审。
- tenant context 从已验证身份和 membership 派生，不信任客户端随手传入的 tenant id。
- Go/Kratos middleware 负责认证和 context 注入；biz/usecase 层做授权；sqlc query 必须带 tenant/owner 条件。
- gRPC metadata 只传认证、request id、trace 和必要横切信息；不传 secret 或完整敏感内容。
- AI agent/tool 调用继承 actor/tenant/permission，高风险工具还需要 dry-run、人审或审批。

## 需要人判断

- 自建密码登录、企业 SSO/SCIM、super admin、break-glass、impersonation。
- support/admin 跨租户访问，service token 写生产数据，AI 代用户执行写操作。
- 处理敏感个人数据、高影响领域数据或受监管数据。
- 新外部处理方、模型供应商、analytics/logging/support 工具接收用户数据。
- 接受 critical/high 漏洞、未签名 release、没有 SBOM/provenance 的客户交付物。
- 新 CI job 或外部 action 获得生产 secret、写权限或部署权限。

## Review A：一人可执行性

本专项把安全隐私和 Auth 收成两组最小工件，避免 W2 同时打开多份高重叠治理文档。一个人可以先为当前 target 写 thin slice，再把未覆盖项交给 W5/W7。

## Review B：产品 / 工程 / 运维风险

保留了越权、跨租户、secret、供应链、AI 工具和数据处理这些高损失风险的独立门禁；不再保留重复入口。最小安全下一步是让每个高影响 OpenSpec change 链接安全/Auth 工件或写明不适用原因。

