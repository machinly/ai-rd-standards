# 任务

## 1. 来源与约束

- [x] 1.1 查证 NIST Privacy Framework、GDPR Article 5、CCPA。
- [x] 1.2 查证 FTC AI guidance / enforcement、OECD AI Principles。
- [x] 1.3 查证 NIST AI RMF / Generative AI Profile、Google People + AI Guidebook、OpenAI system cards。
- [x] 1.4 查证 OpenAI Usage Policies、Safety Best Practices、Data Processing Addendum。
- [x] 1.5 补充 W2 trust/policy/compliance 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 信任政策合规规范

- [x] 2.1 编写 W2 trust/policy/compliance 规范正文。
- [x] 2.2 定义 commitment register、policy surfaces、AI disclosure、data rights、compliance review artifacts。
- [x] 2.3 定义 Go/Kratos/sqlc/gRPC、Vite、AI workflow 默认规则和人审点。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建 W2 trust/policy/compliance change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `trust-policy-compliance-guard` skill。
- [x] 4.2 添加 trust policy artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 trust policy 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实 target 的 `trust` artifacts，因此不连接真实客户、生产数据、供应商账号或法律系统。

验证说明：本仓库是研发规范仓库，不包含真实产品 target 的 `trust` artifacts，也不应在规范阶段连接真实客户、生产数据、供应商账号、法律系统或合同系统。已通过 `verify_trust_policy.py` 的临时 `assistant-app` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `trust/commitment-register`。
