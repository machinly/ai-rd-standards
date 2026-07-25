# ai-model-optimization-training-standard Specification

## ADDED Requirements

### Requirement: AI 模型优化候选必须具备 ai-optimization 工件

Any planned fine-tuning, distillation, provider customization, OSS adapter, or small-model replacement experiment for a user-visible AI capability MUST have AI optimization artifacts.

#### Scenario: 创建模型优化候选

- GIVEN a team considers supervised fine-tuning, DPO, RFT, distillation, small-model replacement, OSS adapter, provider customization, or other training-based optimization
- WHEN 创建研发 OpenSpec change
- THEN 创建 `ai-optimization/optimization-brief/<capability>.md`
- AND 创建 `ai-optimization/training-data-plan/<capability>.json`
- AND 创建 `ai-optimization/optimization-run/<capability>.json`
- AND 创建 `ai-optimization/validation-report/<capability>.md`
- AND 创建 `ai-optimization/rollout-decision/<capability>.md`
- AND 在 OpenSpec proposal 或 design 中链接 ai-optimization artifacts

### Requirement: Optimization brief 必须定义 baseline、失败分析、候选方法、更便宜替代方案、指标、数据边界和回滚

Optimization brief MUST prove that training-based optimization is the right lever before a run starts.

#### Scenario: 判断是否应该优化模型

- GIVEN a model behavior, quality, cost, latency, consistency, or formatting problem exists
- WHEN 创建 `ai-optimization/optimization-brief/<capability>.md`
- THEN it includes Scope, Capability, Baseline Behavior, Failure Analysis, Optimization Hypothesis, Alternatives Tried, Candidate Method, Success Metrics, Data Boundary, Cost / Latency Budget, Safety / Privacy, Rollback, Human Checkpoints, Linked Artifacts, and Review Cadence
- AND failure analysis distinguishes context, prompt, schema, retrieval, route, data quality, product flow, and model behavior causes
- AND Candidate Method selects one primary method for the optimization experiment

### Requirement: Training data plan 必须定义来源、许可、隐私、split、train/eval 分离、泄漏检查、覆盖和格式

Training data plan MUST keep optimization data lawful, representative, and separated from release evaluation data.

#### Scenario: 准备训练或蒸馏数据

- GIVEN optimization may use training, preference, distillation, or provider customization data
- WHEN 创建 `ai-optimization/training-data-plan/<capability>.json`
- THEN it records capability, owner, method, dataset_refs, eval_refs, source_summary, provenance, consent_license, privacy_classification, splits, train_eval_separation, leakage_checks, representative_coverage, data_minimization, format, filtering, human_checkpoint, and status
- AND dataset_refs link to dataset governance artifacts when method uses training or preference data
- AND train_eval_separation describes how release eval, canary, red-team, benchmark answers, incident examples, and production outputs are kept out of training unless explicitly approved
- AND real customer data, raw prompts/responses, production logs, support tickets, customer files, or regulated data require a human checkpoint

### Requirement: Optimization run 必须记录方法、供应商、base/candidate 模型、数据/eval 版本、训练配置、可用性、预算、隐私安全和回滚 route

Optimization run MUST be reproducible and auditable without exposing secrets or raw data.

#### Scenario: 运行模型优化实验

- GIVEN a model optimization candidate is ready to run
- WHEN 创建 `ai-optimization/optimization-run/<capability>.json`
- THEN it records capability, owner, method, provider, base_model, candidate_model_ref, job_or_run_ref, dataset_version_refs, eval_version_refs, training_config, availability_check, cost_limit, latency_target, safety_privacy_checks, rollback_route_ref, audit_refs, human_checkpoint, and status
- AND availability_check records provider API availability, account access, supported models, deprecation or legacy status, and fallback option
- AND candidate_model_ref is not used as production default until rollout-decision approves a route change

### Requirement: Validation report 必须比较 baseline/candidate 的质量、安全、成本、延迟、回归和生产模拟

Validation report MUST prove improvement without hiding regressions.

#### Scenario: 验证优化候选

- GIVEN an optimization run produces a candidate
- WHEN 创建 `ai-optimization/validation-report/<capability>.md`
- THEN it includes Scope, Baseline, Candidate, Eval Results, Regression Cases, Safety / Privacy Results, Cost / Latency Results, Production Simulation, Failure Analysis, Decision Evidence, Linked Artifacts, and Review Cadence
- AND compares baseline and candidate on task success, rubric score, structured output success, safety/refusal, regression cases, p95 latency, token/cost, and fallback rate where applicable
- AND high-risk regressions require a human checkpoint before rollout

### Requirement: Rollout decision 必须明确 no-go、重跑、shadow、小流量、生产或归档，并链接 route、rollback 和监控

Rollout decision MUST prevent optimized models from silently replacing production routes.

#### Scenario: 决定候选模型是否上线

- GIVEN validation report is complete
- WHEN 创建 `ai-optimization/rollout-decision/<capability>.md`
- THEN it includes Scope, Decision, Why, Rollout Plan, Route / Flag Changes, Rollback Plan, Monitoring, User / Support Impact, Follow Up, Human Checkpoints, Linked Artifacts, and Review Cadence
- AND Decision is no-go, rerun-with-better-data, ship-shadow, ship-small-cohort, ship-production, or archive-candidate
- AND ship-production links to model routing eval gate and AI quality rollback artifacts

### Requirement: 高风险优化动作必须保留人工 checkpoint

High-risk model optimization actions MUST be reviewed by the maintainer before they start, train, or roll out.

#### Scenario: 高风险优化动作

- GIVEN artifacts mention real fine-tuning, DPO, RFT, distillation, OSS adapter, provider customization, real customer data, raw prompt/response, support tickets, production logs, customer files, regulated data, eval-to-train movement, red-team-to-train movement, high-risk regression, shadow, small cohort, production route, legacy or deprecated provider capability, increased training budget, expanded data retention, provider data boundary change, or model/training evidence deletion
- WHEN verifier checks ai-optimization artifacts
- THEN the artifact records a human checkpoint or Human Checkpoints section
- AND the maintainer decides whether to proceed, block, narrow, rerun, no-go, archive, shadow, or roll out
