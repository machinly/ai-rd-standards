# 任务

## 1. 来源与约束

- [x] 1.1 查证 Practical Test Pyramid、Google Testing Overview / Test Sizes / Larger Testing。
- [x] 1.2 查证 xUnit Test Patterns。
- [x] 1.3 查证 Go testing、fuzzing、race detector。
- [x] 1.4 查证 sqlc vet / verify、Vitest、Playwright、OpenAI evals。
- [x] 1.5 补充阶段 12 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 测试质量规范

- [x] 2.1 编写阶段 12 规范正文。
- [x] 2.2 定义 `quality/test-strategy`、`quality/test-matrix`、`quality/test-runs`、`quality/flaky-tests` artifacts。
- [x] 2.3 定义 Go/Kratos/sqlc/gRPC、Vite、Playwright、AI eval、flaky、coverage 和人工 checkpoint 规则。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 12 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `quality-test-strategy-guard` skill。
- [x] 4.2 添加 quality testing artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 quality testing 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实服务测试 artifacts，因此不运行真实项目 test suite。

验证说明：本仓库是规范仓库，不包含真实 Go/Vite/AI 服务测试 artifacts，也不应在规范阶段连接真实测试、浏览器、数据库或供应商环境。已通过 `verify_quality_testing.py` 的临时 `ai-assistant` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `quality/test-matrix`。
