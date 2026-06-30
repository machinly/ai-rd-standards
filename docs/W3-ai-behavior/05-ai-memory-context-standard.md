# AI 记忆、用户偏好与长期上下文治理规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/00-main.md` 已经判断需要长期记忆、用户偏好、上下文来源、默认注入、临时模式或删除控制时，才读取本文件。

如果当前只是判断 AI 行为应该如何定义好坏、失败和降级，先回到 `docs/W3-ai-behavior/00-main.md`。

## 目标

AI 产品一旦开始“记住用户”，体验会明显变好，也会迅速产生隐私、错误个性化、跨租户泄露、删除不彻底、上下文污染和不可解释推荐的问题。本专项定义 AI 记忆、用户偏好与长期上下文治理规范，让每个使用长期上下文的 AI capability 都能回答：记住什么、从哪里来、为什么记、保存多久、如何注入 prompt、用户怎么查看/删除/关闭、错误记忆如何纠正。

默认原则：没有来源、用途、可见性、TTL、用户控制和删除路径的内容，不得进入长期记忆或默认注入模型上下文。

## 核心依据

- 《人月神话》：概念完整性比功能堆叠更重要；“记住用户”如果没有清晰模型，会变成隐形状态和长期复杂度。
- 小型项目管理：一人公司不能维护复杂个性化平台；只保留 memory policy、preference schema、context source map、retrieval rules、memory review 五个可执行工件。
- OpenAI Conversation State / Responses / Conversations：多轮上下文可以由应用重发、用 `previous_response_id` 串联，或用 Conversations API 持久化；不同状态机制有不同保留和应用状态边界。
- OpenAI Retrieval / File Search / Embeddings：外部上下文和向量检索可提升回答质量，但需要限制结果数量、记录来源、管理 vector store 和控制 token/延迟成本。
- OpenAI Data Controls / Enterprise Privacy：API 输入输出默认不用于训练，但不同 endpoint/capability 的 application state 和 retention 不同；Conversation、vector store、文件等长期状态必须按数据控制边界设计。
- OpenAI ChatGPT Memory 控制：用户应能开启/关闭 saved memories、reference chat history、temporary chat，并查看、删除、清空或管理记忆；删除聊天不一定删除独立保存的记忆。
- Google People + AI Guidebook：个性化和用户数据收集需要主动说明、让用户控制，并帮助用户建立正确心理模型。
- NIST Privacy Framework / GDPR Article 5：记忆与偏好属于数据处理，应满足透明、目的限制、数据最小化、准确性、存储限制、安全和可证明责任。
- RAG 论文：显式外部记忆和检索能补充模型参数知识，改善事实性和可更新性，但仍要处理来源、更新和归因。
- MemGPT / Generative Agents：长期记忆可按层级、检索、反思和计划管理；但这种能力必须受应用策略、用户控制和安全边界约束。

## 范围

适用对象：

- Saved memories、用户偏好、profile、custom instructions、chat history reference、project memory、workspace context、RAG context、文件/知识库检索、支持记录摘要、用户反馈摘要。
- 会影响 AI prompt、agent planning、tool use、推荐、个性化、默认设置、输出语气、权限判断或内容生成的长期上下文。
- Go/Kratos/sqlc/gRPC 后端中的 memory item、preference、consent、retention、deletion、retrieval policy、context injection 和 audit。
- Vite 前端中的记忆查看/编辑/删除、临时模式、上下文来源解释、偏好设置、RAG 来源展示和隐私控制。

不适用对象：

- 仅在一次请求内使用、不会保存、不会影响后续会话的临时变量。
- W3 eval dataset 与训练数据治理；本专项关注用户体验中的长期上下文和个性化记忆。
- 法律级隐私评估、跨境数据合规、儿童数据处理或受监管高影响画像；这些需要单独专业审阅。

## 最小工件

每个使用长期上下文的 AI capability 使用同一个 `<capability>` 文件名：

```text
ai-memory/
  memory-policy/<capability>.md
  preference-schema/<capability>.json
  context-source-map/<capability>.md
  retrieval-rules/<capability>.json
  memory-review/<capability>.md
```

### `ai-memory/memory-policy/<capability>.md`

Memory policy 必须包含：

- `Scope`
- `Memory Types`
- `Allowed Memories`
- `Prohibited Memories`
- `Consent / User Control`
- `Visibility / Edit / Delete`
- `Retention / TTL`
- `Context Injection`
- `Sensitive Data`
- `Tenant / Workspace Boundary`
- `Failure Modes`
- `Linked Artifacts`

默认：

