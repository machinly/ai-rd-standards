# 体验设计

## 项目目的与边界

体验设计把已定义的产品行为组织成用户能够理解、完成、纠正和退出的任务路径。Explore / UX Prototype 用于比较关键流程与可理解性；Deliver 的 formal visual UX 用于锁定生产性实现输入。两者都关注界面状态、交互契约、可访问性、敏感输入、AI 披露与控制、高风险确认和用户可行动反馈，但不改变产品范围，不替代技术权限、运行处置、发布门禁或专业合规审查。

## 根本原则

- **ITEM-EXPERIENCE-001**：涉及用户界面请求时，体验设计必须覆盖等待、空缺、失败和成功四类状态。

## 核心判断

<!-- rule-id: EXPERIENCE-UX-APPLICABILITY -->
- 当工作涉及用户界面、可访问性、AI UX、交互状态、键盘/焦点、AI disclosure 或界面信任时进入体验设计；产品内 UI、设置、控制台、empty/error 页面、提示框，以及 AI、权限、删除、导出和账单说明都属于适用 surface。

<!-- rule-id: EXPERIENCE-SURFACE-MAP -->
- 先按用户关键任务组织 surface，而不是先列组件；每个 surface 通常保留一至三条关键路径，并记录 desktop、mobile、keyboard-only、reduced motion、light/dark theme 的适用性。

<!-- rule-id: EXPERIENCE-BASE-STATE-COVERAGE -->
- 所有交互 surface 以及前端请求都必须定义 loading、empty、error 和 success 四类基本状态。

<!-- rule-id: EXPERIENCE-ACCESSIBILITY-BASELINE -->
- 文字与关键 UI 以 WCAG AA 为最低对比度基线，可访问性测试默认以 WCAG 2.2 AA 为标准；关键用户路径未达到该基线或未完成 keyboard smoke 时，只有人工决定后才能接受上线风险。

<!-- rule-id: EXPERIENCE-KEYBOARD-FOCUS -->
- surface map 和测试计划要覆盖 keyboard-only、键盘导航、可见焦点与焦点顺序；这些要求进入组件交互契约，不能只在验收末尾补测。

<!-- rule-id: EXPERIENCE-AI-DISCLOSURE -->
- 用户应能识别 AI 何时在生成、推荐、总结、分类或执行。概率性或不确定输出不得伪装成确定事实，也不得用绝对化措辞掩盖不确定性。

<!-- rule-id: EXPERIENCE-AI-CORRECTION-CONTROLS -->
- 对不确定 AI 输出，必须从来源、置信边界、可编辑或撤销路径、人工复核路径中展示适用组合；还应按场景提供理由、下一步或纠错入口中的适用项。

<!-- rule-id: EXPERIENCE-HIGH-IMPACT-AI -->
- 高影响 AI 场景默认需要人工确认或清楚的能力边界。涉及付费、权限、数据删除、医疗、法律、金融、就业、教育、身份或公共安全的建议必须由人决定是否可用；AI suggestion 不得直接转成不可逆动作，并必须连接 admin action guard、auth boundary、red-team 或 release gate 中适用的控制。

<!-- rule-id: EXPERIENCE-TRUSTWORTHY-INTERACTION -->
- 下列任一情况出现，均须由人判断：接受 dark pattern、误导性默认、强迫同意、取消困难或无法撤销的交互；发布新的品牌或营销界面；显著改变产品承诺或用户心理模型。

## 重新组织后的规范要求

### Explore UX Prototype

<!-- rule-id: EXPERIENCE-UX-PROTOTYPE-BOUNDARY -->
- UX Prototype 属于 Explore，用于比较关键任务流程、信息架构、交互和可理解性；可以是静态或可运行工件，并应尽快从实际产品入口向人展示。它不自动要求 Deliver 的 `flow.md`、完整 state wireframes、`review.md` 或 production implementation approval，也不能冒充已批准的 formal visual UX。

### 开发前可视 UX

<!-- rule-id: EXPERIENCE-VISUAL-UX-APPLICABILITY -->
- 新增或实质改变关键用户任务、页面结构、信息架构、导航、关键 surface 关系、高影响交互、会显著影响用户下一步的 loading/empty/error/success，或 desktop/mobile 存在实质布局差异时，须在生产性实现前执行 formal visual UX。该 `visual_ux: required | not-required` 是 Deliver Standard/High-risk 的正式门禁，并在 proposal 中记录判定与理由；是否触发存在合理疑问时按 `required` 处理。Explore promote 后从转换点开始判断，不追溯伪造探索期批准。UX Prototype 与不改变含义的文案、局部 token/间距/单控件外观，以及不改变任务、结构、状态和用户控制的低风险样式修复都不会仅因存在视觉工件而自动触发。

