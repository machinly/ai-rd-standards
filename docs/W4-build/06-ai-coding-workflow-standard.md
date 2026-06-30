# W4 Build 触发专项：AI 协作编码、变更批次与自审规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现由 Codex、Copilot 或其他 AI coding agent 修改生产代码、prompt、配置、迁移、契约、测试、基础设施或发布流水线时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/00-main.md`，由主入口判断是否触发本专项。

## 目标

一人公司使用 AI 写代码时，真正的风险不是“AI 会不会写”，而是它能不能始终围绕正确的目标、小批量推进、留下可 review 的证据，并在越界时停下来让人判断。本专项定义 AI 协作编码规范，把 OpenSpec、Codex/AI agent、代码审查、验证命令和人工 checkpoint 连接成一条轻量闭环。

默认原则：AI 可以加速实现，不能替代人的产品判断和责任边界。每次生产相关变更都必须能回答四个问题：为什么改、改了哪一批、怎么验证、还有什么风险。

## 核心依据

- 《人月神话》：概念完整性来自少数清晰判断，不能靠增加“人手”或 agent 数量自动获得；AI agent 越多，越需要明确分工和边界。
- 小型项目管理：小项目的流程只服务下一步行动；不需要厚重 ceremony，但需要短、准、可恢复的工作记录。
- OpenSpec：AI 编码前先用 proposal/spec/design/tasks 对齐要做什么，避免直接从模糊请求跳到代码。
- Software Engineering at Google, Code Review：代码审查不仅发现 bug，更保护可理解性、一致性、知识传递和历史记录。
- Google Engineering Practices, Small CLs / CL descriptions / Code Review Standard：小而完整的变更更容易设计、review、回滚；描述要说明做了什么和为什么；review 目标是持续改善代码健康，而不是追求完美。
- DORA small batches / trunk-based development：小批量变更缩短反馈环；在生成式 AI 时代，小批量更能放大 AI 对产品表现的正面影响。
- OpenAI Codex best practices：把 Codex 当成可配置、可改进的队友；复杂任务先计划；用 `AGENTS.md`、配置、skills 和自动化沉淀重复经验。
- Codex sandbox / approvals：sandbox 定义 AI 能做什么，approval policy 定义什么时候必须停下来问人；二者共同降低 approval fatigue。
- GitHub Copilot CLI best practices：AI coding agent 应有自定义指令、计划、授权边界、团队规则和安全注意事项。
- GitHub Review AI-generated code：AI 生成代码必须经过功能检查、意图对齐、质量审查、依赖审查和 AI 特有问题审查。

## 范围

适用对象：

- 任何会修改生产代码、prompt、配置、基础设施、迁移、契约、测试或发布流水线的 AI 协作编码任务。
- Go/Kratos/sqlc/gRPC 服务实现、proto/schema 变更、Vite 前端实现、AI workflow prompt/tool/eval 变更。
- Codex、Copilot、Claude Code 或其他 AI coding agent 参与的实现、重构、修复、测试补齐、文档同步。
- 需要中断恢复、并行 agent、review 或未来追溯的编码会话。

不适用对象：

- 纯阅读、解释代码、一次性草稿，且不产生仓库变更。
- 不进入生产、不访问真实数据、不调用真实供应商的 throwaway experiment。
- 已由 W3 prompt/eval、W6 release、W2 security、W2 contract 覆盖的深层专项工件；本专项只要求 AI 编码会话层的证据。

## 最小工件

每个 OpenSpec change 使用同一个 `<change-id>` 文件名：

```text
ai-coding/
  implementation-brief/<change-id>.md
  batch-log/<change-id>.md
  review/<change-id>.md
  verification/<change-id>.json
```

### `ai-coding/implementation-brief/<change-id>.md`

实施 brief 是给人和 AI agent 共用的最小任务卡，必须包含：

- `OpenSpec Change`
- `Desired Outcome`
- `Non-Goals`
- `Context Sources`
- `Target Files / Modules`
- `Allowed Autonomy`
- `Human Checkpoints`
- `Verification Commands`
- `Stop Conditions`
- `Handoff`

