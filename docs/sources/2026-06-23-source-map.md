# 来源索引 - 2026-06-23 起持续维护

本文件只记录各 W 和触发专项要反复引用的高价值来源。W5 测试质量专项于 2026-06-24 补充。具体规范正文只摘取可落地的原则，不复制大段原文。

## 规格与 AI 辅助研发

- OpenSpec 官网与 README：强调规格在代码库中、每个变更包含 proposal/spec/design/tasks，并先审查意图再写代码。
  - https://openspec.dev/
  - https://github.com/Fission-AI/OpenSpec
  - https://raw.githubusercontent.com/Fission-AI/openspec/main/docs/getting-started.md
  - https://raw.githubusercontent.com/Fission-AI/openspec/main/docs/commands.md
- Anthropic, Building Effective Agents：优先简单方案；任务清楚时用 workflow，开放问题才用 agent；谨慎引入框架抽象。
  - https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Prompt Engineering：生产 prompt 应进入代码、使用类型化输入、代码评审、测试和部署流程。
  - https://developers.openai.com/api/docs/guides/prompt-engineering
- OpenAI Prompting / Prompt Guidance：不同模型的 prompt 行为会变化，prompt 需要结合产品表面、工具、eval 和用户体验目标调整。
  - https://developers.openai.com/api/docs/guides/prompting
  - https://developers.openai.com/api/docs/guides/prompt-guidance
- OpenAI Evaluation Best Practices：生成式 AI 需要 eval；早做、持续做、贴近真实任务分布，并结合人工校准。
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
- OpenAI Datasets / Agent Evals：先用 traces 调试行为；明确“好”的定义后，迁移到可重复 datasets 和 eval runs。注意：OpenAI 旧 Evals platform 将在 2026-10-31 对现有用户只读，并计划在 2026-11-30 关闭。
  - https://developers.openai.com/api/docs/guides/evaluation-getting-started
  - https://developers.openai.com/api/docs/guides/agent-evals
  - https://developers.openai.com/api/docs/guides/evals
- OpenAI Agents / Tools / Structured Outputs / Safety：Responses API 适合一次模型调用加工具和应用自有逻辑；Agents SDK 适合应用拥有编排、工具执行、审批和状态；工具、结构化输出和安全边界需要明确。
  - https://developers.openai.com/api/docs/guides/agents
  - https://developers.openai.com/api/docs/guides/tools
  - https://developers.openai.com/api/docs/guides/structured-outputs
  - https://developers.openai.com/api/docs/guides/agent-builder-safety
  - https://developers.openai.com/api/docs/guides/safety-best-practices
  - https://developers.openai.com/api/docs/guides/production-best-practices
- Google Rules of Machine Learning：先保证 pipeline 和指标扎实；能不用 ML 时先用简单启发式；复杂度会拖慢未来发布。
  - https://developers.google.com/machine-learning/guides/rules-of-ml
- Microsoft LLM Red Teaming：红队不是系统度量的替代品，但适合早期发现应用上下文中的风险面。
  - https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/red-teaming

## 项目管理与小型项目

- Frederick P. Brooks, The Mythical Man-Month：用于约束进度幻觉、复杂度幻觉和“没有银弹”的判断。
  - https://www.amazon.com/Mythical-Man-Month-Software-Engineering-Anniversary/dp/0201835959
  - https://en.wikipedia.org/wiki/The_Mythical_Man-Month
- Sandra F. Rowe, Project Management for Small Projects：用于把项目管理裁剪到小项目可承受的最小形态。
  - https://www.skillsoft.com/book/project-management-for-small-projects-third-edition-ca85d9c4-0cc7-457f-af63-7771c846b675
  - https://www.amazon.com/Project-Management-Small-Projects-Sandra/dp/1567264743

## W7 Operate 触发专项：SRE-lite 运维与可靠性依据


- Google SRE Book：后续运维规范的主参考，包括 SLO、toil、监控、发布、简化。
  - https://sre.google/sre-book/table-of-contents/
- Google SRE Workbook, Implementing SLOs：SLO、error budget policy、监控与复审节奏。
  - https://sre.google/workbook/implementing-slos/
- Google SRE Workbook, Alerting on SLOs：告警应围绕用户体验、SLI 和 error budget 消耗，关注 precision、recall、detection time、reset time。
  - https://sre.google/workbook/alerting-on-slos/
- Google SRE, Monitoring Distributed Systems：最小监控优先 latency、traffic、errors、saturation 四个黄金信号，paging 更适合黑盒用户症状。
  - https://sre.google/sre-book/monitoring-distributed-systems/
- Google SRE Workbook, On-Call：值班应匹配服务关键性和人的健康，小团队不能默认照搬大型轮班。
  - https://sre.google/workbook/on-call/
- Google SRE Workbook, Incident Response：事故响应需要预先约定结构、记录、角色和沟通，以降低混乱。
  - https://sre.google/workbook/incident-response/
- Google SRE Workbook, Postmortem Culture：复盘要记录影响、根因、恢复和行动项，避免指责，行动项必须可追踪。
  - https://sre.google/workbook/postmortem-culture/
- Google SRE Workbook, Canarying Releases / SRE Book Release Engineering：发布应可重复、自动化、小批量、可回滚；canary 是高风险发布的渐进方式。
  - https://sre.google/workbook/canarying-releases/
  - https://sre.google/sre-book/release-engineering/
- Google SRE, Eliminating Toil / Automation at Google：toil 是重复、手动、随规模增长的运维劳动；自动化要谨慎服务于系统设计。
  - https://sre.google/sre-book/eliminating-toil/
  - https://sre.google/sre-book/automation-at-google/
- DORA software delivery performance metrics：2026-06-23 查到官方文档采用吞吐与不稳定性视角，包括 change lead time、deployment frequency、failed deployment recovery time、change fail rate、deployment rework rate。
  - https://dora.dev/guides/dora-metrics/
- OpenTelemetry：vendor-neutral observability 框架，应用通过 traces、metrics、logs 发出遥测，后端和可视化由其他工具承担。
  - https://opentelemetry.io/docs/what-is-opentelemetry/
  - https://opentelemetry.io/docs/languages/go/

## 技术栈官方文档

- Kratos：Go 微服务框架，Protobuf 定义 API，HTTP/gRPC 传输，内建 middleware、metrics、tracing、config 等能力。2026-06-23 查到当前官方 README 推荐 Kratos v3、Go 1.25+、`protoc`、`protoc-gen-go`。
  - https://go-kratos.dev/docs/
  - https://go-kratos.dev/docs/intro/design/
  - https://github.com/go-kratos/kratos
  - https://github.com/go-kratos/kratos-layout
- sqlc：从 SQL 生成类型安全、惯用 Go 代码。
  - https://docs.sqlc.dev/
  - https://sqlc.dev/
  - https://docs.sqlc.dev/en/latest/reference/config.html
  - https://docs.sqlc.dev/en/latest/howto/vet.html
- gRPC Go：定义 `.proto`、生成服务端/客户端代码、实现 Go gRPC 服务。
  - https://grpc.io/docs/languages/go/
  - https://grpc.io/docs/languages/go/basics/
  - https://grpc.io/docs/guides/health-checking/
  - https://grpc.io/docs/what-is-grpc/core-concepts/
- Protobuf Go：Go 代码生成行为与语言绑定。
  - https://protobuf.dev/reference/go/go-generated/
  - https://protobuf.dev/programming-guides/proto3/
- Go 官方文档：模块、工作区、测试与语言规范。
  - https://go.dev/doc/
  - https://pkg.go.dev/testing
- OpenTelemetry Go：后续观测性规范参考。
  - https://opentelemetry.io/docs/languages/go/
  - https://opentelemetry.io/docs/languages/go/instrumentation/
- Vite：前端工具链与生产构建。
  - https://vite.dev/guide/
  - https://vite.dev/guide/build
  - https://vite.dev/guide/env-and-mode
  - https://vite.dev/guide/static-deploy
- Vitest：Vite 原生测试框架，用于一人公司前端最小测试门禁。
  - https://vitest.dev/guide/
- Vercel Geist Design System：浅色与深色主题参考。
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md
  - https://vercel.com/geist/introduction
  - https://vercel.com/geist/colors
  - https://vercel.com/geist/grid

## W4 Build 触发专项：Vite 前端体验与可访问性依据


- Web Vitals：用 LCP、INP、CLS 衡量真实用户体验。
  - https://web.dev/articles/vitals
- WCAG 2.2：最低对比度、键盘、焦点、输入等可访问性要求。
  - https://www.w3.org/TR/WCAG22/
  - https://www.w3.org/WAI/WCAG22/quickref/
- MDN Accessibility：语义化 HTML、表单标签、键盘可达性和源码顺序是前端可访问性的低成本起点。
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML

## W4 Build 触发专项：Go/Kratos 服务端最小 SRE 依据


- Google SRE, Simplicity：可靠性来自简化、最小 API、模块化和小批量发布。
  - https://sre.google/sre-book/simplicity/
- Google SRE, Release Engineering：可靠服务需要可重复、自动化、可追溯的构建发布过程。
  - https://sre.google/sre-book/release-engineering/
- Google SRE, Monitoring Distributed Systems：最小监控优先看 latency、traffic、errors、saturation 四个黄金信号。
  - https://sre.google/sre-book/monitoring-distributed-systems/

## W3 AI Behavior 触发专项：AI prompt / eval / agent workflow 依据


- Anthropic, Building Effective Agents：优先简单可组合模式；workflows 适合固定路径，agents 适合开放任务；复杂度只有能证明改善结果时才增加。
  - https://www.anthropic.com/engineering/building-effective-agents
- Google Rules of ML：第一版模型或 AI 能力应保持简单，先把 pipeline、good/bad 定义和集成方式做可信。
  - https://developers.google.com/machine-learning/guides/rules-of-ml
- Google SRE Monitoring：AI 能力上线也要有 latency、traffic、errors、saturation 等用户可见信号。
  - https://sre.google/sre-book/monitoring-distributed-systems/

## W6 Release 触发专项：发布流水线依据


- Twelve-Factor App, Build/Release/Run：严格分离 build、release、run；release 是 append-only ledger，并应有唯一 release id。
  - https://12factor.net/build-release-run
- Google SRE, Release Engineering：发布过程应默认正确、文档充分、自助可用、可回滚。
  - https://sre.google/sre-book/release-engineering/
- Google SRE Workbook, Canarying Releases：测试环境无法完全覆盖生产，风险发布应小批量暴露真实流量并观察信号。
  - https://sre.google/workbook/canarying-releases/
- DORA software delivery performance metrics：吞吐与不稳定性要一起看；小批量变化更容易通过流水线和从失败恢复。
  - https://dora.dev/guides/dora-metrics/
- GitHub Actions workflow syntax / secure use / OIDC：workflow 是 YAML 定义的自动化过程；`GITHUB_TOKEN` 应最小权限；云部署优先 OIDC 短期凭证。
  - https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions
  - https://docs.github.com/en/actions/reference/security/secure-use
  - https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-cloud-providers
- GitHub Artifact Attestations：为发布 artifact 建立 provenance 和 integrity claims，适合外部可运行 artifact。
  - https://docs.github.com/en/actions/concepts/security/artifact-attestations
- Docker Multi-stage Builds / attestations：生产镜像只复制运行需要的 artifact；容器镜像可添加 SBOM 和 provenance attestations。
  - https://docs.docker.com/build/building/multi-stage/
  - https://docs.docker.com/build/ci/github-actions/attestations/
- Go testing / race detector：Go 测试使用 `go test`；并发风险可用 `go test -race`，但它只能发现被执行路径中的 race。
  - https://pkg.go.dev/testing
  - https://go.dev/doc/articles/race_detector
- sqlc vet：`sqlc vet` 用配置中的 lint rules 检查 SQL queries。
  - https://docs.sqlc.dev/en/latest/howto/vet.html
- Vite build / Vercel deployments：Vite 生产构建使用 `vite build`；Vercel 支持 Git、CLI、Deploy Hooks、REST API，并区分 Local、Preview、Production。
  - https://vite.dev/guide/build
  - https://vercel.com/docs/deployments

## W4 Build 触发专项：数据与数据库迁移依据


- Designing Data-Intensive Applications：数据系统设计围绕可靠性、可维护性、可扩展性和工具权衡；一人公司应优先简单、清晰、可恢复的数据路径。
  - https://dataintensive.net/
  - https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/
- Database Reliability Engineering：把 SRE 思想应用到数据库，强调保护数据、风险管理、备份恢复、发布管理、安全和操作可见性。
  - https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/
- Evolutionary Database Design：数据库 artifacts 与应用代码一起版本化；所有数据库变化都是 migrations；小步变更更容易验证和恢复。
  - https://martinfowler.com/articles/evodb.html
  - https://databaserefactoring.com/
- PostgreSQL Backup and Restore / SQL Dump / PITR：PostgreSQL 18 文档列出 SQL dump、文件系统备份、连续归档三类备份；`pg_dump` 提供一致快照但不等同 PITR。
  - https://www.postgresql.org/docs/current/backup.html
  - https://www.postgresql.org/docs/current/backup-dump.html
  - https://www.postgresql.org/docs/current/continuous-archiving.html
- PostgreSQL Modifying Tables：DDL 会影响现有数据、约束和类型转换，ALTER 需要理解锁、重写和兼容性风险。
  - https://www.postgresql.org/docs/current/ddl-alter.html
- sqlc PostgreSQL tutorial / vet / config：sqlc 从 schema 和 queries 生成 Go 代码；`sqlc vet` 可 lint/prepare queries，但依赖已应用 schema 的数据库或 managed database。
  - https://docs.sqlc.dev/en/latest/tutorials/getting-started-postgresql.html
  - https://docs.sqlc.dev/en/latest/howto/vet.html
  - https://docs.sqlc.dev/en/latest/reference/config.html
  - https://docs.sqlc.dev/en/latest/howto/ddl.html
- golang-migrate：Go migration CLI/library，按顺序应用 migration；常见文件约定是 `*.up.sql` / `*.down.sql`。
  - https://github.com/golang-migrate/migrate
- OWASP Database Security / Secrets Management：数据库需要定期备份，备份需权限保护和加密；secrets 需要集中管理、轮换和最小权限。
  - https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- NIST Privacy Framework / GDPR Article 5：用于提示个人数据处理的风险管理、数据最小化、保留限制和完整性/机密性。
  - https://www.nist.gov/privacy-framework
  - https://gdpr-info.eu/art-5-gdpr/

## W2 OpenSpec / Risk 触发专项：身份认证、权限与租户边界依据


- Saltzer & Schroeder, The Protection of Information in Computer Systems：采用 fail-safe defaults、complete mediation、least privilege、economy of mechanism 约束一人公司权限设计。
  - https://web.mit.edu/saltzer/www/publications/protection/
  - https://www.cs.virginia.edu/~evans/cs551/saltzer/
- OWASP Authorization Cheat Sheet：权限设计阶段枚举用户、资源、操作；默认拒绝；每个请求检查权限；定期复审权限漂移。
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Authentication / Session Management / Password Storage：认证、会话和密码存储需要独立设计；自建密码登录不是一人公司默认选项。
  - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- OWASP API Security Top 10 2023：BOLA、Broken Authentication、BOPLA、Broken Function Level Authorization 是 API 权限设计的主要风险。
  - https://owasp.org/www-project-api-security/
  - https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
  - https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/
- OWASP Multi-Tenant Security：tenant context 应在请求生命周期早期建立，绑定 authenticated session，不信任客户端直接传入 tenant id。
  - https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
- OWASP Logging Cheat Sheet：安全事件日志要覆盖身份和权限事件，但避免记录敏感值。
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- NIST SP 800-63-4 Digital Identity Guidelines：2026-06-23 查到当前 NIST SP 800-63-4 已在 2025-07-31 final，并取代 800-63-3；身份、认证、联邦按 IAL/AAL/FAL 风险选择控制。
  - https://pages.nist.gov/800-63-4/
  - https://csrc.nist.gov/pubs/sp/800/63/4/final
