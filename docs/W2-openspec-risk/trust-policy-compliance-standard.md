# 信任政策、用户承诺与合规声明规范
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/one-person-ai-rd-operating-model.md 的场景触发规范命中“隐私页、条款、AI disclosure、退款、安全、合规或用户承诺”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/one-person-ai-rd-operating-model.md。
## 目标

一人公司做 AI 产品时，很多风险不是来自代码，而是来自对用户说了做不到的话：宣传“完全准确”、隐私页说“不用于训练”但供应商设置没验证、AI 页面没说明限制、删除请求没有流程、服务条款和产品行为对不上。本触发专项定义信任政策、用户承诺与合规声明规范，让每个生产 target 都能回答：我们承诺了什么，证据在哪里，用户怎么知道 AI 在工作，数据怎么用，用户权利怎么处理，什么时候必须找人判断或专业意见。

默认原则：承诺即接口。凡是写给用户、客户、审核方或市场的声明，都要能连接到代码、配置、供应商条款、数据记录或人工流程。

## 核心依据

- 《人月神话》：承诺、需求和实现之间的概念不一致会制造长期成本；信任文档不是文案，而是系统边界。
- 小型项目管理：一人公司不能维护厚重 GRC；只保留承诺、政策、AI disclosure、数据权利和复盘五个可执行工件。
- NIST Privacy Framework：隐私风险管理用于在创新产品中识别和管理个人隐私风险。
- GDPR Article 5 / CCPA：透明、公平、数据最小化、保留限制、访问/删除/更正/选择退出等权利是常见隐私基线。
- FTC AI guidance / enforcement：AI 不是法律例外；AI 能力、比较优势、隐私和数据用途声明需要证据，不能误导或遗漏重要事实。
- OECD AI Principles：AI 系统应尊重人权和民主价值，提供透明和可挑战的结果，并具备稳健、安全和问责机制。
- NIST AI RMF / Generative AI Profile：生成式 AI 的信任风险要在设计、开发、使用、评估和持续管理中处理。
- OpenAI Usage Policies / Safety Best Practices / Data Processing Addendum：应用必须遵守模型供应商使用政策、安全实践、数据处理角色和数据控制边界。
- Google People + AI Guidebook：用户需要正确心理模型、解释、反馈与控制，而不是只看到“AI magic”。
- OpenAI system cards / model cards 思想：AI 能力、限制、安全评估和已知风险应以可理解方式对内外说明。

## 范围

适用对象：

- 官网、landing page、pricing page、help center、privacy policy、terms、acceptable use policy、AI disclosure、security page。
- 产品内 AI 提示、免责声明、能力声明、限制说明、用户权利入口、数据删除/导出流程。
- OpenAI 或其他模型供应商、analytics、support、billing、logging、monitoring、customer communication 中涉及用户数据的声明。
- 涉及医疗、法律、金融、就业、教育、身份、未成年人、个人数据、敏感数据、高影响决策或自动化建议的 AI 功能。

不适用对象：

- 正式法律意见、律师审阅、监管申报、合同谈判、DPA/BAA 起草；这些需要专业服务或单独 change。
- 已由阶段 10 安全隐私记录覆盖的底层控制；本阶段关注“对外承诺和实际行为是否一致”。
- 纯内部实验且不对外展示、不处理真实用户数据、不影响用户权益的原型。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
trust/
  commitment-register/<target>.json
  policy-surfaces/<target>.md
  ai-disclosure/<target>.md
  data-rights/<target>.md
  compliance-review/<target>.md
