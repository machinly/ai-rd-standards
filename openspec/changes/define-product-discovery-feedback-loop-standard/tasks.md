# 任务

## 1. 来源与约束

- [x] 1.1 查证 Lean Startup、Steve Blank Customer Development。
- [x] 1.2 查证 The Mom Test、Continuous Discovery / Opportunity Solution Tree。
- [x] 1.3 查证 Shape Up、Google HEART/GSM、在线受控实验资料。
- [x] 1.4 查证 OpenTelemetry events 和产品分析事件命名资料。
- [x] 1.5 补充阶段 11 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 产品发现规范

- [x] 2.1 编写阶段 11 规范正文。
- [x] 2.2 定义 `product/bets`、`product/metrics`、`product/feedback`、`product/experiments`、`product/decisions` artifacts。
- [x] 2.3 定义产品指标、事件、反馈、实验、AI 产品学习和人工 checkpoint 规则。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 11 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `product-discovery-learning-loop` skill。
- [x] 4.2 添加 product discovery artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 product discovery 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实产品 bet，因此不运行真实产品分析平台或 A/B 平台。

验证说明：本仓库是规范仓库，不包含真实产品能力 artifacts，也不应在规范阶段连接真实 analytics 或实验平台。已通过 `verify_product_discovery.py` 的临时 `ai-assistant` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `product/bets`。
