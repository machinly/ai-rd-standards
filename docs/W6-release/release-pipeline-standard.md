# W6 Release 触发专项：生产部署与发布流水线规范 v0.1

## W6 触发定位

本文件是 W6 Release 的触发型专项，不是 W6 主入口。只有当当前工作涉及 CI/CD、release artifact、preview/staging/production deploy、smoke、rollback、post-deploy watch、secrets/OIDC 或 provenance/SBOM 时，才需要读取本文件。

普通 W6 发布入口应先回到 `docs/W6-release/main.md`，由主入口判断是否触发本专项。

## 目标

把前面阶段的研发、AI eval、前端构建和 SRE-lite 运维门禁串成一条一人公司能重复执行的 release path。每个生产服务或用户可见前端都应该从 OpenSpec change 出发，经 CI gates 产出不可变 artifact，再部署到 preview/staging/production，执行 smoke test，观察 SLO，必要时回滚。

本专项的目标不是搭一个复杂平台，而是让“我现在能不能发布”这件事从感觉变成可检查事实。

## 本专项只解决什么

- release pipeline 的最小仓库工件。
- CI gates 的默认顺序和失败处理。
- Go/Kratos/sqlc/gRPC、Vite、AI eval、SRE-lite 的发布门禁整合。
- build / release / run 分离和不可变 release id。
- secrets、OIDC、artifact provenance / SBOM 的一人公司默认策略。
- smoke test、post-deploy watch、rollback 的最小要求。
- 发布流水线 skill 与本地检查脚本。

不在本专项展开：云厂商 Terraform 模块、Kubernetes GitOps 平台、复杂多环境审批矩阵、完整供应链合规、企业级发布列车。这些需要真实产品规模或合规要求时再开独立 OpenSpec change。

## 依据转译

- 《人月神话》：发布流水线不会消除复杂度，只能把复杂度显性化。规范必须防止“有 CI 就安全”的银弹幻觉。
- 小型项目管理：一人公司发布流程只保留能减少返工和事故损失的门禁；失败时要能恢复上下文。
- Twelve-Factor App：严格分离 build、release、run；release 是 append-only ledger，每次 release 有唯一 ID，不能就地修改。
- Google SRE Release Engineering：发布工具应该默认正确、文档充分、自助可用；可靠服务需要可重复、自动化、可回滚的发布过程。
- Google SRE Canarying Releases：测试环境不可能完全等同生产；高风险变化应小批量暴露真实流量，并用信号决定是否继续。
- DORA：交付性能同时看吞吐和不稳定性；小批量变化更容易理解、通过流水线，也更容易从失败中恢复。
- GitHub Actions：workflow 是由 YAML 定义的自动化过程；生产 workflow 应最小化 `GITHUB_TOKEN` 权限。
- GitHub OIDC：CI 访问云资源优先用短期 token，不默认长期云密钥。
- GitHub Artifact Attestations / Docker attestations：需要发布给他人运行的 artifact 应逐步具备 provenance；容器镜像可添加 SBOM/provenance。
- Docker Multi-stage Builds：生产镜像只复制运行需要的 artifact，避免把 SDK、构建工具和中间产物带入运行镜像。
- Go / sqlc / Vite 官方文档：Go 用 `go test` 和必要时 `go test -race`，sqlc 用 `sqlc vet`，Vite 生产构建用 `vite build`。
- Vercel Deployments：前端可通过 Git、CLI、Deploy Hooks 或 API 创建 deployment；Vercel 默认有 Local、Preview、Production 环境。

## 默认决策

- 默认 CI provider 是 GitHub Actions；如果仓库不用 GitHub，`release/pipelines/<service>.json` 必须写明替代 provider 和等价 gates。
- 默认 production deploy 不由本地电脑直接执行；本地可以触发，但 artifact 必须由 CI 构建。
- 默认每次 production release 都有唯一 `release_id`，至少包含 commit SHA 或 image digest。
- 默认 `main` 只表示可发布，不等于已经安全发布到 production；production deploy 需要显式 trigger、tag、environment protection 或平台 preview promote。
- 默认 secrets 不写在 workflow、Dockerfile、build args 或 repo 文件里；云部署优先 OIDC 短期凭证。
- 默认 build artifact 不可变；回滚是部署上一个 release，而不是修改正在运行的 release。
- 默认 first production release 和高风险 release 用人工 checkpoint；普通小改动可以自动部署到 preview/staging。
- 默认一个服务先做最小 release pipeline，不追求 monorepo 大矩阵。

