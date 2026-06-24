# 阶段 4：AI prompt / eval / agent workflow 研发规范 v0.1

## 目标

给一人公司定义一条默认 AI 能力研发路径：任何用户可见 AI 行为都从 OpenSpec 需求开始，先写 prompt/eval artifacts，再实现模型调用、工具、结构化输出、trace 和安全边界。目标不是追逐“最强 agent”，而是让 AI 行为能被版本化、回归测试、观察、回滚。

## 本阶段只解决什么

- prompt、工具说明、输出 schema 和 eval fixtures 的仓库落点。
- prompt/eval 先行的实现顺序。
- 单次模型调用、workflow、agent 的升级判断。
- 结构化输出、工具权限、prompt injection 和人工复核边界。
- 一人公司可执行的最小 AI 质量门禁。

不在本阶段展开：完整 RAG 平台、向量库选型、finetuning、复杂多 agent 组织、实时语音、多模态产品、成本平台、供应商抽象层。这些需要时单独开 OpenSpec change。

## 依据转译

- 《人月神话》：AI 模型、agent 框架和 prompt optimizer 都不是银弹。规范必须压住“换模型就解决”的幻觉。
- 小型项目管理：只保留能减少返工的工件：prompt、schema、eval cases、run log、风险边界。
- OpenAI Prompt Engineering：prompt 是工程资产；指令、示例、格式和缓存位置都会影响稳定性、成本和延迟。
- OpenAI Evaluation Best Practices：eval 应贴近真实任务，优先分类、打分、pairwise、criteria-based 判断，而不是只看开放式生成感觉。
- OpenAI Agent Evals：早期用 traces 调试行为；当“好”的定义稳定后，再把样例迁移到 datasets 和 eval runs。
- OpenAI Agents：一次模型调用加工具和应用逻辑足够时用 Responses API；需要应用拥有编排、工具执行、审批和状态时再用 Agents SDK。
- OpenAI Safety：不把不可信输入塞进 developer message；用 structured outputs 收窄数据流；高风险输出需要 human-in-the-loop。
- Anthropic Agents：先用简单 prompts/workflows，复杂 agent 只有在可度量改善结果时才升级。
- Google Rules of ML：第一版 AI 能力要简单，先把 pipeline、good/bad 定义和集成做好。
- Google SRE：上线后至少看 latency、traffic、errors、saturation；AI 还要看质量回归和人工介入率。

## 默认决策

- 新 AI 能力默认先做 deterministic workflow 或单次 Responses API 调用；不默认 autonomous agent。
- prompt 必须进入仓库，不只留在 Playground、Dashboard、聊天记录或个人笔记。
- eval fixtures 必须先于 prompt/model 改动落地。
- 输出需要给程序消费时，默认 Structured Outputs / JSON schema；不默认让下游解析自由文本。
- 工具调用默认最小权限、显式参数、结构化返回和可审计日志。
- 旧 OpenAI Evals platform 不作为长期唯一依赖。2026-06-23 查到它将在 2026-10-31 只读、2026-11-30 关闭；本规范默认仓库内 fixtures，可选同步到平台 datasets/traces。
- 模型默认值不写死在散落代码里，必须集中配置并记录变更原因。

## AI artifact 目录规范

推荐落点：

```text
ai/
  prompts/<capability>/prompt.md
  evals/<capability>/cases.jsonl
  evals/<capability>/rubric.md
  evals/<capability>/runbook.md
  schemas/<capability>.schema.json
  traces/<capability>/.gitkeep
```

一人公司裁剪规则：

- 每个用户可见 AI 能力至少有一个 `<capability>`。
- `prompt.md` 写目标、输入、输出、拒绝/降级策略、示例和版本记录。
- `cases.jsonl` 至少 3 条：1 条 happy path、1 条边界/失败、1 条对抗或 prompt injection。
- `rubric.md` 写可接受输出标准，而不是“看起来不错”。
- `runbook.md` 写如何运行 eval、如何记录结果、失败时如何回滚。
- `schema.json` 只在程序消费结构化输出时必需；若输出是纯展示文本，可在 design 中说明不需要。

## 实现顺序

每个 AI change 默认按这个顺序推进：

1. 写 OpenSpec：用户可见行为、失败模式、不做什么。
2. 写 eval fixtures：`cases.jsonl`、`rubric.md`、`runbook.md`。
3. 写 prompt：`prompt.md`，包含输入契约、输出契约和安全边界。
4. 写 schema：需要结构化输出时写 JSON Schema。
5. 写最小模型调用：优先单次调用或固定 workflow。
6. 接入工具：只有真实需要外部数据或副作用时才加工具。
7. 补 trace/log：记录 prompt 版本、model、case id、latency、token/cost、tool calls、结果。
8. 跑本地 eval 和人工抽样 review。
9. 决定是否升级为 agent；只有固定 workflow 不够且 eval 证明收益时才升级。
10. 更新 tasks 和 release note。

## prompt 规范

