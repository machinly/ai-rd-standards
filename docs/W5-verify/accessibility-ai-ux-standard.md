# W5 Verify 触发专项：可访问性、AI UX 与界面信任规范

## W5 触发定位

本文件是 W5 Verify 的触发型专项，不是 W5 主入口。只有当当前验证涉及用户界面、关键交互、键盘/焦点、WCAG、AI disclosure、反馈纠错、降级状态或界面信任时，才需要读取本文件。

普通 W5 验证入口应先回到 `docs/W5-verify/main.md`，由主入口判断是否触发本专项。

## 目标

AI 产品的界面失败常常不是模型失败，而是用户无法操作、看不懂状态、误解 AI 能力、错误无法恢复、反馈没有入口、降级状态不诚实。本专项定义可访问性、AI UX 与界面信任规范，让每个用户可见 surface 都能回答：谁在什么环境下使用、关键任务能否只用键盘完成、焦点和错误是否清楚、AI 在哪里工作、用户如何纠错/关闭/反馈、发布前如何验证。

默认原则：可访问性不是发布前扫一遍工具；AI UX 也不是加一句免责声明。关键用户路径必须有可执行的交互契约、可访问性测试计划、AI 透明说明和复盘记录。

## 核心依据

- 《人月神话》：界面的一致性和概念完整性比堆功能更重要。AI 功能如果没有稳定的交互模型，会把复杂度转嫁给用户。
- 小型项目管理：一人公司不能维护厚重设计系统；只保留 surface map、interaction contract、accessibility test plan、AI UX disclosure、UX review 五个工件。
- The Design of Everyday Things：好界面要让用户理解可做什么、发生了什么、如何纠正错误；AI 界面尤其需要可感知的状态和可逆操作。
- ISO 9241-210：人本设计要求在交互系统生命周期中理解用户、任务和环境，并让设计活动围绕真实使用情境迭代。
- Nielsen usability heuristics：系统状态可见、贴近用户语言、用户控制、标准一致、错误预防、识别优于记忆、极简设计、帮助用户恢复错误，是一人公司最划算的 UX 基线。
- WCAG 2.2 / WAI：可访问性覆盖视觉、听觉、运动、认知、语言、学习和神经差异；WCAG 2.2 使用可测试 success criteria，W3C 鼓励采用当前版本。
- WAI-ARIA Authoring Practices / MDN：复杂 widget 需要正确语义、键盘模型和焦点行为；原生 `button`、`a`、`label`、`input` 优先于伪造控件。
- Vercel Geist `design.md` / `design.dark.md`：Geist 强调高对比、克制色彩、清晰焦点、紧凑半径、精确文案和浅/深主题 token；状态不得只靠颜色表达。
- Google People + AI Guidebook：AI 产品需要正确心理模型、反馈、控制、纠错、失败处理和持续学习，而不是把 AI 包装成魔法。
- NIST AI RMF：AI 产品需要把有效性、可靠性、安全、透明、可解释、隐私和公平等可信性因素纳入设计、使用和评估。

## 范围

适用对象：

- Vite / React / TypeScript 前端中的页面、表单、仪表盘、设置页、工作台、弹层、菜单、表格、命令面板、AI chat、AI copilot、AI 推荐、AI 自动化确认页。
- 任何用户可见 AI 能力：生成、摘要、问答、推荐、分类、自动填表、自动执行、风险提示、个性化、记忆、检索和工具调用结果。
- Go/Kratos/gRPC 后端暴露给前端的 loading/error/empty/success 状态、错误码、权限状态、异步任务状态、AI 降级和用户反馈 API。

不适用对象：

- 完整品牌系统、设计稿协作流程、大型组件库、视觉回归平台、全面用户研究计划。
- 法律级无障碍合规审计或正式 VPAT；这些需要专业审阅或单独 change。
- 纯内部一次性脚本界面；但如果它能修改生产数据或触发高风险动作，仍要遵守键盘、错误和确认基线。

## 最小工件

每个关键用户 surface 使用同一个 `<surface>` 文件名：

```text
ux-accessibility/
  surface-map/<surface>.md
  interaction-contract/<surface>.json
  accessibility-test-plan/<surface>.json
  ai-ux-disclosure/<surface>.md
  ux-review/<surface>.md
```

### `ux-accessibility/surface-map/<surface>.md`

Surface map 必须包含：

