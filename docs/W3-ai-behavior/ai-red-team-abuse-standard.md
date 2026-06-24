# AI 红队、滥用场景与对抗样本治理规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/main.md` 已经判断需要红队、滥用场景、对抗样本、mitigation 或安全发布审查时，才读取本文件。

如果当前只是判断 AI 行为应该如何定义好坏、失败和降级，先回到 `docs/W3-ai-behavior/main.md`。

## 目标

一人公司做 AI 产品时，红队最容易退化成“上线前随手试几个 jailbreak”。这不够。AI 风险既包括传统安全问题，也包括提示注入、敏感信息泄露、工具误用、过度代理、错误输出被下游执行、检索污染、成本消耗、政策绕过和用户伤害。本专项定义 AI 红队、滥用场景与对抗样本治理规范，让每个用户可见 AI capability 都能回答：可能被怎样滥用，哪些攻击面需要测，红队发现如何进入 mitigation 和 release gate，哪些风险必须找人判断。

默认原则：红队不是一次性安全仪式，也不是系统性 eval 的替代品；它负责发现新风险、压力测试缓解措施，并把高价值发现转成可重复的安全样本和发布门禁。

## 核心依据

- 《人月神话》：没有银弹；把 AI 安全寄托在一个万能提示词或一次红队上，会制造更隐蔽的复杂度。
- 小型项目管理：一人公司不能养完整红队组织；只保留 abuse case register、red-team plan、adversarial cases、mitigation map、safety release review 五个可执行工件。
- OpenAI Safety Best Practices / Red Teaming：AI 应用需要 moderation、adversarial testing、human oversight、输入输出限制、用户报告和 safety identifier；红队应覆盖代表性使用和“试图打破系统”的输入。
- OpenAI external red teaming paper：红队可用于发现新风险、压力测试缓解、引入领域专家、形成新的评估指标；但它成本高、不是 panacea，需要转化为自动化 eval 和明确阈值。
- Microsoft AI red teaming guidance：红队应在生命周期中提前规划，先做人工探索，再做系统性度量；测试者需要普通用户视角和对抗视角，计划要定义范围、目标、记录方式和联系人。
- OWASP Top 10 for LLM Applications 2025：提示注入、敏感信息披露、供应链、数据/模型污染、不安全输出处理、过度代理、系统提示泄露、向量/嵌入弱点、错误信息和无界消耗是 LLM 应用常见风险。
- NIST AI RMF / Generative AI Profile / AML taxonomy：AI 风险应按生命周期、攻击阶段、攻击目标和缓解方式管理；生成式 AI 需要预部署测试、内容来源、事故披露和持续测量。
- Google SAIF / AI Red Team：AI 红队需要 AI 领域知识、真实攻击 TTP、传统安全控制和持续 work feed；常见攻击包括 prompt attacks、训练数据提取、backdoor、对抗样本、数据污染和数据外泄。
- Anthropic red teaming language models：红队应同时服务于发现、测量和减少伤害，并透明记录流程、统计方法和不确定性。
- MITRE ATLAS：AI 安全可以借鉴 adversarial tactics、techniques 和 case studies，把发现映射成可防御、可监控的行为。

## 范围

适用对象：

- 用户可见 AI chat、agent、RAG、structured output、工具调用、后台 AI operator、客服/支持 AI、内容生成、代码生成、数据分析和自动化工作流。
- Prompt injection、indirect prompt injection、jailbreak、policy bypass、sensitive information disclosure、system prompt leakage、insecure output handling、tool misuse、excessive agency、vector/embedding weakness、misinformation、cost abuse、unbounded consumption。
- 会影响 W3 prompt/eval、W2 安全隐私、W2 API/tool schema、W8 支持信任运营、W7 后台动作、W2 AI disclosure、W3 red-team dataset 的发现。
- Go/Kratos/sqlc/gRPC 后端中处理 abuse telemetry、safety decision、rate limit、tool authorization、moderation result、red-team finding 的数据结构。
- Vite 前端中用于安全审阅、红队发现分流、用户报告、human review 和 release decision 的页面。

不适用对象：

- 未经授权的真实攻击、漏洞利用、绕过第三方系统、攻击现实目标或生成可直接滥用的 payload。
- 完整企业红队服务、外部审计、合规认证、法律披露流程；这些需要单独专业服务。
- 通用网络安全扫描；W2 覆盖基础安全与供应链，本专项只关注 AI 特有和 AI 放大的滥用风险。

## 最小工件

每个用户可见 AI capability 使用同一个 `<capability>` 文件名：

```text
ai-safety/
  abuse-case-register/<capability>.json
  red-team-plan/<capability>.md
  adversarial-cases/<capability>.jsonl
  mitigation-map/<capability>.md
  safety-release-review/<capability>.md
```

### `ai-safety/abuse-case-register/<capability>.json`

