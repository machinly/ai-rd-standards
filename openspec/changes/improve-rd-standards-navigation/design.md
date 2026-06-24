# 设计：研发规范导航层

## 决策

根入口采用 workflow-first 三层结构：

1. `README.md`：只保留第一跳、默认技术偏好和少数高影响人工判断。
2. `docs/00-start-here.md`：定义 W0-W9 AI 研发工作流。
3. `docs/00-standard-index.md`：把每份规范挂到 workflow step，作为 reference 而非阅读顺序。

## Workflow

- W0 Intake：决定是否做。
- W1 Discovery：确认问题、证据和指标。
- W2 OpenSpec / Risk：定义行为、边界和风险。
- W3 AI Behavior：定义 prompt、eval、模型、工具、RAG 和安全样本。
- W4 Build：落到 Go/Kratos/sqlc/gRPC、Vite、数据、配置和任务。
- W5 Verify：测试、eval、安全、性能、韧性和 UX 门禁。
- W6 Release：发布、客户上线、回滚和对外承诺。
- W7 Operate：SLO、观测、事故、恢复和凭据。
- W8 Learn：反馈、指标、质量回归和下一轮决策。
- W9 Maintain：知识恢复、依赖、证据和长期维护。

## 知识恢复

`knowledge/docs-map/rd-standards.json` 记录 canonical entrypoints、Diataxis 覆盖、OpenSpec links、freshness policy 和人工 checkpoint。

`knowledge/context-packs/rd-standards.md` 给 Codex 接手时使用，要求先判断 W0-W9，再读对应规范。

## 自动校验

`tools/verify_workflow_index.py` 检查：

- README 仍然是短入口，且链接 workflow entrypoint、workflow index 和 context pack。
- `docs/00-start-here.md` 包含 W0-W9。
- `docs/00-standard-index.md` 包含 W0-W9 详细段落和新增规范准入规则。
- 每个 `docs/Wx-*/NN-*` 规范文件都恰好映射到一个 workflow step。
- 每个编号规范的物理目录必须和主归属 step 一致。
- 索引里的路径真实存在。

## 取舍

- 选择 Markdown 和 JSON，而不是生成站点，保持一人公司维护成本低。
- 完整清单仍保留，但按照 workflow step 归属展示，编号规范也按 W0-W9 目录存放，避免“想到一个主题就加一个入口”。
- 本变更不新增编号阶段，避免把“索引修复”伪装成又一个领域规范。

## 风险

- 新增阶段后忘记更新索引。缓解：workflow index verifier、freshness log 和 knowledge verifier。
- 索引仍然过长。缓解：README 只指向 workflow entrypoint，完整索引只作 reference。
