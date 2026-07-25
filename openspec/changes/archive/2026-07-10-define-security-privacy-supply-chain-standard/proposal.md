# 提案：定义安全、隐私与供应链基线规范

## 意图

为一人公司建立可检查的安全、隐私与供应链基线，让每个生产服务或用户可见 AI workflow 明确 threat model、privacy record、supply-chain record、secrets record 和 human checkpoint，降低密钥泄露、隐私误用、依赖漏洞、供应链篡改和 AI 工具越权风险。

## 范围

- 定义 security artifacts 目录和最小文件。
- 定义 threat model、privacy record、supply-chain record、secrets record 的字段和模板。
- 定义 Go/Vite/AI 项目的依赖扫描、SAST、secret scanning、SBOM/provenance、CI 权限默认要求。
- 定义 AI prompt injection、敏感信息泄露、不安全输出处理、工具权限和数据保留边界。
- 定义高风险安全/隐私/供应链动作的人工 checkpoint。
- 创建安全隐私供应链落地 skill 和检查脚本。

## 不做

- 不实现 SOC 2、ISO 27001、HIPAA、PCI 等合规认证。
- 不采购或集成商业安全平台。
- 不替代 W4 数据迁移、W2 auth、W2 成本容量规范。
- 不承诺正式法律隐私结论。

## 依据

- 《人月神话》：安全不是银弹，边界和概念完整性比堆工具更重要。
- 小型项目管理：只保留阻止高损失事故和恢复上下文的最小工件。
- Ross Anderson, Security Engineering；Saltzer & Schroeder；Threat Modeling Manifesto。
- NIST SSDF SP 800-218、NIST Privacy Framework、NIST AI RMF Generative AI Profile。
- OWASP SAMM、ASVS、Cheat Sheets、Secrets Management、Top 10 for LLM Applications 2025。
- OpenAI Data Controls、Safety Best Practices。
- SLSA、CycloneDX、Go govulncheck、GitHub Secret Scanning / CodeQL / Dependabot / Artifact Attestations。

## 需要人的判断

建议默认：所有生产服务和用户可见 AI workflow 必须有 `security/threat-models/<service>.md`、`security/privacy/<service>.json`、`security/supply-chain/<service>.json`、`security/secrets/<service>.md`；没有四个工件不得进入生产。
