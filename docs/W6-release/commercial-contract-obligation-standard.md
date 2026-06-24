# W6 Release 触发专项：客户合同、订单、SLA 与商业承诺治理规范

## W6 触发定位

本文件是 W6 Release 的触发型专项，不是 W6 主入口。只有当当前工作涉及客户合同、订单、报价、SLA、服务积分、DPA、安全附件、销售承诺、非标准条款或商业义务时，才需要读取本文件。

普通 W6 发布入口应先回到 `docs/W6-release/main.md`，由主入口判断是否触发本专项。

## 目标

一人公司做 AI 产品时，最危险的工程风险之一不是“代码不会写”，而是合同、订单、报价、SLA、销售邮件、官网承诺和真实系统能力不一致：答应 24/7 支持但没有值班；签了 99.99% SLA 但没有 SLO；承诺数据驻留但供应商链路跨境；保证 AI 输出准确但没有 eval；给了服务积分但计费系统没有 credit ledger。本专项的目标是把客户合同和商业承诺转成可版本化、可验证、可复盘的工程义务。

本专项不是法律意见；它只定义研发和运营如何管理“已经或可能被承诺的东西”。正式合同、条款解释、赔偿、法律合规和争议处理仍需要专业审阅。

## 核心依据

- 《人月神话》：概念完整性来自少数一致决策。合同承诺也是产品接口；如果销售条款、产品能力、SRE 指标、计费权益和 AI 行为各说各话，后期会形成昂贵的概念债。
- 小型项目管理：一人公司不能维护大型法务/销售运营体系；只保留能阻止错误承诺上线的最小工件，并把人的判断留给高风险偏离。
- Getting to Yes / BATNA：红线谈判要先知道可接受范围、替代方案和 walk-away 条件；不要在客户压力下临时发明不可交付的义务。
- NCMA Contract Management Standard：合同管理覆盖 pre-award、award、post-award；合同成功依赖双方清楚理解任务、能力和交付物。
- Cornell LII contract 基础：合同会创造可执行的相互义务。工程规范不判断法律效力，但必须把承诺当成可能需要履行的义务来管理。
- WorldCC Contract Design Pattern Library：合同需要可读、可理解、可被执行；一人公司尤其需要把条款转换为行动清单，而不是只存 PDF。
- Common Paper Cloud Service Agreement / Service Level Agreement / DPA / NDA：SaaS 合同通常由 cover page、order form、key terms、standard terms 和链接政策组成；这些结构适合作为早期标准条款基线。
- Google SRE SLO/SLA：SLO 是用 SLI 衡量的目标；SLA 是带法律或商业后果的协议。默认先有 SLO、观测和 error-budget 处理，再考虑 SLA 或服务积分。
- OpenAI Services Agreement / DPA / Service Terms / Usage Policies：AI 供应商条款会影响数据处理、beta 服务、输出权利、使用限制和赔偿边界；你不能对客户承诺供应商没有给你的能力。
- W7 SRE、W4 计费权益、W2 信任政策、W2 供应商处理方和 W2 IP 来源已经定义了底层证据；本专项负责把这些证据绑定到客户承诺。

## 范围

适用对象：

- SaaS / API / AI workflow 的客户主协议、订单、报价、SOW、设计伙伴协议、DPA、安全附件、支持政策、SLA、服务积分、续费和取消条款。
- 官网、销售材料、帮助中心、定价页、控制台文案、邮件模板、客服回复中可被客户理解为承诺的内容。
- Go/Kratos/sqlc/gRPC 后端能力、Vite 前端展示、AI prompt/eval/model routing、供应商条款、观测、计费、支持和安全证据之间的映射。

不适用对象：

- 正式法律审查、合同起草、争议处理、税务、会计收入确认、保险、融资条款、并购或雇佣合同。
- 全量 CLM、CRM、CPQ、法律知识库或 enterprise sales ops 平台。
- 把合同条款直接塞进代码；工程系统只记录可执行义务、证据和人工检查点。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
commercial-contracts/
  obligation-register/<target>.json
  agreement-map/<target>.md
  sla-service-credit/<target>.json
  redline-playbook/<target>.md
  contract-review/<target>.md
