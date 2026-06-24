# configuration-feature-flag-standard Specification

## Purpose

定义一人公司配置、环境、Feature Flag 与运行时变更的最小基线，使生产服务、前端应用和用户可见 AI workflow 的配置事实、环境差异、flag 生命周期、runtime change、rollback、kill switch 和高风险人审点可检查、可回溯、可清理。

## Requirements

### Requirement: 生产目标必须定义配置与运行时变更工件

生产服务、前端应用或用户可见 AI workflow MUST 在生产配置、环境差异、Feature Flag 或运行时行为可变时具备配置 artifacts。

#### Scenario: 新生产 target 有配置或 flag

- GIVEN 一个 target 会进入生产且依赖配置、环境变量、Feature Flag、AI route 或 runtime config
- WHEN 创建 OpenSpec change
- THEN 创建 `config/registry/<target>.json`
- AND 创建 `config/environments/<target>.md`
- AND 创建 `config/flags/<target>.json`
- AND 创建 `config/runbooks/<target>.md`

#### Scenario: 仅本地实验

- GIVEN 一个实验不会进入生产、不会访问生产数据、不会对用户开放
- WHEN 不创建 config artifacts
- THEN 在 OpenSpec tasks 或 design 中记录跳过原因

### Requirement: Config registry 必须记录配置事实、验证和回滚

Config registry MUST 记录 target、owner、stack、environments、config items、secrets policy、validation、startup checks、reload policy、drift detection、人审点和复审节奏。

#### Scenario: 创建 config registry

- GIVEN 一个 target 有生产配置
- WHEN 创建 `config/registry/<target>.json`
- THEN 文件包含 `target`、`owner`、`stack`、`environments`、`config_items`、`secrets_policy`、`validation`、`startup_checks`、`reload_policy`、`drift_detection`、`human_checkpoint`、`review_cadence`

#### Scenario: 定义 config item

- GIVEN registry 包含 config_items
- WHEN 校验 config item
- THEN 每个 item 包含 `key`、`type`、`owner`、`source`、`environments`、`required`、`default`、`validation`、`sensitive`、`client_exposed`、`restart_required`、`rollout`、`rollback`

### Requirement: Secret 值不得进入配置工件

Config artifacts MUST NOT 记录真实 secret、token、password、private key、database URL 或 connection string。

#### Scenario: 敏感配置

- GIVEN config item 的 `sensitive` 为 true
- WHEN 写入 registry
- THEN `default` 不得包含真实值
- AND item 记录 secret source 或引用方式

#### Scenario: Vite client env

- GIVEN config item 的 `client_exposed` 为 true 或 target 是 Vite frontend
- WHEN 写入 registry
- THEN `sensitive` MUST 为 false
- AND key MUST 使用 `VITE_` 前缀或记录显式 `envPrefix` 例外和人审点

### Requirement: Environment matrix 必须记录环境差异和推广路径

Environment matrix MUST 让人理解 local、preview/staging、production 的配置来源、差异、验证、推广和回滚。

#### Scenario: 创建 environment matrix

- GIVEN 一个 target 有多个环境
- WHEN 创建 `config/environments/<target>.md`
- THEN 文档包含 Scope、Environments、Config Sources、Secrets Sources、Differences、Promotion Path、Validation、Rollback、Human Checkpoints

### Requirement: Feature flags 必须记录类型、默认值、错误行为、rollout 和清理计划

Feature Flag record MUST 记录 flag 列表、evaluation context、provider、defaults、cleanup policy、observability、人审点和复审节奏。

#### Scenario: 创建 flags record

- GIVEN 一个 target 有运行时 Feature Flag
- WHEN 创建 `config/flags/<target>.json`
- THEN 文件包含 `target`、`owner`、`flags`、`evaluation_context`、`provider`、`defaults`、`cleanup_policy`、`observability`、`human_checkpoint`、`review_cadence`

#### Scenario: 定义 flag

- GIVEN flags record 包含 flags
- WHEN 校验每个 flag
- THEN 每个 flag 包含 `key`、`type`、`category`、`owner`、`created_on`、`default`、`fail_behavior`、`targeting`、`rollout_plan`、`observability`、`cleanup_plan`
- AND release 或 experiment flag 包含 `expires_on`
- AND ops、permission、kill_switch、migration、ai_model_route flag 包含 `review_on` 或 `expires_on`

### Requirement: Evaluation context 必须最小化个人数据

Feature Flag evaluation context MUST 只包含必要、低敏、低基数字段，且不得包含不必要个人数据。

#### Scenario: 定义 evaluation context

- GIVEN flags record 包含 `evaluation_context`
- WHEN 校验 context 字段
- THEN 不包含 email、phone、full_name、address、raw_ip、payment、token、secret
- OR `human_checkpoint.required_for` 包含 `personal_flag_targeting`

### Requirement: Runtime changes 必须可追溯且可回滚

生产或准生产运行时配置变更 MUST 追加 JSONL 记录，包含环境、key、actor、reason、result 和 rollback。

#### Scenario: 记录 runtime change

- GIVEN 生产配置、Feature Flag、AI route 或 kill switch 被改变
- WHEN 写入 `config/runtime-changes/<target>.jsonl`
- THEN 每行 JSON 包含 `date`、`target`、`environment`、`change_type`、`key`、`actor`、`reason`、`result`、`rollback`
- AND 不包含真实 secret 或个人联系信息

### Requirement: Runbook 必须定义变更、验证、回滚和 kill switch

Config runbook MUST 定义 scope、change procedure、validation、rollback、kill switch、drift detection 和 human checkpoints。

#### Scenario: 创建 config runbook

- GIVEN 一个 target 有生产配置或 flag
- WHEN 创建 `config/runbooks/<target>.md`
- THEN 文档包含 Scope、Change Procedure、Validation、Rollback、Kill Switch、Drift Detection、Human Checkpoints

### Requirement: 高风险配置变更必须人工 checkpoint

生产配置变更、敏感配置新增/迁移、前端 client env 暴露、长期 flag 例外、AI model/provider route、kill switch、跳过 rollback 或 drift detection MUST 有人工 checkpoint。

#### Scenario: AI route flag

- GIVEN flag category 是 `ai_model_route`
- WHEN 准备生产启用
- THEN flags record 记录 fallback、observability 和 cleanup
- AND `human_checkpoint.required_for` 包含 `ai_route_change`
- AND OpenSpec design 链接 AI eval 和成本 guardrail
