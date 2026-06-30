# 安全、隐私与供应链基线规范
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“威胁模型、数据处理、依赖供应链、secret、构建来源或安全隐私门禁”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## 目标

为一人公司建立一套轻量但可检查的安全、隐私与软件供应链基线：每个生产服务或用户可见 AI workflow 都明确威胁模型、数据处理边界、依赖与构建来源、secrets 管理和高风险人工 checkpoint。目标不是做企业合规认证，而是避免一人公司最容易“看不见直到出事”的风险：泄露密钥、把用户数据发给未评估的外部服务、依赖漏洞进入生产、AI 被 prompt injection 或工具链攻击、构建 artifact 无来源可追。

本阶段默认技术路径：Go/Kratos/sqlc/gRPC 服务使用 Go 官方 vulnerability tooling、最小权限 CI、可追踪 artifact；Vite 前端使用锁文件、依赖审计和构建产物记录；AI workflow 记录 prompt/data/tool 安全边界、外部处理方和安全测试。

## 本专项只解决什么

- 最小 threat model：资产、入口、信任边界、滥用场景、控制、未决风险。
- 最小 privacy record：数据分类、外部处理方、保留期、日志、删除/导出、AI 数据使用。
- 最小 supply-chain record：语言、包管理器、锁文件、依赖扫描、SAST、secret scanning、SBOM/provenance、CI 权限。
- 最小 secrets record：存储、访问、轮换、CI/CD、泄露响应。
- AI 安全边界：prompt injection、敏感信息泄露、不安全输出处理、工具权限、外部模型数据保留。
- 安全隐私 skill 与本地检查脚本。

不在本阶段展开：SOC 2、ISO 27001、HIPAA/PCI 合规认证、正式 DPA 模板、企业安全团队流程、渗透测试采购、完整 GRC 平台。需要时单独开 OpenSpec change。

## 依据转译

- 《人月神话》：安全工具不是银弹。真正要降低的是概念复杂度：边界清楚、接口少、默认安全、例外可见。
- 小型项目管理：一人公司只保留能阻止高损失事故和恢复上下文的工件：threat model、privacy record、supply-chain record、secrets runbook。
- Ross Anderson, Security Engineering：安全工程关注系统在错误、攻击、激励和人类行为下是否仍可靠。本专项因此把“攻击者会怎么绕过我们”和“人会怎么误操作”写进 artifacts。
- Saltzer & Schroeder：继续采用 least privilege、fail-safe defaults、complete mediation、economy of mechanism。默认拒绝、最小权限、每条外部边界都要可解释。
- Threat Modeling Manifesto / OWASP Threat Modeling：威胁建模用四个问题压缩：在做什么、会出什么错、怎么处理、做得够好吗。
- NIST SSDF SP 800-218：安全实践应集成进 SDLC，用来减少已发布软件漏洞、降低未发现漏洞被利用的影响，并解决根因。
- OWASP SAMM：安全保障应按组织风险迭代改进；一人公司使用最小 maturity slice，不照搬完整模型。
- OWASP ASVS / Cheat Sheets：ASVS 提供应用安全验证基线；OWASP Cheat Sheets 提供高价值主题 guidance，本专项只抽取与当前服务风险相关的控制。
- OWASP Secrets Management：secrets 需要集中存储、访问控制、审计、轮换和泄露响应，不能散落在代码、配置、CI 日志或 prompt 中。
- OWASP Top 10 for LLM Applications 2025：LLM 应用要关注 prompt injection、sensitive information disclosure、supply chain、不安全输出处理、模型 DoS、过度代理等风险。
- OpenAI 官方 data controls / safety best practices：API 使用会涉及 abuse monitoring logs、应用状态和数据保留控制；AI 应用需要 moderation、adversarial testing、human oversight 和 prompt 边界。
- NIST Privacy Framework / NIST AI RMF Generative AI Profile：隐私风险和生成式 AI 风险应在设计、开发、使用和评估中管理。
- SLSA / CycloneDX / GitHub / Go 官方文档：供应链安全要有来源、依赖、构建和 artifact 证据；Go 使用 `govulncheck` 降低依赖漏洞噪音；GitHub secret scanning、CodeQL、Dependabot、artifact attestations 可作为默认自动化守门。

## 默认决策

