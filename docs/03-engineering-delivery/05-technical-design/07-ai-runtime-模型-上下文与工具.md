# 技术设计：AI runtime、模型、上下文与工具

## 规范要求

<!-- rule-id: TECH-258-USER-VISIBLE-AI-SAFETY-GATE -->
- 缺少安全边界的用户可见 AI 能力禁止进入实现或发布。

<!-- rule-id: TECH-149-AI-EXTERNAL-CLAIM-BOUNDARY -->
- AI 处理外部文案时，禁止自行发布、扩写或强化 external claim。

<!-- rule-id: TECH-149-AI-CLAIM-CORRECTION-PUBLISH-BOUNDARY -->
- AI 发现 claim 冲突时，禁止自动发布 claim correction。

<!-- rule-id: TECH-234-AI-QUALITY-ROUTING-BOUNDARY -->
- 仅定义 AI 好坏、失败或降级时，由 AI 技术设计总入口继续分流。

<!-- rule-id: TECH-201-DETERMINISTIC-AI-WORKFLOW -->
- AI workflow 优先考虑确定性编排。

<!-- rule-id: TECH-026-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：采集前端事件时。表单、prompt、自由文本、URL、文件名和直接标识禁止进入事件属性。

<!-- rule-id: TECH-014-AI-MODEL-ROUTING-S01 -->
- 适用情形：变更引入所列长期义务时。长期架构、关键供应商、出境、DPA、训练保留或显著成本须交由人工判断。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S01 -->
- 适用情形：组织 Go/Kratos 服务时。internal/biz 禁止 import data、transport、SQL driver 或 model vendor SDK。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S02 -->
- 适用情形：考虑拆分服务时。只在数据、发布、可靠性或供应商安全边界明确时拆服务。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S03 -->
- 适用情形：组织 AI 依赖时。AI model/vendor SDK 不纳入 domain/biz 层。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S05 -->
- 适用情形：考虑所列依赖时。引入新框架、供应商 SDK、agent runtime 或公共组件库须交由人工判断。

<!-- rule-id: TECH-028-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：处理 secret 时。secret 禁止进入仓库、日志或 prompt。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S01 -->
- 适用情形：当前 change 命中所列风险时。只在 change 涉及成本、客户数据、供应商、出境、IP、AI 内容或承诺时读取本专项。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S03 -->
- 适用情形：供应商缺少所列保障时。接受缺少关键条款或数据边界的供应商须交由人工判断。

<!-- rule-id: TECH-028-AI-PROMPT-ARTIFACT-S02 -->
- 适用情形：change 涉及 AI 工具或输入输出时。AI 安全须覆盖AI prompt injection。

<!-- rule-id: TECH-047-AI-SENSITIVE-DISCLOSURE-SAFETY-S01 -->
- 适用情形：change 涉及 AI 工具或输入输出时。AI 安全须覆盖敏感信息泄露。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S07 -->
- 适用情形：设计 AI 成本容量时。供应商调用须有上限。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S09 -->
- 适用情形：调用供应商时。供应商调用须具备：disable switch、数据最小化。

<!-- rule-id: TECH-018-AI-MODEL-ROUTING-S01 -->
- 适用情形：判断 AI 技术设计 适用范围时。模型路由变化纳入 AI 技术设计。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S01 -->
- 适用情形：决定 AI 自治等级时。上线 autonomous agent 须由人工判断。

<!-- rule-id: TECH-018-AI-MODEL-ROUTING-S03 -->
- 适用情形：规划模型优化时。模型优化前先确认数据边界。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S02 -->
- 适用情形：实现新 AI 能力时。新 AI 能力缺省使用 deterministic workflow 或单次 Responses API 调用，不默认采用 autonomous agent。

<!-- rule-id: TECH-051-AI-TOOL-LEAST-PRIVILEGE-S01 -->
- 适用情形：定义 AI 工具调用时。工具调用缺省最小权限。

