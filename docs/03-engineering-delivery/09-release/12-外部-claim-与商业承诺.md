# 发布：外部 claim 与商业承诺

## 执行细则

<!-- rule-id: RELEASE-CLAIM-001 -->
### 识别需要 gate 的外部表述

官网、landing page、pricing、help center、developer portal、API reference、SDK README、release note、status/security 页面、privacy、terms、DPA、AUP、AI disclosure、support macro 与 sales email 都是发布面。涉及能力、准确率、延迟、可用性、安全、隐私、保留/训练/驻留、人工审核、合规、退款/计费、IP、支持响应或 API 稳定性的表述必须进入 claim gate。新增强承诺、扩大范围、减少限制或改变数据、AI、安全、费用、SLA 含义时必须更新 gate，并从本次发布链接适用的 `claim-control/surface-inventory/<target>.json`、`claim-control/claim-evidence-map/<target>.json`、`claim-control/release-gate/<target>.json`、`claim-control/correction-runbook/<target>.md` 与 `claim-control/claim-review/<target>.md`；不适用项要明确，而不是留下断链。

<!-- rule-id: RELEASE-CLAIM-002 -->
### 维护 claim release gate 主记录

每个 production 表述目标使用 `claim-control/release-gate/<target>.json`，记录 `target`、`owner`、`change_id`、`release_or_surface`、`changed_claims`、`new_claims`、`removed_claims`、`evidence_checks`、`surface_checks`、`human_decisions`、`rollback_or_correction`、`linked_artifacts` 与 `status`。字段必须指向当前事实，不能只复制营销文案。

<!-- rule-id: RELEASE-CLAIM-003 -->
### 记录 changed/new claim 差异

每条 changed 或 new claim 使用 `claim_id` 定位，并记录 `change_type`、`old_text`、`new_text`、`risk_level`、`evidence_ref`、`human_checkpoint` 与 `decision`。删除项单独进入 `removed_claims`，避免用空的新文本隐藏撤回。

<!-- rule-id: RELEASE-CLAIM-004 -->
### 固定 claim 身份与更正路径

每条待发布 claim 都以稳定 `claim_id` 关联 evidence reference、owner、适用范围、最后核验时间与可执行 correction path；surface 文案变化不得另造身份来绕开旧证据或更正责任。owner、范围、时间或更正入口变化时，同步更新 release gate 与关联表述面。

<!-- rule-id: RELEASE-CLAIM-007 -->
### 阻断不满足批准条件的 claim

`decision=approve` 前，claim evidence map 不得存在 `unsupported` 或 `expired`，claim 也不得缺少 owner 或 scope。不支持的强声明不得发布；发现任一阻断项时，决定只能保持未批准、降级措辞或返回上游补证，不能靠空的人工确认字段制造批准。

<!-- rule-id: RELEASE-CLAIM-008 -->
### 链接 claim 发布证据

对本次发布实际适用的证据，claim release gate 必须提供链接；可选证据类型包括 PR/commit、evidence package、release checklist 与 OpenSpec change。

<!-- rule-id: RELEASE-CLAIM-009 -->
### 为付费客户重新 review claim

存在付费客户时，每次 release 前必须重新 review claim；developer API 稳定性、数据处理、SLO/SLA、模型或路由、供应商政策、合同条款或销售材料任一发生变化前，也必须复审受影响 claim。复审记录沿用 `EVALUATION-CLAIM-001` 的统一工件合同，本项不另设字段。

<!-- rule-id: RELEASE-CLAIM-010 -->
### 保持 claim 与后端事实一致

依赖政策、合同或运行行为的 claim 必须与底层工件对同一说法给出一致答案。后端依赖至少追溯适用的 Go/Kratos config、feature flag、tenant setting、model route、SLO、audit event、sqlc 数据状态机或 provider client boundary；改变这些事实的配置发布必须同步更新 claim gate，否则阻断 release。

<!-- rule-id: RELEASE-CLAIM-005 -->
### 对高风险 claim 保留人工决定

AI 能力或准确性、专业替代、security/privacy、数据保留、no-training、数据驻留、SLA、合规、费用/退款、IP 与 human review 等强 claim，发布或继续保留都必须由人判断。相同要求适用于条款、AI disclosure、安全、退款、合规、驻留、不保存等外部承诺，以及向客户承诺自定义功能、路线图、公开案例/引用、特定支持窗口或非标准 SLA；无证据时不得发布。

<!-- rule-id: RELEASE-CLAIM-006 -->
### 限制低风险修订与 AI 辅助

仅修 typo、格式或链接且不改变含义时，可记录为低风险而不请求人工判断。按钮、tooltip、empty state 和成功提示不得加入未经 gate 的“永远”“保证”“完全”“无限”“实时”“不训练”“合规级”或“专业级”等强词。AI 可以起草、扫描差异或建议降级措辞，但不能自行发布、扩写或强化 claim，最终文本仍须通过 gate。

<!-- rule-id: RELEASE-COMMERCIAL-001 -->
### 把商业承诺转成可运行义务

合同、订单、SLA、服务积分、DPA、安全附件、红线和其他商业承诺按 High-risk 处理。至少保留适用的 obligation register、agreement map、SLA/service-credit 处理方式、redline playbook 或 contract review，以及证据链接和人工接受记录。非标准条款、24/7、P1 响应、uncapped liability、数据/AI/security 强承诺或超出供应商能力的义务，必须由人决定；复杂情形可另开 OpenSpec 并回到相应边界规则。

<!-- rule-id: RELEASE-HANDOFF-001 -->
### 把发布结果交给运行与评估

完成 release 或客户 go-live 后，把观测、alert、incident 准备、凭据轮换与 watch 交给“运行”；用户、客户、支持或质量反馈交给“评估”。交接清单明确适用的 dashboard、support channel、billing/entitlement、AI quality 与 claim correction 责任，并记录下一去向。只有发布出口证据已完整且接收方知道观察与处置路径时，才能结束本项。
