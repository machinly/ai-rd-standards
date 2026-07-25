# 任务

## 1. 来源与约束

- [x] 1.1 查证 Twelve-Factor App Admin Processes。
- [x] 1.2 查证 Google SRE Automation / Eliminating Toil、Emergency Response、Reliable Product Launches。
- [x] 1.3 查证 OWASP Authorization、Logging、Top 10 A09。
- [x] 1.4 查证 NIST SP 800-53 Rev. 5、OpenAI Agent Builder Safety、Google SRE AI Engineering Reliable Operations。
- [x] 1.5 补充 W7 后台运营专项来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 后台运营动作规范

- [x] 2.1 编写 W7 后台运营触发专项正文。
- [x] 2.2 定义 action registry、operator playbook、audit log schema、break-glass、ops review artifacts。
- [x] 2.3 定义 Go/Kratos/sqlc/gRPC、Vite、AI workflow 默认规则和人审点。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建 W7 后台运营 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `admin-ops-action-guard` skill。
- [x] 4.2 添加 admin ops artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 admin ops 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实 target 的 `admin-ops` artifacts，因此不连接真实生产数据库、云账号、后台系统或用户数据。

验证说明：本仓库是研发规范仓库，不包含真实产品 target 的 `admin-ops` artifacts，也不应在规范阶段连接真实生产数据库、云账号、后台系统、客服系统、支付系统或用户数据。已通过 `verify_admin_ops.py` 的临时 `assistant-app` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `admin-ops/action-registry`。