默认规则：

- `OpenSpec Change` 必须链接 `openspec/changes/<change-id>/`。
- `Context Sources` 只列可信入口：OpenSpec、相关规范、现有实现、官方文档、已有 tests/evals。
- `Allowed Autonomy` 说明 AI 可自动做的事，例如读取文件、修改工作区内文件、运行本地测试、更新 docs。
- `Human Checkpoints` 只列会改变产品方向、数据边界、权限、安全、成本、供应商、破坏性操作或生产发布的判断。
- `Stop Conditions` 说明什么时候必须停：规格不一致、测试无法解释、需要删除测试、新依赖不确定、需要真实凭据、需要真实用户数据、需要外部副作用。

### `ai-coding/batch-log/<change-id>.md`

批次日志用于控制 AI 实施粒度，必须包含：

- `Batch Scope`
- `Changes Made`
- `Commands Run`
- `Decisions`
- `Assumptions`
- `Deviations`
- `Follow-Up`

默认批次大小：

- 一批只回答一个 review 问题，例如“新增 RPC 骨架和测试”“补 sqlc query 与 data test”“实现 Vite 页面状态”。
- 一批尽量不超过 8 个核心文件或 2 个逻辑变更；超过时必须在 `Deviations` 说明为什么没有拆。
- generated code、schema/proto、业务逻辑、UI、migration、eval fixture 默认分批提交或至少分段 review。
- 不记录 raw prompt、raw response、真实 secret、真实用户数据或供应商凭据。

### `ai-coding/review/<change-id>.md`

自审记录必须包含：

- `Diff Summary`
- `Functional Review`
- `Intent / Architecture Review`
- `AI-Specific Review`
- `Dependency / Security Review`
- `Human Checkpoints`
- `Review 1`
- `Review 2`
- `Merge Decision`

默认 review 顺序：

1. 先跑自动化检查，再看代码。
2. 先确认是否解决正确问题，再看实现细节。
3. 优先检查整体设计、边界、权限、数据流、失败路径和测试证据。
4. 专门检查 AI 常见问题：幻觉 API、忽略约束、删除/跳过失败测试、过度抽象、隐藏依赖、看似正确但语义不匹配。
5. `Merge Decision` 只能是 `ready`、`blocked`、`needs-human`、`needs-more-tests`。

### `ai-coding/verification/<change-id>.json`

验证记录必须包含：

- `change_id`
- `owner`
- `openspec_change`
- `stack`
- `batch_size`
- `commands`
- `verification_results`
- `human_checkpoint`
- `residual_risks`
- `status`

`verification_results` 至少包含：

- `openspec`
- `tests`
- `builds`
- `evals`
- `security_checks`
- `contract_checks`
- `release_mapping`

默认验证：

- 所有实现变更运行 `openspec validate --all` 或等价 OpenSpec 检查。
- Go/Kratos/sqlc/gRPC 变更运行 `go test ./...`，涉及 sqlc 时运行 `sqlc generate`，涉及 proto/gRPC 契约时运行 breaking/lint 或 contract check。
- Vite 前端变更运行 `npm run build`，必要时运行 typecheck、Vitest、Playwright smoke。
- AI prompt/model/tool workflow 变更运行最小 eval、fixture 或 dry-run。
- 安全、权限、数据、供应链、契约、发布相关变更链接对应阶段的 guard 或 gate。

## 默认 AI 编码会话流程

1. 先确认是否已有 OpenSpec change；没有则先建 change，不直接写代码。
2. 写 `implementation-brief`，只在高影响点问人；其余按仓库规范默认推进。
3. 让 AI 读取 brief、OpenSpec、相关规范和现有代码，形成小批次计划。
4. 每批实施后更新 `batch-log`，运行对应验证命令。
5. 生成 `review`，完成 AI 自审和两轮一人公司 review。
6. 填写 `verification.json`，记录通过、失败、跳过和 residual risks。
7. 如果 AI 反复犯同一类错误，更新 `AGENTS.md`、skill、script 或模板，而不是靠下次记住。

