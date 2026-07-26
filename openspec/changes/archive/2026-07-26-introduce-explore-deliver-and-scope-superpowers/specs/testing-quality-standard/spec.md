## ADDED Requirements

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

## MODIFIED Requirements

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
