# Proposal: define customer support trust ops standard

## 意图

建立一人公司客户支持、反馈分流与信任运营规范，覆盖支持入口、分类优先级、回复模板、反馈账本、AI 输出投诉、安全隐私升级、事故沟通和定期 root-cause review，避免用户问题散落在聊天记录里并持续打断研发。

## 范围

- 新增 `customer-support-trust-ops-standard` spec。
- 新增 W8 客户支持触发专项文档。
- 创建 `customer-support-trust-ops-guard` skill 和 verifier。
- 补充来源索引与 README。

## 不做什么

- 不引入大型客服平台、呼叫中心流程、客服团队排班或 QA 评分体系。
- 不替代 W7 incident response、W2 security/privacy、W4 billing reconciliation 或 W1 product discovery。
- 不处理正式法律通知、监管问询、合规审计或合同谈判。
- 不连接真实客服系统、真实客户消息、真实邮箱、工单平台或生产数据。

## 依据

- 《人月神话》和小型项目管理。
- The Best Service is No Service 与 The Effortless Experience。
- ITIL 4 Incident Management。
- Google SRE Incident Response / Postmortem Culture。
- Atlassian incident communication。
- Zendesk / Intercom customer support metrics and ticket triage。
- OpenAI Safety Best Practices、Moderation、Safety Checks。
- NIST AI RMF Core / Manage。

## 需要人的判断

只有这些需要人工 checkpoint：公开事故通知/补偿/事后说明、退款/credit/合同承诺、法律/隐私/安全/数据删除请求、AI 输出伤害或滥用、生产用户数据访问/impersonation、24/7 或更短响应承诺、高价值客户例外、把支持反馈提升为产品路线或安全公告。