- `Scope`
- `Users / Context`
- `Critical Tasks`
- `Views / States`
- `Input Modes`
- `Accessibility Baseline`
- `AI Touchpoints`
- `Responsive / Theme`
- `Risks`
- `Linked Artifacts`

默认：

- 先列关键任务，不先列组件。一个 surface 通常只保留 1 到 3 条关键路径。
- 必须记录 desktop、mobile、keyboard-only、screen reader smoke、reduced motion、light/dark theme 是否适用。
- AI touchpoints 必须说明 AI 出现在哪里、影响什么决定、用户能否反馈/撤销/纠正。

### `ux-accessibility/interaction-contract/<surface>.json`

Interaction contract 必须包含：

- `surface`
- `owner`
- `users`
- `critical_tasks`
- `components`
- `states`
- `input_modes`
- `keyboard`
- `focus`
- `forms`
- `errors`
- `loading_empty_offline`
- `responsive`
- `theme`
- `ai_interactions`
- `human_checkpoint`
- `review_cadence`

`components` 每项至少包含：

- `id`
- `name`
- `role`
- `purpose`
- `states`
- `keyboard_support`
- `focus_behavior`
- `accessible_name_source`
- `aria_strategy`
- `status`

默认：

- 优先使用原生 HTML 控件；只有原生控件无法满足时才写 ARIA。
- 所有交互控件必须 keyboard reachable、visible focus、accessible name。
- `states` 至少覆盖 loading、empty、error、success；AI surface 还要覆盖 generating、degraded、blocked 或 human-review。
- 图标按钮必须有 `aria-label` 或可见文本；颜色状态必须配文本或图标。
- 表单字段必须有 label、helper text、error text、提交中状态和重复提交防护。

### `ux-accessibility/accessibility-test-plan/<surface>.json`

Accessibility test plan 必须包含：

- `surface`
- `owner`
- `standards`
- `tools`
- `checks`
- `viewports`
- `assistive_tech`
- `gates`
- `exceptions`
- `evidence_refs`
- `human_checkpoint`
- `status`

默认 `standards` 至少包含：

- `wcag_2_2_aa`
- `wai_aria_apg`
- `geist_design_md`

默认 `checks` 至少覆盖：

- `semantic_structure`
- `keyboard_navigation`
- `visible_focus`
- `focus_order`
- `contrast_light_dark`
- `form_labels_errors`
- `screen_reader_smoke`
- `reduced_motion`
- `responsive_reflow`
- `touch_target_size`
- `status_not_color_only`
- `ai_disclosure_feedback`

默认：

- 自动化工具只能作为底线，不能替代 keyboard-only 和人工 screen reader smoke。
- 早期一人公司不要求全屏幕阅读器矩阵；至少保留一个桌面浏览器 keyboard pass、一个移动 viewport pass、一个 screen reader smoke 记录。
- 有例外必须记录 `reason`、`owner`、`expires_at` 和 `mitigation`。

### `ux-accessibility/ai-ux-disclosure/<surface>.md`

AI UX disclosure 必须包含：

- `Scope`
- `AI Surfaces`
- `User Mental Model`
- `Disclosure Labels`
- `Limitations / Uncertainty`
- `Feedback / Correction`
- `Human Handoff`
- `Data Use / Controls`
- `Error / Degraded States`
- `Linked Artifacts`

默认：

- 用户应知道什么时候 AI 在生成、推荐、总结、分类或执行。
- AI 输出不能伪装成确定事实；需要展示来源、置信边界、可编辑/可撤销路径或人工复核路径。
- 高影响场景默认需要人工确认或明确边界。
- 用户反馈必须连接 W8 支持/反馈、W3 eval、W3 红队或 W5 UX review。

### `ux-accessibility/ux-review/<surface>.md`

UX review 必须包含：

- `Recent Changes`
- `Usability Findings`
- `Accessibility Findings`
- `AI Expectation Risks`
- `Metrics / Feedback`
- `Exceptions`
- `Open Risks`
- `Next One Change`

默认：

- pre-revenue：每月一次，或关键 surface / AI interaction 发布前。
- 有活跃用户：每两周一次，或每次改变关键任务、AI 输出呈现、用户控制、表单、导航、权限或计费路径前。
- 每次只选一个最高影响改进，避免一个人陷入无限打磨界面。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端错误模型必须能映射到用户可理解的 UI 状态：validation、auth、permission、quota、dependency、ai_degraded、ai_blocked、internal。
- gRPC / HTTP 响应不得只返回内部错误字符串；前端需要 code、message key、retryability、field errors、request id 和 user-safe next step。
- 异步 AI 任务必须暴露 pending/running/succeeded/failed/cancelled/degraded 状态，不让前端无限 loading。
- 支持反馈、纠错、撤销、重新生成、人工处理的 API 应有 actor、tenant、surface、ai_feature、request id 和 audit。
- sqlc 表可按需包含：`ux_feedback_events`、`ai_output_feedback`、`accessibility_exceptions`、`ui_incident_reports`。

