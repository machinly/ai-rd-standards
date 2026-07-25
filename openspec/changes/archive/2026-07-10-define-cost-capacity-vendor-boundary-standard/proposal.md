# 提案：定义成本、容量与供应商边界规范

## 意图

为一人公司建立可检查的成本、容量和供应商边界规范，让每个生产服务或用户可见 AI workflow 明确 budget、unit metric、cost drivers、limits、degradation、vendor dependency、exit plan 和 human checkpoint，降低账单失控、过载雪崩和供应商锁定风险。

## 范围

- 定义 cost artifacts 目录和最小文件。
- 定义预算、单位成本、用量驱动、告警阈值和硬限制。
- 定义 AI token/request/tool iteration/agent loop 的成本容量边界。
- 定义 overload、rate limit、load shedding、graceful degradation 的默认要求。
- 定义供应商依赖、锁定风险、fallback、exit plan 和人工 checkpoint。
- 创建成本容量落地 skill 和检查脚本。

## 不做

- 不实现财务系统、云账单导入、采购流程或成本分摊平台。
- 不默认多云或自建供应商替代。
- 不硬编码外部供应商价格表。
- 不定义企业级容量预测模型。

## 依据

- 《人月神话》：成本容量工具不是银弹，复杂度来自业务价值、系统容量、供应商约束和人的注意力。
- 小型项目管理：只让人判断显著现金流、可用性和锁定风险。
- FinOps Framework、Planning & Estimating、Unit Economics。
- Google SRE Handling Overload、Cascading Failures、NALSD。
- OpenAI Rate Limits、Production Best Practices、Cost Optimization、Prompt Caching。
- OWASP API4 Unrestricted Resource Consumption、API10 Unsafe Consumption of APIs。
- Twelve-Factor App Backing Services。
- AWS Well-Architected Cost Optimization、Google Cloud Costs and Usage。

## 需要人的判断

建议默认：所有生产服务和用户可见 AI workflow 必须有 `cost/budgets/<service>.json`、`cost/vendors/<service>.md`、`cost/runbooks/<service>.md`；没有预算、硬限制和降级路径的功能不得进入生产。