- NIST SP 800-207 Zero Trust Architecture：身份和授权不应因网络位置或资产归属被隐式信任；访问资源前完成认证和授权。
  - https://csrc.nist.gov/pubs/sp/800/207/final
- NIST RBAC / ABAC：RBAC 适合小型角色矩阵；ABAC 在需要 subject/object/action/environment 属性组合时使用。
  - https://csrc.nist.gov/projects/role-based-access-control
  - https://www.nist.gov/publications/guide-attribute-based-access-control-abac-definition-and-considerations-1
- OAuth / OIDC / JWT：RFC 9700 是 OAuth 2.0 Security Best Current Practice；OIDC ID Token 表达认证结果；JWT 是 claims 格式而非完整安全方案。
  - https://datatracker.ietf.org/doc/rfc9700/
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://datatracker.ietf.org/doc/html/rfc7519
- gRPC / Kratos auth：gRPC metadata 可传认证凭据等横切信息；Kratos auth middleware 支持 HTTP/gRPC JWT 认证并把 claims 放入 context。
  - https://grpc.io/docs/guides/auth/
  - https://grpc.io/docs/guides/metadata/
  - https://go-kratos.dev/docs/component/middleware/auth/

## W2 OpenSpec / Risk 触发专项：成本、容量与供应商边界依据


- FinOps Framework：把技术花费管理成工程、财务和业务协作的操作模型；W2 成本容量专项裁剪为预算、单位成本、成本驱动和可行动阈值。
  - https://www.finops.org/framework/
  - https://www.finops.org/framework/capabilities/planning-estimating/
  - https://www.finops.org/framework/capabilities/unit-economics/
- Google SRE Handling Overload / Cascading Failures / NALSD：容量上限、过载处理、提前拒绝、低成本降级和容量规划要进入设计与 runbook。
  - https://sre.google/sre-book/handling-overload/
  - https://sre.google/sre-book/addressing-cascading-failures/
  - https://sre.google/workbook/non-abstract-design/
- OpenAI API Rate Limits / Production Best Practices / Cost Optimization / Prompt Caching：AI 服务同时受请求、token、模型、项目和月度 usage limit 约束；生产应用要管理 billing limits；缓存、Batch/Flex 等可用于成本与延迟优化。
  - https://developers.openai.com/api/docs/guides/rate-limits
  - https://developers.openai.com/api/docs/guides/production-best-practices
  - https://developers.openai.com/api/docs/guides/cost-optimization
  - https://developers.openai.com/api/docs/guides/prompt-caching
- OWASP API Security 2023 API4/API10：缺少资源限制会导致 DoS 或运营成本上升；第三方 API 消费也需要超时、资源限制和数据校验。
  - https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/
  - https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/
- Twelve-Factor App Backing Services：外部依赖应作为 attached resources，通过配置连接并尽量可替换。
  - https://12factor.net/backing-services
- AWS Well-Architected Cost Optimization / Google Cloud Costs and Usage：云成本管理共同强调花费可见性、预算告警、配额、资源效率和持续优化。
  - https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html
  - https://docs.cloud.google.com/docs/costs-usage

## W2 OpenSpec / Risk 触发专项：安全、隐私与供应链基线依据


- Ross Anderson, Security Engineering / Saltzer & Schroeder：安全工程要把错误、攻击者、激励和人类误操作纳入系统设计；W2 安全隐私专项继续采用 least privilege、fail-safe defaults、complete mediation 和 economy of mechanism。
  - https://www.cl.cam.ac.uk/archive/rja14/book.html
  - https://web.mit.edu/saltzer/www/publications/protection/
- Threat Modeling Manifesto / OWASP Threat Modeling：威胁建模用于改进开发期安全隐私；最小四问是“在做什么、会出什么错、如何处理、是否足够”。
  - https://www.threatmodelingmanifesto.org/
  - https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
- NIST SSDF SP 800-218：安全软件开发实践应集成进 SDLC，用于减少漏洞、降低未修复漏洞影响并处理根因。
  - https://csrc.nist.gov/pubs/sp/800/218/final
- OWASP SAMM / ASVS / Cheat Sheets / Secrets Management：安全保障应按风险迭代；ASVS 可作为应用安全验证基线；secrets 需要集中存储、访问控制、审计、轮换和泄露响应。
  - https://owasp.org/www-project-samm/
  - https://owasp.org/www-project-application-security-verification-standard/
  - https://cheatsheetseries.owasp.org/index.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- OWASP Top 10 for LLM Applications 2025：LLM 应用重点关注 prompt injection、sensitive information disclosure、supply chain 等风险。
  - https://genai.owasp.org/llm-top-10/
- OpenAI Data Controls / Safety Best Practices：API 使用涉及 abuse monitoring logs、应用状态和数据保留控制；生产 AI 应用需要 moderation、adversarial testing、human oversight 和 prompt 边界。
  - https://developers.openai.com/api/docs/guides/your-data
  - https://developers.openai.com/api/docs/guides/safety-best-practices
- NIST Privacy Framework / NIST AI RMF Generative AI Profile：隐私风险和生成式 AI 风险应在设计、开发、使用和评估中管理。
  - https://www.nist.gov/privacy-framework
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- SLSA / CycloneDX：供应链安全要防 tampering、提升 artifact integrity，并用 BOM 描述组件和供应链风险。
  - https://slsa.dev/
  - https://cyclonedx.org/
- Go / GitHub / npm 官方安全文档：Go 使用 `govulncheck` 查找实际影响代码路径的漏洞；GitHub 提供 secret scanning、CodeQL、Dependabot 和 artifact attestations；npm audit 可按漏洞级别失败。
  - https://go.dev/doc/security/vuln/
  - https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
  - https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning
  - https://docs.github.com/code-security/dependabot/dependabot-alerts/about-dependabot-alerts
  - https://docs.github.com/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds
  - https://docs.npmjs.com/cli/v9/commands/npm-audit

## W1 Discovery：产品发现、实验与反馈闭环依据


- Lean Startup Principles：用 build-measure-learn、MVP、validated learning、actionable metrics 和 pivot 约束产品研发循环。
  - https://theleanstartup.com/principles
- Steve Blank Customer Development Manifesto：建筑物内没有事实；假设需要通过客户开发、实验和创业指标验证。
  - https://steveblank.com/category/customer-development-manifesto/
- The Mom Test：客户访谈应帮助团队从真实对话中获得更多学习，避免被礼貌性反馈误导。
  - https://www.momtestbook.com/
- Continuous Discovery / Opportunity Solution Tree：产品发现是决定做什么；持续发现强调每周客户触点、目标 outcome、机会、方案和假设测试。
  - https://www.producttalk.org/getting-started-with-discovery/
  - https://www.producttalk.org/opportunity-solution-trees/
- Basecamp Shape Up：用 fixed time variable scope、appetite、bets not backlogs 和 circuit breaker 限制产品赌注。
  - https://basecamp.com/shapeup
- Google HEART / GSM：把用户体验目标映射为 signals 和 metrics，用于产品决策。
  - https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/
- Trustworthy Online Controlled Experiments / Microsoft ExP：受控实验可建立因果证据，但需要 OEC、trustworthiness assumptions、guardrails 和实验陷阱意识。
  - https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59
  - https://www.microsoft.com/en-us/research/publication/online-experimentation-at-microsoft/
- OpenTelemetry Events / PostHog product analytics docs：事件适合记录用户交互、状态转换和 feature flag 暴露；事件命名应稳定、一致、低基数。
  - https://opentelemetry.io/docs/specs/semconv/general/events/
  - https://posthog.com/tutorials/event-tracking-guide
  - https://posthog.com/docs/product-analytics/best-practices

## W5 Verify 触发专项：测试与质量策略依据


- Martin Fowler, Practical Test Pyramid / Test Pyramid：测试组合应有更多低层、快速、确定的测试，少量高层测试用于端到端信心。
  - https://martinfowler.com/articles/practical-test-pyramid.html
  - https://martinfowler.com/bliki/TestPyramid.html
- Google Software Engineering at Google, Testing Overview / Larger Testing；Google Testing Blog Test Sizes：按 size 和 scope 区分测试，small tests 应快速确定，medium/large tests 需要更谨慎控制 nondeterminism 和 flaky。
  - https://abseil.io/resources/swe-book/html/ch11.html
  - https://abseil.io/resources/swe-book/html/ch14.html
  - https://testing.googleblog.com/2010/12/test-sizes.html
- Gerard Meszaros, xUnit Test Patterns：测试自动化需要关注 fixture setup、exercise、verification、teardown、test doubles、test smells 和可维护性。
  - https://www.oreilly.com/library/view/xunit-test-patterns/9780131495050/
  - https://martinfowler.com/books/meszaros.html
  - https://xunitpatterns.com/
- Go 官方 testing / fuzzing / race detector：`go test` 是 Go 自动化测试基础；fuzzing 适合发现边界和安全问题；`-race` 能发现被执行路径中的数据竞争但有资源成本。
  - https://pkg.go.dev/testing
  - https://go.dev/doc/security/fuzz/
  - https://go.dev/blog/race-detector
- sqlc vet / verify：`sqlc vet` 对 query 运行 lint rules，`sqlc verify` 用于验证 schema changes 与 queries 的兼容性。
  - https://docs.sqlc.dev/en/latest/howto/vet.html
  - https://docs.sqlc.dev/en/latest/howto/verify.html
- Testcontainers for Go / gRPC bufconn：真实依赖 integration tests 可用容器化依赖；gRPC bufconn 可用内存连接测试 handler、metadata、deadline 和 status code。
  - https://golang.testcontainers.org/
  - https://golang.testcontainers.org/modules/postgres/
  - https://pkg.go.dev/google.golang.org/grpc/test/bufconn
- Vitest / Playwright：Vite 前端快速测试使用 Vitest；关键用户流和跨浏览器 E2E 使用 Playwright 的 auto-wait、web-first assertions、isolation、tracing 和 parallelism。
  - https://vitest.dev/guide/
  - https://vitest.dev/guide/coverage
  - https://playwright.dev/
- OpenAI eval docs：生产 AI 行为需要 eval-driven development，代表真实分布的 datasets、自动评分和人工校准；prompt 变化前添加代表 fixtures、tests 和 eval checks。
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
  - https://developers.openai.com/api/docs/guides/agent-evals
  - https://developers.openai.com/api/docs/guides/prompt-engineering

## W2 OpenSpec / Risk 触发专项：架构决策、代码组织与模块边界依据


- D. L. Parnas, On the Criteria To Be Used in Decomposing Systems into Modules：模块化用于提升灵活性、可理解性和并行开发效率，关键在于按什么标准分解模块。
  - https://wstomv.win.tue.nl/edu/2ip30/references/criteria_for_modularization.pdf
  - https://dl.acm.org/doi/10.1145/361598.361623
- Michael Nygard, Documenting Architecture Decisions / ADR：记录影响结构、非功能特性、依赖、接口或构建技术的架构决策；ADR 应保留 context、decision、status 和 consequences。
  - https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  - https://adr.github.io/
  - https://www.thoughtworks.com/en-us/radar/techniques/lightweight-architecture-decision-records
- C4 Model：用 context、container、component、code 四级静态结构视图沟通架构，多数团队只需 context/container 级别。
  - https://c4model.com/introduction
  - https://c4model.com/diagrams
- Domain-Driven Design / Bounded Context：当语言、规则或模型含义变化时，应显式划分 bounded contexts 和关系。
  - https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf
  - https://martinfowler.com/bliki/BoundedContext.html
- Alistair Cockburn, Hexagonal Architecture / Ports and Adapters：应用核心通过 ports 与外部 adapters 连接，避免应用逻辑泄漏到数据库、UI、测试或集成技术中。
  - https://alistair.cockburn.us/hexagonal-architecture
- Go 官方模块组织 / internal packages / workspaces：Go projects 可按 package、command 或组合组织；`internal` 由 go command 强制限制外部 import；workspaces 支持多模块本地开发。
  - https://go.dev/doc/modules/layout
  - https://go.dev/doc/go1.4
  - https://go.dev/doc/tutorial/workspaces
  - https://go.dev/ref/mod
- Kratos layout：Kratos layout 是 `kratos new` 使用的项目模板，包含 `api`、`cmd`、`configs`、`internal` 等目录，用于 Go/Kratos 微服务最佳实践。
  - https://go-kratos.dev/docs/intro/layout/
  - https://github.com/go-kratos/kratos-layout
- Vite / React 文件结构：Vite 以 project root 和 `index.html` 为入口；React 文件结构无唯一官方结构，常见做法是按 feature/route 组织并避免过深嵌套。
  - https://vite.dev/guide/
  - https://vite.dev/config/shared-options
  - https://legacy.reactjs.org/docs/faq-structure.html
- OpenAI prompt engineering / Agents：生产 prompt 应进入代码、靠近 feature、使用 typed inputs；Responses API 适合一次模型调用加工具和应用自有逻辑，Agents SDK 适合应用拥有编排、工具执行、审批和状态。
  - https://developers.openai.com/api/docs/guides/prompt-engineering
  - https://developers.openai.com/api/docs/guides/agents
- Google SRE Simplicity：最小 API、松耦合、删除死代码、清晰模块边界可以同时提升稳定性和敏捷性。
  - https://sre.google/sre-book/simplicity/

## W4 Build 触发专项：配置、环境、Feature Flag 与运行时变更依据


- Twelve-Factor App Config / Dev-Prod Parity：配置应和代码严格分离，环境之间的差异应明确且尽量缩小。
  - https://12factor.net/config
  - https://12factor.net/dev-prod-parity
- Google SRE Workbook, Configuration Design and Best Practices / Configuration Specifics：好的配置接口应能快速、可信、可测试地修改；配置相关 toil 需要通过自动化、位置清晰和验证降低。
  - https://sre.google/workbook/configuration-design/
  - https://sre.google/workbook/configuration-specifics/
- Google SRE, Reliable Product Launches / Canarying Releases / Production Services Best Practices：配置和二进制变更都引入风险，功能发布可与二进制发布分离，并通过分阶段 rollout 降低风险。
  - https://sre.google/sre-book/reliable-product-launches/
  - https://sre.google/workbook/canarying-releases/
  - https://sre.google/sre-book/service-best-practices/
- Martin Fowler, Feature Toggles：Feature Toggles 能不改代码改变行为，但会增加复杂度，需要按 toggle 类型和生命周期管理。
  - https://martinfowler.com/articles/feature-toggles.html
  - https://martinfowler.com/bliki/FeatureFlag.html
- OpenFeature Specification：Feature Flag evaluation API、evaluation context 和 provider 边界应 vendor-neutral；默认值、reason、variant、error details 等应可获取。
  - https://openfeature.dev/specification/sections/flag-evaluation/
  - https://openfeature.dev/specification/sections/evaluation-context/
  - https://openfeature.dev/specification/types/
- Kratos Config：微服务配置应与代码和镜像分离，Kratos config 支持从不同来源加载并合并配置。
  - https://go-kratos.dev/docs/component/config/
- Vite Env and Modes：Vite 将 env 常量暴露在 `import.meta.env`，并在构建时静态替换；只有带前缀的变量暴露给客户端。
  - https://vite.dev/guide/env-and-mode
- gRPC Service Config：gRPC service config 可配置 wait-for-ready、timeout、retry、hedging、load balancing 等 RPC 行为，属于生产风险配置。
  - https://grpc.io/docs/guides/service-config/

## W7 Operate 触发专项：观测性、遥测与 AI Trace 依据


- Google SRE Monitoring Distributed Systems / Workbook Monitoring：监控应优先用户症状和四个黄金信号；dashboard 指标应围绕 latency、traffic、errors、saturation 和依赖行为。
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://sre.google/workbook/monitoring/
- Observability Engineering / Distributed Systems Observability：观测性用于在复杂系统中提出新问题、关联事件并降低调试时间；一人公司需要裁剪为高价值信号。
  - https://www.oreilly.com/library/view/observability-engineering/9781492076438/
  - https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/
