# release-pipeline-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义一人公司生产部署与发布流水线的最小规范，使服务从 OpenSpec change 到 CI gates、不可变 artifact、production deploy、smoke test、SLO 观察和 rollback 都可追踪、可检查、可恢复。

## Requirements

### Requirement: 生产服务必须定义 release pipeline artifact

生产服务或用户可见前端 MUST 在生产部署前具备机器可检查的 release pipeline artifact。

#### Scenario: 新服务准备发布

- GIVEN 一个服务准备部署到 production
- WHEN 定义发布流程
- THEN 创建 `release/pipelines/<service>.json`
- AND 文件包含 `service`、`owner`、`trigger`、`ci`、`environments`、`build`、`gates`、`deploy`、`smoke_test`、`rollback`、`post_deploy_watch`

#### Scenario: 非 GitHub CI

- GIVEN 仓库不使用 GitHub Actions
- WHEN 创建 release pipeline artifact
- THEN `ci.provider` 记录实际 CI provider
- AND `gates` 记录与本规范等价的验证命令或人工步骤

### Requirement: Release 必须分离 build、release、run

生产 release MUST 使用不可变 build artifact 和唯一 release id，不得在 runtime 手工修改代码或配置来替代 release。

#### Scenario: 创建 production release

- GIVEN 一个 production deployment
- WHEN release 被创建
- THEN 记录 release id、commit SHA、artifact digest 或 deployment URL
- AND release log 记录 OpenSpec change id 和 gates 结果

#### Scenario: 需要修改生产行为

- GIVEN 生产行为需要改变
- WHEN 准备修复或配置变更
- THEN 创建新的 release 或明确记录平台配置 release
- AND 不得直接修改 runtime 后声称 release 已完成

### Requirement: CI gates 必须覆盖构建、测试、smoke、回滚和观测

生产发布 MUST 在部署前通过最小 CI gates，并在部署后执行 smoke test 和 SLO 观察。

#### Scenario: 最小 gates

- GIVEN `release/pipelines/<service>.json`
- WHEN 评审 `gates`
- THEN 至少包含 openspec、test、build、smoke、rollback、observability 类 gate
- AND smoke 和 rollback gate 指向可读文件

#### Scenario: Gate 失败

- GIVEN 必需 gate 失败
- WHEN 准备继续发布
- THEN 阻止 production deployment
- OR 在 release log 中记录人工接受风险、原因和回滚计划

### Requirement: 技术栈门禁必须随服务类型启用

Release pipeline MUST 根据服务类型启用 Go/Kratos/sqlc/gRPC、Vite、AI eval 和 SRE-lite 对应门禁。

#### Scenario: Go/Kratos/sqlc/gRPC 服务

- GIVEN 服务包含 Go backend
- WHEN 创建 gates
- THEN 包含 `go test ./...`
- AND 对 sqlc 项目包含 `sqlc vet` 或等价 SQL 检查
- AND 对生产容器包含 build 或 image artifact

#### Scenario: Vite 前端

- GIVEN 服务包含 Vite frontend
- WHEN 创建 gates
- THEN 包含 production build
- AND smoke test 覆盖关键页面或用户路径

#### Scenario: 用户可见 AI 能力

- GIVEN release 影响用户可见 AI 行为
- WHEN 创建 gates
- THEN 包含相关 eval 或明确记录 eval 豁免
- AND release log 记录 prompt/model/schema version

#### Scenario: 生产服务

- GIVEN 服务进入 production
- WHEN 创建 release pipeline
- THEN 关联 `ops/slo/<service>.json`
- AND 关联 `ops/release/<service>-checklist.md`

### Requirement: 部署凭证必须最小权限

生产部署 MUST 使用最小权限凭证，优先短期 OIDC token，不得把 secrets 写入仓库、workflow 明文或 Docker build args。

#### Scenario: GitHub Actions 部署云资源

- GIVEN GitHub Actions 需要部署到云资源
- WHEN 配置 workflow
- THEN 默认 `GITHUB_TOKEN` 使用最小权限
- AND 优先使用 OIDC 获取短期云凭证

#### Scenario: 不能使用 OIDC

- GIVEN provider 不支持 OIDC 或短期凭证
- WHEN 使用长期 secret
- THEN secret 只存在 CI secret store
- AND release pipeline 记录轮换和最小权限策略

### Requirement: Rollback 必须在生产部署前可执行

生产部署 MUST 在发布前具备可执行 rollback 或 disable switch。

#### Scenario: 创建 rollback 文件

- GIVEN 服务准备生产发布
- WHEN 创建 `release/rollback/<service>.md`
- THEN 说明回滚 artifact、migration 处理、feature flag 或 disable switch、回滚后 smoke test、执行入口

#### Scenario: 不可逆 migration

- GIVEN 发布包含不可逆 migration
- WHEN 准备生产部署
- THEN 必须人工 checkpoint
- AND 记录降级、补偿或数据恢复方案

### Requirement: 外部可运行 artifact 必须逐步具备 provenance

发布给外部用户运行的二进制、包或镜像 MUST 记录 provenance / SBOM 策略。

#### Scenario: 外部 artifact

- GIVEN artifact 会被外部用户或客户环境运行
- WHEN 创建 release pipeline
- THEN 记录 artifact digest
- AND 启用或计划启用 artifact attestation、SBOM 或等价供应链证明
