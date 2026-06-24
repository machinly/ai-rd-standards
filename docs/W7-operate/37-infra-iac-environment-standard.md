# 阶段 37：基础设施即代码、环境拓扑与云资源治理规范

## 目标

一人公司的基础设施常常从“控制台点一下”开始，最后变成最难恢复的生产状态：资源不知道谁创建、环境差异靠记忆、Terraform state 含敏感信息、手工 hotfix 没回写代码、preview/staging/production 不一致、销毁资源时误删数据、成本和安全暴露没人看。第 37 阶段定义基础设施即代码、环境拓扑与云资源治理规范，让每个生产 target 能回答：有哪些环境，哪些资源由 IaC 管，state 在哪里，谁能 apply，如何预览变更，如何处理手工变更和 drift，如何销毁或恢复，哪些地方必须人工判断。

默认原则：基础设施的期望状态进入版本控制，真实状态通过 state/backend 和云 API 校验，控制台手工变更只能是有记录的例外。对一人公司来说，先把环境地图、资源清单、变更策略、执行 runbook、漂移复盘做实，比追求复杂平台更重要。

## 核心依据

- 《人月神话》：复杂度不会因为工具消失；IaC 的价值是让环境和资源的概念模型保持完整，而不是把控制台操作换成脚本。
- 小型项目管理：一人公司不能维护重型平台团队；先保留 environment map、resource inventory、IaC change policy、provisioning runbook、drift review 五个可执行工件。
- Infrastructure as Code / Kief Morris：基础设施应像软件一样版本化、测试、审查、可重复创建和演进；重点是实践和反馈，不是某个工具。
- Google SRE Configuration Design / Specifics：生产配置和基础设施变更需要可理解、可验证、可回滚，减少配置 toil 和大范围误操作。
- Google SRE Release Engineering / Canarying：基础设施变更也应小批量、可重复、可回滚，并用真实信号确认是否继续。
- AWS Well-Architected Operational Excellence：云环境可以把应用、基础设施、配置和操作流程都作为代码管理，降低人工错误并提高一致性。
- Terraform / OpenTofu：state 是 IaC 与真实资源之间的映射，plan/apply/state/backend 是核心边界；state/plan 可能包含敏感值，必须保护访问和存储。
- Kubernetes Declarative Management：声明式对象配置支持 diff/apply，但 live object 与文件可能产生差异，需要明确配置来源和漂移处理。
- Twelve-Factor App：使用声明式格式做 setup automation，分离 build/release/run，保持 dev/prod parity，把 backing services 当作附加资源。
- DORA / Accelerate：版本控制、自动化部署、小批量变更、快速恢复和可观测反馈是高绩效交付能力，基础设施变更同样适用。

## 范围

适用对象：

- 云账号/项目、环境、region、network、DNS、TLS、load balancer、container runtime、serverless、database、queue、object storage、cache、secret manager、observability backend、CI/CD identity、AI provider integration、vector store、backup storage。
- Terraform、OpenTofu、CloudFormation、CDK、Pulumi、Kubernetes YAML/Kustomize/Helm、Vercel project/env、provider CLI 生成但已固化的配置。
- Go/Kratos/sqlc/gRPC 服务、Vite 前端、AI worker、RAG ingestion、webhook endpoint、admin/support 工具依赖的运行环境。
- preview、dev、staging、production、break-glass、disaster recovery、customer-dedicated 或 demo 环境。

不适用对象：

- 已由阶段 6 管理的应用发布流水线细节；本阶段关注云资源、环境和 state。
- 已由阶段 14 管理的应用 runtime config/feature flag 细节；本阶段关注基础设施层配置与环境拓扑。
- 企业级平台工程、复杂 GitOps、多云抽象平台、Kubernetes operator 开发、组织级云治理；需要时单独开架构 change。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
infra/
  environment-map/<target>.json
  resource-inventory/<target>.json
  iac-change-policy/<target>.md
  provisioning-runbook/<target>.md
  drift-review/<target>.md
