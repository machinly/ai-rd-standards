# 任务

## 1. 来源与约束

- [x] 1.1 查证 Google SRE Release Engineering、Canarying Releases。
- [x] 1.2 查证 Twelve-Factor build/release/run、DORA delivery metrics。
- [x] 1.3 查证 GitHub Actions workflow/security/OIDC/artifact attestations、Docker multi-stage/SBOM/provenance、Go/sqlc/Vite/Vercel 官方文档。
- [x] 1.4 补充阶段 6 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 发布流水线规范

- [x] 2.1 编写阶段 6 规范正文。
- [x] 2.2 定义 `release/` artifact 目录、pipeline JSON、smoke、rollback、release log。
- [x] 2.3 定义后端、前端、AI、SRE-lite、secrets、供应链、rollback gates。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 6 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `release-pipeline-gates` skill。
- [x] 4.2 添加 release pipeline artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 release pipeline 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实生产 release pipeline，因此不运行真实部署。

验证说明：本仓库是规范仓库，不包含真实生产 release pipeline，也不应在规范阶段触发真实部署。已通过 `verify_release_pipeline.py` 的临时 `checkout-api` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `release/pipelines`。
