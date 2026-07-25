# rag-retrieval-source-standard 规格

## ADDED Requirements

### Requirement: 生产 RAG capability 必须定义 rag artifacts

Any production capability that retrieves external knowledge, uploaded files, vector store chunks, keyword search results, support records, customer documents, workspace documents, code/docs, policy pages, web crawl content, or connector data for AI answer generation MUST define RAG artifacts.

#### Scenario: 新 RAG capability 准备进入生产

- GIVEN 一个 capability 会把检索结果注入 AI prompt 或用检索结果生成用户可见答案
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `rag/source-registry/<capability>.json`
- AND 创建 `rag/ingestion-pipeline/<capability>.md`
- AND 创建 `rag/retrieval-policy/<capability>.json`
- AND 创建 `rag/citation-grounding/<capability>.md`
- AND 创建 `rag/rag-eval-review/<capability>.md`

### Requirement: Source registry 必须定义 source、index、embedding、权限、freshness、provenance、数据策略和人工 checkpoint

Source registry MUST record capability、owner、sources、indexes、embedding models、access policy、freshness policy、provenance policy、data policy、human checkpoint 和 review cadence.

#### Scenario: Reviewer 判断知识源能否入库

- GIVEN reviewer 打开 `rag/source-registry/<capability>.json`
- WHEN 需要理解 RAG 来源
- THEN 每个 source 包含 id、name、source_type、owner、scope、system_of_record、ingestion_mode、access_check、freshness_slo、license_or_rights、data_classification、pii_expected、citation_required、deletion_policy 和 status
- AND sources 有 owner、scope、权限检查、freshness、删除路径和授权/版权说明
- AND sensitive/restricted/customer_confidential 来源不会进入公共或跨租户检索

### Requirement: Ingestion pipeline 必须定义 source admission、parsing、chunking、embedding/indexing、tenant filter、freshness、deletion、poisoning control、observability 和 linked artifacts

Ingestion pipeline MUST record scope、source admission、parsing/extraction、chunking、embedding/indexing、access/tenant filters、freshness/reindex、deletion/expiry、poisoning/injection controls、observability/cost 和 linked artifacts.

#### Scenario: 来源被摄取、重建或删除

- GIVEN 新文档、更新文档、删除请求、reindex、backfill 或 hosted vector store sync
- WHEN ingestion pipeline 执行
- THEN chunk metadata 记录 source id、source version/hash、chunk id、tenant/workspace scope、created_at、embedding model 和 index version
- AND indexing/reindex/backfill 作为 async job 处理幂等、重试、dead letter、取消、速率限制和成本预算
- AND 删除路径覆盖 source、chunk、embedding、cache、OpenAI file/vector store、自管 pgvector/Postgres 和检索快照边界

### Requirement: Retrieval policy 必须定义 retrieval mode、query processing、filter、ranking、threshold、context budget、injection policy、citation policy、fallback、telemetry、cost、privacy 和 required controls

Retrieval policy MUST record capability、owner、retrieval modes、query processing、filters、ranking、thresholds、context budget、injection policy、citation policy、fallback、telemetry、cost limits、privacy、required controls、human checkpoint、review cadence 和 status.

#### Scenario: 用户请求触发 RAG 检索

- GIVEN 用户请求需要检索知识源
- WHEN retrieval service 执行检索
- THEN 在向量/关键词/混合检索前执行 access check、tenant/workspace/project/user scope filter、source allowlist、freshness filter 和 sensitivity filter
- AND required_controls 至少包含 source_allowlist、tenant_scope_filter、access_check_before_retrieval、freshness_filter、sensitivity_filter、max_results、max_tokens、score_threshold、untrusted_context_boundary、prompt_injection_scan、citation_required、fallback_on_low_confidence、deletion_reindex_path 和 retrieval_telemetry
- AND 低分、过期、冲突、缺 citation 或来源不可信时走 fallback、询问、说明不确定或拒答

### Requirement: Citation grounding 必须定义可回答范围、引用规则、grounding、冲突、低置信行为、来源展示、反馈、安全隐私限制和关联工件

Citation grounding rules MUST record scope、answerable questions、citation rules、grounding rules、contradictions/conflicts、low confidence behavior、source display、user feedback、safety/privacy limits 和 linked artifacts.

#### Scenario: AI 生成 RAG 答案

- GIVEN 模型准备生成需要事实依据的回答
- WHEN RAG context 不足、来源冲突、来源过期、缺少 citation 或检索命中低置信
- THEN 模型不得输出确定性事实声明
- AND 输出必须引用 source id、title/name、version/date 或可点击来源
- AND 无法回答时说明不知道、请求更多信息、给出下一步或降级

### Requirement: RAG eval review 必须覆盖 source coverage、retrieval quality、grounding/citation、poisoning、privacy/tenant、freshness/deletion、latency/cost、feedback、risk 和下一项改进

RAG eval review MUST record recent changes、source coverage、retrieval quality、grounding/citation quality、prompt injection/poisoning tests、privacy/tenant tests、freshness/deletion tests、latency/cost、user feedback、open risks 和 next one change.

#### Scenario: 周期性复查 RAG 质量和安全

- GIVEN capability 新增来源、改变 chunking、embedding、retrieval、reranking、citation、freshness、删除策略或用户反馈显示 RAG 错误
- WHEN 更新 `rag/rag-eval-review/<capability>.md`
- THEN eval 覆盖 answerable query、unanswerable query、stale source、conflicting source、wrong tenant、deleted source、sensitive source、prompt injection in retrieved text、citation missing、low confidence、cost/latency budget
- AND 每次只选择一个最高影响的 next one change

### Requirement: 高风险 RAG 变更必须人工 checkpoint

New external/private sources, sensitive/customer data indexing, cross-tenant sharing, unclear content rights, low-confidence factual answers, embedding/vector-store changes, deletion/reindex exceptions, and high-impact RAG output MUST have human checkpoint coverage.

#### Scenario: RAG 触发高风险条件

- GIVEN source registry、ingestion pipeline、retrieval policy、citation grounding、RAG eval review 或 release 触发高风险条件
- WHEN 准备发布、导入、共享、导出、删除、保留或接受例外
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、阻塞、降级、删除计划或专业审阅需求

### Requirement: RAG artifacts 不得保存敏感内容

RAG artifacts MUST NOT store secrets, production tokens, API keys, OAuth refresh tokens, private keys, session cookies, database connection strings, payment data, raw prompts, raw responses, raw tool outputs, raw document text, full chunks, raw provider payloads, unredacted personal data, customer confidential content, or executable attack payloads.

#### Scenario: 记录 source、chunk、检索、citation、eval 或 poisoning case

- GIVEN 需要保存 source example、chunk example、retrieval event、citation evidence、eval case、poisoning finding 或 deletion evidence
- WHEN 写入 `rag/` artifacts
- THEN 使用 synthetic example、redacted summary、source id、chunk id、document hash、trace id、request id、eval case id、finding id 或 controlled attachment reference
- AND 不保存 secret、production token、API key、OAuth refresh token、private key、session cookie、数据库连接串、支付数据、原始 prompt/response/tool output、raw document text、完整 chunk、raw provider payload、未脱敏个人数据、客户机密内容或可直接执行的攻击 payload