## Vite / Geist 前端默认规则

- 默认 `Vite + React + TypeScript`；复杂交互用受控组件和清晰状态机，少量本地组件优先。
- 使用语义 HTML 和语义 token；不要在组件里散落 Vercel 原始 token。
- Geist light/dark token 必须分别检查 contrast、focus、hover、disabled、empty、error。
- `:focus-visible` 不得被移除；弹层/菜单/抽屉必须处理 focus trap、Esc、返回触发元素。
- 页面必须有 `main`、合理 heading、label、button、link、status/live region 或等价语义。
- 不使用颜色单独表达状态；AI 置信、风险、错误、警告、成功都要配文本或图标。
- 动效必须尊重 `prefers-reduced-motion`；AI 生成中状态不得依赖闪烁或长循环动画。
- 移动端和桌面端都不得出现文本溢出、按钮文字截断、控件重叠或不可点击目标。

## AI workflow 默认规则

- AI 输出区域必须区分 user input、AI output、retrieved context、tool result、human-reviewed result。
- AI 不确定时应提供来源、理由、下一步或纠错入口，不用绝对化语言包装概率结果。
- 生成、重试、取消、编辑、撤销、提交、人工复核必须有明确状态和可恢复路径。
- 对高风险动作，AI suggestion 不得直接变成 irreversible action；必须连接 admin action guard、auth boundary、red-team 或 release gate。
- 用户纠错和反馈进入 eval / prompt / routing 改进闭环，而不是只写进不可查询日志。

## 需要人判断的关键点

只把这些判断交给人：

- 是否允许关键用户路径未达到 WCAG 2.2 AA 或未完成 keyboard smoke 就上线。
- 是否采用自定义复杂 widget，而不是原生控件或成熟可访问组件。
- 是否在付费、权限、数据删除、医疗、法律、金融、就业、教育、身份或公共安全场景使用 AI 建议。
- 是否隐藏、弱化或省略 AI disclosure、限制、反馈、人工复核或用户控制。
- 是否接受 dark pattern、误导性默认值、强迫同意、取消困难或无法撤销的交互。
- 是否收集 sensitive personal data、biometric data、未成年人数据或会影响用户重大权益的数据。
- 是否发布新的品牌/营销界面，或明显改变产品承诺和用户心理模型。

其他字段完整性、章节、JSON 枚举、标准清单、测试项、状态覆盖、例外格式、敏感内容扫描和 OpenSpec linkage 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“谁用、怎么交互、怎么测、AI 如何说明、复盘什么”。
- 保留：人只判断 WCAG 例外、复杂 widget、高影响 AI、隐藏披露、dark pattern、敏感数据和品牌承诺。
- 调整：不要求正式用户研究团队；用关键任务、keyboard pass、screen reader smoke、反馈记录先建立最低闭环。
- 调整：不要求一次性覆盖所有页面；先覆盖登录、付费、设置、AI 输出、数据删除和核心工作流。
- 风险：可访问性容易被工具报告替代。缓解：test plan 必须包含人工 keyboard 和 screen reader smoke。

结论：可落地。一个人可以先为最重要 surface 写一个 interaction contract，再用 verifier 保证关键状态、焦点、表单和 AI disclosure 没被忘掉。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户能理解 AI 在做什么、哪里可能错、如何反馈或撤销，降低误用和信任损耗。
- 工程角度：前端状态和后端错误模型连接，避免“后端返回字符串、前端猜状态”。
- 运维角度：AI 降级、异步任务、反馈、无障碍例外和 UI incident 有复盘入口。
- 安全隐私角度：敏感数据、强制同意、隐藏控制、高影响建议和不可逆动作被显式升级。
- 成本角度：先用小型 smoke 和关键路径检查，不默认引入昂贵 UX lab、视觉回归平台或完整设计系统。

结论：可落地。本专项把“界面好不好用、AI 是否诚实、用户能否纠错”压成一组轻量但可检查的产品工程契约。
