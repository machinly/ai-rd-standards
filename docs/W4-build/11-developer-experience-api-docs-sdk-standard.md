# W4 Build 触发专项：开发者体验、API 文档、SDK 与示例治理规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及对外 API 文档、SDK、CLI、示例、developer changelog、文档站、quickstart、OpenAPI/proto reference 或开发者可依赖的 AI/API 能力说明时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/00-main.md`，由主入口判断是否触发本专项。

## 目标

一人公司做 AI 产品时，外部开发者体验往往是增长杠杆，也是支持成本来源：API 能调但不知道怎么认证；gRPC/proto 有定义但没有 quickstart；SDK 示例过期；错误码、rate limit、idempotency、webhook 签名、AI 输出限制没有写清；changelog 只是一堆 commit；AI tool 或 RAG API 的安全边界藏在客服回复里。本专项的目标是把对外 API、SDK、示例、文档站和变更沟通压成一套可生成、可验证、可维护的最小 DX 系统。

本专项不要求立刻建设完整 developer portal。默认先用仓库工件、生成 reference、少量可运行示例和 release notes，把“开发者能否在 15 分钟内安全调用成功”作为核心验收。

## 核心依据

- 《人月神话》：概念完整性体现在接口、术语、示例和错误语义的一致性；文档不一致会让用户替你发现系统边界。
- 小型项目管理：一人公司不能维护厚重文档团队；只维护最影响 adoption 和支持成本的五个工件。
- Diátaxis：开发者文档要分清 tutorial、how-to、reference、explanation；quickstart 不是 reference，概念解释也不是操作步骤。
- Google Developer Documentation Style Guide：开发者文档应清晰、一致、可执行，面向具体任务，用主动语态和明确步骤。
- Google AIP-192 / API Design Guide：API 文档是 API 设计的一部分；用户通常只能通过 API surface 和文档理解你的系统。
- OpenAPI Specification：HTTP API 应有机器可读描述，让人和工具理解服务能力、生成 reference、client 和测试。
- gRPC / Protobuf / Buf：gRPC 文档应包含 quickstart、教程和 reference；proto 定义、注释、breaking check 和 generated client 是文档事实源。
- SemVer / Keep a Changelog / GitHub API versioning：公开 API/SDK/CLI 需要声明 public API、版本边界、升级指引、破坏性变化和可读 changelog。
- Stripe / GitHub / OpenAI API docs：高质量 API 文档通常同时说明认证、错误、rate limit、request id、idempotency、SDK 示例、sandbox/test mode 和版本变更。
- W9 知识恢复、W2 API 契约、W8 支持、W2 信任声明、W5 可访问性和 W6 商业承诺：内部知识、API 契约、支持、信任声明、可访问性和商业承诺已经定义底层边界；本专项负责把它们面向开发者表达。

## 范围

适用对象：

- 对外 HTTP API、gRPC/protobuf API、webhook、SDK、CLI、OpenAPI/Proto reference、示例代码、文档站、developer dashboard、AI API、RAG API、tool/integration API。
- 面向客户开发者的 quickstart、how-to、reference、explanation、changelog、migration guide、known limitations、rate limit/error docs。
- Go/Kratos/sqlc/gRPC 服务、Vite 文档站或控制台、AI workflow、SDK 和示例仓库。

不适用对象：

- 纯内部 context pack 和团队知识恢复；由 W9 知识恢复专项管。
- API 兼容性决策本身；由 W2 API compatibility 专项管。
- 客服回复和支持队列；由 W8 客户支持专项管。
- 营销首页、品牌叙事、SEO 内容农场；除非它们包含开发者可依赖的技术承诺。

## 最小工件

每个对外开发者 target 使用同一个 `<target>` 文件名：

```text
developer-experience/
  docs-portal/<target>.json
  api-reference/<target>.json
  sdk-examples/<target>.json
  changelog-release-notes/<target>.md
  dx-review/<target>.md
```

### `developer-experience/docs-portal/<target>.json`

文档入口地图必须包含：

- `target`
- `owner`
- `audiences`
- `entrypoints`
- `diataxis_coverage`
- `quickstart`
- `authentication`
- `environments`
- `support_paths`
- `linked_artifacts`
- `human_checkpoint`
- `review_cadence`
- `status`

