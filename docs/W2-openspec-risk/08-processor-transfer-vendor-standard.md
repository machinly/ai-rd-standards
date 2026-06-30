# 供应商处理方、DPA、子处理方与数据出境治理规范
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“新供应商、DPA、子处理方、数据出境、供应商训练或保留条款”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## 目标

一人公司的 AI 产品很容易把客户数据交给外部供应商：模型 API、embedding、reranker、对象存储、日志、分析、客服、支付、邮件、错误追踪、托管数据库、云函数、浏览器录屏、数据标注、人工审核。本触发专项的目标是建立最小可执行的供应商数据处理治理：每个会处理客户数据的供应商都能回答“它是什么角色、处理什么数据、合同/DPA 覆盖什么、子处理方怎么变、跨境或区域边界是什么、删除和事故时怎么配合、什么时候必须人判断”。

本阶段不是法律意见，也不替代律师审阅。它把高风险供应商判断压成可 review、可脚本检查、可在 OpenSpec 中追踪的工程工件。

## 核心依据

- 《人月神话》：复杂系统最怕概念不一致。供应商不是“外部工具”，而是数据处理接口；接口不清楚，系统边界就会失真。
- 小型项目管理：一人公司不能维护企业采购/GRC 流程，只保留能阻止高损失错误的判断点：新供应商、敏感数据、跨境、训练/保留、子处理方、删除协助、事故通知、关键路径依赖。
- Ross Anderson, Security Engineering：安全问题常出现在信任边界、激励和运营现实中。供应商治理要看它会不会、能不能、愿不愿意按你的指令处理数据。
- Software Engineering at Google, Dependency Management：外部依赖是我们不控制的网络。供应商的数据条款、区域、模型、子处理方和产品能力都会演进，因此需要版本化记录和复审。
- NIST SP 800-161 Rev. 1 Update 1：供应链风险来自对外部产品和服务的可见性、理解和控制下降；要把 supplier risk 纳入风险评估和持续监控。
- ISO/IEC 27036：供应商关系本身需要信息安全治理，既要看采购方，也要看供应方责任。
- GDPR / EDPB：controller、processor、joint controller 是功能性角色；处理方合同需要明确目的、数据类别、指令、保密、安全、子处理方、权利协助、删除/返还、审计和跨境处理；跨境传输要有适当保障并持续复评。
- CCPA / CPRA 服务提供商规则：服务提供商或承包商合同要限制目的、禁止出售/共享、要求同等隐私保护、协助消费者请求、允许合理审查并约束分包。
- FTC AI 隐私指导：AI 公司必须兑现隐私和保密承诺；更宽松的数据共享、第三方处理或训练用途不能靠隐蔽条款变更完成。
- OpenAI 官方 DPA、Data Controls、Sub-processor List：AI API 的数据控制、训练默认、区域/驻留、ZDR、子处理方和支持/审核边界会变化，必须按实际项目设置记录。
- Google SRE SLO with dependencies：用户可见可靠性依赖外部服务时，SLO、告警和降级不能只看自己的服务。
- OWASP LLM Top 10：LLM 应用供应链风险包括第三方服务、组件、模型、数据集和部署平台，可能导致泄露、失败或完整性问题。

## 范围

适用对象：

- 会处理客户数据、客户内容、个人数据、提示词、响应、文件、日志、支持材料、用量、账单、标注样本、RAG 内容或向量数据的外部供应商。
- OpenAI、其他模型供应商、embedding/rerank、云数据库、对象存储、CDN、邮件、短信、支付、客服、分析、错误追踪、监控、日志、数据标注、人工审核、身份提供商和集成平台。
- 会影响删除、导出、更正、停止同步、事故通知、区域驻留、客户合同、隐私政策或 AI disclosure 的供应商变更。

不适用对象：

