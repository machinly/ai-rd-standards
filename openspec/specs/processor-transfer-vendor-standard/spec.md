# processor-transfer-vendor-standard Specification

## Purpose

Define the minimum one-person-company governance for vendors that process customer data, including processor/service-provider roles, DPA or equivalent contract coverage, subprocessor monitoring, international transfer and data residency impact, AI provider data controls, deletion assistance, breach notice, and vendor review.

## Requirements

### Requirement: 客户数据处理供应商必须具备 vendor-risk 工件

任何生产 target 只要向外部供应商发送客户数据、客户内容、个人数据、提示词、响应、文件、日志、支持材料、RAG 内容、embedding input/output 或生产分析数据，MUST 具备 vendor-risk artifacts。

#### Scenario: 新增客户数据处理供应商

- GIVEN 一个 target 会把客户数据或客户内容交给新供应商处理
- WHEN 创建研发 OpenSpec change
- THEN 创建 `vendor-risk/processor-register/<target>.json`
- AND 创建 `vendor-risk/dpa-checklist/<target>.json`
- AND 创建 `vendor-risk/subprocessor-watch/<target>.md`
- AND 创建 `vendor-risk/transfer-impact/<target>.json`
- AND 创建 `vendor-risk/vendor-review/<target>.md`
- AND 在 OpenSpec proposal 或 design 中链接 vendor-risk artifacts

### Requirement: Processor register 必须定义供应商角色、数据类别、训练/保留和协助义务

Processor register MUST 记录 target、owner、processing activities、critical vendors、data boundaries、linked artifacts、human checkpoint、review cadence 和状态。

#### Scenario: 登记处理活动

- GIVEN 一个供应商会处理 target 的客户数据
- WHEN 创建 `vendor-risk/processor-register/<target>.json`
- THEN 每个 processing activity 包含 id、vendor、product_service、role、purpose、data_classes、personal_data、sensitive_data、customer_content、model_training_allowed、retention_summary、region_or_residency、subprocessor_source、dpa_ref、transfer_ref、security_refs、deletion_assistance、incident_notice、status
- AND role 只能使用 processor、service_provider、contractor、independent_controller、joint_controller 或 no_customer_data
- AND model_training_allowed 默认为 false，任何 true 或 unknown 都需要 human checkpoint

### Requirement: DPA checklist 必须覆盖合同、处理方、子处理方、权利协助、删除、审计、跨境和 AI 条款

DPA checklist MUST 记录 agreements、exceptions、renewal/recheck、human checkpoint 和状态。

#### Scenario: 检查供应商合同

- GIVEN 一个供应商处理个人数据、客户内容、提示词、响应、文件、日志或支持材料
- WHEN 创建 `vendor-risk/dpa-checklist/<target>.json`
- THEN 每个 agreement 包含 vendor、agreement_type、effective_date、scope、controller_processor_roles、documented_instructions、confidentiality、security_measures、subprocessor_authorization、data_subject_assistance、breach_notice、delete_or_return、audit_or_assurance、international_transfer_terms、ccpa_service_provider_terms、ai_training_terms、retention_terms、status
- AND DPA/等价条款缺口必须进入 exceptions
- AND 缺少 DPA、删除协助、事故通知、子处理方透明度、AI training 限制或跨境条款时必须有人审或暂停上线

### Requirement: Subprocessor watch 必须定义官方来源、通知方式、变更审查、反对/退出和客户通知

Subprocessor watch MUST 记录供应商子处理方来源、订阅或通知方式、变更审查规则、反对或退出路径、客户通知和证据链接。

#### Scenario: 供应商子处理方发生变化

- GIVEN 一个关键供应商新增或替换子处理方
- WHEN 子处理方变化影响地区、目的、数据类别、人工审核、模型训练、支持流程、安全边界或客户承诺
- THEN `vendor-risk/subprocessor-watch/<target>.md` 必须记录 change review
- AND `vendor-risk/vendor-review/<target>.md` 必须记录风险、决定和下一步
- AND 没有可执行 objection/exit path 时必须有人审

### Requirement: Transfer impact 必须区分客户内容、系统数据、区域驻留、跨境机制和补充措施

Transfer impact MUST 记录 transfers、data residency、unsupported regions、linked artifacts、human checkpoint、review cadence 和状态。

#### Scenario: 供应商涉及跨境或区域驻留

- GIVEN 供应商处理客户数据且 origin/destination region、endpoint、model feature、support flow、subprocessor 或 storage location 可能跨境
- WHEN 创建 `vendor-risk/transfer-impact/<target>.json`
- THEN 每个 transfer 包含 vendor、origin_regions、destination_regions、data_categories、customer_content、system_data、transfer_mechanism、adequacy_or_exception、scc_module、supplementary_measures、subprocessors、residual_risk、last_verified、status
- AND data_residency 必须记录项目级配置、endpoint、支持功能、限制和最后验证时间
- AND SCC 或合同条款需要补充措施说明，不能作为唯一证据

### Requirement: Vendor review 必须复盘供应商变更、DPA、子处理方、传输、删除协助、事故和依赖健康

Vendor review MUST 记录 recent changes、new vendors、DPA status、subprocessor changes、transfer/residency、data rights/deletion assistance、incidents/breach notices、SLO/dependency health、open risks、one next change 和 review cadence。

#### Scenario: 高风险供应商动作前复盘

- GIVEN 即将上线新客户数据供应商、启用 AI provider、改变区域/数据驻留、允许训练/反馈分享、处理敏感数据、接受合同缺口或更新客户承诺
- WHEN 做出上线或继续使用决定
- THEN `vendor-risk/vendor-review/<target>.md` 不得过期
- AND 不存在未解释的 DPA 缺口、子处理方变化、跨境缺口、删除协助缺口、事故通知缺口、关键路径无 fallback 或供应商政策变化
