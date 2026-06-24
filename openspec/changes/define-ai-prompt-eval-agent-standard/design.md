# 设计：AI prompt / eval / agent workflow 研发规范

## 设计决策

### 1. 仓库内 fixtures 是长期事实来源

OpenAI 文档显示旧 Evals platform 会在 2026-10-31 只读，并计划在 2026-11-30 关闭。为了避免一人公司未来迁移成本，本规范默认把 eval fixtures 放在仓库，平台 datasets/traces 作为可选增强。

### 2. eval 先于 prompt/model/tool 变化

AI 行为非确定性强，只靠人工感觉会漂移。先定义 cases 和 rubric，再改 prompt、model、schema 或 tool，能让一人公司用少量样例守住回归底线。

### 3. 默认简单 workflow，agent 是升级项

单次调用或 deterministic workflow 能解决时，不引入 agent。只有步数不可预知、需要工具探索和恢复，并且 eval/trace 证明收益时，才升级为 agent。

### 4. 结构化输出优先服务程序边界

当下游程序要消费模型输出时，使用 JSON Schema/Structured Outputs，避免自由文本解析。schema 与 prompt 同版本管理。

### 5. 工具安全按副作用分级

读工具、搜索工具、写工具、金钱/权限/通知类工具风险不同。高风险工具默认 dry-run 或 human approval，并记录审计日志。

## 取舍

- 本地 fixtures 没有平台 UI 方便，但长期可迁移、可 review、可随代码变更。
- 至少 3 条 eval 不能证明全面质量，但能防止一人公司最常见的 prompt 回归。
- 不默认 agent 会让部分复杂任务早期显得朴素，但能控制成本、延迟和错误放大。
- 不在本阶段写 SDK 模板，避免与后续 Go/Kratos 服务实现混在一起。

