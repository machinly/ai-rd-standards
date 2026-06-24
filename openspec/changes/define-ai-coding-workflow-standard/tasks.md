# 任务

## 1. 来源与约束

- [x] 1.1 查证 OpenSpec、Google Code Review / Engineering Practices。
- [x] 1.2 查证 DORA small batches / trunk-based development。
- [x] 1.3 查证 OpenAI Codex best practices、AGENTS.md、sandbox / approvals、skills。
- [x] 1.4 查证 GitHub Copilot CLI best practices 与 AI-generated code review。
- [x] 1.5 补充阶段 20 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. AI coding workflow 规范

- [x] 2.1 编写阶段 20 规范正文。
- [x] 2.2 定义 implementation brief、batch log、review、verification artifacts。
- [x] 2.3 定义 Go/Kratos/sqlc/gRPC、Vite、AI workflow 默认规则和人审点。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 20 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `ai-coding-workflow-guard` skill。
- [x] 4.2 添加 AI coding workflow artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 AI coding workflow 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实 target 的 `ai-coding` artifacts，因此不运行真实产品代码或连接真实供应商。

验证说明：本仓库是研发规范仓库，不包含真实产品 target 的 `ai-coding` artifacts，也不应在规范阶段运行真实产品代码、连接真实供应商、访问真实数据或执行生产发布。已通过 `verify_ai_coding_workflow.py` 的临时 `add-assistant-reply-rpc` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `ai-coding/implementation-brief`。
