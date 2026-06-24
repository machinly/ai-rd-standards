# 任务

## 1. 来源与约束

- [x] 1.1 查证 FinOps Framework、Planning & Estimating、Unit Economics。
- [x] 1.2 查证 Google SRE overload、cascading failures、capacity/design 相关内容。
- [x] 1.3 查证 OpenAI rate limits、production billing limits、cost optimization、prompt caching 官方文档。
- [x] 1.4 查证 OWASP API4/API10、Twelve-Factor Backing Services、AWS/Google Cloud 成本管理依据。
- [x] 1.5 补充阶段 9 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 成本容量规范

- [x] 2.1 编写阶段 9 规范正文。
- [x] 2.2 定义 `cost/budgets`、`cost/vendors`、`cost/runbooks`、`cost/usage` artifacts。
- [x] 2.3 定义预算阈值、AI token/tool/request 限制、overload 降级、供应商退出规则。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 9 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `cost-capacity-guard` skill。
- [x] 4.2 添加 cost/capacity/vendor artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 cost capacity 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实生产服务预算，因此不运行真实云账单或供应商 API。

验证说明：本仓库是规范仓库，不包含真实生产服务预算，也不应在规范阶段连接真实云账单或供应商 API。已通过 `verify_cost_capacity.py` 的临时 `ai-assistant` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `cost/budgets`。
