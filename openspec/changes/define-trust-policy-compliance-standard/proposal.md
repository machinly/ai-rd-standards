# Proposal: define trust policy compliance standard

## 意图

建立一人公司信任政策、用户承诺与合规声明规范，覆盖对外 claim、隐私/条款/可接受使用页面、AI disclosure、数据权利请求、供应商政策依赖和合规复盘，避免营销、政策、客服和真实系统行为不一致。

## 范围

- 新增 `trust-policy-compliance-standard` spec。
- 新增阶段 25 规范文档。
- 创建 `trust-policy-compliance-guard` skill 和 verifier。
- 补充来源索引与 README。

## 不做什么

- 不提供法律意见，不替代律师、隐私专业人士、安全评估、监管申报或合同谈判。
- 不起草正式 DPA、BAA、企业合同、行业合规认证或监管文件。
- 不连接真实客户、生产数据、供应商账号或法律系统。
- 不要求一开始完整 GRC 平台；只建立承诺和证据的最小映射。

## 依据

- 《人月神话》和小型项目管理。
- NIST Privacy Framework、GDPR Article 5、CCPA。
- FTC AI guidance / enforcement。
- OECD AI Principles。
- NIST AI RMF / Generative AI Profile。
- OpenAI Usage Policies、Safety Best Practices、Data Processing Addendum。
- Google People + AI Guidebook。
- OpenAI system card / model card transparency practice。

## 需要人的判断

只有这些需要人工 checkpoint：发布新的隐私/条款/AI disclosure/退款/安全/合规承诺，宣称 AI 专业级或高准确率，处理敏感数据/未成年人/高影响领域，改变数据用途/训练/保留/供应商，接受无法证明的 claim 或实现不一致，触发法律/隐私/安全/客户合同审阅。
