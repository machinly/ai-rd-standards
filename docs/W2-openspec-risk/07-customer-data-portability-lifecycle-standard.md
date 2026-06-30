# 客户数据导入、导出、同步与删除治理规范
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“客户数据导入、导出、同步、删除、备份、向量库或 AI 记忆数据流”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## 目标

一人公司很容易把“客户数据”拆散在主库、对象存储、向量库、日志、分析事件、备份、第三方 SaaS、AI 记忆和支持工具里。等用户要求导出、删除、迁移或停止同步时，才发现没有一张图能回答：数据从哪里来、在哪里存、导出什么、删除到什么程度、第三方怎么同步、备份里怎么办、AI 向量索引和缓存是否还残留。

本专项定义客户数据导入、导出、同步与删除治理规范。目标不是做企业数据治理平台，而是让每个生产 target 都能用五个小工件回答：数据在哪里，如何安全进出，如何可靠同步，如何响应访问/导出/删除/更正请求，如何证明链路还能信。

默认原则：客户数据搬运必须先有数据地图、格式契约、身份/权限、幂等、审计、敏感字段边界和删除传播路径。没有这些，不能把导入/导出/同步/删除做成生产功能。

## 核心依据

- 《人月神话》：复杂系统的成本来自隐形状态和概念不一致；客户数据一旦没有系统地图，后续导出和删除会变成考古。
- 小型项目管理：一人公司只保留能减少灾难性返工的工件：数据地图、传输契约、同步 runbook、权利请求策略、生命周期复盘。
- Designing Data-Intensive Applications：数据系统要可靠、可维护、可演进；导入、同步、导出和删除都应被视为数据系统的一部分，而不是临时脚本。
- Database Reliability Engineering：数据库操作要具备可恢复、可审计、可自动化和可验证的习惯；批量导入/删除不能绕开可靠性边界。
- GDPR / EDPB 数据主体权利：访问、更正、删除、限制处理、可携带性和反对处理等权利要求系统能定位、导出、删除或说明例外。即使不把 GDPR 当作全球默认法律，也应把这些权利用作产品设计基线。
- NIST Privacy Framework：隐私风险管理覆盖数据生命周期，包括收集、保留、使用、披露、共享、传输和处置。
- NIST SP 800-88 Rev. 2：数据销毁/清除要让目标数据在给定努力水平下不可访问；云与现代存储也需要逻辑销毁和可验证控制。
- FTC Protecting Personal Information：没有业务需要的敏感个人信息不要收集，确需保留时只保留必要时间并安全处置。
- OWASP File Upload / CSV Injection：导入文件是不可信输入；导出 CSV/表格也可能成为公式注入载体。
- RFC 4180：CSV 是常见交换格式，但要承认实现差异并明确 MIME、编码、列、换行和转义约束。
- Google SRE Data Processing Pipelines：数据管道延迟或错误会直接造成用户问题；导入、同步、删除传播都需要健康信号、错误处理和可重放边界。
- PostgreSQL COPY：批量导入导出可以用 COPY/`\copy` 等能力，但必须理解服务器端文件访问、列映射、错误处理和权限边界。
- OpenAI Data Controls：AI 平台可能保存 abuse monitoring logs 或 application state；文件、vector store、conversation state、responses、embeddings 等要按各自 retention/delete 边界管理。

## 范围

适用对象：

- 用户或客户上传 CSV/TSV/JSON/JSONL/ZIP/文件包、从第三方系统导入数据、从旧系统迁移数据。
- 客户数据导出、数据可携带性、管理员导出、审计导出、机器可读导出、客户迁出。
- 与 CRM、支付、身份、邮件、知识库、文件存储、代码托管、客服、模型供应商、分析平台之间的数据同步。
- 用户请求访问、更正、删除、限制处理、停止同步、撤回授权、导出数据。
- Go/Kratos/sqlc/gRPC 服务中的 import job、export job、sync cursor、deletion job、data subject request、audit event、staging table。
- Vite 前端中的导入向导、字段映射、导出中心、删除请求状态、同步设置、错误解释和危险动作确认。
- AI 产品中的 memory、RAG source、vector store、file upload、embedding、cache、prompt/response retention、eval fixture、tool output 和第三方模型状态。

不适用对象：

