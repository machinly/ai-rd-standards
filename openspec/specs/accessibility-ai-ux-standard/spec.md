# accessibility-ai-ux-standard 规格

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

Define the minimum one-person-company governance for accessibility, AI UX disclosure, keyboard/focus interaction, user feedback/correction, degraded states, and interface trust on critical user-facing surfaces.
## Requirements
### Requirement: 关键用户 surface 必须定义 ux-accessibility artifacts

Any critical user-facing surface, especially one that includes AI-generated, AI-recommended, AI-classified, AI-executed, paid, account, data-rights, admin, or high-impact workflows, MUST define UX accessibility artifacts.

#### Scenario: 新关键 surface 或 AI surface 准备发布

- GIVEN 一个用户可见 surface 包含关键任务、AI 输出、付费、设置、数据删除、权限、后台操作或高影响建议
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `ux-accessibility/surface-map/<surface>.md`
- AND 创建 `ux-accessibility/interaction-contract/<surface>.json`
- AND 创建 `ux-accessibility/accessibility-test-plan/<surface>.json`
- AND 创建 `ux-accessibility/ai-ux-disclosure/<surface>.md`
- AND 创建 `ux-accessibility/ux-review/<surface>.md`

### Requirement: Surface map 必须定义用户、任务、状态、输入模式、AI 接触点和风险

Surface map MUST record scope、users/context、critical tasks、views/states、input modes、accessibility baseline、AI touchpoints、responsive/theme、risks 和 linked artifacts。

#### Scenario: Reviewer 判断 surface 是否值得发布

- GIVEN reviewer 打开 `ux-accessibility/surface-map/<surface>.md`
- WHEN 需要理解用户界面风险
- THEN 能看到用户、使用环境、1 到 3 条关键任务、视图/状态、输入模式、可访问性基线、AI 接触点、响应式/主题要求和风险
- AND AI touchpoints 说明 AI 影响什么、用户如何反馈、撤销、纠正或升级人工处理

### Requirement: Interaction contract 必须定义组件、状态、输入、键盘、焦点、表单、错误和 AI 交互

Interaction contract MUST record surface、owner、users、critical tasks、components、states、input modes、keyboard、focus、forms、errors、loading/empty/offline、responsive、theme、AI interactions、human checkpoint 和 review cadence。

#### Scenario: 前端实现或审查关键交互

- GIVEN Vite frontend 或 reviewer 读取 `ux-accessibility/interaction-contract/<surface>.json`
- WHEN 实现或检查 surface
- THEN 每个 component 包含 id、name、role、purpose、states、keyboard_support、focus_behavior、accessible_name_source、aria_strategy 和 status
- AND contract 覆盖 loading、empty、error、success 以及适用的 AI generating、degraded、blocked 或 human-review 状态

### Requirement: Accessibility test plan 必须包含标准、工具、人工检查、辅助技术、门禁、例外和证据

Accessibility test plan MUST record surface、owner、standards、tools、checks、viewports、assistive tech、gates、exceptions、evidence refs、human checkpoint 和 status。

#### Scenario: 发布前检查可访问性

- GIVEN surface 准备发布
- WHEN 运行或记录 `ux-accessibility/accessibility-test-plan/<surface>.json`
- THEN standards 至少包含 `wcag_2_2_aa`、`wai_aria_apg` 和 `geist_design_md`
- AND checks 覆盖 semantic structure、keyboard navigation、visible focus、focus order、contrast light/dark、form labels/errors、screen reader smoke、reduced motion、responsive reflow、touch target size、status not color-only 和 AI disclosure/feedback
- AND exceptions 记录 reason、owner、expires_at 和 mitigation

### Requirement: AI UX disclosure 必须解释 AI 使用、心理模型、限制、反馈、人工处理、数据控制和降级状态

AI UX disclosure MUST record scope、AI surfaces、user mental model、disclosure labels、limitations/uncertainty、feedback/correction、human handoff、data use/controls、error/degraded states 和 linked artifacts。

#### Scenario: 用户看到 AI 输出或建议

- GIVEN surface 展示 AI 输出、建议、自动化、总结、分类或风险提示
- WHEN 用户与 surface 交互
- THEN 界面说明 AI 在哪里工作、输出可能有什么限制、用户如何反馈/纠正/撤销、何时升级人工处理、数据如何使用或控制
- AND 高影响场景不把 AI suggestion 伪装成最终人工决定

### Requirement: UX review 必须复盘可用性、可访问性、AI 预期风险、指标反馈、例外和下一项改进

UX review MUST record recent changes、usability findings、accessibility findings、AI expectation risks、metrics/feedback、exceptions、open risks 和 next one change。