```

### `trust/commitment-register/<target>.json`

承诺注册表必须包含：

- `target`
- `owner`
- `audiences`
- `claims`
- `evidence`
- `policy_dependencies`
- `supplier_dependencies`
- `regulated_domains`
- `human_checkpoint`
- `review_cadence`

`claims` 每项至少包含：

- `id`
- `surface`
- `claim_text`
- `claim_type`
- `risk_level`
- `evidence_ref`
- `owner`
- `last_verified`
- `status`

`claim_type` 默认包含：

- `ai_capability`
- `ai_limitation`
- `privacy_data_use`
- `security`
- `reliability_slo`
- `billing_or_refund`
- `human_review`
- `compliance_boundary`

默认：

- 任何 “always”、 “guaranteed”、 “accurate”、 “secure”、 “private”、 “not used for training”、 “human reviewed”、 “legal/medical/financial grade” 之类强承诺都必须有证据或改写。
- 对外 AI 能力声明必须连接 eval、测试、用户研究、供应商 system card、限制说明或人工流程。
- 没有 evidence 的 claim 只能是 draft，不得进入生产页面。

### `trust/policy-surfaces/<target>.md`

政策页面清单必须包含：

- `Scope`
- `User-Facing Surfaces`
- `Required Policies`
- `Privacy / Data Use`
- `Terms / Acceptable Use`
- `Security Claims`
- `Billing / Refund Claims`
- `Change Notice`
- `Owner And Review Cadence`
- `Linked Artifacts`

默认政策 surface：

- Privacy / data use notice
- Terms or user agreement
- Acceptable use / prohibited use
- AI disclosure / limitations
- Security and vulnerability contact
- Billing, cancellation and refund explanation
- Data deletion/export request path

一人公司可以先用简短页面和明确链接，不要求法律团队级文档；但任何对外页面都要有 owner、更新日期和 linked artifacts。

### `trust/ai-disclosure/<target>.md`

AI 透明度说明必须包含：

- `Where AI Is Used`
- `What AI Can Do`
- `Known Limitations`
- `Human Oversight`
- `User Controls`
- `Data Sent To Models`
- `Safety And Abuse Handling`
- `High Impact Boundaries`
- `Feedback / Appeal`
- `Version And Review`

默认：

- 用户应知道什么时候在和 AI 交互，AI 输出是否可能错误，如何反馈或申诉。
- 涉及钱、权限、法律、医疗、安全、就业、教育、身份、个人重大权益时，必须说明 AI 不是最终决定者或明确人工流程。
- AI disclosure 不得把模型供应商的能力当成自己产品已验证能力。

### `trust/data-rights/<target>.md`

数据权利 runbook 必须包含：

- `Scope`
- `Data Inventory Link`
- `Request Types`
- `Identity Verification`
- `Response Targets`
- `Deletion / Export / Correction`
- `Opt-Out / Consent`
- `Processor / Supplier Handling`
- `Exceptions`
- `Audit Trail`
- `Human Checkpoints`

默认：

- 即使早期法律门槛未触发，也要有最小删除/导出/更正/停止使用请求路径。
- 不为了验证身份而收集过量数据。
- 用户数据进入 OpenAI、analytics、support、billing 或 logging 时，必须能从 privacy record 找到处理目的和保留边界。
- 无法完成请求时，要记录原因和用户沟通。

### `trust/compliance-review/<target>.md`

合规复盘必须包含：

- `Recent Changes`
- `Claim Changes`
- `Data Use Changes`
- `AI Policy / Provider Changes`
- `User Rights Requests`
- `Regulated Domain Check`
- `Open Risks`
- `Next One Change`

默认节奏：

- pre-revenue：每月一次或重大页面/数据/AI 变更前。
- 有付费用户：每两周或每次发布前检查 changed claims。
- 涉及敏感数据、高影响领域、政策更新、客户合同、监管问题：立即人工 checkpoint。

## Go / Kratos / sqlc / gRPC 默认规则

- 对外承诺如果依赖后端行为，必须能在 Go/Kratos 服务或配置中找到证据，例如 data retention、delete/export、human review flag、model routing、training opt-out。
- gRPC API 不返回未经授权的隐私/合规状态；租户数据权利请求必须绑定 actor 和 tenant。
- sqlc 表默认包含：`trust_claims`、`policy_versions`、`data_rights_requests`、`consent_records`、`ai_disclosure_versions`。
- 数据删除、导出、更正、consent/opt-out 必须有审计和状态机。
- 供应商政策或 OpenAI usage policy 变更影响产品行为时，走 OpenSpec change。

## Vite 前端默认规则

- Privacy、Terms、AI disclosure、security contact、billing/refund、data rights 入口必须可被用户找到，不藏在只有 footer 小字的深链。
- AI 功能旁边应有轻量说明或链接：AI 会做什么、可能错在哪里、如何反馈。
- 表单收集个人数据时说明用途、必要性和保留或链接政策。
- 不使用营销化 hero 文案承诺未验证的准确率、节省比例、收入增长、法律/医疗/财务效果。
- 使用 Vercel/Geist 风格时保持清晰层级、克制措辞和可扫描布局，避免暗色小字掩盖重要限制。

## AI workflow 默认规则

- Prompt、eval、model routing、safety filters、human review、fallback 和 logging 设置是 AI disclosure 的证据来源。
- 高风险 claim 需要 eval 或人工验收支持；不能只用供应商模型名称背书。
- OpenAI usage policy、safety best practices、moderation 和 data processing terms 进入 release checklist。
- 对用户可见 AI 输出不得假装人类、专业人士或权威机构；如需专业建议，必须有适当专业参与或明确边界。
- 用户反馈、appeal 和 harmful output report 必须连接阶段 23 支持信任运营与阶段 4 eval。

## 需要人判断的关键点

只把这些判断交给人：

- 是否发布新的隐私、条款、可接受使用、AI disclosure、退款、安全或合规承诺。
- 是否宣称 AI 具备专业级、自动决策、高准确率、合规、无训练、无保存、无人工查看或高可用能力。
- 是否处理敏感个人数据、未成年人、高影响领域、受监管行业或跨境/区域数据要求。
- 是否改变数据用途、训练/保留、供应商、analytics/support/logging 数据流或用户权利流程。
- 是否接受无法证明的 claim、政策和实现不一致、或用户权利请求无法履行。
- 是否需要律师、隐私专业人士、安全评估或客户合同审阅。

其他字段完整性、章节、承诺证据、敏感内容、OpenAI/供应商政策链接、review 节奏由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“承诺了什么、页面在哪里、AI 怎么解释、用户权利怎么处理、多久复盘”。
- 保留：人只判断强承诺、敏感数据、高影响领域、用户权利无法履行、供应商数据用途变化和专业审阅。
- 调整：不要求一开始写完整法律文书；先建立承诺和证据的映射，法律文本需要时再审。
- 调整：不让每次文案微调都进合规会；只有 claim 类型、风险级别或用户数据用途变化才升级。
- 风险：团队容易把免责声明当安全控制。缓解：`claim.evidence_ref` 必须链接代码、配置、eval、policy version 或 runbook。

结论：可落地。一个人可以先列出 10 到 20 个对外 claim，删除或降级没有证据的强承诺，再把剩余承诺挂到真实工件上。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：AI disclosure 帮用户建立正确心理模型，减少误用和支持负担。
- 工程角度：承诺必须连接 Go/Kratos 配置、sqlc 状态机、eval、release gate 或供应商设置。
- 运维角度：政策变更、OpenAI usage policy 变更和用户权利请求都有 review 和 runbook。
- 安全隐私角度：隐私、数据最小化、保留、删除/导出、更正、供应商处理和敏感数据进入明确边界。
- 成本角度：避免为了未验证营销承诺背上昂贵 SLA、人工审阅或合规义务。

结论：可落地。第 25 阶段把“我们说了什么”和“系统真的怎么做”绑在一起，保护一人公司的用户信任、研发节奏和法律/合规风险边界。


