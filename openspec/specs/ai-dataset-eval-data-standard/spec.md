# ai-dataset-eval-data-standard 规格

> 状态：可选历史主题规格，不是默认研发流程。只有主动选择本主题时，适用的 requirement 才作为检查清单；与 `docs/01-minimal-rd-kernel.md` 冲突时以最小内核为准。

## Purpose

Define the minimum one-person-company governance for AI datasets, eval examples, labeling rubrics, data quality reports, and refresh reviews so that AI release evidence is lawful, privacy-aware, repeatable, and separated from training data.

## Requirements

### Requirement: AI release evidence 必须定义 ai-data artifacts

Any AI capability, prompt/model/tool change, agent workflow, RAG behavior, safety behavior, or structured-output behavior used as release evidence MUST define AI dataset governance artifacts.

#### Scenario: 新 AI capability 准备进入发布门禁

- GIVEN 一个 AI capability 的输出会影响用户体验、用户承诺、安全边界、模型选择、prompt 变更或 release gate
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `ai-data/dataset-card/<dataset>.md`
- AND 创建 `ai-data/eval-set/<dataset>.jsonl`
- AND 创建 `ai-data/labeling-guide/<dataset>.md`
- AND 创建 `ai-data/quality-report/<dataset>.json`
- AND 创建 `ai-data/refresh-review/<dataset>.md`

### Requirement: Dataset card 必须记录来源、许可、隐私、用途和维护

Dataset card MUST record scope、purpose、source/provenance、consent/license、composition、splits、privacy/redaction、intended use、prohibited use、known gaps、maintenance 和 linked artifacts。

#### Scenario: Reviewer 判断数据是否可用于 release gate

- GIVEN AI release evidence 引用了某个 dataset
- WHEN reviewer 打开 `ai-data/dataset-card/<dataset>.md`
- THEN 能看到数据来源、是否可用、隐私分类、用途限制、缺口、维护人和相关 artifacts
- AND 公开数据、第三方数据、用户反馈、生产样本摘要或合成数据均有 provenance 与限制说明

### Requirement: Eval set 必须使用稳定 JSONL schema

Eval set MUST be JSONL and each row MUST include id、capability、input_ref 或 input、expected_behavior、rubric_ref、tags、source、split、risk_category、privacy_class、consent_or_license、created_at、reviewed_by、status 和 linked_artifact。

#### Scenario: Release gate 读取 eval examples

- GIVEN release gate 使用 `ai-data/eval-set/<dataset>.jsonl`
- WHEN 逐行解析 JSONL
- THEN 每行是 JSON object
- AND 每行有稳定 id、来源、split、隐私分类、许可/同意、rubric 引用和 linked artifact
- AND release gate 只使用 status 为 `ready` 且 split 属于 `eval`、`canary` 或 `red_team` 的样本

### Requirement: Labeling guide 必须定义标签、rubric、样例、分歧和校准

Labeling guide MUST define scope、labels、rubric、positive examples、negative examples、edge cases、disagreement、reviewer calibration 和 human checkpoints。

#### Scenario: 新标签或 grader 进入发布门禁

- GIVEN 一个标签、rubric、grader 或 judge score 将影响 release gate
- WHEN 更新 `ai-data/labeling-guide/<dataset>.md`
- THEN guide 说明如何判定 pass/fail、哪些是正例和反例、边界样本如何处理
- AND 模型生成标签或模型评分必须有人工校准或 spot check 记录

### Requirement: Quality report 必须记录覆盖、隐私、许可、重复、泄漏、标签质量和 gate 状态

Quality report MUST include dataset、owner、version、counts、splits、coverage、privacy_checks、license_checks、duplicate_checks、leakage_checks、label_quality、known_gaps、baseline_results、release_gate、human_checkpoint 和 status。

#### Scenario: 发布前评估 dataset 是否足够可信

- GIVEN 一个 AI release gate 准备运行或已经运行
- WHEN 查看 `ai-data/quality-report/<dataset>.json`
- THEN 能看到覆盖范围、隐私检查、许可检查、重复检查、train/eval 泄漏检查、标注质量、基线结果和 gate 结论
- AND `human_checkpoint.required_for` 包含本标准定义的高风险判断项

### Requirement: Refresh review 必须连接生产信号、用户反馈、漂移和下一步

Refresh review MUST record recent changes、production signals、user feedback、added/removed examples、drift/coverage、eval/train separation、open risks 和 next one change。

#### Scenario: AI 行为或数据分布变化

- GIVEN 近期有 prompt/model/tool/release 变更、用户反馈、投诉、安全事件、供应商条款变化或指标漂移
- WHEN 更新 `ai-data/refresh-review/<dataset>.md`
- THEN 记录新增/删除样本、覆盖变化、eval/train 分离状态和开放风险
- AND 只选择一个最高影响的 next one change

### Requirement: Eval、train、fine-tuning 和 prompt examples 必须分离并可追踪

Eval evidence MUST remain separated from training, validation, fine-tuning, distillation, and prompt-example data unless a human checkpoint records the movement, version, and reason.

#### Scenario: 将失败 eval case 移入训练或 prompt examples

- GIVEN 某个 eval case 暴露了产品失败
- WHEN 准备将该 case 移入训练、微调、蒸馏或 prompt examples
- THEN quality report 或 refresh review 记录源 id、目标用途、版本、原因和风险
- AND `human_checkpoint.required_for` 包含 `eval_to_training_or_finetune_move`
- AND 原 release evidence 保留可审计历史，不静默覆盖

### Requirement: 高风险数据和口径变化必须人工 checkpoint

Real user data, raw prompt/response use, sensitive or minor data, unclear consent/license, eval-to-training movement, third-party sharing, high-impact domains, synthetic-only release evidence, rubric/gate threshold changes, and deleting failed eval cases MUST have human checkpoint coverage.

#### Scenario: 数据或评测口径触发高风险条件

- GIVEN OpenSpec change、release、dataset refresh、quality report 或 labeling guide 触发高风险条件
- WHEN 准备把 dataset 标为 ready 或将其用于 release gate
- THEN `human_checkpoint.required_for` 包含对应触发项
- AND artifact 记录人的判断、风险接受或阻塞状态

### Requirement: AI data artifacts 不得保存敏感内容

AI data artifacts MUST NOT store secrets, production tokens, supplier credentials, full raw prompts, full raw responses, unredacted user data, payment data, private keys, or unnecessary personal contact data.

#### Scenario: 记录 eval example 或数据来源证据

- GIVEN 需要保存样本、来源、用户反馈、生产信号或失败案例
- WHEN 写入 `ai-data/` artifacts
- THEN 使用 redacted example、source id、hash、case id、artifact reference 或最小片段
- AND 不保存 secrets、生产 token、供应商凭据、完整 raw prompt、完整 raw response、未脱敏用户数据、支付数据或私钥