- 普通 schema migration、backfill 和数据修复；W4 管。
- Webhook 签名、inbox/outbox 和事件 catalog；W4 管。
- 备份恢复演练；W7 管。
- 审计证据包和对外合规材料；W9 管。
- 正式法律意见、跨境传输法律分析、诉讼保全、监管回应；需要专业服务或单独 OpenSpec change。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
customer-data/
  data-map/<target>.json
  transfer-contract/<target>.json
  sync-runbook/<target>.md
  rights-deletion-policy/<target>.json
  lifecycle-review/<target>.md
```

### `customer-data/data-map/<target>.json`

数据地图是导入、导出、同步和删除的事实来源，必须包含：

- `target`
- `owner`
- `systems_of_record`
- `data_sets`
- `derived_stores`
- `external_processors`
- `ai_stores`
- `backup_locations`
- `identity_keys`
- `tenant_boundary`
- `retention_classes`
- `exportability`
- `deletion_classes`
- `audit_refs`
- `human_checkpoint`
- `review_cadence`
- `status`

`data_sets` 每项至少包含：

- `id`
- `name`
- `system_of_record`
- `data_classification`
- `contains_personal_data`
- `contains_sensitive_data`
- `tenant_scope`
- `source`
- `purpose`
- `retention`
- `export_policy`
- `delete_policy`
- `sync_targets`
- `status`

默认规则：

- 每个客户数据字段或数据集必须有 system of record；没有主权系统的数据不进入同步。
- derived stores 包括 analytics、search index、cache、RAG chunks、embeddings、AI memory、exports、logs、support summaries。
- backup_locations 必须说明保留期、恢复后的再删除流程和是否能单条删除。
- identity_keys 记录 user、tenant、workspace、external id、provider id 的映射方式；不得把 email 当作唯一同步键。
- exportability 区分 customer_provided、observed_behavior、derived_inference、system_generated、audit/security、billing/tax、third_party。

### `customer-data/transfer-contract/<target>.json`

传输契约定义允许客户数据如何导入、导出和交换，必须包含：

- `target`
- `owner`
- `formats`
- `import_contracts`
- `export_contracts`
- `schema_policy`
- `validation_policy`
- `security_policy`
- `privacy_policy`
- `limits`
- `idempotency`
- `error_policy`
- `audit_policy`
- `human_checkpoint`
- `status`

`import_contracts` 每项至少包含：

- `id`
- `format`
- `source`
- `allowed_data_classes`
- `schema_ref`
- `field_mapping`
- `validation`
- `staging`
- `dedupe_key`
- `idempotency_key`
- `dry_run_required`
- `rollback_or_compensation`
- `status`

`export_contracts` 每项至少包含：

- `id`
- `format`
- `audience`
- `included_data_sets`
- `excluded_data_sets`
- `redaction`
- `csv_injection_protection`
- `delivery_method`
- `expiry`
- `access_control`
- `status`

默认规则：

- 导入文件默认是不可信输入：允许格式白名单、大小限制、MIME/签名校验、文件名重写、隔离存储、恶意内容检查、schema validation。
- CSV/TSV 导出默认启用公式注入防护，任何以 `= + - @ tab CR LF` 或全角等价字符开头的单元格都要安全处理。
- 客户导出默认用机器可读格式：CSV/JSON/JSONL + schema/readme；大型导出异步生成、有过期时间和访问审计。
- 导入默认先进入 staging，不直接写业务表；通过 dry-run、字段映射、样本验证、去重和批处理后再 commit。
- 导出默认排除 secret、token、password、session cookie、内部安全日志、其他租户数据、第三方受限数据、raw prompt/response 和不可公开审计记录。

### `customer-data/sync-runbook/<target>.md`

同步 runbook 定义外部系统之间如何保持一致，必须包含：

- `Scope`
- `Systems`
- `Source Of Truth`
- `Identity Mapping`
- `Sync Direction`
- `Initial Import`
- `Incremental Sync`
- `Conflict Resolution`
- `Idempotency / Dedupe`
- `Backfill / Replay`
- `Deletion / Tombstone Propagation`
- `Rate Limits / Backpressure`
- `Observability`
- `Incident Actions`
- `Linked Artifacts`

默认规则：

- 同步必须明确单向、双向或人工确认；双向同步默认高风险，需要人审。
- 外部 id、tenant/workspace id、provider id 映射必须落库，不靠名称、邮箱或 UI 文案匹配。
- 增量同步必须有 cursor/checkpoint、last_success_at、attempt、error_class、dead letter 或等价记录。
- 冲突解决必须先保护客户数据：不确定时暂停、标记冲突或要求人工确认，而不是静默覆盖。
- 删除同步用 tombstone/deletion job 表达；删除事件不等于立即物理销毁，必须说明每个系统的最终状态。
- provider 失败、rate limit、schema drift、auth revoked、partial sync、duplicate import、跨租户疑似错配必须进入 incident/review。

### `customer-data/rights-deletion-policy/<target>.json`

权利请求与删除策略必须包含：

- `target`
- `owner`
- `request_types`
- `identity_verification`
- `scope_resolution`
- `workflow`
- `deletion_targets`
- `export_targets`
- `third_party_propagation`
- `backup_policy`
- `exceptions`
- `sla`
- `audit_policy`
- `human_checkpoint`
- `status`

`request_types` 默认至少覆盖：

- `access`
- `export`
- `rectification`
- `deletion`
- `restriction`
- `stop_sync`

`deletion_targets` 每项至少包含：

- `system`
- `data_sets`
- `method`
- `mode`
- `verification`
- `retention_exception`
- `status`

默认规则：

- 删除默认按 scope 解析：user、tenant、workspace、project、document、conversation、memory、file、vector store、analytics、third-party processor。
- 删除必须覆盖主库、对象存储、cache、search index、RAG chunks、embedding/vector store、AI memory、conversation/application state、analytics join key、support summaries、exports 和第三方同步目标中适用项。
- audit/security、billing/tax、fraud prevention、legal hold、合同义务和备份保留可能是例外，但必须可解释、可审计、有到期或复审。
- 删除请求必须有状态：received、verified、scoped、in_progress、partially_completed、completed、rejected、blocked_by_exception。
- 备份不默认单条擦除，但必须记录保留期、隔离、访问限制和从备份恢复后的再删除流程。
- AI/vector store 删除必须区分从索引移除、删除底层文件、删除 embedding、删除 cache 和删除模型供应商 application state。

### `customer-data/lifecycle-review/<target>.md`

生命周期复盘必须包含：

- `Recent Changes`
- `Imports`
- `Exports`
- `Sync Health`
- `Deletion / Rights Requests`
- `Third Party Propagation`
- `AI / Vector / Cache Coverage`
- `Backup / Restore Implications`
- `Security / Privacy Findings`
- `Incidents`
- `Open Risks`
- `One Next Change`
- `Review Cadence`

默认节奏：

- pre-revenue：每月一次，或新增导入/导出/删除/同步能力前。
- 有付费客户：每两周一次，或每次出现导入失败、错误导出、同步错配、删除失败、第三方传播失败、AI 残留、客户请求或隐私投诉后。
- 每次只选一个最高影响改进：补数据地图、限制导出字段、加 dry-run、加 tombstone、补第三方删除、补 AI/vector 删除、缩短导出有效期或补审计。

## Go / Kratos / sqlc / gRPC 默认规则

- 默认建立 customer data lifecycle service，集中处理 import/export/sync/delete，不让业务 handler 各自写一次。
- Protobuf API 明确定义 `ImportJob`、`ExportJob`、`SyncCursor`、`RightsRequest`、`DeletionJob`、`DeletionTarget`、`DataSetRef`。
- gRPC metadata 传播 actor、tenant、workspace、request id、trace id、idempotency key；payload 不包含 secret 或完整敏感内容。
- sqlc 默认表可包含：`customer_data_sets`、`customer_data_import_jobs`、`customer_data_import_rows`、`customer_data_export_jobs`、`customer_data_sync_cursors`、`customer_data_rights_requests`、`customer_data_deletion_jobs`、`customer_data_deletion_targets`、`customer_data_tombstones`、`customer_data_transfer_audit_events`。
- 批量导入使用 staging table + validation + commit step；生产 COPY/`\copy` 只能在受控 job 或 runbook 中使用。
- 导出使用异步 job，生成 artifact 有 expiry、checksum、audit event、download count、access scope。
- 删除使用可恢复的状态机：先 scope/dry-run，再执行 target tasks，再验证，再关闭请求；高风险删除需要人工 checkpoint。
- 所有 job 必须幂等、可重试、可取消、有 batch size、rate limit、checkpoint 和 dead letter。

## Vite 前端默认规则

- 导入向导必须显示格式、字段映射、样本预览、验证错误、dry-run 结果和 commit 确认。
- 导出中心必须显示导出范围、格式、生成时间、过期时间、下载次数、敏感字段排除说明和撤销入口。
- 删除/停止同步请求必须显示影响范围、不可逆部分、保留例外、预计完成状态和支持联系路径。
- 危险操作使用明确确认，不把“删除账号”“删除 workspace”“删除 AI 记忆”“停止同步”混在同一个模糊按钮里。
- UI 保持 Vercel/Geist 风格：密集但清晰，表格可扫描，状态标签克制，深色模式可读，不用营销文案掩盖不可逆后果。

## AI workflow 默认规则

- AI 不得直接执行客户数据导入、导出、同步或删除；最多生成 mapping 建议、异常摘要、dry-run 解释和 checklist。
- AI 参与字段映射或数据清洗时，输入样本必须脱敏或最小化；不能把完整客户文件发给模型，除非 privacy record 和 human checkpoint 允许。
- AI 数据删除覆盖 memory、RAG source、vector store、uploaded file、embedding、conversation/application state、eval fixture、trace/debug sample、tool output cache。
- 删除后的 AI 行为必须有最小 eval 或 dry-run：删除对象不再被检索、记忆不再注入、引用不再出现、导出不再包含。
- AI 生成的数据导出说明、删除确认或客户沟通只能作为 draft，发送前需要人审。

## 需要人判断的关键点

只把这些问题交给人：

- 是否新增客户数据类别、外部 processor、第三方同步目标、跨租户/跨产品数据流或跨境传输。
- 是否允许导入/导出 sensitive、restricted、customer_confidential、支付、身份、健康、法律、金融、未成年人或高影响领域数据。
- 是否执行不可逆删除、批量删除、租户级删除、账号合并、跨系统覆盖、双向同步或从备份覆盖生产。
- 是否接受删除例外：billing/tax、security/audit、fraud、legal hold、合同义务、备份保留、供应商不可删。
- 是否允许 AI/model provider 接收客户文件、导入样本、raw prompt/response、support data 或用于 eval/training。
- 是否对外分享导出包、迁移包、审计包、第三方接收方列表或删除证明。

其他字段完整性、章节、JSON 枚举、allowed formats、敏感字段扫描、dry-run/idempotency/retry/status、OpenSpec linkage、positive/negative fixture 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“数据在哪、怎么进出、怎么同步、怎么删/响应请求、最近是否可信”。
- 保留：人只判断新增数据边界、敏感导入导出、不可逆动作、删除例外、AI/供应商数据使用和对外证明。
- 调整：不要求企业数据目录或隐私平台；先用 JSON/Markdown 把数据地图和 job 状态机定住。
- 调整：导入/导出/删除都默认异步 job，不要求一开始实时同步所有系统。
- 风险：数据地图可能过期。缓解：lifecycle review 和 verifier 检查 derived stores、AI stores、backup locations、third-party propagation。

结论：可落地。一个人可以先为最关键 target 写五个文件，把“客户走的时候数据能带走、该删的能删、删不了的能解释”变成工程能力。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：导入/导出/删除状态可见，降低客户对数据被困住或删不干净的焦虑。
- 工程角度：Go/Kratos lifecycle service、sqlc job/target/tombstone 表和 gRPC 状态机让批量动作可追踪。
- 运维角度：同步 cursor、dead letter、rate limit、checkpoint、retry 和 lifecycle review 支撑排障。
- 安全隐私角度：文件上传、CSV 注入、敏感字段、第三方传播、AI/vector 残留和备份保留都有边界。
- 成本角度：大型导出、全量重同步、向量重建和供应商删除都走 job 和人审，避免一次请求烧穿资源。

结论：可落地。本专项把客户数据生命周期从“散落的功能按钮”压成一条可检查、可恢复、可审计的数据搬运和删除链路。


