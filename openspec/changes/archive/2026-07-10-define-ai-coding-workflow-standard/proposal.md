# Proposal: define AI coding workflow standard

## 意图

建立一人公司 AI 协作编码、变更批次、自审和验证证据规范，让 Codex/AI coding agent 的实现过程可计划、可 review、可恢复，并且只在真正高影响决策上打断人。

## 范围

- 新增 `ai-coding-workflow-standard` spec。
- 新增 W4 AI 协作编码触发专项文档。
- 创建 `ai-coding-workflow-guard` skill 和 verifier。
- 补充来源索引与 README。

## 不做什么

- 不替代 W3 AI prompt/eval、W5 testing、W2 API contract、W4 dev workspace automation。
- 不要求每次只读或解释代码时创建工件。
- 不连接真实 GitHub、Codex cloud、Copilot、OpenAI API、供应商或生产环境。
- 不规定必须使用某一个 AI coding agent；Codex 是默认优先适配对象。

## 依据

- 《人月神话》。
- OpenSpec getting started。
- Software Engineering at Google, Code Review。
- Google Engineering Practices: Code Review Standard、Small CLs、CL descriptions、What to look for in a code review。
- DORA small batches / trunk-based development。
- OpenAI Codex best practices、AGENTS.md、sandbox / approvals、skills。
- GitHub Copilot CLI best practices。
- GitHub Review AI-generated code。

## 需要人的判断

只有这些需要人工 checkpoint：产品目标或用户可见行为变化、真实数据/secret/供应商访问、破坏性命令或生产发布、新长期依赖或成本提升、auth/tenant/permission/API contract 变化、删除/跳过失败测试、多个 agent 并行修改同一边界。
