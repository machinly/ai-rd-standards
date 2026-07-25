# Proposal: define maintenance, dependency, debt, and deprecation standard

## 意图

建立一人公司维护治理规范，覆盖依赖清单、更新策略、重大升级计划、技术债登记和弃用计划，让 Go/Kratos/sqlc/gRPC、Vite、AI workflow 和 CI/tooling 的长期维护有可验证入口。

## 范围

- 新增 `maintenance-dependency-debt-standard` spec。
- 新增 W9 维护债务触发专项文档。
- 创建 `maintenance-dependency-debt-guard` skill 和 verifier。
- 补充来源索引与 README。

## 不做什么

- 不要求每周追新或自动合并依赖更新。
- 不把所有 TODO 都升级为流程。
- 不替代 W6 release、W2 security、W5 testing、W2 architecture 或 W9 knowledge artifacts。
- 不连接真实 GitHub/Dependabot 或外部 issue tracker。

## 依据

- Software Engineering at Google: Dependency Management、Deprecation、Static Analysis。
- Martin Fowler: Technical Debt、Technical Debt Quadrant、Refactoring。
- Working Effectively with Legacy Code。
- Hidden Technical Debt in Machine Learning Systems。
- Go modules / govulncheck、GitHub Dependabot、npm package-lock / npm ci / npm audit、Vite migration guide。

## 需要人的判断

只有这些需要人工 checkpoint：runtime/framework/provider major upgrade、真实可达漏洞例外、replace/fork/long pin、breaking API/schema/prompt/eval contract、弃用删除、长期延期技术债。
