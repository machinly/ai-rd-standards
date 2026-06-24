# api-contract-compatibility-standard 规格

## Purpose

定义一人公司生产 target 的 API 契约、兼容性、错误模型、contract tests 和 AI tool schema 演进规则，确保 gRPC/Protobuf、HTTP、event、frontend client 和 AI workflow 能安全演进。

## Requirements

### Requirement: 生产 target 必须定义 API 契约工件

生产服务、前端应用、webhook/event 或用户可见 AI workflow MUST 在发布前具备 API contract artifacts。

#### Scenario: 新生产 target 进入研发

- GIVEN 一个 target 会暴露 gRPC、HTTP、event、webhook、AI tool schema、frontend client 或其他可依赖 surface
- WHEN 创建 OpenSpec change
- THEN 创建 `contracts/surface-map/<target>.json`
- AND 创建 `contracts/compatibility-policy/<target>.md`
- AND 创建 `contracts/protobuf-evolution/<target>.md`
- AND 创建 `contracts/error-model/<target>.md`
- AND 创建 `contracts/contract-tests/<target>.json`
- AND 在 OpenSpec design 或 tasks 中链接 contract artifacts

### Requirement: Surface map 必须列出可依赖契约和消费者

Surface map MUST 记录 target、owner、audiences、surfaces、consumers、versioning、protobuf roots、generated clients、AI tool schemas、人审点和复审节奏。

#### Scenario: 创建 surface map

- GIVEN 一个 target 有可依赖 surface
- WHEN 创建 `contracts/surface-map/<target>.json`
- THEN 文件包含 `target`、`owner`、`audiences`、`surfaces`、`consumers`、`versioning`、`protobuf_roots`、`generated_clients`、`ai_tool_schemas`、`human_checkpoint`、`review_cadence`
- AND 每个 surface 记录 name、type、path、stability、version、consumers、owner、compatibility、deprecation

### Requirement: Compatibility policy 必须定义允许和破坏性变化

Compatibility policy MUST 以人可读方式记录 scope、compatibility definition、allowed changes、breaking changes、versioning、deprecation、consumer communication 和 human checkpoints。

#### Scenario: 创建 compatibility policy

- GIVEN 一个 target 有 stable 或 public surface
- WHEN 创建 `contracts/compatibility-policy/<target>.md`
- THEN 文档包含 Scope、Compatibility Definition、Allowed Changes、Breaking Changes、Versioning、Deprecation、Consumer Communication、Human Checkpoints
- AND policy 说明 source、wire 和 semantic compatibility

### Requirement: Protobuf 演进必须保护字段号、enum 和 generated code

Protobuf evolution document MUST 记录 proto sources、safe changes、reserved fields、enum rules、breaking checks、generated code 和 rollback。

#### Scenario: 创建 protobuf evolution 文档

- GIVEN 一个 target 有 gRPC/Protobuf surface
- WHEN 创建 `contracts/protobuf-evolution/<target>.md`
- THEN 文档包含 Scope、Proto Sources、Safe Changes、Reserved Fields、Enum Rules、Breaking Change Checks、Generated Code、Rollback
- AND 记录不改已发布字段号、不复用 tag、删除字段 reserve number/name、运行 buf breaking 或等价检查

### Requirement: Error model 必须稳定客户端可观察失败语义

Error model MUST 记录 gRPC status codes、validation errors、retry semantics、auth/permission errors、user-facing messages、observability 和 compatibility。

#### Scenario: 创建 error model

- GIVEN 一个 target 有 API 或 AI workflow
- WHEN 创建 `contracts/error-model/<target>.md`
- THEN 文档包含 Scope、gRPC Status Codes、Validation Errors、Retry Semantics、Auth / Permission Errors、User-Facing Messages、Observability、Compatibility
- AND 记录哪些错误可重试、哪些错误可展示给用户、哪些字段进入 telemetry

### Requirement: Contract tests 必须覆盖基线、消费者 fixtures 和 CI/release gates

Contract test plan MUST 记录 compatibility baseline、test suites、consumer fixtures、generated clients、CI gates、release gates、AI eval links 和 human checkpoints。

#### Scenario: 创建 contract test plan

- GIVEN 一个 target 有 stable 或 public surface
- WHEN 创建 `contracts/contract-tests/<target>.json`
- THEN 文件包含 `target`、`owner`、`compatibility_baseline`、`test_suites`、`consumer_fixtures`、`generated_clients`、`ci_gates`、`release_gates`、`ai_eval_links`、`human_checkpoint`
- AND Protobuf 变更包含 breaking check gate

### Requirement: AI tool schema 变化必须视为行为契约变化

AI tool schema、structured output schema、function name、required field、side-effect flag 或 fallback path changes MUST 具备 schema artifact、eval links、compatibility policy 和 rollback。

#### Scenario: 创建 AI tool schema contract

- GIVEN target 包含 AI tool 或 structured output
- WHEN 创建 `contracts/ai-tool-schemas/<target>.json`
- THEN 文件包含 `target`、`owner`、`schemas`、`eval_links`、`compatibility_policy`、`rollback`、`human_checkpoint`
- AND 每个 schema 记录 name、version、schema_path、strict、consumers、allowed_changes、breaking_changes、fallback
- AND human_checkpoint.required_for 包含 `ai_tool_schema_change`

### Requirement: 高风险契约变化必须人工 checkpoint

Stable/public 升级、breaking contract、proto field delete/renumber、error semantics change、AI tool schema change、deprecation removal 或 multi-version migration MUST 有人工 checkpoint。

#### Scenario: 接受高风险契约变化

- GIVEN 契约变更触发高风险条件
- WHEN 准备合并或发布
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND OpenSpec design 记录兼容性结论、消费者影响、测试证据和 rollback
