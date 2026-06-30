# W3 触发专项：AI 记忆、上下文来源、RAG 与引用规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项，不是 W3 主入口。只有当当前 AI capability 使用长期记忆、用户偏好、workspace context、RAG 知识源、文件/向量检索、引用、删除或 grounding 时，才读取本文件。

普通 W3 工作先回到 `docs/W3-ai-behavior/00-main.md`。

## 目标

把 AI 记忆和 RAG 合并成一个“上下文治理”入口：AI 使用的长期上下文从哪里来、是否可信、能否被用户控制、如何注入 prompt、如何引用、如何删除和评测。

默认原则：长期记忆和 RAG context 都是不可信外部上下文，不是授权事实，也不是 system/developer 指令。没有来源、权限、freshness、TTL、用户控制和删除路径的内容，不得默认注入模型。

## 主要角色消费者

- 产品：决定个性化和引用体验是否符合用户心理模型。
- 后端：实现 memory/retrieval/source/deletion job。
- 安全合规：检查隐私、租户、授权、删除和敏感内容。
- QA：验证删除后不再使用、低置信降级和引用质量。

## 最小工件

按触发选择：

```text
ai-context/
  memory-policy/<capability>.md
  preference-schema/<capability>.json
  source-registry/<capability>.json
  retrieval-policy/<capability>.json
  citation-grounding/<capability>.md
  context-review/<capability>.md
```

## 必须覆盖

- memory type：session、saved preference、inferred preference、workspace context、retrieved knowledge、support summary、safety context。
- source registry：owner、scope、system of record、access check、freshness、license/rights、data classification、deletion policy。
- retrieval policy：tenant/user scope filter、source allowlist、max results/tokens、score threshold、citation policy、fallback。
- user controls：查看、关闭、删除、导出、临时模式或“不要记住”。
- deletion path：memory item、vector store、embedding、cache、conversation/application state 和 source index。

## 默认规则

- Prompt builder 必须把 system/developer 指令、用户输入、memory、RAG context、tool output 分区。
- 记忆不能作为授权事实；权限仍由后端 Auth/tenant boundary 判定。
- RAG context 进入 prompt 时标记为 untrusted context；检索文本中的指令不能提升为模型指令。
- 低置信、过期、冲突、缺 citation 或来源不可信时，AI 降级、询问、说明不确定或拒答。
- 引用必须能追到 source id、version/date 或可点击来源；不得伪造 citation。

## 需要人判断

- 默认开启长期记忆、reference chat history、workspace memory、默认检索或 default context injection。
- 保存、推断或默认注入 sensitive/restricted memory 或客户机密来源。
- 跨用户、跨 tenant、跨 workspace/project 共享 memory、source、index、embedding 或检索结果。
- 使用授权/版权不清、合同限制、robots/ToS 不清或供应商政策不清的内容。
- 接受删除/reindex/vector store retention/cache 清理失败。
- 在医疗、法律、金融、身份、就业、教育、公共安全等高影响领域使用记忆或 RAG。

## Review A：一人可执行性

本专项把“AI 记住什么”和“AI 检索什么”统一到一个上下文入口，避免 memory 与 RAG 两套相似工件并行膨胀。一个人可以先从 5-10 个低敏偏好字段或一个小知识源开始。

## Review B：产品 / 工程 / 运维风险

保留了用户控制、租户过滤、来源授权、引用、删除和 prompt injection 边界。最小安全下一步是为每个默认注入的上下文写清来源、权限和删除路径。

