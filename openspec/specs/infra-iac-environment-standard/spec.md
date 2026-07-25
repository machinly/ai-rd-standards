# infra-iac-environment-standard 规格

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

Define the minimum one-person-company governance for infrastructure-as-code, environment topology, cloud resource inventory, state backends, plan/apply, provisioning, manual changes, drift, and decommissioning across Go/Kratos/sqlc/gRPC services, Vite frontends, and AI workflows.

## Requirements

### Requirement: 生产 target 必须定义 infra artifacts

Any production target that depends on cloud accounts/projects, environments, regions, networks, DNS/TLS, runtime platforms, databases, queues, object storage, caches, secret managers, CI/CD identities, observability backends, AI provider resources, vector stores, backup storage, or Kubernetes/cloud resources MUST define infrastructure artifacts.

#### Scenario: 新生产 target 需要可复现基础设施

- GIVEN 一个 target 有生产或类生产基础设施资源
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `infra/environment-map/<target>.json`
- AND 创建 `infra/resource-inventory/<target>.json`
- AND 创建 `infra/iac-change-policy/<target>.md`
- AND 创建 `infra/provisioning-runbook/<target>.md`
- AND 创建 `infra/drift-review/<target>.md`

### Requirement: Environment map 必须定义环境、账号/project、region、网络边界、state backend、部署链接、数据分类、parity 和人工 checkpoint

Environment map MUST record target、owner、environments、accounts/projects、regions、network boundaries、state backends、deployment links、data classification、parity policy、human checkpoint 和 review cadence.

#### Scenario: Reviewer 判断环境拓扑

- GIVEN reviewer 打开 `infra/environment-map/<target>.json`
- WHEN 需要理解 dev/preview/staging/production 环境
- THEN 每个 environment 包含 id、purpose、criticality、cloud_account_or_project、region、runtime、managed_by、state_ref、deploy_pipeline、secrets_boundary、data_classification、public_exposure 和 status
- AND production/staging/dev 差异被显式记录
- AND 高风险 apply 前能找到 state backend、secret boundary、network boundary 和 deploy pipeline

### Requirement: Resource inventory 必须定义资源、模块、依赖、标签、成本、备份恢复、观测、安全边界和人工 checkpoint

Resource inventory MUST record target、owner、resources、modules、dependencies、tags、cost allocation、backup/restore links、observability links、security boundaries、human checkpoint 和 status.

#### Scenario: Reviewer 判断生产资源风险

- GIVEN reviewer 打开 `infra/resource-inventory/<target>.json`
- WHEN 需要理解生产资源
- THEN 每个 resource 包含 id、type、environment、provider、module_ref、state_address、owner、criticality、data_classification、public_exposure、backup_required、cost_center 和 status
- AND 生产数据库、队列、对象存储、secret manager、CI deploy identity、外网入口、DNS/TLS、AI/RAG 存储被列入 inventory
- AND 未进入 inventory 的生产资源被视为 drift 或例外

### Requirement: IaC change policy 必须定义 source of truth、state backend、plan/apply、review gates、manual changes、sensitive state、rollback/destroy、drift detection 和关联工件

IaC change policy MUST record scope、source of truth、state backend、plan/apply flow、review gates、manual changes、secrets/sensitive state、rollback/destroy、drift detection 和 linked artifacts.

#### Scenario: IaC 变更准备 apply

- GIVEN IaC change 会创建、替换、销毁或修改基础设施资源
- WHEN apply 前 review
- THEN plan 输出或摘要被保存到受控位置
- AND state/plan 被视为敏感，不提交到仓库、issue、聊天或普通日志
- AND destroy、replace、public exposure、IAM broaden、network exposure、database/storage change 触发人工 checkpoint

### Requirement: Provisioning runbook 必须定义 bootstrap、plan、apply、promotion、state recovery、emergency changes、destroy/decommission、verification 和关联工件

Provisioning runbook MUST record scope、bootstrap、plan、apply、promotion、state recovery、emergency changes、destroy/decommission、verification 和 linked artifacts.

#### Scenario: Operator 创建、恢复、紧急修改或销毁基础设施

- GIVEN operator 需要 bootstrap、plan、apply、promote、recover state、break-glass、destroy 或 decommission
- WHEN 读取 `infra/provisioning-runbook/<target>.md`
- THEN 能看到 state backend、锁、加密、CI/OIDC identity、provider credentials、apply 环境、state recovery、emergency backport、destroy/decommission 检查和 verification
- AND emergency change 必须回写 IaC、运行 plan、更新 resource inventory 和 drift review

### Requirement: Drift review 必须复盘 recent changes、plan results、drift findings、manual changes、cost/capacity、security exposure、state health、incidents、open risks 和 next one change

Drift review MUST record recent changes、plan results、drift findings、manual changes、cost/capacity、security exposure、state health、incidents、open risks 和 next one change.

#### Scenario: 周期性复查基础设施漂移和状态健康

- GIVEN target 有生产资源、环境、state backend、网络/IAM/数据库变更、事故、成本异常、安全暴露、备份恢复或 provider 变更
- WHEN 更新 `infra/drift-review/<target>.md`
- THEN 记录 plan results、drift findings、manual changes、cost/capacity、security exposure、state health、incidents 和 open risks
- AND 每次只选择一个最高影响的 next one change

### Requirement: 高风险基础设施变更必须人工 checkpoint

New cloud accounts/projects/environments/regions/state backends, production apply/destroy, database/storage/IAM/network/public exposure changes, manual console changes, state operations, backup/encryption/monitoring reductions, cross-environment sharing, and high-cost platform changes MUST have human checkpoint coverage.

#### Scenario: Infra 变更触发高风险条件

- GIVEN environment map、resource inventory、IaC policy、provisioning runbook、drift review 或 release 触发高风险条件
- WHEN 准备 apply、destroy、import、force unlock、state migration、manual change、expose public ingress 或接受 drift
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、阻塞、降级、备份、回滚或专业审阅需求

### Requirement: Infra artifacts 不得保存敏感 state、secret 或凭证

Infra artifacts MUST NOT store Terraform/OpenTofu state or plan contents, production tokens, API keys, OAuth refresh tokens, private keys, session cookies, database connection strings, cloud credentials, kubeconfig credentials, secret values, passwords, payment data, raw AI prompts/responses, unredacted personal data, or customer-confidential payloads.

#### Scenario: 记录 plan、state、resource、credential 或 provider evidence

- GIVEN 需要保存 plan evidence、state evidence、resource evidence、provider error、manual change note、drift finding 或 rollback evidence
- WHEN 写入 `infra/` artifacts
- THEN 使用 redacted summary、state backend id、plan id、resource id、state address、commit、run id、trace id、audit event id、hash、ticket id 或 controlled attachment reference
- AND 不保存 state/plan 全文、生产 token、API key、OAuth refresh token、private key、session cookie、数据库连接串、云凭证、kubeconfig 凭证、secret value、password、支付数据、原始 AI prompt/response、未脱敏个人数据或客户机密 payload