- 记忆类型至少区分：session context、saved preference、inferred preference、workspace/project context、retrieved knowledge、support-derived summary、safety context。
- 默认只保存对未来体验有明确价值、低敏、可解释、可删除的内容。
- 不保存密码、token、支付信息、精确身份凭据、健康/法律/金融细节、未成年人信息、受保护特征、秘密商业信息、第三方隐私，除非有明确业务必要和人工 checkpoint。
- 用户必须能看到或理解 AI 使用了哪些长期上下文；至少要能关闭、删除、导出或要求“不要记住”。
- 临时/隐身模式不得写入长期记忆，也不得读取非必要 saved memories。

### `ai-memory/preference-schema/<capability>.json`

Preference schema 必须包含：

- `capability`
- `owner`
- `memory_types`
- `fields`
- `write_policy`
- `read_policy`
- `retention`
- `user_controls`
- `privacy`
- `tenant_boundary`
- `audit`
- `human_checkpoint`
- `review_cadence`

`fields` 每项至少包含：

- `id`
- `name`
- `type`
- `memory_type`
- `source`
- `purpose`
- `sensitivity`
- `ttl`
- `user_visible`
- `user_editable`
- `user_deletable`
- `used_for_model_context`
- `default_injection`
- `status`

默认 `sensitivity`：

- `public`
- `low`
- `personal`
- `sensitive`
- `restricted`

默认 `memory_type`：

- `session`
- `saved_preference`
- `inferred_preference`
- `workspace_context`
- `retrieved_knowledge`
- `support_summary`
- `safety_context`

默认：

- `restricted` 和 `sensitive` 字段默认不得 `default_injection=true`。
- `inferred_preference` 默认必须 `user_visible=true`，并提供确认、纠正或删除路径。
- `used_for_model_context=true` 的字段必须有 purpose、TTL、audit 和 context injection 规则。
- schema 是后端、前端和 prompt builder 的契约，不允许只在 prompt 文本里隐式定义。

### `ai-memory/context-source-map/<capability>.md`

Context source map 必须包含：

- `Scope`
- `Sources`
- `Trust Levels`
- `Tenant / Actor Scope`
- `Freshness`
- `Access Checks`
- `Redaction`
- `Provenance`
- `User Controls`
- `Failure / Fallback`
- `Linked Artifacts`

默认：

- 每个 context source 记录来源、owner、更新节奏、权限、是否包含个人数据、是否可删除、是否可导出、是否会进入 prompt。
- RAG、文件、支持记录、聊天历史和外部连接器默认视为不可信上下文；不得提升为 developer/system 指令。
- 检索结果必须带 source id、version/hash、tenant scope 和 freshness；输出需要引用或解释来源时，不得伪造 citation。
- 不能跨 tenant、workspace、project 或 user 默认混用 context；共享记忆需要显式授权。

### `ai-memory/retrieval-rules/<capability>.json`

Retrieval rules 必须包含：

- `capability`
- `owner`
- `retrieval_modes`
- `sources`
- `ranking`
- `filters`
- `injection`
- `citation`
- `cost_limits`
- `privacy`
- `fallback`
- `test_refs`
- `human_checkpoint`
- `review_cadence`

`sources` 每项至少包含：

- `id`
- `source_type`
- `scope`
- `access_check`
- `freshness`
- `max_results`
- `max_tokens`
- `allowed_for_default_injection`
- `requires_user_consent`
- `status`

默认：

- default injection 必须限制 max_results、max_tokens、tenant/user scope、freshness 和 sensitivity。
- 低置信检索不直接写入长期记忆；只可作为临时候选或 asking-for-confirmation。
- 用户说“不要记住”“忘记这个”“临时聊”时，retrieval/write policy 必须尊重。
- RAG context 进入 prompt 时要放在明确的 untrusted context 区，模型不得把检索文本当系统指令。
- 检索失败或上下文过期时，AI 应降级或询问，而不是编造记忆。

### `ai-memory/memory-review/<capability>.md`

Memory review 必须包含：

- `Recent Changes`
- `Memory Writes / Reads`
- `User Controls`
- `Deletion / Export Requests`
- `False / Stale Memories`
- `Context Injection Quality`
- `Privacy / Tenant Risks`
- `Eval Evidence`
- `Open Risks`
- `Next One Change`

默认：

