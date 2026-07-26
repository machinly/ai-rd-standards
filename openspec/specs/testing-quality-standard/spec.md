# testing-quality-standard Specification

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

定义一人公司测试与质量策略的最小基线，使生产服务、前端应用和用户可见 AI workflow 能用风险驱动方式记录测试组合、运行命令、AI eval、flaky 处理、发布前 test run 和质量例外人审点。
## Requirements
### Requirement: 生产目标必须定义测试质量工件

用户可见 Deliver Standard/High-risk target MUST 在实现前于 `governance/quality/` 定义测试策略、测试矩阵和关键用户旅程；Deliver Quick、不改变行为的工作和轻量 Explore 不默认创建完整质量工件。Explore 或 Quick 实际命中的授权、安全、数据或其他风险控制 MUST 继续适用。

#### Scenario: 新目标进入研发

- **GIVEN** 一个 target 会进入生产或影响用户可见行为
- **WHEN** 创建 Deliver Standard/High-risk OpenSpec change
- **THEN** 创建 `governance/quality/test-strategy/<target>.md`
- **AND** 创建 `governance/quality/test-matrix/<target>.json`
- **AND** 创建 `governance/quality/user-journeys.json`
- **AND** 在 OpenSpec design 或 tasks 中链接质量 artifacts

#### Scenario: 小型无风险变更

- **GIVEN** 一个变更不改变用户行为、权限、数据、成本、安全、AI 行为或发布配置
- **WHEN** 选择 Deliver Quick
- **THEN** 不创建 quality artifacts
- **AND** 交付时保留相关验证和剩余风险

#### Scenario: 轻量 Explore

- **GIVEN** 工作保持在本地可恢复 sandbox 且目标是减少关键未知
- **WHEN** 选择 Explore
- **THEN** 不默认创建完整 test strategy、test matrix、user journey matrix 或 Browser E2E
- **AND** showcase 仍使用真实入口、可理解 fixture 并准确记录证据限制

### Requirement: Test strategy 必须覆盖风险、组合、命令和例外

Test strategy MUST 记录测试范围、风险、测试组合、AI eval、fixtures、flaky policy、命令和人工 checkpoint。

#### Scenario: 创建 test strategy

- GIVEN 一个 target 准备进入生产质量门禁
- WHEN 创建 `quality/test-strategy/<target>.md`
- THEN 文档包含 Scope、Risk、Test Portfolio、Small Tests、Medium Tests、Large Tests、AI Evals、Fixtures、Flaky Policy、Commands、Human Checkpoints

### Requirement: Test matrix 必须把 stack 风险映射到可运行命令

Test matrix MUST 用机器可检查格式记录 stack、变更类型、测试层级、命令、coverage focus、flaky policy、release gate 和人审点。

#### Scenario: 创建 test matrix

- GIVEN 一个 target 需要质量门禁
- WHEN 创建 `quality/test-matrix/<target>.json`
- THEN 文件包含 `target`、`owner`、`risk_level`、`stack`、`change_types`、`small_tests`、`medium_tests`、`large_tests`、`contract_tests`、`smoke_tests`、`ai_evals`、`commands`、`coverage_focus`、`fixtures`、`flaky_policy`、`release_gate`、`human_checkpoint`、`review_cadence`

#### Scenario: 定义 commands

- GIVEN test matrix 包含 commands
- WHEN 校验 commands
- THEN 每个 command 包含 `name`、`command`、`tier`、`when`
- AND release gate 至少引用一个 command

### Requirement: Go/Kratos/sqlc/gRPC 目标必须有默认后端测试门禁

Go/Kratos/sqlc/gRPC target MUST 记录 Go 测试、sqlc 检查和 gRPC/API 行为测试。

#### Scenario: Go target

- GIVEN `stack.languages` 包含 Go
- WHEN 创建 test matrix
- THEN commands 包含 `go test ./...`

#### Scenario: 并发风险

- GIVEN `change_types` 或 `risk_level` 表示 concurrency、worker、stream、cache、goroutine、agent loop 或 shared state
- WHEN 创建 test matrix
- THEN commands 包含 `go test -race`
- OR `human_checkpoint.required_for` 包含 `skip_race_test`

#### Scenario: sqlc 或 schema 变化

- GIVEN `stack` 表示 sqlc、MySQL、database 或 schema_changes
- WHEN 创建 test matrix
- THEN commands 包含 `sqlc generate`
- AND commands 包含 `sqlc vet`
- AND schema 兼容性高风险时 commands 包含 `sqlc verify` 或人审点包含 `skip_sqlc_verify`

#### Scenario: gRPC API 变化

- GIVEN `stack.protocols` 包含 gRPC 或 change_types 包含 grpc_api
- WHEN 创建 test matrix
- THEN contract_tests 或 medium_tests 覆盖 success、validation failure、auth/permission failure、not found、deadline/cancel 中适用项

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

### Requirement: AI workflow 变化必须有 eval 门禁

AI prompt、model、tool、agent route、retrieval、guardrail 或 output schema 变化 MUST 定义可重复 eval。

#### Scenario: AI workflow target

- GIVEN `stack.ai_workflow` 为 true 或 change_types 包含 prompt、model、tool、agent、retrieval、guardrail、output_schema
- WHEN 创建 test matrix
- THEN `ai_evals` 包含 dataset、representative_cases、boundary_cases、failure_cases、metrics、threshold、command、human_calibration

#### Scenario: AI eval 未通过

- GIVEN AI eval 结果低于 threshold
- WHEN 准备发布
- THEN `human_checkpoint.required_for` 包含 `ship_with_failed_ai_eval` 或 release gate 阻止发布

