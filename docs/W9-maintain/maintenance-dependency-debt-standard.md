# W9 Maintain 触发专项：维护、依赖升级、技术债与弃用治理规范

## W9 触发定位

本文件是 W9 Maintain 的触发型专项，不是 W9 主入口。只有当当前工作涉及依赖升级、技术债、弃用、runtime/framework/AI SDK 维护、Dependabot、重大升级或 deprecation plan 时，才需要读取本文件。

普通 W9 维护入口应先回到 `docs/W9-maintain/main.md`，由主入口判断是否触发本专项。

## 目标

一人公司最危险的维护问题通常不是“今天不能跑”，而是几个月后依赖、运行时、生成代码、AI workflow、测试夹具和弃用接口一起过期，任何小改动都变成未知风险。本专项定义最小维护治理规范，让依赖升级、技术债、弃用和 refactor 变成可计划、可验证、可暂停的工作。

默认原则：不追新，但也不长期冻结。依赖和技术债都有利息；一人公司要把利息看见、分批支付，并把高风险判断留给人。

## 核心依据

- 《人月神话》：没有银弹；复杂度不能靠一次“大清理”消失，必须通过持续纪律降低。
- 小型项目管理：小项目维护计划应围绕风险、下一步和责任人，避免把维护写成长期愿望清单。
- Google Software Engineering at Google, Dependency Management：依赖管理是随着时间变化的依赖网络问题，不只是安装某个包；外部依赖会带来安全、弃用、兼容性和升级级联。
- Google Software Engineering at Google, Deprecation：代码是负债；有序迁移和移除 obsolete systems 能降低成本并提升速度。
- Google Software Engineering at Google, Static Analysis：静态分析可帮助保持代码使用现代 API、发现 deprecated API，并减少技术债回流。
- Martin Fowler, Technical Debt / Technical Debt Quadrant：技术债要区分鲁莽/审慎、主动/无意，重点管理未来额外修改成本。
- Martin Fowler, Refactoring：refactor 是不改变外部行为的小步设计改进，应有测试保护。
- Working Effectively with Legacy Code：修改遗留代码前先建立 characterization tests 和接缝，避免重写冲动。
- Hidden Technical Debt in Machine Learning Systems：AI/ML 系统债务不仅在代码，还在数据依赖、配置、反馈环、胶水代码和外部世界变化。
- Go 官方依赖管理 / govulncheck：Go modules 记录依赖并支持升级、替换和安全扫描；govulncheck 根据实际可达代码路径降低漏洞噪音。
- GitHub Dependabot：自动化依赖更新和安全更新需要配置 schedule、ecosystem、grouping 和 PR 策略。
- npm package-lock / npm ci / npm audit：前端依赖需要 lockfile、可复现安装和安全审计。
- Vite migration guide：前端框架大版本升级应先读迁移指南，必要时采用渐进迁移。

## 范围

适用对象：

- Go/Kratos/gRPC/sqlc 后端服务、shared Go module、generated code。
- Vite 前端、Node/npm 依赖、构建工具和浏览器端 SDK。
- AI prompt/model/tool/eval workflow、模型路由、外部 AI SDK。
- GitHub Actions、Docker、数据库 migration 工具、observability/security/release 供应商。
- 技术债、弃用接口、旧配置、旧 feature flag、旧 prompt/eval dataset。

不适用对象：

- 不进入生产、不会复用、不会访问真实数据或真实供应商的一次性实验。
- 自动生成且可丢弃的本地缓存。
- 单次小 patch，前提是没有改变运行时、框架、API、数据、auth、安全或 AI 行为契约。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
maintenance/
  dependency-inventory/<target>.json
  update-policy/<target>.md
  upgrade-plans/<target>.md
  debt-register/<target>.jsonl
  deprecation-plans/<target>.md
