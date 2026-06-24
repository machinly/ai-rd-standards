# AI 数据集、评测样本、标注与数据刷新治理规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/main.md` 已经判断需要治理 eval 数据集、样本来源、标注口径、train/eval 分离、质量报告或刷新复盘时，才读取本文件。

如果当前只是判断 AI capability 的目标行为、失败行为、拒绝行为或降级行为，先回到 `docs/W3-ai-behavior/main.md`。

## 目标

一人公司做 AI 产品时，最容易被低估的风险不是“没有 eval”，而是 eval 背后的数据没有来历、没有许可、没有隐私边界、没有标注口径、没有刷新记录，最后变成一堆看似能跑、实际不可复用也不可解释的样本。本专项定义 AI 数据集、评测样本、标注与刷新治理规范，让每个 AI capability 都能回答：样本从哪里来，能不能用，用来评测还是训练，谁标注，怎样复查，什么时候需要人判断。

默认原则：没有 provenance、许可或同意、隐私分类、标注口径和刷新记录的数据集，不得作为 release gate 证据。

## 核心依据

- 《人月神话》：复杂度经常藏在边界和概念不一致里；数据集如果没有统一口径，会把 prompt、模型、产品和运维判断拖进长期返工。
- 小型项目管理：一人公司不能维护完整数据治理平台；只保留 dataset card、eval set、labeling guide、quality report、refresh review 五个可执行工件。
- OpenAI Evaluation Best Practices / Datasets / Graders：eval 需要贴近真实任务分布，明确“好”的定义，使用可重复数据集和评分器，并持续迭代。
- OpenAI Model Optimization：训练、验证和优化数据的格式与质量会直接影响模型优化结果；评测集和训练/微调数据必须分离。
- Google Rules of ML：先保证 pipeline、指标、good/bad 定义和数据新鲜度，再增加模型复杂度；训练/服务偏差和静默数据失败需要监控。
- Datasheets for Datasets / Data Cards：数据集应记录动机、组成、收集方式、处理、推荐用途、限制和维护计划。
- Hidden Technical Debt in ML Systems：ML 系统的债务常来自数据依赖、隐式消费者、配置、反馈环和无人维护的数据路径。
- NIST AI RMF / Generative AI Profile：AI 风险管理要覆盖设计、开发、部署、运营和评估；生成式 AI 需要关注数据隐私、内容来源、预部署测试和持续管理。

## 范围

适用对象：

- Prompt eval、agent eval、RAG eval、structured output eval、safety eval、red-team set、canary set、golden set。
- 用户反馈沉淀的 eval case、人工标注样本、模型生成的合成样本、微调/蒸馏候选数据。
- 影响 release gate、模型选择、prompt 变更、工具调用策略、AI disclosure、用户承诺或安全边界的数据。
- Go/Kratos/sqlc/gRPC 后端中保存 dataset metadata、eval result、label review、quality run 的数据结构。
- Vite 前端中用于样本审阅、标注、人工复核、数据刷新和质量看板的页面。

不适用对象：

- 通用业务日志、完整生产数据仓库、BI 指标体系；这些由 W7 观测性、W2 隐私安全、W8 支持反馈和 W2 信任政策覆盖。
- 未连接到产品发布、模型优化或 AI 能力验证的一次性本地实验。
- 法务级数据授权、研究伦理审查、监管备案或商业数据采购合同；这些需要单独专业审阅。

## 最小工件

每个 AI capability 或 dataset 使用同一个 `<dataset>` 文件名：

```text
ai-data/
  dataset-card/<dataset>.md
  eval-set/<dataset>.jsonl
  labeling-guide/<dataset>.md
  quality-report/<dataset>.json
  refresh-review/<dataset>.md
```

### `ai-data/dataset-card/<dataset>.md`

Dataset card 必须包含：

- `Scope`
- `Purpose`
- `Source And Provenance`
- `Consent / License`
- `Composition`
- `Splits`
- `Privacy / Redaction`
- `Intended Use`
- `Prohibited Use`
- `Known Gaps`
- `Maintenance`
- `Linked Artifacts`

默认：

