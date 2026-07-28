# 实现：凭据与 secret 实现边界

## 执行细则

<!-- rule-id: IMPL-SECRET-ALLOWED-STORAGE -->
- 对真实 secret 值实行存储白名单：允许的载体仅为短期环境变量、开发者本机的受保护存储、云平台、CI secrets 与 secret manager。

<!-- rule-id: IMPL-CREDENTIAL-SCOPE-SET -->
- 凭据治理的实现范围是一个封闭集合，按用途包括：MCP/connector token 与 RAG/vector store；encryption key、JWT signing key、TLS/private key、deploy token 与 cloud IAM；CI/CD、monitoring、analytics、OAuth client 与 Webhook；数据库、对象存储、短信、邮件、支付，以及 OpenAI 或其他模型供应商。

<!-- rule-id: IMPL-CREDENTIAL-STORAGE-REF -->
- `storage_ref` 禁止保存 secret value。该字段的允许值只表示位置或标识，可写本地占位说明、version id、key id、cloud resource id、CI secret name 或 secret manager path。

<!-- rule-id: IMPL-AI-NO-REAL-SECRET-ACCESS -->
- Codex 或其他 AI agent 禁止读取真实 secret。

<!-- rule-id: IMPL-CI-SHORT-LIVED-IDENTITY -->
- CI 缺省使用 OIDC/federated identity 或短期 token。

<!-- rule-id: IMPL-FRONTEND-CREDENTIAL-BAN -->
- Vite 前端不得承载任何能够替代后端身份的凭据，明确包括 JWT secret、service token、数据库 URL、OpenAI key 与 API key。

<!-- rule-id: IMPL-EXPOSED-CREDENTIAL-REVOKE-FIRST -->
- 一旦发现真实值属于 session cookie、OAuth refresh token、CI token、Webhook secret、private key、database URL、OpenAI key 或 production credential 中任一类，处理顺序必须先撤销或轮换，随后才清理历史。

<!-- rule-id: IMPL-KRATOS-SECRET-REFERENCE-ONLY -->
- 交给 Kratos config struct 的内容仅可采用两种形态：secret reference，或已经在运行时完成注入的配置对象。

<!-- rule-id: IMPL-NO-BUSINESS-OPENAI-GETENV -->
- 业务代码禁止散落读取 `os.Getenv("OPENAI_API_KEY")`。

<!-- rule-id: IMPL-GRPC-CREDENTIAL-ENCRYPTED-CHANNEL -->
- gRPC call credentials 禁止在未加密 channel 上传输。

<!-- rule-id: IMPL-FRONTEND-PRIVATE-SERVICE-PROXY -->
- 浏览器需要访问私有 API、数据库、对象存储、支付或 OpenAI 时，secret 须留在后端；请求必须通过 serverless function、BFF 或后端中的一种代理边界。

<!-- rule-id: IMPL-AI-ARTIFACT-SECRET-BAN -->
- 真实 secret 缺省禁止进入任何 AI 内容载体；受约束的表面依次为 support transcript、RAG source、memory、trace、eval fixture、tool output 与 AI prompt。