<!-- rule-id: TECH-052-AI-TOOL-NECESSITY-S01 -->
- 适用情形：接入 AI 工具时。仅真实需要外部数据或副作用时添加工具。

<!-- rule-id: TECH-003-AI-AGENT-USE-CASE-S01 -->
- 适用情形：决定是否升级 agent 时。仅有固定 workflow 不足时才考虑升级 agent。

<!-- rule-id: TECH-009-AI-INSTRUCTION-TRUST-BOUNDARY-S01 -->
- 适用情形：处理用户输入时。不可信用户输入只能进入 user/input 数据区，禁止拼入 developer/system 高优先级指令。

<!-- rule-id: TECH-019-AI-MODEL-ROUTING-S01 -->
- 适用情形：选择 AI workflow 层级时。规则或传统代码能解决时不用模型。

<!-- rule-id: TECH-019-AI-MODEL-ROUTING-S02 -->
- 适用情形：选择 AI workflow 层级时。单次模型调用能解决时不用 workflow。

<!-- rule-id: TECH-067-AI-WORKFLOW-PATTERN-SELECTION-S01 -->
- 适用情形：选择 AI workflow 层级时。固定步骤能提升质量时采用 deterministic workflow。

<!-- rule-id: TECH-067-AI-WORKFLOW-PATTERN-SELECTION-S02 -->
- 适用情形：选择 AI workflow 层级时。需要分类分流时采用 routing。

<!-- rule-id: TECH-067-AI-WORKFLOW-PATTERN-SELECTION-S03 -->
- 适用情形：选择 AI workflow 层级时。需要多个独立视角时采用 parallelization。

<!-- rule-id: TECH-003-AI-AGENT-USE-CASE-S02 -->
- 适用情形：选择 AI workflow 层级时。仅步数不可预知且需工具探索恢复时采用 agent。

<!-- rule-id: TECH-069-AI-WORKFLOW-STOP-CHECKPOINT-S01 -->
- 适用情形：升级 AI workflow 时。升级 workflow 须至少有明确停止条件、最大迭代次数或人工 checkpoint 之一。

<!-- rule-id: TECH-068-AI-WORKFLOW-SIDE-EFFECT-CONTROL-S01 -->
- 适用情形：升级 AI workflow 时。升级 workflow 的工具权限和副作用须可审计；升级 workflow 的工具权限和副作用须可回滚或可人工确认。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S01 -->
- 适用情形：定义 AI 工具时。工具名称须清楚。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S02 -->
- 适用情形：定义 AI 工具时。工具参数须清楚。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S03 -->
- 适用情形：定义 AI 工具时。工具描述须清楚。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S05 -->
- 适用情形：定义 AI 工具时。工具参数应避免用自由文本承载指令。

<!-- rule-id: TECH-063-AI-TOOL-SIDE-EFFECT-CONTROL-S01 -->
- 适用情形：定义高风险 AI 工具时。高风险工具缺省 dry-run 或人工批准。

<!-- rule-id: TECH-063-AI-TOOL-SIDE-EFFECT-CONTROL-S02 -->
- 适用情形：定义写操作 AI 工具时。写操作工具须具备：幂等键、审计日志。

<!-- rule-id: TECH-051-AI-TOOL-LEAST-PRIVILEGE-S02 -->
- 适用情形：定义写操作 AI 工具时。写操作工具须有权限检查。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S01 -->
- 适用情形：处理外部工具数据时。外部检索内容须视为不可信输入。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S02 -->
- 适用情形：处理外部工具数据时。网页内容须视为不可信输入。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S03 -->
- 适用情形：处理外部工具数据时。邮件内容须视为不可信输入。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S04 -->
- 适用情形：处理外部工具数据时。用户文件须视为不可信输入。

<!-- rule-id: TECH-066-AI-UNTRUSTED-TOOL-CONTENT-S05 -->
- 适用情形：处理工具返回数据时。工具返回数据禁止直接升级为高优先级指令。

