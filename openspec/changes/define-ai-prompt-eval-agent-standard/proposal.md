# 提案：定义 AI prompt / eval / agent workflow 研发规范

## 意图

为一人公司建立默认 AI 能力研发路径，让 prompt、eval、schema、tool、trace 和安全边界进入代码库，并能在模型、prompt 或 agent workflow 变化时做回归验证。

## 范围

- 定义 AI artifacts 目录和最小文件。
- 定义 prompt/eval/schema/tool 的实现顺序。
- 定义单次调用、workflow、agent 的升级判断。
- 定义结构化输出、工具权限、不可信输入和人工复核边界。
- 创建 AI prompt/eval 落地 skill 和检查脚本。

## 不做

- 不实现真实 AI 产品代码。
- 不定义完整 RAG、向量库、finetuning 或多 agent 平台。
- 不绑定旧 OpenAI Evals platform。
- 不展开 Go/Kratos AI adapter 代码模板。

## 依据

- 《人月神话》：不要把模型或 agent 框架当银弹。
- 小型项目管理：只保留能避免返工和质量漂移的工件。
- OpenAI Prompting、Evaluation、Structured Outputs、Tools、Agents、Safety、Production best practices。
- Anthropic Building Effective Agents：优先简单 prompts/workflows，复杂 agent 需要可度量收益。
- Google Rules of ML：第一版先做可信 pipeline 和 good/bad 定义。
- Google SRE：上线后看 latency、traffic、errors、saturation 和质量信号。

## 需要人的判断

建议默认要求：所有用户可见 AI 能力必须先有本地 eval fixtures，至少 3 条样例，才能改 prompt/model/tool。内部一次性实验可在 OpenSpec 中说明豁免。