## Release artifact 目录规范

推荐落点：

```text
release/
  pipelines/<service>.json
  smoke/<service>.md
  rollback/<service>.md
  runs/YYYY-MM-DD-<service>-<release-id>.md
```

同时引用 W7 SRE-lite 运维工件：

```text
ops/
  slo/<service>.json
  release/<service>-checklist.md
  runbooks/<service>.md
```

`release/pipelines/<service>.json` 是机器可检查的事实来源，推荐字段：

```json
{
  "service": "checkout-api",
  "owner": "founder",
  "trigger": "tag v* or workflow_dispatch",
  "ci": {
    "provider": "github-actions",
    "workflow": ".github/workflows/release.yml",
    "permissions": "contents:read by default; id-token:write only in deploy jobs"
  },
  "environments": ["preview", "production"],
  "build": {
    "kind": "container",
    "commands": ["go test ./...", "sqlc vet", "docker build --target runtime"],
    "artifact": "container image digest"
  },
  "gates": [
    {"name": "openspec", "required": true, "command": "openspec validate <change-id>"},
    {"name": "backend-tests", "required": true, "command": "go test ./..."},
    {"name": "sqlc-vet", "required": true, "command": "sqlc vet"},
    {"name": "ai-eval", "required": false, "command": "python .../verify_ai_artifacts.py ."},
    {"name": "sre-lite", "required": true, "command": "python .../verify_sre_lite.py . --service checkout-api"},
    {"name": "smoke", "required": true, "command": "release/smoke/checkout-api.md"},
    {"name": "rollback", "required": true, "command": "release/rollback/checkout-api.md"},
    {"name": "observability", "required": true, "command": "watch SLO and dashboard for 30 minutes"}
  ],
  "deploy": {
    "strategy": "manual production promote",
    "canary": "only when enough traffic exists",
    "production_checkpoint": "human"
  },
  "smoke_test": "release/smoke/checkout-api.md",
  "rollback": "release/rollback/checkout-api.md",
  "post_deploy_watch": {
    "duration_minutes": 30,
    "signals": ["latency", "traffic", "errors", "saturation"]
  },
  "provenance": {
    "required": false,
    "policy": "enable artifact attestation/SBOM when publishing binaries or images outside private deployment"
  }
}
```

一人公司裁剪规则：

- 第一版只维护一个 `release/pipelines/<service>.json`，不要抽象平台。
- `gates` 必须包含 `openspec`、`test`、`build`、`smoke`、`rollback`、`observability` 类动作。
- `smoke_test` 和 `rollback` 必须指向可读文件；不能只写“看情况”。
- 生产服务必须能关联 `ops/slo/<service>.json` 和 `ops/release/<service>-checklist.md`。

## 默认流水线

每个 change 从小到大走：

1. OpenSpec：proposal、spec、design、tasks 明确，未完成事项标出来。
2. 静态检查：格式、lint、生成代码一致性、sqlc vet、proto 生成一致性。
3. 单元测试：Go `go test ./...`；前端 Vitest；AI 本地 eval fixtures。
4. 风险测试：并发或关键路径跑 `go test -race`；schema migration 跑 dry-run；高风险输入跑 fuzz 或对抗样例。
5. Build：Go 服务产出容器镜像；Vite 产出 `dist`；AI prompt/schema 版本进入 artifact 或配置。
6. Security：最小 token 权限，依赖扫描或漏洞检查按风险加入；外部发布 artifact 逐步加 provenance/SBOM。
7. Deploy preview/staging：自动或手动。
8. Smoke test：验证关键用户路径、health、gRPC/HTTP endpoint、前端关键页面、AI fallback。
9. Production checkpoint：首次、高风险、migration、资金/权限/隐私/AI 副作用必须人工确认。
10. Production deploy：小批量、canary、blue/green 或平台 promote；没有流量时使用生产 smoke + 外部 uptime。
11. Post-deploy watch：观察 SLO 四黄金信号 15-30 分钟。
12. Release log：记录 release id、commit、artifact digest、gates、结果、回滚方式。

## Backend gates

Go/Kratos/sqlc/gRPC 服务默认 gates：

- `go test ./...`
- `go test -race ./...`：关键并发路径或发布前周期性执行；耗时过大时至少在 nightly 或高风险 change 执行。
- `sqlc generate` 后无未提交差异。
- `sqlc vet`。
- Protobuf/gRPC 生成代码无未提交差异。
- migration dry-run 或可恢复说明。
- container build 使用 multi-stage，runtime image 不包含 Go SDK、源码、测试数据、secret。
- health endpoint 和 gRPC health 可用于 smoke。