`entrypoints` 每项至少包含：

- `title`
- `path`
- `type`：`tutorial`、`how_to`、`reference`、`explanation`、`changelog`、`migration`、`support`。
- `audience`
- `source_of_truth`
- `freshness`

默认规则：

- 每个 public/stable API 至少有 quickstart、authentication、errors/rate limits、reference、changelog。
- AI API 还必须有 model/route limitation、input/output boundaries、safety/abuse boundary、data retention/training note 的链接。
- 文档入口不复制内部规范，只链接 contracts、SRE、billing、trust、security、support、AI eval 等事实源。

### `developer-experience/api-reference/<target>.json`

API reference 工件必须包含：

- `target`
- `owner`
- `api_surfaces`
- `spec_sources`
- `generated_reference`
- `auth`
- `errors`
- `rate_limits`
- `idempotency`
- `pagination`
- `webhooks`
- `request_response_examples`
- `sdk_links`
- `contract_test_links`
- `status`

`api_surfaces` 每项至少包含：

- `name`
- `protocol`：`grpc`、`http`、`webhook`、`event`、`sdk`、`cli`、`ai_tool`。
- `stability`
- `version`
- `source`
- `reference_path`
- `example_path`
- `owner`

默认规则：

- gRPC/protobuf reference 从 `.proto` 和注释生成；不要手写与 proto 矛盾的字段说明。
- HTTP reference 优先来自 OpenAPI；没有 OpenAPI 时必须登记手写 reference 和同步检查。
- 错误码、request id、trace id、rate limit、retry、idempotency、pagination、webhook signature 都是 reference 的一部分。
- 示例请求/响应不得包含真实 API key、真实个人数据、客户内容、生产 URL token、完整 prompt/response 或秘密。

### `developer-experience/sdk-examples/<target>.json`

SDK 与示例工件必须包含：

- `target`
- `owner`
- `languages`
- `sdks`
- `examples`
- `quickstart_commands`
- `test_mode_or_sandbox`
- `security_notes`
- `ci_gates`
- `release_gates`
- `human_checkpoint`
- `status`

`examples` 每项至少包含：

- `name`
- `language`
- `path`
- `scenario`
- `uses_test_mode`
- `required_env_vars`
- `expected_output`
- `last_verified`
- `status`

默认规则：

- 示例必须能在 test mode/sandbox/local mock 下运行；不要求用户先接触真实生产数据。
- Go SDK 示例优先覆盖认证、简单调用、错误处理、重试/idempotency、分页/streaming、webhook verify、AI safety boundary。
- TypeScript/Vite 示例不得把 server API key 暴露到浏览器；浏览器示例只能使用公开 key、短期 token 或后端代理。
- 每个 public SDK release 至少跑 example smoke test；跑不了的示例必须标记为 conceptual，不得伪装成可运行。

### `developer-experience/changelog-release-notes/<target>.md`

开发者 changelog / release notes 必须包含：

```markdown
# <target> Developer Changelog

## Scope

## Versioning Policy

## Unreleased

## Breaking Changes

## Added

## Changed

## Deprecated

## Fixed

## Security

## Migration Notes

## Linked Releases

## Review Cadence
```

默认规则：

- Changelog 为开发者服务，不是 commit log；只记录开发者需要知道的 notable changes。
- Breaking changes 必须链接 migration guide、contract tests、支持窗口和客户沟通渠道。
- Security changes 不泄露可利用细节，必要时链接 W7 安全/隐私事故专项的安全 advisory 或事故记录。
- AI model、prompt、tool schema、rate limit、cost behavior、data retention、SDK default 变化如果影响用户集成，必须记录。

### `developer-experience/dx-review/<target>.md`

DX review 必须包含：

```markdown
# <target> Developer Experience Review

## Recent Changes

## Quickstart Health

## Reference Accuracy

## SDK / Examples

## Error / Rate Limit / Idempotency Docs

## AI / Data / Security Boundaries

## Changelog / Migration

## Support Signals

## Open Risks

## One Next Change

## Review Cadence
```

默认节奏：

- pre-revenue：每月一次，或每次 public API/SDK/AI behavior 变更前。
- 有开发者客户：每次 API/SDK release、breaking/deprecation、主要文档改版、support driver 上升后。
- 发现支持问题来自 docs：当天或当周修复入口、示例或 reference。

