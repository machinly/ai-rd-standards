# 发布：客户试点与 go-live

## 执行细则

<!-- rule-id: RELEASE-CUSTOMER-001 -->
### 识别客户上线触发范围

design partner、private beta、proof of concept、pilot、paid pilot、enterprise onboarding 与 production go-live 都属于客户上线。新建 workspace/tenant，启用 SSO/SCIM、客户 flag、entitlement、billing、webhook/API、数据导入或同步，以及客户专属 AI route、RAG、memory 或 tool action，同样触发本组规则；从试点转付费、从内部转外部、从单客户 beta 转公开可用时必须重新判断。

<!-- rule-id: RELEASE-CUSTOMER-016 -->
### 满足 go-live 最小资格并完成交接

客户进入 production 前，至少维护适用的 pilot charter、tenant provisioning、launch readiness、success plan 或 handoff review。没有租户事实、上线 gate、支持路径或退出路径时不得上线；readiness、support path 与 rollback/offboarding 必须可执行。交接要明确客户成功、支持和退出责任，以少量高价值工件保护一人公司的注意力。

<!-- rule-id: RELEASE-CUSTOMER-013 -->
### 使用不泄露客户身份的 account 别名

同一客户的上线工件统一使用 `<account>` 别名。别名不得含真实公司名、个人姓名、邮箱、手机号或 customer secret；需要回到真实对象时使用受控引用，而不是把身份信息复制进仓库文件。

<!-- rule-id: RELEASE-CUSTOMER-002 -->
### 维护 tenant provisioning 主记录

租户事实写入 `customer-onboarding/tenant-provisioning/<account>.json`。主记录至少包含 `target`、`owner`、`customer_alias`、`environment`、`tenant_id_ref`、`identity`、`roles`、`entitlements`、`feature_flags`、`data_imports`、`integrations`、`billing`、`ai_settings`、`observability`、`support_refs`、`rollback_or_offboarding`、`audit_refs`、`human_checkpoint`、`review_cadence` 与 `status`；敏感值只放安全引用。

<!-- rule-id: RELEASE-CUSTOMER-003 -->
### 解释客户身份与权限

`identity` 记录身份来源、SSO/SCIM 状态、管理员角色来源和生命周期 owner，真实 IdP secret 不进入文件。`roles` 与 `entitlements` 必须能回答客户被允许做什么、被禁止做什么以及授权理由，不能只列角色名。

<!-- rule-id: RELEASE-CUSTOMER-004 -->
### 描述客户 feature flag

`feature_flags[]` 的每项记录 `key`、`environment`、`value`、`owner`、`rollout_scope`、`rollback` 和 `status`。缺少范围或回退的 flag 不得作为客户上线控制手段。

<!-- rule-id: RELEASE-CUSTOMER-005 -->
### 描述客户数据导入

`data_imports[]` 的每项记录 `id`、`source`、`data_classification`、`contract_ref`、`status` 和 `dry_run_required`。需要 dry-run 却没有证据时，对应导入 gate 不能通过。

<!-- rule-id: RELEASE-CUSTOMER-006 -->
### 描述客户集成

`integrations[]` 的 release 投影至少记录 `id`、`kind`、`provider`、`secrets_ref`、`webhook_or_api_refs` 与 `status`。这里只保存受控引用；数据边界与测试证据由相关技术设计和验证规则提供并链接。

<!-- rule-id: RELEASE-CUSTOMER-007 -->
### 描述客户 billing

`billing` 明确 test 或 live、plan、entitlement source，以及 Stripe/customer id 的安全引用。由 test 切换 live 属于人工 checkpoint，不能因字段已经存在就自动发生。

<!-- rule-id: RELEASE-CUSTOMER-008 -->
### 描述客户 AI settings

`ai_settings` 记录 model route、RAG source、memory、tool action 和 human review；相应 eval 与 provider/data boundary 必须通过链接交给验证和边界规则。缺少 human review 或降级路径时，不得启用真实客户数据驱动的高影响 action。

