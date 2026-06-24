# 提案：定义 Go/Kratos/sqlc/gRPC 服务端研发规范

## 意图

为一人公司建立默认服务端落地路径，让后端研发从 OpenSpec 需求开始，稳定落到 Go、Kratos、Protobuf/gRPC、sqlc、测试和最小运维信号上。

## 范围

- 定义新服务目录结构和分层职责。
- 定义 Protobuf/gRPC API 设计规则。
- 定义 sqlc 数据访问规则。
- 定义服务端实现顺序和质量门禁。
- 定义服务上线前最小健康检查和观测要求。
- 创建服务端落地 skill，降低重复操作成本。

## 不做

- 不创建真实业务服务代码。
- 不定义完整云部署、CI/CD、告警和值班体系。
- 不展开认证、多租户、计费或事件架构。
- 不定义前端 Vite 规范。

## 依据

- 《人月神话》：避免银弹幻觉，控制偶然复杂度。
- 小型项目管理：只保留小项目真正需要的计划和检查点。
- Kratos 官方文档与 layout：Protobuf-first、HTTP/gRPC 生成、middleware、config、logging、metrics、tracing、默认分层。
- gRPC/Protobuf 官方文档：`.proto` 定义服务、生成代码、deadline、health checking、兼容演进。
- sqlc 官方文档：schema/query/config 生成类型安全 Go 代码，使用 `sqlc vet` 检查查询。
- Google SRE：简单性、可重复发布、四个黄金信号。

## 需要人的判断

本阶段只有一个建议默认值：新生产服务默认 PostgreSQL + sqlc，不引入 ORM。若用户明确偏好其他数据库，再改规范。