## Go / Kratos / sqlc / gRPC 默认规则

- AI 不得绕过 `.proto`、sql schema、migration 或 OpenSpec 直接发明接口语义。
- proto/schema/generated code/业务逻辑/handler/test 尽量分批，方便 review 和回滚。
- sqlc query 改动必须同步 schema、generated code、data test 和 migration 证据。
- gRPC 错误码、auth/tenant metadata、idempotency、retry 语义变化触发人工 checkpoint。
- 无法解释的失败测试不能删除或 skip；必须标记 `needs-human` 或 `needs-more-tests`。

## Vite 前端默认规则

- AI 修改 UI 时必须说明目标用户路径和状态：loading、empty、error、success、permission denied。
- 参考 Vercel `design.md` / `design.dark.md` 时，落点应是 token、布局、密度、可访问性和暗色模式，不是复制营销页风格。
- UI 变更至少运行 build；涉及交互、路由、表单、权限或状态机时补 Vitest/Playwright smoke。
- AI 不得用可见说明文字替代真实交互，也不得把测试性文案留在生产 UI。

## AI workflow 默认规则

- prompt、model、tool schema、agent loop、自主权限、fallback 路径变化必须链接 W3 eval 工件。
- 真实模型调用、真实工具副作用、真实供应商写入、成本上限提升触发人工 checkpoint。
- 会话记录不保存 raw prompt/raw response；只保存行为版本、fixture、eval 结论和失败类型。
- AI 生成的测试不能只证明当前实现；必须包含代表样例、边界样例和失败样例。

## 需要人判断的关键点

只把这些判断交给人：

- 是否改变产品目标、用户可见行为或 OpenSpec scope。
- 是否访问真实用户数据、生产数据、真实 secret 或真实供应商。
- 是否执行破坏性命令、迁移、删除、生产发布或外部写入。
- 是否新增长期依赖、付费服务、模型供应商、运行成本或 agent 自主权限。
- 是否改变 auth、tenant、permission、数据边界、公共 API、错误语义或 contract。
- 是否接受失败测试被删除/跳过、未解释 flaky、未覆盖高风险路径。
- 是否让多个 agent 并行修改同一边界。

其他例行代码修改、局部重构、测试补齐、文档同步、生成代码、格式化、构建和本地验证由 AI 在 sandbox 与 guard 内推进。

## Review 1：一人公司注意力审查

- 保留：四个工件足以恢复上下文，不要求完整 PR 流程。
- 保留：人只审高影响 checkpoint 和 residual risks，低风险实现交给 AI + verifier。
- 调整：批次大小用“一个 review 问题”而不是固定行数，适合 Go、Vite、AI workflow 不同变更。
- 调整：允许 `needs-more-tests`，避免 AI 为了通过而删除或弱化测试。
- 风险：工件过多会拖慢小修复。缓解：纯文档解释、throwaway 实验和无仓库变更任务不适用；小修复可用最短 brief。

结论：可落地。一个人可以把 AI coding session 从“聊天记录”变成四份轻量证据，中断后能恢复，review 时只看真正需要判断的点。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：实施前绑定 OpenSpec，避免 AI 做错问题；用户可见行为变化必须人审。
- 工程角度：小批次、CL 描述、自审、测试和 verifier 让 AI 代码进入正常工程节奏。
- 运维角度：verification JSON 把 tests/build/eval/security/contract/release gate 串起来，减少发布前临时找证据。
- 安全隐私角度：sandbox、approval、stop condition、禁止 raw prompt/secret/真实数据进入工件，降低 agent 副作用风险。
- 成本角度：把失败模式沉淀进 `AGENTS.md`、skill 或脚本，避免重复消耗 token 和人的检查时间。

结论：可落地。本专项把“AI 帮我写代码”升级为“AI 在可审查边界内交付小批次变更”，并与 W2 OpenSpec、W3 eval、W5 testing、W4 workspace automation 衔接。