```

### `commercial-contracts/obligation-register/<target>.json`

义务登记表必须包含：

- `target`
- `owner`
- `contract_surfaces`
- `obligations`
- `dependencies`
- `human_checkpoint`
- `review_cadence`
- `status`

`obligations` 每项至少包含：

- `id`
- `customer_segment`
- `source_doc`
- `clause_ref`
- `obligation_type`
- `commitment_text`
- `engineering_evidence_ref`
- `owner`
- `due_or_window`
- `measurement`
- `exception_or_exclusion`
- `operational_runbook_ref`
- `risk_level`
- `status`

默认 `obligation_type`：

- `availability_sla`
- `uptime_credit`
- `support_response`
- `security`
- `privacy_dpa`
- `data_residency`
- `deletion_export`
- `ai_training_use`
- `ai_accuracy_limit`
- `human_review`
- `billing_payment`
- `renewal_cancel`
- `indemnity_ip`
- `audit_evidence`
- `integration_delivery`
- `professional_services`
- `custom_feature`
- `termination_export`
- `acceptable_use`
- `confidentiality`

默认规则：

- 没有证据链接的承诺不得进入合同、订单、官网、销售邮件或客户控制台。
- `risk_level=high` 的义务必须有 `human_checkpoint`，并链接 W7 SRE-lite、W4 计费、W2 信任政策、W2 供应商处理方和 W2 IP 来源中的相应证据。
- 客户特例不得只存在于聊天、邮件或 Linear 票据；必须进入义务登记表。
- 承诺的 owner 默认是创始人本人；不能虚构“法务/客服/值班团队”。

### `commercial-contracts/agreement-map/<target>.md`

协议地图必须包含：

```markdown
# <target> Agreement Map

## Scope

## Standard Forms

## Order Forms

## Linked Policies

## DPA / Security / Subprocessors

## SLA / Support

## Product / Entitlement Mapping

## Non-Standard Terms

## Renewal / Cancellation

## Evidence Links

## Review Cadence
```

默认规则：

- 标准合同、订单、DPA、安全页面、子处理方页面、SLA、支持政策、定价页和官网 claim 必须能互相链接。
- Order form 中的 seats、usage、support tier、data region、AI features、retention、服务积分、custom feature 必须能映射到产品 catalog、entitlement、config 或人工 runbook。
- 不把“客户说过/销售说过/我记得”当证据。

### `commercial-contracts/sla-service-credit/<target>.json`

SLA 与服务积分工件必须包含：

- `target`
- `owner`
- `customer_segments`
- `slis`
- `slos`
- `sla_terms`
- `credits`
- `exclusions`
- `measurement_window`
- `dependencies`
- `observability`
- `incident_communication`
- `human_checkpoint`
- `status`

默认规则：

- 没有 SLI、SLO、dashboard、alert、runbook 和 incident communication，就不得签 SLA。
- SLA target 不得高于实际可长期运营的 SLO；一人公司默认从无 SLA、beta SLA 或宽松商业补救开始。
- 服务积分必须能连接W4 计费与权益专项的 billing ledger / credit note / entitlement adjustment；不得只写在邮件里。
- 外部供应商在用户路径上时，OpenAI、支付、邮件、云服务、向量库等依赖必须进入 `dependencies` 和例外条款。
- 99.9% 以上 availability、24/7、P1 响应、严格赔偿、自动退款、无排除项都需要人工判断。

### `commercial-contracts/redline-playbook/<target>.md`

红线手册必须包含：

```markdown
# <target> Redline Playbook

## Scope

## Standard Position

## Acceptable Without Review

## Needs Human Review

## Walk-Away Terms

## Fallback Language

## Evidence Required

## Legal Review Triggers

## Negotiation Notes

## Review Cadence
```

默认规则：

- 低风险条款可以预设接受范围；高风险条款必须升级给人。
- 红线不是“客户越大越让步”，而是先看是否有证据、系统能力、供应商支持、保险/现金承受力和可执行 runbook。
- Fallback language 只写方向，不在规范里给法律模板。
- 每次接受非标准条款，都要在 obligation register 和 agreement map 中留下痕迹。

高风险红线默认包括：

- 无限责任、uncapped liability、间接损害扩大、strict liability。
- 99.99%、24/7、P1 15 分钟响应、无维护窗口、无供应商例外的 SLA。
- AI 输出准确性、合规性、专业意见、无幻觉、无第三方权利风险的保证。
- “不用于训练”“零保留”“数据驻留”“专属环境”“客户自定义删除期限”超出实际供应商和架构能力。
- 宽泛 indemnity、source code escrow、MFN、独家、无限审计、客户单方变更安全要求。
- SOC 2、ISO 27001、HIPAA、PCI、BAA、政府/医疗/金融监管声明超出已有证据。

### `commercial-contracts/contract-review/<target>.md`

合同复盘必须包含：

```markdown
# <target> Contract Review

## Recent Changes

## New Customers / Order Forms

## Obligation Changes

## SLA / Support Commitments

## Data / AI / Security Terms

## Billing / Renewal Terms

## Redlines / Exceptions

## Incidents / Breaches

## Open Risks

## One Next Change

