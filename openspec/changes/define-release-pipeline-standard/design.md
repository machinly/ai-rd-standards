# 设计：生产部署与发布流水线规范

## 设计决策

### 1. 机器可检查的 pipeline JSON

发布流程容易退化为口头记忆。`release/pipelines/<service>.json` 用结构化字段记录 trigger、CI、build、gates、deploy、smoke、rollback、post-deploy watch，使 skill 和脚本能检查最低要求。

### 2. 复用 SRE-lite artifacts

阶段 5 已有 `ops/slo`、`ops/release`、runbook 和 incident 工件。阶段 6 不再复制运维内容，只把 release pipeline 连接到这些文件。

### 3. CI 构建 artifact，本地只触发

生产 artifact 默认由 CI 构建，避免本地环境漂移、隐藏依赖和不可追溯产物。release log 必须记录 commit、artifact digest 或 deployment URL。

### 4. Production checkpoint 按风险升级

一人公司不能让所有发布都变成人工仪式，也不能让高风险变化静默上线。默认 preview/staging 自动，production 首次和高风险人工确认，普通低风险小改动可逐步自动化。

### 5. Secrets 用最小权限和短期凭证

GitHub Actions 默认读权限；部署 job 才提升必要权限。云资源优先 OIDC，长期 secret 作为无法使用 OIDC 时的例外。

### 6. Provenance/SBOM 渐进采用

私有早期服务不强制完整供应链合规；当发布二进制、包或镜像给外部用户运行时，启用 artifact attestation、image digest 和 SBOM。

## 取舍

- JSON 比 Markdown 生硬，但可验证。
- 不强制所有项目用 GitHub Actions，避免锁定平台；但默认 GitHub Actions 能给一人公司最快落地。
- 不要求全量 canary；低流量早期产品用 smoke test 和外部 uptime 代替。
- 不强制 SBOM/provenance 到第一天，避免把安全合规平台化。
