# 定义

## 项目目的与边界

定义把已选中的问题或结果转化为本轮可交付的产品行为、范围、验收、指标、风险边界和退出方式。它确定“交付什么”和“哪些条件下不得继续”，但不替代体验设计、系统方案、工程排期、实现、验证、发布或运行；后续项目消费这里的决定并回传证据，不得各自重写产品含义。

## 根本原则

- **ITEM-DEFINITION-001**：定义产品变化时，应同时明确要改变的行为与明确不改变的范围。

## 核心判断

<!-- rule-id: DEFINITION-HUMAN-PRODUCT-DECISION -->
- 目标用户、产品方向、当前最重要结果，以及目标用户和痛点是否足够具体，必须由人作出判断；自动化只能整理材料或提出选项。

<!-- rule-id: DEFINITION-PRODUCT-SCOPE -->
- 定义本轮产品变化时，同时写明要改变的行为与明确不改变的部分，避免用功能名称代替范围。

<!-- rule-id: DEFINITION-IMPLEMENTATION-READINESS -->
- Standard 或 High-risk 的实现性工作只有在风险边界、验收要求和退出条件都已明确时才能进入实现。

<!-- rule-id: DEFINITION-PRODUCT-ROUTING -->
- 目标用户、问题、证据、成功指标、学习决定或产品方向不清时返回调研；投入价值或 appetite 不成立时返回选题停车、终止或补证据。实现或质量结果推翻这些前提时同样回退，不得在定义、AI 或实现项目中继续猜测。

<!-- rule-id: DEFINITION-AI-ENTRY -->
- 只有已经确认会改变用户可见 AI 行为、相关输入或风险边界时才进入 AI 定义；AI 专项不取代前置风险判断。用户可见行为由本项目定义，交互感知转交[体验设计](04-experience-design.md)，模型、工具、RAG、记忆与 eval 方案转交[技术设计](../03-engineering-delivery/05-technical-design.md)，不再以旧阶段资料作为操作入口。

<!-- rule-id: DEFINITION-AI-APPLICABILITY -->
- 下列变化进入 AI 行为定义：prompt 或 developer/system 指令、工具描述或调用、agent/workflow、RAG 与引用、记忆、内容审核或政策、模型或优化、多语言和本地化，以及 chat、assistant、agent、客服 AI、问答、内容/代码生成、数据分析、后台 operator 和自动化 workflow。即使产品表面不变，只要输出质量、安全拒绝、个性化、供应商、token 成本或延迟发生变化，也属于该范围。

<!-- rule-id: DEFINITION-AI-BEHAVIOR-CONTRACT -->
- 每个用户可见 AI 能力在实现前定义目标、失败、拒绝和降级四类行为；其中任何一类未定义，都不能用模型调用或 prompt 细节补位。

<!-- rule-id: DEFINITION-COMMERCIAL-BOUNDARY -->
- 改变产品方向、目标用户、定价、套餐、计费、对外承诺或客户合同边界，必须由人决定；用户可见行为的实质变化也不能由实现者静默确定。

<!-- rule-id: DEFINITION-AI-HIGH-IMPACT -->
- AI 涉及医疗、法律、金融、未成年人、身份、就业、教育、公共安全、隐私、敏感个人数据或其他高影响领域时，范围与可接受边界必须逐项由人判断。

<!-- rule-id: DEFINITION-AI-DATA-RECIPIENT -->
- 把用户数据交给新的模型或模型供应商、工具、RAG 来源、第三方/供应商、训练或微调流程、外部翻译服务时，必须由人批准相应接收方或用途变化。

<!-- rule-id: DEFINITION-AI-SIDE-EFFECT -->
- AI 输出若可直接引发付款或其他金钱动作、删除、权限变更、通知、外部提交、后台动作或代码执行，是否允许该副作用必须由人决定。

<!-- rule-id: DEFINITION-AI-HUMAN-REVIEW -->
- 是否允许 AI 输出绕过人工复核并直接进入生产决策，必须由人作出明确决定。

## 重新组织后的规范要求

### 产品赌注、成功与指标

<!-- rule-id: DEFINITION-PRODUCT-BET -->
- 对用户可见能力维护一份 product bet，至少记录目标用户、问题、appetite、范围、非目标、风险、学习目标、关联 OpenSpec、决定日期，并回答谁会因该能力获得更好的结果。

