# commercial-contract-obligation-standard Specification

## Purpose

Define the minimum artifacts and review gates that keep customer contracts, order forms, SLAs, service credits, redlines, and public commercial commitments aligned with one-person-company engineering capacity.

## Requirements

### Requirement: 客户合同和商业承诺必须具备 commercial-contracts 工件

任何生产 target 只要在合同、订单、报价、SOW、SLA、支持政策、DPA、安全页面、定价页、销售材料、客服模板或客户控制台中形成客户可依赖的承诺，MUST 具备 commercial-contracts artifacts。

#### Scenario: 新增客户承诺

- GIVEN 一个 target 会对客户承诺产品、支持、SLA、数据、AI、安全、计费、续费、取消、交付或合规边界
- WHEN 创建研发 OpenSpec change
- THEN 创建 `commercial-contracts/obligation-register/<target>.json`
- AND 创建 `commercial-contracts/agreement-map/<target>.md`
- AND 创建 `commercial-contracts/sla-service-credit/<target>.json`
- AND 创建 `commercial-contracts/redline-playbook/<target>.md`
- AND 创建 `commercial-contracts/contract-review/<target>.md`
- AND 在 OpenSpec proposal 或 design 中链接 commercial-contracts artifacts

### Requirement: Obligation register 必须记录承诺、来源、证据、owner、度量、例外和风险

Obligation register MUST 记录 target、owner、contract surfaces、obligations、dependencies、human checkpoint、review cadence 和状态。

#### Scenario: 登记合同义务

- GIVEN 一个 target 有合同、订单、官网或销售承诺
- WHEN 创建 `commercial-contracts/obligation-register/<target>.json`
- THEN 每个 obligation 包含 id、customer_segment、source_doc、clause_ref、obligation_type、commitment_text、engineering_evidence_ref、owner、due_or_window、measurement、exception_or_exclusion、operational_runbook_ref、risk_level、status
- AND high-risk obligations require explicit human checkpoint
- AND customer-specific exceptions link to product, entitlement, config, runbook, vendor, evidence, or billing artifacts

### Requirement: Agreement map 必须连接标准合同、订单、链接政策、DPA、安全、SLA、权益和例外条款

Agreement map MUST show where commitments live and how they map to product and operational facts.

#### Scenario: 审查协议表面

- GIVEN 一个 target 有标准条款、订单、DPA、安全页面、子处理方页面、SLA、支持政策、定价页或官网 claim
- WHEN 创建 `commercial-contracts/agreement-map/<target>.md`
- THEN it includes Scope, Standard Forms, Order Forms, Linked Policies, DPA / Security / Subprocessors, SLA / Support, Product / Entitlement Mapping, Non-Standard Terms, Renewal / Cancellation, Evidence Links, and Review Cadence
- AND no customer commitment exists only in chat, email, memory, or a ticket without an evidence link

### Requirement: SLA 和服务积分必须建立在 SLO、观测、runbook、依赖例外、事故沟通和计费证据上

SLA/service-credit artifacts MUST separate internal SLOs from customer-facing SLAs and commercial remedies.

#### Scenario: 创建 SLA 或服务积分

- GIVEN 一个 target plans to offer availability, support response, incident communication, service credits, or auto-refund commitments
- WHEN 创建 `commercial-contracts/sla-service-credit/<target>.json`
- THEN it records target、owner、customer_segments、slis、slos、sla_terms、credits、exclusions、measurement_window、dependencies、observability、incident_communication、human_checkpoint、status
- AND any `sla_terms` require SLI/SLO, dashboard, alert, runbook, dependency exclusions, and incident communication evidence
- AND any service credit requires billing-ledger or credit-note evidence
- AND 99.9%+ availability, 24/7, P1/P2 response, automatic refund, or strict liability language requires human checkpoint

### Requirement: Redline playbook 必须定义可接受范围、需人审范围、walk-away、fallback、证据和法律审阅触发器

Redline playbook MUST prevent ad hoc promises that exceed system, vendor, cash, insurance, or founder-capacity limits.

#### Scenario: 客户提出非标准条款

- GIVEN a customer requests non-standard contract, DPA, security, support, SLA, AI, data, billing, indemnity, audit, or SOW terms
- WHEN 更新 `commercial-contracts/redline-playbook/<target>.md`
- THEN it includes Scope, Standard Position, Acceptable Without Review, Needs Human Review, Walk-Away Terms, Fallback Language, Evidence Required, Legal Review Triggers, Negotiation Notes, and Review Cadence
- AND accepted non-standard terms are copied into obligation register and agreement map

### Requirement: Contract review 必须复盘客户订单、义务变化、SLA、数据/AI/安全、计费、红线、事故和开放风险

Contract review MUST keep commercial commitments aligned with production capability.

#### Scenario: 合同或承诺变化前复盘

- GIVEN a new customer, changed order form, pricing page update, support/SLA change, DPA/security change, AI commitment, provider-term change, incident, breach, or high-risk redline
- WHEN 做上线、签署或发送前审查
- THEN `commercial-contracts/contract-review/<target>.md` records Recent Changes, New Customers / Order Forms, Obligation Changes, SLA / Support Commitments, Data / AI / Security Terms, Billing / Renewal Terms, Redlines / Exceptions, Incidents / Breaches, Open Risks, One Next Change, and Review Cadence
- AND unresolved high-risk obligations block release or require explicit human checkpoint