## Go / Kratos / sqlc / gRPC 默认规则

- `.proto`、OpenAPI、sqlc schema/query、gRPC error model、contract tests 是 reference 的事实源；文档不得覆盖或改写事实。
- Kratos/gRPC 服务示例至少包含 auth metadata、tenant context、request id、deadline、retry/idempotency 说明。
- Go SDK 或 generated client 必须声明版本、支持的 API version、错误类型、context/deadline 用法、可观测字段和 release policy。
- gRPC streaming、long-running job、webhook replay、async job status 必须有示例和失败路径说明。
- API docs 中的字段名、enum、错误码、quota、rate limit、billing meter 必须能链接到对应契约、计费或观测工件。

## Vite / 文档站默认规则

- 文档站或 developer console 可以用 Vite/VitePress/同类工具，但第一屏应是可用文档入口，不是营销 hero。
- UI 风格参考 Vercel Geist：可扫描导航、清晰 code block、浅/深色 token、紧凑表格、少装饰、状态明确。
- 文档站必须支持搜索或清晰目录，代码块可复制，错误/限制/安全说明不能藏在折叠深处。
- 认证、API key、webhook secret、环境变量示例必须明确 server-side / client-side 边界。
- 文档站构建至少跑 `vite build` 或等价构建检查；关键 quickstart 页面可用链接检查或 smoke test。

## AI workflow 默认规则

- AI API docs 必须说明输入边界、输出不确定性、结构化输出 schema、tool side effects、rate/cost limits、safety policy、数据保留/训练边界。
- 示例不得暗示 AI 输出一定正确、可替代专业意见、无版权风险、无隐私风险或总能复现。
- 每个 AI 示例至少有一个失败/降级路径：schema parse failure、tool denied、rate limit、model fallback、unsafe request、RAG no-answer。
- AI behavior 变更如果影响开发者集成，必须同时更新 eval 链接、changelog、known limitations 和示例。

## 需要人判断的关键点

默认不问：章节顺序、低风险文案、非 public/internal 示例、普通 typo、自动生成 reference 的格式差异。

必须问：

- 是否将 API/SDK/AI capability 从 experimental 升级为 stable/public。
- 是否发布 breaking change、deprecation、migration guide 或 support window。
- 是否承诺特定模型、准确率、延迟、rate limit、成本、数据保留、不训练、合规或安全能力。
- 是否把示例连接到真实生产环境、真实客户数据、真实资金/权限/删除动作。
- 是否公开 security-sensitive、abuse-sensitive、prompt-injection、webhook signature bypass 或 exploit-like 示例。
- 是否发布官方 SDK、CLI、template、integration 或客户可依赖的 code sample。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“入口在哪里、reference 是否准、SDK/示例能不能跑、变更怎么说、体验哪里卡”。
- 保留：人只判断 stable/public、破坏性变更、强承诺、真实生产示例和安全敏感内容。
- 调整：不要求完整 developer portal；先用 docs map + generated reference + smoke-tested examples。
- 调整：不强制所有语言 SDK；优先 Go 和 TypeScript，因为它们对应后端和 Vite 主要栈。
- 风险：文档容易过期。缓解：把 reference 绑定 proto/OpenAPI，示例绑定 CI smoke test，changelog 绑定 release gate。

结论：可落地。一个人可以先把第一个 public API 的 quickstart、reference、一个 Go 示例、一个 TypeScript/Vite 示例和 changelog 跑通。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：15 分钟 quickstart 和清晰示例降低开发者流失，比堆更多功能更直接。
- 工程角度：proto/OpenAPI/generated reference 避免文档和实现分叉；contract tests 与 examples 形成真实验收。
- 运维角度：错误、rate limit、request id、status、webhook replay 和 idempotency 文档能降低支持和事故排查成本。
- 安全隐私角度：示例默认 test mode，不泄露 API key、客户数据、raw prompt/response 或 exploit 细节。
- 成本角度：优先维护少量高影响示例和 changelog，避免文档站变成另一个产品。

结论：可落地。本专项把开发者体验变成可验证的研发 surface，而不是上线后靠支持消息补洞。