<!-- rule-id: EXPERIENCE-VISUAL-UX-ARTIFACTS -->
- `visual_ux: required` 的 change 在 `ux/<change-id>/` 或项目既有的一个权威设计目录维护 `flow.md`、`wireframes/<surface>--<state>.html|svg` 与 `review.md`，其中 `<state>` 按适用范围覆盖 `success`、`loading`、`empty`、`error`。`flow.md` 记录用户目标、入口、正常步骤、error/retry/cancel/exit、non-goals 和线框索引；线框只表达布局、信息层级、内容与操作位置，不含业务脚本、真实 API、数据写入或仓库外资源。desktop 为默认，只有布局实质变化时才补 mobile；不适用状态须在 `flow.md` 说明理由。

<!-- rule-id: EXPERIENCE-VISUAL-UX-APPROVAL -->
- `review.md` 至少记录 Decision owner、Reviewed at、Artifacts reviewed、Decision 与 Notes。只有明确的人类决定可以产生 `approved`；AI 不得根据沉默、一般授权、OpenSpec validation 或后续实现状态推断批准。`approved` 是进入生产性实现的门禁；批准后任务路径、结构、状态、权限含义或高风险确认发生实质变化时，须更新可视 UX 并重新 review。

<!-- rule-id: EXPERIENCE-VISUAL-UX-HIGH-FIDELITY -->
- 低保真静态 UX 是默认。新品牌/营销页面、新视觉语言、信息密度或视觉层级本身构成主要风险，或低保真不足以支持真实取舍时，由人决定是否增加高保真静态设计；该升级不增加可交互原型阶段，确认后仍直接进入开发。

### 交互契约、组件与错误

<!-- rule-id: EXPERIENCE-INTERACTION-CONTRACT -->
- 每个关键 surface 维护 `interaction-contract/<surface>.json` 或等价记录，包含 surface、owner、users、critical tasks、components、states、input modes、keyboard、focus、forms、errors、loading/empty/offline、responsive、theme、AI interactions、human checkpoint 和 review cadence。

<!-- rule-id: EXPERIENCE-COMPONENT-CONTRACT -->
- 交互契约中的每个组件记录 id、name、role、purpose、states、keyboard support、focus behavior、accessible name source、ARIA strategy 与 status。

<!-- rule-id: EXPERIENCE-AI-STATE-COVERAGE -->
- AI surface 除基本状态外，还要从 generating、degraded、blocked、human-review 中覆盖所有适用状态。

<!-- rule-id: EXPERIENCE-FRONTEND-ERROR-CONTRACT -->
- 返回前端的错误合同提供稳定 code、message key、适用的 field errors、request id、retryability 和对用户安全的下一步，不能迫使界面解析内部字符串。

<!-- rule-id: EXPERIENCE-ERROR-STATE-MAPPING -->
- 后端错误要能映射到 validation、auth、permission、quota、dependency、AI degraded、AI blocked 和 internal 中适用的 UI 状态；gRPC/HTTP 响应不得只暴露内部错误文本。

<!-- rule-id: EXPERIENCE-STATUS-REDUNDANCY -->
- 状态不能只依赖颜色；颜色状态以及 AI 置信、风险、错误、警告和成功提示必须同时配文本或图标中的至少一种。AI generating 状态不得依赖闪烁或长循环动画。

### 可访问性、例外与组件选择

<!-- rule-id: EXPERIENCE-ACCESSIBILITY-ARTIFACTS -->
- 每个关键 surface 维护 accessibility test plan，并在 surface map 记录 Accessibility Baseline、在 UX review 记录 Accessibility Findings。

<!-- rule-id: EXPERIENCE-ACCESSIBILITY-EXCEPTION -->
- 每项可访问性例外必须单独记录 reason、owner、expires_at 和 mitigation，不能以一条长期豁免覆盖多个缺口。

<!-- rule-id: EXPERIENCE-EXCEPTION-APPROVAL -->
- 当体验方案请求偏离既定的可访问性或信任边界时，放行决定必须由人作出；受控范围包括 WCAG 2.2 AA、键盘可操作性、焦点行为、AI disclosure、用户反馈通道和界面信任要求。

