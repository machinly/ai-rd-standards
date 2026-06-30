# W7 Operate 触发专项：SRE-lite 运维规范 v0.1

## W7 触发定位

本文件是 W7 Operate 的触发型专项，不是 W7 主入口。只有当当前工作涉及 SLO、告警、runbook、incident、postmortem、toil、发布后 watch 或运维复盘时，才需要读取本文件。

普通 W7 运行入口应先回到 `docs/W7-operate/00-main.md`，由主入口判断是否触发本专项。

## 目标

给一人公司定义一条最小但真实可用的生产运维闭环：每个服务或关键 workflow 有一个用户可见 SLO，有能触发行动的告警，有 runbook，有发布回滚检查，有事故记录和轻量复盘。目标不是模仿大公司 SRE 组织，而是让一个人能在有限注意力下守住用户体验、恢复能力和后续学习。

## 本专项只解决什么

- SLO / SLI / error budget policy 的最小仓库工件。
- 监控、告警、runbook、dashboard 和 trace/log/metric 关联的默认边界。
- 一人公司发布前后的安全检查。
- incident response 和 postmortem 的轻量模板。
- 备份/恢复、RPO/RTO、restore drill、业务连续性和供应商故障的最小提醒。
- 环境拓扑、云资源、IaC drift、plan/apply 和 decommission 的最小运行准备。
- toil 识别和每周运维复盘。
- SRE-lite skill 与本地检查脚本。

不在本专项展开：多区域高可用架构、Kubernetes 平台工程、完整 PagerDuty 排班、复杂容量模型、全量 FinOps 平台、SOC2/ISO 合规体系。这些只有在产品收入、用户规模或合同义务出现后，才单独开 OpenSpec change。

## 依据转译

- 《人月神话》：运维平台、监控系统和自动化脚本都不是银弹。可靠性首先来自清晰边界、概念完整性和少量关键决策。
- 小型项目管理：一人公司只保留能降低事故损失和恢复认知上下文的工件，不引入需要多人维护的仪式。
- Google SRE Implementing SLOs：SLO 是可靠性工作的优先级工具，用 error budget 帮助权衡功能交付和可靠性投入。
- Google SRE Monitoring：最小监控优先 latency、traffic、errors、saturation 四个黄金信号。
- Google SRE Alerting on SLOs：告警应围绕用户体验和 error budget 消耗，而不是每个指标都叫醒人。
- Google SRE On-Call：值班必须匹配服务重要性和人的健康；小团队不应默认承担不可持续的 24/7 pager。
- Google SRE Incident Response / Postmortem Culture：事故前定义结构，事故中保留工作记录，事故后用无责复盘推动行动项。
- Google SRE Release Engineering / Canarying Releases：发布要可重复、自动化、小批量、可回滚；高风险变化逐步放量。
- Google SRE Eliminating Toil：重复、手动、随规模线性增长的运维劳动要被记录并逐步自动化。
- DORA：用交付吞吐和不稳定性指标观察发布系统，不把“发得快”和“发得稳”误认为二选一。
- OpenTelemetry：应用要发出 traces、metrics、logs，并避免把数据锁死在单一供应商。

## 默认决策

- 每个生产服务或关键 workflow 默认先写 1 个用户可见 SLO；没有用户路径时，先写最关键后台结果的 freshness 或 correctness SLO。
- 早期用户可见 MVP 默认从 `99.5% monthly availability` 开始讨论；有合同 SLA、付费关键流程或高损失场景时必须人工确认更高目标。
- 默认不做 24/7 值班。除非已有付费用户、合同义务、真实收入风险或外部依赖要求，否则只做营业时间告警和关键黑盒 uptime 检查。
- 告警默认分两类：`page` 只用于用户可见、正在发生、需要立即行动的问题；`ticket` 用于非紧急修复。
- 告警必须指向 runbook；没有 runbook 的告警默认不允许升级为 page。
- 发布默认小批量、可回滚；涉及 schema migration、权限、资金、AI 自动副作用时必须有 rollback 或 disable switch。
- 运维优先使用托管服务和供应商默认能力，避免一开始自建监控平台。

## 运维 artifact 目录规范

推荐落点：

```text
ops/
  slo/<service>.json
  observability/<service>.md
  runbooks/<service>.md
  recovery/<service>.md
  infra/<service>.md
  release/<service>-checklist.md
  incidents/README.md
  incidents/YYYY-MM-DD-<slug>.md
```

