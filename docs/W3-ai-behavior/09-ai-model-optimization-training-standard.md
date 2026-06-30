# AI 模型优化、微调/蒸馏与训练运行治理规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/00-main.md` 已经判断需要微调、蒸馏、模型优化、训练数据计划、验证报告或 rollout decision 时，才读取本文件。

如果当前只是判断 AI 行为应该如何定义好坏、失败和降级，先回到 `docs/W3-ai-behavior/00-main.md`。

## 目标

一人公司的 AI 产品很容易在质量焦虑下过早进入微调、蒸馏、偏好优化或自建训练流程。问题是：模型优化不是“让模型更聪明”的按钮，它会引入训练数据治理、train/eval 泄漏、供应商可用性、成本、延迟、回滚、质量漂移和长期维护负担。

本专项负责回答一个窄问题：**什么时候才允许做模型优化，以及一次优化实验如何证明它比 prompt、RAG、路由或产品流程改动更值得。**

默认原则：**没有 baseline eval、失败原因分类、可用训练数据边界、候选方法对比、验证报告和回滚路径，就不做模型优化。** 一人公司先榨干 prompt、检索、路由和数据质量，再进入微调/蒸馏/训练。

## 核心依据

- 《人月神话》：模型优化不是银弹；真正困难的是把产品定义、数据、评测、运行和回滚边界保持一致。
- 小型项目管理：一人公司不维护完整 MLOps 平台；只保留五个能支持 go/no-go 的工件。
- OpenAI Model Optimization / Optimizing LLM Accuracy：优化是 eval、prompt、RAG、fine-tuning 等方法的反馈循环；先找失败原因，再选合适杠杆。
- OpenAI Supervised Fine-Tuning / Fine-Tuning Best Practices：fine-tuning 前必须有可靠 eval；训练集和测试/评测集要分离；例子要代表生产输入输出。
- OpenAI Model Selection：先达到准确性目标，再优化成本和延迟；蒸馏通常是在已有准确性数据后，用较小模型维持质量、降低成本/延迟。
- OpenAI 当前 fine-tuning 文档：部分 fine-tuning 平台能力正在退场或转 legacy；新项目必须先确认官方可用性、模型支持和 deprecation timeline，不把某个训练接口当长期默认。
- Hidden Technical Debt in ML Systems：ML 系统的隐性债务来自数据依赖、配置、纠缠、反馈环和无人维护的训练路径。
- The ML Test Score：训练数据、模型、基础设施和监控都要测试；模型应像二进制一样可调试、可回滚、可监控。
- Google Rules of ML：先有简单可靠 pipeline、指标、good/bad 定义和数据新鲜度，再增加模型复杂度；警惕训练/服务偏移。
- NIST AI RMF / Generative AI Profile：AI 风险管理要覆盖设计、开发、评估、部署、使用和持续监控。

## 范围

适用对象：

- 用户可见 AI capability 的 supervised fine-tuning、DPO/RFT、vision fine-tuning、model distillation、prompt distillation、small-model replacement、OSS LoRA/adapter、provider-specific customization 或训练运行。
- 为了提高一致性、格式遵循、风格、分类、抽取、低成本/低延迟、特定任务表现而改变模型权重、训练数据或蒸馏数据的工作。
- Go/Kratos/sqlc/gRPC 后端中管理优化候选、训练运行、验证报告、模型版本、route 切换和审计的系统。
- Vite 前端中用于查看优化证据、验证结果、rollout 决策和人工审批的内部管理界面。

不适用对象：

- 普通 prompt、eval、agent workflow 的基础研发；走 W3 prompt/eval 专项。
- 数据集来源、标注、许可、刷新和 train/eval 分离的基础治理；走 W3 数据集专项。
- 生产模型路由、供应商 fallback、route policy 和 eval gate；走 W3 模型路由专项。
- RAG source、chunking、retrieval、citation 和 grounding；走 W3 RAG 专项。
- 线上 AI 质量事故、回滚和事故样例沉淀；走 W8 AI 质量回归专项。
- 大型自建训练平台、GPU 集群调度、持续训练、在线学习、RLHF 平台或研究团队级 MLOps；真实规模证明需要后再单独开 change。