- 每个数据来源都要说明是 synthetic、公开数据、用户反馈、人工构造、生产样本摘要、第三方数据还是供应商数据。
- 真实用户数据默认不进仓库；需要用时保存 redacted example、source id、hash、case id 或最小片段。
- 公开数据不等于可商用、可训练、可再分发；必须记录 license、terms、retrieval date 和用途限制。
- Dataset card 是 release reviewer 的入口，不是论文；一屏内要能看出用途、风险、缺口和维护节奏。

### `ai-data/eval-set/<dataset>.jsonl`

Eval set 每行是一个 JSON object，至少包含：

- `id`
- `capability`
- `input_ref` 或 `input`
- `expected_behavior`
- `rubric_ref`
- `tags`
- `source`
- `split`
- `risk_category`
- `privacy_class`
- `consent_or_license`
- `created_at`
- `reviewed_by`
- `status`
- `linked_artifact`

默认 `split`：

- `dev`
- `eval`
- `canary`
- `red_team`
- `train`
- `validation`
- `archive`

默认 `status`：

- `draft`
- `ready`
- `blocked`
- `retired`
- `needs-human`

默认：

- release gate 只使用 `ready` 且属于 `eval`、`canary` 或 `red_team` 的样本。
- `train` / `validation` 数据不得和发布评测集混用；如果 eval case 被移动到训练或微调候选，必须记录版本、原因和人工 checkpoint。
- 合成样本必须显式标为 synthetic；高风险能力不得只靠合成样本证明。
- Eval set 不保存完整 raw prompt、raw response、长对话、secret、支付数据或不必要个人信息。
- 样本 id 稳定，不随文案微调改变；内容变化时用版本或 linked artifact 记录。

### `ai-data/labeling-guide/<dataset>.md`

Labeling guide 必须包含：

- `Scope`
- `Labels`
- `Rubric`
- `Positive Examples`
- `Negative Examples`
- `Edge Cases`
- `Disagreement`
- `Reviewer Calibration`
- `Human Checkpoints`

默认：

- 任何作为 release gate 的标签、评分器或 grader，必须先有可读 rubric。
- 模型可以辅助初标，但不得把模型输出直接当 ground truth；至少要有人工 spot check 或校准样本。
- 标注分歧不是噪音；分歧集中处通常是产品定义、用户承诺或 prompt 边界不清。
- Rubric 变更会影响历史结果，必须连接 quality report 和 refresh review。

### `ai-data/quality-report/<dataset>.json`

Quality report 必须包含：

- `dataset`
- `owner`
- `version`
- `counts`
- `splits`
- `coverage`
- `privacy_checks`
- `license_checks`
- `duplicate_checks`
- `leakage_checks`
- `label_quality`
- `known_gaps`
- `baseline_results`
- `release_gate`
- `human_checkpoint`
- `status`

默认：

- `coverage` 记录覆盖了哪些 product capability、risk category、language、tenant mode、happy path、edge case 和 failure mode。
- `privacy_checks` 记录 redaction、PII、sensitive data、minor data、retention 和 access boundary。
- `license_checks` 记录 license、consent、terms、redistribution、commercial use、training/fine-tuning allowance。
- `duplicate_checks` 防止样本重复导致指标虚高。
- `leakage_checks` 防止 train/eval 互相污染，防止 benchmark answer 或生产输出泄漏到 prompt。
- `baseline_results` 保存发布前基线，不要求大平台，但至少要有版本、运行时间、主要指标和失败摘要。

### `ai-data/refresh-review/<dataset>.md`

Refresh review 必须包含：

- `Recent Changes`
- `Production Signals`
- `User Feedback`
- `Added / Removed Examples`
- `Drift / Coverage`
- `Eval / Train Separation`
- `Open Risks`
- `Next One Change`

默认节奏：

- pre-revenue：每月一次，或任何 AI capability / prompt / model / tool / policy release 前。
- 有付费用户：每两周一次，或每次影响 AI 输出的 release 前。
- 高风险领域、真实用户数据、供应商条款变化、重大投诉、指标漂移或安全事件：立即刷新 review。
- 每次复盘只选一个最高影响改进，避免把数据治理变成 backlog 黑洞。

## Go / Kratos / sqlc / gRPC 默认规则