<!-- rule-id: TECH-036-AI-QUALITY-COST-LATENCY-TRADEOFF-S01 -->
- 适用情形：决定 AI 质量取舍时。接受更高成本换质量须由人工判断。

<!-- rule-id: TECH-036-AI-QUALITY-COST-LATENCY-TRADEOFF-S02 -->
- 适用情形：决定 AI 质量取舍时。接受更高延迟换质量须由人工判断。

<!-- rule-id: TECH-199-GOVERNANCE-AI-EVAL-SAFETY-S01 -->
- 适用情形：设计内容审核时。禁止把内容审核缩减为单次分类器调用。

<!-- rule-id: TECH-198-GOVERNANCE-AI-CONTEXT-MEMORY-RETRIEVAL-S01 -->
- 适用情形：应用 AI context 专项时。与本规范的正式分类及项目原则冲突时，以正式规范为准。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S01 -->
- 适用情形：构建 AI 上下文时。长期记忆和 RAG context 须视为不可信外部上下文。

<!-- rule-id: TECH-029-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：构建 AI prompt 时。长期记忆和 RAG context 禁止作为 system/developer 指令。

<!-- rule-id: TECH-020-AI-MODEL-ROUTING-S01 -->
- 适用情形：默认注入长期上下文时。缺少来源的内容禁止默认注入模型。

<!-- rule-id: TECH-020-AI-MODEL-ROUTING-S02 -->
- 适用情形：默认注入长期上下文时。缺少 TTL 的内容禁止默认注入模型。

<!-- rule-id: TECH-020-AI-MODEL-ROUTING-S03 -->
- 适用情形：默认注入长期上下文时。缺少删除路径的内容禁止默认注入模型。

<!-- rule-id: TECH-029-AI-PROMPT-ARTIFACT-S03 -->
- 适用情形：注入 RAG context 时。RAG context 进入 prompt 时须标记 untrusted context。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S04 -->
- 适用情形：注入 RAG context 时。检索文本中的指令禁止提升为模型指令。

<!-- rule-id: TECH-010-AI-MEMORY-CONTEXT-DEFAULTS-S01 -->
- 适用情形：改变 memory 默认时。默认开启长期记忆须由人工判断；默认引用 chat history 须由人工判断；默认启用 workspace memory 须由人工判断。

<!-- rule-id: TECH-010-AI-MEMORY-CONTEXT-DEFAULTS-S02 -->
- 适用情形：改变 retrieval 默认时。默认检索须由人工判断。

<!-- rule-id: TECH-010-AI-MEMORY-CONTEXT-DEFAULTS-S03 -->
- 适用情形：改变 context injection 默认时。default context injection 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S05 -->
- 适用情形：处理敏感上下文时。保存 sensitive/restricted memory 或客户机密来源须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S06 -->
- 适用情形：处理敏感上下文时。推断 sensitive/restricted memory 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S07 -->
- 适用情形：处理敏感上下文时。默认注入 sensitive/restricted memory 或客户机密来源须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S08 -->
- 适用情形：选择 RAG 来源时。使用权利或政策不清的内容须由人工判断。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S03 -->
- 适用情形：处理上下文删除失败时。接受删除失败须由人工判断。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S04 -->
- 适用情形：处理上下文删除失败时。接受 reindex 失败须由人工判断。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S05 -->
- 适用情形：处理上下文删除失败时。接受 vector store retention 清理失败须由人工判断。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S06 -->
- 适用情形：处理上下文删除失败时。接受 cache 清理失败须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S09 -->
- 适用情形：使用高影响上下文时。在医疗领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S10 -->
- 适用情形：使用高影响上下文时。在法律领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S11 -->
- 适用情形：使用高影响上下文时。在金融领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S12 -->
- 适用情形：使用高影响上下文时。在身份领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S13 -->
- 适用情形：使用高影响上下文时。在就业领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S14 -->
- 适用情形：使用高影响上下文时。在教育领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S15 -->
- 适用情形：使用高影响上下文时。在公共安全领域使用记忆或 RAG 须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：应用 AI runtime 专项时。与本规范的正式分类及项目原则冲突时，以正式规范为准。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S01 -->
- 适用情形：决定是否使用 AI runtime 专项时。仅有 AI 技术设计总入口触发模型或工具运行时变化时才使用本专项。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S02 -->
- 适用情形：设计 AI runtime 时。仅有应用运行时拥有执行权。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S02 -->
- 适用情形：改变生产模型、工具或数据边界时。生产 AI runtime 默认变化须有降级路径。

