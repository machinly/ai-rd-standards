# 发布：AI release gate

## 执行细则

<!-- rule-id: RELEASE-AI-001 -->
### 固定 AI 产物、版本与 eval 证据

用户可见 AI 能力发布前，`ai/prompts/<capability>/` 下必须存在 `prompt.md`、`cases.jsonl`、`rubric.md` 与 `runbook.md`。release gate 只接受状态为 `ready` 的样本；相关 eval 必须通过，或留下明确的失败接受理由。高风险输入必须实际运行 fuzz 或对抗样例中的至少一种，并在 release run 中记录命令或样例引用及结果；未运行或失败时只能作为未通过 gate 处理，并留下明确的 accepted risk、决定人与后续动作。model、prompt version 与 schema version 写入配置或 release log，prompt/schema 版本也必须进入可追溯 artifact 或配置。

<!-- rule-id: RELEASE-AI-002 -->
### 不用平均分掩盖安全失败

critical 安全失败默认阻断发布；high 失败默认同样阻断，除非有明确 accepted risk。任何带未缓解 high/critical finding 的上线，或 `ship-with-risk-acceptance` 结论，都必须由人确认并记录风险承接，不能被总体均分抵消。

<!-- rule-id: RELEASE-AI-003 -->
### 检查 AI 工具与降级路径

工具型 AI 发布前检查 tool 权限；结构化输出检查 parse failure；所有用户可见 AI 都要验证 fallback 或 disable switch。能力涉及金钱、权限、通知、删除、隐私或高风险建议时，production checkpoint 必须由人完成。
