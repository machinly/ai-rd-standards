# 可选个人技术栈偏好

本文件不是研发流程，也不因 `$opc-rd` 被调用而自动生效。只有用户明确要求采用这些个人偏好、且当前仓库没有自己的技术决定时才读取；项目事实和用户当前选择始终优先，偏离本文件不需要例外审批。

## 应用与目录

- 新应用优先从官方或已批准、可版本化的模板生成。
- 单应用仓库可以直接使用仓库根；多应用仓库先声明各应用根，再把服务和前端放入清晰、互不混淆的目录。
- 多组件项目提供一个可重复的本地集成入口，能够启动实际需要的应用和依赖并完成 smoke check。

## 后端与数据

- 新后端优先 Go；需要完整服务框架时优先 go-kratos。
- API 契约优先 Protobuf；服务间通信可优先 gRPC，浏览器、webhook 或公共兼容场景再暴露 HTTP。
- 关系数据优先 MySQL 与清晰 SQL；Go 数据访问可优先 sqlc。
- 默认不依赖 foreign key 时，用事务、约束、幂等、删除策略、补偿和一致性检查承担完整性。

## 前端

- 新前端优先小型 Vite 脚手架；已有框架则沿用。
- UI 保持清晰排版、可访问语义、稳定 token 和少装饰噪音，不把某一视觉品牌当成强制标准。

## AI

- 规则或普通代码能解决时不引入模型；单次调用足够时不升级为复杂 workflow。
- 生产 prompt、模型设置或工具行为变化应可版本化，并用与风险相称的样例或 eval 验证。
- 外部内容按不可信数据处理；真实写操作遵守最小权限、明确授权和可恢复边界。

## 参考

- Kratos: https://go-kratos.dev/docs/
- sqlc: https://docs.sqlc.dev/
- gRPC Go: https://grpc.io/docs/languages/go/
- Vite: https://vite.dev/guide/
- OpenAI evals: https://developers.openai.com/api/docs/guides/evaluation-best-practices