### Requirement: Flaky 测试必须可见且有修复期限

Known flaky、retry 或 quarantine MUST 有 owner、影响、修复期限和发布风险记录。

#### Scenario: 存在 flaky 测试

- GIVEN `flaky_policy.known_flaky` 非空或 `flaky_policy.retry_allowed` 为 true
- WHEN 创建 quality artifacts
- THEN 创建 `quality/flaky-tests/<target>.md`
- AND 文档包含 Known Flakes、Impact、Quarantine Rule、Owner、Fix By、Release Risk

#### Scenario: 带 flaky 发布

- GIVEN 有 known flaky 且 release gate 准备通过
- WHEN 发布
- THEN `human_checkpoint.required_for` 包含 `ship_with_known_flaky`
- AND release log 或 test-runs 记录风险接受

### Requirement: Test run 必须记录发布前质量证据

生产发布前 MUST 记录最近一次关键 test run 结果。

#### Scenario: 发布前记录 test run

- GIVEN target 准备发布
- WHEN 运行 release gate tests
- THEN 追加 `quality/test-runs/<target>.jsonl`
- AND 每行包含 `date`、`target`、`context`、`command`、`result`
- AND result 失败时不得发布，除非有对应 human checkpoint

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

### Requirement: Required 可视 UX 必须以浏览器证据核对已批准方案

`visual_ux: required` change MUST 用可重复 Browser E2E 证明关键旅程，并用 desktop screenshot 核对已批准 wireframes；只有布局实质不同时才要求 mobile screenshot。验证 MUST 覆盖适用的 loading、empty、error、success、keyboard-only、visible focus 和 focus order，并记录实质差异及重新 review 证据。Screenshot MUST NOT 替代 Browser E2E。

#### Scenario: 实现与已批准 UX 一致

- **WHEN** 在干净完整本地环境验证 required 可视 UX change
- **THEN** Browser E2E 从页面入口完成真实用户动作并断言最终状态
- **AND** desktop screenshot 可与当前批准 wireframe 核对
- **AND** 布局实质不同时有 mobile screenshot

#### Scenario: 浏览器实现存在实质偏差

- **WHEN** 任务路径、结构、状态、权限含义或高风险确认与批准 UX 不一致
- **THEN** 验证不得把该路径标为 accepted
- **AND** 返回体验设计更新并重新 review

### Requirement: Explore showcase 必须使用真实产品入口和可理解 fixture

用户可见 Explore showcase MUST 复用实际产品入口和真实页面动作，使用 Alice、Bob、Admin 等人类可识别 fixture，并展示可理解的业务结果。它 MUST NOT 通过另建静态展示站、opaque ID、API success、DOM 存在或数据库行来代替用户是否理解并完成任务的事实。

#### Scenario: UX Prototype 进行 showcase

- **GIVEN** UX Prototype 已形成一个可运行 shortest slice
- **WHEN** 向人展示结果
- **THEN** 从实际产品入口完成关键页面动作
- **AND** 使用可识别角色和数据
- **AND** 记录 observed behavior、visible fact、limits 和 next decision

#### Scenario: Technical Spike 只有 API 成功

- **GIVEN** Technical Spike 的 API、数据库和服务分别通过检查
- **WHEN** 尚未从一个用户入口形成可见业务结果
- **THEN** 不把这些局部成功声明为完整 showcase
- **AND** 继续缩小 Walking Skeleton 或准确记录未覆盖证据

### Requirement: Explore 证据不得冒充 Deliver 验收

Explore showcase MUST 准确命名 observed behavior、visible fact 和证据限制。除非满足完整 Browser E2E 最低证据契约，否则 MUST NOT 命名为 Browser E2E；无论是否可运行，Explore 证据 MUST NOT 被声明为 Deliver accepted、release-ready 或 production-ready。

#### Scenario: Showcase 尚未满足 Browser E2E

- **GIVEN** Explore 从实际入口展示了一个可见结果
- **AND** 没有满足完整环境、自动化旅程、业务断言和可重复执行契约
- **WHEN** 记录验证证据
- **THEN** 将证据命名为 showcase
- **AND** 明确未覆盖 Browser E2E 和 Deliver acceptance

#### Scenario: Explore 结果无效

- **GIVEN** showcase 证伪了当前 hypothesis
- **WHEN** 结束本轮 Explore
- **THEN** 可以记录 `invalidated`、`revise` 或 `stopped`
- **AND** 不为获得通过状态而隐藏负面事实

### Requirement: 测试先行范围必须与行为风险匹配

测试策略 MUST 对核心领域规则、服务端授权、安全边界、数据一致性、公共契约、bugfix 和危险重构优先测试先行。抛弃式 UI 脚手架、生成代码、简单配置和 UX/Technical Explore MAY 先实现后补 selected behavior 的自动化；任何准备 promote 的稳定行为 MUST 在 Deliver 前补齐与风险相称的回归证据。

#### Scenario: Explore 中的抛弃式脚手架

- **GIVEN** 脚手架仅用于比较 UX 或验证技术可行性
- **AND** 当前实现不会作为 selected increment 进入 Deliver
- **WHEN** 选择测试顺序
- **THEN** 不要求所有探索代码先写失败测试
- **AND** 仍对实际命中的安全、授权或数据风险执行对应门禁

#### Scenario: Selected behavior 准备 promote

- **GIVEN** 人选择一个 Explore 行为作为稳定增量
- **WHEN** 准备转换为 Deliver
- **THEN** 为该行为补齐与风险相称的自动化回归证据
- **AND** 不追溯要求所有失败探索采用 TDD