## 最小工件

每个优化候选使用同一个 `<capability>` 文件名：

```text
ai-optimization/
  optimization-brief/<capability>.md
  training-data-plan/<capability>.json
  optimization-run/<capability>.json
  validation-report/<capability>.md
  rollout-decision/<capability>.md
```

### `ai-optimization/optimization-brief/<capability>.md`

优化 brief 必须包含：

```markdown
# <capability> Model Optimization Brief

## Scope

## Capability

## Baseline Behavior

## Failure Analysis

## Optimization Hypothesis

## Alternatives Tried

## Candidate Method

## Success Metrics

## Data Boundary

## Cost / Latency Budget

## Safety / Privacy

## Rollback

## Human Checkpoints

## Linked Artifacts

## Review Cadence
```

默认规则：

- `Failure Analysis` 先判断失败属于：缺上下文、指令不清、格式不稳、风格不一致、分类边界不清、工具/流程错误、数据质量差、模型能力不足、成本/延迟过高。
- 如果失败主要是缺知识、过期知识、租户上下文或引用不足，优先 RAG/检索/数据同步，不优先 fine-tuning。
- 如果失败主要是输出格式、风格、分类、抽取口径或固定任务一致性，才考虑 SFT/DPO/RFT/蒸馏。
- `Alternatives Tried` 至少记录 prompt、few-shot、schema、RAG、route 或产品流程中适用的 1-3 个更便宜方案，以及为什么不够。
- `Candidate Method` 只允许一个主方法进入本轮实验，避免同时调 prompt、RAG、数据、模型和 route 导致不可归因。

### `ai-optimization/training-data-plan/<capability>.json`

训练数据计划必须包含：

- `capability`
- `owner`
- `method`
- `dataset_refs`
- `eval_refs`
- `source_summary`
- `provenance`
- `consent_license`
- `privacy_classification`
- `splits`
- `train_eval_separation`
- `leakage_checks`
- `representative_coverage`
- `data_minimization`
- `format`
- `filtering`
- `human_checkpoint`
- `status`

默认规则：

- `method` 使用 `sft`、`dpo`、`rft`、`distillation`、`small_model_replacement`、`oss_adapter`、`provider_customization`、`no_training_baseline`。
- `dataset_refs` 必须链接 W3 数据集专项的 dataset card / eval set / quality report；不在本文件存训练样本原文。
- `eval_refs` 必须包含 holdout eval、canary 或 red-team 中适用的评测引用。
- `splits` 至少明确 train、validation、eval/holdout 的来源或说明为什么某个 split 不适用。
- `train_eval_separation` 必须说明如何防止 release eval、benchmark answer、事故样例和生产输出泄漏到训练集。
- 真实客户数据、支持工单、生产日志、raw prompt/response、客户文件或受监管数据进入训练候选时，必须有人工 checkpoint，并连接 W2 客户数据/供应商/IP 证据和 W3 数据集证据。

### `ai-optimization/optimization-run/<capability>.json`

优化运行记录必须包含：

- `capability`
- `owner`
- `method`
- `provider`
- `base_model`
- `candidate_model_ref`
- `job_or_run_ref`
- `dataset_version_refs`
- `eval_version_refs`
- `training_config`
- `availability_check`
- `cost_limit`
- `latency_target`
- `safety_privacy_checks`
- `rollback_route_ref`
- `audit_refs`
- `human_checkpoint`
- `status`

默认规则：

