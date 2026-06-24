# 任务

## 1. 来源与约束

- [x] 1.1 查证 NIST SSDF、Privacy Framework、AI RMF Generative AI Profile。
- [x] 1.2 查证 OWASP SAMM、ASVS、Secrets Management、Threat Modeling、LLM Top 10。
- [x] 1.3 查证 OpenAI Data Controls、Safety Best Practices。
- [x] 1.4 查证 SLSA、CycloneDX、Go govulncheck、GitHub security docs。
- [x] 1.5 补充 W2 security/privacy/supply-chain 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 安全隐私供应链规范

- [x] 2.1 编写 W2 security/privacy/supply-chain 规范正文。
- [x] 2.2 定义 `security/threat-models`、`security/privacy`、`security/supply-chain`、`security/secrets` artifacts。
- [x] 2.3 定义 AI 安全、隐私、供应链、secrets、CI 权限和人工 checkpoint 规则。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建 W2 security/privacy/supply-chain change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `security-privacy-supply-chain-guard` skill。
- [x] 4.2 添加 security/privacy/supply-chain artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 security privacy 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实生产服务安全 artifacts，因此不运行真实云供应商或安全平台扫描。

验证说明：本仓库是规范仓库，不包含真实生产服务安全 artifacts，也不应在规范阶段连接真实云供应商或安全平台。已通过 `verify_security_privacy.py` 的临时 `ai-assistant` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `security/threat-models`。