<!-- rule-id: EXPERIENCE-COMPONENT-CHOICE -->
- 可视 UX 与实现默认优先当前项目已有组件、设计 token、原生控件或成熟可访问组件；在线框中用 `AppShell`、`FormField`、`StatePanel`、`ConfirmAction` 等稳定语义名称标出重复区域，同一项目的重复交互只实现一次并通过组合复用，一次性业务结构留在当前 change。采用自定义复杂 widget 必须由人判断；跨项目 catalog、通用 UX Kit 和共享 renderer 另立 change。

<!-- rule-id: EXPERIENCE-INTERNAL-HIGH-RISK-BASELINE -->
- 纯内部一次性脚本通常不进入完整 UX playbook；但只要能改生产数据或触发高风险动作，仍必须满足键盘、错误和确认基线。

### AI 披露、记忆与运行状态

<!-- rule-id: EXPERIENCE-AI-DISCLOSURE-ARTIFACT -->
- 每个关键 AI surface 维护 AI UX disclosure；同一工件至少说明 Scope、AI Surfaces、User Mental Model、Disclosure Labels、Limitations/Uncertainty、Feedback/Correction、Human Handoff、Data Use/Controls、Error/Degraded States 与 Linked Artifacts。触发信任专项时可放在 `ai-disclosure/<target>.md`，UX surface 默认使用 `ai-ux-disclosure/<surface>.md`。

<!-- rule-id: EXPERIENCE-AI-SURFACE-MAP -->
- AI surface map 写明 AI 出现的位置、影响的决定，以及用户能否反馈、撤销或纠正。

<!-- rule-id: EXPERIENCE-AI-MEMORY-CONTROLS -->
- 使用长期上下文或记忆时，用户必须能够查看、关闭、删除和导出，并获得“临时模式”或“不要记住”中的至少一种选择；缺少这些控制的内容不得默认注入模型。

<!-- rule-id: EXPERIENCE-AI-MODE-SELECTION -->
- 高成本或慢速模式使用明确按钮或切换让用户选择，不能把更贵、更慢的模型隐藏成默认体验。

<!-- rule-id: EXPERIENCE-AI-RUNTIME-STATUS -->
- AI 工具界面明确区分失败、等待批准、降级、取消、rollback/compensation、rate limit 和 kill switch 状态。

<!-- rule-id: EXPERIENCE-AI-DEGRADATION -->
- AI 降级时只展示与真实状态相符、用户可行动的信息，例如结果可能受限、生成较慢、暂时少功能、已切基础模式、已转后台/人工、可重试或稍后通知；从这些表达中选择适用项，不虚构恢复能力。

<!-- rule-id: EXPERIENCE-AI-TRANSPARENCY-APPROVAL -->
- 隐藏、弱化或省略 AI disclosure、限制、反馈、人工复核或用户控制，必须由人决定。

### 授权与高风险动作

<!-- rule-id: EXPERIENCE-AI-TOOL-AUTHORIZATION -->
- 工具授权确认展示动作名、目标、影响、权限 scope、dry-run、批准状态、撤销或补偿方式与风险，使用户在授权前看见实际后果。

<!-- rule-id: EXPERIENCE-HIGH-RISK-CONFIRMATION -->
- 高风险确认不得只问“确定吗”。确认界面必须显示工具或动作名称、目标对象、数量或金额、外部收件人、权限变化、dry-run 结果、approval 状态、rollback/compensate 说明和不可逆后果；R2/R3/R4 动作必须二次确认，危险动作需要确认与 evidence，不能用营销文案弱化风险。

<!-- rule-id: EXPERIENCE-ASYNC-USER-CONTROL -->
- 下列任一情况出现，均须由人判断：把用户可见核心路径改为异步；异步长任务缺少状态查询、取消或失败解释中的任何一项。使用 background mode 时必须记录取消策略。

<!-- rule-id: EXPERIENCE-NOTIFICATION-APPROVAL -->
- 改变通知行为必须由人判断。

<!-- rule-id: EXPERIENCE-COMMERCIAL-UNSUBSCRIBE -->
- 商业邮件必须向接收者提供退订路径。

### 敏感输入与支持

<!-- rule-id: EXPERIENCE-SENSITIVE-DATA-APPROVAL -->
- 收集敏感个人数据、生物识别数据、未成年人数据或会影响用户重大权益的数据，必须由人判断必要性与边界。

<!-- rule-id: EXPERIENCE-SENSITIVE-SUPPORT-INPUT -->
- 支持或问题报告表单默认不要求用户粘贴完整 prompt/response、secret、完整日志、个人数据或支付信息。AI 输出旁可以提供“报告问题”入口，但必须提示不要提交敏感信息。

<!-- rule-id: EXPERIENCE-SUPPORT-INTAKE -->
- 产品内支持入口保持低摩擦，并允许用户随请求携带 request id、feature、发生时间和错误类别。