- 数据集内容和用户原文优先存对象存储或受控数据仓，不默认进应用库；Go/Kratos 服务保存 metadata、version、hash、status 和 artifact reference。
- sqlc 表默认包含：`ai_datasets`、`ai_dataset_versions`、`ai_eval_examples`、`ai_label_reviews`、`ai_data_quality_runs`。
- gRPC API 默认只暴露 dataset metadata、review status、release gate result 和 redacted example，不跨租户返回原始样本。
- Dataset version、eval run id、prompt version、model id、tool schema version 和 release id 必须可关联。
- 删除、retire、移动 eval case 到训练/微调候选集属于高风险数据动作，走 W7 后台运营动作审计。
- Go 服务不得把 production prompt、用户 raw input、供应商 key、PII 或支付数据写入 eval artifact。

## Vite 前端默认规则

- 标注和审阅 UI 使用紧凑、可扫描的工作台形态：source、privacy、split、status、rubric、风险标签和 linked artifact 必须同屏可见。
- 真实用户数据默认显示 redacted preview；查看原文需要明确权限、审计和理由。
- 标注控件使用明确 label、segmented controls、checkbox、select、diff 和状态徽标；不要用营销式卡片解释流程。
- 使用 Vercel/Geist 风格时保持清晰层级、足够对比度、可键盘操作和暗色模式可读性。
- 前端不得让 reviewer 在不知道来源、许可、隐私分类和 split 的情况下把样本标为 `ready`。

## AI workflow 默认规则

- Prompt、grader、agent policy、tool schema、model routing 或 safety rule 变更时，必须说明使用哪个 dataset version 验证。
- 模型生成的 synthetic cases、labels 或 judge scores 必须标注生成方式，并用人工校准或小样本人工复核约束。
- Red-team set 和 canary set 与普通 eval set 分开统计；安全失败不能被平均分掩盖。
- Eval threshold 变更、rubric 变更、删除失败样本、把 eval case 用于训练，都必须人工 checkpoint。
- 高风险 AI 能力必须保留失败样本和 known gaps；不能为了让 release gate 通过而静默删样本。

## 需要人判断的关键点

只把这些判断交给人：

- 是否使用真实用户数据、raw prompt、raw response、敏感数据、未成年人数据或高影响领域数据。
- 是否接受许可、同意、来源、公开数据 terms 或第三方数据用途不清的样本。
- 是否把 eval case 移入训练、微调、蒸馏或 prompt examples。
- 是否对外共享、发布、导出或采购数据集。
- 是否用纯合成样本支撑高风险 release。
- 是否改变 labeling rubric、grader 口径、benchmark threshold 或 release gate 指标。
- 是否删除、retire 或降权当前失败的 eval case。
- 是否把有争议的标注结果标为 ready。

其他字段完整性、章节、JSONL 格式、状态枚举、敏感内容扫描、重复 id、必需 checkpoint 和 OpenSpec linkage 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“数据是什么、样本长什么样、怎么标、质量如何、多久刷新”。
- 保留：人只判断真实/敏感/高影响数据、许可同意、eval/train 边界、阈值口径和删除失败样本。
- 调整：不要求 MLOps 平台、数据 catalog、复杂标注队列；先用 repo artifacts 和最小 JSON/JSONL。
- 调整：不要求所有样本人工双标；只有 release gate 标签、分歧样本和高风险样本需要人工校准。
- 风险：容易把 eval set 当训练素材。缓解：`split`、`leakage_checks`、`human_checkpoint.required_for` 和 verifier 一起约束。

结论：可落地。一个人可以先为最重要 AI capability 建 20 到 50 条高质量 eval case，记录来源与口径，再逐步补充 red-team 和 canary。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：数据缺口直接暴露产品未知风险，refresh review 把用户反馈和 eval 改进连接起来。
- 工程角度：dataset version、eval run、prompt version、model id、release id 可关联，便于复现和回滚。
- 运维角度：数据新鲜度、静默失败、coverage drift 和 canary/red-team 失败进入发布前检查。
- 安全隐私角度：来源、许可、同意、隐私分类、redaction、train/eval leakage 和原文访问都有边界。
- 成本角度：小而准的数据集优先，避免一开始采购、清洗、标注和跑大规模 eval 的成本黑洞。

结论：可落地。本专项把 AI 质量从“感觉变好了”压到“这个版本、这些样本、这个口径、这次复盘”，同时不把一人公司拖进重型数据平台。
