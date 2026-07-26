## Why

当前正式研发规范已经定义关键任务、surface、基本状态、可访问性和浏览器证据，但没有把“开发前看见静态界面方案并由人确认可开发”设为清晰门禁。结果是实现者可能只凭文字推断页面结构、高风险交互和状态反馈，直到开发后才发现体验分歧。

本 change 落实已获认可的 `docs/superpowers/specs/2026-07-24-rd-visual-ux-step-design.md`，只调整现有研发规范和薄路由，不建设通用 UX Kit。

## Routing

- path: Standard
- visual_ux: not-required
- reason: 本 change 修改研发规范文档与路由，不新增或改变产品用户界面。

## What Changes

- 在“体验设计”中加入条件触发的静态低保真 UX、最小仓库产物、高保真条件升级和人工 `approved` 门禁。
- 在“计划”中加入 `visual_ux` 判定、工件链接和 production implementation readiness 检查。
- 在“实现”中加入批准检查，以及任务路径、状态、权限含义或高风险确认偏离时返回体验设计的规则。
- 在“验证”中加入 Browser E2E、desktop/mobile 条件截图、四类基本状态、keyboard/focus 与已批准线框的一致性检查。
- 更新 `one-person-openspec-rd` 的路由和 review rubric，不复制正式体验设计正文。
- 更新正式 rule-id 测试、既有来源映射和当前治理状态。

## Non-Goals

- 不新增研发分类或项目。
- 不建设通用 UX Kit、跨项目组件 catalog、pattern ID、schema、renderer 或专用 verifier。
- 不制作可交互原型，不强制 Figma、Penpot 或其他外部设计工具。
- 不建立像素级视觉回归平台。
- 不自动迁移历史项目，不修改产品方向、发布授权或高风险责任边界。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `accessibility-ai-ux-standard`：在适用界面变更中加入开发前静态可视 UX 与明确人类批准。
- `ai-coding-workflow-standard`：禁止实现者在 required UX 未批准时开始生产性实现，禁止在代码中静默改设计。
- `testing-quality-standard`：要求用 Browser E2E 和条件截图对照已批准 UX，截图不替代业务旅程。

## Impact

- 正式规范继续保持四分类、十一项目，体验设计拥有可视 UX 语义。
- 新增 8 个正式 rule-id，总数由 2313 变为 2321；原子来源规则仍为 5956。
- 运行时只同步 `one-person-openspec-rd` 的三个路由/review 文件。
- 回滚通过后续 Standard change 收窄触发范围或移除计划/实现门禁；已有线框和 review 保留为历史证据。
