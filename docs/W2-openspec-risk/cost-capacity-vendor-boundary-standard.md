# 成本、容量与供应商边界规范
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/main.md 的场景触发规范命中“成本预算、容量、限流、供应商依赖、超支或降级”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/main.md。
## 目标

为一人公司建立最小成本与容量控制闭环：每个生产服务或用户可见 AI workflow 都明确预算、单位成本、限额、降级方式、供应商依赖、退出边界和超支处理。目标不是搭一套企业 FinOps 平台，而是避免三类高损失事故：账单突然失控、过载导致服务雪崩、关键供应商绑定后无法调整。

本阶段默认技术路径：Go/Kratos/gRPC 服务在入口、中间件或 usecase 层做 request/token/tool iteration 限制；AI 能力必须记录 token/request/model 成本驱动；发布前检查预算和供应商边界；SRE-lite runbook 负责超支、限流、降级和恢复。

## 本专项只解决什么

- 成本预算、单位成本、用量驱动和告警阈值的最小仓库工件。
- AI token、请求、工具调用、agent loop 和批处理任务的硬限制。
- 服务容量、rate limit、load shedding、graceful degradation 的默认要求。
- 外部供应商依赖、锁定风险、替代方案和退出计划。
- 超支、限流、供应商故障和容量不足时的一人公司 runbook。
- 成本容量 skill 与本地检查脚本。

不在本阶段展开：完整财务系统、多云迁移平台、复杂采购流程、成本分摊平台、云承诺购买策略、企业级容量预测模型。需要时单独开 OpenSpec change。

## 依据转译

- 《人月神话》：成本与容量工具也不是银弹。真正困难的是把业务价值、系统容量、供应商约束和人的注意力放进同一组小决策。
- 小型项目管理：只让人判断会改变现金流、可用性或供应商锁定的事项；文件命名、阈值小修正和普通告警文案默认由规范处理。
- FinOps Framework：FinOps 是让工程、财务和业务围绕技术花费协作、及时决策和承担责任的操作模型。对一人公司，三件事足够：看见成本、知道单位成本、能对异常采取动作。
- FinOps Planning / Unit Economics：估算应围绕场景和参数；单位指标要连接预算、预测、报告和 guardrails。本专项因此要求每个服务有 `unit_metric` 和 `cost_drivers`。
- Google SRE Handling Overload / Cascading Failures：可靠系统必须知道容量上限，在过载时提前拒绝、降级或减少工作量；降级路径也要被测试，否则真正过载时很可能不可用。
- Google SRE NALSD：容量规划、组件隔离和 graceful degradation 应变成具体资源方案，而不是抽象愿望。
- OpenAI 官方 Rate Limits / Production Best Practices / Cost Optimization / Prompt Caching：OpenAI API 同时受 RPM、TPM、RPD、TPD、模型、项目和月度 usage limit 等限制；生产应用要管理 billing limits；长公共 prompt 可以通过缓存降低成本和延迟；批处理或低优先级任务可考虑 Batch/Flex 等官方成本路径。
- OWASP API4 Unrestricted Resource Consumption：API 若缺少资源限制，会被普通请求或批量请求耗尽 CPU、内存、网络、第三方调用和按次付费资源。
- OWASP API10 Unsafe Consumption of APIs：第三方 API 也必须设 timeout、资源限制和数据校验，不能因为供应商知名就降低边界。
- Twelve-Factor App Backing Services：外部依赖应当作为 attached resources，通过配置连接，尽量做到替换资源不改业务代码。
- AWS Well-Architected Cost Optimization / Google Cloud Costs and Usage：云成本优化的共同核心是看见花费、设置预算/告警、管理用量和资源配额、持续优化。

## 默认决策