<!-- rule-id: TECH-044-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：生产 AI runtime 默认变化时。生产 AI runtime 默认变化须有回滚或补偿方式。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S03 -->
- 适用情形：调用模型供应商时。request context 须有 deadline。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S04 -->
- 适用情形：处理 runtime secret 时。token、key、cookie 和连接串禁止进入模型上下文。

<!-- rule-id: TECH-033-AI-PROMPT-RUNTIME-CONTRACT-S02 -->
- 适用情形：构建 AI prompt 时。prompt 禁止自行决定供应商；prompt 禁止自行决定权限；prompt 禁止自行决定审批；prompt 禁止自行决定幂等策略；prompt 禁止自行决定租户边界；prompt 禁止自行决定成本上限；prompt 禁止自行决定重试策略。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S03 -->
- 适用情形：实现 autonomous loop 时。autonomous loop须具备：有限步数、有限工具 fanout、有限 token、有限 cost、有限重试。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S04 -->
- 适用情形：loop 超限时。autonomous loop 超限后须降级、转人工或排队。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S05 -->
- 适用情形：改变生产 route 时。改变用户可见生产默认模型须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S06 -->
- 适用情形：改变生产 route 时。改变用户可见生产供应商须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S07 -->
- 适用情形：改变生产 route 时。改变用户可见生产 route 须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S08 -->
- 适用情形：扩大 runtime 供应商时。引入新外部模型供应商须由人工判断。

<!-- rule-id: TECH-043-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：扩大 runtime 集成时。引入新 connector 须由人工判断。

<!-- rule-id: TECH-043-AI-RUNTIME-ROUTING-S02 -->
- 适用情形：扩大 runtime 集成时。引入新 remote MCP server 须由人工判断。

<!-- rule-id: TECH-043-AI-RUNTIME-ROUTING-S03 -->
- 适用情形：扩大 runtime 集成时。引入新本地 MCP server 须由人工判断。

<!-- rule-id: TECH-043-AI-RUNTIME-ROUTING-S04 -->
- 适用情形：扩大 runtime 工具能力时。引入浏览器或电脑控制工具须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S09 -->
- 适用情形：改变 route 数据时。让敏感、监管或高影响数据进入 route 须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S10 -->
- 适用情形：改变供应商数据边界时。扩大供应商或 connector 数据保留边界须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S11 -->
- 适用情形：改变供应商数据边界时。扩大供应商或 connector 数据驻留边界须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S12 -->
- 适用情形：改变供应商数据边界时。扩大供应商或 connector 数据训练边界须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S13 -->
- 适用情形：改变供应商数据边界时。扩大供应商或 connector scope 边界须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S14 -->
- 适用情形：改变 AI 安全 route 时。改变 refusal 或 safety behavior 须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S15 -->
- 适用情形：改变 AI 安全 route 时。改变 moderation route 须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S16 -->
- 适用情形：改变 AI 安全 route 时。改变安全阈值须由人工判断。