#### Scenario: 周期性复查关键 surface

- GIVEN surface 有近期界面、AI 交互、表单、导航、权限、计费、设置或反馈变更
- WHEN 更新 `ux-accessibility/ux-review/<surface>.md`
- THEN 记录可用性发现、可访问性发现、AI 预期风险、指标/反馈、例外和开放风险
- AND 只选择一个最高影响的 next one change

### Requirement: 高风险 UX 和可访问性例外必须人工 checkpoint

Critical path WCAG/keyboard exceptions, custom complex widgets, high-impact AI UI, hidden or weakened AI disclosure, missing user feedback/control, dark pattern risk, sensitive data capture, irreversible action UX, and new brand/claim surfaces MUST have human checkpoint coverage.

#### Scenario: Surface 触发高风险 UX 条件

- GIVEN interaction contract、test plan、AI disclosure、release 或 UX review 触发高风险条件
- WHEN 准备发布或接受例外
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifacts 记录人的判断、风险接受、升级或阻塞状态

### Requirement: UX accessibility artifacts 不得保存敏感内容

UX accessibility artifacts MUST NOT store secrets, production tokens, private keys, payment data, raw prompts, raw responses, raw tool outputs, unredacted personal data, access tokens, session cookies, or sensitive user feedback text.

#### Scenario: 记录测试证据、反馈或 UI incident

- GIVEN 需要保存 screenshot note、feedback、AI output example、error example 或 UI incident evidence
- WHEN 写入 `ux-accessibility/` artifacts
- THEN 使用 synthetic example、redacted summary、trace id、request id、surface id、hash 或 controlled attachment reference
- AND 不保存 secrets、生产 token、私钥、支付数据、完整 raw prompt/response/tool output、未脱敏个人数据或敏感反馈原文

### Requirement: 可视 UX 适用性必须在生产性实现前判定

Standard/High-risk change MUST 在 proposal 中记录 `visual_ux: required | not-required` 和理由。新增或实质改变关键用户任务、页面结构、信息架构、导航、关键 surface 关系、高影响交互、会影响下一步的基本状态，或 desktop/mobile 实质布局差异时 MUST 为 `required`；不改变含义的文案、局部 token/间距/单控件外观和不改变任务、结构、状态或用户控制的低风险修复 MAY 为 `not-required`。

#### Scenario: 新关键页面流程

- **WHEN** change 新增或实质改变关键用户任务与页面结构
- **THEN** proposal 记录 `visual_ux: required`
- **AND** 在生产性实现前完成静态可视 UX

#### Scenario: 不改变含义的文案修正

- **WHEN** change 只修正文案且不改变任务、结构、状态或用户控制
- **THEN** proposal 可以记录 `visual_ux: not-required`
- **AND** 记录不触发理由

### Requirement: Required 可视 UX 必须形成最小静态仓库产物

`visual_ux: required` change MUST 在一个权威目录维护 `flow.md`、`wireframes/<surface>--<state>.html|svg` 和 `review.md`。Wireframes MUST 覆盖关键路径与适用的 loading、empty、error、success；desktop 为默认，只有布局实质不同才增加 mobile；不适用状态 MUST 在 `flow.md` 说明理由。

#### Scenario: 准备关键 surface 的开发前 review

- **WHEN** change 的 `visual_ux` 为 `required`
- **THEN** `flow.md` 记录目标、入口、正常步骤、error/retry/cancel/exit、non-goals 和 wireframe 索引
- **AND** 静态 wireframes 不包含业务脚本、真实 API、数据写入或仓库外资源
- **AND** 重复区域使用项目内稳定语义名称

### Requirement: 生产性实现必须取得明确的人类 UX 批准

`visual_ux: required` change MUST 在生产性实现前由人类明确给出 `approved`。`review.md` MUST 记录 decision owner、reviewed at、artifacts reviewed、decision 和 notes；沉默、一般授权、AI 推断、OpenSpec validation 或后续实现状态 MUST NOT 产生批准。批准后任务路径、结构、状态、权限含义或高风险确认发生实质变化时 MUST 重新 review。

#### Scenario: Required UX 尚未批准

- **WHEN** `review.md` 缺失或 decision 不是 `approved`
- **THEN** 可以继续技术调查或记录开放问题
- **AND** 不得开始或标记 production implementation ready

#### Scenario: 品牌营销页需要更高视觉判断

- **WHEN** 新品牌/营销页、新视觉语言、信息密度或视觉层级使低保真不足
- **THEN** 由人决定是否增加高保真静态设计
- **AND** 不因此增加可交互原型阶段