<!-- rule-id: DEFINITION-PILOT-SUCCESS -->
- 客户试点开始前定义可观察的成功标准，并把它写入 charter；可按实际选择激活、任务完成、节省时间、错误减少、付费转换、留存、人工验收或明确业务事件。成功标准缺失时不得 production go-live。

<!-- rule-id: DEFINITION-METRICS-MAP -->
- metrics map 连接产品问题与可判定指标，记录 `target`、owner、当前关键问题、唯一主指标、supporting metrics、guardrail metrics、dashboard、decision policy、人工 checkpoint、复查节奏和状态。

<!-- rule-id: DEFINITION-METRIC-SPECIFICATION -->
- 每项产品指标都要写清分子、分母、过滤条件、时间窗口、去重、归因和查询位置，并关联其事件依赖；不得使用“近期”“活跃用户”等无法复现的窗口描述，没有事件依赖的指标不得用于发布判断。

<!-- rule-id: DEFINITION-GUARDRAIL-METRICS -->
- 为适用风险定义 guardrails，至少逐项考虑延迟、错误、成本、隐私、支持投诉、退订/退出和 AI safety trigger。AI 质量指标要同时连接 eval 版本与产品事件，不能只以 token 用量或点击代替质量。

<!-- rule-id: DEFINITION-DASHBOARD-QUESTIONS -->
- 产品 dashboard 只承载少数决策问题：关键任务是否完成、用户在哪里流失、guardrail 是否受损、接下来应调查什么；它不扩展产品范围或替代人的决定。

### 规格与权威边界

<!-- rule-id: DEFINITION-OPENSPEC-CONTROL -->
- Standard/High-risk 变更默认由 OpenSpec 承载，`proposal.md` 记录意图、范围、非范围、依据和待人工判断项，`tasks.md` 作为执行状态而不再复制 work brief。跳过 OpenSpec 只能由用户明确批准并记录理由。

<!-- rule-id: DEFINITION-NORM-PRECEDENCE -->
- 可选的 AI、外部声明等专项材料与本规范的正式分类及项目原则冲突时，以正式规范为准。

<!-- rule-id: DEFINITION-LOW-RISK-AUTOMATION -->
- 文件落点、模板或 rubric 初稿、低风险字段/标签补齐、普通章节或 runbook 命名、普通 prompt 文案、case id、可回滚局部实现及仓库已确定的技术细节，默认可以自动处理；此默认不扩大到任何产品或风险决定。

### AI 行为、证据与边界

<!-- rule-id: DEFINITION-AI-ARTIFACT-CHOICE -->
- AI 行为目标可放入 work brief 或 OpenSpec；AI playbook 与 OpenSpec 都不是所有 AI 工作的固定前置，只按工作风险和既有治理选择承载工件。

<!-- rule-id: DEFINITION-AI-BEHAVIOR-RECORD -->
- 选定承载工件后，记录用户可见行为与行为目标，并先把目标和 eval 写清，再进入模型、工具、结构化输出、trace 或安全实现。

<!-- rule-id: DEFINITION-AI-CAPABILITY-FILES -->
- 每个用户可见 AI capability 至少建立一个能力目录，并为它维护 prompt 文件；文件名或目录是执行约定，不替代行为定义。

<!-- rule-id: DEFINITION-AI-EVAL-STANDARD -->
- 每个用户可见 AI capability 必须维护 `evals/<capability>/rubric.md`。每条 eval case 必须有验收 criteria；rubric 定义可接受输出而不是“看起来不错”。case id、runbook 小节和低风险 rubric 初稿可以按默认模板形成，但验收含义必须可判定。

<!-- rule-id: DEFINITION-AI-MODEL-DEFAULT -->
- 默认模型发生变化时记录理由；是否改变默认模型必须由人决定。

<!-- rule-id: DEFINITION-AI-MODEL-SUPPLIER -->
- 定义 AI 能力时确认模型供应商边界可接受；更换供应商必须由人决定，供应商边界未定义则停止并回到前置风险定义。

<!-- rule-id: DEFINITION-AI-COST-LATENCY -->
- 定义 AI 能力时同时确认成本与延迟边界，不能只描述理想输出。

<!-- rule-id: DEFINITION-AI-DATA-PROVENANCE -->
- 改变训练数据，或接受来源/许可不清的数据，必须由人判断；来源和许可两项分别记录，不能互相代替。