Abuse case register 必须包含：

- `capability`
- `owner`
- `surfaces`
- `assets_at_risk`
- `users_and_actors`
- `abuse_cases`
- `risk_matrix`
- `safety_controls`
- `policy_refs`
- `human_checkpoint`
- `review_cadence`

`abuse_cases` 每项至少包含：

- `id`
- `category`
- `owasp_llm_risk`
- `severity`
- `likelihood`
- `affected_surface`
- `attacker_goal`
- `expected_safe_behavior`
- `primary_mitigation`
- `eval_ref`
- `owner`
- `status`

默认：

- `category` 应优先映射到 OWASP LLM Top 10、MITRE ATLAS 或内部 risk taxonomy。
- `severity` 默认使用 `critical`、`high`、`medium`、`low`、`info`。
- `status` 默认使用 `draft`、`ready`、`blocked`、`mitigated`、`accepted-risk`、`retired`。
- `critical` 或 `high` abuse case 不得在没有 mitigation、owner 和 human checkpoint 的情况下进入生产 release。

### `ai-safety/red-team-plan/<capability>.md`

Red-team plan 必须包含：

- `Scope`
- `Goals`
- `Non-Goals`
- `Test Surfaces`
- `Risk Categories`
- `Roles`
- `Rules Of Engagement`
- `Data Handling`
- `Safety Controls`
- `Stop Conditions`
- `Reporting`
- `Schedule`
- `Linked Artifacts`

默认：

- 先做 30 到 90 分钟的手工探索，再把高价值发现沉淀成 adversarial cases 和 eval。
- 一人公司默认由 founder + Codex 做内部红队；高影响领域、专业领域或安全敏感 release 才找外部专家。
- 计划必须写清不做什么：不攻击真实第三方、不保存真实有害内容、不诱导生成可直接滥用的步骤、不绕过生产访问控制。
- Stop conditions 必须覆盖：真实用户数据暴露、可利用安全漏洞、违法/高危内容、第三方系统风险、测试者心理负担过高。

### `ai-safety/adversarial-cases/<capability>.jsonl`

Adversarial cases 每行是一个 JSON object，至少包含：

- `id`
- `capability`
- `attack_family`
- `risk_category`
- `input_ref` 或 `redacted_input`
- `expected_safe_behavior`
- `policy_ref`
- `mitigation_ref`
- `eval_dataset_ref`
- `severity`
- `source`
- `tags`
- `created_at`
- `reviewed_by`
- `status`
- `linked_finding`

默认：

- 优先保存 `input_ref`、redacted prompt、摘要或 synthetic safe proxy，不保存完整可直接滥用 payload。
- 每个 capability 至少有 prompt injection、sensitive information disclosure、tool/permission misuse 或 equivalent domain risk 的对抗样本。
- `critical` / `high` 样本必须连接 mitigation 和 release review。
- 能转成稳定 eval 的发现进入 W3 数据集专项的 `ai-data/eval-set/`，但安全发现本身保留在 `ai-safety/`。

### `ai-safety/mitigation-map/<capability>.md`

Mitigation map 必须包含：

- `Scope`
- `Controls`
- `Prompt And Policy Controls`
- `Input / Output Moderation`
- `Tool And Permission Controls`
- `Data And Retrieval Controls`
- `Rate / Cost Controls`
- `Human Review`
- `Telemetry And Abuse Monitoring`
- `Known Gaps`
- `Linked Artifacts`

默认 controls：

- Prompt：明确角色、边界、拒绝策略、工具使用条件，不把不可信输入放入高优先级指令。
- Moderation：输入和输出分别考虑；高风险类别使用 block、review、degrade 或 safe completion。
- Tool：最小权限、dry-run、人审、幂等键、tenant/actor authorization、审计日志。
- Retrieval：检索内容视为不可信，标记来源，不让外部文本改写系统指令。
- Output handling：模型输出进入 SQL、shell、HTML、markdown、email、webhook 或第三方 API 前必须验证、转义或结构化解析。
- Cost：对 token、循环、工具 fanout、并发、文件大小和重试设置上限。
- Telemetry：记录安全决策、拒绝原因、risk category、safety identifier、finding id 和 release id，避免记录敏感原文。

### `ai-safety/safety-release-review/<capability>.md`

Safety release review 必须包含：

- `Recent Changes`
- `Red-Team Findings`
- `Critical / High Findings`
- `Mitigation Status`
- `Eval Evidence`
- `Residual Risk`
- `User Reporting`
- `Incident Linkage`
- `Human Checkpoints`
- `Release Decision`
- `Next One Change`

默认：

