# AI RAG、知识源、检索与引用治理规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/00-main.md` 已经判断需要 RAG 知识源、摄取、检索、引用、删除、prompt injection 或 grounding 治理时，才读取本文件。

如果当前只是判断 AI 行为应该如何定义好坏、失败和降级，先回到 `docs/W3-ai-behavior/00-main.md`。

## 目标

RAG 让 AI 产品能使用外部知识，但一人公司最容易在这里踩坑：把未经授权的资料塞进向量库、跨租户检索、文档过期、引用伪造、检索结果被 prompt injection 污染、删除请求无法从 embedding/index 中落实、低置信答案被包装成确定事实。本专项定义 AI RAG、知识源、检索与引用治理规范，让每个 RAG capability 能回答：哪些来源可用，如何摄取、分块、嵌入、索引、过滤、引用、评测、删除和降级。

默认原则：RAG context 是不可信外部上下文，不是系统指令。检索只能扩大可引用知识，不能绕过权限、替代事实核验、替代 eval、替代产品承诺或替代用户同意。

## 核心依据

- 《人月神话》：概念完整性比功能叠加重要；RAG 系统如果没有来源、权限、freshness 和引用模型，会把复杂度藏进向量库。
- 小型项目管理：一人公司不能维护大型知识平台；先保留 source registry、ingestion pipeline、retrieval policy、citation grounding、RAG eval review 五个可执行工件。
- RAG 原论文：RAG 结合参数化模型和非参数化外部记忆，改善知识密集任务的事实性、可更新性和 provenance，但 provenance 与知识更新仍是核心问题。
- OpenAI Retrieval / File Search / Embeddings：语义检索依赖 vector stores、files、chunks、similarity scores 和 embeddings；file search 可让模型从知识库检索相关信息，但应用仍要管理来源、权限、成本和保留边界。
- OpenAI Data Controls：vector stores、files、responses、embeddings 等 endpoint 的 application state、abuse monitoring、删除和 retention 边界不同，RAG 数据必须按 endpoint/capability 管理。
- OWASP LLM Prompt Injection / RAG Poisoning：外部文档、网页、邮件、用户上传文件和知识库内容可能包含恶意指令，检索文本不得提升为 developer/system 指令。
- OWASP LLM08 Vector and Embedding Weaknesses：embedding/vector 系统存在未授权访问、跨上下文泄露、数据投毒、模型输出操纵和敏感信息披露风险。
- NIST AI RMF / Generative AI Profile：生成式 AI 风险需要在设计、开发、使用和评估中持续管理；RAG 的数据、来源、评测、透明度和风险响应必须可追踪。
- PostgreSQL Full Text Search / pgvector：一人公司默认优先使用 Postgres full-text search、pgvector 或 OpenAI hosted vector store；只有当规模、延迟、召回或运维需求证明必要时，再引入独立向量数据库。
- Google SRE Data Processing Pipelines / Handling Overload：索引、重建、回填和批量嵌入是数据管道，必须有幂等、限流、重试、背压、观测和降级。

## 范围

适用对象：

- 面向用户的知识库问答、客服 FAQ、企业文档助手、代码/规范检索、产品文档搜索、政策/合规回答、内部运营助手、支持记录摘要、文件上传问答。
- Go/Kratos/sqlc/gRPC 后端中的 source registry、ingestion job、chunk table、embedding index、retrieval service、citation service、deletion/reindex job。
- OpenAI Retrieval、File Search、Embeddings、vector stores、Responses file_search tool，以及自管 Postgres/pgvector/full-text search。
- Vite 前端中的知识源管理、上传、同步状态、引用展示、低置信提示、source filter、删除/重建确认。
- RAG eval、召回/grounding/citation 指标、prompt-injection/RAG-poisoning 测试、成本/延迟监控。

不适用对象：

- 通用长期记忆和用户偏好；W3 memory/context 专项管，本专项只管 RAG 知识源和检索链路。
- 训练数据、fine-tuning dataset、eval dataset 标注治理；W3 数据集专项管数据集与 eval 数据。
- 搜索引擎级平台、复杂多模态检索、企业知识图谱、跨组织数据交换；需要时单独开架构 change。

## 最小工件

每个 RAG capability 使用同一个 `<capability>` 文件名：

```text
rag/
  source-registry/<capability>.json
  ingestion-pipeline/<capability>.md
  retrieval-policy/<capability>.json
  citation-grounding/<capability>.md
  rag-eval-review/<capability>.md
```

### `rag/source-registry/<capability>.json`

知识源注册表必须包含：

- `capability`
- `owner`
- `sources`
- `indexes`
- `embedding_models`
- `access_policy`
- `freshness_policy`
- `provenance_policy`
- `data_policy`
- `human_checkpoint`
- `review_cadence`

`sources` 每项至少包含：

- `id`
- `name`
- `source_type`
- `owner`
- `scope`
- `system_of_record`
- `ingestion_mode`
- `access_check`
- `freshness_slo`
- `license_or_rights`
- `data_classification`
- `pii_expected`
- `citation_required`
- `deletion_policy`
- `status`