- 每个生产服务或用户可见 AI workflow 必须有四个安全基线 artifact：threat model、privacy record、supply-chain record、secrets record。
- 默认不把 secret、API key、token、密码、session id、私钥写入仓库、日志、prompt、eval fixture、migration 或文档样例。
- 默认 CI/CD token 最小权限；GitHub Actions 默认 `contents: read`，单 job 按需提升。
- 默认 Go 服务运行 `govulncheck ./...` 或记录跳过原因；Vite/npm 项目运行 `npm audit --audit-level=high` 或等价依赖漏洞检查。
- 默认生产 artifact 需要 SBOM 或 provenance 计划；公开/客户交付 artifact 优先生成 SBOM 和 attestation。
- 默认 AI workflow 记录外部模型供应商、prompt/response 是否包含用户数据、保留期、ZDR/modified monitoring 是否适用、是否发送文件/图像。
- 默认 AI 工具输出不直接执行高风险副作用；必须经过 schema 校验、权限检查和必要的人审。
- 默认每月只处理一个最高风险 security/privacy/supply-chain 改进，避免安全工作变成无底洞。

## Security artifact 目录规范

推荐落点：

```text
security/
  threat-models/<service>.md
  privacy/<service>.json
  supply-chain/<service>.json
  secrets/<service>.md
```

`security/threat-models/<service>.md` 最少写：

```markdown
# <service> Threat Model
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“威胁模型、数据处理、依赖供应链、secret、构建来源或安全隐私门禁”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## Scope

## Assets

## Trust Boundaries

## Entry Points

## Abuse Cases

## Controls / Mitigations

## Open Risks

## Review Cadence
```

AI workflow 的 threat model 还必须显式覆盖 prompt injection、sensitive information disclosure、insecure output handling、tool misuse 或说明不适用。

`security/privacy/<service>.json` 是数据处理事实来源：

```json
{
  "service": "ai-assistant",
  "owner": "founder",
  "data_classes": ["account", "workspace_content", "prompt", "response"],
  "personal_data": true,
  "sensitive_data": false,
  "processors": [
    {
      "name": "OpenAI",
      "purpose": "model inference",
      "data_sent": ["prompt", "response context"],
      "retention_note": "OpenAI API data controls apply; verify current project setting before production"
    }
  ],
  "retention": {
    "application": "30 days for debug traces unless user deletes workspace",
    "logs": "14 days, no full prompt unless debug flag approved"
  },
  "logging": {
    "allowed": ["request_id", "tenant_id", "model", "latency", "token_count"],
    "forbidden": ["secret", "password", "full token", "raw sensitive prompt"]
  },
  "encryption": {
    "in_transit": "TLS",
    "at_rest": "managed database/storage encryption"
  },
  "deletion_export": "user workspace deletion removes prompts and generated outputs from application storage",
  "ai_data_use": {
    "external_model": true,
    "training_opt_in": false,
    "files_or_images_sent": false,
    "zdr_required": false
  },
  "review_cadence": "monthly",
  "human_checkpoint": {
    "required_for": ["new_external_processor", "sensitive_data", "training_opt_in", "zdr_required", "longer_retention"]
  }
}
```

`security/supply-chain/<service>.json` 是依赖与构建事实来源：

```json
{
  "service": "ai-assistant",
  "owner": "founder",
  "languages": ["go", "typescript"],
  "package_managers": ["go modules", "npm"],
  "lockfiles": ["go.sum", "package-lock.json"],
  "dependency_scans": ["govulncheck ./...", "npm audit --audit-level=high", "dependabot alerts"],
  "sast": ["CodeQL default setup for Go and JavaScript/TypeScript"],
  "secret_scanning": "GitHub secret scanning or local equivalent before release",
  "sbom": {
    "required": true,
    "format": "CycloneDX or SPDX",
    "path": "artifacts/sbom/ai-assistant.json"
  },
  "provenance": {
    "required_for": ["production container", "public binary", "customer-delivered artifact"],
    "method": "GitHub artifact attestation or equivalent"
  },
  "ci_permissions": {
    "default": "contents: read",
    "write_permissions": ["id-token for OIDC deploy", "attestations for provenance"]
  },
  "update_cadence": "weekly security alerts, monthly dependency review",
  "human_checkpoint": {
    "required_for": ["critical_vulnerability_accepted", "unsigned_release", "unpinned_action", "new_build_secret"]
  }
}
```

`security/secrets/<service>.md` 最少写：

```markdown
# <service> Secrets
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“威胁模型、数据处理、依赖供应链、secret、构建来源或安全隐私门禁”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## Storage

## Access

## Rotation

## CI/CD

## Incident Response

## Review Cadence
```

## 实现顺序

