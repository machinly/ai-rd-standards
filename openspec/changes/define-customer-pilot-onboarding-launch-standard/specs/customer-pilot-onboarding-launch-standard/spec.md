# customer-pilot-onboarding-launch-standard Specification

## ADDED Requirements

### Requirement: 客户试点或上线必须具备 customer-onboarding 工件

Any external customer pilot, paid pilot, private beta, design partner, or production customer launch MUST have customer onboarding artifacts.

#### Scenario: 创建客户试点或上线 OpenSpec change

- GIVEN a customer-facing pilot, paid pilot, private beta, design partner, or production go-live is planned
- WHEN 创建研发 OpenSpec change
- THEN 创建 `customer-onboarding/pilot-charter/<account>.md`
- AND 创建 `customer-onboarding/tenant-provisioning/<account>.json`
- AND 创建 `customer-onboarding/launch-readiness/<account>.json`
- AND 创建 `customer-onboarding/success-plan/<account>.md`
- AND 创建 `customer-onboarding/handoff-review/<account>.md`
- AND 在 OpenSpec proposal 或 design 中链接 customer-onboarding artifacts

### Requirement: Pilot charter 必须定义成功标准、范围边界、数据边界、AI 边界、集成边界和退出条件

Pilot charter MUST make the pilot measurable and bounded.

#### Scenario: 定义客户试点

- GIVEN a customer pilot or design partner engagement is planned
- WHEN 创建 `customer-onboarding/pilot-charter/<account>.md`
- THEN it includes Scope, Customer Alias, Problem / Outcome, Pilot Type, Success Criteria, In Scope, Out Of Scope, Data Boundary, AI Boundary, Integration Boundary, Timeline / Appetite, Exit Criteria, Human Checkpoints, Linked Artifacts, and Review Cadence
- AND success criteria describe observable customer outcomes or acceptance evidence
- AND exit criteria describe conversion, extension, termination, data cleanup, feature flag removal, and entitlement cleanup as applicable

### Requirement: Tenant provisioning 必须记录租户、身份、角色、entitlement、flag、数据、集成、计费、AI、观测、支持、回滚和审计事实

Tenant provisioning MUST be reproducible without storing secrets or raw customer data.

#### Scenario: 导入或配置客户租户

- GIVEN a customer tenant, workspace, account, or production customer environment is created or changed
- WHEN 创建 `customer-onboarding/tenant-provisioning/<account>.json`
- THEN it records target, owner, customer_alias, environment, tenant_id_ref, identity, roles, entitlements, feature_flags, data_imports, integrations, billing, ai_settings, observability, support_refs, rollback_or_offboarding, audit_refs, human_checkpoint, review_cadence, and status
- AND feature flag entries record key, value, environment, rollout_scope, rollback, owner, and status
- AND integration entries record id, kind, provider, data_boundary, secrets_ref, webhook_or_api_refs, test_plan, and status when integrations exist
- AND data import entries record id, data_classification, source, contract_ref, dry_run_required, and status when data imports exist
- AND artifacts do not contain real customer email addresses, secrets, payment card data, raw prompts/responses, or raw customer data

### Requirement: Launch readiness 必须检查商业、租户、数据、计费、集成、AI、隐私安全、观测、支持、回滚和客户验收 gate

Launch readiness MUST prevent customer exposure when required gates are failed, blocked, or accepted as risk without human approval.

#### Scenario: 外部客户上线 readiness

- GIVEN launch_type is design_partner, private_beta, pilot, paid_pilot, or production
- WHEN 创建 `customer-onboarding/launch-readiness/<account>.json`
- THEN readiness_gates include commercial, auth_tenant, data, billing_entitlement, integrations, ai_eval, security_privacy, observability_slo, support, rollback, and customer_acceptance areas
- AND each gate records id, area, check, evidence_ref, required, result, owner, and status
- AND required gates with result fail, blocked, or accepted_risk require a human checkpoint
- AND production or paid launches include support_plan, communication_plan, rollback_or_exit, and linked_artifacts

### Requirement: Success plan 和 handoff review 必须定义采用信号、风险信号、支持路径、退出路径、决策和一个下一步

Customer success handoff MUST keep customer learning and operations bounded.

#### Scenario: 跟踪客户上线后的价值实现

- GIVEN a customer pilot or launch is active
- WHEN 创建 `customer-onboarding/success-plan/<account>.md`
- THEN it includes Scope, Stakeholders, Activation Milestones, Customer Responsibilities, Product Responsibilities, Training / Docs, Adoption Signals, Risk Signals, Support Path, Expansion / Conversion, Exit / Offboarding, Linked Artifacts, and Review Cadence

#### Scenario: 结束或交接客户上线阶段

- GIVEN a pilot, paid pilot, private beta, or production launch reaches a review point
- WHEN 创建 `customer-onboarding/handoff-review/<account>.md`
- THEN it includes Recent Progress, Success Criteria Result, Adoption / Usage, Reliability / Support, Data / Security / Privacy, AI Quality / Safety, Commercial / Billing, Open Risks, Decision, One Next Change, and Review Cadence
- AND Decision records continue, convert, extend, pause, terminate, human-service fallback, cleanup, or gate follow-up
- AND One Next Change contains one highest-impact next action

### Requirement: 高风险客户上线动作必须保留人工 checkpoint

High-risk customer launch actions MUST be reviewed by the maintainer before exposure.

#### Scenario: 高风险上线动作

- GIVEN artifacts mention production, paid launch, real customer data, SSO, SCIM, billing, production webhook, AI on customer data, RAG, memory, tool action, external connector, SLA, custom feature, public reference, missing rollback, or customer content reuse
- WHEN verifier checks customer-onboarding artifacts
- THEN the artifact records a human checkpoint or Human Checkpoints section
- AND the maintainer decides whether to continue, block, rollback, narrow scope, or ask the customer for explicit approval