- OpenTelemetry signals / Go / JavaScript / logs：OpenTelemetry 是 vendor-neutral framework，用于生成、收集和导出 traces、metrics、logs；Go 和 JavaScript/browser 都有官方 SDK/API。
  - https://opentelemetry.io/docs/concepts/signals/
  - https://opentelemetry.io/docs/what-is-opentelemetry/
  - https://opentelemetry.io/docs/languages/go/
  - https://opentelemetry.io/docs/languages/go/instrumentation/
  - https://opentelemetry.io/docs/languages/js/
  - https://opentelemetry.io/docs/languages/js/instrumentation/
  - https://opentelemetry.io/docs/languages/js/getting-started/browser/
  - https://opentelemetry.io/docs/specs/otel/logs/
- OpenTelemetry Semantic Conventions / GenAI：semantic conventions 定义 span、metrics、attributes、units 和 valid values；GenAI conventions 标准化模型、token、tool、agent 等遥测属性。
  - https://opentelemetry.io/docs/specs/semconv/
  - https://opentelemetry.io/blog/2024/otel-generative-ai/
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/
- W3C Trace Context：标准化 traceparent / tracestate 等跨服务上下文传播格式，支持分布式追踪。
  - https://www.w3.org/TR/trace-context/
- Prometheus metric naming：metric 和 label 命名应一致，label 用于维度，避免把 label 名写进 metric 名，并避免无界高基数 label。
  - https://prometheus.io/docs/practices/naming/
  - https://prometheus.io/docs/concepts/data_model/
- OpenAI Agents tracing / Integrations and observability：Agents SDK tracing 可记录 model calls、tool calls、handoffs、guardrails 和 custom spans，用于开发和生产调试监控。
  - https://developers.openai.com/api/docs/guides/agents/integrations-observability
  - https://openai.github.io/openai-agents-python/tracing/

## W9 Maintain 触发专项：知识管理、文档与上下文恢复依据


- Diátaxis：文档满足 tutorial、how-to、reference、explanation 四种不同用户需求，应按需求组织而不是混写。
  - https://diataxis.fr/
- Google Software Engineering at Google, Knowledge Sharing：组织需要机制传播知识，避免隐性知识只存在于少数人脑中；一人公司裁剪为可恢复上下文和 canonical 入口。
  - https://abseil.io/resources/swe-book/html/ch03.html
- Google Software Engineering at Google, Documentation is Like Code：文档应像代码一样拥有 canonical 入口、版本控制、可审查和持续维护机制。
  - https://abseil.io/resources/swe-book/html/ch10.html
- Google Developer Documentation Style Guide：技术文档应面向开发者，保持清晰、一致、主动语态和可执行语言。
  - https://developers.google.com/style
  - https://developers.google.com/tech-writing/resources
- Write the Docs documentation principles：文档应尽早参与开发，需求和规格可以成为第一版文档，帮助反馈和决策。
  - https://www.writethedocs.org/guide/writing/docs-principles/
- Docs-as-code：文档使用与代码类似的版本控制、review 和自动化流程，以保持同步和可维护。
  - https://engineering.homeoffice.gov.uk/patterns/docs-as-code/
  - https://konghq.com/blog/learning-center/what-is-docs-as-code

## W9 Maintain 触发专项：维护、依赖升级、技术债与弃用治理依据


- Google Software Engineering at Google, Dependency Management：依赖管理是外部代码网络随时间变化的问题，必须考虑传递依赖、安全、弃用、版本冲突和升级级联。
  - https://abseil.io/resources/swe-book/html/ch21.html
- Google Software Engineering at Google, Deprecation：obsolete systems 需要有序迁移和移除；代码长期维护有成本，移除冗余可降低复杂度并提升速度。
  - https://abseil.io/resources/swe-book/html/ch15.html
- Google Software Engineering at Google, Static Analysis：静态分析可帮助保持现代 API、发现 deprecated API、防止技术债回流。
  - https://abseil.io/resources/swe-book/html/ch20.html
- Google Software Engineering at Google, What Is Software Engineering：软件工程关注代码在时间尺度上的可持续维护，technical debt 是代码与理想状态之间的差距。
  - https://abseil.io/resources/swe-book/html/ch01.html
- Martin Fowler Technical Debt / Technical Debt Quadrant / Refactoring：技术债是未来修改额外成本；应区分债务类型；refactor 是行为保持的小步设计改进。
  - https://martinfowler.com/bliki/TechnicalDebt.html
  - https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
  - https://martinfowler.com/books/refactoring.html
  - https://refactoring.com/
- Working Effectively with Legacy Code：遗留代码修改应先建立测试保护、寻找接缝，避免无保护重写。
  - https://www.oreilly.com/library/view/working-effectively-with/0131177052/
- Hidden Technical Debt in Machine Learning Systems / Machine Learning: The High Interest Credit Card of Technical Debt：AI/ML 系统债务会出现在数据依赖、配置、反馈环、胶水代码、外部世界变化和系统边界侵蚀中。
  - https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-syst
  - https://research.google/pubs/machine-learning-the-high-interest-credit-card-of-technical-debt/
- Go modules / govulncheck：Go modules 管理依赖、升级和替换；govulncheck 根据实际调用路径查找 Go 依赖漏洞。
  - https://go.dev/ref/mod
  - https://go.dev/doc/modules/managing-dependencies
  - https://go.dev/doc/tutorial/govulncheck
- GitHub Dependabot：version/security updates 可通过 `dependabot.yml` 配置 ecosystem、schedule、groups 和 PR 行为。
  - https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates
  - https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates
  - https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference
- npm package-lock / npm ci / npm audit：lockfile 用于可复现依赖树；`npm ci` 在 lockfile 与 package.json 不一致时失败；`npm audit` 检查已知漏洞。
  - https://docs.npmjs.com/cli/v8/configuring-npm/package-lock-json/
  - https://docs.npmjs.com/cli/v9/commands/npm-ci
  - https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities/
- Vite migration guide：大版本升级前应阅读官方迁移指南；复杂项目可采用渐进迁移。
  - https://vite.dev/guide/migration
  - https://vite.dev/blog/announcing-vite8

## W2 OpenSpec / Risk 触发专项：API 契约、兼容性与版本演进依据


- Hyrum's Law：API 的所有可观察行为都可能被消费者依赖，契约治理必须限制未声明行为泄漏。
  - https://www.hyrumslaw.com/
- Google AIP-180 Backwards Compatibility：API 演进需要考虑 source compatibility、wire compatibility 和 semantic compatibility。
  - https://google.aip.dev/180
- Protocol Buffers proto3 guide / best practices：已发布字段号不能改；删除字段要 reserve number/name；不要复用 tag；字段类型和 oneof 变化会影响兼容性。
  - https://protobuf.dev/programming-guides/proto3/
  - https://protobuf.dev/best-practices/dos-donts/
- Buf breaking change detection：Protobuf source 可以通过 `buf breaking` 与 baseline 比较，自动发现 breaking changes。
  - https://buf.build/docs/breaking/quickstart/
  - https://buf.build/docs/breaking/rules/
- gRPC error handling / status codes：gRPC 使用标准 status codes 表达错误，错误状态、详情和 retry 语义属于客户端可观察契约。
  - https://grpc.io/docs/guides/error/
  - https://grpc.github.io/grpc/core/md_doc_statuscodes.html
- SemVer：使用版本号前必须声明 public API；版本号用于表达兼容性和破坏性变化边界。
  - https://semver.org/
- OpenAI function calling / Structured Outputs：AI tool 和 structured output 使用 JSON Schema 约束，strict schema 会影响模型输出和应用解析，应按契约管理。
  - https://developers.openai.com/api/docs/guides/function-calling
  - https://developers.openai.com/api/docs/guides/structured-outputs
  - https://developers.openai.com/api/docs/guides/tools
- Confluent schema evolution：schema 演进需要明确 backward、forward、full compatibility，以及 producer/consumer 的读取关系。
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
- Software Engineering at Google, Deprecation：移除旧系统和旧接口需要有序迁移，避免消费者隐式依赖导致删除失败。
  - https://abseil.io/resources/swe-book/html/ch15.html

## W4 Build 触发专项：开发环境、命令自动化与本地可复现依据


- The Joel Test：source control、一步构建和持续构建是高质量软件团队的基础信号；一人公司裁剪为一条本地黄金路径和 one-step verify。
  - https://www.joelonsoftware.com/2000/08/09/the-joel-test-12-steps-to-better-code/
- Software Engineering at Google, Build Systems and Build Philosophy：构建系统把源代码变成可运行 artifact，好的构建系统重视可靠性、可重复和开发者效率。
  - https://abseil.io/resources/swe-book/html/ch18.html
- Software Engineering at Google, Continuous Integration：快速反馈、自动化和持续测试能降低缺陷越晚发现越昂贵的问题。
  - https://abseil.io/resources/swe-book/html/ch23.html
- Twelve-Factor App Dependencies / Dev-Prod Parity / Admin Processes：依赖显式声明；开发、预览和生产尽量接近；管理任务也应在同样环境中运行。
  - https://12factor.net/dependencies
  - https://12factor.net/dev-prod-parity
  - https://12factor.net/admin-processes
- Development Containers Specification：开发环境可用代码描述、创建和重建，适合把工具链和运行时配置显式化。
  - https://devcontainers.github.io/
  - https://devcontainers.github.io/implementors/spec/
  - https://devcontainers.github.io/implementors/json_reference/
- Docker Compose：用一个 YAML 配置和命令定义并启动多容器本地应用栈。
  - https://docs.docker.com/compose/
  - https://docs.docker.com/reference/compose-file/services/
- Go Toolchains / Workspaces：Go toolchain、`go.mod` 和 workspace mode 会影响构建，`go env GOWORK` 可判断 workspace 状态。
  - https://go.dev/doc/toolchain
  - https://go.dev/doc/tutorial/workspaces
  - https://go.dev/blog/get-familiar-with-workspaces
- sqlc generate / vet：`sqlc generate` 从 SQL schema/query 生成代码，`sqlc vet` 用 lint rules 检查 queries。
  - https://docs.sqlc.dev/en/latest/howto/generate.html
  - https://docs.sqlc.dev/en/latest/howto/vet.html
- Vite CLI：Vite 项目通过 dev/build/preview 命令运行开发服务器、生产构建和本地预览。
  - https://vite.dev/guide/
  - https://vite.dev/guide/cli

## W4 Build 触发专项：AI 协作编码、变更批次与自审依据


- 《人月神话》：软件项目不能靠增加人手或 agent 数量自动获得进度；概念完整性和清晰边界仍然需要少数稳定判断。
  - https://martinfowler.com/bliki/MythicalManMonth.html
- OpenSpec getting started：OpenSpec 用 proposal / spec / tasks 等工件让人和 AI coding assistant 在写代码前对齐要做什么。
  - https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md
- Software Engineering at Google, Code Review：代码审查保护正确性、可理解性、一致性、知识共享和历史记录。
  - https://abseil.io/resources/swe-book/html/ch09.html
- Google Engineering Practices Code Review：review 的目标是让代码健康持续改善；小 CL 更易设计、review 和回滚；CL 描述要解释做了什么和为什么。
  - https://google.github.io/eng-practices/review/reviewer/standard.html
  - https://google.github.io/eng-practices/review/developer/small-cls.html
  - https://google.github.io/eng-practices/review/developer/cl-descriptions.html
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
- DORA small batches / trunk-based development：小批量缩短反馈环；生成式 AI 时代，小批量能放大 AI 采用对产品表现的正面影响。
  - https://dora.dev/capabilities/working-in-small-batches/
  - https://dora.dev/capabilities/trunk-based-development/
- OpenAI Codex best practices / AGENTS.md / sandbox / approvals / skills：Codex 应被配置成可改进的队友，复杂任务先计划，重复经验沉淀为 AGENTS.md、skills 和自动化；sandbox 与 approval policy 定义安全自治边界。
  - https://developers.openai.com/codex/learn/best-practices
  - https://developers.openai.com/codex/guides/agents-md
  - https://developers.openai.com/codex/concepts/sandboxing
  - https://developers.openai.com/codex/agent-approvals-security
  - https://developers.openai.com/codex/skills
- GitHub Copilot CLI best practices / Review AI-generated code：AI coding agent 需要自定义指令、计划、review、安全边界；AI 生成代码必须经过功能、意图、质量、依赖和 AI 特有问题检查。
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices
  - https://docs.github.com/en/copilot/tutorials/review-ai-generated-code

## W7 Operate 触发专项：备份、恢复、灾难演练与业务连续性依据


- Google SRE Data Integrity：备份和归档目的不同；备份的核心价值是能在服务可用性需求内恢复数据。
  - https://sre.google/sre-book/data-integrity/
- Google SRE Lessons Learned / Emergency Response / DiRT：恢复能力来自模拟、演练、out-of-band communication、替代访问方式、rollback 和事故历史记录。
  - https://sre.google/sre-book/lessons-learned/
  - https://sre.google/sre-book/emergency-response/
  - https://cloud.google.com/blog/products/management-tools/shrinking-the-time-to-mitigate-production-incidents
- Google Cloud Disaster Recovery：RTO 定义最大可接受中断时间，RPO 定义可接受恢复点年龄；DR planning 应按业务影响、容量、安全、网络、支持、带宽和设施等约束设计。
  - https://cloud.google.com/learn/what-is-disaster-recovery
  - https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide
- AWS Well-Architected Reliability：每个 workload 应定义 RTO/RPO，并通过周期性恢复测试验证备份完整性和流程是否满足目标。
  - https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_objective_defined_recovery.html
  - https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html
- NIST SP 800-34：contingency planning 应帮助评估系统和业务优先级，形成恢复策略、计划、测试和维护机制。
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
- PostgreSQL Backup and Restore / PITR / pg_dump / pg_restore：PostgreSQL 支持 SQL dump、文件系统备份、连续归档/PITR；`pg_dump` 可一致导出但不是生产常规备份的唯一方案，`pg_restore` 可从 archive 重建数据库。
  - https://www.postgresql.org/docs/current/backup.html
  - https://www.postgresql.org/docs/current/continuous-archiving.html
  - https://www.postgresql.org/docs/current/app-pgdump.html
  - https://www.postgresql.org/docs/current/app-pgrestore.html

## W4 Build 触发专项：计费、权益、用量计量与对账依据


- Stripe Billing Subscriptions / Entitlements：订阅状态和 active entitlements 可用于授权功能，但应用后端仍需执行最终权益判断。
  - https://docs.stripe.com/billing/subscriptions/overview
  - https://docs.stripe.com/billing/entitlements?dashboard-or-api=api
- Stripe Meter Events / Meters：usage-based billing 通过 meter event 表达客户动作，billing meters 在账期内聚合这些事件并关联价格。
  - https://docs.stripe.com/api/billing/meter-event
  - https://docs.stripe.com/api/billing/meter-event/create
  - https://docs.stripe.com/api/billing/meter
- Stripe Webhooks / Process undelivered events：Webhook 会重试且不保证事件顺序；手工处理 undelivered events 时要避免重复处理已成功事件。
  - https://docs.stripe.com/webhooks
  - https://docs.stripe.com/webhooks/process-undelivered-events
- Stripe Idempotent Requests / Advanced Error Handling：POST 请求可用 idempotency key 安全重试；GET/DELETE 通常是安全重试语义。
  - https://docs.stripe.com/api/idempotent_requests
  - https://docs.stripe.com/error-low-level
- Stripe Integration Security：使用 hosted payment surface 可降低 PCI 范围；直接处理卡数据会显著增加合规责任。
  - https://docs.stripe.com/security/guide
- Stripe SaaS pricing / AI usage-based billing：SaaS 定价要把 packaging、limits、entitlements 和 value metric 一起设计；AI 用量因 token、agent loop、tool fanout 和成本波动更需要清晰事件契约。
  - https://stripe.com/resources/more/saas-pricing-and-packaging-strategy
  - https://stripe.com/resources/more/ai-companies-and-usage-based-billing
- OpenAI Projects budgets / Rate Limits / Production Best Practices / Prompt Caching：项目预算是提醒阈值而非硬上限；应用需要自己的 rate/quota/cost guard，并利用缓存等策略降低成本。
  - https://help.openai.com/en/articles/9186755-managing-your-work-in-the-api-platform-with-projects
  - https://developers.openai.com/api/docs/guides/rate-limits
  - https://developers.openai.com/api/docs/guides/production-best-practices
  - https://developers.openai.com/api/docs/guides/prompt-caching