- 纯本地开发工具且不接收真实客户数据。
- 只提供公开静态资源且不接收用户标识、日志或内容的服务。
- 正式 DPA、SCC、BAA、客户合同和法律谈判文本的起草；这些需要专业审阅或单独 change。
- 完整 TPRM/GRC 平台、供应商问卷系统、采购审批流和法律档案库。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
vendor-risk/
  processor-register/<target>.json
  dpa-checklist/<target>.json
  subprocessor-watch/<target>.md
  transfer-impact/<target>.json
  vendor-review/<target>.md
```

### `vendor-risk/processor-register/<target>.json`

供应商处理方注册表必须包含：

- `target`
- `owner`
- `processing_activities`
- `critical_vendors`
- `data_boundaries`
- `linked_artifacts`
- `human_checkpoint`
- `review_cadence`
- `status`

`processing_activities` 每项至少包含：

- `id`
- `vendor`
- `product_service`
- `role`
- `purpose`
- `data_classes`
- `personal_data`
- `sensitive_data`
- `customer_content`
- `model_training_allowed`
- `retention_summary`
- `region_or_residency`
- `subprocessor_source`
- `dpa_ref`
- `transfer_ref`
- `security_refs`
- `deletion_assistance`
- `incident_notice`
- `status`

`role` 默认只允许：

- `processor`
- `service_provider`
- `contractor`
- `independent_controller`
- `joint_controller`
- `no_customer_data`

默认：

- 只要供应商处理客户内容、个人数据、提示词、响应、文件、日志或支持材料，就必须登记。
- 如果供应商不是 `processor`、`service_provider` 或 `contractor`，默认高风险，需要人审。
- `model_training_allowed` 默认 `false`；任何 opt-in、feedback sharing、fine-tuning、eval sharing 或供应商改进用途都需要人审。
- `customer_content` 与 `system_data` 要分开记录；不要把账户、账单、用量、支持请求误认为数据驻留一定覆盖。
- `security_refs` 可以链接 SOC 2、ISO 27001、trust center、DPA、security page 或内部评估，不要求一人公司一开始跑完整问卷。

### `vendor-risk/dpa-checklist/<target>.json`

DPA/合同检查清单必须包含：

- `target`
- `owner`
- `agreements`
- `exceptions`
- `renewal_or_recheck`
- `human_checkpoint`
- `status`

`agreements` 每项至少包含：

- `vendor`
- `agreement_type`
- `effective_date`
- `scope`
- `controller_processor_roles`
- `documented_instructions`
- `confidentiality`
- `security_measures`
- `subprocessor_authorization`
- `data_subject_assistance`
- `breach_notice`
- `delete_or_return`
- `audit_or_assurance`
- `international_transfer_terms`
- `ccpa_service_provider_terms`
- `ai_training_terms`
- `retention_terms`
- `status`

默认：

- `agreement_type` 可以是 `dpa`、`service_terms`、`baa`、`scc`、`customer_contract`、`no_personal_data` 或 `not_required_with_reason`。
- 不要求所有早期供应商都签企业 DPA，但必须说明为什么可接受、覆盖哪些数据、未覆盖什么、何时升级。
- 如果供应商承载客户内容、敏感数据、生产日志、支持材料、模型输入/输出或跨境传输，必须有 DPA/等价条款或明确暂停上线。
- 合同缺口不靠“以后补”进入生产；需要 `exceptions` 写明风险、限制、到期日期和下一步。
- CCPA/CPRA 场景下，服务提供商或承包商必须限制目的、禁止出售/共享、协助用户请求、接受合理审查和约束分包。

### `vendor-risk/subprocessor-watch/<target>.md`

子处理方监控说明必须包含：

```markdown
# <target> Subprocessor Watch
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“新供应商、DPA、子处理方、数据出境、供应商训练或保留条款”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## Scope

## Vendor Sources

## Subprocessor Lists

## Notification Method

## Change Review

## Objection / Exit Path

## Customer Notice

## Evidence Links