`ops/slo/<service>.json` 是机器可检查的事实来源，推荐字段：

```json
{
  "service": "checkout-api",
  "owner": "founder",
  "user_journey": "用户可以创建订单并完成付款",
  "sli": {
    "availability": "successful_checkout_requests / total_checkout_requests",
    "latency": "p95 checkout request latency"
  },
  "slo_target": {
    "availability": "99.5% monthly",
    "latency": "p95 < 1200ms"
  },
  "window": "30d",
  "signals": ["latency", "traffic", "errors", "saturation"],
  "error_budget_policy": "当 7 天 burn rate 超过预算 25% 时，暂停非紧急功能发布并修复最高影响可靠性问题。",
  "alerts": [
    {
      "name": "checkout-error-budget-burn",
      "type": "page",
      "condition": "5xx 或业务失败率持续消耗 error budget",
      "runbook": "ops/runbooks/checkout-api.md"
    }
  ],
  "dashboards": ["checkout overview"],
  "rollback": "回滚服务镜像；必要时关闭 checkout_v2 feature flag"
}
```

一人公司裁剪规则：

- 第一版只允许 1-2 个 SLO，宁可少而能行动。
- `slo_target` 必须能从现有日志、指标或外部 uptime 检查计算；算不出来的目标先不作为正式 SLO。
- `error_budget_policy` 必须写出触发后的动作，例如暂停发布、回滚、增加人工复核或修复最高影响问题。
- `alerts[].type = page` 必须有 `runbook`，并且 runbook 里有诊断、缓解和回滚步骤。

## 监控与观测

每个 Go/Kratos/gRPC 服务至少暴露：

- latency：按 RPC / endpoint 记录成功和失败请求的延迟，优先 p95 或 p99，不只看平均值。
- traffic：请求量、任务量或关键 workflow 次数。
- errors：协议错误、业务失败、依赖失败和 parse / schema 失败。
- saturation：CPU、内存、连接池、队列长度、数据库连接或第三方 rate limit。

OpenTelemetry 是默认数据语义和导出方式；具体 backend 可以是托管云监控、Grafana/Prometheus、供应商 APM 或日志平台。规范只要求服务产生可关联的 traces、metrics、logs，不要求一开始自建全套栈。

AI 能力额外记录：

- `ai_feature`、prompt version、model、schema version。
- eval pass rate 或人工抽检通过率。
- token/cost、tool failure rate、structured output parse failure rate。
- fallback、disable switch 或 rollback 方式。

## 恢复与基础设施提醒

备份、恢复和基础设施不再作为默认独立专项。只有出现真实合同、付费关键数据、生产 IaC apply、跨区域恢复、客户证据或高风险资源销毁时，才单独开 OpenSpec change。普通 W7 运行准备先在本文件留下最小事实：

- `ops/recovery/<service>.md`：关键资产、RPO/RTO、备份来源、restore steps、验证命令、下一次演练日期。
- `ops/infra/<service>.md`：环境、region、runtime、state backend、关键云资源、public exposure、backup_required、drift 处理。
- 生产恢复、PITR、覆盖生产、丢弃数据、destroy/decommission、IAM 扩权、public ingress 和 state 操作仍然必须人审。

## 告警规范

告警必须回答四个问题：

1. 用户是否正在受影响？
2. 是否正在消耗 error budget？
3. 一个人现在能做什么？
4. 是否有 runbook 指向第一步？

默认策略：

- 用户不可见、非紧急、不可立即行动的信号进入 ticket，不 page。
- 低流量服务优先用黑盒探测和端到端 smoke test，避免少量样本造成误报。
- page 告警必须有 `condition`、`impact`、`runbook`、`rollback`。
- 连续两次误报或无法行动的 page，必须降级或修改条件。

## 发布规范

每个服务使用 `ops/release/<service>-checklist.md` 记录发布门禁：

- OpenSpec tasks 已完成或明确延后。
- Go / frontend / AI eval / migration 相关测试已跑。
- 变更可回滚，或有 feature flag / disable switch。
- 迁移前有备份或恢复路径。
- SLO、dashboard、日志字段和告警能观察到发布影响。
- 发布后执行 smoke test，并观察 15-30 分钟关键 SLI。
- 如果触发错误预算快速消耗，先回滚或关闭开关，再排查。