- Martin Fowler Accounting Patterns / Stripe Ledger：账务和资金变动需要可追踪 entry/transaction，并通过类似复式记账的结构验证状态。
  - https://martinfowler.com/eaaDev/AccountingEntry.html
  - https://martinfowler.com/eaaDev/AccountingTransaction.html
  - https://martinfowler.com/eaaDev/AccountingNarrative.html
  - https://stripe.dev/blog/ledger-stripe-system-for-tracking-and-validating-money-movement
- Monetizing Innovation / Simon-Kucher：产品和商业化应围绕愿付价格、客户分段、套餐和价值指标一起设计。
  - https://www.amazon.com/Monetizing-Innovation-Companies-Design-Product/dp/1119240867
  - https://www.simon-kucher.com/en/insights/monetizing-innovation

## W8 Learn 触发专项：客户支持、反馈分流与信任运营依据


- The Best Service is No Service：把客户联系支持视为产品或流程失效的数据点，目标是消除重复联系原因，而不是扩大人工支持。
  - https://books.google.li/books?id=1h71O9rpCIcC
- The Effortless Experience：客户忠诚更依赖低努力地解决问题，而不是“惊喜式”客服。
  - https://www.amazon.com/Effortless-Experience-Conquering-Battleground-Customer/dp/1591845815
  - https://books.google.com/books/about/The_Effortless_Experience.html?id=9mzbBQ2wVdEC
- ITIL 4 Incident Management / PeopleCert：incident management 关注在 disruption 后快速恢复正常服务并减少负面影响。
  - https://www.peoplecert.org/browse-certifications/it-governance-and-service-management/ITIL-1/itil4-practices-incident-management-3684
- Google SRE Incident Response / Postmortem Culture：事故响应需要结构化沟通、工作记录、早声明、明确角色和复盘行动项。
  - https://sre.google/workbook/incident-response/
  - https://sre.google/workbook/postmortem-culture/
- Atlassian Incident Communication / Incident Response：用户影响事故需要单一事实来源、尽早准确沟通、持续更新和模板化消息。
  - https://www.atlassian.com/incident-management/incident-communication
  - https://www.atlassian.com/incident-management/handbook/incident-response
  - https://support.atlassian.com/statuspage/docs/incident-communication-tips/
- Zendesk / Intercom support metrics and ticketing：支持队列应跟踪响应、解决、reopen、CSAT/CES、ticket volume 等信号，并用分类/优先级管理请求。
  - https://www.zendesk.com/blog/customer-service/satisfaction/customer-service-metrics-matter/
  - https://www.intercom.com/learning-center/support-ticket
- OpenAI Safety Best Practices / Moderation / Safety Checks：AI 应用需要 moderation、人审、red team、用户级 safety identifier 和对有害内容/账号风险的处理。
  - https://developers.openai.com/api/docs/guides/safety-best-practices
  - https://developers.openai.com/api/docs/guides/moderation
  - https://developers.openai.com/api/docs/guides/safety-checks
- NIST AI RMF Core / Manage：部署后的 AI 系统需要持续监控、捕获外部反馈、申诉/覆盖、事故响应、恢复和变更管理。
  - https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
  - https://airc.nist.gov/airmf-resources/playbook/manage/

## W7 Operate 触发专项：后台运营、人工操作与高风险动作依据


- Twelve-Factor App Admin Processes：one-off 管理任务应运行在与应用相同 release、codebase 和 config 中，管理代码应随应用代码发布。
  - https://12factor.net/admin-processes
- Google SRE Automation / Eliminating Toil：自动化可以减少 toil，但拥有 admin 权限时必须防御性校验输入、评估风险、设置安全保护，并在不安全时退回人工。
  - https://sre.google/sre-book/automation-at-google/
  - https://sre.google/workbook/eliminating-toil/
- Google SRE Emergency Response / Reliable Product Launches：rollback 和应急流程需要提前测试；checklist 能提高可重复可靠性，但必须按上下文裁剪。
  - https://sre.google/sre-book/emergency-response/
  - https://sre.google/sre-book/reliable-product-launches/
  - https://sre.google/sre-book/launch-checklist/
- OWASP Authorization Cheat Sheet：后台和 admin 操作也要 least privilege、deny by default、每次请求校验权限、记录日志并测试授权逻辑。
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Logging / Top 10 A09：应用安全日志要覆盖高价值事务和安全事件；审计轨迹应防止篡改或删除。
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://owasp.org/Top10/2021/A09_2021-Security_Logging_and_Monitoring_Failures/
- NIST SP 800-53 Rev. 5：访问控制、审计与问责、事件响应等控制可按风险裁剪，用于保护组织资产、个人和隐私。
  - https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- OpenAI Agent Builder Safety：高权限工具链中不要把不可信输入放进 developer messages，并用结构化输出约束数据流。
  - https://developers.openai.com/api/docs/guides/agent-builder-safety
- Google SRE AI Engineering Reliable Operations：AI 运维自治应按 Monitoring、Investigation、Approval、Actuation、Self-Directed 逐级推进，高风险 actuation 需要更高安全控制和批准。
  - https://sre.google/resources/practices-and-processes/ai-engineering-reliable-operations/

## W2 OpenSpec / Risk 触发专项：信任政策、用户承诺与合规声明依据


- NIST Privacy Framework：用于识别和管理隐私风险，在创新产品和服务中保护个人隐私。
  - https://www.nist.gov/privacy-framework
- GDPR Article 5 / ICO Data Minimisation / CCPA：透明、公平、数据最小化、存储限制、访问/删除/更正/选择退出等权利构成常见隐私基线。
  - https://gdpr-info.eu/art-5-gdpr/
  - https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/data-minimisation/
  - https://oag.ca.gov/privacy/ccpa
- FTC AI guidance / enforcement：AI 没有法律例外；AI 能力、隐私、数据用途和比较优势声明需要证据，不能误导或遗漏重要事实。
  - https://www.ftc.gov/policy/advocacy-research/tech-at-ftc/2024/01/ai-companies-uphold-your-privacy-confidentiality-commitments
  - https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes
  - https://www.ftc.gov/industry/technology/artificial-intelligence
- OECD AI Principles：AI 应创新且可信，尊重人权和民主价值，包含透明、稳健、安全与问责原则。
  - https://www.oecd.org/en/topics/sub-issues/ai-principles.html
  - https://oecd.ai/en/dashboards/ai-principles/P7
- NIST AI RMF / Generative AI Profile：用于把可信 AI 风险管理纳入生成式 AI 的设计、开发、使用和评估。
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
  - https://airc.nist.gov/airmf-resources/playbook/
- OpenAI Usage Policies / Safety Best Practices / Data Processing Addendum / Enterprise Privacy：应用需遵守供应商使用政策、安全实践、数据处理角色、数据控制和企业数据默认不训练等边界。
  - https://openai.com/policies/usage-policies/
  - https://developers.openai.com/api/docs/guides/safety-best-practices
  - https://openai.com/policies/data-processing-addendum/
  - https://openai.com/enterprise-privacy/
- Google People + AI Guidebook：AI 产品需要帮助用户建立正确心理模型，提供解释、反馈与控制。
  - https://pair.withgoogle.com/guidebook/
- OpenAI system cards / model cards practice：AI 能力、限制、安全评估和已知风险应被文档化，供产品 disclosure 和内部风险判断使用。
  - https://openai.com/index/gpt-4o-system-card/
  - https://openai.com/index/gpt-5-system-card/

## W3 AI Behavior 触发专项：AI 数据集、评测样本、标注与刷新治理依据


- OpenAI Evaluation Best Practices / Datasets / Graders：eval 应贴近真实任务分布，明确“好”的定义，使用可重复 datasets、graders 和持续评估。
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
  - https://developers.openai.com/api/docs/guides/evaluation-getting-started
  - https://developers.openai.com/api/docs/guides/graders
- OpenAI Model Optimization / Fine-tuning：训练、验证和优化数据质量影响模型优化结果；评测数据需要与训练/微调数据分离并版本化。
  - https://developers.openai.com/api/docs/guides/model-optimization
- Google Rules of Machine Learning：先保证 pipeline、指标、good/bad 定义、数据新鲜度和训练/服务一致性，再增加模型复杂度。
  - https://developers.google.com/machine-learning/guides/rules-of-ml
- Datasheets for Datasets：数据集文档应覆盖动机、组成、收集、预处理、用途、分发和维护。
  - https://arxiv.org/abs/1803.09010
- Data Cards：用结构化 data card 提高数据集透明度、用途边界和责任 AI 实践。
  - https://research.google/pubs/data-cards-purposeful-and-transparent-dataset-documentation-for-responsible-ai/
- Hidden Technical Debt in Machine Learning Systems：ML 系统的长期债务常来自数据依赖、反馈环、配置和隐式消费者。
  - https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
- NIST AI RMF / Generative AI Profile：AI 风险管理覆盖设计、开发、部署、运营和评估；生成式 AI 特别关注数据隐私、内容来源、预部署测试和持续治理。
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://doi.org/10.6028/NIST.AI.600-1

## W3 AI Behavior 触发专项：AI 红队、滥用场景与对抗样本治理依据


- OpenAI Safety Best Practices / Red Teaming / Moderation / Safety Checks：AI 应用需要 moderation、adversarial testing、human oversight、输入输出约束、用户报告和 safety identifier。
  - https://developers.openai.com/api/docs/guides/safety-best-practices
  - https://developers.openai.com/api/docs/guides/red-teaming
  - https://developers.openai.com/api/docs/guides/moderation
  - https://developers.openai.com/api/docs/guides/safety-checks
- OpenAI external red teaming paper：外部红队可发现新风险、压力测试缓解、引入领域专家、增强风险评估，但需要配合自动化 eval 和明确阈值。
  - https://cdn.openai.com/papers/openais-approach-to-external-red-teaming.pdf
- Microsoft AI Red Team / Planning red teaming for LLMs：红队应在生命周期内提前规划，定义 tester 组成、范围、目标、记录方式和后续度量。
  - https://learn.microsoft.com/en-us/security/ai-red-team/
  - https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/red-teaming
- OWASP Top 10 for LLM Applications 2025：提示注入、敏感信息披露、供应链、数据/模型污染、不安全输出处理、过度代理、系统提示泄露、向量/嵌入弱点、错误信息和无界消耗构成主要风险清单。
  - https://genai.owasp.org/llm-top-10/
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/
- NIST AI RMF / GenAI Profile / Adversarial Machine Learning taxonomy：AI 风险管理与对抗 ML 需要共同语言、生命周期视角、攻击目标/能力/知识和缓解方法。
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://doi.org/10.6028/NIST.AI.600-1
  - https://csrc.nist.gov/pubs/ai/100/2/e2025/final
- Google SAIF / AI Red Team：AI 红队应结合传统红队、AI 专家、真实 TTP 和持续 work feed，覆盖 prompt attacks、数据提取、backdoor、对抗样本、污染和外泄。
  - https://saif.google/
  - https://blog.google/innovation-and-ai/technology/safety-security/googles-ai-red-team-the-ethical-hackers-making-ai-safer/
- Anthropic red teaming language models：红队用于发现、测量并减少有害输出，且需要透明记录流程、数据和不确定性。
  - https://www.anthropic.com/research/red-teaming-language-models-to-reduce-harms-methods-scaling-behaviors-and-lessons-learned
- MITRE ATLAS：AI 安全可借鉴 adversarial tactics、techniques 和 case studies 来组织红队发现和缓解。
  - https://atlas.mitre.org/

## W3 AI Behavior 触发专项：内容安全、用户生成内容与审核策略依据


- OpenAI Moderation / Safety Best Practices / Safety Checks / Usage Policies：应用应检测 harmful content，用 moderation 结果执行过滤、review、干预或账号处理，并结合人审、反馈、safety identifier 和使用政策。
  - https://developers.openai.com/api/docs/guides/moderation
  - https://developers.openai.com/api/docs/guides/safety-best-practices
  - https://developers.openai.com/api/docs/guides/safety-checks
  - https://openai.com/policies/usage-policies/
- Santa Clara Principles：内容审核需要透明、可解释、可申诉，用户应知道规则、原因和救济路径。
  - https://santaclaraprinciples.org/
- EU Digital Services Act：notice-and-action、statement of reasons、appeal、透明度报告、未成年人保护和用户控制是可借鉴的产品原则。
  - https://digital-strategy.ec.europa.eu/en/policies/dsa-impact-platforms
- TSPA Content Moderation and Operations / Metrics：内容审核是按平台政策审查 UGC 的流程，成熟流程需要人工/自动化组合、申诉、队列和指标。
  - https://www.tspa.org/curriculum/ts-fundamentals/content-moderation-and-operations/
  - https://www.tspa.org/curriculum/ts-fundamentals/content-moderation-and-operations/metrics-for-content-moderation/
- Building Successful Online Communities：社区安全和参与度来自规则、反馈、激励、承诺和社会设计，不只是事后删除。
  - https://mitpress.mit.edu/9780262016575/building-successful-online-communities/
- Custodians of the Internet：内容审核塑造平台边界、公共空间和用户信任，是平台核心功能。
  - https://yalebooks.yale.edu/book/9780300235029/custodians-of-the-internet/
- Behind the Screen：人工审核有心理和劳动成本；审核流程应限制不必要暴露并保护审核者。
  - https://yalebooks.yale.edu/book/9780300261479/behind-the-screen/
- Partnership on AI Responsible Practices for Synthetic Media：AI 生成或修改媒体需要合适披露、标签、来源信号和使用场景约束。
  - https://syntheticmedia.partnershiponai.org/
- Perspective API：可作为内容审核参考工具，但 2026-06-24 查到官网提示服务将在 2026 年后结束，因此不应作为长期唯一控制。
  - https://perspectiveapi.com/

## W3 AI Behavior 触发专项：AI 记忆、用户偏好与长期上下文治理依据


- OpenAI Conversation State / Responses / Conversations：多轮上下文可以由应用重发、用 `previous_response_id` 串联，或用 Conversations API 持久化；不同状态机制有不同应用状态边界。
  - https://developers.openai.com/api/docs/guides/conversation-state
  - https://developers.openai.com/api/docs/guides/migrate-to-responses
- OpenAI Retrieval / File Search / Embeddings：外部上下文和向量检索可提升回答质量，但需要限制结果数量、记录来源、管理 vector store 和控制 token/延迟成本。
  - https://developers.openai.com/api/docs/guides/retrieval
  - https://developers.openai.com/api/docs/guides/tools-file-search
  - https://developers.openai.com/api/docs/guides/embeddings
- OpenAI Data Controls / Enterprise Privacy / Business Data：API 输入输出默认不用于训练，但 Conversations、vector stores、files 等长期 application state 与 data retention 需要按 endpoint/capability 管理。
  - https://developers.openai.com/api/docs/guides/your-data
  - https://openai.com/enterprise-privacy/
  - https://openai.com/business-data/
- OpenAI ChatGPT Memory / Data Controls：saved memories、reference chat history、temporary chat、查看/删除/清空记忆和 data controls 是用户控制长期记忆的产品参考。
  - https://help.openai.com/en/articles/8590148-memory-faq
  - https://openai.com/index/memory-and-new-controls-for-chatgpt/
  - https://openai.com/consumer-privacy/
- Google People + AI Guidebook：个性化和用户数据收集需要主动说明、用户控制、正确心理模型和可纠错体验。
  - https://pair.withgoogle.com/guidebook/
  - https://pair.withgoogle.com/guidebook/patterns
- NIST Privacy Framework / GDPR Article 5：长期记忆和偏好处理需要透明、目的限制、数据最小化、准确性、存储限制、安全和可证明责任。
  - https://www.nist.gov/privacy-framework
  - https://gdpr-info.eu/art-5-gdpr/
- RAG paper：显式外部记忆和检索能补充模型参数知识，改善事实性和可更新性，但仍要处理来源、更新和归因。
  - https://arxiv.org/abs/2005.11401