```

### `infra/environment-map/<target>.json`

环境地图必须包含：

- `target`
- `owner`
- `environments`
- `accounts_or_projects`
- `regions`
- `network_boundaries`
- `state_backends`
- `deployment_links`
- `data_classification`
- `parity_policy`
- `human_checkpoint`
- `review_cadence`

`environments` 每项至少包含：

- `id`
- `purpose`
- `criticality`
- `cloud_account_or_project`
- `region`
- `runtime`
- `managed_by`
- `state_ref`
- `deploy_pipeline`
- `secrets_boundary`
- `data_classification`
- `public_exposure`
- `status`

默认：

- production、staging/preview、dev/local 的差异必须显式写出；不能只说“差不多”。
- production 和 staging 至少共享同类 runtime、数据库类型、migration 路径、deploy path 和 secrets 管理方式；差异必须有原因。
- 环境、云账号、region、network、state backend、secret boundary 不明确时，不得执行高风险 apply。

### `infra/resource-inventory/<target>.json`

资源清单必须包含：

- `target`
- `owner`
- `resources`
- `modules`
- `dependencies`
- `tags`
- `cost_allocation`
- `backup_restore_links`
- `observability_links`
- `security_boundaries`
- `human_checkpoint`
- `status`

`resources` 每项至少包含：

- `id`
- `type`
- `environment`
- `provider`
- `module_ref`
- `state_address`
- `owner`
- `criticality`
- `data_classification`
- `public_exposure`
- `backup_required`
- `cost_center`
- `status`

默认：

- 生产数据库、队列、对象存储、secret manager、CI deploy identity、外网入口、DNS/TLS、AI/RAG 相关存储必须进入 resource inventory。
- 任何 `public_exposure=true`、`backup_required=true`、`criticality=critical`、`data_classification` 为 `sensitive/restricted/customer_confidential` 的资源都需要更严格 review。
- 未进入 inventory 的生产资源视为 drift 或例外，必须在 drift review 中处理。

### `infra/iac-change-policy/<target>.md`

IaC 变更策略必须包含：

- `Scope`
- `Source Of Truth`
- `State Backend`
- `Plan / Apply Flow`
- `Review Gates`
- `Manual Changes`
- `Secrets / Sensitive State`
- `Rollback / Destroy`
- `Drift Detection`
- `Linked Artifacts`

默认：

- IaC 代码、模块版本、provider 版本、lock file、state backend、plan 输出位置和 apply 权限必须可追踪。
- `plan` 在 apply 前必须被保存或摘要记录；destroy、replace、public exposure、IAM broaden、network exposure、database/storage change 必须人工 checkpoint。
- state/plan 可能包含敏感信息，不得提交到仓库、issue、聊天或普通日志。
- 手工控制台变更必须有原因、时间、操作者、影响、回写代码或回滚计划。

### `infra/provisioning-runbook/<target>.md`

Provisioning runbook 必须包含：

- `Scope`
- `Bootstrap`
- `Plan`
- `Apply`
- `Promotion`
- `State Recovery`
- `Emergency Changes`
- `Destroy / Decommission`
- `Verification`
- `Linked Artifacts`

默认：

- bootstrap 单独记录：state backend、锁、加密、CI/OIDC identity、provider credentials、初始 secret manager。
- apply 默认从 CI 或受控环境执行；本地 apply 只能用于非生产或明确 break-glass。
- destroy/decommission 必须先检查备份、数据导出、DNS/traffic、客户影响、billing、secret rotation 和 evidence。
- emergency change 需要事后回写 IaC、运行 plan、更新 resource inventory 和 drift review。

### `infra/drift-review/<target>.md`

Drift review 必须包含：

- `Recent Changes`
- `Plan Results`
- `Drift Findings`
- `Manual Changes`
- `Cost / Capacity`
- `Security Exposure`
- `State Health`
- `Incidents`
- `Open Risks`
- `Next One Change`

默认节奏：

- pre-revenue：每月一次，或每次生产资源、环境、state backend、网络/IAM/数据库变更后。
- 有付费用户：每两周一次，或每次 apply、事故、成本异常、安全暴露、备份恢复、provider 变更后。
- 每次只选一个最高影响改进：补 inventory、关闭公网暴露、修 drift、加 state lock、加 backup、收紧 IAM、拆环境、补 destroy guard。

## Go / Kratos / sqlc / gRPC 默认规则

- 服务运行环境必须能从 `environment-map` 追到 deploy pipeline、runtime、config boundary、secret boundary、network boundary 和 state backend。
- Go/Kratos 服务的 health、metrics、traces、gRPC health、graceful shutdown 和 config schema 要进入 provisioning verification。
- sqlc/PostgreSQL 相关资源必须标明 migration path、backup policy、restore link、data classification 和 destroy guard。
- gRPC 内部服务 discovery、DNS、TLS/mTLS、service account、network policy 或 equivalent boundary 要进入 resource inventory。
- AI worker、RAG indexer、embedding job、webhook worker、batch/background processor 必须在 inventory 标明队列、存储、成本/容量限制和 shutdown/deploy 边界。

## Vite 前端默认规则

- Vite 前端的 preview、staging、production URL、Vercel/project env、build command、environment variables boundary、DNS/TLS、rollback/promote path 进入 environment map。
- 前端公开环境变量必须与阶段 14 config registry 对齐；不得把 secret 放入 Vite client env。
- UI 管理面板如展示环境/资源状态，使用 Vercel/Geist 风格：表格清晰、状态可扫、危险动作有确认，不用营销文案掩盖生产风险。

## AI workflow 默认规则

- AI provider key、model route、vector store、file store、eval runner、agent sandbox、tool runtime、batch/background processor 依赖的云资源进入 resource inventory。
- AI 成本/容量限制连接阶段 9；model route 连接阶段 30；RAG 资源连接阶段 36；tool runtime 连接阶段 32。
- AI agent 不得自行执行 production IaC apply/destroy、扩大 IAM、打开公网、修改 state backend 或删除资源；最多生成 plan draft 和风险摘要。
- AI 生成的 Terraform/OpenTofu/Kubernetes 配置必须经过 plan、policy、human checkpoint 和 drift review，才能 apply 到生产。

## 需要人判断的关键点

只把这些判断交给人：

- 是否新增云账号/project、production environment、region、network boundary、state backend、Kubernetes cluster 或托管数据库。
- 是否 apply 会 create/replace/destroy production、database/storage/queue、IAM/secret、DNS/TLS、public ingress、backup、billing 或 AI/RAG 关键资源。
- 是否接受手工控制台变更、drift、state 不一致、plan 不完整、provider/模块大版本升级或 state migration。
- 是否允许本地生产 apply、break-glass 变更、destroy/decommission、资源导入 state、force unlock、state rm/mv/import。
- 是否扩大公网暴露、跨环境共享资源、跨租户共享基础设施、降低 backup/retention/encryption、关闭 monitoring/alerts。
- 是否引入独立 Kubernetes/GitOps/vector/cloud 平台、多云抽象或高月费资源。

其他字段完整性、章节、JSON 枚举、required controls、sensitive state 扫描、positive/negative fixture 和 OpenSpec linkage 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“环境是什么、资源有哪些、IaC 怎么变、怎么执行、怎么查漂移”。
- 保留：人只判断新增环境/账号/region、生产 apply/destroy、数据库/IAM/网络/公网暴露、手工变更、state 操作、高成本平台和安全降级。
- 调整：不默认上 Kubernetes、GitOps 或多云平台；先用 Terraform/OpenTofu 或云厂商 IaC，加清晰 state 和 inventory。
- 调整：不要求完美 dev/prod parity，只要求差异显式、能解释、能复现。
- 风险：基础设施工件容易变成过期文档。缓解：drift review 和 verifier 强制把环境、资源、state、pipeline、备份和 observability 链接起来。

结论：可落地。一个人可以先为最关键 production target 写五个文件，把环境和资源从“脑内地图”变成可 review 状态。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：preview/staging/production 差异清楚，减少“测试没问题、生产不同”的发布风险。
- 工程角度：Go/Kratos/sqlc/gRPC、Vite、AI worker 的 runtime、network、secret、state、deploy path 能相互追溯。
- 运维角度：plan/apply、state recovery、drift detection、destroy/decommission 和 emergency change 有 runbook。
- 安全隐私角度：state/plan 敏感、IAM 扩权、公网暴露、跨租户共享、secret boundary 和数据资源销毁都有人审。
- 成本角度：resource inventory 连接 cost allocation、capacity 和高月费资源，避免忘记关闭资源或盲目扩容。

结论：可落地。第 37 阶段把云基础设施从“控制台状态”压成可版本化、可计划、可审查、可恢复的最小治理闭环。