高风险发布默认拆小；有足够流量时使用 canary / progressive rollout。没有流量时，用 staging smoke test、生产只读检查和外部 uptime 检查代替。

## Incident response 与复盘

一人公司事故响应不需要复杂角色，但需要清楚顺序：

1. 宣告事故：写时间、影响、入口和当前假设。
2. 先止血：回滚、关闭 feature flag、降级、限流或切换依赖。
3. 保留工作记录：记录每次关键动作和结果。
4. 对用户或自己未来复盘说明影响。
5. 事故结束后写轻量 postmortem。

事故等级默认：

- SEV1：大量用户不可用、数据损坏、资金/权限/隐私风险、合同 SLA 风险。
- SEV2：核心路径部分失败、明显性能退化、需要当天处理。
- SEV3：小范围影响、内部工具失败、可排入普通修复。

`ops/incidents/YYYY-MM-DD-<slug>.md` 最小结构：

```markdown
# Incident: <title>

- Date:
- Severity:
- Service:
- User impact:
- Detection:
- Resolution:

## Timeline

## Root Causes And Trigger

## What Went Well

## What Went Poorly

## Action Items

| Action | Type | Owner | Due | Tracking |
| --- | --- | --- | --- | --- |
```

复盘规则：

- 不归咎个人，描述系统条件、触发因素和缺失防护。
- 至少一个行动项必须有 owner、due date 和 tracking。
- 行动项最多 3 个；多了就说明范围过大。
- 用户有明显影响时，复盘必须记录可量化影响，即使只能估算。

## Toil 与每周运维复盘

每周或每两周用 30 分钟做一次 SRE-lite review：

- 哪个 SLO 最近最接近预算耗尽？
- 最近一次发布是否造成回滚、hotfix 或用户影响？
- 哪个 page 是误报或不可行动？
- 哪个手动动作重复 2 次以上，应该脚本化或写进 runbook？
- 下周只选一个最高影响运维改进。

toil 判断：

- 手动、重复、可自动化、随服务或用户规模线性增长。
- 只恢复原状，没有永久改善。
- 中断研发注意力，但没有产生产品或可靠性增量。

一人公司目标不是把 toil 压到 0，而是避免它吞掉连续研发时间。默认每周运维改进最多选 1 个，避免可靠性工作反过来失控。

## 只问人的关键判断

默认不问：SLO 文件名、runbook 标题、dashboard 名称、incident 模板小字段、告警 ticket 文案。

必须问：

- 是否承诺合同 SLA 或 24/7 响应。
- 是否愿意用更高云成本换更高可用性。
- 是否允许自动回滚、自动降级或自动关闭用户功能。
- 是否涉及数据删除、资金、权限、隐私、安全事件。
- 是否需要对用户公开事故状态页或事后说明。

当前建议默认接受：除非你明确说某个服务已经有付费关键路径或合同 SLA，否则本规范不默认 24/7 pager，只要求营业时间告警、外部 uptime 检查、runbook 和可回滚发布。

## 本专项 Review A：一人公司可落地性

结论：可落地，但必须把 SRE 压成“少量文件 + 少量信号 + 少量动作”。

- `slo.json + runbook + release checklist + incident README` 足够让一个人在中断后恢复上下文。
- 默认 1-2 个 SLO 避免一开始写一堆无法维护的指标。
- 不默认 24/7 值班，保护一人公司的注意力和健康。
- 最大摩擦是 SLO 数据可能一开始不可得；因此允许先写采集计划，但不能把不可测指标当正式目标。
- 下一步应在第一个真实服务上用 `sre-lite-ops` 生成 `ops/` 工件，并让脚本检查。

## 本专项 Review B：产品/工程/运维风险

结论：主要风险是两个极端：过早平台化，或完全没有恢复机制。

- 规范避免自建平台，优先托管监控和 OpenTelemetry 数据语义。
- 告警必须有 runbook，降低“半夜醒来但不知道做什么”的风险。
- 发布检查把 migration、rollback、smoke test、SLO 观察纳入最低门禁。
- incident 模板要求行动项有 owner/due/tracking，避免复盘变成情绪记录。
- 仍缺真实服务的 dashboard/backend 选择；这应由具体部署环境决定，不在规范阶段提前锁死。
