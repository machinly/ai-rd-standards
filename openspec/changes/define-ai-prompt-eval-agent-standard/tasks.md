# 任务

## 1. 来源与约束

- [x] 1.1 查证 OpenAI Prompting、Evaluation、Agents、Tools、Structured Outputs、Safety、Production best practices。
- [x] 1.2 查证 Anthropic agents、Google Rules of ML、Google SRE monitoring。
- [x] 1.3 补充阶段 4 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. AI 研发规范

- [x] 2.1 编写阶段 4 规范正文。
- [x] 2.2 定义 artifact 目录、prompt、eval、schema、workflow/agent、tool safety、最小运维要求。
- [x] 2.3 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 4 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `ai-prompt-eval-loop` skill。
- [x] 4.2 添加 AI artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 AI artifacts 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不适用的真实 AI eval/API 门禁。

验证说明：本仓库是规范仓库，不包含真实 AI capability artifacts，也不应在规范阶段调用 OpenAI API 或运行真实 eval。已通过 `verify_ai_artifacts.py` 的临时 AI artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失项。