<!-- rule-id: TECH-021-AI-MODEL-ROUTING-S17 -->
- 适用情形：改变 AI 工具 route 时。改变 tool-heavy route 须由人工判断。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S05 -->
- 适用情形：改变 AI 自治等级时。改变 agent 自治等级须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S05 -->
- 适用情形：接受 runtime 控制缺口时。接受没有 dry-run 的用户可见 AI 能力须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S06 -->
- 适用情形：接受 runtime 控制缺口时。接受没有幂等的用户可见 AI 能力须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S07 -->
- 适用情形：接受 runtime 控制缺口时。接受没有审计的用户可见 AI 能力须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S08 -->
- 适用情形：扩大 AI runtime 资源时。提高 AI 预算须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S09 -->
- 适用情形：扩大 AI runtime 资源时。扩大 context window 须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S10 -->
- 适用情形：扩大 AI runtime 资源时。默认高 reasoning effort 须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S11 -->
- 适用情形：扩大 AI runtime 资源时。扩大 loop 上限须由人工判断。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S12 -->
- 适用情形：扩大 AI runtime 资源时。扩大 fanout 须由人工判断。

<!-- rule-id: TECH-022-AI-MODEL-ROUTING-S01 -->
- 适用情形：引入外部供应商时。新增模型供应商须由人工判断。

<!-- rule-id: TECH-004-AI-AUTONOMY-BOUNDARY-S06 -->
- 适用情形：授权 AI coding 时。扩大 AI agent 自主权限须由人工判断。

<!-- rule-id: TECH-046-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：设计 runtime 行为时。代码须决定能力边界。

<!-- rule-id: TECH-207-GOVERNANCE-DEV-WORKSPACE-AI-CODING-S01 -->
- 适用情形：使用 AI coding 时。work brief 仅允许承载执行状态。

<!-- rule-id: TECH-023-AI-MODEL-ROUTING-S01 -->
- 适用情形：运行本地 AI workflow 时。本地 AI workflow 缺省使用 dry-run、mock provider 或低成本 sandbox，不默认调用真实模型和真实工具。

<!-- rule-id: TECH-023-AI-MODEL-ROUTING-S02 -->
- 适用情形：使用 AI coding 时。未经人审 AI 禁止访问真实 secret、用户数据、生产数据或真实供应商。

<!-- rule-id: TECH-198-GOVERNANCE-AI-CONTEXT-MEMORY-RETRIEVAL-S02 -->
- 适用情形：决定是否采用该专项时。AI context 专项是可选 playbook，不是缺省流程。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S13 -->
- 适用情形：决定是否采用该专项时。AI runtime 专项是可选 playbook，不是缺省流程。

<!-- rule-id: TECH-030-AI-PROMPT-ARTIFACT-S02 -->
- 适用情形：启用客户数据进入 AI 前。客户数据进入 prompt/RAG/memory/tool action 前须有 data boundary。


## 执行细则

<!-- rule-id: TECH-102-AI-QUALITY-ERROR-CATEGORIES -->
- AI quality 的 gRPC status/error model 须分别表达 `temporarily degraded`、`fallback active`、`safety block`、`retrieval miss`、`tool failure`、`schema/parse failure` 与质量退化。

<!-- rule-id: TECH-086-PROMPT-INPUT-OUTPUT-CONTRACT -->
- 按默认顺序编写 prompt 时，`prompt.md` 须同时写明输入契约和输出契约。

<!-- rule-id: TECH-215-SUPPLY-CHAIN-LOCKFILE-COVERAGE -->
- 涉及依赖或构建时，供应链专项须覆盖 lockfile。

<!-- rule-id: TECH-079-AI-CONTRACT-SCHEMA-TRIGGER -->
- 仅当 target 含 AI tool、structured output 或 agent tool contract 时，须形成 `ai-tool-schemas`。

<!-- rule-id: TECH-079-AI-CONTRACT-MINIMUM-ARTIFACT -->
- target 含 AI 契约时，其最小工件须包含 AI tool schemas。

<!-- rule-id: TECH-079-AI-CONTRACT-SCHEMA -->
- AI contract（包括 AI tool 或 structured output）须登记 `target`、`owner`、`schemas`、`compatibility policy`、`rollback` 和 `human checkpoint`。