- 每个生产服务、付费供应商集成和用户可见 AI workflow 必须有成本预算 artifact。
- 默认不允许无上限 agent loop、无限 tool iteration、无限 batch、无限导出、无限重试。
- 默认每个 AI 能力记录 `ai_max_tokens_per_task`、`ai_max_tool_iterations`、`requests_per_user_per_day` 或等价限制。
- 默认预算阈值至少有 50%、80%、100% 三档：50% 复核趋势，80% 启动降级或人工判断，100% 触发硬限制或明确接受风险。
- 默认先做业务级降级，再做硬失败：缓存、较小模型、排队、降低频率、关闭昂贵非核心 workflow。
- 默认供应商单点依赖可接受，但必须写明原因、替代方案、退出触发条件和迁移成本；不默认多云。
- 默认每月 30 分钟成本复审；只有真实账单、增长或事故证明需要时才增加流程。
- 默认预算上调、取消硬限制、使用预留/承诺购买、引入单点高锁定供应商、允许 AI 执行高成本自主循环，都需要人工 checkpoint。

## Cost artifact 目录规范

推荐落点：

```text
cost/
  budgets/<service>.json
  vendors/<service>.md
  runbooks/<service>.md
  usage/<service>.md
```

`cost/budgets/<service>.json` 是机器可检查的成本与容量事实来源：

```json
{
  "service": "ai-assistant",
  "owner": "founder",
  "currency": "USD",
  "monthly_budget": 200,
  "unit_metric": "cost per successful user task",
  "cost_drivers": ["openai_tokens", "database", "egress"],
  "usage_units": [
    {"name": "openai_tokens", "soft_limit": "6M input+output tokens/month", "hard_limit": "8M input+output tokens/month"},
    {"name": "requests", "soft_limit": "2000/day", "hard_limit": "3000/day"}
  ],
  "alerts": [
    {"threshold_percent": 50, "action": "review trend and top drivers"},
    {"threshold_percent": 80, "action": "enable cheaper model or queue noncritical jobs"},
    {"threshold_percent": 100, "action": "hard cap noncritical workflows"}
  ],
  "limits": {
    "requests_per_user_per_day": 100,
    "ai_max_tokens_per_task": 8000,
    "ai_max_tool_iterations": 5,
    "retry_budget": "3 attempts with exponential backoff"
  },
  "degradation": ["use cached answer", "switch to smaller model", "queue background tasks", "disable expensive workflow"],
  "vendors": [
    {
      "name": "OpenAI",
      "criticality": "high",
      "lock_in": "medium",
      "fallback": "smaller OpenAI model or manual workflow",
      "exit_plan": "cost/vendors/ai-assistant.md"
    }
  ],
  "review_cadence": "monthly",
  "human_checkpoint": {
    "required_for": ["monthly_budget_increase", "no_hard_cap", "single_vendor_no_fallback", "autonomous_agent_loop"]
  }
}
```

`cost/vendors/<service>.md` 最少写：

```markdown
# <service> Vendor Boundary
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/main.md 的场景触发规范命中“成本预算、容量、限流、供应商依赖、超支或降级”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/main.md。
## Vendors

## Critical Paths

## Lock-In Risk

## Fallback

## Exit Plan

## Contract / SLA Notes

## Review Cadence
```

`cost/runbooks/<service>.md` 最少写：

```markdown
# <service> Cost and Capacity Runbook
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/main.md 的场景触发规范命中“成本预算、容量、限流、供应商依赖、超支或降级”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/main.md。
## Signals

## 50 Percent Budget Action

## 80 Percent Budget Action

## 100 Percent Budget Action

## Overload / Rate Limit Action

## Vendor Incident Action

## Rollback / Disable Switch
```

`cost/usage/<service>.md` 可选，但建议在真实上线后记录每月 5 行以内的事实：预算、实际花费、主要驱动、是否触发降级、下月动作。

## 实现顺序

1. 写 OpenSpec：服务或 AI workflow 的用户路径、成本驱动、容量风险、供应商依赖。
2. 写 `cost/budgets/<service>.json`：预算、单位指标、阈值、限制、降级、供应商。
3. 写 `cost/vendors/<service>.md`：关键供应商、锁定风险、替代方案、退出触发条件。
4. 写 `cost/runbooks/<service>.md`：50/80/100% 预算动作、过载动作、供应商故障动作。
5. 在 Go/Kratos/gRPC 中实现入口限流、deadline、retry budget、per-user/per-tenant 限额和 AI tool iteration 上限。
6. 在 AI workflow 中记录模型、token 上限、缓存策略、batch/flex 适用性、降级模型或关闭开关。
7. 在发布门禁中运行成本容量检查；高风险支出或取消硬限制时人工确认。
8. 每月复审一次真实账单和单位成本，只保留一个最高影响优化动作。