## Review Cadence
```

默认：

- 对关键 AI、云、数据库、日志、分析、客服和支付供应商，记录其官方 subprocessor list、更新订阅或 changelog 来源。
- 如果供应商新增子处理方会改变国家/地区、目的、数据类别、人工审核、模型训练、支持流程或安全边界，需要人审。
- 如果无法反对或退出，也要写清楚可接受原因和替代方案；不要假装有不存在的合同权利。
- 有客户合同或公开隐私承诺时，子处理方变更要连接 W2 信任承诺注册表和 W9 审计证据。

### `vendor-risk/transfer-impact/<target>.json`

数据出境/区域影响记录必须包含：

- `target`
- `owner`
- `transfers`
- `data_residency`
- `unsupported_regions`
- `linked_artifacts`
- `human_checkpoint`
- `review_cadence`
- `status`

`transfers` 每项至少包含：

- `vendor`
- `origin_regions`
- `destination_regions`
- `data_categories`
- `customer_content`
- `system_data`
- `transfer_mechanism`
- `adequacy_or_exception`
- `scc_module`
- `supplementary_measures`
- `subprocessors`
- `residual_risk`
- `last_verified`
- `status`

默认：

- 出境不是只看数据库区域；模型推理、对象存储、缓存、日志、支持、审核、CDN、备份、analytics、trace 和子处理方都可能构成跨境处理。
- `transfer_mechanism` 可记录 `adequacy`、`scc`、`uk_idta_or_addendum`、`dp_framework`、`contractual_terms`、`not_personal_data` 或 `not_applicable`。
- SCC 或类似合同不是自动通行证；需要记录是否有加密、密钥控制、最小化、区域端点、ZDR/abuse monitoring 控制、日志脱敏、删除/保留限制等补充措施。
- 如果选择 OpenAI 或其他模型 API 的数据驻留，必须记录项目级配置、端点、支持的模型/功能和限制，不把营销页当作实际配置证据。
- `system_data` 不等于 `customer_content`；供应商可能把账户、账单、用量、支持、schema 或元数据放在其他区域。

### `vendor-risk/vendor-review/<target>.md`

供应商处理方复盘必须包含：

```markdown
# <target> Vendor Review
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“新供应商、DPA、子处理方、数据出境、供应商训练或保留条款”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## Recent Changes

## New Vendors

## DPA Status

## Subprocessor Changes

## Transfer / Residency

## Data Rights / Deletion Assistance

## Incidents / Breach Notices

## SLO / Dependency Health

## Open Risks

## One Next Change

