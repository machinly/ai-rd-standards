# ai-coding-workflow-standard 规格

## Purpose

定义一人公司 AI 协作编码、变更批次、自审、验证证据和人工 checkpoint 规则，确保 Codex/AI coding agent 的实现过程可计划、可 review、可恢复，并与 OpenSpec、测试、发布和安全边界衔接。

## Requirements

### Requirement: AI 协作编码变更必须具备会话工件

生产相关代码、prompt、配置、基础设施、测试、契约或发布流水线变更由 AI coding agent 参与实现时，MUST 创建 AI coding workflow artifacts。

#### Scenario: 开始 AI 协作实现

- GIVEN 一个 OpenSpec change 会产生生产相关仓库变更
- WHEN AI coding agent 开始实现
- THEN 创建 `ai-coding/implementation-brief/<change-id>.md`
- AND 创建 `ai-coding/batch-log/<change-id>.md`
- AND 创建 `ai-coding/review/<change-id>.md`
- AND 创建 `ai-coding/verification/<change-id>.json`

### Requirement: Implementation brief 必须界定目标、上下文、自治边界和停机条件

Implementation brief MUST 记录 OpenSpec change、desired outcome、non-goals、context sources、target files/modules、allowed autonomy、human checkpoints、verification commands、stop conditions 和 handoff。

#### Scenario: 创建实施 brief

- GIVEN 一个 AI coding session 准备修改仓库
- WHEN 创建 `ai-coding/implementation-brief/<change-id>.md`
- THEN 文档包含 OpenSpec Change、Desired Outcome、Non-Goals、Context Sources、Target Files / Modules、Allowed Autonomy、Human Checkpoints、Verification Commands、Stop Conditions、Handoff
- AND OpenSpec Change 链接 `openspec/changes/<change-id>/`

### Requirement: Batch log 必须控制变更批次和记录偏离

Batch log MUST 记录 batch scope、changes made、commands run、decisions、assumptions、deviations 和 follow-up。

#### Scenario: 完成一批 AI 实现

- GIVEN AI agent 完成一个实现批次
- WHEN 更新 `ai-coding/batch-log/<change-id>.md`
- THEN 文档包含 Batch Scope、Changes Made、Commands Run、Decisions、Assumptions、Deviations、Follow-Up
- AND 如果批次超过 8 个核心文件或 2 个逻辑变更，Deviations 说明拆分理由

### Requirement: Review artifact 必须覆盖功能、意图、AI 特有风险和合并判断

Review artifact MUST 记录 diff summary、functional review、intent/architecture review、AI-specific review、dependency/security review、human checkpoints、两轮 review 和 merge decision。

#### Scenario: AI 生成自审记录

- GIVEN AI coding session 有实现 diff
- WHEN 创建 `ai-coding/review/<change-id>.md`
- THEN 文档包含 Diff Summary、Functional Review、Intent / Architecture Review、AI-Specific Review、Dependency / Security Review、Human Checkpoints、Review 1、Review 2、Merge Decision
- AND Merge Decision 为 ready、blocked、needs-human 或 needs-more-tests

### Requirement: Verification JSON 必须记录可机器检查的验证证据

Verification JSON MUST 记录 change_id、owner、openspec_change、stack、batch_size、commands、verification_results、human_checkpoint、residual_risks 和 status。

#### Scenario: 记录验证结果

- GIVEN AI coding session 完成一批可 review 变更
- WHEN 创建 `ai-coding/verification/<change-id>.json`
- THEN 文件包含 `change_id`、`owner`、`openspec_change`、`stack`、`batch_size`、`commands`、`verification_results`、`human_checkpoint`、`residual_risks`、`status`
- AND `verification_results` 包含 `openspec`、`tests`、`builds`、`evals`、`security_checks`、`contract_checks`、`release_mapping`

### Requirement: Stack 相关验证命令必须与变更类型匹配

AI coding workflow MUST 根据 stack 记录对应验证命令和结果。

#### Scenario: Go/Kratos/sqlc/gRPC 变更

- GIVEN `stack` 包含 go、kratos、grpc、protobuf 或 sqlc
- WHEN 记录 verification JSON
- THEN `commands` 包含 `openspec validate`
- AND Go 变更包含 `go test`
- AND sqlc 变更包含 `sqlc generate`
- AND gRPC/Protobuf 契约变更包含 breaking、lint、buf 或 contract check

#### Scenario: Vite 前端或 AI workflow 变更

- GIVEN `stack` 包含 vite、frontend、react、ai、prompt、eval 或 agent
- WHEN 记录 verification JSON
- THEN Vite/frontend 变更包含 `npm run build` 或等价构建命令
- AND AI workflow 变更包含 eval、fixture 或 dry-run 验证

### Requirement: 高影响 AI 自治越界必须人工 checkpoint

Product scope change、real data/secret/vendor access、destructive operation、production deploy、new long-lived dependency、cost/autonomy increase、auth/tenant/API contract change、test deletion 或 multi-agent same-boundary change MUST 触发人工 checkpoint。

#### Scenario: AI agent 需要越过低风险自治边界

- GIVEN AI coding session 触发高影响条件
- WHEN 准备继续实现、合并或发布
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND implementation brief 或 review 记录需要人的判断

### Requirement: AI coding artifacts 不得保存敏感内容或 raw prompt/response

AI coding workflow artifacts MUST NOT 保存真实 secret、真实用户数据、供应商凭据、raw prompt、raw response 或可识别个人联系方式。

#### Scenario: 记录 AI coding session 证据

- GIVEN AI coding session 需要记录上下文和验证
- WHEN 写入 `ai-coding/` artifacts
- THEN 只保存可信上下文链接、行为版本、fixture、命令、结果和风险摘要
- AND 不保存 raw prompt、raw response、真实 secret、真实用户数据或供应商凭据
