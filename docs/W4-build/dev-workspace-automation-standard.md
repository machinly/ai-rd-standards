# W4 Build 触发专项：开发环境、命令自动化与本地可复现规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及本地工具链、命令目录、依赖服务、seed/fixtures、reset、one-step verify、Codex handoff 或开发工作区可复现性时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/main.md`，由主入口判断是否触发本专项。

## 目标

一人公司最常见的注意力泄漏不是技术难题，而是每天重新找命令、重建环境、猜 seed 数据、修本机依赖、想不起生成代码顺序。本专项定义开发工作区和命令自动化规范，让 Go/Kratos/sqlc/gRPC、Vite 和 AI workflow 的本地开发有一条可复制的黄金路径。

默认原则：本地能一键验证，生产才有资格稳定。命令、工具链、依赖服务、环境变量、fixtures 和 reset 步骤必须显式记录；不能靠人的肌肉记忆。

## 核心依据

- 《人月神话》：没有银弹；工程生产率来自持续降低偶然复杂度，而不是期待个人记忆永远可靠。
- 小型项目管理：小项目的流程要服务下一步行动，命令和环境说明必须短、准、可执行。
- The Joel Test：高质量团队至少应能使用 source control、一步构建和持续构建；一人公司裁剪为“一步本地验证”和“一条黄金路径”。
- Software Engineering at Google, Build Systems and Build Philosophy：构建系统把源代码变成机器可运行 artifact；好的构建重视可靠性、可重复和开发者效率。
- Software Engineering at Google, Continuous Integration：快速反馈、自动化和持续测试能降低缺陷越晚发现越昂贵的问题。
- Twelve-Factor App Dependencies / Dev-Prod Parity / Admin Processes：依赖要显式声明；开发、预览、生产尽量保持接近；一次性管理任务也应以同样环境运行。
- Development Containers Specification：开发环境应能用代码描述、创建和重建。
- Docker Compose：多容器本地依赖服务可用一个配置和命令启动。
- Go Toolchains / Workspaces：Go toolchain 和 workspace mode 会影响构建，应记录版本和 `GOWORK` 状态。
- sqlc generate/vet：SQL schema/query 到 Go 代码的生成、检查必须成为显式命令。
- Vite CLI：前端 dev/build/preview 应通过 npm scripts 或等价命令固定。

## 范围

适用对象：

- Go/Kratos/gRPC/sqlc 后端服务。
- Vite 前端应用。
- PostgreSQL、Redis、queue、object storage、mail/webhook mock、observability mock 等本地依赖。
- AI prompt/eval/tool workflow 的本地 fixtures、mock provider、dry-run。
- 代码生成、测试、lint、build、preview、reset、seed、debug、smoke、release prep。
- Codex 或人中断后恢复本地开发上下文。

不适用对象：

- 一次性 throwaway script，且不进入生产、不访问真实数据、不调用真实供应商。
- 完全由 CI 执行且本地不需要运行的供应链证明任务。
- 真实生产 secret、真实用户数据、真实供应商凭据。

## 最小工件

每个产品、服务、前端应用或 AI workflow 使用同一个 `<target>` 文件名：

```text
dev-workspace/
  workspace-map/<target>.json
  command-catalog/<target>.md
  local-environment/<target>.md
  seed-fixtures/<target>.md
  verification/<target>.json
```

### `dev-workspace/workspace-map/<target>.json`

工作区地图用于机器检查和快速恢复，必须包含：

- `target`
- `owner`
- `stack`
- `toolchains`
- `package_managers`
- `entrypoints`
- `command_runner`
- `local_services`
- `env_files`
- `generated_artifacts`
- `seed_fixtures`
- `verification`
- `human_checkpoint`
- `review_cadence`

`toolchains` 每条至少包含：

- `name`
- `version_source`
- `install_check`
- `required`

`entrypoints` 每条至少包含：

- `name`
- `path`
- `kind`：`backend`、`frontend`、`worker`、`ai_workflow`、`migration`、`tooling`
- `run_command`

默认：Go、Node/npm、sqlc、protoc/buf、Docker/Compose、OpenSpec、Vite 只要被 target 使用，都要在 toolchains 中列出。

### `dev-workspace/command-catalog/<target>.md`

命令目录必须包含：

- `Setup`
- `Generate`
- `Develop`
- `Test`
- `Verify`
- `Run Local`
- `Reset`
- `Debug`
- `Release Prep`
- `Codex Handoff`

默认命令设计：

- 命令少于 12 条，按常见动作组织。
- 每条命令包含目的、执行目录、命令、预期结果、失败时下一步。
- 至少有一个 one-step local verify 命令，能跑生成、测试、构建和关键 smoke 的本地子集。

### `dev-workspace/local-environment/<target>.md`

本地环境说明必须包含：

