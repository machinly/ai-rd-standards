# W3 AI Behavior 核心入口

## W3 定位

本文件是 W3 AI Behavior 的核心入口，也是进入 `docs/W3-ai-behavior/` 后默认先读的唯一主规范。W3 只回答一个问题：**AI 能力在什么输入下算好、算坏、必须拒绝或降级？**

W3 不替代 W1 的产品证据，也不替代 W2 的风险边界。只有当 W2 已经确认变更会影响用户可见 AI 行为、prompt、模型、工具、RAG、记忆、内容安全、eval、数据或多语言输出时，才进入 W3。W3 完成后，才能进入 W4 实现或回到 W2 调整边界。

## 核心问题

W3 必须让一人公司在改 AI 行为前回答：

- 这个 AI capability 的目标行为、失败行为、拒绝行为和降级行为是什么？
- 哪些样本代表 happy path、边界、失败、对抗、隐私、安全、低置信和多语言场景？
- prompt、schema、工具、模型、RAG、记忆、内容安全和路由变化如何被 eval 证明？
- 用户数据、客户内容、供应商、权限、成本、延迟和安全边界是否可接受？
- 失败时如何 fallback、rollback、人工复核、阻塞发布或回到 W2/W1？

默认原则：用户可见 AI 行为不能只靠“感觉更好”。没有最小 eval、失败样例、安全边界和回滚/降级路径，就不进入实现或发布。

## 适用范围

适用：

- Prompt、developer/system 指令、结构化输出、工具描述、agent workflow、模型路由、RAG、记忆、内容审核、多语言 AI 输出、模型优化。
- 用户可见 AI chat、assistant、agent、RAG 问答、客服 AI、内容生成、代码生成、数据分析、后台 AI operator 或自动化 workflow。
- 会改变 AI 输出质量、安全拒绝、工具调用、引用、个性化、模型供应商、token 成本、延迟、内容政策或本地化行为的工作。

不适用：

- 产品方向、目标用户、成功指标和学习决策不清；回到 W1。
- 数据边界、安全隐私、供应商、IP、客户数据生命周期或公开承诺尚未定义；回到 W2。
- 已经定义好的 AI 行为如何落到 Go/Vite/worker/config；进入 W4。
- AI 线上质量事故、支持投诉和学习回流；进入 W8。

## 最小产出

每个用户可见 AI capability 至少需要：

```text
ai/
  prompts/<capability>/prompt.md
  evals/<capability>/cases.jsonl
  evals/<capability>/rubric.md
  evals/<capability>/runbook.md
```

若触发相应场景，再补：

- `ai-data/`：dataset card、eval set、labeling guide、quality report、refresh review。
- `ai-safety/`：abuse case、red-team plan、adversarial cases、mitigation map、safety release review。
- `content-safety/`：policy、moderation rules、enforcement runbook、notice/appeal、moderation review。
- `ai-memory/`：memory policy、preference schema、context source map、retrieval rules、memory review。
- `ai-routing/`：model registry、route policy、fallback runbook、eval gate、provider review。
- `ai-tools/`：tool registry、permission policy、execution runbook、tool test plan、tool review。
- `rag/`：source registry、ingestion pipeline、retrieval policy、citation grounding、RAG eval review。
- `ai-optimization/`：optimization brief、training data plan、optimization run、validation report、rollout decision。
- `localization/`：locale policy、message catalog、time/currency rules、AI locale eval、localization review。

最小 eval 要求：至少 3 条样例，包括 happy path、边界/失败、对抗或注入；高风险能力还必须包含安全、隐私、拒绝、降级和人工复核样例。

## 人工判断点

默认不问人的事项：case id、rubric 初稿、普通 prompt 文案、低风险样本标签、JSON/JSONL 字段顺序、runbook 小节命名。

必须人工判断：