## Review Cadence
```

默认节奏：

- pre-revenue：每月一次或新增真实客户数据供应商前。
- 有付费客户：每次供应商、数据类别、区域、AI provider、日志/支持/分析流变化前。
- 企业客户、敏感数据、跨境、DPA/SCC、删除失败、供应商事故、subprocessor 变更：立即复盘。

## Go / Kratos / sqlc / gRPC 默认规则

- 所有对外供应商调用必须经过可定位的 client boundary，不允许业务代码到处散落供应商 SDK 调用。
- Kratos config 中记录供应商 endpoint、region、data residency、timeout、retry、disable switch；secret 只从 secrets manager 或环境注入。
- gRPC/HTTP 调用必须有 deadline、retry budget、idempotency key、request id 和 vendor name 进入 trace/log；日志不得包含 raw prompt、raw response、customer file、secret 或敏感字段。
- sqlc 默认表可以包含：`vendor_processors`、`vendor_agreements`、`vendor_transfers`、`vendor_subprocessor_events`、`vendor_reviews`，但早期可以先用 repo artifacts。
- 新增供应商前，OpenSpec design 必须链接 `processor-register`、`dpa-checklist` 和 `transfer-impact`。
- 删除、导出、更正、停止同步请求如果涉及供应商，必须连接 W2 客户数据 deletion/rights policy 和 W9 evidence package。

## Vite 前端默认规则

- 面向用户的隐私、AI disclosure、数据区域、训练/反馈分享、第三方处理说明必须短、清楚、可找到。
- 管理台如果提供区域、模型供应商、数据分享或日志开关，默认使用 Vercel/Geist 风格的克制设置界面：明确标签、状态、最后验证时间、危险变更确认。
- 不在 UI 中用“完全本地”“不出境”“不保存”“不训练”“企业级合规”等强承诺，除非 `commitment-register` 和供应商工件有证据。
- 供应商故障、区域不支持或数据权利请求不能完成时，前端显示真实状态和下一步，不用模糊错误文案掩盖。

## AI workflow 默认规则

- 新模型、embedding、reranker、agent tool、web search、browser connector、MCP server、人工审核或数据标注供应商，只要接触客户数据，都必须登记。
- Prompt、response、file、RAG chunk、embedding input、tool output、support transcript 默认视为 customer content 或高敏数据边界，除非 data map 明确排除。
- API business 默认不训练不等于所有 OpenAI 消费产品或所有反馈/评测/微调数据都不训练；必须按具体产品、项目和 data controls 记录。
- 启用 data residency、ZDR、abuse monitoring controls、BAA/HIPAA、EU endpoint、fine-tuning、eval sharing、feedback sharing 前，必须记录实际项目设置和限制。
- AI 供应商的子处理方、区域、模型弃用、保留和政策变化进入 release checklist；不要把一次性查询当作永久事实。

## 需要人判断的关键点

默认不问：JSON 字段顺序、低风险供应商描述、普通 trust center 链接、章节标题、小的证据链接修正。

必须问：

- 是否把客户内容、个人数据、提示词、响应、文件、日志、支持材料或向量数据发给新供应商。
- 是否处理敏感数据、未成年人、高影响领域、受监管数据或客户合同限制数据。
- 是否接受没有 DPA/等价条款、没有删除协助、没有事故通知、没有子处理方透明度或无法审查的供应商。
- 是否允许供应商把数据用于训练、模型改进、反馈、评测、微调、人工审核或更长保留。
- 是否发生跨境/区域变化，或使用不支持目标区域/目标模型/目标 endpoint 的功能。
- 是否供应商角色变成 independent controller、joint controller、广告/分析再利用方或数据经纪类风险。
- 是否关键路径只有单一供应商，且没有降级、退出、SLO 解释或客户通知。
- 是否需要律师、隐私专业人士、安全评估、客户合同审阅或正式 DPA/SCC/BAA。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“有哪些处理方、合同是否覆盖、子处理方怎么变、数据是否出境、多久复盘”。
- 保留：人只判断新数据供应商、敏感/高影响数据、训练/保留、跨境、DPA 缺口、子处理方变化和关键路径无替代。
- 调整：不要求一开始做完整供应商问卷；先看供应商官方 DPA、trust center、subprocessor list、data controls 和当前项目配置。
- 调整：不把所有 SaaS 都当同等风险；只处理客户数据或生产关键路径的供应商需要完整工件。
- 风险：一人公司容易把“供应商说支持数据驻留”误读为“我的项目已经启用”。缓解：`transfer-impact` 必须记录项目级配置、端点、支持功能和 last_verified。

结论：可落地。一个人可以先登记 5 到 15 个真实供应商，把无法证明的数据承诺降级或暂停上线，再只跟进高风险变化。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：供应商数据边界清楚后，AI disclosure、privacy policy、enterprise FAQ 和客户问答不会互相矛盾。
- 工程角度：供应商调用收口到 client boundary，Go/Kratos 配置、trace、timeout、retry 和 disable switch 可实现。
- 运维角度：外部依赖进入 SLO/incident/release checklist，供应商事故和子处理方变化有明确复盘入口。
- 安全隐私角度：DPA、子处理方、跨境、删除协助、事故通知、训练/保留和敏感数据处理进入人工 checkpoint。
- 成本角度：不默认多云/多供应商，只要求关键路径写清 fallback、退出触发和人工成本，避免早期过度架构。

结论：可落地。本专项把“供应商能不能处理我们的客户数据”变成工程化证据链，而不是临上线前翻合同和政策页面。


