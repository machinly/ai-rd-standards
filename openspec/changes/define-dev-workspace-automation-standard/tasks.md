# 任务

## 1. 来源与约束

- [x] 1.1 查证 Joel Test、Software Engineering at Google Build Systems / CI。
- [x] 1.2 查证 Twelve-Factor Dependencies / Dev-Prod Parity / Admin Processes。
- [x] 1.3 查证 Dev Containers、Docker Compose、Go Toolchains/Workspaces、sqlc、Vite CLI。
- [x] 1.4 补充阶段 19 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 开发工作区规范

- [x] 2.1 编写阶段 19 规范正文。
- [x] 2.2 定义 workspace map、command catalog、local environment、seed fixtures、verification artifacts。
- [x] 2.3 定义 Go/Kratos/sqlc/gRPC、Vite、AI workflow 默认规则和人审点。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 19 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `dev-workspace-automation-guard` skill。
- [x] 4.2 添加 dev workspace artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证开发工作区检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实 target dev-workspace artifacts，因此不启动本地服务或连接真实供应商。

验证说明：本仓库是研发规范仓库，不包含真实产品 target 的 `dev-workspace` artifacts，也不应在规范阶段启动本地服务、连接真实供应商或访问真实数据。已通过 `verify_dev_workspace.py` 的临时 `assistant-app` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `dev-workspace/workspace-map`。
