# 可选技术栈偏好

> 状态：按需参考，不是 Quick/Standard/High-risk 路由的默认前置条件。

除非仓库或用户明确覆盖，否则使用这些默认值。

## Application Template

- 新应用必须由批准模板在空目录生成，不手工拼装项目根目录。
- 当前 Go 服务批准来源是 Kratos CLI 官方脚手架；记录 CLI 版本、`kratos new` 命令、模板来源/revision、生成文件和首次构建结果。
- 后续发布自有应用模板后，以自有模板的版本化生成器为准；切换模板要保留迁移与回退说明。
- 手工目录与模板相似不构成同源证据，现有非模板项目必须通过明确迁移或重建决定处理。

## Backend

- 优先 Go。
- 优先 go-kratos 管服务结构、middleware、transport、config、logging、metrics 和 tracing。
- API 优先由 Protobuf 定义，服务间通信默认 gRPC。
- HTTP 只在浏览器、webhook、第三方或公开 API 兼容场景暴露。

## Data

- 默认数据库优先 MySQL；项目应固定受支持版本，并在例外选择 PostgreSQL、SQLite 或其他数据库时记录原因。
- SQL 优先采用 MySQL/PostgreSQL 都能清晰表达的通用语法；避免把数据库专有函数、类型、操作符、扩展或隐式行为写进核心领域查询。确需使用时，隔离在适配层并记录替代路径。
- 默认不创建 foreign key。跨表引用完整性由应用层校验、事务、幂等、唯一/非空约束、删除策略、补偿任务和定期一致性扫描共同保证；不能因没有外键而省略并发与孤儿数据测试。
- 优先清晰 SQL schema 和 query。
- 使用 sqlc 生成类型安全 Go 数据访问代码。
- migration、schema、query 文件和生成代码都必须可 review。

## Local Integration Environment

- 多组件项目必须提供统一的本地集成入口，覆盖全部后端、前端、MySQL 和必要 mock/provider；入口应包含启动、就绪、smoke、日志定位和清理。
- 前端开发服务器可以运行在宿主机，不要求为测试单独制作镜像；完整集成记录必须列出并实际启动前端，不能把只有依赖容器或后端的组合称为完整环境。
- Compose、脚本、任务运行器或等价方案都可以采用，关键是从干净环境可重复恢复，而不是指定某一种编排工具。

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