<!-- rule-id: DEFINITION-AI-BOUNDARY-REVIEW -->
- AI 能力必须明确客户内容边界；接受安全或隐私例外时分别取得人工决定，不得把复合“风险已接受”作为替代。

<!-- rule-id: DEFINITION-AI-BOUNDARY-ROUTING -->
- 安全隐私、IP、客户数据生命周期、供应商、数据接收方或公开承诺任一边界不清时，退出 AI 定义并返回前置风险设计；不得在行为规格中暗自补齐这些决定。

<!-- rule-id: DEFINITION-AI-CONTEXT-SOURCE -->
- 使用 RAG、记忆或其他上下文时记录其来源；改变 RAG 来源或把记忆默认开启必须由人决定。

<!-- rule-id: DEFINITION-AI-SAFETY-DECISION -->
- 修改拒绝边界、moderation threshold 或申诉拒绝路径，必须由人判断。

<!-- rule-id: DEFINITION-AI-FALLBACK -->
- AI 失败处置要从 fallback、rollback、人工复核、阻塞发布或返回前置定义中选择适用路径；上线没有 fallback 的能力必须取得人工决定。

<!-- rule-id: DEFINITION-AI-LOCALIZATION -->
- 支持本地化前记录 locale 风险；改变 locale 默认或高风险多语言文案时必须人工判断。

<!-- rule-id: DEFINITION-AI-OPTIMIZATION-PREREQUISITES -->
- 启动模型优化前先形成失败分类并确认预算，不能把“需要优化”直接当作实施授权。

<!-- rule-id: DEFINITION-AI-SPECIALIZED-CHANGE -->
- 真实训练/微调，以及正式新增 locale、多币种、RTL 或高风险翻译能力，必须另建 Standard 或 High-risk change 后再执行。

<!-- rule-id: DEFINITION-AI-LEARNING-ROUTING -->
- 上线后的 AI 质量事故与投诉进入运行/评估，形成的新样本再回流到 AI 定义作为下一轮输入。

<!-- rule-id: DEFINITION-SUPPORT-AI-AUTHORITY -->
- 回复一旦涉及退款、法律结论、数据删除、权限变更或事故恢复时间，就只能交由具备相应权限的人或既定流程确认；AI support assistant 不能代表组织直接作出承诺。

### 权利、内容安全与外部声明

<!-- rule-id: DEFINITION-IP-RISK -->
- 涉及高风险许可证、无授权素材、客户内容复用或 AI 输出强权利声明时，由人判断可接受性；需要时补充 source register、license policy、AI output policy 和 notice/attribution。

<!-- rule-id: DEFINITION-CONTRACT-ARTIFACTS -->
- 触发契约专项后，按需要补齐范围和演进说明，所用工件是 error model、surface map、Protobuf evolution 与 compatibility policy。另以 AI tool schema 和 contract tests 组成可执行契约证据。

<!-- rule-id: DEFINITION-CONTENT-SAFETY-RECOURSE -->
- 内容审核必须定义 notice 与 appeal；自动化 enforcement 超过标注或复核时，两者均不可省略。

<!-- rule-id: DEFINITION-CLAIM-APPLICABILITY -->
- 外部声明治理保持为条件触发的可选 playbook：官网、pricing、docs、developer portal、AI disclosure、trust/security/privacy、support/sales、release notes、商业沟通或其他对外强声明适用；完全不发送给用户、客户、公众、审核方或供应商的内部草稿通常不适用。正式法律、广告、监管或诉讼事项转交专业服务或单独 change。

<!-- rule-id: DEFINITION-CLAIM-TARGET-IDENTITY -->
- 同一 production target 的声明工件统一使用一个 `<target>` 名称，并维护对应的 surface inventory。

<!-- rule-id: DEFINITION-CLAIM-PRESENTATION -->
- 强声明旁必须能找到范围、限制、更新时间或有效链接中的适用信息；页面以克制、可扫描的结构呈现，不能把限制藏进 hero 或装饰文案。声明降级或更正时直接展示真实状态和下一步，禁止用模糊措辞遮掩能力退化。

<!-- rule-id: DEFINITION-CLAIM-AI-REVIEW -->
- AI 生成外部材料时必须标出新增或被强化的 claim，供后续证据与发布门禁检查。