```

### `maintenance/dependency-inventory/<target>.json`

依赖清单必须包含：

- `target`
- `owner`
- `stack`
- `package_managers`
- `manifests`
- `lockfiles`
- `generated_artifacts`
- `critical_dependencies`
- `runtime_versions`
- `update_channels`
- `security_scanning`
- `dependency_automation`
- `human_checkpoint`
- `review_cadence`

`critical_dependencies` 每条至少包含：

- `name`
- `ecosystem`
- `role`
- `version_source`
- `update_policy`
- `risk`
- `upstream_source`
- `rollback`

默认把这些列为 critical：Go runtime、Kratos、grpc-go、protobuf、sqlc、migration 工具、PostgreSQL driver、Vite、React/路由/状态库、OpenAI/AI SDK、auth provider SDK、payment/email/storage/observability SDK、GitHub Actions runner/tooling。

### `maintenance/update-policy/<target>.md`

更新策略必须包含：

- `Scope`
- `Supported Toolchains`
- `Update Cadence`
- `Security Updates`
- `Batch Strategy`
- `Verification Gates`
- `Rollback`
- `Human Checkpoints`

默认节奏：

- security patch：发现后 1 个工作块内 triage；真实可达、高危或公网暴露路径优先处理。
- patch/minor：按月小批量处理，除非触发安全、兼容性或成本问题。
- major/runtime/framework：单独 OpenSpec change，先读官方 migration guide，再做升级计划。
- AI SDK/model route/eval dataset：必须跑最小 eval，并记录成本、质量和回退。

### `maintenance/upgrade-plans/<target>.md`

升级计划用于重大升级或维护工作，必须包含：

- `Scope`
- `Trigger`
- `Compatibility Notes`
- `Steps`
- `Generated Code`
- `Test / Eval Matrix`
- `Release Strategy`
- `Rollback`
- `Decision Log`

如果当前没有重大升级，也要写明“暂无待升级项”和下一次复审日期，防止依赖清单与现实脱节。

### `maintenance/debt-register/<target>.jsonl`

技术债登记每行一个 JSON object，必须包含：

```json
{"id":"DEBT-0001","date":"2026-06-24","target":"api","area":"testing","type":"test_debt","source":"incident","symptom":"critical path lacks regression test","impact":"slower safe change","interest":"manual verification before each release","owner":"solo-founder","status":"accepted","planned_action":"add characterization test","review_on":"2026-07-24","linked_change":"openspec/changes/example/"}
```

允许 `status`：`accepted`、`planned`、`in_progress`、`paid_down`、`closed`、`superseded`。

默认规则：

- 债务必须写“利息”：它会让下一次开发多付出什么。
- `TODO`、`FIXME`、`HACK`、临时 workaround、跳过测试、禁用 lint、长期 feature flag、弃用 API 使用，都要有登记或明确说明为什么不是债。
- 只登记会影响未来修改、可靠性、安全、成本或 AI 行为的债；普通清洁感问题不进登记。

### `maintenance/deprecation-plans/<target>.md`

弃用计划必须包含：

- `Scope`
- `Deprecated Surface`
- `Consumers`
- `Migration Path`
- `Compatibility Window`
- `Observability`
- `Removal Steps`
- `Rollback`
- `Human Checkpoints`

弃用对象包括 API、gRPC 方法、DB 字段、配置项、feature flag、AI prompt/model route、CLI、webhook、frontend route、第三方 provider。

## Go / Kratos / sqlc / gRPC 默认规则

- `go.mod`、`go.sum` 必须入库；CI 使用 `go mod tidy` 检查漂移。
- Go 依赖安全扫描使用 `govulncheck ./...` 或等价 gate；真实可达漏洞优先。
- `replace`、`exclude`、fork、private module 必须记录原因、到期复审和退出计划。
- Kratos、grpc-go、protobuf、sqlc、migration 工具升级必须重新生成代码，并运行 Go tests、sqlc vet/verify、gRPC contract tests。
- gRPC/protobuf breaking change 走 W2 architecture / API compatibility 和 W6 release gate；不得用依赖升级顺手改协议契约。
- sqlc 升级必须确认 generated code diff 是否只来自工具升级，不混入业务改动。

## Vite / npm 默认规则

- `package-lock.json` 或仓库选定 lockfile 必须入库；CI 使用 `npm ci`。
- `npm audit` 或等价安全审计进入 release/security gate；`audit fix --force` 不作为默认自动操作。
- Vite、React、router、state、test runner、Playwright 等大版本升级必须读官方 migration guide。
- 前端依赖升级后至少运行 typecheck、unit tests、build、关键 Playwright smoke 和视觉/可访问性检查。
- UI token、Vercel Geist 风格、dark/light 主题变化不得和依赖升级混在一个无关 change 中。

## AI workflow 默认规则

- AI SDK、模型路由、prompt builder、tool schema、eval dataset、guardrail 升级都视为行为契约变更。
- 升级前记录当前 eval baseline、成本 baseline、latency baseline 和 fallback。
- 升级后必须跑代表样例、边界样例、失败样例，并对比质量、成本和错误类型。
- 不把“新模型更强”当作发布理由；必须说明它改善了哪个产品 outcome 或降低了哪个风险/成本。
- 删除旧 prompt/model route 前先确认没有 production trace、eval 或用户路径仍依赖旧版本。

## Dependabot / 自动化默认规则

- 自动化依赖更新默认按 ecosystem 分组，减少 PR 噪音。
- security updates 可更快；version updates 默认按月或按维护窗口批处理。
- 自动 PR 必须触发测试、构建、安全扫描和相关 eval，不允许只凭版本号合并。
- 一人公司默认限制同时打开的依赖 PR 数量，避免维护噪音淹没产品工作。
- 自动化只提出变更；重大升级、破坏性变更、fork/replace、付费供应商 SDK 替换仍需人审。

## 需要人判断的关键点

只把这些维护判断交给人：

- 是否升级 runtime、框架、数据库、auth/payment/security/AI provider 的 major version。
- 是否接受真实可达漏洞的临时例外。
- 是否替换、fork 或长期 pin 关键依赖。
- 是否引入 breaking API / protobuf / schema / prompt / eval contract change。
- 是否删除弃用接口、配置、feature flag、prompt/model route。
- 是否把一笔债从 `accepted` 改成长期 `planned` 或继续延期。

其他字段完整性、路径存在性、复审日期、敏感内容、lockfile 和脚本检查由 Codex 和 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五类工件对应“有什么依赖、怎么更新、怎么升级、欠了什么、怎么删除旧东西”，不要求维护委员会。
- 保留：人审点集中在高风险、不可逆、供应商锁定和行为契约变化。
- 调整：不强制每周升级；patch/minor 按月，security 按风险，major 单独 change。
- 调整：技术债必须写利息，防止登记表变成情绪垃圾桶。
- 风险：维护工件可能变成另一套 backlog。缓解：只记录会影响未来修改、可靠性、安全、成本或 AI 行为的债。

结论：可落地。一个人可以在一个维护工作块内为一个 target 写出依赖清单和策略，并把大升级拆成单独 OpenSpec change。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：依赖升级不能顺手改变用户行为；AI/model/prompt 变化必须回到 eval 和产品 outcome。
- 工程角度：Go/Vite/sqlc/gRPC/generated code 都有明确检查，减少“升级顺便重构”的混乱。
- 运维角度：security patch、rollback、release strategy 和 observability 入口保证升级能上线也能撤回。
- 安全隐私角度：真实可达漏洞、fork/replace、auth/payment/security SDK 都有人审和记录。
- 成本角度：自动化分组、PR 限流、债务利息和弃用移除，减少长期上下文和维护成本。

结论：可落地。本专项把“维护不是产品功能”的隐性风险变成可计划的小批量研发工作。
