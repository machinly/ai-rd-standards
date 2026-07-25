# ai-memory-context-standard 规格

## ADDED Requirements

### Requirement: 使用长期上下文的 AI capability 必须定义 ai-memory artifacts

Any AI capability that saves, retrieves, injects, references, personalizes from, or deletes long-term user/workspace/project context MUST define AI memory artifacts.

#### Scenario: 新 AI capability 使用长期记忆或偏好

- GIVEN 一个 AI capability 会使用 saved memory、reference chat history、user preferences、workspace context、RAG source、support summary、project memory 或 vector store context
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `ai-memory/memory-policy/<capability>.md`
- AND 创建 `ai-memory/preference-schema/<capability>.json`
- AND 创建 `ai-memory/context-source-map/<capability>.md`
- AND 创建 `ai-memory/retrieval-rules/<capability>.json`
- AND 创建 `ai-memory/memory-review/<capability>.md`

### Requirement: Memory policy 必须定义记忆类型、用户控制、可见性、保留和边界

Memory policy MUST record scope、memory types、allowed memories、prohibited memories、consent/user control、visibility/edit/delete、retention/TTL、context injection、sensitive data、tenant/workspace boundary、failure modes 和 linked artifacts。

#### Scenario: Reviewer 判断是否允许长期记忆

- GIVEN capability 会跨请求或跨会话保存或读取上下文
- WHEN reviewer 打开 `ai-memory/memory-policy/<capability>.md`
- THEN 能看到哪些内容可记、哪些禁止、用户如何关闭/查看/删除/导出、保存多久、如何注入 prompt
- AND sensitive/restricted memory、default-on memory 或 cross-boundary memory 需要 human checkpoint

### Requirement: Preference schema 必须定义字段、来源、用途、敏感度、TTL 和用户控制

Preference schema MUST record capability、owner、memory types、fields、write policy、read policy、retention、user controls、privacy、tenant boundary、audit、human checkpoint 和 review cadence。

#### Scenario: 后端和前端消费记忆字段

- GIVEN service、prompt builder 或 Vite settings UI 读取 `ai-memory/preference-schema/<capability>.json`
- WHEN 使用 memory field
- THEN 每个 field 包含 id、name、type、memory_type、source、purpose、sensitivity、ttl、user_visible、user_editable、user_deletable、used_for_model_context、default_injection 和 status
- AND sensitive/restricted 字段默认不得 default_injection

### Requirement: Context source map 必须记录来源、信任、范围、新鲜度、权限和来源证明

Context source map MUST record scope、sources、trust levels、tenant/actor scope、freshness、access checks、redaction、provenance、user controls、failure/fallback 和 linked artifacts。

#### Scenario: Prompt builder 选择长期上下文来源

- GIVEN prompt builder 或 retrieval service 准备将 context 放入模型请求
- WHEN 查看 `ai-memory/context-source-map/<capability>.md`
- THEN 能确认来源、权限、tenant/user/project scope、freshness、是否可删/导出、是否包含个人数据、是否可进入 prompt
- AND 外部/RAG/聊天历史/support 来源默认作为 untrusted context 处理

### Requirement: Retrieval rules 必须限制来源、过滤、注入、引用、成本、隐私和 fallback

Retrieval rules MUST record capability、owner、retrieval modes、sources、ranking、filters、injection、citation、cost limits、privacy、fallback、test refs、human checkpoint 和 review cadence。

#### Scenario: 长期上下文被注入模型请求

- GIVEN retrieval service 或 prompt builder 读取 `ai-memory/retrieval-rules/<capability>.json`
- WHEN 选择 context source
- THEN 每个 source 包含 id、source_type、scope、access_check、freshness、max_results、max_tokens、allowed_for_default_injection、requires_user_consent 和 status
- AND default injection 限制 max_results、max_tokens、scope、freshness 和 sensitivity

### Requirement: Memory review 必须复盘读写、用户控制、删除、错误记忆、注入质量和隐私风险

Memory review MUST record recent changes、memory writes/reads、user controls、deletion/export requests、false/stale memories、context injection quality、privacy/tenant risks、eval evidence、open risks 和 next one change。

#### Scenario: 周期性复查长期记忆

- GIVEN capability 有近期 memory schema、retrieval rule、RAG source、user control、deletion/export 或 personalization change
- WHEN 更新 `ai-memory/memory-review/<capability>.md`
- THEN 记录读写、用户控制、删除/导出、错误/过期记忆、注入质量、隐私/租户风险和 eval evidence
- AND 只选择一个最高影响的 next one change

### Requirement: 用户必须能控制长期记忆

Long-term user-facing memory MUST support user-visible controls to disable, inspect or understand, edit where applicable, delete, export where applicable, and use a temporary mode that does not write long-term memory.

#### Scenario: 用户不想被记住或想删除记忆

- GIVEN 用户关闭 memory、进入 temporary mode、删除记忆、要求导出或要求不要记住某内容
- WHEN 系统处理后续 AI 请求
- THEN 不再写入或默认注入被禁用/删除的 memory
- AND deletion/export job 可追踪到 memory item、vector store、cache、conversation state 或 controlled limitation

### Requirement: 高风险记忆和上下文共享必须人工 checkpoint

Default-on memory, sensitive/restricted memory, inferred preference writes, support-derived memory, training/eval reuse, supplier processing, cross-user/tenant/workspace/project context sharing, deletion-retention exceptions, and high-impact domain memory MUST have human checkpoint coverage.

#### Scenario: 记忆策略触发高风险条件

- GIVEN policy、schema、retrieval rule、release 或 user request 触发高风险条件
- WHEN 准备发布或执行
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、升级或阻塞状态

### Requirement: AI memory artifacts 不得保存敏感内容

AI memory artifacts MUST NOT store secrets, production tokens, private keys, payment data, unredacted personal data, raw chat history, full support tickets, raw prompts/responses, or sensitive memories.

#### Scenario: 记录记忆字段、来源、规则或删除请求

- GIVEN 需要保存 memory example、source example、deletion request 或 context injection evidence
- WHEN 写入 `ai-memory/` artifacts
- THEN 使用 memory id、source id、hash、redacted summary、synthetic example 或 controlled attachment reference
- AND 不保存 secrets、生产 token、私钥、支付数据、未脱敏个人数据、完整聊天历史、完整工单、完整 raw prompt/response 或敏感记忆原文