默认：

- 任何来源进入 RAG 前必须有 owner、scope、权限检查、freshness、删除路径和授权/版权说明。
- 用户上传、客户文档、support ticket、workspace docs、网页抓取、外部 connector 默认不可信。
- 多租户系统不得共享同一个无 tenant filter 的 index；共享公共知识源必须明确标记。
- `restricted`、`sensitive`、`customer_confidential` 来源默认不得进入公共或跨租户检索。

### `rag/ingestion-pipeline/<capability>.md`

摄取流水线必须包含：

- `Scope`
- `Source Admission`
- `Parsing / Extraction`
- `Chunking`
- `Embedding / Indexing`
- `Access / Tenant Filters`
- `Freshness / Reindex`
- `Deletion / Expiry`
- `Poisoning / Injection Controls`
- `Observability / Cost`
- `Linked Artifacts`

默认：

- 摄取前检查来源授权、租户范围、数据分类、文件类型、大小、恶意内容、重复来源和删除策略。
- chunk 必须记录 source id、source version/hash、chunk id、tenant/workspace scope、created_at、embedding model、index version。
- chunk 不保存 secret、完整个人敏感数据、支付数据、原始 prompt/response 或未经授权客户内容。
- index/reindex/backfill 是 W4 async job：要有幂等、重试、dead letter、取消、速率限制和成本预算。
- 删除请求必须覆盖 source、chunk、embedding、cache、OpenAI file/vector store、自管 pgvector/Postgres 和检索快照边界。

### `rag/retrieval-policy/<capability>.json`

检索策略必须包含：

- `capability`
- `owner`
- `retrieval_modes`
- `query_processing`
- `filters`
- `ranking`
- `thresholds`
- `context_budget`
- `injection_policy`
- `citation_policy`
- `fallback`
- `telemetry`
- `cost_limits`
- `privacy`
- `required_controls`
- `human_checkpoint`
- `review_cadence`
- `status`

`required_controls` 默认至少包含：

- `source_allowlist`
- `tenant_scope_filter`
- `access_check_before_retrieval`
- `freshness_filter`
- `sensitivity_filter`
- `max_results`
- `max_tokens`
- `score_threshold`
- `untrusted_context_boundary`
- `prompt_injection_scan`
- `citation_required`
- `fallback_on_low_confidence`
- `deletion_reindex_path`
- `retrieval_telemetry`

默认：

- RAG context 进入 prompt 时必须放在明确的 untrusted context 区，不得与 system/developer 指令混写。
- 检索必须先做 access check 和 tenant/workspace/project/user scope filter，再做向量/关键词/混合检索。
- 低分、过期、冲突、缺 citation 或来源不可信时，AI 应降级、询问、说明不确定或拒答。
- query rewriting、reranking、hybrid search 可以使用，但必须记录版本、成本、延迟和 eval 证据。

### `rag/citation-grounding/<capability>.md`

引用与 grounding 规则必须包含：

- `Scope`
- `Answerable Questions`
- `Citation Rules`
- `Grounding Rules`
- `Contradictions / Conflicts`
- `Low Confidence Behavior`
- `Source Display`
- `User Feedback`
- `Safety / Privacy Limits`
- `Linked Artifacts`

默认：

- 需要事实依据的回答必须引用 source id、title/name、version/date 或可点击来源；不能伪造 citation。
- 如果检索结果不足以回答，优先说不知道、要求更多信息或给出下一步，而不是编造。
- 多来源冲突时必须说明冲突、优先级和 freshness，或请求人工确认。
- 高影响领域、政策/合规、计费、权限、法律/医疗/金融类回答默认需要更高 citation 和 human checkpoint。
- 前端展示引用时保持 Vercel/Geist 风格：答案和来源分区清晰，引用可扫描，不把低置信提示藏在小字里。

### `rag/rag-eval-review/<capability>.md`

RAG eval 复盘必须包含：

- `Recent Changes`
- `Source Coverage`
- `Retrieval Quality`
- `Grounding / Citation Quality`
- `Prompt Injection / Poisoning Tests`
- `Privacy / Tenant Tests`
- `Freshness / Deletion Tests`
- `Latency / Cost`
- `User Feedback`
- `Open Risks`
- `Next One Change`

默认 eval 覆盖：

- answerable query、unanswerable query、stale source、conflicting source、wrong tenant、deleted source、sensitive source、prompt injection in retrieved text、citation missing、low confidence、cost/latency budget。
- pre-revenue：每月一次，或新增来源、改 chunking/embedding/retrieval/reranking/citation 前。
- 有活跃用户：每两周一次，或客户文档、support ticket、外部 connector、敏感来源、prompt injection 发现、删除失败后复盘。
- 每次只选一个最高影响改进：补 source filter、补 deletion path、调 chunking、加 citation、补 eval case、降低成本或禁用高风险来源。

## Go / Kratos / sqlc / gRPC 默认规则