- MemGPT / Generative Agents：长期记忆可按层级、检索、反思和计划管理，但需要应用策略、用户控制和安全边界。
  - https://arxiv.org/abs/2310.08560
  - https://arxiv.org/abs/2304.03442

## W3 AI Behavior 触发专项：AI 模型、供应商路由与降级治理依据


- OpenAI Model Selection / Models：模型选择应先达到准确率目标并建立 eval dataset，再在保持质量的前提下优化成本和延迟；最新模型推荐和模型族能力会变化，因此内部工件记录 route 决策和证据，不硬编码长期外部事实。
  - https://developers.openai.com/api/docs/guides/model-selection
  - https://developers.openai.com/api/docs/models
- OpenAI GPT-5.5 / Reasoning / Prompt Guidance：新模型族不能视为旧模型的 drop-in replacement；应从 fresh baseline、最小 prompt、代表样例、reasoning effort、verbosity、tool description 和输出格式开始调优。
  - https://developers.openai.com/api/docs/guides/latest-model
  - https://developers.openai.com/api/docs/guides/reasoning
  - https://developers.openai.com/api/docs/guides/prompt-guidance
- OpenAI Latency / Cost / Prompt Caching / Batch / Flex / Priority：模型路线需要同时记录质量、token、输出长度、模型大小、缓存、异步批处理、低优先级处理和高优先级低延迟路径的取舍。
  - https://developers.openai.com/api/docs/guides/latency-optimization
  - https://developers.openai.com/api/docs/guides/cost-optimization
  - https://developers.openai.com/api/docs/guides/prompt-caching
  - https://developers.openai.com/api/docs/guides/batch
  - https://developers.openai.com/api/docs/guides/flex-processing
  - https://developers.openai.com/api/docs/guides/priority-processing
- OpenAI Rate Limits / Error Codes / Production Best Practices：生产调用需要处理 rate limit、timeout、5xx、503、重试、退避、状态页和稳定流量模式。
  - https://developers.openai.com/api/docs/guides/rate-limits
  - https://developers.openai.com/api/docs/guides/error-codes
  - https://developers.openai.com/api/docs/guides/production-best-practices
- Google SRE Handling Overload / Cascading Failures：过载和级联故障需要提前设计 degraded response、拒绝、限流和恢复，而不是把所有错误交给重试。
  - https://sre.google/sre-book/handling-overload/
  - https://sre.google/sre-book/addressing-cascading-failures/
- Google Rules of ML：先把 pipeline、指标、简单模型和独立测试做可靠，再增加模型复杂度；模型路线的基础设施比追逐复杂模型更重要。
  - https://developers.google.com/machine-learning/guides/rules-of-ml
- Hidden Technical Debt in ML Systems：AI/ML 系统容易出现 glue code、配置债、隐式依赖、纠缠和反馈环；模型路由和供应商边界需要显式工件。
  - https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/
- OpenTelemetry GenAI Semantic Conventions：GenAI 调用应标准化记录 provider、request model、response model、token、stream、finish reason、tool call、retrieval 和 latency 等属性。
  - https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/

## W5 Verify 触发专项：可访问性、AI UX 与界面信任依据


- WCAG 2.2 / WAI WCAG Overview：WCAG 2.2 是当前 W3C 推荐标准，覆盖广泛残障类型，使用可测试 success criteria，组织在 Perceivable、Operable、Understandable、Robust 四个原则下；W3C 鼓励采用当前版本。
  - https://www.w3.org/TR/WCAG22/
  - https://www.w3.org/WAI/standards-guidelines/wcag/
  - https://www.w3.org/WAI/WCAG22/Understanding/
- WAI-ARIA Authoring Practices / MDN Accessibility：复杂 widget 需要正确语义、键盘支持、焦点管理和 accessible names；原生控件优先，伪造控件必须补齐键盘可达和交互语义。
  - https://www.w3.org/WAI/ARIA/apg/
  - https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA
  - https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Understanding_WCAG/Keyboard
- Vercel Geist / `design.md` / `design.dark.md`：Geist 提供高对比、可访问色彩、浅/深主题 token、精确文案、焦点环、克制动效和不单靠颜色表达状态的规则。
  - https://vercel.com/geist/introduction
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md
- Google People + AI Guidebook：AI 产品需要正确心理模型、反馈、控制、纠错和失败处理；用户体验需要围绕人的任务和信任设计。
  - https://pair.withgoogle.com/guidebook/
  - https://pair.withgoogle.com/guidebook/patterns
- ISO 9241-210：人本设计贯穿交互系统生命周期，要求关注用户、任务、环境和人机交互质量。
  - https://www.iso.org/standard/77520.html
- Nielsen Norman Group usability heuristics：系统状态可见、贴近用户语言、用户控制、标准一致、错误预防、帮助用户识别和恢复错误等启发式适合作为一人公司最小 UX 复盘框架。
  - https://www.nngroup.com/articles/ten-usability-heuristics/
- NIST AI RMF：AI 风险管理要把可信性考虑纳入 AI 产品的设计、开发、使用和评估。
  - https://www.nist.gov/itl/ai-risk-management-framework
- React accessibility docs：React UI 仍需语义 HTML、错误通知、键盘操作、焦点轮廓、skip links、landmarks 和焦点管理。
  - https://legacy.reactjs.org/docs/accessibility.html

## W3 AI Behavior 触发专项：AI 工具运行时、外部连接器与沙箱治理依据


- OpenAI Function Calling / Tools / Structured Outputs：工具调用是应用侧多步执行流程；函数工具使用 schema，严格模式能提升参数约束；工具、tool search 和 remote MCP 会扩展模型能力，因此需要应用侧边界。
  - https://developers.openai.com/api/docs/guides/function-calling
  - https://developers.openai.com/api/docs/guides/tools
  - https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI Agents SDK / MCP Connectors / Developer Mode：应用拥有编排、工具执行、审批和状态时使用 agent runtime；远程 MCP/connector 默认应审批；读写 MCP developer mode 强大但危险，要防提示注入、错误写操作和恶意 MCP。
  - https://developers.openai.com/api/docs/guides/agents
  - https://developers.openai.com/api/docs/guides/tools-connectors-mcp
  - https://developers.openai.com/api/docs/guides/developer-mode
- OpenAI Safety Best Practices / Data Controls：高风险输出需要 human review；远程 MCP server 是第三方服务，发给它的数据受其数据保留和驻留政策约束。
  - https://developers.openai.com/api/docs/guides/safety-best-practices
  - https://developers.openai.com/api/docs/guides/your-data
- Model Context Protocol Security Best Practices：MCP 实现需要处理 confused deputy、token passthrough、SSRF、session hijacking、本地 MCP server compromise 和 scope minimization。
  - https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- OWASP Top 10 for LLM Applications：prompt injection、insecure output handling、insecure plugin/tool design、excessive agency、sensitive disclosure 和 unbounded consumption 会在工具调用场景被放大。
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/
  - https://genai.owasp.org/llm-top-10/
- Google SRE Handling Overload / Cascading Failures：工具 fanout、自动重试和无限 agent loop 会制造过载和级联故障；需要限流、退避、降级、拒绝和恢复。
  - https://sre.google/sre-book/handling-overload/
  - https://sre.google/sre-book/addressing-cascading-failures/
- Saltzer & Schroeder / OWASP Authorization：工具权限采用 least privilege、fail-safe defaults、complete mediation、deny by default 和每次请求校验。
  - https://web.mit.edu/saltzer/www/publications/protection/
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- Kratos / sqlc / gRPC / Vercel Geist：工具运行时落地到 Go/Kratos middleware、gRPC metadata、sqlc audit tables 和克制清晰的 Vite 确认 UI。
  - https://go-kratos.dev/docs/component/middleware/overview/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/guides/metadata/
  - https://vercel.com/geist/introduction

## W4 Build 触发专项：AI 异步任务、队列与后台 Worker 治理依据


- Enterprise Integration Patterns：消息、队列、竞争消费者、幂等接收者、消息存储和消息历史提供异步系统的经典设计词汇。
  - https://www.enterpriseintegrationpatterns.com/
- Designing Data-Intensive Applications：后台任务、批处理、流处理、消息系统和可恢复数据管道需要在可靠性、可维护性和复杂度之间权衡。
  - https://dataintensive.net/
  - https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/
- Google SRE Distributed Periodic Scheduling with Cron / Data Processing Pipelines：定时任务和后台数据管道需要处理重复、失败、依赖、延迟、状态和运行生命周期。
  - https://sre.google/sre-book/distributed-periodic-scheduling/
  - https://sre.google/workbook/data-processing-pipelines/
- Google SRE Handling Overload / Cascading Failures：队列、worker fanout、批处理和自动重试需要背压、限流、退避、降级、拒绝和恢复，避免级联故障。
  - https://sre.google/sre-book/handling-overload/
  - https://sre.google/sre-book/addressing-cascading-failures/
- Twelve-Factor App Concurrency / Disposability：后台工作应作为独立 worker process 水平扩展；进程应快速启动、优雅停止，避免部署或崩溃时丢任务。
  - https://12factor.net/concurrency
  - https://12factor.net/disposability
- PostgreSQL explicit locking：`FOR UPDATE SKIP LOCKED` 可用于多个消费者避免等待已锁行，但返回不一致视图，适合 queue-like table 的抢占语义。
  - https://www.postgresql.org/docs/current/sql-select.html
- OpenAI Background Mode / Batch API：长任务可以异步执行并轮询状态；Batch 适合不要求即时响应的大量请求，需记录状态、结果引用、成本和保留边界。
  - https://developers.openai.com/api/docs/guides/background
  - https://developers.openai.com/api/docs/guides/batch
- OpenTelemetry Messaging Semantic Conventions：队列和消息处理应使用稳定语义记录 producer/consumer、operation、destination、message、latency 和错误信息。
  - https://opentelemetry.io/docs/specs/semconv/messaging/
- Kratos / sqlc / gRPC / Vercel Geist：异步任务落地到 Go/Kratos worker/gRPC API、sqlc job tables、gRPC metadata 和清晰可取消的 Vite 任务状态 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/guides/metadata/
  - https://vercel.com/geist/introduction

## W4 Build 触发专项：事件驱动、Webhook 与外部系统集成治理依据


- Enterprise Integration Patterns：事件、消息通道、幂等接收者、消息存储、消息历史、死信通道和竞争消费者提供外部集成的经典设计词汇。
  - https://www.enterpriseintegrationpatterns.com/
- Designing Data-Intensive Applications：分布式系统默认要面对重试、重复、乱序、部分失败和最终一致；应用层仍需幂等、恢复和可观察性。
  - https://dataintensive.net/
  - https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/
- CloudEvents / CNCF：CloudEvents 提供统一事件元数据，帮助跨系统表达 event id、source、type、subject、time、schema 和 data。
  - https://cloudevents.io/
  - https://www.cncf.io/projects/cloudevents/
  - https://github.com/cloudevents/spec
- Transactional Outbox：业务数据库写入和消息发布存在双写风险；outbox pattern 把业务状态和待发送事件放入同一事务。
  - https://microservices.io/patterns/data/transactional-outbox.html
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
- Stripe Webhooks：Webhook 需要用官方库或等价方式验证签名，处理重复事件，快速返回成功，并能处理自动重试和未送达事件。
  - https://docs.stripe.com/webhooks
  - https://docs.stripe.com/webhooks/process-undelivered-events
- GitHub Webhooks：接收方应验证 webhook signature；GitHub 提供 delivery 查看、重投递和调试能力，但 delivery 记录保留时间有限。
  - https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
  - https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/viewing-webhook-deliveries
- OWASP API Security：Webhook endpoint 是外部 API，需防伪造、重放、资源消耗、权限绕过、敏感数据泄漏和不安全第三方 API 消费。
  - https://owasp.org/www-project-api-security/
- Google SRE Handling Overload / Cascading Failures：事件风暴、Webhook 重试和出站 fanout 需要背压、限流、快速 ack、队列、死信和降级。
  - https://sre.google/sre-book/handling-overload/
  - https://sre.google/sre-book/addressing-cascading-failures/
- OpenTelemetry Messaging / CloudEvents Semantic Conventions：消息和 CloudEvents 处理应使用统一 span/metric/log 属性，便于跨系统排障。
  - https://opentelemetry.io/docs/specs/semconv/messaging/
  - https://opentelemetry.io/docs/specs/semconv/cloudevents/cloudevents-spans/
- Kratos / sqlc / gRPC / Vercel Geist：集成边界落地到 Go/Kratos webhook handler、sqlc inbox/outbox tables、gRPC/internal event API 和清晰的 Vite 集成状态 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/guides/metadata/
  - https://vercel.com/geist/introduction

## W9 Maintain 触发专项：AI 产品审计、证据保全与合规证据包治理依据


- Google SRE Incident Response / Postmortem Culture：事故处理需要结构化响应、边处理边记录、无责复盘、可读证据和可关闭的行动项。
  - https://sre.google/workbook/incident-response/
  - https://sre.google/workbook/postmortem-culture/
- OWASP Logging Cheat Sheet：应用日志应支持安全、运营、审计和合规用途；日志字段要包含 when/where/who/what，同时排除或脱敏 token、PII、密钥、支付数据和敏感内容，并保护日志完整性。
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- NIST SP 800-53 Rev. 5：Audit and Accountability、Assessment/Authorization/Monitoring、Incident Response、PII Processing and Transparency 等控制族提供审计、问责、控制证据和隐私保护词汇。
  - https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST AI RMF / Generative AI Profile：AI 风险管理应贯穿 AI 产品设计、开发、使用和评估；生成式 AI 需要可追踪的治理、评估、风险和管理证据。
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- AICPA Trust Services Criteria / SOC 2：安全、可用性、处理完整性、机密性和隐私是客户可理解的证据包组织维度。
  - https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022
- OpenTelemetry semantic conventions：统一 traces、metrics、logs、events 和 resource 属性，减少跨服务、跨供应商证据关联成本。
  - https://opentelemetry.io/docs/concepts/semantic-conventions/
- OpenAI Evaluation Best Practices / Data Controls：AI 行为证据应连接 eval、日志、人工判断和数据保留边界；API 数据默认不用于训练，但不同 endpoint 的应用状态和 abuse monitoring 留存边界不同。
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
  - https://developers.openai.com/api/docs/guides/your-data
- Kratos / sqlc / gRPC / Vercel Geist：审计证据落地到 Go/Kratos middleware/usecase hook、sqlc audit tables、gRPC metadata、Vite trust/admin surface 和清晰克制的证据包导出 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/guides/metadata/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W3 AI Behavior 触发专项：AI RAG、知识源、检索与引用治理依据


- RAG 原论文：RAG 将参数化模型与非参数化外部记忆结合，用于知识密集任务；provenance、知识更新和检索质量是核心问题。
  - https://arxiv.org/abs/2005.11401
- OpenAI Retrieval / File Search / Embeddings：语义检索由 vector stores、files、chunks、similarity scores 和 embeddings 支撑；file search 可让模型从知识库检索，但应用仍需管理权限、来源、成本和保留。
  - https://developers.openai.com/api/docs/guides/retrieval
  - https://developers.openai.com/api/docs/guides/tools-file-search
  - https://developers.openai.com/api/docs/guides/embeddings
- OpenAI Data Controls：OpenAI API 数据默认不用于训练；vector stores、files、responses、embeddings 等 endpoint 的 application state、retention、删除和 ZDR 资格不同。
  - https://developers.openai.com/api/docs/guides/your-data
- OWASP LLM Prompt Injection / RAG Poisoning：外部资料、网页、邮件、文件和知识库可携带恶意指令；RAG context 需要当作不可信上下文。
  - https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
- OWASP LLM08 Vector and Embedding Weaknesses：向量与 embedding 系统可能带来未授权访问、跨上下文泄露、数据投毒、输出操纵和敏感信息披露风险。
  - https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/
- NIST AI RMF / Generative AI Profile：RAG 属于生成式 AI 风险管理的一部分，需要在设计、开发、使用和评估中持续管理信任风险。
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- PostgreSQL Full Text Search / pgvector：一人公司可优先用 Postgres full-text search、pgvector 或 OpenAI hosted vector store；pgvector 支持在 Postgres 中存储和检索向量，并保留 ACID、PITR、JOIN 等数据库能力。
  - https://www.postgresql.org/docs/current/textsearch.html
  - https://www.postgresql.org/docs/current/textsearch-intro.html
  - https://github.com/pgvector/pgvector