- `critical` 未缓解：阻塞发布。
- `high` 未缓解：默认阻塞；只有明确 accepted-risk、降级方案、监控和 owner 时才可发布。
- `medium` 可带行动项发布，但必须进入 mitigation map 或 backlog。
- Release decision 只允许 `ship`、`ship-with-risk-acceptance`、`block`。
- 用户报告入口必须连接 W8 支持信任运营；重大安全发现连接 W2 安全隐私、W7 后台动作和 W2 信任承诺。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端服务必须把 AI safety decision 当作业务状态记录：allow、block、review、degrade、rate-limit、tool-deny。
- sqlc 表默认包含：`ai_abuse_cases`、`ai_safety_findings`、`ai_safety_decisions`、`ai_tool_safety_reviews`、`ai_abuse_reports`。
- gRPC 方法处理 AI 工具调用前必须校验 actor、tenant、capability、tool permission、idempotency key 和 risk level。
- Safety identifier 使用稳定、隐私保护的 user/session hash；不得把 email、手机号或真实姓名直接发给模型供应商。
- Moderation、rate limit、tool deny 和 human review 结果应能关联 release id、prompt version、model id、tool schema version、finding id。
- 红队发现中的真实 payload、用户原文或安全漏洞细节不默认进应用日志；用 finding id 和受控附件引用。

## Vite 前端默认规则

- 用户报告入口应可见，能报告 harmful output、privacy leak、unsafe advice、tool mistake、billing/cost anomaly 和 account abuse。
- 内部安全审阅 UI 保持工作台形态：severity、category、affected surface、mitigation status、owner、release decision 同屏可见。
- 展示红队样本时默认 redacted；查看完整敏感内容需要权限、理由和审计。
- 对用户可见的 AI 限制说明要清楚但不过度暴露系统提示或绕过策略。
- 使用 Vercel/Geist 风格时保持克制、清晰、可扫描，危险状态使用明确文案和颜色 token，不用装饰性效果掩盖风险。

## AI workflow 默认规则

- 改 prompt、model、tool、RAG corpus、agent policy、moderation threshold 或 safety control 前，必须检查相关 abuse case 和 adversarial cases。
- 对抗发现先进入 `ai-safety/`，再按价值转为 `ai-data/` 的 red-team eval case；不要把所有红队输入直接塞进训练或 prompt examples。
- Red-team pass 不等于安全；它只证明当前范围内没有发现阻塞问题。
- 自动化红队工具只能补充，不替代人工问题定义、scope、risk acceptance 和 release decision。
- 高风险工具和 autonomous agent 默认需要 dry-run、人审、审计、回滚和 kill switch。

## 需要人判断的关键点

只把这些判断交给人：

- 是否发布存在未缓解 `critical` / `high` finding 的 AI capability。
- 是否接受 `ship-with-risk-acceptance`。
- 是否把真实攻击 payload、真实用户有害内容、敏感样本或安全漏洞细节写入 artifacts。
- 是否邀请外部红队、领域专家或披露安全发现。
- 是否改变 moderation threshold、policy boundary、refusal boundary 或 safety control。
- 是否给 AI agent 开放写操作、金钱、权限、删除、外部通知、第三方写入或后台操作。
- 是否公开红队结果、复现步骤、系统提示细节或模型/供应商弱点。
- 是否处理高影响领域、未成年人、安全、医疗、法律、金融、就业、教育、身份或公共安全相关 capability。

其他字段完整性、章节、JSONL 格式、状态枚举、敏感内容扫描、必需 checkpoint、OpenSpec linkage 和 positive/negative fixture 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“会怎样被滥用、怎么测、样本在哪里、怎么缓解、能不能发布”。
- 保留：人只判断未缓解高危发现、风险接受、真实攻击样本、外部披露、安全阈值和高权限 agent。
- 调整：不要求正式红队团队；一开始用 founder + Codex + 90 分钟计划化探索。
- 调整：不保存完整可滥用 payload；用 redacted/synthetic proxy 和 finding id 管理风险。
- 风险：红队发现容易停在文档里。缓解：每个 finding 必须连接 mitigation、eval evidence、owner 和 release decision。

结论：可落地。一个人可以先为最重要 AI capability 建 8 到 15 个 abuse cases，做一轮手工红队，再把最高价值 3 到 5 个发现转成稳定 adversarial cases。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户报告和红队发现连接起来，避免只看内部理想路径。
- 工程角度：abuse case、finding、mitigation、eval、release id 可追踪，便于复现和回滚。
- 运维角度：critical/high finding 有阻塞规则，safety decision 与 telemetry 能支撑事故响应。
- 安全隐私角度：覆盖 OWASP LLM、prompt injection、敏感信息泄露、过度代理、工具滥用和检索污染。
- 成本角度：先用小范围手工红队和少量高价值样本，避免一开始采购昂贵外部红队或跑大规模自动攻击。

结论：可落地。本专项把“AI 安全感觉还行”压成可审查的 abuse case、对抗样本、缓解映射和发布决定，同时保留一人公司能承受的流程重量。