<!-- rule-id: TECH-191-AI-PRODUCT-EVENT-DEFAULTS -->
- AI 产品事件缺省记录 workflow、latency_bucket、token_bucket、result_class、safety_action 和 human_correction_required。

<!-- rule-id: TECH-241-MODEL-ROUTE-RESILIENCE-FIELDS -->
- 每条 model route 至少登记 timeout、retry 和 fallback chain。

<!-- rule-id: TECH-027-PROMPT-BUILDER-PLACEMENT -->
- prompt builder 的技术位置靠近所属 feature。

<!-- rule-id: TECH-006-AI-EVAL-FIXTURE-S01 -->
- 适用情形：组织 AI 服务代码时。internal/ai 存放 prompt、tool port、workflow 和 eval fixtures。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S04 -->
- 适用情形：组织 AI 依赖时。AI model/vendor SDK 仅在 adapter 或 workflow boundary 使用。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S06 -->
- 适用情形：组织前端时。缺省按 feature/route 组织 Vite 前端且不过度技术分层。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S02 -->
- 适用情形：调用供应商时。供应商调用收口到 client boundary。

<!-- rule-id: TECH-015-AI-MODEL-ROUTING-S07 -->
- 适用情形：组织 Vite 前端时。Vite 缺省目录包含 routes。

<!-- rule-id: TECH-016-AI-MODEL-ROUTING-S01 -->
- 适用情形：change 触发安全专项时。最小安全工件纳入 threat model。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S04 -->
- 适用情形：change 引入数据处理方时。供应商专项最小工件纳入 processor register。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S05 -->
- 适用情形：change 引入数据处理方时。供应商专项最小工件纳入 DPA checklist。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S06 -->
- 适用情形：change 涉及数据出境时。供应商专项最小工件纳入 transfer impact。

<!-- rule-id: TECH-013-AI-MODEL-ROUTING-S01 -->
- 适用情形：采集前端事件且该关联项适用时。前端事件须关联适用的 route pattern。

<!-- rule-id: TECH-026-AI-PROMPT-ARTIFACT-S02 -->
- 适用情形：采集 AI 产品事件时。AI 产品事件缺省记录 prompt_version。

<!-- rule-id: TECH-013-AI-MODEL-ROUTING-S02 -->
- 适用情形：采集 AI 产品事件时。AI 产品事件缺省记录 model_route。

<!-- rule-id: TECH-016-AI-MODEL-ROUTING-S02 -->
- 适用情形：change 触发安全专项时。安全专项须覆盖资产；安全专项须覆盖入口。

<!-- rule-id: TECH-017-AI-MODEL-ROUTING-S08 -->
- 适用情形：引入新供应商时。新供应商须登记：role、purpose、data classes、DPA/terms、retention、region、training/use 政策、删除协助。

<!-- rule-id: TECH-018-AI-MODEL-ROUTING-S02 -->
- 适用情形：需要模型路由治理时。触发模型路由或供应商治理时补充 ai-routing 工件。

<!-- rule-id: TECH-032-AI-PROMPT-DEGRADATION-STRATEGY-S01 -->
- 适用情形：编写 prompt.md 时。prompt.md 须记录降级策略。

<!-- rule-id: TECH-034-AI-PROMPT-SAFETY-BOUNDARY-S01 -->
- 适用情形：按默认顺序编写 prompt 时。prompt.md 须包含安全边界。

<!-- rule-id: TECH-065-AI-TRACE-LOG-CONTRACT-S01 -->
- 适用情形：记录 AI 调用证据时。trace/log须登记：prompt 版本、model、case id、latency、token、cost、tool calls、结果。

<!-- rule-id: TECH-050-AI-TOOL-CONTRACT-CLARITY-S04 -->
- 适用情形：定义 AI 工具时。工具参数应尽量结构化。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S02 -->
- 适用情形：触发上下文治理工件时。memory policy 缺省位于 ai-context/memory-policy/<capability>.md。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S01 -->
- 适用情形：触发上下文治理工件时。source registry 缺省位于 ai-context/source-registry/<capability>.json。