- Google SRE Data Processing Pipelines / Handling Overload：RAG 摄取、重建索引、批量 embedding 和删除回填是数据管道，需要幂等、背压、限流、重试、观测和降级。
  - https://sre.google/workbook/data-processing-pipelines/
  - https://sre.google/sre-book/handling-overload/
- Kratos / sqlc / gRPC / Vercel Geist：RAG 落地到 Go/Kratos ingestion/retrieval service、sqlc source/chunk/index tables、gRPC retrieval API 和清晰可扫描的 Vite 知识源/引用 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W7 Operate 触发专项：基础设施即代码、环境拓扑与云资源治理依据


- Infrastructure as Code / Kief Morris：基础设施应像软件一样版本化、测试、审查、可重复创建和演进，避免手工环境和 snowflake infrastructure。
  - https://infrastructure-as-code.com/book/
  - https://www.thoughtworks.com/en-us/insights/books/infrastructure-as-code-3rd-ed
- Google SRE Configuration Design / Configuration Specifics：生产配置和基础设施变更需要可理解、可验证、可回滚，减少配置 toil 和大范围误操作。
  - https://sre.google/workbook/configuration-design/
  - https://sre.google/workbook/configuration-specifics/
- Google SRE Release Engineering / Canarying：基础设施变更也应可重复、自动化、渐进、可回滚，并用信号确认是否继续。
  - https://sre.google/sre-book/release-engineering/
  - https://sre.google/workbook/canarying-releases/
- AWS Well-Architected Operational Excellence：云环境可以把应用、基础设施、配置和操作流程作为代码管理，降低人工错误并提高一致性。
  - https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/operational-excellence.html
  - https://docs.aws.amazon.com/wellarchitected/latest/framework/operational-excellence.html
- Terraform State / Drift / Sensitive Data：Terraform state 用于映射真实资源和配置；plan/state 可能包含敏感值；drift 需要检测并修复。
  - https://developer.hashicorp.com/terraform/language/state
  - https://developer.hashicorp.com/terraform/language/backend
  - https://developer.hashicorp.com/terraform/language/manage-sensitive-data
  - https://developer.hashicorp.com/terraform/tutorials/state/resource-drift
- OpenTofu State and Plan Encryption：OpenTofu 支持 state 与 plan 文件静态加密，可作为 state 敏感信息治理选项。
  - https://opentofu.org/docs/language/state/encryption/
- Kubernetes Declarative Management：Kubernetes 对象可通过配置文件声明式管理，`kubectl diff` 可预览 apply 变更，但 live object 与配置文件的差异仍需治理。
  - https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/
  - https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/
- Twelve-Factor App：使用声明式格式做 setup automation，分离 build/release/run，保持 dev/prod parity，把 backing services 当作附加资源。
  - https://12factor.net/
  - https://12factor.net/config
- DORA Capability Catalog：版本控制、自动化部署、快速反馈和持续改进是软件交付与运营性能的核心能力，基础设施变更同样适用。
  - https://dora.dev/capabilities/
- Kratos / sqlc / gRPC / Vite：基础设施治理落地到 Go/Kratos 服务运行环境、sqlc/PostgreSQL 资源、gRPC 网络/TLS 边界和 Vite/Vercel preview/production 环境。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vite.dev/guide/
  - https://vercel.com/design.md

## W4 Build 触发专项：用户通知、邮件/SMS/Push 与触达治理依据


- FTC CAN-SPAM：商业邮件需要真实 header/subject、退订机制和及时处理；事务/关系消息也不能使用误导性路由信息。
  - https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FCC TCPA / robotext guidance：自动短信通常需要事先同意，退订请求必须能被识别并执行。
  - https://docs.fcc.gov/public/attachments/da-16-1299a1.pdf
  - https://www.federalregister.gov/documents/2024/01/26/2023-28832/targeting-and-eliminating-unlawful-text-messages-implementation-of-the-telephone-consumer-protection
- Gmail sender guidelines / RFC 8058 / RFC 2369：批量商业邮件需要身份认证、低投诉、清晰退订；one-click unsubscribe 使用 List-Unsubscribe 和 List-Unsubscribe-Post。
  - https://support.google.com/mail/answer/14229414
  - https://datatracker.ietf.org/doc/html/rfc8058
  - https://datatracker.ietf.org/doc/html/rfc2369
- Amazon SES deliverability / event publishing：bounce、complaint、delivery、reject、rendering failure 等事件应被监控；硬退信和投诉要进入 suppression。
  - https://docs.aws.amazon.com/ses/latest/dg/send-email-concepts-deliverability.html
  - https://docs.aws.amazon.com/ses/latest/dg/monitor-using-event-publishing.html
  - https://docs.aws.amazon.com/ses/latest/dg/event-publishing-retrieving-sns-contents.html
- Twilio SMS compliance guidance：短信营销是 permission-based，需要清晰 opt-in、确认、退订和 help 说明。
  - https://www.twilio.com/en-us/resource-center/guide-to-us-sms-compliance
  - https://help.twilio.com/articles/223134027-Twilio-support-for-Opt-out-keywords-SMS-STOP-filtering-
- Firebase Cloud Messaging / W3C Push API / APNs：push 需要用户授权、设备 token、平台 API、配额、速率和失败处理。
  - https://firebase.google.com/docs/cloud-messaging/scale-fcm
  - https://firebase.google.com/docs/cloud-messaging/throttling-and-quotas
  - https://www.w3.org/TR/push-api/
  - https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns
- Google SRE Incident Response / Atlassian Incident Communication：用户影响事件需要单一事实来源、及时更新、准确口径和行动项。
  - https://sre.google/workbook/incident-response/
  - https://www.atlassian.com/incident-management/incident-communication
- Kratos / sqlc / gRPC / Vite / Vercel Geist：用户触达落地到 Go/Kratos notification service、sqlc delivery/preference/suppression tables、gRPC idempotent send API 和清晰的 Vite 偏好/退订 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vite.dev/guide/
  - https://vercel.com/design.md

## W1 Discovery 触发专项：产品分析、事件埋点与隐私友好实验依据


- Google HEART / GSM：产品度量先从目标、信号、指标映射开始，避免只看虚荣数字。
  - https://research.google.com/pubs/archive/36299.pdf
- Trustworthy Online Controlled Experiments / SRM：A/B 结果必须经过可信度检查；Sample Ratio Mismatch 是实验数据质量异常的重要信号。
  - https://books.google.com/books/about/Trustworthy_Online_Controlled_Experiment.html?id=TFjPDwAAQBAJ
  - https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/sample-ratio-mismatch-and-other-trustrelated-guardrail-metrics/8DBB0F59AC7729D7BC6B94690DB9CCD5
  - https://exp-platform.com/Documents/2019_KDDFabijanGupchupFuptaOmhoverVermeerDmitriev.pdf
- OpenTelemetry semantic conventions：事件是有名称的、有意义时间点上的发生；统一属性命名能降低跨代码和工具的理解成本。
  - https://opentelemetry.io/docs/concepts/semantic-conventions/
  - https://opentelemetry.io/docs/specs/semconv/general/events/
- Tracking plan 官方资料：产品事件应先计划事件、属性、来源、用途和所有权，再进入实现或 vendor。
  - https://www.twilio.com/docs/segment/protocols/tracking-plan/create
  - https://docs.snowplow.io/docs/fundamentals/tracking-design-best-practice/
  - https://amplitude.com/docs/data/create-tracking-plan
  - https://amplitude.com/docs/data/data-planning-playbook
- W3C Privacy Principles / FTC：数据最小化降低泄露和误用风险；没有合法业务需要的敏感个人信息不要收集或保留。
  - https://www.w3.org/TR/privacy-principles/
  - https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- Google Analytics PII policy：第三方分析默认不得接收可直接识别、联系或定位个人的信息。
  - https://support.google.com/analytics/answer/6366371
  - https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- Vite / OpenFeature：Vite `VITE_*` 会暴露到客户端；实验分流和 feature flag evaluation context 需要稳定 targeting key 和可控上下文。
  - https://vite.dev/guide/env-and-mode
  - https://openfeature.dev/specification/sections/evaluation-context/
- Kratos / sqlc / gRPC / Vercel Geist：产品分析落地到 Go/Kratos event service、sqlc event/assignment tables、gRPC metadata、Vite typed analytics client 和清晰克制的设置/同意 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W2 OpenSpec / Risk 触发专项：客户数据导入、导出、同步与删除治理依据


- GDPR / EDPB 数据主体权利：访问、删除、限制处理、可携带性和反对处理要求系统能定位、导出、删除或说明例外。
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
  - https://www.edpb.europa.eu/sme-data-protection-guide/respect-individuals-rights_en
- NIST Privacy Framework / SP 800-88 Rev. 2：隐私风险管理覆盖数据生命周期；数据销毁/清除要按敏感级别和存储介质设计可验证控制。
  - https://www.nist.gov/privacy-framework
  - https://csrc.nist.gov/pubs/sp/800/88/r2/final
- FTC Protecting Personal Information：没有业务需要的敏感个人信息不要收集，确需保留时只保留必要时间并安全处置。
  - https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
- OWASP File Upload / CSV Injection：导入文件是不可信输入；CSV/表格导出需要防公式注入和恶意文件风险。
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
  - https://owasp.org/www-community/attacks/CSV_Injection
- RFC 4180 / PostgreSQL COPY：CSV 是常见交换格式；PostgreSQL COPY 可用于批量导入导出，但要理解列映射、服务器端文件权限和错误处理。
  - https://www.rfc-editor.org/info/rfc4180/
  - https://www.postgresql.org/docs/current/sql-copy.html
- Google SRE Data Processing Pipelines / Data Integrity：数据管道错误会导致用户可见问题；备份和归档不同，恢复和数据完整性需要可验证流程。
  - https://sre.google/workbook/data-processing/
  - https://sre.google/sre-book/data-processing-pipelines/
  - https://sre.google/sre-book/data-integrity/
- OpenAI Data Controls：AI application state、abuse monitoring logs、files、vector stores、responses 等有不同保留和删除边界，客户数据删除需逐项管理。
  - https://developers.openai.com/api/docs/guides/your-data
- Designing Data-Intensive Applications / Database Reliability Engineering：客户数据搬运和删除应服务可靠、可维护、可演进的数据系统，并具备可恢复、可审计、可自动化和可验证的操作习惯。
  - https://dataintensive.net/
  - https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/
- Kratos / sqlc / gRPC / Vercel Geist：客户数据生命周期落地到 Go/Kratos lifecycle service、sqlc import/export/sync/deletion job tables、gRPC 状态 API 和清晰克制的 Vite 导入/导出/删除 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W2 OpenSpec / Risk 触发专项：供应商处理方、DPA、子处理方与数据出境治理依据


- GDPR / EDPB：处理方合同、子处理方授权、跨境传输、SCC 和补充措施需要可验证记录；controller/processor 角色取决于实际处理目的和手段。
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
  - https://www.edpb.europa.eu/system/files/2023-10/EDPB_guidelines_202007_controllerprocessor_final_en.pdf
  - https://www.edpb.europa.eu/system/files/2022-04/edpb_recommendations_202001vo.2.0_supplementarymeasurestransferstools_en.pdf
- European Commission SCC / Data Privacy Framework：跨境机制需要合同模块、适用范围、补充措施和复评，不能只写“使用 SCC”。
  - https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en
  - https://www.dataprivacyframework.gov/
- CCPA/CPRA 服务提供商与承包商规则：合同要限制目的、禁止出售/共享、要求同等保护、协助消费者请求、允许合理审查并约束分包。
  - https://oag.ca.gov/privacy/ccpa
- FTC AI privacy/confidentiality commitments：AI 产品不得用隐蔽条款变化绕过隐私或保密承诺；第三方和训练用途变化需要真实透明。
  - https://www.ftc.gov/policy/advocacy-research/tech-at-ftc/2024/01/ai-companies-uphold-your-privacy-confidentiality-commitments
- NIST SP 800-161 Rev. 1 Update 1 / ISO 27036：供应链风险来自外部供应商可见性和控制下降；供应商关系需要信息安全治理、持续监控和责任划分。
  - https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final
  - https://www.iso.org/standard/82905.html
- OpenAI DPA / Data Controls / Enterprise Privacy / Sub-processors：AI provider 的训练、保留、ZDR、数据驻留、支持边界和子处理方要按实际项目设置记录。
  - https://openai.com/policies/data-processing-addendum/
  - https://developers.openai.com/api/docs/guides/your-data
  - https://openai.com/enterprise-privacy/
  - https://openai.com/policies/subprocessors/
- Google SRE SLO with Dependencies / Monitoring Distributed Systems：外部供应商在用户路径上时，SLO、依赖健康、告警和降级不能只看本服务。
  - https://sre.google/workbook/implementing-slos/
  - https://sre.google/sre-book/monitoring-distributed-systems/
- OWASP LLM Top 10 / Software Engineering at Google：LLM 供应链风险包括模型、数据、平台和第三方组件；外部依赖要被版本化、监控并纳入 review。
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/
  - https://abseil.io/resources/swe-book
- Kratos / sqlc / gRPC / Vercel Geist：供应商处理方治理落地到 Go/Kratos vendor client boundary、sqlc vendor tables、gRPC trace/deadline 和清晰克制的 Vite 隐私/区域/供应商设置 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W2 OpenSpec / Risk 触发专项：开源许可证、AI 生成内容与知识产权来源治理依据


- SPDX / REUSE / OSI：许可证和 copyright 信息应使用标准化、机器可读表达；开源许可证必须明确授予使用、修改和分发权利。
  - https://spdx.org/licenses/
  - https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/
  - https://reuse.software/spec-3.3/
  - https://opensource.org/licenses
  - https://opensource.org/osd
- npm / Go / GitHub Dependency Review：npm license 字段使用 SPDX expression；Go modules 是 Go 依赖管理基础；Dependency Review 可在 PR 阶段暴露许可证和依赖风险。
  - https://docs.npmjs.com/cli/v10/configuring-npm/package-json/
  - https://go.dev/ref/mod
  - https://pkg.go.dev/about
  - https://docs.github.com/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review
- U.S. Copyright Office / USPTO / WIPO：AI 生成材料的 copyrightability 需要人类作者贡献分析；版权、商标、专利和商业秘密不同；生成式 AI 采用要考虑多种 IP 风险和防护。
  - https://www.copyright.gov/ai/
  - https://www.copyright.gov/fair-use/
  - https://www.uspto.gov/trademarks/basics/trademark-patent-copyright
  - https://www.wipo.int/publications/en/details.jsp?id=4713
- OpenAI Terms / Services Agreement / Usage Policies：供应商条款可分配 input/output 权利，但输出可能不唯一，使用者仍需评估准确性、适用性、第三方权利和政策义务。
  - https://openai.com/policies/row-terms-of-use/
  - https://openai.com/policies/services-agreement/
  - https://openai.com/policies/usage-policies/
- Creative Commons / Open Data Commons / Hugging Face：内容、数据库、数据集和模型许可证不同于软件许可证；license、attribution、share-alike、non-commercial、dataset/model card metadata 要单独记录。
  - https://creativecommons.org/chooser/
  - https://wiki.creativecommons.org/wiki/Recommended_practices_for_attribution
  - https://opendatacommons.org/licenses/
  - https://huggingface.co/docs/hub/datasets-cards
  - https://huggingface.co/docs/hub/en/model-cards
- The Cathedral and the Bazaar / Producing Open Source Software / Software Engineering at Google：开源复用同时是技术、协作和许可系统；外部依赖网络会变化，需要持续 review。
  - https://www.catb.org/esr/writings/cathedral-bazaar/
  - https://producingoss.com/
  - https://abseil.io/resources/swe-book/html/ch21.html
