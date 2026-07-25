# 提案：建立一人公司 AI 研发操作系统

## 意图

建立一人公司最小研发流程层：保留意图、降低人工注意力消耗，并让 AI 辅助研发在跨会话后仍然可恢复。

## 范围

- 定义默认工作单元为 OpenSpec change。
- 定义哪些决策必须交给人判断。
- 定义每个规范段落完成后的两轮 review。
- 定义用户可见 AI 行为的第一条规则：先 eval，再改 prompt 或模型。
- 安装一个 Codex skill，让后续回合能复用这套流程。

## 不做

- 不定义完整 Go/Kratos/sqlc/gRPC 实现模板。
- 不创建前端项目脚手架。
- 不定义完整 SRE 政策。
- 不展开安全、隐私和事故响应细则，只保留第一层关口。

## 依据

- OpenSpec：规格和变更 artifact 进入仓库，而不是留在聊天记录。
- 《人月神话》：警惕进度幻觉和银弹幻觉。
- 小型项目管理：把流程裁剪到能避免返工和遗漏的最小形态。
- Anthropic：优先简单 workflow，开放任务才升级为 agent。
- OpenAI：生产 prompt 进入代码，prompt 变化需要测试/eval。
- Google SRE：后续可靠性投入应由 SLO 和 error budget 驱动。

