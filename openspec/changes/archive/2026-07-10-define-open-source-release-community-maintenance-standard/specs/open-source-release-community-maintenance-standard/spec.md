# open-source-release-community-maintenance-standard Specification

## ADDED Requirements

### Requirement: 公开或接受外部贡献的仓库必须具备 open-source 工件

任何生产 target 只要公开仓库、分发开源包、接受外部 issue/PR/security report，MUST 具备 open-source artifacts。

#### Scenario: 发布公开仓库或开源 package

- GIVEN 一个 target 公开 GitHub/GitLab 仓库、SDK、CLI、template、example、MCP server、connector、eval harness、Go module、npm package 或 Docker image
- WHEN 创建研发 OpenSpec change
- THEN 创建 `open-source/project-register/<target>.json`
- AND 创建 `open-source/community-health/<target>.json`
- AND 创建 `open-source/contribution-policy/<target>.md`
- AND 创建 `open-source/maintainer-runbook/<target>.md`
- AND 创建 `open-source/release-security-review/<target>.md`
- AND 在 OpenSpec proposal 或 design 中链接 open-source artifacts

### Requirement: Project register 必须定义仓库、包、许可证、公开范围、支持边界、安全策略和贡献模型

Project register MUST make public repository scope and maintenance boundaries explicit.

#### Scenario: 登记开源项目

- GIVEN 一个 target 有公开或准备公开的仓库
- WHEN 创建 `open-source/project-register/<target>.json`
- THEN it records target、owner、repositories、packages、license_policy、public_scope、support_boundary、security_policy、contribution_model、linked_artifacts、human_checkpoint、review_cadence、status
- AND each repository records id、name、url_or_path、visibility、purpose、license_expression、default_branch、release_channels、package_artifacts、community_health_ref、security_ref、owner、status

### Requirement: Community health 必须覆盖 README、LICENSE、CONTRIBUTING、CODE_OF_CONDUCT、SECURITY、SUPPORT 和 issue/PR 模板

Community health artifacts MUST define how users and contributors interact with the project.

#### Scenario: 创建社区健康入口

- GIVEN 一个 target has public active repositories
- WHEN 创建 `open-source/community-health/<target>.json`
- THEN it records target、owner、files、templates、code_of_conduct、support、security、contributing、issue_pr_templates、governance、linked_artifacts、human_checkpoint、review_cadence、status
- AND public active repositories include README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, SUPPORT, ISSUE_TEMPLATE, and PULL_REQUEST_TEMPLATE status

### Requirement: Contribution policy 必须定义贡献类型、issue/PR 模板、review、测试、DCO/CLA、license/provenance、安全报告和 AI 生成贡献

Contribution policy MUST reduce maintainer attention cost and clarify rights and safety requirements for external contributions.

#### Scenario: 接受外部贡献

- GIVEN a public repository accepts issues, discussions, pull requests, examples, docs, code, prompts, data, or AI workflow changes
- WHEN 创建 `open-source/contribution-policy/<target>.md`
- THEN it includes Scope, Contribution Types, Triage Labels, Issue Templates, Pull Request Requirements, Review Policy, Tests / CI, DCO / CLA, License / Provenance, Security Reports, AI Generated Contributions, Maintainer Boundaries, and Review Cadence
- AND non-trivial external contributions have a DCO, CLA, or equivalent contribution rights mechanism

### Requirement: Maintainer runbook 必须定义支持边界、issue 分流、PR review、版本发布、行为准则、拒绝/关闭、自动化、暂停/归档和升级

Maintainer runbook MUST protect solo-founder attention and define when maintainers can say no.

#### Scenario: 维护公开仓库

- GIVEN an open source target receives issue, PR, support, conduct, or release work
- WHEN 创建 `open-source/maintainer-runbook/<target>.md`
- THEN it includes Scope, Support Boundary, Issue Triage, Pull Request Review, Release / Versioning, Community Conduct, Saying No / Closing, Automation, Pause / Archive Criteria, Escalation, Linked Artifacts, and Review Cadence
- AND the runbook separates community issue handling from customer support, security reports, and production incidents

### Requirement: Release/security review 必须覆盖版本、支持版本、发布产物、license/notice、漏洞检查、advisory、provenance/SBOM/signing 和 API/SDK 兼容性

Release/security review MUST make public package release safe enough for downstream users.

#### Scenario: 发布开源版本或安全修复

- GIVEN a target releases public packages, SDKs, CLIs, templates, examples, Docker images, or security fixes
- WHEN 创建 `open-source/release-security-review/<target>.md`
- THEN it includes Scope, Recent Releases, Supported Versions, Release Artifacts, License / Notice, Dependency / Vulnerability Checks, Security Reporting / Advisories, Provenance / Signing / SBOM, API / SDK Compatibility, Open Risks, One Next Change, and Review Cadence
- AND official SDKs/packages link compatibility, developer changelog, license/notice, and security advisory evidence where applicable