- Kratos / sqlc / gRPC / Vercel Geist：IP/license/provenance 落地到 Go/Kratos dependency boundary、sqlc/generated code evidence、gRPC/SDK release package、Vite 素材来源和用户可理解的生成内容权利说明。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W6 Release 触发专项：客户合同、订单、SLA 与商业承诺治理依据


- Contract management / negotiation：合同治理要覆盖 pre-award、award、post-award，并在谈判前明确 BATNA、可接受范围和 walk-away 条件。
  - https://ncmahq.org/Web/Web/Standards---Practices/Contract-Management-Standard-Publication.aspx
  - https://www.pon.harvard.edu/category/daily/batna/
  - https://www.pon.harvard.edu/daily/negotiation-skills-daily/six-guidelines-for-getting-to-yes/
- Cornell LII contract basics：合同会创造可执行的相互义务；工程侧不解释法律效力，但要把承诺当作可能需要履行的义务管理。
  - https://www.law.cornell.edu/wex/contract
  - https://www.law.cornell.edu/ucc/2/2-204
- WorldCC Contract Design Pattern Library：合同应被读懂、理解并执行；一人公司需要把条款转换为行动清单和证据链接。
  - https://contract-design.worldcc.foundation/
  - https://www.worldcc.com/knowledge-insights/tools/contract-design-pattern-library.html
- Common Paper SaaS contract standards：Cloud Service Agreement、Service Level Agreement、DPA、NDA 提供 SaaS 标准条款、order form、key terms、linked policies 的轻量结构参考。
  - https://commonpaper.com/standards/cloud-service-agreement/
  - https://commonpaper.com/standards/cloud-service-agreement/2.0/
  - https://commonpaper.com/standards/service-level-agreement/
  - https://commonpaper.com/standards/data-processing-agreement/
  - https://commonpaper.com/standards/mutual-nda/
- Google SRE SLO/SLA：先定义 SLI/SLO、观测、error budget 和 runbook，再把 SLA 或商业补救写给客户。
  - https://sre.google/sre-book/service-level-objectives/
  - https://sre.google/workbook/implementing-slos/
  - https://sre.google/workbook/alerting-on-slos/
- OpenAI terms and policies：AI provider 的服务协议、DPA、service terms 和 usage policies 会限制你能向客户承诺的数据处理、beta 服务、输出、使用限制和赔偿边界。
  - https://openai.com/policies/services-agreement/
  - https://openai.com/policies/data-processing-addendum/
  - https://openai.com/policies/service-terms/
  - https://openai.com/policies/usage-policies/
- Kratos / sqlc / gRPC / Vite / Vercel Geist：商业承诺落地到 Go/Kratos contract/entitlement service、sqlc obligation/service-credit tables、gRPC internal APIs、Vite 客户可见权益界面和克制可扫描的合同/权益 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vite.dev/guide/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W7 Operate 触发专项：安全/隐私事故、漏洞披露与应急响应治理依据


- NIST SP 800-61 Rev. 3：事故响应建议嵌入 NIST CSF 2.0 风险管理活动，目标是提升准备、检测、响应、恢复和持续改进能力。
  - https://csrc.nist.gov/pubs/sp/800/61/r3/final
  - https://www.nist.gov/cyberframework
- Google SRE Incident Response / Postmortem Culture：事故响应需要预先结构化协调；复盘应无责、事实化、行动项可追踪。
  - https://sre.google/workbook/incident-response/
  - https://sre.google/workbook/postmortem-culture/
  - https://sre.google/sre-book/postmortem-culture/
- Breach notification and data breach response：FTC、GDPR Article 33/34、EDPB 和 HIPAA breach guidance 提醒个人数据事故需要按风险、角色、合同和法域判断通知。
  - https://www.ftc.gov/business-guidance/resources/data-breach-response-guide-business
  - https://gdpr-info.eu/art-33-gdpr/
  - https://gdpr-info.eu/art-34-gdpr/
  - https://www.edpb.europa.eu/system/files/2023-04/edpb_guidelines_202209_personal_data_breach_notification_v2.0_en.pdf
  - https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html
- Vulnerability disclosure / PSIRT：OWASP、CISA 和 FIRST 提供漏洞报告、协调披露、PSIRT 服务、severity 和 advisory 的参考。
  - https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html
  - https://www.cisa.gov/resources-tools/programs/coordinated-vulnerability-disclosure-program
  - https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1
  - https://www.first.org/cvss/v4.0/specification-document
  - https://www.cve.org/
- Threat and vulnerability prioritization：MITRE ATT&CK、CISA KEV、CVSS、CVE/NVD 用于给真实利用、攻击路径、严重度和公开漏洞建立共同语言。
  - https://attack.mitre.org/
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
  - https://nvd.nist.gov/vuln-metrics/cvss
  - https://nvd.nist.gov/general/news/cisa-exploit-catalog
- AI incident risk：NIST AI RMF Playbook 和 OWASP LLM Top 10 提醒 AI 事故包括 prompt injection、敏感信息泄露、供应链、RAG/向量、过度代理、工具误用、模型拒绝服务和监控/恢复。
  - https://airc.nist.gov/airmf-resources/playbook/
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/
  - https://genai.owasp.org/llm-top-10/
- Kratos / sqlc / gRPC / Vite / Vercel Geist：安全事故治理落地到 Go/Kratos security audit middleware、sqlc incident tables、gRPC internal incident APIs、Vite 安全通知/披露界面和克制可扫描的信息结构。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vite.dev/guide/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W4 Build 触发专项：开发者体验、API 文档、SDK 与示例治理依据


- Diátaxis / Google developer docs：开发者文档要区分 tutorial、how-to、reference、explanation，并保持清晰、一致、可执行。
  - https://diataxis.fr/
  - https://diataxis.fr/start-here/
  - https://developers.google.com/style
  - https://developers.google.com/tech-writing/resources
- API documentation and design：Google AIP-192 强调 API 文档是 API 设计的一部分；AIP-180、Google API Design Guide、OpenAPI 用于把 API surface、兼容性和 HTTP reference 机器化表达。
  - https://google.aip.dev/192
  - https://google.aip.dev/180
  - https://docs.cloud.google.com/apis/design
  - https://spec.openapis.org/oas/v3.2.0.html
  - https://learn.openapis.org/
- gRPC / Protobuf / Buf：gRPC 文档要提供概念、quickstart、教程和 reference；proto style、proto3、Buf breaking detection 用于保持 reference 与契约一致。
  - https://grpc.io/docs/
  - https://grpc.io/docs/languages/go/quickstart/
  - https://protobuf.dev/programming-guides/style/
  - https://protobuf.dev/programming-guides/proto3/
  - https://buf.build/docs/breaking/quickstart/
  - https://buf.build/docs/breaking/rules/
- Versioning and changelog：SemVer、Keep a Changelog、GitHub API versioning/changelog 和 Stripe changelog 用于把 public API/SDK 变化写给开发者，而不是倾倒 commit log。
  - https://semver.org/
  - https://keepachangelog.com/en/1.1.0/
  - https://docs.github.com/en/rest/about-the-rest-api/api-versions
  - https://docs.github.com/en/graphql/overview/changelog
  - https://docs.stripe.com/changelog
- SDK, examples, and API docs patterns：Stripe、GitHub、OpenAI 和 Google Cloud client libraries 展示了认证、错误、rate limit、idempotency、request id、sandbox/test mode、SDK 与版本支持的开发者体验边界。
  - https://docs.stripe.com/api
  - https://docs.stripe.com/api/idempotent_requests
  - https://docs.stripe.com/sdks
  - https://docs.github.com/en/rest
  - https://developers.openai.com/api/reference/overview/
  - https://developers.openai.com/api/docs/guides/rate-limits
  - https://developers.openai.com/api/docs/guides/error-codes
  - https://docs.cloud.google.com/apis/docs/client-libraries-best-practices
- Kratos / sqlc / gRPC / Vite / Vercel Geist：开发者体验落地到 Go/Kratos/gRPC API reference、sqlc-backed examples、generated clients、Vite/VitePress 文档站和克制可扫描的代码/表格/错误说明。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vite.dev/guide/
  - https://vite.dev/guide/build
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W6 Release 触发专项：对外承诺、声明与证据发布门禁依据


- FTC claim substantiation / advertising basics：客观产品或服务声明需要合理依据；广告声明必须真实、不可欺骗且有证据。
  - https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation
  - https://www.ftc.gov/business-guidance/advertising-marketing
- FTC AI enforcement：Operation AI Comply 说明 AI hype、专业替代、收入增长、虚假评论和欺骗性 AI 能力声明没有法律例外。
  - https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes
  - https://www.ftc.gov/industry/technology/artificial-intelligence
- NIST AI RMF / Generative AI Profile：AI 风险管理应覆盖设计、开发、使用、评估和持续管理；生成式 AI 需要跨生命周期治理。
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- NIST Privacy Framework：隐私实践需要连接业务目标、角色、数据处理和沟通；对外隐私声明要能落到实际数据流和控制。
  - https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.01162020.pdf
  - https://www.nist.gov/privacy-framework
- OECD AI Principles：AI actor 应提供透明、适当、可理解的信息，说明能力、限制、数据/输入和可挑战路径，并对 AI 系统生命周期保持问责。
  - https://www.oecd.org/en/topics/sub-issues/ai-principles.html
  - https://oecd.ai/en/ai-principles
- Google SRE SLO/SLA：SLO 是可测可靠性目标，SLA 是对外协议或商业后果；对外可靠性承诺要先有 SLI/SLO、error budget、观测和 runbook。
  - https://sre.google/sre-book/service-level-objectives/
  - https://sre.google/workbook/implementing-slos/
- OpenAI data and policy boundaries：API 数据控制、usage policies 和 DPA 影响“不训练”、保留、可接受使用、处理方和客户数据声明。
  - https://developers.openai.com/api/docs/guides/your-data
  - https://openai.com/policies/usage-policies/
  - https://openai.com/policies/data-processing-addendum/
  - https://openai.com/business-data/
- Kratos / sqlc / gRPC / Vite / Vercel Geist：对外声明门禁落地到 Go/Kratos claim/config/release services、sqlc claim tables、gRPC internal APIs、Vite trust/settings surfaces 和克制可扫描的声明 UI。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vite.dev/guide/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W9 Maintain 触发专项：开源发布、社区贡献与维护边界依据


- Open Source Guides / maintainer practices：维护者需要记录流程、学会说不、利用社区和自动化，也可在负担过高时暂停。
  - https://opensource.guide/best-practices/
  - https://opensource.guide/building-community/
  - https://opensource.guide/
- GitHub community health / issue templates：README、LICENSE、CONTRIBUTING、CODE_OF_CONDUCT、SUPPORT、SECURITY、issue/PR templates 能标准化贡献入口。
  - https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
  - https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates
- GitHub security reporting / advisories：公开仓库应有 SECURITY.md、私下漏洞报告和安全公告协作修复路径。
  - https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy
  - https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately
  - https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories
- Contributor Covenant / DCO：行为准则和贡献权利声明让社区规则和贡献授权显式化。
  - https://www.contributor-covenant.org/
  - https://developercertificate.org/
- OpenSSF / SLSA：Scorecard、Best Practices、SLSA 用于公开仓库供应链安全、依赖风险和发布完整性。
  - https://scorecard.dev/
  - https://openssf.org/projects/scorecard/
  - https://www.bestpractices.dev/en
  - https://openssf.org/projects/best-practices-badge/
  - https://slsa.dev/
- SPDX / REUSE / OSI：公开仓库许可证和文件级版权信息需要机器可读、可随分发保留。
  - https://spdx.org/licenses/
  - https://spdx.dev/learn/handling-license-info/
  - https://reuse.software/spec-3.2/
  - https://opensource.org/licenses
- Kratos / sqlc / gRPC / Vite / Vercel Geist：开源 SDK、示例、模板和文档落地到 Go module、Kratos/gRPC examples、sqlc synthetic fixtures、Vite starter/docs 和克制可扫描的开源项目信息结构。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/
  - https://vite.dev/guide/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W8 Learn 触发专项：AI 质量回归、线上质量事故与回滚依据


- Google / ML production readiness：Hidden Technical Debt、ML Test Score 和 Rules of ML 强调 ML/AI 系统的隐性依赖、训练/服务偏移、监控、可调试和回滚。
  - https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/
  - https://papers.neurips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf
  - https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
  - https://research.google.com/pubs/archive/aad9f93b86b7addfea4c419b9100c6cdd26cacea.pdf
  - https://developers.google.com/machine-learning/guides/rules-of-ml
- Google SRE：AI 质量回归借用 SLO、burn-rate alert、incident response 和 blameless postmortem 的结构，但只保留一人公司能执行的止血、时间线和行动项。
  - https://sre.google/sre-book/service-level-objectives/
  - https://sre.google/workbook/implementing-slos/
  - https://sre.google/workbook/alerting-on-slos/
  - https://sre.google/resources/practices-and-processes/incident-management-guide/
  - https://sre.google/workbook/incident-response/
  - https://sre.google/workbook/postmortem-culture/
  - https://sre.google/sre-book/postmortem-culture/
- OpenAI evals / tracing：生产 AI 质量需要用真实任务定义 eval，agent workflow 先用 traces 调试，再进入 datasets、graders 和 eval runs。
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
  - https://developers.openai.com/api/docs/guides/evals
  - https://developers.openai.com/api/docs/guides/agent-evals
  - https://developers.openai.com/api/docs/guides/agents
  - https://openai.github.io/openai-agents-python/tracing/
- OpenTelemetry / NIST：GenAI telemetry 提供标准化 AI 调用信号；NIST AI RMF/Generative AI Profile 提醒 AI 风险需要跨生命周期测量、管理和持续监控。
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/
  - https://github.com/open-telemetry/semantic-conventions-genai
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- Kratos / sqlc / gRPC / Vite / Vercel Geist：质量回归治理落地到 Go/Kratos middleware/usecase、sqlc incident/action tables、gRPC status、Vite 降级/反馈 UI 和克制清晰的信息结构。
  - https://go-kratos.dev/docs/component/middleware/overview/
  - https://go-kratos.dev/docs/component/metrics/
  - https://docs.sqlc.dev/
  - https://docs.sqlc.dev/en/stable/tutorials/getting-started.html
  - https://grpc.io/docs/guides/status-codes/
  - https://vite.dev/guide/build
  - https://vite.dev/guide/env-and-mode
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W6 Release 触发专项：客户试点、上线导入与租户交付依据


- 《人月神话》：客户上线中的每个特例都会增加沟通、协调和概念完整性成本；一人公司要把客户特例压到租户配置、flag、entitlement 和明确边界中。
- 小型项目管理：小项目用清晰范围、责任、节奏和退出条件替代复杂流程；本专项用五个工件控制客户上线。
- The Lean Startup / Customer Development / The Mom Test：试点应验证真实客户行为、业务结果和愿意投入，而不是验证礼貌性正反馈。
- Crossing the Chasm：客户上线要交付 whole product，包括配置、数据、支持、培训、验收和退出路径。
- Google SRE Reliable Product Launches：Google 将 launch 视为外部可见变化；launch process 应 lightweight、robust、thorough、scalable、adaptable，并通过可管理 checklist 降低失败。
  - https://sre.google/sre-book/reliable-product-launches/
- Google SRE Launch Checklist：上线 checklist 应覆盖架构、依赖、容量、失败模式、客户端行为、流程和自动化等领域。
  - https://sre.google/sre-book/launch-checklist/
- Google SRE Production Readiness Review：PRR 在生产支持前识别可靠性需求，避免 late-stage 可靠性成本。
  - https://sre.google/sre-book/evolving-sre-engagement-model/
- Google Cloud Well-Architected Operational Readiness：go-live 和 day-2 需要明确期望、监控、告警、性能、容量和运营责任。
  - https://docs.cloud.google.com/architecture/framework/operational-excellence/operational-readiness-and-performance-using-cloudops
- AWS SaaS Lens Tenant Onboarding：tenant onboarding 应能以可预测方式配置租户、身份、隔离、计费、配置和基础设施。
  - https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/tenant-onboarding.html
  - https://wa.aws.amazon.com/saas.question.OPS_3.en.html
