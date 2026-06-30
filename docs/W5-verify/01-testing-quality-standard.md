# W5 Verify 触发专项：测试与质量策略规范

## W5 触发定位

本文件是 W5 Verify 的触发型专项，不是 W5 主入口。只有当当前验证涉及测试策略、test matrix、test run、flaky、Go/Vite/sqlc/gRPC 门禁、AI eval 或发布前质量证据时，才需要读取本文件。

普通 W5 验证入口应先回到 `docs/W5-verify/00-main.md`，由主入口判断是否触发本专项。

## 目标

一人公司需要的不是“测试越多越好”，而是用最少、最快、最可信的测试保护最重要行为。本专项定义一个风险驱动的测试组合，让 Go/Kratos/sqlc/gRPC、Vite 前端和 AI workflow 都有明确的测试层级、运行命令、flaky 处理和人审触发点。

默认原则：任何超过 1 个工作日的用户可见变更，必须先说明要保护哪些行为、用哪些测试证明、哪些风险需要人工验收。

## 核心依据

- 《人月神话》：测试不是银弹。复杂系统仍会有概念错误和集成错误，质量需要设计、规格、实现和验证共同承担。
- 小型项目管理：测试计划必须轻量到一个人能维护，只保留能减少返工、提升信心和恢复上下文的工件。
- Martin Fowler Practical Test Pyramid：测试组合应有更多低层、快速、确定的测试，少量端到端测试用于信心确认。
- Google Software Engineering / Testing Blog：按 small、medium、large 区分测试资源、速度和确定性；测试价值来自信任，flaky 会摧毁信任。
- xUnit Test Patterns：测试代码也需要可维护性，关注 fixture、exercise、verify、teardown 和 test smells。
- Go 官方 testing、fuzzing、race detector：Go 的基础门禁来自 `go test`、fuzz、benchmark 和 `-race`。
- sqlc 官方 `vet` / `verify`：SQL query 和 schema 变化需要在生成代码之外被验证。
- Vitest / Playwright 官方文档：Vite 前端默认用 Vitest 做快速测试，用 Playwright 做关键用户流 E2E。
- OpenAI evals / prompt engineering：AI 行为变化必须有代表样例、边界样例、失败样例和可重复 eval。

## 范围

适用对象：

- Go/Kratos/sqlc/gRPC 后端服务。
- Vite 前端应用和关键用户路径。
- AI prompt、model、tool、agent workflow。
- 数据迁移、权限、成本、安全、发布相关的高风险变更。

不适用对象：

- 一行以内、可人工直接确认且不进入生产的临时代码。
- 事故中的紧急缓解动作。事故后补充回归测试或显式记录不补的原因。
- 只更新文案或注释，且不影响产品、权限、隐私、成本或发布。

## 最小工件

每个生产服务、前端应用或用户可见 AI workflow 使用同一个 `<target>` 文件名：

```text
quality/
  test-strategy/<target>.md
  test-matrix/<target>.json
  test-runs/<target>.jsonl
  flaky-tests/<target>.md
```

`flaky-tests` 只有存在 quarantine、retry 或已知 flaky 时必须创建；没有 flaky 时可省略。

### `quality/test-strategy/<target>.md`

必须包含：

- `Scope`：本策略保护哪个服务、前端或 AI workflow。
- `Risk`：用户、数据、权限、成本、可靠性、安全和 AI 行为风险。
- `Test Portfolio`：small、medium、large、contract、smoke、manual exploratory 的组合。
- `Small Tests`：纯逻辑、领域规则、prompt builder、权限判断、错误映射等。
- `Medium Tests`：数据库、gRPC bufconn、testcontainers、组件测试、工具集成等。
- `Large Tests`：关键用户流、preview 环境、生产前 smoke、第三方真实依赖等。
- `AI Evals`：代表样例、边界样例、失败样例、grader 或人工校准。
- `Fixtures`：测试数据、seed corpus、golden files、脱敏样例。
- `Flaky Policy`：失败处理、retry、quarantine、修复期限。
- `Commands`：本地和 CI 必跑命令。
- `Human Checkpoints`：哪些质量例外必须人审。

### `quality/test-matrix/<target>.json`

用于机器检查，必须包含：

- `target`、`owner`、`risk_level`、`stack`、`change_types`
- `small_tests`、`medium_tests`、`large_tests`
- `contract_tests`、`smoke_tests`
- `ai_evals`
- `commands`
- `coverage_focus`
- `fixtures`
- `flaky_policy`
- `release_gate`
- `human_checkpoint`
- `review_cadence`

每个 `commands` 条目至少包含 `name`、`command`、`tier`、`when`。

### `quality/test-runs/<target>.jsonl`

记录关键 test run。生产发布前至少保留最近一次 release gate run：

```json
{"date":"2026-06-24","target":"billing-api","context":"release","command":"go test ./...","result":"pass","duration_seconds":42,"notes":"release 2026-06-24.1"}
```

### `quality/flaky-tests/<target>.md`

只有存在 flaky 时需要。必须包含：

- `Known Flakes`
- `Impact`
- `Quarantine Rule`
- `Owner`
- `Fix By`
- `Release Risk`

默认不允许长期依赖 retry。retry 只能作为短期隔离信号，不能替代修复。

## 测试分层默认值

### Small tests

目标：最快发现逻辑回归。

默认覆盖：

