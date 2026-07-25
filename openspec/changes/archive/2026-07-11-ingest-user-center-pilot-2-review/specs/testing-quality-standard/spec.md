# testing-quality-standard 的变更规格

## MODIFIED Requirements

### Requirement: 生产目标必须定义测试质量工件

用户可见 Standard/High-risk target MUST 在实现前于 `governance/quality/` 定义测试策略、测试矩阵和关键用户旅程；Quick 和不改变行为的工作不创建。

#### Scenario: 新目标进入研发

- GIVEN 一个 target 会进入生产或影响用户可见行为
- WHEN 创建 Standard/High-risk OpenSpec change
- THEN 创建 `governance/quality/test-strategy/<target>.md`
- AND 创建 `governance/quality/test-matrix/<target>.json`
- AND 创建 `governance/quality/user-journeys.json`
- AND 在 OpenSpec design 或 tasks 中链接质量 artifacts

#### Scenario: 小型无风险变更

- GIVEN 一个变更不改变用户行为、权限、数据、成本、安全、AI 行为或发布配置
- WHEN 选择 Quick
- THEN 不创建 quality artifacts
- AND 交付时保留相关验证和剩余风险

### Requirement: Vite 前端必须有快速测试和关键路径 E2E

Vite frontend target MUST 记录 Vitest 或等价快速测试，并为每条阻断完成声明的关键用户路径提供 Playwright 或等价的可重复 Browser E2E。`skip_e2e` MAY 记录暂时阻塞，但 MUST NOT 支持 accepted 或 release-ready。

#### Scenario: Vite target

- GIVEN `stack.frontend` 是 Vite 或 change_types 包含 frontend
- WHEN 创建 test matrix
- THEN commands 包含 Vitest run 或等价命令
- AND commands 包含 build 命令

#### Scenario: 用户关键路径变化

- GIVEN change_types 包含 critical_user_flow、routing、form_submit、payment、file_upload、file_download 或 accessibility
- WHEN 判断范围是否完成
- THEN commands 包含 Playwright 或等价 E2E 命令
- AND 对应关键旅程最近一次状态为 pass
- AND 缺少或跳过 E2E 时当前状态不是 accepted

## ADDED Requirements

### Requirement: 用户可见能力必须定义关键旅程矩阵

关键旅程矩阵 MUST 对每条场景记录 id、role、goal、preconditions、steps、success、failure、evidence_level、command、evidence、status 和 last_run_at。功能/API 清单 MUST NOT 替代旅程。

#### Scenario: 定义登录旅程

- GIVEN 产品范围包含用户登录
- WHEN 建立验收映射
- THEN 场景记录角色与目标、前置账号/权限、真实页面步骤、成功和失败结果
- AND 记录自动化层级、运行命令、证据位置、状态和最后执行时间

### Requirement: Browser E2E 声明必须满足最低证据契约

`browser-e2e` evidence_level MUST 只用于可重复浏览器自动化：从页面入口完成真实点击、输入、导航和确认，业务动作不由 API 代替，断言页面与最终业务状态，失败保留 trace/截图/视频，并能从干净完整本地环境运行。

#### Scenario: 人工浏览器检查局部页面

- GIVEN 验收者手工检查了焦点、错误提示或局部 DOM
- WHEN 记录证据
- THEN 标为 `manual-browser-check` 或局部 component evidence
- AND 不标为 browser-e2e

#### Scenario: 自动化关键旅程

- GIVEN Playwright 从真实页面入口执行用户动作
- WHEN 旅程完成
- THEN 断言用户可见结果和必要最终业务状态
- AND 失败配置保留 trace、截图或视频
- AND 统一命令可在干净完整本地环境重跑
