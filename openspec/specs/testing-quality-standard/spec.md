# testing-quality-standard Specification

## Purpose

定义一人公司测试与质量策略的最小基线，使生产服务、前端应用和用户可见 AI workflow 能用风险驱动方式记录测试组合、运行命令、AI eval、flaky 处理、发布前 test run 和质量例外人审点。

## Requirements

### Requirement: 生产目标必须定义测试质量工件

生产服务、前端应用或用户可见 AI workflow MUST 在超过 1 个工作日的用户可见变更前具备测试质量 artifacts。

#### Scenario: 新目标进入研发

- GIVEN 一个 target 会进入生产或影响用户可见行为
- WHEN 创建超过 1 个工作日的 OpenSpec change
- THEN 创建 `quality/test-strategy/<target>.md`
- AND 创建 `quality/test-matrix/<target>.json`
- AND 在 OpenSpec design 或 tasks 中链接测试质量 artifacts

#### Scenario: 小型无风险变更

- GIVEN 一个变更不改变用户行为、权限、数据、成本、安全、AI 行为或发布配置
- WHEN 不创建 quality artifacts
- THEN 在 OpenSpec tasks 或变更说明中记录跳过原因

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

- GIVEN `stack` 表示 sqlc、PostgreSQL、database 或 schema_changes
- WHEN 创建 test matrix
- THEN commands 包含 `sqlc generate`
- AND commands 包含 `sqlc vet`
- AND schema 兼容性高风险时 commands 包含 `sqlc verify` 或人审点包含 `skip_sqlc_verify`

#### Scenario: gRPC API 变化

- GIVEN `stack.protocols` 包含 gRPC 或 change_types 包含 grpc_api
- WHEN 创建 test matrix
- THEN contract_tests 或 medium_tests 覆盖 success、validation failure、auth/permission failure、not found、deadline/cancel 中适用项

### Requirement: Vite 前端必须有快速测试和关键路径 E2E

Vite frontend target MUST 记录 Vitest 或等价快速测试，并为关键用户路径定义 Playwright 或等价 E2E。

#### Scenario: Vite target

- GIVEN `stack.frontend` 是 Vite 或 change_types 包含 frontend
- WHEN 创建 test matrix
- THEN commands 包含 Vitest run 或等价命令
- AND commands 包含 build 命令

#### Scenario: 用户关键路径变化

- GIVEN change_types 包含 critical_user_flow、routing、form_submit、payment、file_upload、file_download 或 accessibility
- WHEN 创建 test matrix
- THEN commands 包含 Playwright 或等价 E2E 命令
- OR `human_checkpoint.required_for` 包含 `skip_e2e`

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
