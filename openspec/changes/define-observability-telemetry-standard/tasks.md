# 任务

## 1. 来源与约束

- [x] 1.1 查证 Google SRE Monitoring / Workbook Monitoring。
- [x] 1.2 查证 OpenTelemetry signals、Go、JavaScript、logs、semantic conventions。
- [x] 1.3 查证 W3C Trace Context、Prometheus naming。
- [x] 1.4 查证 OpenAI Agents tracing / observability。
- [x] 1.5 补充阶段 15 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 观测性规范

- [x] 2.1 编写阶段 15 规范正文。
- [x] 2.2 定义 instrumentation、telemetry schema、dashboard、trace correlation、AI telemetry artifacts。
- [x] 2.3 定义 Go/Kratos/gRPC/sqlc、Vite、AI workflow 默认遥测规则。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 15 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `observability-telemetry-guard` skill。
- [x] 4.2 添加 observability artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 observability 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实服务 observability artifacts，因此不连接真实 telemetry backend。

验证说明：本仓库是规范仓库，不包含真实生产服务 observability artifacts，也不应在规范阶段连接真实 telemetry backend。已通过 `verify_observability.py` 的临时 `ai-assistant` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `observability/instrumentation`。
