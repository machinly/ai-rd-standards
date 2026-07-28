# 实现：AI prompt、上下文与 runtime

## 规范要求

<!-- rule-id: IMPL-EVAL-JSON-FIELD-ORDER-DISCRETION -->
- 编写 eval 数据时，JSON/JSONL 字段顺序缺省无需人工判断。

<!-- rule-id: IMPL-PROMPT-EVAL-SPECIALTY-TRIGGER -->
- 只有[技术设计](../05-technical-design.md)要求进一步定义 prompt、eval、结构化输出、workflow/agent 升级或最小质量门禁时，才使用 prompt/eval 专项。

<!-- rule-id: IMPL-PROMPT-VERSION-REPOSITORY -->
- 每个 prompt 都须纳入仓库版本管理；个人笔记、聊天记录、Dashboard 与 Playground 可以作为辅助工作面，但不能成为其唯一保存位置。

<!-- rule-id: IMPL-MODEL-DEFAULT-CENTRAL-CONFIG -->
- 模型默认值须集中配置，禁止散落硬编码。

<!-- rule-id: IMPL-PROMPT-ARTIFACT-PATH -->
- prompt 工件缺省位于 `ai/prompts/<capability>/prompt.md`。

<!-- rule-id: IMPL-AI-TRACE-DIRECTORY -->
- trace 目录缺省位于 `ai/traces/<capability>/`。

<!-- rule-id: IMPL-PROMPT-REQUIRED-SECTIONS -->
- `prompt.md` 须记录目标、输入、输出、拒绝或降级策略、示例与版本记录。

<!-- rule-id: IMPL-MINIMAL-MODEL-CALL-SHAPE -->
- 最小模型调用优先单次调用或固定 workflow。

<!-- rule-id: IMPL-PROMPT-METADATA -->
- 版本化 prompt 须记录 `version`、`owner`、`last_reviewed` 与 `model_default`。

<!-- rule-id: IMPL-PROMPT-INSTRUCTION-QUALITY -->
- prompt 指令须短、具体、可验证，且不得堆积历史原因。

<!-- rule-id: IMPL-PROMPT-EXAMPLE-COVERAGE -->
- prompt 示例须覆盖常见、拒绝和降级情况。

<!-- rule-id: IMPL-PROMPT-SENSITIVE-CONTENT-BAN -->
- prompt 禁止包含 secret、API key、内部不可泄露策略或用户隐私样例。

<!-- rule-id: IMPL-PROMPT-CHANGE-EXPECTED-BEHAVIOR -->
- prompt 改动须说明预期行为变化。

<!-- rule-id: IMPL-PROMPT-FILENAME-DISCRETION -->
- 低风险 AI change 的 prompt 文件命名缺省无需人工判断。

<!-- rule-id: IMPL-EVAL-CASE-ID-DISCRETION -->
- 低风险 AI change 的 case id 缺省无需人工判断。

<!-- rule-id: IMPL-LOCAL-JSONL-FIXTURE-DISCRETION -->
- 低风险 AI change 是否用本地 JSONL 存 fixture，缺省无需人工判断。

<!-- rule-id: IMPL-MEMORY-WORKSPACE-CONTEXT-TYPE -->
- memory policy 的 memory type 须覆盖 workspace context。

<!-- rule-id: IMPL-CONTEXT-DELETION-SURFACES -->
- 上下文删除路径须覆盖 memory item、vector store、embedding、cache、conversation state、application state 与 source index。

<!-- rule-id: IMPL-AI-RUNTIME-W4-LANDING -->
- AI runtime 的配置、flag 与 worker 落地须进入实现项目。

<!-- rule-id: IMPL-AI-RUNTIME-EXPLICIT-USECASE -->
- 后端处理 AI runtime 时，须先经过职责明确的内部 usecase；该入口可以是 `ToolRegistry`、`AIRuntime`、`ModelRouter`，也可以采用职责等价的实现。

<!-- rule-id: IMPL-AI-RUNTIME-INPUT-SCHEMA -->
- AI runtime usecase 输入须包含 capability、task type、actor、tenant、risk tier、latency class、budget class、required tools 与 data boundary。

<!-- rule-id: IMPL-AI-RUNTIME-OUTPUT-SCHEMA -->
- AI runtime usecase 输出须包含 route id、request options 与 allowed tool set。

<!-- rule-id: IMPL-AI-RUNTIME-NO-SCATTERED-HARDCODE -->
- 业务代码禁止散落硬编码 model name、provider URL、max token、reasoning effort、temperature、tool allowlist 或 connector scope。

<!-- rule-id: IMPL-AI-ADAPTER-STABLE-INTERFACE -->
- provider adapter 与 tool adapter 须暴露稳定内部接口。

<!-- rule-id: IMPL-AI-ADAPTER-NO-LEAKAGE -->
- adapter 禁止把供应商 SDK 类型、access token 或 raw tool output 泄漏到业务层。

<!-- rule-id: IMPL-CODE-EXECUTION-TOOL-HUMAN-GATE -->
- 扩大 runtime 能力并引入新代码执行工具时，须交由人工判断。
