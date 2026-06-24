# 设计：Go/Kratos/sqlc/gRPC 服务端研发规范

## 设计决策

### 1. 采用 Kratos layout 作为默认，而不是强制框架形状

Kratos 官方说明 layout 是默认模板但不强制。对一人公司，默认模板能减少决策成本；当服务很小时，可以删除不用的示例和包，不做过度分层。

### 2. 以 `.proto` 作为服务契约源头

API 先写 OpenSpec scenario，再写 `.proto`，最后生成服务端/客户端代码。这样 AI、代码和文档共享同一个契约，不靠聊天上下文记忆。

### 3. 数据层采用 SQL-first + sqlc

sqlc 让 schema/query 成为事实来源，生成类型安全 Go 代码。它比 ORM 更透明，更适合一人公司排查生产问题；动态查询必须在 design 中说明。

### 4. 服务层只适配协议，业务放入 biz

`internal/service` 只处理请求校验、调用 usecase、映射响应和错误。业务规则放 `internal/biz`，数据库细节放 `internal/data`，避免 transport 和 storage 污染核心逻辑。

### 5. 运维信号从第一天最小化内建

只要求 health check、结构化日志、四个黄金信号落点和优雅关闭。不在阶段 2 引入完整告警平台，避免平台工作吞掉产品开发。

## 取舍

- gRPC first 会提升服务间契约稳定性，但对浏览器/第三方集成需要 HTTP 兼容层，后续应单独规范 gateway/HTTP。
- sqlc 要求手写 SQL，早期会慢一点，但减少运行时 ORM 魔法。
- PostgreSQL 是默认生产数据库，但仍允许按项目场景改用 MySQL/SQLite。
- 质量门禁少而明确，牺牲了全面性，换取一人公司能稳定执行。

