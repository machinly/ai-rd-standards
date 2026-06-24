# accessibility-ai-ux-standard 规格

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