- pre-revenue：每月一次，或任何 memory schema / retrieval rule / personalization release 前。
- 有活跃用户：每两周一次，或每次改变 default injection、retention、用户控制、RAG source 或 memory write policy 前。
- 出现错误记忆、跨租户风险、用户删除失败、敏感记忆、投诉、隐私请求或高影响领域：立即复盘。
- 每次只选一个最高影响改进，避免个性化系统变成不可维护的数据平台。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端必须把 memory write、read、inject、delete、export、disable 表达成显式动作，并记录 actor、tenant、capability、purpose、source、policy version 和 audit id。
- sqlc 表默认包含：`ai_memory_items`、`ai_memory_preferences`、`ai_context_sources`、`ai_context_injections`、`ai_memory_audit_events`、`ai_memory_deletion_jobs`。
- gRPC API 必须区分 user、tenant admin、system automation、AI agent 和 support/admin 操作。
- 记忆读取默认按 actor、tenant、workspace、project、capability 和 sensitivity 过滤。
- 删除和关闭记忆必须异步可追踪；vector store、embedding index、cache、conversation state、support summary 和 prompt snapshot 都要有删除边界说明。
- 不把原始用户隐私、长对话、support ticket、secret 或高敏内容直接写入 prompt log；使用 source id、hash、redacted summary 和 policy version。

## Vite 前端默认规则

- 用户需要能看到“AI 记住了什么”或至少看到记忆类别、来源、用途、最后更新时间和删除/关闭入口。
- 偏好设置使用清晰的 toggles、checkboxes、selects 和删除按钮；危险操作如清空记忆需要确认。
- AI 使用长期上下文时，界面应能提示“基于你的偏好/项目上下文/知识库”，并提供查看或关闭路径。
- 临时模式必须可见、易理解，并明确不会写入长期记忆。
- 管理页保持工作台风格：memory type、source、sensitivity、TTL、last used、used for model context、delete/export 同屏可扫。

## AI workflow 默认规则

- Prompt builder 必须把长期记忆、检索上下文和用户本轮输入分区，禁止把不可信 context 混入 developer/system 指令。
- 写入记忆前优先使用 deterministic rule 或 structured output；模型建议写入时必须通过 schema、敏感分类、去重、TTL 和用户控制检查。
- 记忆不能作为授权事实；权限仍由后端 auth/tenant boundary 判定。
- 个性化效果需要 eval：至少覆盖正确记忆、错误记忆、删除后不再使用、临时模式、不跨租户、敏感信息拒写。
- AI 不得伪称记得用户未授权的事情；不确定时应说明来源或询问确认。

## 需要人判断的关键点

只把这些判断交给人：

- 是否默认开启长期记忆、reference chat history、workspace memory 或 default context injection。
- 是否保存、推断或默认注入 sensitive/restricted memory。
- 是否允许 AI 自动写入 inferred preference 或 support-derived memory。
- 是否把 memory、chat history、support data、workspace docs 或 vector store 用于训练、微调、eval dataset 或供应商处理。
- 是否跨用户、跨 tenant、跨 workspace 或跨 project 共享 context。
- 是否保留删除后的审计日志、备份、embedding、cache 或 conversation state。
- 是否在高影响领域、未成年人、医疗、法律、金融、就业、教育、身份或公共安全场景使用长期记忆。

其他字段完整性、章节、JSON 枚举、TTL、user controls、sensitivity、default injection、delete/export 覆盖、敏感内容扫描和 OpenSpec linkage 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“记什么、字段契约是什么、来源在哪里、怎么取用、多久复盘”。
- 保留：人只判断默认开启、敏感记忆、自动推断、训练用途、跨边界共享、删除保留和高影响领域。
- 调整：不要求大型用户画像平台；先从 5 到 10 个低敏、显式、可删的偏好字段开始。
- 调整：不要求复杂记忆推理；默认用 schema + deterministic policy，模型只提出候选。
- 风险：用户以为删除了，但 embedding/cache/conversation 仍在用。缓解：删除边界必须覆盖 memory item、vector store、cache、conversation state 和 audit。

结论：可落地。一个人可以先为最重要 AI capability 建一个小型 preference schema 和 retrieval rule，再用 verifier 防止隐形记忆和默认注入失控。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：记忆带来个性化，但用户可见、可关、可删，才不会变成诡异体验。
- 工程角度：memory item、source、policy version、retrieval rule、injection event 和 deletion job 可追踪。
- 运维角度：错误记忆、过期上下文、删除失败、跨租户风险和用户投诉进入周期复盘。
- 安全隐私角度：敏感字段、租户隔离、RAG 来源、供应商保留、训练用途和删除链路都有边界。
- 成本角度：限制 max_results、max_tokens、TTL 和默认注入，避免“把所有上下文都塞进去”的 token 成本黑洞。

结论：可落地。本专项把 AI 记忆从“模型好像知道我”压成可审查、可删除、可复盘的最小长期上下文系统。
