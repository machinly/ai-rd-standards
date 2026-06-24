# maintenance-dependency-debt-standard 规格

## Purpose

定义一人公司生产 target 的依赖清单、更新策略、重大升级计划、技术债登记和弃用计划，确保长期维护风险可见、可验证、可回滚。

## Requirements

### Requirement: 生产 target 必须定义维护治理工件

生产服务、前端应用、AI workflow 或关键 tooling MUST 在发布前具备维护治理 artifacts。

#### Scenario: 新生产 target 进入研发

- GIVEN 一个 target 会进入生产或长期维护
- WHEN 创建 OpenSpec change
- THEN 创建 `maintenance/dependency-inventory/<target>.json`
- AND 创建 `maintenance/update-policy/<target>.md`
- AND 创建 `maintenance/upgrade-plans/<target>.md`
- AND 创建 `maintenance/debt-register/<target>.jsonl`
- AND 创建 `maintenance/deprecation-plans/<target>.md`
- AND 在 OpenSpec design 或 tasks 中链接 maintenance artifacts

### Requirement: Dependency inventory 必须列出依赖网络与维护责任

Dependency inventory MUST 记录 target、owner、stack、package managers、manifests、lockfiles、generated artifacts、critical dependencies、runtime versions、update channels、security scanning、dependency automation、人审点和复审节奏。

#### Scenario: 创建 dependency inventory

- GIVEN 一个 target 需要长期维护
- WHEN 创建 `maintenance/dependency-inventory/<target>.json`
- THEN 文件包含 `target`、`owner`、`stack`、`package_managers`、`manifests`、`lockfiles`、`generated_artifacts`、`critical_dependencies`、`runtime_versions`、`update_channels`、`security_scanning`、`dependency_automation`、`human_checkpoint`、`review_cadence`
- AND critical dependencies 记录 name、ecosystem、role、version source、update policy、risk、upstream source、rollback

### Requirement: Update policy 必须定义节奏、安全响应、验证和回滚

Update policy MUST 以人可读方式记录 scope、supported toolchains、update cadence、security updates、batch strategy、verification gates、rollback 和 human checkpoints。

#### Scenario: 创建 update policy

- GIVEN 一个 target 有外部依赖或工具链
- WHEN 创建 `maintenance/update-policy/<target>.md`
- THEN 文档包含 Scope、Supported Toolchains、Update Cadence、Security Updates、Batch Strategy、Verification Gates、Rollback、Human Checkpoints
- AND policy 区分 security、patch/minor、major/runtime/framework、AI SDK/model/eval 变更

### Requirement: 重大升级必须有升级计划

Major runtime、framework、provider、generated-code、AI behavior 或 breaking dependency update MUST 有 upgrade plan。

#### Scenario: 创建升级计划

- GIVEN 一个 target 需要重大升级
- WHEN 创建 `maintenance/upgrade-plans/<target>.md`
- THEN 文档包含 Scope、Trigger、Compatibility Notes、Steps、Generated Code、Test / Eval Matrix、Release Strategy、Rollback、Decision Log
- AND upgrade plan 链接相关 OpenSpec change、tests/evals、release plan 和 rollback path

### Requirement: 技术债必须登记利息、行动和复审日期

Accepted technical debt MUST 记录为什么接受、未来利息、计划行动、状态和复审日期。

#### Scenario: 记录技术债

- GIVEN 一个 change 引入或发现影响未来修改的债务
- WHEN 写入 `maintenance/debt-register/<target>.jsonl`
- THEN 每行 JSON 包含 `id`、`date`、`target`、`area`、`type`、`source`、`symptom`、`impact`、`interest`、`owner`、`status`、`planned_action`、`review_on`、`linked_change`
- AND status 为 `accepted`、`planned`、`in_progress`、`paid_down`、`closed` 或 `superseded`

### Requirement: 弃用计划必须定义消费者、迁移、观察和删除路径

Deprecated API、config、feature flag、DB field、prompt/model route、webhook、CLI 或 UI route MUST 有 deprecation plan。

#### Scenario: 创建弃用计划

- GIVEN 一个 surface 将被弃用或删除
- WHEN 创建 `maintenance/deprecation-plans/<target>.md`
- THEN 文档包含 Scope、Deprecated Surface、Consumers、Migration Path、Compatibility Window、Observability、Removal Steps、Rollback、Human Checkpoints
- AND 删除动作前有消费者检查和 rollback path

### Requirement: 高风险维护决策必须人工 checkpoint

Runtime/framework/provider major upgrade、真实可达漏洞例外、fork/replace/long pin、breaking contract、deprecation removal、AI behavior contract change 或长期延期债务 MUST 有人工 checkpoint。

#### Scenario: 接受高风险维护决策

- GIVEN 维护变更触发高风险条件
- WHEN 准备合并或发布
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND OpenSpec design 记录取舍、验证证据和回滚方式