- `Scope`
- `Toolchains`
- `Environment Files`
- `Local Services`
- `Ports`
- `Seed Data`
- `Secrets Policy`
- `Reset Procedure`
- `Troubleshooting`

默认：`.env.example` 可以记录变量名、说明和假值；不得提交真实 secret。外部供应商默认 mock、sandbox 或 dry-run。

### `dev-workspace/seed-fixtures/<target>.md`

seed/fixtures 说明必须包含：

- `Scope`
- `Datasets`
- `Creation Command`
- `Reset Command`
- `AI Fixtures`
- `Privacy Limits`
- `Determinism`
- `Refresh Cadence`

默认：本地 seed 必须可重跑；不使用真实用户数据；AI fixtures 包含代表、边界和失败样例。

### `dev-workspace/verification/<target>.json`

本地验证计划必须包含：

- `target`
- `owner`
- `one_step_commands`
- `smoke_checks`
- `generated_checks`
- `data_checks`
- `frontend_checks`
- `ai_checks`
- `ci_mapping`
- `human_checkpoint`

默认：`one_step_commands` 至少包含一条 `verify` 或等价命令；Go target 包含 `go test ./...`；sqlc target 包含 `sqlc generate` 与 `sqlc vet` 或说明；Vite target 包含 `npm ci`、`npm run build`；AI target 包含最小 eval 或 fixture check。

## Go / Kratos / sqlc / gRPC 默认规则

- 记录 Go toolchain 来源、`go env GOWORK` 期望状态、`go test ./...`、`go test -race` 的使用边界。
- Kratos 服务至少记录启动命令、配置来源、gRPC/HTTP 端口、health check、local config。
- sqlc 生成命令必须独立可跑；generated code diff 必须可 review。
- Protobuf/buf 生成、lint、breaking check 进入 command catalog 或 verification。
- migration/seed/reset 命令必须说明是否会破坏本地数据；任何生产数据操作都不属于本地 reset。

## Vite 前端默认规则

- package manager、lockfile、Node 版本来源必须记录。
- `npm ci`、`npm run dev`、`npm run build`、`npm run preview` 或等价命令进入 command catalog。
- 本地 API endpoint、mock、CORS、env 前缀和 preview URL 必须记录。
- dark/light theme、Vercel Geist token、Web Vitals 或 Playwright smoke 若存在，必须有本地检查入口。

## AI workflow 默认规则

- 本地 AI workflow 默认 dry-run、mock provider 或低成本 sandbox，不默认调用生产模型和真实工具。
- prompt/tool/eval fixtures 必须能本地重跑，且不包含真实用户隐私内容。
- tool side effect 默认 off；需要 commit 模式时必须有明确人工 checkpoint。
- local eval 记录模型路由、prompt version、dataset/fixture 版本和成本上限。

## 需要人判断的关键点

只把这些工作区判断交给人：

- 是否允许本地命令调用真实供应商、真实模型、真实支付、真实邮件或真实生产数据。
- 是否接受本地/预览/生产环境差异。
- 是否把破坏性 reset、migration、backfill 或 tool commit 暴露为一键命令。
- 是否引入新的长期工具链、devcontainer、compose stack 或付费开发工具。
- 是否让 AI agent 自动运行有副作用命令。

其他命令完整性、路径存在性、章节、secret 扫描、verify gate 结构由 Codex 和 verifier 检查。

## Review 1：一人公司注意力审查

- 保留：五类工件回答“工作区有什么、命令怎么跑、环境怎么搭、数据怎么来、怎么验证”。
- 保留：人审点只覆盖真实外部副作用、环境差异、破坏性命令和长期工具链选择。
- 调整：不强制 devcontainer 或 Docker Compose；只有需要重建环境或本地依赖服务时才使用。
- 调整：命令目录限制数量，避免变成命令百科。
- 风险：本地验证太慢会没人跑。缓解：要求 one-step local verify 是 CI 的快速子集，而不是完整 CI。

结论：可落地。一个人可以在一个专注工作块内为 target 写出黄金路径，并让 Codex 后续按同一命令面执行。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：seed/fixtures 支持稳定复现关键用户路径和 AI 行为，不依赖偶然数据。
- 工程角度：Go/sqlc/protobuf/Vite/AI 命令顺序明确，减少“本机能跑”的隐性差异。
- 运维角度：本地 health、ports、reset、debug 和 smoke 与 release gate 对齐，降低上线前盲区。
- 安全隐私角度：真实 secret、真实用户数据、真实供应商副作用默认禁止。
- 成本角度：AI sandbox、mock 和本地快速验证降低 token、云资源和人类上下文浪费。

结论：可落地。本专项把“每天怎么开始、怎么验证、怎么恢复”固定成低摩擦入口，保护一人公司的注意力。