## Frontend gates

Vite 前端默认 gates：

- `npm ci` 或锁文件一致安装。
- `npm run build`，即 Vite production build。
- Vitest / component / accessibility smoke 按项目风险执行。
- 预览环境可访问关键页面。
- Web Vitals 或平台 speed/observability 至少有采集计划。
- 生产 promote 后验证关键页面、登录/支付/核心表单、错误页和静态资源。

Vercel 默认使用 Preview 和 Production 分离；production 通过 Git、CLI、Deploy Hook 或 API 触发均可，但必须能追溯 commit 和 deployment URL。

## AI gates

用户可见 AI 能力默认 gates：

- `ai/prompts/<capability>/prompt.md`、`cases.jsonl`、`rubric.md`、`runbook.md` 存在。
- 相关 eval 通过，或明确记录失败接受原因。
- model、prompt version、schema version 写入配置或 release log。
- tool 权限、structured output parse failure、fallback/disable switch 已检查。
- 涉及金钱、权限、通知、删除、隐私、高风险建议时必须人工 checkpoint。

## Secrets 与供应链

- GitHub Actions 默认 `permissions: contents: read`；只有部署 job 提升到必要权限。
- 云部署优先 OIDC；没有 OIDC 时，长期 secret 必须最小权限、可轮换、只存在 CI secret store。
- 不用 Docker build args 传 secret；公开仓库的 provenance 可能暴露 build args。
- 发布给外部用户运行的二进制、包或镜像，逐步启用 artifact attestation、image digest、SBOM。
- 第三方 action 默认固定主版本或 SHA；高风险部署 action 应有 owner、用途和替代方案记录。

## Rollback 与 release log

`release/rollback/<service>.md` 最少写：

- 回滚到哪个 artifact 或上一 release。
- 数据库 migration 是否可逆；不可逆时如何降级或补偿。
- feature flag / disable switch。
- 回滚后的 smoke test。
- 谁可以执行，执行入口在哪里。

`release/runs/YYYY-MM-DD-<service>-<release-id>.md` 最少写：

- release id、commit SHA、artifact digest/deployment URL。
- OpenSpec change id。
- gates 结果。
- deploy 时间和环境。
- smoke test 结果。
- 观察到的 SLO/错误信号。
- 是否回滚，或下一步 action。

## 只问人的关键判断

默认不问：workflow 文件名、job 名、release JSON 字段顺序、smoke 文案细节、是否把 preview 叫 staging。

必须问：

- 是否把 production deploy 设为自动还是人工 checkpoint。
- 是否允许 CI 自动执行 migration。
- 是否允许自动回滚或自动关闭功能。
- 是否使用长期云 secret，而不是 OIDC。
- 是否发布 artifact 给外部用户运行并需要 provenance/SBOM。
- 是否有付费 SLA、资金、隐私、安全或合规风险。

当前建议默认接受：生产部署默认由 CI 构建 artifact，首次和高风险 release 需要人工 checkpoint；普通小改动可自动到 preview/staging，但 production 不默认静默自动发布。

## 本专项 Review A：一人公司可落地性

结论：可落地，前提是把发布流水线当作少量可检查事实，而不是平台项目。

- `release/pipelines/<service>.json` 能让一个人快速判断缺哪类 gate。
- `smoke.md` 和 `rollback.md` 把最容易临场遗忘的步骤提前写好。
- 与 W7 SRE-lite 的 `ops/slo` 和 `ops/release` 复用，不新增多人审批流程。
- GitHub Actions 是默认，不是强绑定；不用 GitHub 时只要提供等价 gates。
- 最大摩擦是第一条真实流水线需要一次性整理脚本；因此需要 `release-pipeline-gates` skill 和验证脚本。

## 本专项 Review B：产品/工程/运维风险

结论：这阶段主要降低“测试通过但发布失败”和“发布失败不知道怎么退”的风险。

- build/release/run 分离和 release id 解决 artifact 不可追溯问题。
- secrets/OIDC/provenance 规则降低 CI 泄密和供应链风险。
- post-deploy watch 连接 SLO，避免发布后立刻离开。
- migration、AI 副作用、资金/权限/隐私风险都被列为人工 checkpoint。
- 仍不锁定云厂商；真实项目需要在具体部署 change 中补 provider 细节。
