# 任务

## 1. 来源与约束

- [x] 1.1 查证 Software Engineering at Google 的 dependency management、deprecation、static analysis。
- [x] 1.2 查证 Go modules / govulncheck、GitHub Dependabot、npm lockfile/audit/ci、Vite migration。
- [x] 1.3 查证 Fowler technical debt/refactoring、Working Effectively with Legacy Code、Hidden Technical Debt in ML Systems。
- [x] 1.4 补充 W9 维护债务专项来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 维护治理规范

- [x] 2.1 编写 W9 维护债务触发专项正文。
- [x] 2.2 定义 dependency inventory、update policy、upgrade plan、debt register、deprecation plan。
- [x] 2.3 定义 Go/Vite/AI/Dependabot 默认规则和人审点。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建 W9 维护债务 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `maintenance-dependency-debt-guard` skill。
- [x] 4.2 添加维护治理 artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证维护治理检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实 target maintenance artifacts，因此不连接 Dependabot/GitHub。

验证说明：本仓库是规范仓库，不包含真实产品 target 的 maintenance artifacts，也不应在规范阶段连接 GitHub/Dependabot。已通过 `verify_maintenance_debt.py` 的临时 `ai-platform` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `maintenance/dependency-inventory`。
