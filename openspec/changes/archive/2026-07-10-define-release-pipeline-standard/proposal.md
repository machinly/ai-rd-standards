# 提案：定义生产部署与发布流水线规范

## 意图

把一人公司的研发规范串成可重复执行的 release path：OpenSpec change 通过 CI gates，产出不可变 artifact，部署到 preview/staging/production，执行 smoke test，观察 SLO，并在失败时可回滚。

## 范围

- 定义 release pipeline 的最小仓库 artifacts。
- 定义 Go/Kratos/sqlc/gRPC、Vite、AI eval、SRE-lite 的发布门禁。
- 定义 build / release / run 分离、release id、artifact digest 和 release log。
- 定义 secrets、OIDC、provenance/SBOM 的默认策略。
- 定义 smoke test、post-deploy watch 和 rollback 要求。
- 创建发布流水线落地 skill 和检查脚本。

## 不做

- 不实现真实云厂商部署。
- 不定义 Kubernetes / Terraform / GitOps 平台。
- 不默认复杂多环境审批矩阵。
- 不把 production 自动发布作为所有项目的默认。

## 依据

- 《人月神话》：发布自动化不是银弹，必须把复杂度显性化并保持概念完整。
- 小型项目管理：只保留减少返工和事故损失的最小门禁。
- Twelve-Factor App：严格分离 build、release、run，release 是 append-only ledger。
- Google SRE Release Engineering / Canarying Releases：发布应可重复、自动化、自助、可回滚，高风险变更小批量放量。
- DORA：用交付吞吐和不稳定性观察流水线，优先小批量变化。
- GitHub Actions / OIDC / Artifact Attestations、Docker、Go、sqlc、Vite、Vercel 官方文档。

## 需要人的判断

建议默认：生产 artifact 由 CI 构建，首次和高风险 release 需要人工 checkpoint；普通小改动可自动到 preview/staging，但 production 不默认静默自动发布。
