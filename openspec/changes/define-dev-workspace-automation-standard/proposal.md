# Proposal: define development workspace automation standard

## 意图

建立一人公司开发环境、命令自动化与本地可复现规范，覆盖工作区地图、命令目录、本地环境、seed/fixtures 和本地验证计划，让 Go/Kratos/sqlc/gRPC、Vite 和 AI workflow 有一条可复制的黄金路径。

## 范围

- 新增 `dev-workspace-automation-standard` spec。
- 新增阶段 19 规范文档。
- 创建 `dev-workspace-automation-guard` skill 和 verifier。
- 补充来源索引与 README。

## 不做什么

- 不强制使用 devcontainer、Docker Compose、Makefile、Taskfile 或特定 IDE。
- 不替代阶段 6 CI/release、阶段 12 test strategy、阶段 16 context recovery。
- 不连接真实供应商、本地真实 secret 或生产数据。
- 不要求本地验证等同完整 CI。

## 依据

- The Joel Test。
- Software Engineering at Google: Build Systems and Build Philosophy、Continuous Integration。
- Twelve-Factor App: Dependencies、Dev-Prod Parity、Admin Processes。
- Development Containers Specification。
- Docker Compose official docs。
- Go Toolchains / Workspaces。
- sqlc generate/vet。
- Vite CLI。

## 需要人的判断

只有这些需要人工 checkpoint：本地命令是否可调用真实供应商/真实模型/真实生产数据，是否接受环境差异，是否暴露破坏性 reset/migration/backfill/tool commit，一人公司是否引入长期工具链/devcontainer/compose stack/付费开发工具，AI agent 是否可运行有副作用命令。