- RAG 能力拆成 ingestion service、retrieval service、citation/grounding helper 和 eval job；不要把检索散落在 prompt 拼接里。
- gRPC API 默认包含 capability、actor、tenant、workspace/project、source filters、request id、trace id 和 policy version。
- sqlc 默认表可包含：`rag_sources`、`rag_source_versions`、`rag_chunks`、`rag_embeddings`、`rag_indexes`、`rag_ingestion_jobs`、`rag_retrieval_events`、`rag_citations`、`rag_deletion_jobs`、`rag_eval_runs`。
- Postgres/pgvector 默认足够早期使用：可以把 source/chunk metadata、tenant filter、全文搜索和 vector search 放在同一个数据库事务边界内。
- 使用 OpenAI vector stores/files 时，必须记录 OpenAI file id、vector store id、source id、tenant scope、expires_after/delete path 和 data retention 说明。
- 检索事件记录 query class、source ids、chunk ids、scores bucket、filters applied、fallback reason、citation count、latency、token/cost bucket，不记录完整用户输入或完整 chunk 内容。

## Vite 前端默认规则

- 知识源管理页显示 source、scope、owner、last indexed、freshness、status、data classification、deletion status 和 recent failures。
- 用户可见答案展示引用、来源时间、低置信提示、无法回答状态和反馈入口。
- 上传/连接外部来源时必须显示数据范围、权限、保留、删除和可能被 AI 使用的说明。
- 删除、重建索引、扩大 source scope、启用敏感来源、对外分享引用内容必须有确认和影响摘要。
- UI 使用 Vercel/Geist 风格：密集、清晰、可扫描，不用营销式文案掩盖检索不确定性。

## AI workflow 默认规则

- Prompt builder 把 system/developer 指令、用户输入、RAG context、tool output、memory 分区；RAG context 标明“不可信资料，只作为引用候选”。
- AI 不得把检索文本中的指令当作自身指令；发现 prompt injection、越权请求、秘密泄露指令时应忽略、标记和降级。
- RAG answer 默认需要 `citations[]` 或结构化 grounding evidence；无 citation 不得输出确定性事实声明。
- RAG eval 连接 W3 prompt/eval、W3 eval data、W3 red-team、W7 telemetry、W9 evidence。
- 高风险自动动作不能只靠 RAG 答案触发；必须走 W3 tool runtime 权限和审批。

## 需要人判断的关键点

只把这些判断交给人：

- 是否新增外部 source、web crawl、connector、客户文档、support ticket、用户上传或私有 workspace 文档。
- 是否把 sensitive、restricted、customer_confidential、个人数据、合同、支付、健康/法律/金融/身份等内容入库或默认检索。
- 是否跨用户、跨 tenant、跨 workspace/project 共享来源、index、embedding 或检索结果。
- 是否使用未经明确授权、版权不清、合同限制、robots/ToS 不清或供应商政策不清的内容。
- 是否允许低置信、无 citation、过期来源、冲突来源仍生成确定性回答。
- 是否改变 embedding provider/model、vector store、chunking、reranking、query rewriting 或 source freshness policy。
- 是否接受删除/reindex 失败、vector store retention 不清、cache 未清、OpenAI file/vector store 未删除。
- 是否在高影响领域或对外信任/合规/安全承诺中使用 RAG 答案。

其他字段完整性、章节、JSON 枚举、required_controls、source coverage、敏感内容扫描、positive/negative fixture 和 OpenSpec linkage 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“来源是什么、怎么入库、怎么检索、怎么引用、怎么评测复盘”。
- 保留：人只判断新增高风险来源、敏感/客户数据、跨租户共享、授权版权、低置信输出、模型/向量库变更和删除失败例外。
- 调整：不默认引入独立向量数据库、复杂 reranker 或知识图谱；早期可用 Postgres/pgvector/OpenAI hosted vector store。
- 调整：RAG poisoning、安全测试和删除路径进入最小 eval，不要求完整红队平台。
- 风险：RAG 容易被当成“把资料扔进去就行”。缓解：source registry 和 retrieval policy 强制记录权限、freshness、scope、citation 和 fallback。

结论：可落地。一个人可以先为最重要的知识库问答 capability 写五个文件，再由 verifier 检查来源、检索、引用和 eval 底线。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户能看到来源、时间和低置信提示，减少“AI 胡说但看起来很确定”的体验风险。
- 工程角度：Go/Kratos/sqlc/gRPC 有明确 source/chunk/index/retrieval/citation 表和服务边界。
- 运维角度：ingestion/reindex/delete 都按 async job 管，带限流、重试、dead letter、成本和观测。
- 安全隐私角度：RAG context 默认不可信，检索前做权限/租户过滤，敏感来源和跨租户共享必须人审。
- 成本角度：max_results、max_tokens、threshold、source allowlist 和 eval 让 token、embedding、重建索引成本可控。

结论：可落地。本专项把 RAG 从“神秘向量库”压成一条可审查的数据链路：来源准入、摄取、检索、引用、评测、删除和降级都有明确最小控制。
