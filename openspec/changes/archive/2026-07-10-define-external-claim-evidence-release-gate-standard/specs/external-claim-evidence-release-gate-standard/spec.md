# external-claim-evidence-release-gate-standard Specification

## ADDED Requirements

### Requirement: 对外声明必须具备 claim-control 工件

任何生产 target 只要发布客观、用户可依赖或客户可引用的外部 claim，MUST 具备 claim-control artifacts。

#### Scenario: 发布外部 claim

- GIVEN 一个 target 在 marketing、pricing、docs、developer docs、product UI、contract、support、security、privacy、status、release notes 或 sales surface 发布 claim
- WHEN 创建研发 OpenSpec change
- THEN 创建 `claim-control/surface-inventory/<target>.json`
- AND 创建 `claim-control/claim-evidence-map/<target>.json`
- AND 创建 `claim-control/release-gate/<target>.json`
- AND 创建 `claim-control/correction-runbook/<target>.md`
- AND 创建 `claim-control/claim-review/<target>.md`
- AND 在 OpenSpec proposal 或 design 中链接 claim-control artifacts

### Requirement: Surface inventory 必须定义外部 surface、受众、事实源和扫描策略

Surface inventory MUST make externally visible claim surfaces discoverable and tied to authoritative sources.

#### Scenario: 创建外部声明 surface 清单

- GIVEN 一个 target 有官网、文档、产品 UI、合同、客服、隐私、安全、状态页、release notes 或销售 surface
- WHEN 创建 `claim-control/surface-inventory/<target>.json`
- THEN it records target、owner、surfaces、source_artifacts、claim_sources、scan_policy、human_checkpoint、review_cadence、status
- AND each surface records id、name、surface_type、location、audience、owner、source_of_truth、last_scanned、status

### Requirement: Claim evidence map 必须记录 claim 文本、类型、surface、风险、范围、证据、验证时间、过期和状态

Claim evidence map MUST prove that objective or customer-reliant claims have current evidence before publication.

#### Scenario: 登记和验证 claim

- GIVEN 一个 target has external claims
- WHEN 创建 `claim-control/claim-evidence-map/<target>.json`
- THEN it records target、owner、claims、evidence_sources、substantiation_policy、expiry_policy、human_checkpoint、status
- AND each claim records id、claim_text、claim_type、surface_refs、risk_level、scope、evidence_refs、substantiation_level、last_verified、expires_at、owner、status
- AND unsupported or expired claims are not approved or published

### Requirement: Release gate 必须记录新增、变更、删除 claim 与证据检查和人审决策

Release gate MUST prevent publishing claim changes that exceed evidence, scope, or human approval boundaries.

#### Scenario: 对外 surface 变更前运行 claim gate

- GIVEN a change updates external wording, policy, docs, UI, contract, support template, or release notes
- WHEN 创建 `claim-control/release-gate/<target>.json`
- THEN it records target、owner、change_id、release_or_surface、changed_claims、new_claims、removed_claims、evidence_checks、surface_checks、human_decisions、rollback_or_correction、linked_artifacts、status
- AND high-risk new or changed claims include evidence_ref, human_checkpoint, and decision
- AND approval is blocked when claims have missing owner, missing scope, missing evidence, expired evidence, or unsupported status

### Requirement: Correction runbook 必须覆盖错误 claim 的触发、分流、surface 更新、客户/开发者通知、证据保全和缓解

Correction runbook MUST define how to fix externally visible inaccurate or unsupported claims.

#### Scenario: 发现已发布 claim 错误或证据失效

- GIVEN a published claim becomes inaccurate, unsupported, expired, misleading, or broader than system capability
- WHEN 更新 `claim-control/correction-runbook/<target>.md`
- THEN it includes Scope, Trigger Conditions, Triage, Surfaces To Update, Customer / Developer Notice, Contract / Support Handling, Evidence Preservation, Rollback / Mitigation, Owner And Timeline, and Review Cadence
- AND high-risk corrections require human review before customer, developer, auditor, regulator, or public notice

### Requirement: Claim review 必须复盘 surface 变化、新增/变更 claim、证据缺口、过期、高风险类别、更正和一个下一步

Claim review MUST keep external statements aligned with current product, data, vendor, contract, SRE, and AI evidence.

#### Scenario: 定期或发布前 claim review

- GIVEN a target publishes external claims or modifies customer-facing surfaces
- WHEN 创建或更新 `claim-control/claim-review/<target>.md`
- THEN it records Recent Surface Changes, New / Changed Claims, Evidence Gaps, Expiring Claims, AI / Data / Security Claims, SLA / Contract / Billing Claims, Developer / API Stability Claims, Corrections / Notices, Open Risks, One Next Change, and Review Cadence
- AND one-person review chooses one highest-impact claim, evidence, or correction improvement
