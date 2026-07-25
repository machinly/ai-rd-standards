# ai-prompt-eval-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义一人公司 AI prompt、eval、schema、tool 和 agent workflow 的默认研发规范，使用户可见 AI 行为能够版本化、回归测试、观测和回滚。

## Requirements

### Requirement: 用户可见 AI 能力必须有版本化 artifacts

用户可见 AI 能力 MUST 在实现或修改前具备 prompt、eval、rubric 和 runbook artifacts。

#### Scenario: 新增 AI 能力

- GIVEN 一个新用户可见 AI 能力
- WHEN 开始实现
- THEN 创建 `ai/prompts/<capability>/prompt.md`
- AND 创建 `ai/evals/<capability>/cases.jsonl`
- AND 创建 `ai/evals/<capability>/rubric.md`
- AND 创建 `ai/evals/<capability>/runbook.md`

#### Scenario: 修改 AI 行为

- GIVEN 需要修改 prompt、model、schema、tool 或 workflow
- WHEN 变更会影响用户可见输出
- THEN 更新关联 eval cases
- AND 在 artifacts 或 tasks 中记录预期行为变化

### Requirement: eval fixtures 必须先于 prompt/model/tool 变更

AI 行为变更 MUST 先定义本地 eval fixtures，再修改 prompt、model、schema、tool 或 agent workflow。

#### Scenario: 最小 eval 集

- GIVEN 一个用户可见 AI 能力
- WHEN 创建 eval fixtures
- THEN `cases.jsonl` 至少包含 3 条 case
- AND 至少包含 happy path、边界或失败、对抗或 prompt injection 中的三类覆盖
- AND 每条 case 包含稳定 `id`、`input` 和 `criteria`

#### Scenario: eval 失败

- GIVEN eval 运行失败
- WHEN 准备交付
- THEN 记录失败原因、是否接受风险、是否回滚或补 prompt/schema/tool
- AND 不得只用“模型偶然波动”作为唯一解释

### Requirement: 程序消费的模型输出必须结构化

程序要消费的 AI 输出 MUST 使用结构化 schema 或明确适配层，避免下游解析自由文本。

#### Scenario: 下游程序消费输出

- GIVEN 模型输出会被后端、前端或工具继续处理
- WHEN 设计输出格式
- THEN 定义 JSON Schema 或等价结构
- AND prompt 说明输出契约
- AND 解析失败有 fallback 或错误处理

#### Scenario: 纯展示文本

- GIVEN 模型输出只展示给人阅读
- WHEN 不使用结构化输出
- THEN 在 design 中说明原因
- AND eval rubric 覆盖文本质量标准

### Requirement: agent 必须由 workflow 逐级升级

AI 能力 MUST 优先使用规则、单次模型调用或 deterministic workflow；只有可验证需要时才升级为 agent。

#### Scenario: 固定路径足够

- GIVEN 任务步骤可预知
- WHEN 单次调用或固定 workflow 能通过 eval
- THEN 不引入 autonomous agent

#### Scenario: 升级为 agent

- GIVEN 任务步数不可预知且需要工具探索
- WHEN 准备使用 agent
- THEN 记录 eval 或 trace 证据
- AND 定义停止条件、最大迭代次数或人工 checkpoint
- AND 定义工具权限和审计日志

### Requirement: 工具调用必须最小权限并可审计

AI 工具调用 MUST 使用最小权限、结构化参数和可审计记录，高风险副作用必须有人类确认或 dry-run。

#### Scenario: 新增工具

- GIVEN AI 能力需要调用工具
- WHEN 定义工具
- THEN 写清工具名称、参数、返回结构、权限、失败模式和示例
- AND 不把外部不可信内容作为高优先级指令

#### Scenario: 高风险工具

- GIVEN 工具会产生金钱、权限、删除、通知、外部写入或不可逆副作用
- WHEN agent 或 workflow 准备调用
- THEN 默认 dry-run 或 human approval
- AND 记录审计日志

### Requirement: AI 能力必须有最小运维信号

上线的 AI 能力 MUST 记录质量、成本、延迟、错误和人工介入信号。

#### Scenario: AI 能力上线

- GIVEN AI 能力进入生产或真实用户流程
- WHEN 记录运行日志或指标
- THEN 包含 `ai_feature`、prompt version、model、schema version
- AND 记录 latency、traffic、errors、token/cost 或采集计划
- AND 记录 eval pass rate 或人工抽检通过率