- Go domain/usecase 函数、权限判断、错误映射、config 解析。
- prompt builder、schema validator、tool permission resolver。
- 前端纯函数、状态 reducer、格式化、表单校验。

约束：

- 不访问外部网络。
- 不依赖真实数据库。
- 不使用 sleep。
- 不读取生产配置或 secret。

### Medium tests

目标：验证组件之间的真实交互。

默认覆盖：

- sqlc query 对真实 PostgreSQL schema 的读写。
- Kratos usecase/repo/service 之间的集成。
- gRPC handler 使用 bufconn 或本地 listener 验证 status code、metadata、deadline、auth context。
- Vite 组件在 Vitest browser mode 或等价环境中的交互。
- AI tool workflow 的 dry-run、schema、权限和错误路径。

### Large tests

目标：验证关键用户路径和发布配置。

默认覆盖：

- Playwright 关键路径，例如登录、创建、保存、导出、支付前检查。
- preview 环境 smoke。
- 第三方 sandbox 或真实供应商的最小兼容性检查。
- 生产发布后的只读 smoke。

大型测试数量必须少，失败必须能定位到 owner 和下一步。

## Go / Kratos / sqlc / gRPC 默认门禁

默认命令：

```bash
go test ./...
go test -race ./...
sqlc generate
sqlc vet
```

触发条件：

- 并发、cache、goroutine、stream、worker、共享 map、异步 agent loop 改动：运行 `go test -race ./...`。
- 输入解析、URL、JSON、SQL filter、权限表达式、prompt 模板变量：补 Go fuzz test 或记录不补原因。
- migration 或 schema 变化：运行 sqlc generate、sqlc vet；生产 schema 兼容性风险高时运行 sqlc verify 或记录跳过原因。
- gRPC API 变化：补 handler 或 bufconn 测试，覆盖成功、权限失败、validation 失败、not found、deadline/cancel 中适用项。

## Vite 前端默认门禁

默认命令：

```bash
npm run test -- --run
npm run build
npx playwright test
```

触发条件：

- 纯逻辑或组件状态变化：Vitest。
- 用户关键路径、可访问性风险、导航、表单提交、支付前确认、文件上传下载：Playwright。
- 视觉密集或响应式布局变化：至少做 desktop/mobile 截图或 Playwright 断言，避免文字重叠、按钮溢出、焦点丢失。

## AI workflow 默认门禁

AI 变更包括 prompt、model、temperature、tool schema、retrieval、agent route、guardrail 或 output schema。

默认要求：

- 至少包含代表样例、边界样例、失败样例。
- 记录 eval dataset 或本地 fixtures。
- 自动 grader 必须有人类校准记录，不能只看模型自评。
- 生产 prompt 变化需要链接 OpenSpec、eval 结果和回滚方式。
- 工具调用型 agent 必须测试错误工具、拒绝越权、超时、空结果、部分失败和人工审批路径。

## Flaky 策略

- 失败默认是真问题，先复现和定位。
- retry 只能用于降低临时噪音，必须创建 `quality/flaky-tests/<target>.md` 并设 `Fix By`。
- 不允许把 flaky 测试长期从 release gate 中静默移除。
- 如果测试依赖时间、随机数、网络、外部服务、共享数据库或全局状态，优先改成可控 fixture。

## 覆盖率策略

覆盖率只能作为风险提示，不作为唯一质量目标。

默认要求：

- 记录 `coverage_focus`，写清哪些行为必须被覆盖。
- 不为了达到百分比写无断言测试。
- 关键路径、权限、数据写入、成本限制、AI 工具副作用的测试优先级高于总体行覆盖率。

## 需要人判断的关键点

只把这些质量判断交给人：

- 哪些用户行为是不能破坏的核心行为。
- 哪些风险可以接受手工验收，哪些必须自动化。
- 是否允许带已知 flaky、跳过 race/sqlc verify/eval 发布。
- AI eval 失败时是修复、降级、回滚还是人工兜底。
- 大型 E2E 失败但小测试通过时是否继续发布。

其他内容由 Codex 先按模板创建并用脚本检查。

## Review 1：一人公司注意力审查

- 保留：只要求 `test-strategy` 和 `test-matrix` 两个核心工件，`test-runs` 记录事实，`flaky-tests` 条件触发。
- 保留：不追求完整 QA 部门流程，只要求能在本地和 CI 复现的命令。
- 调整：覆盖率不作为硬门槛，避免一个人为百分比写低价值测试。
- 调整：大型 E2E 只覆盖关键路径，防止测试维护成本超过产品代码。
- 风险：test matrix 可能形式化。缓解：验证脚本检查命令、风险、AI eval、flaky policy 和 release gate。

结论：可落地。本专项能在 30 到 60 分钟内为一个服务建立质量基线，适合一人公司长期维护。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：测试组合必须从“不能破坏的用户行为”反推，不从工具清单反推。
- 工程角度：Go/Kratos/sqlc/gRPC、Vite、AI workflow 都有默认门禁，减少每次重新思考。
- 运维角度：smoke、race、flaky 和 release gate 直接连接生产稳定性。
- 安全隐私角度：权限、数据写入、个人数据 analytics、AI 工具副作用需要进入测试矩阵。
- 成本角度：AI eval 和 E2E 不能无限扩张，必须记录何时运行和谁处理失败。

结论：可落地。该阶段补上了 release pipeline 之前的“测试设计依据”，也为后续真实项目提供可执行 quality gate。