- prompt 文件必须版本化，文件内记录 `version`、`owner`、`last_reviewed`、`model_default`。
- 指令要短、具体、可验证；不要堆历史原因。
- 示例要覆盖常见、边界和拒绝/降级情况。
- 不可信用户输入只能进入 user/input 数据区，不得拼进 developer/system 高优先级指令。
- prompt 不直接包含 secret、API key、内部不可泄露策略或用户隐私样例。
- prompt 改动必须说明关联 eval case 和预期行为变化。

## eval 规范

`cases.jsonl` 每行推荐字段：

```json
{"id":"happy-basic","input":{"text":"..."},"criteria":["..."],"tags":["happy"],"expected_shape":"..."}
```

最低要求：

- 每条 case 有稳定 `id`。
- 每条 case 有输入和验收 criteria。
- 至少一个 `boundary`、`failure`、`adversarial` 或 `injection` 标签。
- 每次 prompt、model、schema、tool 变化都要跑相关 eval。
- eval 失败不能用“模型偶然波动”直接忽略；必须记录原因、是否接受、是否回滚。
- 重要能力保留历史结果，至少记录日期、commit、prompt version、model、通过率、人工备注。

## workflow / agent 升级规则

默认层级：

1. 规则或传统代码能解决：不用模型。
2. 单次模型调用能解决：不用 workflow。
3. 固定步骤能提升质量：用 deterministic workflow。
4. 需要分类分流：用 routing。
5. 需要多个独立视角：用 parallelization。
6. 需要迭代优化且有明确评价标准：用 evaluator-optimizer。
7. 步数不可预知、需要工具探索和恢复：才用 agent。

升级条件：

- 有 eval 或 trace 证明当前层级不足。
- 有明确停止条件、最大迭代次数或人工 checkpoint。
- 工具权限和副作用可审计、可回滚或可人工确认。
- 成本和延迟在产品可接受范围内。

## 工具与安全规范

- 工具名称、参数和描述要像给初级工程师的 docstring 一样清楚。
- 工具参数尽量结构化，避免自由文本承载指令。
- 高风险工具默认 dry-run 或 human approval。
- 写操作工具必须有幂等键、权限检查和审计日志。
- 外部检索内容、网页、邮件、用户文件等都视为不可信输入。
- 工具返回的数据不得直接升级为高优先级指令。
- 结构化输出的 schema 必须设置必要字段和 `additionalProperties: false`。
- 安全测试至少覆盖 prompt injection、越权工具调用、私密数据泄露和拒绝策略。

## 最小运维要求

每个 AI 能力上线至少记录：

- `ai_feature`、prompt version、model、schema version。
- latency、traffic、errors、saturation。
- token/cost 估计或采集计划。
- eval pass rate 或人工抽检通过率。
- fallback/rollback 方式。
- human review rate、tool failure rate、structured output parse failure rate。

## 只问人的关键判断

默认不问：prompt 文件命名、case id、rubric 文案、局部 eval tags、是否用本地 JSONL 存 fixtures。

必须问：

- 是否允许 AI 输出直接触发金钱、数据删除、权限变更、通知发送等副作用。
- 是否处理隐私、医疗、法律、金融、未成年人等高风险内容。
- 是否要把用户数据发给新的模型供应商、外部工具或第三方服务。
- 是否接受更高成本/延迟换取质量。
- 是否上线 autonomous agent，而不是固定 workflow。
- 是否让 AI 输出绕过人工 review 进入生产决策。

## 本阶段 Review A：一人公司可落地性

结论：可落地，但必须坚持“小 eval 先行”，不追求一开始就有完整评测平台。

- `prompt.md + cases.jsonl + rubric.md + runbook.md` 四件套足够让一个人恢复上下文。
- 本地 JSONL fixtures 比平台依赖更稳定，适合长期维护。
- 升级规则能阻止一人公司过早做多 agent 平台。
- 最大摩擦是写 eval 需要纪律；因此需要 skill 和脚本检查最低样例数、边界样例和 prompt 元数据。
- 下一步应在第一个真实 AI 能力上用 `ai-prompt-eval-loop` 生成 artifacts。

## 本阶段 Review B：产品/工程/运维风险

结论：风险边界比前几阶段更关键，尤其是工具副作用、隐私和 prompt injection。

- 已把不可信输入、developer message、结构化输出和工具权限写成硬约束。
- 已避免绑定即将退场的旧 Evals platform，降低未来迁移风险。
- 已把 latency/cost/quality/human review rate 纳入最小运维信号。
- 仍缺具体 OpenAI/Go SDK 模板；后续可在“AI service implementation”阶段补 Go/Kratos adapter。
- 最大风险是用户业务一开始就要求高风险自动化；这必须走人工判断，不默认授权。

## 当前只需要你判断的事项

我建议默认接受：所有用户可见 AI 能力必须先有本地 `ai/evals/<capability>/cases.jsonl`，至少 3 条样例，才能改 prompt/model/tool。只有你明确说某个能力是内部一次性实验时才豁免。