<!-- rule-id: RELEASE-CUSTOMER-009 -->
### 提供 tenant rollback 或 offboarding

`rollback_or_offboarding` 必须能直接说明如何关闭租户访问、暂停同步、导出或删除数据、停用集成并通知客户。每个动作写明执行条件和责任人；只有“联系支持”而没有实际路径不算可退出。

<!-- rule-id: RELEASE-CUSTOMER-010 -->
### 维护 launch readiness 主记录

上线判断写入 `customer-onboarding/launch-readiness/<account>.json`，包含 `target`、`owner`、`customer_alias`、`launch_type`、`readiness_gates`、`blockers`、`success_criteria`、`support_plan`、`communication_plan`、`rollback_or_exit`、`linked_artifacts`、`human_checkpoint` 与 `status`。`launch_type` 只能取 `internal_trial`、`design_partner`、`private_beta`、`pilot`、`paid_pilot` 或 `production`；上线前必须完成该记录。

<!-- rule-id: RELEASE-CUSTOMER-011 -->
### 使用统一 readiness gate 合同

外部客户默认检查 `commercial`、`auth_tenant`、`data`、`billing_entitlement`、`integrations`、`ai_eval`、`security_privacy`、`observability_slo`、`support`、`rollback` 与 `customer_acceptance`。每条 gate 记录 `id`、`area`、`check`、`evidence_ref`、`required`、`result`、`owner` 和 `status`。`result` 仅可为 `pending`、`pass`、`fail`、`blocked`、`not_applicable` 或 `accepted_risk`。

<!-- rule-id: RELEASE-CUSTOMER-012 -->
### 阻断付费与 production 上线缺口

`required=true` 的 gate 若为 `fail`、`blocked` 或 `accepted_risk`，不得静默继续；必须经过人工 checkpoint。`paid_pilot` 或 `production` 缺少可执行的 rollback、offboarding、support 证据或 customer acceptance 时属于硬阻断，不得用“限定试点”或一般 accepted risk 绕过。转 paid pilot/production、导入真实客户数据、启用同步/RAG/memory/tool/connector、SSO/SCIM、admin impersonation、cross-tenant support、production webhook、live billing 或客户专属 entitlement，同样需要人的明确决定。

<!-- rule-id: RELEASE-CUSTOMER-014 -->
### 控制客户数据进入 AI

客户数据进入 prompt、RAG、memory 或 tool action 前，必须具备 human review 或 fallback。试点样例进入长期 eval/dataset 前要确认授权、脱敏与用途；默认只保存受控引用以及合成或脱敏案例，不把原始客户内容当作通用 fixture。

<!-- rule-id: RELEASE-CUSTOMER-015 -->
### 链接客户专属 AI 的验证与恢复证据

客户专属 prompt、tool、retrieval source 或 model route 必须链接相应的数据集、红队、RAG 与 AI quality rollback 工件。任一链接失效时，该客户配置不得继续按已验证状态 rollout。

<!-- rule-id: RELEASE-CUSTOMER-017 -->
### 单独批准客户内容二次使用

把客户内容用于 eval、demo、训练、文档或公开材料必须单独取得人工决定；原上线授权不能自动扩展为这些用途，拒绝或未决定时保持不使用。

<!-- rule-id: RELEASE-CUSTOMER-018 -->
### 限定未验收的非生产试点

`internal_trial`、`design_partner`、`private_beta` 或非付费 `pilot` 尚无 customer acceptance 时，只能经人工 checkpoint 保持在明示的有限、非生产范围，并在 readiness 记录中写出 `cannot_promote_to_production=true`、缺口、重新判断条件和退出动作。缺少可执行 rollback 或 offboarding 时，不得把该缺口解释为已接受并继续扩大；人的决定只能补齐受控退出后留在有限范围，或选择不发布/退出。请求 paid pilot 或 production 时立即适用硬阻断规则。
