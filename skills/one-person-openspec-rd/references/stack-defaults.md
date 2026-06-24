# 默认技术栈

除非仓库或用户明确覆盖，否则使用这些默认值。

## Backend

- 优先 Go。
- 优先 go-kratos 管服务结构、middleware、transport、config、logging、metrics 和 tracing。
- API 优先由 Protobuf 定义，服务间通信默认 gRPC。
- HTTP 只在浏览器、webhook、第三方或公开 API 兼容场景暴露。

## Data

- 优先清晰 SQL schema 和 query。
- 使用 sqlc 生成类型安全 Go 数据访问代码。
- migration、schema、query 文件和生成代码都必须可 review。

## Frontend

- 前端项目优先 Vite。
- 已有框架时沿用；新项目保持脚手架小。
- UI 风格参考 Vercel Geist：克制界面、清晰排版、浅色/深色 token、精确边界和少装饰噪音。

## AI Behavior

- 优先 deterministic workflow，再考虑 autonomous agent。
- 生产 prompt 或 prompt builder 必须进入代码/配置。
- 改 prompt、模型设置或工具 workflow 前，先补最小 eval。
- 记录模型、prompt 版本、eval 日期和代表样例。

## Operations

- 每个服务或 workflow 先有一个用户可见 SLO。
- 先定义 error budget action，再搭 dashboard。
- 观测性只服务决策：日志用于排障，metrics 用于 SLO，traces 用于跨服务延迟。

## Source Anchors

- Kratos: https://go-kratos.dev/docs/
- sqlc: https://docs.sqlc.dev/
- gRPC Go: https://grpc.io/docs/languages/go/
- Vite: https://vite.dev/guide/
- Vercel light design: https://vercel.com/design.md
- Vercel dark design: https://vercel.com/design.dark.md
- OpenAI prompt engineering: https://developers.openai.com/api/docs/guides/prompt-engineering
- OpenAI evals: https://developers.openai.com/api/docs/guides/evaluation-best-practices
- Anthropic agents: https://www.anthropic.com/engineering/building-effective-agents
- Google SRE: https://sre.google/workbook/implementing-slos/