- `availability_check` 记录供应商接口、账号权限、模型支持、deprecation/legacy 状态和替代方案；OpenAI fine-tuning 等平台能力必须按当前官方文档确认。
- `training_config` 只保存参数、版本和引用，不保存 secret、完整训练数据、客户原文或供应商 token。
- `cost_limit` 和 `latency_target` 必须先写；优化运行不能在没有预算边界时反复试。
- `candidate_model_ref` 不得直接替换生产默认 route；必须先进入 validation report 和 rollout decision。
- 每个训练/优化运行必须可审计：谁启动、为什么、用哪个数据版本、预算多少、输出模型如何禁用或删除。

### `ai-optimization/validation-report/<capability>.md`

验证报告必须包含：

```markdown
# <capability> Model Optimization Validation Report

## Scope

## Baseline

## Candidate

## Eval Results

## Regression Cases

## Safety / Privacy Results

## Cost / Latency Results

## Production Simulation

## Failure Analysis

## Decision Evidence

## Linked Artifacts

## Review Cadence
```

默认规则：

- 至少比较 baseline 与 candidate：任务成功、rubric 分数、结构化输出成功率、安全/拒答、关键失败样例、p95 latency、token/成本、fallback 触发率。
- `Regression Cases` 必须包含 candidate 变差的样例；不能只展示提升样例。
- `Production Simulation` 说明候选模型是否使用和生产相同 prompt、RAG context、tool schema、system/developer instructions、locale、tenant/data boundary。
- 如果指标提升但失败集中在高风险用户路径、安全/隐私、资金/权限/法律/医疗等场景，默认 no-go 或人工 checkpoint。
- 验证报告不等同上线许可；上线仍需 rollout decision 和 W3 route/eval gate。

### `ai-optimization/rollout-decision/<capability>.md`

上线决策必须包含：

```markdown
# <capability> Model Optimization Rollout Decision

## Scope

## Decision

## Why

## Rollout Plan

## Route / Flag Changes

## Rollback Plan

## Monitoring

## User / Support Impact

## Follow Up

## Human Checkpoints

## Linked Artifacts

## Review Cadence
```

`Decision` 只允许：

- `no-go`
- `rerun-with-better-data`
- `ship-shadow`
- `ship-small-cohort`
- `ship-production`
- `archive-candidate`

默认规则：

- `ship-production` 必须链接 W3 route policy/eval gate 和 W8 quality rollback。
- `ship-small-cohort` 必须有 feature flag、tenant/user cohort、rollback route、quality signal 和支持路径。
- `no-go` 也要记录原因，避免以后重复花钱训练同一方向。
- 如果候选优化依赖即将退场的供应商能力、实验性模型、不可迁移数据格式或高成本训练路径，默认不作为核心生产依赖。

## 默认流程

1. 写 `optimization-brief`：确认失败类型、baseline 和更便宜方案是否已经尝试。
2. 写 `training-data-plan`：确认数据来源、split、泄漏检查、隐私/许可和 W3 数据集链接。
3. 写 `optimization-run`：确认供应商可用性、模型支持、预算、训练配置和回滚 route。
4. 跑候选优化或记录 no-training baseline。
5. 写 `validation-report`：比较 baseline/candidate 的质量、安全、成本、延迟和 regression。
6. 写 `rollout-decision`：no-go、重跑、shadow、小流量或生产；生产必须连接 W3 route gate 和 W8 quality rollback。

## Go / Kratos / sqlc / gRPC 默认规则

- 后端使用显式 `ModelOptimizationService` 或等价 usecase 管理优化候选、数据计划、运行、验证和 rollout 决策。
- gRPC API 可选：CreateOptimizationBrief、ValidateTrainingDataPlan、RegisterOptimizationRun、RecordValidationReport、DecideOptimizationRollout。
- sqlc 表可选：`ai_optimization_candidates`、`ai_optimization_runs`、`ai_optimization_validations`、`ai_optimization_decisions`；只保存引用、状态、指标摘要和审计信息。
- 训练作业、供应商文件、模型 id、数据版本和 eval run id 必须可关联；生产请求只读 route，不直接读 optimization run。
- 不在业务代码硬编码 fine-tuned model id；通过 W3 route registry / feature flag / config 推进。
- 所有优化运行必须有 audit ref；涉及真实数据、供应商训练文件、模型删除、生产 route 切换时连接 W7 admin ops。

