# Design

## 工件形态

每个生产 target 使用轻量 support artifacts：

- `support/intake/<target>.json`
- `support/playbooks/<target>.md`
- `support/templates/<target>.md`
- `support/feedback-ledger/<target>.jsonl`
- `support/reviews/<target>.md`

JSON 记录机器可检查的入口、分类、SLO-like 响应目标、数据处理和人审点。Markdown 记录 playbook、回复模板和定期 review。JSONL 记录脱敏后的支持反馈事实。工件不得保存真实邮箱、电话、姓名、支付信息、secret、完整 raw prompt、完整 raw response 或不必要个人数据。

## 验证策略

`customer-support-trust-ops-guard` 提供 `verify_support_trust_ops.py`：

- 检查 intake 的 channels、categories、severity、first response targets、data handling、routing、metrics 和 human checkpoints。
- 检查 playbook 必要章节和 AI/billing/privacy/incident 升级语义。
- 检查 response templates 必要章节和过度承诺风险。
- 检查 feedback ledger JSONL 字段、脱敏标记、linked artifact 和敏感内容泄漏。
- 检查 support review 的 queue health、top contact drivers、root cause fixes、AI trust/safety 和 next one change。

## 裁剪原则

- pre-revenue 可以只有邮件或表单入口；有付费用户后必须记录响应目标、计费/权益处理和事故沟通模板。
- verifier 不判断客服话术是否完美，只检查是否可分流、可升级、可脱敏、可连接研发。
- 早期不需要 chatbot 或 automation；先让重复联系原因进入产品、文档、eval 或 runbook 修复。
- AI 支持助手只能辅助分类和草拟回复；退款、法律、数据删除、权限、事故恢复时间等高风险动作必须人工确认。
