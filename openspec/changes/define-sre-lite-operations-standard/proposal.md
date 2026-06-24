# 提案：定义 SRE-lite 运维规范

## 意图

为一人公司建立最小生产运维闭环，让服务上线后具备 SLO、告警、runbook、发布回滚和事故复盘能力，同时避免引入需要多人组织才能维护的 SRE 仪式。

## 范围

- 定义 SLO / SLI / error budget policy 的最小 artifact。
- 定义监控、告警、runbook 的默认要求。
- 定义发布前后检查、回滚和 smoke test 要求。
- 定义 incident response 和 postmortem 的轻量流程。
- 定义 toil review 和一人公司运维节奏。
- 创建 SRE-lite 落地 skill 和检查脚本。

## 不做

- 不实现真实部署平台或监控后端。
- 不定义 Kubernetes / Terraform / 云厂商专属架构。
- 不默认 24/7 pager 或完整排班。
- 不承诺通用 SLA 数字；付费关键路径和合同 SLA 需要单独确认。

## 依据

- 《人月神话》：不要把运维工具和自动化当银弹，优先保持概念完整性。
- 小型项目管理：只保留能降低风险和恢复上下文的最小工件。
- Google SRE：SLO、error budget、四个黄金信号、SLO-based alerting、on-call、incident response、postmortem、release engineering、toil。
- DORA：用交付吞吐和不稳定性指标观察发布系统。
- OpenTelemetry：用 vendor-neutral 的 traces、metrics、logs 作为观测数据基础。

## 需要人的判断

默认建议：除非已经有付费关键路径、合同 SLA 或明确收入风险，否则不默认 24/7 pager；先做营业时间告警、关键黑盒检查、runbook、可回滚发布和事故复盘。