## Review Cadence
```

默认节奏：

- pre-revenue：每月一次，或每次对外改 pricing / terms / DPA / SLA / security / support claim 前。
- 有付费客户：每个新订单、非标准条款、SLA/support 变更、安全/隐私承诺变更、AI provider 条款变化后复盘。
- enterprise prospect：发出红线、SOW、DPA、安全问卷或 SLA 前复盘。

## Go / Kratos / sqlc / gRPC 默认规则

- 合同义务中影响产品行为的内容必须映射到后端事实源：product catalog、entitlement、tenant settings、feature flags、data region、retention policy、support tier、SLO config 或 audit evidence。
- 可选数据库表：`contract_obligations`、`customer_terms`、`sla_commitments`、`service_credits`、`redline_exceptions`、`contract_reviews`。使用 sqlc 生成类型安全查询。
- gRPC API 可以暴露 `GetCustomerContractProfile`、`GetEntitlementStatus`、`ListSlaCommitments`、`RecordServiceCredit` 等内部接口，但不得让浏览器自行决定客户是否享有特殊条款。
- SLA measurement 来自观测系统，不来自人工猜测；服务积分来自计费 ledger，不来自手工退款记忆。
- 合同特例必须能被 trace 到 customer/tenant/order，而不是散落在 config、support note、Slack 或邮件。

## Vite 前端默认规则

- 定价页、取消/续费、SLA/support tier、AI disclosure、DPA、安全承诺和客户控制台展示必须来自同一事实源或明确链接对应 policy。
- 不在 UI 中承诺“无限”“实时”“保证准确”“永久免费”“随时删除”“不训练”“企业级安全”“24/7”这类词，除非 obligation register 有证据。
- 客户控制台只展示当前客户真实享有的计划、权益、SLA、support tier、data region、DPA 状态和服务积分，不展示营销式泛承诺。
- Vercel/Geist 风格用于清晰信息层级和克制状态表达；合同/权益/信用额度界面优先可扫描表格、状态徽标和明确操作记录。

## AI workflow 默认规则

- AI 能力的客户承诺必须连接 W3 prompt/eval、数据集、红队、model routing、tool runtime、RAG，以及 W2 vendor 和 IP evidence。
- 不承诺 AI 输出“总是正确”“可替代专业意见”“无版权/隐私/安全风险”“不会泄露”“永不使用客户数据训练”，除非对应技术、供应商和政策证据已存在。
- Beta、preview、experimental AI 功能默认不得纳入强 SLA、赔偿或合规保证。
- 客户要求 human review、data retention、training opt-out、model/provider restriction、region restriction、audit evidence 时，必须落到配置、runbook 或供应商合同边界。

## 需要人判断的关键点

默认不问：低风险标准条款、字段命名、无 SLA 的免费/beta 试用、普通月付/年付订单、已在 W4 计费、W2 信任政策和 W2 供应商处理方专项覆盖的标准说明。

必须问：

- 是否接受非标准客户条款、侧信、销售邮件承诺或 SOW。
- 是否承诺 99.9% 以上可用性、24/7、P1/P2 响应、服务积分、自动退款或无维护窗口。
- 是否承诺数据驻留、零保留、不训练、专属环境、客户指定供应商、删除/导出时限或跨境限制。
- 是否承诺 AI 准确性、专业合规、无幻觉、无 IP 风险、人工复核或特定模型/供应商。
- 是否接受 uncapped liability、宽泛 indemnity、source code escrow、MFN、独家、无限审计、监管级合规或安全保证。
- 是否把官网、销售材料、客服模板或控制台文案改成强承诺。
- 是否需要律师、保险、专业合规、客户安全审查或供应商合同升级。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“承诺是什么、协议在哪里、SLA 怎么量、红线怎么判、多久复盘”。
- 保留：人的判断只放在非标准条款、强 SLA、责任/赔偿、数据/AI/安全强承诺和供应商能力边界。
- 调整：不要求引入 CLM/CRM/CPQ；先用仓库工件和 verifier 管住真实承诺。
- 调整：不把合同文本复制入仓库；只登记工程义务、证据链接和风险状态，降低敏感信息暴露。
- 风险：义务登记可能被遗忘。缓解：官网/定价/SLA/support/DPA/AI claim 改动时，把 verifier 作为研发 gate。

结论：可落地。一个人可以先管理标准合同和前几个客户订单，把所有强承诺拦在“证据是否存在”这一关。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：防止为了成交承诺不存在的功能、支持等级、数据边界或 AI 能力。
- 工程角度：合同义务映射到 Go/Kratos/sqlc/gRPC 的事实源，减少“客户特例靠记忆”的隐性复杂度。
- 运维角度：SLA 必须建立在 SLO、观测、runbook、incident communication 和供应商依赖之上。
- 安全隐私角度：DPA、数据驻留、训练/保留、子处理方和 audit evidence 与 W2 供应商/信任承诺和 W9 审计证据连起来。
- 成本角度：24/7、高 SLA、专属环境、无限审计和服务积分会带来真实现金/时间成本，必须先算承受力。

结论：可落地。本专项把“商业承诺”变成研发输入和上线 gate，而不是客户签完后才发现系统不能履行。