<!-- rule-id: EXPERIENCE-SUPPORT-TRACEABILITY -->
- AI 反馈记录应能关联 capability、版本、route 和 trace/request id，以便后续定位，同时不向用户暴露内部实现。

<!-- rule-id: EXPERIENCE-INTERNAL-ERROR-CONFIDENTIALITY -->
- 用户界面不得泄露供应商内部错误、具体模型细节、prompt、trace 原文或安全绕过信息。

## 按主题整理的执行细则

### 工件身份与默认技术栈

<!-- rule-id: EXPERIENCE-UX-ARTIFACT-IDENTITY -->
- 同一关键 surface 的 UX 工件使用一致的 `<surface>` 文件名，使 map、contract、test plan、disclosure 与 review 可相互关联。

<!-- rule-id: EXPERIENCE-FRONTEND-STACK-DEFAULT -->
- 交互型前端默认使用 Vite、React 与 TypeScript；这是执行默认，不属于体验原则，也不能覆盖仓库明确的其他技术决定。

<!-- rule-id: EXPERIENCE-PLAYBOOK-BOUNDARY -->
- 轻量静态 wireframes 与开发前人工 review 属于条件触发的体验设计步骤，并服从本规范的正式分类及项目原则。完整品牌系统、通用 UX Kit、设计稿协作流程、大型组件库、视觉回归平台或全面用户研究计划不属于此轻量流程；法律级无障碍审计或正式 VPAT 转交专业审阅或单独 change。

<!-- rule-id: EXPERIENCE-FOCUS-REVIEW-TRIGGER -->
- 只有周期性的 focus review 确实会改变取舍时才增加该治理动作，不能把会议本身当作体验产物。

### 工作台、状态页与安全沟通

<!-- rule-id: EXPERIENCE-WORKBENCH-PRESENTATION -->
- 后台工作台、密钥防护界面或内部控制台以高信息密度、清楚状态和少量明确动作组织，默认采用克制的 Vercel/Geist 风格而不是营销页布局。

<!-- rule-id: EXPERIENCE-STATUS-PAGE-PRESENTATION -->
- 帮助页和状态页保持简洁、少装饰，突出当前状态、已知问题与下一步，并采用 Vercel/Geist 风格。

<!-- rule-id: EXPERIENCE-SECURITY-COMMUNICATION -->
- 漏洞披露页按范围、联系方式、安全边界、报告要求和响应节奏组织，不用营销口吻包装安全事故。安全通知必须可访问、可复制、可导出，且不能只依赖颜色或弹窗表达状态；客户事件中心只呈现与该客户相关的影响、状态、建议动作和更新节奏。

<!-- rule-id: EXPERIENCE-AI-INCIDENT-NOTICE -->
- AI 质量事故的用户提示必须同时对齐通知、support 和 external claim gate 的权威规则，避免状态、承诺与支持口径互相冲突。

## 输入与产物

输入包括已批准的产品行为和范围、目标用户与关键任务、AI 行为/风险定义、权限与数据边界、错误合同，以及运行和支持场景。进入可视 UX 前还须已有本轮改变/不改变的行为、验收与退出条件、已知错误和降级场景；上游输入不成立时返回定义。

产物按适用范围包括 surface map、interaction contract、component contract、状态与错误映射、accessibility test plan、AI disclosure、授权/确认设计、敏感输入提示和支持入口。触发可视 UX 时还包括一个权威目录中的 `flow.md`、关键静态 wireframes 和人类 review；单纯内部低风险界面或不触发条件的局部修正不要求机械创建全部工件。

## 完成、停止或退出条件

体验设计在关键任务、组件与输入方式、基本/AI 状态、错误与下一步、键盘/焦点、可访问性、AI disclosure/纠错/降级、敏感输入和高风险确认均已覆盖，且适用的可视 UX 已取得人类 `approved` 时完成。缺少可视 UX 批准、例外批准、敏感数据收集决定、高影响 AI、异步控制或通知变化时停止；需要改变产品行为或范围时返回定义。

## 相关项目引用

- 定义提供产品行为、范围、AI 风险与验收；体验设计不得自行扩大这些决定。
- 技术设计负责权限、数据、错误与异步机制，体验设计只规定用户可见合同并引用其权威实现。
- 实现落地组件和状态，验证证明键盘、焦点、WCAG、错误、AI disclosure 与高风险确认符合本规范。
- 发布和运行管理实际开放、降级、事故与恢复；支持和质量信号经评估回流下一轮定义与体验设计。
