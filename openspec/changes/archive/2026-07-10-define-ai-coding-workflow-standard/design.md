# Design

## 工件形态

每个 OpenSpec change 使用轻量 AI coding 工件：

- `ai-coding/implementation-brief/<change-id>.md`
- `ai-coding/batch-log/<change-id>.md`
- `ai-coding/review/<change-id>.md`
- `ai-coding/verification/<change-id>.json`

Markdown 用于人和 AI agent 共享上下文，JSON 用于机器检查。工件只记录意图、批次、验证和风险，不保存 raw prompt、raw response、secret、真实用户数据或供应商凭据。

## 验证策略

`ai-coding-workflow-guard` 提供 `verify_ai_coding_workflow.py`：

- 检查 implementation brief、batch log、review 文档必要章节。
- 检查 verification JSON 的必填字段、OpenSpec change 链接、stack、commands、verification_results、人审点和 residual risks。
- 检查是否包含 OpenSpec validate、Go/sqlc/gRPC/Vite/AI eval 等与 stack 匹配的验证命令。
- 检查批次是否过大，并对超过阈值的批次给出 warning。
- 检查 secret、PII、raw prompt/response 不进入工件。

## 裁剪原则

- Tiny fix 可以使用最短 brief，但仍要链接 OpenSpec 和验证结果。
- 低风险实现默认由 AI 自动推进；只有高影响 checkpoint 升级给人。
- verifier 不判断业务实现是否正确，只检查 AI 编码会话是否留下足够证据。
- 多 agent 并行只适用于边界清晰、不会同时修改同一模块的任务。