- 是否允许 AI 输出触发金钱、删除、权限、通知、外部提交、后台动作或代码执行。
- 是否处理医疗、法律、金融、未成年人、身份、就业、教育、公共安全、敏感个人数据或高影响领域。
- 是否把用户数据发给新模型、工具、RAG source、供应商、训练/微调流程或外部翻译服务。
- 是否上线 autonomous agent、高权限工具、无 fallback 的 AI 能力或未缓解 high/critical 安全发现。
- 是否改变默认模型、供应商、moderation threshold、拒绝边界、记忆默认开启、RAG 来源、训练数据、locale 或多语言高风险文案。
- 是否接受 eval 失败、质量回归、安全/隐私例外、数据来源/许可不清或 train/eval 泄漏风险。

## 触发型专项

- Prompt、eval、结构化输出、workflow/agent 升级和最小 AI 质量门禁：读 `docs/W3-ai-behavior/prompt-eval-agent-workflow-standard.md`。
- Eval 数据集、样本来源、标注、train/eval 分离、质量报告和刷新：读 `docs/W3-ai-behavior/ai-dataset-eval-data-standard.md`。
- 红队、滥用场景、对抗样本、mitigation 和安全发布审查：读 `docs/W3-ai-behavior/ai-red-team-abuse-standard.md`。
- 内容安全、UGC、AI 生成内容审核、通知和申诉：读 `docs/W3-ai-behavior/content-safety-moderation-standard.md`。
- AI 记忆、用户偏好、长期上下文、临时模式和删除控制：读 `docs/W3-ai-behavior/ai-memory-context-standard.md`。
- 模型选择、供应商路由、fallback、成本/延迟和 route eval gate：读 `docs/W3-ai-behavior/ai-model-routing-provider-standard.md`。
- AI 工具运行时、外部连接器、MCP、沙箱、审批、幂等和审计：读 `docs/W3-ai-behavior/ai-tool-runtime-standard.md`。
- RAG 知识源、摄取、检索、引用、删除、prompt injection 和 grounding：读 `docs/W3-ai-behavior/rag-retrieval-source-standard.md`。
- 微调、蒸馏、模型优化、训练数据计划、验证和 rollout：读 `docs/W3-ai-behavior/ai-model-optimization-training-standard.md`。
- 国际化、本地化、时区/货币、多语言 AI 输出和 locale eval：读 `docs/W3-ai-behavior/localization-locale-time-ai-standard.md`。

## 出口

- 产品问题或成功指标不清：回到 W1。
- 数据、安全、供应商、IP、客户数据或承诺边界不清：回到 W2。
- AI 行为定义、eval、失败样例、安全边界和 fallback 已可执行：进入 W4 实现。
- 需要证明质量、安全、可访问性、性能或韧性：进入 W5。
- 需要发布、客户上线、公开 claim 或 release gate：进入 W6。
- 已上线后出现反馈、质量回归、支持投诉或事故：进入 W8，并把新样本回流到 W3。

## Review 1：一人公司注意力审查

- 保留：W3 只处理用户可见 AI 行为，不把所有 AI 专项都变成默认必读。
- 保留：最小 eval 四件套是默认产出，专项工件只在触发条件命中时创建。
- 调整：旧数字文件全部降级为语义化触发专项，避免目录里多个“阶段”并列。
- 风险：AI 规范容易膨胀。缓解：每次只围绕一个 capability、一个行为变化和一个明确的 release/eval gate。

结论：可落地。W3 把 AI 行为从“调 prompt 和换模型”压成可验证的样本、边界、路由、工具、来源和降级决策。

## Review 2：产品、工程、运维、安全、成本审查

- 产品角度：AI 输出、拒绝、引用、个性化和本地化都连接用户任务和信任边界。
- 工程角度：prompt、schema、tool、route、RAG、memory 和 eval artifact 都能进入版本控制。
- 运维角度：fallback、telemetry、quality gate 和 rollback 能支撑上线后恢复。
- 安全隐私角度：红队、内容安全、工具权限、RAG 不可信上下文、记忆删除和数据来源都有边界。
- 成本角度：模型路由、token、工具 fanout、RAG 检索、训练运行和多语言支持都有预算和人工判断点。

结论：可落地。W3 完成后，下一步应该是小范围实现和验证，而不是继续凭感觉增加模型复杂度。