## Vite 前端默认规则

- 内部管理 UI 只展示优化证据：baseline、candidate、数据版本、eval 结果、回归样例、安全/隐私、成本/延迟和决策。
- 高风险按钮使用明确动作：启动训练、取消训练、归档候选、进入 shadow、小流量、生产、回滚。
- 不展示 raw customer data、raw prompt/response、供应商 secret、训练文件下载链接或未脱敏样本原文。
- 用 Vercel Geist 风格保持密集、可扫描、低装饰；结果表格优先显示 pass/fail、delta、evidence link 和 blocker。
- `ship-production` 或 `archive-candidate` 必须显示 linked route、rollback 和 audit evidence。

## AI workflow 默认规则

- 优化前先跑 baseline eval；优化后必须跑同一 eval version 加上 regression/canary/red-team 中适用集合。
- 不把 eval set、red-team answer、benchmark answer 或线上事故样例直接加入训练，除非 W3 数据集专项记录 split 迁移和人工 checkpoint。
- 合成数据可以用于扩展覆盖，但高风险能力不能只靠合成数据证明 fine-tune/distillation 可上线。
- 自动生成训练样本或 preference pair 时，必须有人工 spot check、rubric 和污染检查。
- 如果候选模型让 prompt 更短、成本更低但质量/安全回归，默认 no-go；不能只看成本胜出。

## 需要人判断的关键点

默认不问：

- 文件命名、普通字段完整性、指标表格格式、低风险 no-go 归档、synthetic-only 本地实验记录。

必须问：

- 是否进入真实 fine-tuning、DPO/RFT、蒸馏、OSS adapter 或供应商自定义训练。
- 是否使用真实客户数据、raw prompt/response、支持工单、生产日志、客户文件、受监管数据或授权不清数据。
- 是否把 eval/canary/red-team/事故样例移入训练或偏好数据。
- 是否接受候选模型在高风险路径、安全/隐私、权限/资金/法律/医疗场景的回归。
- 是否把候选模型切到 shadow、小流量或生产 route。
- 是否依赖 legacy/deprecated/实验性供应商训练能力作为核心生产路径。
- 是否提高训练预算、扩大数据保留、改变供应商数据边界或删除候选模型/训练文件。

其他章节、字段、敏感信息、状态枚举、split 检查、OpenSpec 链接、positive/negative fixture 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“为什么优化、用什么数据、跑了什么、是否更好、能否上线”。
- 保留：人只判断真实训练、敏感数据、eval/train 边界、高风险回归、route 切换、legacy 依赖和预算/数据边界变化。
- 调整：不要求训练平台、模型 registry 平台或自动调参；先用文件和 eval evidence 控制一次实验。
- 调整：允许 `no_training_baseline`，把“不要训练”也变成可记录决策。
- 风险：优化实验会变成无止境调参。缓解：每次只允许一个主方法、一个 success metric 组合和明确 no-go 规则。

结论：可落地。本专项能让一个人在半天到数天内完成一次可审查优化实验，而不是把微调变成长期黑洞。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：先按失败类型选杠杆，避免为缺上下文问题做 fine-tuning。
- 工程角度：训练运行、数据版本、eval 版本、候选模型和 route 决策可追踪、可回滚。
- 运维角度：候选模型进入生产前要连接 W3 route gate 和 W8 quality rollback。
- 安全隐私角度：真实数据、客户内容、train/eval 泄漏、供应商训练文件和 legacy 能力都有 checkpoint。
- 成本角度：预算、latency target、small model replacement 和 no-go 归档能避免反复训练烧钱。

结论：可落地。它补上 W3 prompt/eval、数据集、模型路由与 W8 质量回滚之间的训练治理空白：先评估和证明，再训练；先验证和回滚，再上线。
