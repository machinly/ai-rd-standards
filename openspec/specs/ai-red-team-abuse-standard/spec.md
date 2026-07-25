# ai-red-team-abuse-standard 规格

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

Define the minimum one-person-company governance for AI red teaming, abuse cases, adversarial cases, mitigations, and safety release reviews so that AI safety findings become actionable release evidence rather than ad hoc jailbreak attempts.

## Requirements

### Requirement: 用户可见 AI capability 必须定义 ai-safety artifacts

Any user-visible AI capability, prompt/model/tool/RAG/agent change, safety control, or release gate that can affect users MUST define AI red-team and abuse-risk artifacts.

#### Scenario: 新 AI capability 准备公开发布

- GIVEN 一个 AI capability 会产生用户可见输出、调用工具、检索外部内容、处理用户数据、影响权限/钱/通知/删除，或支撑对外 AI 承诺
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `ai-safety/abuse-case-register/<capability>.json`
- AND 创建 `ai-safety/red-team-plan/<capability>.md`
- AND 创建 `ai-safety/adversarial-cases/<capability>.jsonl`
- AND 创建 `ai-safety/mitigation-map/<capability>.md`
- AND 创建 `ai-safety/safety-release-review/<capability>.md`

### Requirement: Abuse case register 必须记录攻击面、风险、缓解和负责人

Abuse case register MUST record capability、owner、surfaces、assets at risk、users and actors、abuse cases、risk matrix、safety controls、policy refs、human checkpoint 和 review cadence。

#### Scenario: Reviewer 判断 capability 的滥用风险

- GIVEN AI release evidence 引用了某个 capability
- WHEN reviewer 打开 `ai-safety/abuse-case-register/<capability>.json`
- THEN 能看到 abuse cases 的 category、OWASP/MITRE/internal risk mapping、severity、likelihood、affected surface、attacker goal、expected safe behavior、mitigation、eval reference、owner 和 status
- AND critical/high abuse case 没有 owner、mitigation 和 human checkpoint 时不得 release-ready

### Requirement: Red-team plan 必须定义范围、规则、数据处理、停止条件和报告方式

Red-team plan MUST define scope、goals、non-goals、test surfaces、risk categories、roles、rules of engagement、data handling、safety controls、stop conditions、reporting、schedule 和 linked artifacts。

#### Scenario: 执行红队前准备测试

- GIVEN 一次 AI 红队、对抗测试或 abuse-risk review 即将开始
- WHEN 使用 `ai-safety/red-team-plan/<capability>.md`
- THEN tester 能知道测什么、不测什么、如何记录、何时停止、如何处理敏感数据、发现交给谁
- AND 不允许未经授权攻击真实第三方系统或保存可直接滥用 payload

### Requirement: Adversarial cases 必须使用稳定 JSONL schema

Adversarial cases MUST be JSONL and each row MUST include id、capability、attack_family、risk_category、input_ref 或 redacted_input、expected_safe_behavior、policy_ref、mitigation_ref、eval_dataset_ref、severity、source、tags、created_at、reviewed_by、status 和 linked_finding。

#### Scenario: Safety eval 读取对抗样本

- GIVEN release gate 或手工安全复查使用 `ai-safety/adversarial-cases/<capability>.jsonl`
- WHEN 逐行解析 JSONL
- THEN 每行是 JSON object
- AND 每行有稳定 id、风险分类、预期安全行为、策略/缓解/eval 引用、严重度、来源、reviewer 和状态
- AND 不保存完整 raw exploit、secret、未脱敏用户数据或可直接滥用 payload

### Requirement: Mitigation map 必须把风险连接到具体控制

Mitigation map MUST define scope、controls、prompt/policy controls、input/output moderation、tool/permission controls、data/retrieval controls、rate/cost controls、human review、telemetry/abuse monitoring、known gaps 和 linked artifacts。

#### Scenario: 高风险 finding 需要缓解

- GIVEN red-team finding 或 abuse case 需要缓解
- WHEN 更新 `ai-safety/mitigation-map/<capability>.md`
- THEN 能看到 prompt、moderation、tool、retrieval、output handling、rate/cost、human review 和 telemetry 中哪些控制负责
- AND known gaps 连接 owner、release review 或后续 OpenSpec change

### Requirement: Safety release review 必须记录发现、缓解、证据、剩余风险和发布决定

Safety release review MUST define recent changes、red-team findings、critical/high findings、mitigation status、eval evidence、residual risk、user reporting、incident linkage、human checkpoints、release decision 和 next one change。

#### Scenario: 发布前做 AI safety gate

- GIVEN capability 有新的 prompt、model、tool、RAG corpus、agent policy、moderation threshold 或 safety control 变化
- WHEN 更新 `ai-safety/safety-release-review/<capability>.md`
- THEN reviewer 能看到 critical/high findings 是否缓解、eval evidence、剩余风险、用户报告入口、事故链接和 release decision
- AND release decision 只允许 `ship`、`ship-with-risk-acceptance` 或 `block`

### Requirement: Critical/high finding 必须阻塞或明确风险接受

Unresolved critical finding MUST block release. Unresolved high finding MUST block release unless explicit human risk acceptance records owner, mitigation, telemetry, rollback, and expiry.

#### Scenario: 高危发现仍未缓解

- GIVEN abuse case、red-team finding 或 adversarial case 标为 critical 或 high
- WHEN 准备发布 capability
- THEN safety release review 的 release decision 为 `block`
- OR release decision 为 `ship-with-risk-acceptance` 且 human checkpoint 记录 owner、原因、临时缓解、监控、回滚和过期日期

### Requirement: 高权限工具和 autonomous agent 必须人工 checkpoint

AI tools or agents that can spend money, delete data, change permissions, send external notifications, write to third-party systems, perform irreversible operations, or operate autonomously MUST require human checkpoint and mitigation mapping.

#### Scenario: AI agent 获得写操作或高风险工具

- GIVEN AI workflow 将新增或扩大工具权限、agent autonomy 或后台操作能力
- WHEN 更新 abuse case register、mitigation map 和 safety release review
- THEN `human_checkpoint.required_for` 包含对应高风险动作
- AND mitigation map 记录 dry-run、human approval、authorization、idempotency、audit log、rollback 或 kill switch

### Requirement: AI safety artifacts 不得保存敏感或可直接滥用内容

AI safety artifacts MUST NOT store secrets, production tokens, private keys, supplier credentials, unredacted user data, raw exploit payloads, full harmful instructions, system prompt secrets, vulnerability reproduction details, or payment data.

#### Scenario: 记录红队发现和对抗样本

- GIVEN 需要保存 red-team finding、对抗输入、用户报告或安全漏洞证据
- WHEN 写入 `ai-safety/` artifacts
- THEN 使用 redacted input、synthetic proxy、finding id、controlled attachment reference 或最小摘要
- AND 不保存 secrets、生产 token、私钥、未脱敏用户数据、完整可滥用 payload、系统提示秘密、漏洞复现细节或支付数据