<!-- rule-id: DEFINITION-CLAIM-HUMAN-DECISION -->
- 扩大 claim 从 beta/internal/experimental 到 public/stable/customer-contract，承认合同、SLA、DPA、隐私政策、安全页、销售邮件或支持回复已形成承诺，决定是否向客户、开发者、审计/监管方或公众更正，以及是否需要法律、隐私、安全、合同、广告或合规专业意见，都必须由人判断。字段顺序、低风险措辞、链接修正、内部草稿和不改变含义的 typo 默认无需人工决定。

## 按主题整理的执行细则

### 条件工件

<!-- rule-id: DEFINITION-AI-CONDITIONAL-ARTIFACTS -->
- 仅在相应风险被触发时增加专项工件：上下文/RAG/记忆使用 `ai-context/`，模型优化使用 `ai-optimization/`，内容安全使用 `content-safety/`，本地化使用 `localization/`。

<!-- rule-id: DEFINITION-AI-VENDOR-COST-ARTIFACTS -->
- 成本容量触发时补预算、vendor boundary 与 cost/capacity runbook；外部处理方触发时补 processor register、DPA checklist、subprocessor watch 与 transfer impact。

<!-- rule-id: DEFINITION-CONTENT-SAFETY-ARTIFACTS -->
- 内容安全政策默认记录在 `content-safety/policy/<surface>.md`，通知和申诉设计默认记录在 `content-safety/notice-appeal/<surface>.md`。

### 外部声明清单与审计

<!-- rule-id: DEFINITION-CLAIM-SURFACE-INVENTORY -->
- surface inventory 顶层记录 target、owner、surfaces、source artifacts、claim sources、scan policy、human checkpoint、review cadence 与 status。每个 surface 记录 id、name、`surface_type`、location、audience、owner、last scanned 与 status；`surface_type` 从 marketing、pricing、docs、developer_docs、product_ui、contract、support、security、privacy、status、release_notes、sales 中选择。只登记会被外部依赖的 surface；AI、隐私、安全、SLA、计费、合同或开发者稳定性等高风险 surface 必须有 owner 和 last scanned。

<!-- rule-id: DEFINITION-CLAIM-AUDIT-EVENT -->
- claim gate 事件保存 claim id、surface id、actor、decision、request id 和 trace id，以便从决定回到触发表面和证据。

### 客户试点

<!-- rule-id: DEFINITION-PILOT-CHARTER -->
- 每个客户试点开始前维护 `pilot-charter/<account>.md`，至少包含标题、Customer Alias、Pilot Type、Timeline/Appetite、Exit Criteria、Human Checkpoints、Linked Artifacts 与 Review Cadence。

<!-- rule-id: DEFINITION-PILOT-SCOPE -->
- charter 同时记录 Scope、Problem/Outcome、In Scope 与 Out Of Scope。Out Of Scope 优先写清客户特例、临时人工服务、未承诺集成和未承诺 SLA，避免试点被解释为正式承诺。

<!-- rule-id: DEFINITION-PILOT-EXIT -->
- 试点 Exit Criteria 必须覆盖转生产、延长、终止、数据删除或导出、关闭 feature flag 和取消 entitlement 六种路径。

## 输入与产物

输入包括被选中的 outcome 与 appetite、目标用户和问题证据、实验/反馈结论、现有产品行为、客户与商业边界、AI 数据及风险信息。

产物按适用范围包括 product bet、行为与非范围、成功标准、metrics map、风险/人工 checkpoint、OpenSpec 链接、AI 行为与 eval 定义、外部声明清单，以及试点 charter。低风险工作不要求创建全部工件。

## 完成、停止或退出条件

定义在行为、范围与非范围、验收或成功标准、关键指标与 guardrails、风险边界、人工决定和退出路径均可追溯时完成。任何实现前置缺失按 `DEFINITION-IMPLEMENTATION-READINESS` 停止；产品输入不清按 `DEFINITION-PRODUCT-ROUTING` 回退；AI、商业、高影响或外部声明的人类决定未取得时，不得进入下一项目。

## 相关项目引用

- 选题提供投入决定与 appetite，调研提供问题证据和学习结论；定义消费这些输入，不重新排列优先级。
- 体验设计把已定义行为转为任务、状态、反馈与用户控制，不改变这里的产品范围。
- 技术设计决定系统实现方式；工程计划、实现和验证分别组织工作、产生技术产物和证明结果。
- 发布消费外部声明与试点边界，运行/评估把事故、投诉、指标和新样本回流下一轮定义。
