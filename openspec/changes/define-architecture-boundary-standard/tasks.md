# 任务

## 1. 来源与约束

- [x] 1.1 查证 Parnas 模块化、ADR、C4、bounded context、ports/adapters。
- [x] 1.2 查证 Go module layout、Go internal packages、Kratos layout。
- [x] 1.3 查证 Vite / React file structure、OpenAI prompt / Agents、Google SRE simplicity。
- [x] 1.4 补充阶段 13 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 架构边界规范

- [x] 2.1 编写阶段 13 规范正文。
- [x] 2.2 定义 ADR、boundary JSON、module map、dependency rules artifacts。
- [x] 2.3 定义 Go/Kratos/sqlc/gRPC、Vite、AI workflow 默认边界和人审点。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 13 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `architecture-boundary-guard` skill。
- [x] 4.2 添加 architecture boundary artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 architecture boundary 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实服务 architecture artifacts，因此不扫描真实业务代码。

验证说明：本仓库是规范仓库，不包含真实生产服务架构边界 artifacts，也不应在规范阶段重排真实业务代码。已通过 `verify_architecture_boundaries.py` 的临时 `ai-assistant` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `architecture/boundaries`。
