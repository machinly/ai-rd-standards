# developer-experience-api-docs-sdk-standard Specification

## ADDED Requirements

### Requirement: 对外开发者 surface 必须具备 developer-experience 工件

任何生产 target 只要暴露 public/stable API、SDK、CLI、webhook、developer console、AI API、RAG API、tool/integration API 或客户可依赖的技术文档，MUST 具备 developer-experience artifacts。

#### Scenario: 发布开发者可依赖 surface

- GIVEN 一个 target 暴露 API、SDK、CLI、webhook、AI API、RAG API、tool/integration API 或技术文档给外部开发者
- WHEN 创建研发 OpenSpec change
- THEN 创建 `developer-experience/docs-portal/<target>.json`
- AND 创建 `developer-experience/api-reference/<target>.json`
- AND 创建 `developer-experience/sdk-examples/<target>.json`
- AND 创建 `developer-experience/changelog-release-notes/<target>.md`
- AND 创建 `developer-experience/dx-review/<target>.md`
- AND 在 OpenSpec proposal 或 design 中链接 developer-experience artifacts

### Requirement: Docs portal map 必须定义入口、受众、Diátaxis 覆盖、quickstart、认证、环境、支持路径和事实源

Docs portal map MUST make developer documentation discoverable and tied to authoritative sources.

#### Scenario: 创建开发者文档入口

- GIVEN 一个 target 有外部开发者文档
- WHEN 创建 `developer-experience/docs-portal/<target>.json`
- THEN it records target、owner、audiences、entrypoints、diataxis_coverage、quickstart、authentication、environments、support_paths、linked_artifacts、human_checkpoint、review_cadence、status
- AND public/stable APIs include quickstart, authentication, reference, errors/rate-limit docs, and changelog links

### Requirement: API reference 必须连接 spec source、生成 reference、认证、错误、rate limit、idempotency、pagination、webhook、示例和 contract tests

API reference artifacts MUST keep customer-facing reference aligned with proto, OpenAPI, schema, and contract-test facts.

#### Scenario: 发布或更新 API reference

- GIVEN 一个 target exposes gRPC, HTTP, webhook, event, SDK, CLI, or AI tool surfaces
- WHEN 创建 `developer-experience/api-reference/<target>.json`
- THEN it records target、owner、api_surfaces、spec_sources、generated_reference、auth、errors、rate_limits、idempotency、pagination、webhooks、request_response_examples、sdk_links、contract_test_links、status
- AND each api_surface includes name、protocol、stability、version、source、reference_path、example_path、owner
- AND examples do not contain secrets, personal data, customer content, raw prompts/responses, or production credentials

### Requirement: SDK/examples 必须记录语言、SDK、示例、quickstart 命令、test mode/sandbox、安全说明、CI gate 和 release gate

SDK/example artifacts MUST prove that developer onboarding examples are runnable or clearly marked conceptual.

#### Scenario: 发布 SDK 或示例代码

- GIVEN a target has SDKs, code samples, quickstart snippets, CLI examples, webhook examples, or AI examples
- WHEN 创建 `developer-experience/sdk-examples/<target>.json`
- THEN it records target、owner、languages、sdks、examples、quickstart_commands、test_mode_or_sandbox、security_notes、ci_gates、release_gates、human_checkpoint、status
- AND each example includes name、language、path、scenario、uses_test_mode、required_env_vars、expected_output、last_verified、status
- AND public runnable examples are verified in CI, release gates, or an explicit smoke-test record

### Requirement: Developer changelog 必须区分 breaking、added、changed、deprecated、fixed、security、migration 和 linked releases

Developer changelog MUST communicate notable integration changes instead of dumping commit history.

#### Scenario: 发布开发者可见变更

- GIVEN API, SDK, CLI, webhook, AI behavior, rate limit, error, auth, or schema behavior changes affect developers
- WHEN 更新 `developer-experience/changelog-release-notes/<target>.md`
- THEN it includes Scope, Versioning Policy, Unreleased, Breaking Changes, Added, Changed, Deprecated, Fixed, Security, Migration Notes, Linked Releases, and Review Cadence
- AND breaking/deprecation entries link to migration notes, contract tests, support window, or communication plan

### Requirement: DX review 必须复盘 quickstart、reference、SDK/examples、错误/rate limit/idempotency、AI/数据/安全边界、changelog、支持信号和一个下一步

DX review MUST keep developer experience aligned with actual support and adoption friction.

#### Scenario: 定期或变更前 DX review

- GIVEN a public developer surface changes or support signals show documentation friction
- WHEN 创建或更新 `developer-experience/dx-review/<target>.md`
- THEN it records Recent Changes, Quickstart Health, Reference Accuracy, SDK / Examples, Error / Rate Limit / Idempotency Docs, AI / Data / Security Boundaries, Changelog / Migration, Support Signals, Open Risks, One Next Change, and Review Cadence
- AND one-person review chooses one highest-impact next documentation or example fix