## AI 成本与容量规则

- Prompt、工具定义和长公共上下文应把稳定部分放前面，方便利用 prompt caching；不要为了缓存牺牲安全边界或输出质量。
- 每个用户可见 AI workflow 必须有 token/request/tool iteration 上限；agent workflow 还必须有 wall-clock timeout 和 disable switch。
- 成本优化先按风险排序：少调用、少 token、较小模型、缓存、batch/flex、延迟非关键任务；不要先做复杂模型路由平台。
- 如果更高质量模型会显著增加成本或延迟，必须在 OpenSpec design 或 cost budget 中记录取舍。
- OpenAI 价格和模型能力会变化，预算文件只记录内部预算和限制，不把外部价格表硬编码为长期事实。

## 容量与过载规则

- 每个服务至少知道一个容量信号：RPS、queue length、CPU/memory saturation、DB connection、p95 latency、TPM/RPM 或供应商配额。
- 入口层必须有 deadline/timeout；重试必须有上限和 backoff，避免把供应商或自身打爆。
- 过载时优先 fail early、load shedding、queue noncritical work、serve degraded result；不得让昂贵路径无限排队。
- 降级路径必须在 release 或 runbook 中可测试；从未测试过的降级不视为可靠控制。

## 供应商边界规则

- 所有付费或关键外部服务都是 `vendor dependency`，包括 OpenAI、云数据库、对象存储、邮件、支付、监控、搜索、地图和认证。
- 单点供应商不是错误；没有退出计划、没有预算、没有限额才是错误。
- 一人公司不默认多云或自建替代；默认用托管服务换取维护成本下降。
- 当供应商承载核心数据、核心 AI 能力、登录、支付或生产数据库时，必须记录 fallback、exit trigger、迁移数据格式和预估人工成本。

## 只问人的关键判断

默认不问：JSON 字段顺序、阈值说明文字、runbook 小节顺序、低风险供应商描述、普通缓存策略。

必须问：

- 每月预算是否上调，或单服务预算是否超过当前现金流可承受范围。
- 是否允许 100% 阈值后自动停用非核心功能。
- 是否取消硬限制、允许无限重试、无限 batch 或 autonomous agent loop。
- 是否购买云/模型预留容量、承诺消费或更高价格的优先处理。
- 是否接受关键路径单一供应商且没有可运行 fallback。
- 是否把用户数据发送给新的外部供应商或跨境服务。

当前建议默认接受：所有生产服务和用户可见 AI workflow 必须有 `cost/budgets/<service>.json`、`cost/vendors/<service>.md`、`cost/runbooks/<service>.md`；没有预算、没有硬限制、没有降级路径的功能不得进入生产。

## 本专项 Review A：一人公司可落地性

结论：可落地，但要把 FinOps 压成三个文件和一次月度复审。

- 一个人可以维护 budget/vendor/runbook 三类工件，不需要财务、采购、SRE 多角色流程。
- `unit_metric` 和 `cost_drivers` 让成本讨论回到产品价值，而不是只看云账单总额。
- 50/80/100% 阈值足够形成行动，不需要早期引入复杂预测平台。
- 最大摩擦是 AI 成本限制容易被忘记，因此必须由 skill 脚本检查 token/tool/request 限额。
- 下一步应在第一个真实 AI workflow 上用 `cost-capacity-guard` 生成 artifacts。

## 本专项 Review B：产品/工程/运维风险

结论：本专项主要降低现金流失控、容量过载和供应商锁定风险。

- 已把预算、硬限制、降级、供应商退出计划写成生产前置条件。
- 已把 OpenAI rate/usage limits、token 成本、prompt caching、batch/flex 等官方约束转为内部工件，而不硬编码易过期价格。
- 已连接 Google SRE 的 overload/cascading failure 思路：提前拒绝、降低工作量、测试降级路径。
- 已连接 OWASP API4/API10：资源消耗和第三方 API 消费都要设限、超时和校验。
- 仍不强制多云或复杂 FinOps 平台；真实项目可按账单、客户 SLA 和风险逐步升级。


