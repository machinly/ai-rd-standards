# 任务

## 1. 来源与约束

- [x] 1.1 查证 Google SRE SLO、监控、告警、值班、事故响应、复盘、发布、toil。
- [x] 1.2 查证 DORA 软件交付指标和 OpenTelemetry observability / Go 文档。
- [x] 1.3 补充 W7 SRE-lite 专项来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. SRE-lite 运维规范

- [x] 2.1 编写 W7 SRE-lite 触发专项正文。
- [x] 2.2 定义 `ops/` artifact 目录、SLO JSON、runbook、release checklist、incident 模板。
- [x] 2.3 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建 W7 SRE-lite change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `sre-lite-ops` skill。
- [x] 4.2 添加 SRE-lite artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 SRE-lite 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实生产服务，因此不运行真实告警、发布或事故演练。

验证说明：本仓库是规范仓库，不包含真实生产服务，也不应在规范阶段配置真实告警、发布或事故演练。已通过 `verify_sre_lite.py` 的临时 `checkout-api` 运维 artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `ops/slo`。