- OpenAI Production / Data / Safety Best Practices：AI 生产上线要考虑安全、速率、成本、数据控制、人工监督和对抗性测试。
  - https://developers.openai.com/api/docs/guides/production-best-practices
  - https://developers.openai.com/api/docs/guides/your-data
  - https://developers.openai.com/api/docs/guides/safety-best-practices
- Stripe Go-live Checklist：live key、live webhook、错误处理、安全日志、test/live 数据边界和支付边界是上线前检查项。
  - https://docs.stripe.com/get-started/checklist/go-live
- Gainsight / Intercom Customer Onboarding：客户上线要覆盖 setup、training、support、engagement metrics 和 lifecycle onboarding。
  - https://www.gainsight.com/blog/customer-onboarding/
  - https://www.gainsight.com/essential-guide/customer-success/
  - https://www.intercom.com/blog/onboarding-guide/

## W0 Intake：路线图、工作入口与研发优先级依据


- 《人月神话》：少数清晰判断保护概念完整性；把所有请求并行推进会增加协调成本和认知负担。
- 小型项目管理：小项目只保留范围、责任、节奏、停止条件和可恢复记录；不需要企业级 PMO。
- Good Strategy / Bad Strategy：路线图需要诊断、指导方针和连贯行动，不是功能愿望清单。
- Escaping the Build Trap：产品工作要围绕 outcome，不以功能输出数量衡量成功。
- Shape Up：appetite 先于 scope；fixed time / variable scope、soft no、bets-not-backlogs 和 circuit breaker 适合一人公司保护当前焦点。
  - https://basecamp.com/shapeup/1.2-chapter-03
  - https://basecamp.com/shapeup
- ProductTalk / Continuous Discovery：Opportunity Solution Tree 把 outcome、opportunity、solution、experiment 连起来；Now/Next/Later roadmap 用不确定性分层表达未来。
  - https://www.producttalk.org/opportunity-solution-trees/
  - https://www.producttalk.org/product-roadmaps/
- ProdPad Now/Next/Later：Now/Next/Later roadmap 用时间视野和业务目标组织工作，避免把远期想法写成日期承诺。
  - https://www.prodpad.com/blog/invented-now-next-later-roadmap/
- Intercom RICE：reach、impact、confidence、effort 能辅助比较候选，但不替代战略和风险判断。
  - https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
- DORA Working in Small Batches / Trunk-Based Development：小批量能更快测试假设、减少返工和降低合并风险。
  - https://dora.dev/capabilities/working-in-small-batches/
  - https://dora.dev/capabilities/trunk-based-development/
- Google SRE Dealing with Interrupts / Eliminating Toil：中断、tickets、toil 会破坏专注时间；需要区分项目工作、interrupt buffer 和根因消除。
  - https://sre.google/sre-book/dealing-with-interrupts/
  - https://sre.google/sre-book/eliminating-toil/
- GitHub Projects / Issue Templates：项目视图、字段、状态更新、issue templates 和自动化可减少低质量请求和重复上下文。
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects
  - https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
- Linear Triage：triage 状态用于在接受进入 backlog/cycle 前先审查 issue，适合作为工作入口概念参考。
  - https://linear.app/docs/conceptual-model

## W3 AI Behavior 触发专项：AI 模型优化、微调/蒸馏与训练运行依据


- 《人月神话》：模型优化不是银弹；真正困难的是让产品定义、数据、评测、运行和回滚边界保持一致。
- 小型项目管理：一人公司不维护完整 MLOps 平台；W3 模型优化专项只保留优化 brief、数据计划、运行记录、验证报告和 rollout 决策。
- OpenAI Model Optimization：OpenAI 将优化描述为 eval、prompt engineering 和 fine-tuning 的反馈循环；应先建立 baseline eval，再调整 prompt、数据或候选模型。
  - https://developers.openai.com/api/docs/guides/model-optimization
- OpenAI Optimizing LLM Accuracy：优化应先判断失败原因；RAG 解决上下文/知识问题，fine-tuning 更适合一致性、格式、风格或固定任务行为；不要为了 sophistication 直接上 RAG + fine-tuning。
  - https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy
- OpenAI Supervised Fine-Tuning / Fine-Tuning Best Practices：fine-tuning 前要有可靠 eval；训练和测试/评测数据要分离；训练样本应代表生产输入输出，且从少量高质量样本开始。
  - https://developers.openai.com/api/docs/guides/supervised-fine-tuning
  - https://developers.openai.com/api/docs/guides/fine-tuning-best-practices
- OpenAI Model Selection / Latency Optimization：先达到准确率目标，再优化成本和延迟；可通过小模型、减少 token、缓存、批处理、蒸馏等方式优化。
  - https://developers.openai.com/api/docs/guides/model-selection
  - https://developers.openai.com/api/docs/guides/latency-optimization
- OpenAI fine-tuning current availability：官方 fine-tuning 文档显示部分平台能力正在退场或 legacy 化；训练运行前必须确认模型支持、账号权限和 deprecation 状态。
  - https://developers.openai.com/api/docs/guides/supervised-fine-tuning
  - https://developers.openai.com/api/docs/guides/direct-preference-optimization
  - https://developers.openai.com/api/docs/guides/reinforcement-fine-tuning
- Google / ML production readiness：Hidden Technical Debt、ML Test Score 和 Rules of ML 提醒训练数据、模型、基础设施和监控都需要测试，训练/服务偏移和隐式依赖会形成长期债务。
  - https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/
  - https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
  - https://developers.google.com/machine-learning/guides/rules-of-ml
- NIST AI RMF / Generative AI Profile：AI 风险管理覆盖设计、开发、评估、部署、使用和持续监控；生成式 AI 还要关注隐私、安全、IP、信息完整性和价值链风险。
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

## W5 Verify 触发专项：性能预算、负载验证与性能回归依据


- 《人月神话》：性能优化不是银弹；真正困难的是在需求、接口、数据、运行环境和用户体验之间保持概念完整性。
- 小型项目管理：一人公司不维护性能工程团队或完整压测平台；本专项只保留预算、负载画像、benchmark 计划、回归报告和复盘。
- Google SRE Monitoring / Handling Overload：性能必须连接 latency、traffic、errors、saturation；过载时要用资源上限、优先级、降级、快速拒绝和 retry budget 保护系统。
  - https://sre.google/workbook/monitoring/
  - https://sre.google/sre-book/handling-overload/
- Brendan Gregg Systems Performance / USE Method：性能调查先看每个资源的 utilization、saturation、errors，避免只看平均值或单点指标。
  - https://www.brendangregg.com/usemethod.html
  - https://www.brendangregg.com/sysperfbook.html
- The Art of Capacity Planning：容量规划要基于测量、部署和管理 web 负载，避免在流量峰值到来后才发现容量缺口。
  - https://www.oreilly.com/library/view/the-art-of/9781491939192/
- Go 官方 testing / pprof：Go benchmark、parallel benchmark 和 pprof 是一人公司定位代码级性能回归的低成本入口。
  - https://pkg.go.dev/testing
  - https://go.dev/blog/pprof
- gRPC Performance Best Practices：长生命周期数据流可用 streaming 减少重复 RPC 开销；高并发或长连接场景要注意 HTTP/2 stream queueing 和连接策略。
  - https://grpc.io/docs/guides/performance/
- Web Vitals：LCP、INP、CLS 是前端真实用户体验的核心指标；lab 数据适合发布前发现回归，field 数据适合持续确认。
  - https://web.dev/articles/vitals
- PostgreSQL EXPLAIN：查询性能要看计划、实际行数和执行时间，同时理解 `EXPLAIN ANALYZE` 的测量边界。
  - https://www.postgresql.org/docs/current/using-explain.html
- Vite Performance：Vite 默认很快，但项目增长后仍要检查 server start、page load 和 build 性能。
  - https://vite.dev/guide/performance
- OpenAI Latency Optimization：AI 延迟可通过更快处理 token、更少输出/输入 token、更少请求、并行化、改善等待体验或不用 LLM 来优化。
  - https://developers.openai.com/api/docs/guides/latency-optimization
- Kratos / sqlc / gRPC / Vite / Vercel Geist：性能治理落地到 Go/Kratos middleware/usecase、sqlc query/EXPLAIN、gRPC deadline/retry、Vite build/Web Vitals 和克制清晰的内部证据界面。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/languages/go/
  - https://vite.dev/guide/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W5 Verify 触发专项：韧性演练、故障注入与降级验证依据


- 《人月神话》：复杂系统没有银弹；韧性来自清晰接口、概念完整性和持续暴露隐藏耦合。
- 小型项目管理：一人公司不维护重型 chaos program；本专项只保留失败模式、实验计划、注入运行、降级证据和复盘。
- Google SRE Testing for Reliability：可靠性测试用于减少变更后对未来行为的不确定性；没有尝试过的路径应假设可能损坏。
  - https://sre.google/sre-book/testing-reliability/
- Google SRE Addressing Cascading Failures / Handling Overload：级联故障常由过载、无界重试、资源耗尽和依赖失败放大；需要 backoff、jitter、限流、降级和快速失败。
  - https://sre.google/sre-book/addressing-cascading-failures/
  - https://sre.google/sre-book/handling-overload/
- Google SRE Incident Response / DiRT：演练能在不影响客户的控制场景中训练响应流程，并在事后复盘缺口。
  - https://sre.google/workbook/incident-response/
  - https://cloud.google.com/blog/products/management-tools/sre-principles-in-practice-for-business-continuity
- Principles of Chaos Engineering：实验应定义 steady state、提出假设、注入真实世界变量、观察差异并最小化 blast radius。
  - https://principlesofchaos.org/
- Release It!：稳定性模式包括 timeout、circuit breaker、bulkhead、fail fast、test harness、shed load、back pressure 和 governor。
  - https://pragprog.com/titles/mnee2/release-it-second-edition/
- Building Secure and Reliable Systems：单系统 fault injection 可在不打扰全系统或依赖方的情况下验证 timeout 和异常处理。
  - https://google.github.io/building-secure-and-reliable-systems/raw/ch16.html
- gRPC Deadlines / Go context：gRPC 默认没有 deadline；Go context 需要取消以释放资源，并让长任务停止。
  - https://grpc.io/docs/guides/deadlines/
  - https://pkg.go.dev/context
- Kratos Circuit Breaker：client circuit breaker 触发后应快速失败，返回 circuit breaker 错误，避免继续压垮下游。
  - https://go-kratos.dev/docs/component/middleware/circuitbreaker/
- OpenAI Rate Limits：rate limit 要用带随机 jitter 的指数退避和最大重试次数；失败请求仍会消耗每分钟限额，连续重发不可行。
  - https://developers.openai.com/api/docs/guides/rate-limits
- AWS Well-Architected Game Days：game day 用受控方式模拟失败，测试系统、流程和团队响应。
  - https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_testing_resiliency_game_days_resiliency.html
- Kratos / sqlc / gRPC / Vite / Vercel Geist：韧性演练落地到 Go/Kratos middleware、sqlc 幂等与数据库失败、gRPC deadline、Vite degraded UI 和克制清晰的错误/降级状态。
  - https://go-kratos.dev/docs/
  - https://docs.sqlc.dev/
  - https://grpc.io/docs/languages/go/
  - https://vite.dev/guide/
  - https://vercel.com/design.md
  - https://vercel.com/design.dark.md

## W7 Operate 触发专项：凭据、密钥与服务账号生命周期依据


- 《人月神话》：密钥治理的难点不是某个工具，而是凭据用途、owner、作用域、撤销路径和轮换证据的概念完整性。
- 小型项目管理：一人公司不维护完整 PAM/KMS/GRC 平台；本专项只保留清单、访问策略、轮换计划、轮换记录和泄露复盘。
- OWASP Secrets Management：secret 管理需要集中存储、访问控制、自动化、审计、生命周期、轮换、撤销、过期、policy、metadata 和 incident response。
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- NIST SP 800-57 Part 1 Rev. 5：key management 需要保护 key material，定义 key 用途、生命周期、backup、compromise、inventory 和 policy。
  - https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- Twelve-Factor App Config：配置与代码分离，代码库应能随时公开而不暴露凭据。
  - https://12factor.net/config
- GitHub Secret Scanning / Push Protection：secret scanning 发现仓库历史、PR、issue、discussion 等位置的凭据；push protection 在凭据进入仓库前阻止提交。
  - https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
  - https://docs.github.com/en/code-security/concepts/secret-security/push-protection
- OpenAI API Key Safety / Production Best Practices：API key 不应共享、暴露到浏览器/移动端或提交仓库；生产使用环境变量或 secret management service，并按 project 隔离 staging/production、监控 usage。
  - https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
  - https://developers.openai.com/api/docs/guides/production-best-practices
- Google Cloud Secret Manager Best Practices：周期性轮换限制泄露影响、移除不再需要访问的人，并通过 inventory、access logs、组织策略和 quota 管理降低事故风险。
  - https://cloud.google.com/secret-manager/docs/best-practices
- Building Secure and Reliable Systems：简单、可理解的设计能降低攻击面，提升事故时的 MTTR；credential boundary 也应保持简单。
  - https://google.github.io/building-secure-and-reliable-systems/raw/ch01.html
- Kratos Config / gRPC Auth / Vite Env：Go/Kratos 支持 runtime config sources，gRPC credential 应配合 TLS/channel 边界，Vite `VITE_*` 会进入浏览器 bundle，不能放敏感值。
  - https://go-kratos.dev/docs/component/config/
  - https://grpc.io/docs/guides/auth/
  - https://vite.dev/guide/env-and-mode

## W3 AI Behavior 触发专项：国际化、本地化、时区/货币与多语言 AI 体验依据


- 《人月神话》：本地化复杂度来自概念不一致；语言、时区、货币、AI 输出和错误文案必须共享同一套产品规则。
- 小型项目管理：一人公司不维护完整翻译平台；W3 本地化专项只保留 locale policy、message catalog、time/currency rules、AI locale eval 和 localization review。
- W3C Internationalization：Web 技术应支持不同语言、文字、书写方向和文化环境。
  - https://www.w3.org/International/
- W3C String Metadata / Unicode Bidirectional Algorithm：字符串需要 language 与 direction metadata；RTL/BiDi 不能只靠猜测或 CSS 补丁。
  - https://www.w3.org/TR/string-meta/
  - https://unicode.org/reports/tr9/
- IETF BCP 47 / RFC 5646：language tag 用于标识人类语言；产品 locale 不应自造不可互操作的枚举。
  - https://datatracker.ietf.org/doc/html/rfc5646
  - https://www.rfc-editor.org/info/bcp47/
- Unicode CLDR / LDML：CLDR 提供日期、数字、货币、复数、区域等 locale 数据，是平台 Intl 和多语言软件的重要基础。
  - https://cldr.unicode.org/
  - https://www.unicode.org/reports/tr35/
- IANA Time Zone Database：time zone 数据会周期性更新以反映政治边界、UTC offset 和 DST 规则变化；应使用 IANA zone name，而不只存 offset。
  - https://www.iana.org/time-zones
- ISO 4217：货币使用三字母和数字标准代码，减少多币种展示和账单歧义。
  - https://www.iso.org/iso-4217-currency-codes.html
- ECMAScript Intl / W3C Intl guide：浏览器原生 Intl 支持 locale-sensitive 的日期、数字、货币和排序格式。
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
  - https://www.w3.org/International/articles/intl/index
- Go `time` / `golang.org/x/text/language`：Go 的时间计算使用 location 语义；`x/text/language` 实现 BCP 47 language tags 和匹配。
  - https://pkg.go.dev/time
  - https://pkg.go.dev/golang.org/x/text/language
  - https://go.dev/blog/matchlang
- PostgreSQL date/time：`timestamp with time zone` 和 `timestamp without time zone` 语义不同；业务需要原始用户时区时必须显式记录。
  - https://www.postgresql.org/docs/current/datatype-datetime.html
- OpenAI Prompt Engineering / evaluation best practices：多语言 AI 行为要用明确指令、代表样例和 eval 验证，不假设模型稳定保持目标语言。
  - https://developers.openai.com/api/docs/guides/prompt-engineering
  - https://developers.openai.com/api/docs/guides/evaluation-best-practices