<!-- rule-id: TECH-005-AI-CONTEXT-RAG-S02 -->
- 适用情形：触发上下文治理工件时。context review 缺省位于 ai-context/context-review/<capability>.md。

<!-- rule-id: TECH-038-AI-RAG-MEMORY-S03 -->
- 适用情形：定义 memory policy 时。memory type 须覆盖 session；memory type 须覆盖 saved preference；memory type 须覆盖 inferred preference；memory type 须覆盖 retrieved knowledge；memory type 须覆盖 support summary；memory type 须覆盖 safety context。

<!-- rule-id: TECH-029-AI-PROMPT-ARTIFACT-S02 -->
- 适用情形：构建 AI prompt 时。Prompt builder 须分区 system/developer 指令；Prompt builder 须分区用户输入；Prompt builder 须分区 memory；Prompt builder 须分区 RAG context；Prompt builder 须分区 tool output。

<!-- rule-id: TECH-041-AI-RUNTIME-GOVERNANCE-LINK-S01 -->
- 适用情形：处理成本、供应商或客户数据时。AI runtime 约束须链接 技术设计整体边界。

<!-- rule-id: TECH-040-AI-ROUTE-POLICY-ARTIFACT-S01 -->
- 适用情形：生产 AI capability 建立 runtime 工件时。route policy 缺省位于 ai-runtime/route-policy/<capability>.md。

<!-- rule-id: TECH-011-AI-MODEL-REGISTRY-S01 -->
- 适用情形：生产 AI capability 建立 runtime 工件时。model registry 缺省位于 ai-runtime/model-registry/<capability>.json。

<!-- rule-id: TECH-045-AI-RUNTIME-ROUTING-S01 -->
- 适用情形：生产 AI capability 建立 runtime 工件时。tool registry 缺省位于 ai-runtime/tool-registry/<capability>.json。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S03 -->
- 适用情形：生产 AI capability 建立 runtime 工件时。runtime review 缺省位于 ai-runtime/runtime-review/<capability>.md。

<!-- rule-id: TECH-040-AI-ROUTE-POLICY-ARTIFACT-S02 -->
- 适用情形：编写 route policy 时。route policy须包含：Scope、Decision Matrix、Default Model Route、Tool/Connector Routes、Cost/Latency、Data Boundary、Safety/Privacy、Human Checkpoints、Linked Artifacts。

<!-- rule-id: TECH-025-AI-PRODUCTION-ROUTE-RECORD-S01 -->
- 适用情形：定义生产 route 时。生产 route须登记：模型族、route id、回滚路线。

<!-- rule-id: TECH-011-AI-MODEL-REGISTRY-S02 -->
- 适用情形：编写 model registry 时。model registry须包含：capability、owner、providers、routes、default_route、budgets、safety_gate、human_checkpoint、review_cadence。

<!-- rule-id: TECH-012-AI-MODEL-ROUTE-CONTRACT-S01 -->
- 适用情形：登记 model route 时。每条 route至少登记：模型、供应商、数据边界、max token、reasoning capability、tool capability、cost tier、latency target、safety refs、状态。

<!-- rule-id: TECH-035-AI-PROVIDER-CALL-TELEMETRY-S01 -->
- 适用情形：调用模型供应商时。provider 调用须登记：route id、provider、model、workflow version、eval version、latency、token、cost bucket、fallback reason。

