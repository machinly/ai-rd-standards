# dev-workspace-automation-standard 规格

## Purpose

定义一人公司生产 target 的开发环境、命令自动化、本地依赖、seed/fixtures 和本地验证规则，让 Go/Kratos/sqlc/gRPC、Vite 和 AI workflow 能被人和 Codex 稳定复现。

## Requirements

### Requirement: 生产 target 必须定义开发工作区工件

生产服务、前端应用或用户可见 AI workflow MUST 在进入研发前具备 dev workspace artifacts。

#### Scenario: 新生产 target 进入研发

- GIVEN 一个 target 会长期维护或进入生产
- WHEN 创建 OpenSpec change
- THEN 创建 `dev-workspace/workspace-map/<target>.json`
- AND 创建 `dev-workspace/command-catalog/<target>.md`
- AND 创建 `dev-workspace/local-environment/<target>.md`
- AND 创建 `dev-workspace/seed-fixtures/<target>.md`
- AND 创建 `dev-workspace/verification/<target>.json`
- AND 在 OpenSpec design 或 tasks 中链接 dev workspace artifacts

### Requirement: Workspace map 必须定义工具链、入口、服务和生成物

Workspace map MUST 记录 target、owner、stack、toolchains、package managers、entrypoints、command runner、local services、env files、generated artifacts、seed fixtures、verification、人审点和复审节奏。

#### Scenario: 创建 workspace map

- GIVEN 一个 target 需要本地开发
- WHEN 创建 `dev-workspace/workspace-map/<target>.json`
- THEN 文件包含 `target`、`owner`、`stack`、`toolchains`、`package_managers`、`entrypoints`、`command_runner`、`local_services`、`env_files`、`generated_artifacts`、`seed_fixtures`、`verification`、`human_checkpoint`、`review_cadence`
- AND toolchains 记录 name、version_source、install_check、required
- AND entrypoints 记录 name、path、kind、run_command

### Requirement: Command catalog 必须提供黄金路径命令

Command catalog MUST 以人可读方式记录 setup、generate、develop、test、verify、run local、reset、debug、release prep 和 Codex handoff。

#### Scenario: 创建 command catalog

- GIVEN 一个 target 需要本地命令入口
- WHEN 创建 `dev-workspace/command-catalog/<target>.md`
- THEN 文档包含 Setup、Generate、Develop、Test、Verify、Run Local、Reset、Debug、Release Prep、Codex Handoff
- AND 至少包含一个 one-step local verify 命令

### Requirement: Local environment 必须记录工具链、服务、端口、环境变量和 reset

Local environment document MUST 记录 scope、toolchains、environment files、local services、ports、seed data、secrets policy、reset procedure 和 troubleshooting。

#### Scenario: 创建 local environment

- GIVEN 一个 target 有本地依赖或环境变量
- WHEN 创建 `dev-workspace/local-environment/<target>.md`
- THEN 文档包含 Scope、Toolchains、Environment Files、Local Services、Ports、Seed Data、Secrets Policy、Reset Procedure、Troubleshooting
- AND 不包含真实 secret、真实用户数据或生产凭据

### Requirement: Seed fixtures 必须可重建且不含真实用户数据

Seed fixtures document MUST 记录 scope、datasets、creation command、reset command、AI fixtures、privacy limits、determinism 和 refresh cadence。

#### Scenario: 创建 seed fixtures

- GIVEN 一个 target 需要本地数据或 AI fixtures
- WHEN 创建 `dev-workspace/seed-fixtures/<target>.md`
- THEN 文档包含 Scope、Datasets、Creation Command、Reset Command、AI Fixtures、Privacy Limits、Determinism、Refresh Cadence
- AND seed/fixtures 可重跑且不依赖真实用户数据

### Requirement: Verification plan 必须映射本地快速验证和 CI

Verification plan MUST 记录 one-step commands、smoke checks、generated checks、data checks、frontend checks、AI checks、CI mapping 和 human checkpoints。

#### Scenario: 创建 verification plan

- GIVEN 一个 target 有本地开发黄金路径
- WHEN 创建 `dev-workspace/verification/<target>.json`
- THEN 文件包含 `target`、`owner`、`one_step_commands`、`smoke_checks`、`generated_checks`、`data_checks`、`frontend_checks`、`ai_checks`、`ci_mapping`、`human_checkpoint`
- AND one_step_commands 至少包含一条 verify 或等价命令

### Requirement: 真实外部副作用和破坏性本地命令必须人工 checkpoint

调用真实供应商、真实模型、真实生产数据、破坏性 reset/migration/backfill/tool commit、新长期工具链或 AI agent 副作用命令 MUST 有人工 checkpoint。

#### Scenario: 暴露高风险本地命令

- GIVEN 本地命令会触发真实外部副作用或破坏性动作
- WHEN 准备合并 dev workspace artifacts
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND command catalog 记录风险、dry-run、安全替代命令和 rollback/reset 方法
