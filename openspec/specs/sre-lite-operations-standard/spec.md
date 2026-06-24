# sre-lite-operations-standard Specification

## Purpose

定义一人公司生产运维的最小可靠性规范，使服务上线后具备 SLO、可行动告警、runbook、可回滚发布、事故复盘和 toil 收敛能力。

## Requirements

### Requirement: 生产服务必须有最小 SLO artifact

生产服务或关键 workflow MUST 在进入真实用户流程前具备一个可测量的 SLO artifact。

#### Scenario: 新服务上线

- GIVEN 一个服务准备进入生产或真实用户流程
- WHEN 创建运维 artifacts
- THEN 创建 `ops/slo/<service>.json`
- AND 文件包含 `service`、`owner`、`user_journey`、`sli`、`slo_target`、`window`、`error_budget_policy`

#### Scenario: SLO 暂不可测

- GIVEN 关键用户路径已经明确
- WHEN 当前系统还不能计算正式 SLI
- THEN 在 SLO artifact 中记录采集计划
- AND 不把不可测目标声明为已生效 SLO

### Requirement: 告警必须用户可见且可行动

生产 page 告警 MUST 对应用户可见影响、error budget 消耗或即将发生的容量风险，并且具备 runbook。

#### Scenario: 创建 page 告警

- GIVEN 一个告警准备升级为 page
- WHEN 配置 `ops/slo/<service>.json`
- THEN `alerts` 中包含告警名称、类型、触发条件和 runbook
- AND `ops/runbooks/<service>.md` 说明诊断、缓解、回滚和升级路径

#### Scenario: 告警不可行动

- GIVEN 一个告警没有明确人工动作
- WHEN 评审告警
- THEN 将其降级为 ticket、dashboard signal 或删除
- AND 不得作为 page 告警保留

### Requirement: 发布必须可回滚且可观察

生产发布 MUST 在发布前记录测试、迁移、回滚、观测和 smoke test 检查。

#### Scenario: 服务发布

- GIVEN 一个服务准备发布
- WHEN 执行发布 checklist
- THEN 更新 `ops/release/<service>-checklist.md`
- AND 记录测试结果、migration 风险、rollback 或 disable switch、SLO/dashboard 观察点
- AND 发布后执行 smoke test

#### Scenario: 发布消耗 error budget

- GIVEN 发布后关键 SLI 快速恶化
- WHEN error budget policy 被触发
- THEN 优先回滚、关闭 feature flag 或降级
- AND 在 incident 或 release notes 中记录原因和后续行动

### Requirement: 事故必须有轻量记录和行动项

用户可见事故 MUST 记录影响、时间线、根因/触发因素、恢复方式和后续行动项。

#### Scenario: 用户可见事故结束

- GIVEN 一个 SEV1 或 SEV2 事故已缓解
- WHEN 事故结束后复盘
- THEN 创建 `ops/incidents/YYYY-MM-DD-<slug>.md`
- AND 记录 user impact、detection、resolution、timeline、root causes and trigger
- AND 至少一个 action item 包含 owner、due date 和 tracking

#### Scenario: 轻微事故

- GIVEN 一个 SEV3 事故或内部影响事件
- WHEN 不创建完整 postmortem
- THEN 至少在 `ops/incidents/README.md` 或 release notes 中记录摘要、影响和一个后续动作

### Requirement: 运维 toil 必须定期收敛

重复、手动、可自动化且随规模增长的运维工作 MUST 在 SRE-lite review 中被记录并优先处理最高影响项。

#### Scenario: 每周或双周 review

- GIVEN 有生产服务运行
- WHEN 进行 SRE-lite review
- THEN 检查 SLO/error budget、发布失败、告警噪音、事故行动项和重复手工动作
- AND 只选择一个最高影响运维改进入 tasks 或 OpenSpec change

### Requirement: 一人公司值班必须显式升级

24/7 pager 或合同级响应 MUST 由人工显式确认，不得作为默认运维要求。

#### Scenario: 早期服务

- GIVEN 服务没有合同 SLA、付费关键路径或高损失场景
- WHEN 定义响应策略
- THEN 使用营业时间告警、关键黑盒检查和 runbook
- AND 不默认 24/7 pager

#### Scenario: 高关键服务

- GIVEN 服务涉及合同 SLA、资金、权限、隐私、安全或显著收入风险
- WHEN 定义响应策略
- THEN 人工确认响应时间、升级路径、预算和健康边界
- AND 更新 SLO artifact 与 runbook