<!-- rule-id: TECH-062-AI-TOOL-REGISTRY-SCHEMA-S01 -->
- 适用情形：编写 tool registry 时。tool registry须包含：capability、owner、tools、connectors、side_effect_classes、auth、rate_limits、budgets、telemetry、human_checkpoint、review_cadence。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S01 -->
- 适用情形：分类工具副作用时。只读且无敏感数据外发和持久副作用的工具划入 read_only。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S02 -->
- 适用情形：分类工具副作用时。写业务数据或创建内部记录的工具划入 write。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S03 -->
- 适用情形：分类工具副作用时。删除、覆盖、批量修改或难恢复工具划入 destructive。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S04 -->
- 适用情形：分类工具副作用时。发送外部消息或通知的工具划入 external_message。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S05 -->
- 适用情形：分类工具副作用时。退款、credit、收费、发票、额度或结算工具划入 money_movement。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S06 -->
- 适用情形：分类工具副作用时。改变订阅、权限、配额或 feature access 的工具划入 entitlement。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S07 -->
- 适用情形：分类工具副作用时。后台运营、生产配置、break-glass 或支持工具划入 admin。

<!-- rule-id: TECH-064-AI-TOOL-SIDE-EFFECT-TAXONOMY-S08 -->
- 适用情形：分类工具副作用时。shell、解释器、浏览器自动化、本地 MCP、容器或文件写入工具划入 code_execution。

<!-- rule-id: TECH-033-AI-PROMPT-RUNTIME-CONTRACT-S01 -->
- 适用情形：构建 AI prompt 时。Prompt builder 须读取 route id；Prompt builder 须读取 route policy；Prompt builder 须读取 allowed tool set。

<!-- rule-id: TECH-042-AI-RUNTIME-ROUTING-S04 -->
- 适用情形：实现工具路由时。工具路由须与 red-team 工件相连。

<!-- rule-id: TECH-207-GOVERNANCE-DEV-WORKSPACE-AI-CODING-S02 -->
- 适用情形：使用自有应用模板时。批准自有模板后须记录回退边界。

<!-- rule-id: TECH-007-AI-EVAL-FIXTURE-S01 -->
- 适用情形：建立 AI fixtures 时。AI fixtures 须包含边界样例。

<!-- rule-id: TECH-039-AI-RAG-MEMORY-S01 -->
- 适用情形：定义试点数据边界时。Data Boundary 须说明是否接触RAG source。

<!-- rule-id: TECH-008-AI-EVAL-FIXTURE-S01 -->
- 适用情形：定义试点数据边界时。Data Boundary 须说明是否接触训练/eval 材料。

<!-- rule-id: TECH-030-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：定义试点 AI 边界时。AI Boundary 须说明客户数据是否用于prompt。

<!-- rule-id: TECH-039-AI-RAG-MEMORY-S02 -->
- 适用情形：定义试点 AI 边界时。AI Boundary 须说明客户数据是否用于RAG；AI Boundary 须说明客户数据是否用于memory。

<!-- rule-id: TECH-024-AI-MODEL-ROUTING-S01 -->
- 适用情形：定义试点 AI 边界时。AI Boundary 须说明客户数据是否用于供应商处理。

<!-- rule-id: TECH-024-AI-MODEL-ROUTING-S02 -->
- 适用情形：启用客户专属 AI 配置时。客户专属 AI 配置须链接相应的 模型路由 工件。

<!-- rule-id: TECH-031-AI-PROMPT-ARTIFACT-S01 -->
- 适用情形：发现 AI prompt、tool 或 RAG source 的 secret exposure 时。发现 prompt injection 诱导模型泄露 secret、工具返回 secret、RAG/source 含 secret 时，按 exposure review 处理，并补充 AI red-team case 或 AI tool runtime guard。

<!-- rule-id: TECH-037-AI-QUALITY-TELEMETRY-CONTRACT-S01 -->
- 适用情形：定义Go / Kratos / sqlc / gRPC 默认规则工件时。Kratos middleware/handler 须记录 capability；Kratos middleware/handler 须记录 workflow version；Kratos middleware/handler 须记录 prompt version；Kratos middleware/handler 须记录 route id；Kratos middleware/handler 须记录 eval version；Kratos middleware/handler 须记录 trace id；Kratos middleware/handler 须记录 fallback reason；Kratos middleware/handler 须记录 quality severity；Kratos middleware/handler 禁止记录原始内容。
