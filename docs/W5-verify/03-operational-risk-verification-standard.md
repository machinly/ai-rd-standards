# W5 触发专项：性能、容量、韧性与降级验证规范

## W5 触发定位

本文件是 W5 Verify 的触发型专项，不是 W5 主入口。只有当当前验证涉及性能预算、负载画像、benchmark、Web Vitals、DB/AI latency、容量、依赖失败、429/5xx/timeout、重试、dead letter、fallback 或降级 UI 时，才读取本文件。

普通 W5 验证先回到 `docs/W5-verify/00-main.md`。

## 目标

把性能回归和韧性演练合并成一个上线前运行风险门禁：变更是否仍在预算内，关键依赖坏掉时是否能降级、停止、恢复，并把 blast radius 控制在一个人能处理的范围内。

默认原则：没有预算、基线、失败模式、降级证据和 go/no-go 决策，就不要声称性能或韧性可控。

## 主要角色消费者

- QA：决定是否可进入 W6。
- 运维：接收 W7 runbook、SLO 和 watch 需求。
- 后端/前端：修复 timeout、retry、DB、bundle、fallback 和 degraded UI。

## 最小工件

按触发选择：

```text
operational-risk/
  budget/<target>.json
  load-profile/<target>.json
  failure-mode-map/<target>.json
  verification-plan/<target>.md
  run-report/<target>.json
  degradation-check/<target>.md
```

## 必须覆盖

- latency 至少记录 p95 或 p99；不要只看平均值。
- 前端记录 LCP/INP/CLS、bundle、route transition 或关键 API 延迟中适用项。
- DB/worker/AI 记录慢查询、queue depth、provider quota、token、tool iteration、timeout 或 cost 中适用项。
- failure mode 至少覆盖 1-3 个最高影响依赖：latency、timeout、5xx、429、malformed response、queue backlog、AI schema/tool/RAG failure。
- stop conditions 能让一个人知道何时停止验证或演练。
- 降级后用户还能做什么、不能做什么、是否可稍后重试或转人工。

## 默认规则

- 没有基线时不能直接 `pass`；只能 `pass_with_notes`、`needs_fix` 或 `needs-more-tests`。
- 生产压测、真实供应商压测、真实付费 AI 调用、真实客户数据或共享环境验证必须人审。
- 真实 provider 故障演练默认用 mock、recorded response、sandbox 或 staging。
- retry 必须有上限、backoff 和 retry budget；不得无限 spinner、无限队列或无限 agent 自救。
- `accepted_risk`、`defer-release`、`rollback` 或带性能/降级缺口发布必须人审。

## 需要人判断

- 放宽 p95/p99、Core Web Vitals、bundle、token、timeout、SLO、quota 或饱和预算。
- 在 production、共享环境、真实客户流量、真实数据、真实供应商或真实付费 AI provider 上跑 load/stress/fault injection。
- 接受性能回归、未知基线、跳过降级验证、扩大 blast radius 或带 gap 发布。
- 增加显著云资源、数据库索引/缓存/CDN/队列、供应商优先级或模型成本。
- 关闭/弱化 timeout、rate limit、retry budget、circuit breaker、fallback、dead letter 或人工审批。

## Review A：一人可执行性

性能和韧性共享同一个“上线前运行风险”问题，合并后更符合 QA/运维的实际读取路径。一个人可以先为一个核心路径写预算和 1 个失败模式验证，不必搭完整性能或 chaos 平台。

## Review B：产品 / 工程 / 运维风险

保留了预算、负载、基线、stop condition、降级和 accepted risk 门禁。最小安全下一步是让 W6 release checklist 引用本专项的 go/no-go 结论。

