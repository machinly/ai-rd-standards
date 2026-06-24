# Design

## 工件形态

每个生产 target 使用轻量 trust artifacts：

- `trust/commitment-register/<target>.json`
- `trust/policy-surfaces/<target>.md`
- `trust/ai-disclosure/<target>.md`
- `trust/data-rights/<target>.md`
- `trust/compliance-review/<target>.md`

JSON 记录机器可检查的 claims、evidence、policy dependencies、supplier dependencies 和人审点。Markdown 记录用户可见政策面、AI 透明度、数据权利 runbook 和复盘结论。工件不得保存真实用户数据、secret、完整 raw prompt、完整 raw response、合同原文或不必要个人信息。

## 验证策略

`trust-policy-compliance-guard` 提供 `verify_trust_policy.py`：

- 检查 commitment register 必填字段、claim shape、claim 类型、证据引用、状态和 human checkpoints。
- 标记强承诺词：guaranteed、always、accurate、secure、private、not used for training、human reviewed 等，要求证据和人审。
- 检查 policy surfaces 必要章节、Privacy/Terms/AUP/AI disclosure/security/billing/data rights 入口。
- 检查 AI disclosure 说明 AI 使用位置、能力、限制、人审、用户控制、数据发送、安全处理和 feedback/appeal。
- 检查 data rights runbook 覆盖删除、导出、更正、opt-out/consent、processor handling、exceptions 和 audit trail。
- 检查 compliance review 覆盖 claim/data/provider/policy/user rights 变化和 next one change。

## 裁剪原则

- pre-revenue 可以从短政策页面和 claim register 开始；有真实用户或付费用户后必须补数据权利和合规复盘。
- verifier 不判断法律合规是否充分，只检查承诺是否有证据、政策是否可找到、数据权利是否有流程、AI 限制是否说明。
- 法律文本、DPA/BAA、行业合规和监管义务一律作为 human checkpoint，不由 Codex 默认承诺。
