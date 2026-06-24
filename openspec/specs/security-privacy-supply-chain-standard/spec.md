# security-privacy-supply-chain-standard Specification

## Purpose

定义一人公司安全、隐私与软件供应链的最小基线，使生产服务、付费供应商集成和用户可见 AI workflow 都可威胁建模、可记录数据处理、可追踪依赖与构建来源、可管理 secrets、可触发高风险人工判断。

## Requirements

### Requirement: 生产服务必须定义安全、隐私与供应链基线

生产服务、付费供应商集成或用户可见 AI workflow MUST 在发布前具备安全、隐私与供应链 artifacts。

#### Scenario: 新服务进入生产

- GIVEN 一个服务或 AI workflow 会进入生产
- WHEN 创建 security artifacts
- THEN 创建 `security/threat-models/<service>.md`
- AND 创建 `security/privacy/<service>.json`
- AND 创建 `security/supply-chain/<service>.json`
- AND 创建 `security/secrets/<service>.md`

#### Scenario: 仅本地实验

- GIVEN 一个实验不会访问生产数据、不会处理用户数据、不会调用真实供应商、不会对用户开放
- WHEN 不创建 security artifacts
- THEN 在 OpenSpec tasks 或 design 中记录豁免原因
- AND 不得把该实验作为 production workflow 使用

### Requirement: Threat model 必须覆盖资产、边界、入口、滥用和控制

服务 threat model MUST 记录当前服务的安全范围、资产、信任边界、入口、滥用场景、控制、未决风险和复审节奏。

#### Scenario: 创建 threat model

- GIVEN 一个服务进入生产
- WHEN 创建 `security/threat-models/<service>.md`
- THEN 文档包含 Scope、Assets、Trust Boundaries、Entry Points、Abuse Cases、Controls / Mitigations、Open Risks、Review Cadence

#### Scenario: AI workflow 有私有数据或工具调用

- GIVEN AI workflow 能读取私有数据、调用工具或生成可执行输出
- WHEN 更新 threat model
- THEN 显式覆盖 prompt injection、sensitive information disclosure、insecure output handling、tool misuse
- AND 记录对应控制或说明不适用原因

### Requirement: Privacy record 必须记录数据处理事实

服务 privacy record MUST 记录数据类别、个人/敏感数据、外部处理方、保留、日志、加密、删除/导出、AI 数据使用和人工 checkpoint。

#### Scenario: 创建 privacy record

- GIVEN 服务处理用户数据或 AI prompt/response
- WHEN 创建 `security/privacy/<service>.json`
- THEN 文件包含 `service`、`owner`、`data_classes`、`personal_data`、`sensitive_data`、`processors`、`retention`、`logging`、`encryption`、`deletion_export`、`ai_data_use`、`review_cadence`、`human_checkpoint`

#### Scenario: 发送用户数据给新外部处理方

- GIVEN 新增外部模型、分析、日志、客服或供应商处理用户数据
- WHEN 更新 privacy record
- THEN `processors` 记录 name、purpose、data_sent、retention_note
- AND `human_checkpoint.required_for` 记录 `new_external_processor` 或等价条目

### Requirement: Supply-chain record 必须记录依赖、扫描、构建来源和 CI 权限

服务 supply-chain record MUST 记录语言、包管理器、锁文件、依赖扫描、SAST、secret scanning、SBOM/provenance、CI 权限、更新节奏和人工 checkpoint。

#### Scenario: 创建 supply-chain record

- GIVEN 服务进入生产
- WHEN 创建 `security/supply-chain/<service>.json`
- THEN 文件包含 `service`、`owner`、`languages`、`package_managers`、`lockfiles`、`dependency_scans`、`sast`、`secret_scanning`、`sbom`、`provenance`、`ci_permissions`、`update_cadence`、`human_checkpoint`

#### Scenario: Go 服务

- GIVEN `languages` 包含 Go
- WHEN 定义 dependency scans
- THEN `dependency_scans` 包含 `govulncheck` 或记录明确跳过原因

#### Scenario: Vite/npm 前端

- GIVEN `package_managers` 包含 npm、pnpm 或 yarn
- WHEN 定义 dependency scans
- THEN `dependency_scans` 包含 npm audit、Dependabot、pnpm audit、yarn npm audit 或等价检查

### Requirement: Secrets 必须集中管理并有泄露响应

服务 secrets record MUST 记录 secret 存储、访问、轮换、CI/CD 使用和泄露响应，且不得包含真实 secret。

#### Scenario: 创建 secrets record

- GIVEN 服务需要 API key、数据库凭据、OIDC secret、signing key 或 service token
- WHEN 创建 `security/secrets/<service>.md`
- THEN 文档包含 Storage、Access、Rotation、CI/CD、Incident Response、Review Cadence
- AND 不包含真实 secret、password、token、private key 或 connection string

#### Scenario: 发现 secret 泄露

- GIVEN secret scanning 或人工 review 发现泄露
- WHEN 处理事件
- THEN 立即 revoke/rotate 受影响 secret
- AND 更新 incident/release/security record

### Requirement: 高风险安全隐私供应链例外必须人工 checkpoint

敏感数据、新外部处理方、训练 opt-in、critical/high 漏洞接受、未签名 release、无 SBOM/provenance 客户交付 artifact、新 build secret、AI 高风险工具副作用 MUST 有人工 checkpoint。

#### Scenario: 接受 critical vulnerability

- GIVEN 依赖或代码扫描发现 critical/high 漏洞
- WHEN 准备发布且暂不修复
- THEN `human_checkpoint.required_for` 记录 `critical_vulnerability_accepted` 或等价条目
- AND OpenSpec design 或 release log 记录影响、缓解、补救日期

#### Scenario: AI tool 执行高风险副作用

- GIVEN AI tool 会执行金钱、删除、权限、通知、外部提交或生产写入
- WHEN 准备发布
- THEN threat model 记录 tool misuse
- AND privacy/auth artifacts 记录 actor、tenant、permission 和 human approval 或 dry-run