1. 写 OpenSpec：服务资产、数据、依赖、外部处理方和高风险副作用。
2. 写 `security/threat-models/<service>.md`：先用四问法，不画复杂图也可以。
3. 写 `security/privacy/<service>.json`：数据类别、处理方、保留、日志、删除、AI 数据使用。
4. 写 `security/supply-chain/<service>.json`：语言、包管理器、锁文件、扫描、SBOM/provenance、CI 权限。
5. 写 `security/secrets/<service>.md`：存储、访问、轮换、CI/CD、泄露响应。
6. 在 CI 或 release checklist 中连接检查：Go `govulncheck`、npm audit/Dependabot、CodeQL/等价 SAST、secret scanning、SBOM/provenance。
7. 对 AI workflow 补充 adversarial cases：prompt injection、敏感信息诱导、工具越权、不安全输出。
8. 每次高风险变更后更新 artifacts；每月只选择一个最高风险改进。

## AI 安全与隐私规则

- Prompt injection 默认存在；任何能读取私有数据或调用工具的 workflow 都要有隔离、权限、输出校验和失败模式。
- 模型输出默认不可信；进入 SQL、shell、文件、HTTP、支付、通知、权限变更前必须由程序验证和授权。
- 用户数据发给新模型、embedding、reranker、analytics、logging、support 工具时，必须更新 privacy record。
- Debug traces、eval fixtures 和 prompt logs 默认不保留完整敏感内容；必须保留时写 retention 和访问控制。
- 处理医疗、金融、法律、未成年人、政府身份、精确位置、生物识别等敏感数据时，默认人工 checkpoint。

## 供应链规则

- 锁文件是默认要求；没有锁文件的生产项目必须说明原因。
- 新增依赖时优先少依赖、小依赖、活跃维护、许可证清晰；重大依赖必须能解释替代方案。
- GitHub Actions 或等价 CI 默认最小权限；外部 action 优先 pin 到 commit SHA 或明确接受风险。
- 生产容器、公开 binary、客户交付 artifact 默认要有 SBOM/provenance 计划；早期内部服务可先记录计划，真实发布前补齐。
- Critical/high 漏洞不得静默发布；接受风险必须写 human checkpoint、影响范围、补救日期。

## 只问人的关键判断

默认不问：文档小节顺序、普通威胁命名、低风险依赖更新、扫描工具文案、artifact 路径命名。

必须问：

- 是否处理敏感个人数据或受监管数据。
- 是否把用户数据发送给新的外部模型、分析、日志、客服或供应商。
- 是否允许模型供应商把数据用于训练或长期保留。
- 是否接受 critical/high 漏洞、未签名 release、没有 SBOM/provenance 的客户交付 artifact。
- 是否新增能访问生产 secrets 的 CI job、外部 action 或第三方服务。
- 是否允许 AI tool 执行金钱、删除、权限、通知、外部提交等高风险副作用。

当前建议默认接受：所有生产服务和用户可见 AI workflow 必须有 `security/threat-models/<service>.md`、`security/privacy/<service>.json`、`security/supply-chain/<service>.json`、`security/secrets/<service>.md`；没有这四个工件不得进入生产。

## 本专项 Review A：一人公司可落地性

结论：可落地，但必须保持“薄安全层”。

- 四个 artifact 覆盖安全、隐私、供应链和 secrets，不需要安全团队或 GRC 平台。
- threat model 用四问法，比完整 STRIDE 表更适合单人快速执行。
- Go/Vite/AI 的检查都能连接现有 release gates，不要求新建复杂平台。
- 最大摩擦是 privacy record 容易被漏写；因此把新外部处理方和 AI 数据使用列为脚本检查项。
- 下一步应在第一个真实服务上用 `security-privacy-supply-chain-guard` 生成 artifacts。

## 本专项 Review B：产品/工程/运维风险

结论：本专项主要降低泄密、隐私误用、依赖漏洞和供应链篡改风险。

- 已把 secret 泄露、第三方数据处理、critical 漏洞、未签名 release、AI 工具副作用列为人工 checkpoint。
- 已把 OpenAI data controls 和安全实践转为内部 privacy/AI 安全记录，而不假设供应商设置永远不变。
- 已连接 NIST SSDF、OWASP SAMM/ASVS 和 SLSA/CycloneDX，但只取一人公司可执行的最小 slice。
- 已要求模型输出不可信、工具调用需授权，连接 W3 AI eval 和 W2 auth 边界。
- 仍不承诺合规认证；真实客户或行业要求出现时再单独开合规 change。


