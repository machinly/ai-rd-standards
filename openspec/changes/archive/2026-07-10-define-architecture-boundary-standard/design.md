# 设计：架构决策、代码组织与模块边界规范

## 设计决策

### 1. ADR 只记录架构显著决策

一人公司不需要每个实现细节都写 ADR。只有影响结构、依赖、接口、数据、非功能约束、构建、部署或供应商锁定的决策才写。ADR 保留 context、decision 和 consequences，服务未来恢复上下文。

### 2. Boundary JSON 给脚本检查，Module map 给人阅读

`architecture/boundaries` 用 JSON 表达 target、modules、依赖方向、API/data/AI 边界。`module-maps` 用 Markdown 解释系统形状。这样既能自动检查，也能让人快速恢复系统意图。

### 3. Dependency rules 用局部规则，不做全仓库复杂静态分析

第一版只检查 import 文本中的 forbidden patterns，足以发现 domain import data、feature 私自跨界、AI workflow 直连生产 writer 等一人公司常见问题。复杂依赖图工具后续按需要引入。

### 4. 默认 modular monolith，谨慎微服务

用户偏好是 Go/Kratos/gRPC，但一人公司不应把每个 bounded context 都立刻拆成服务。默认在一个服务内建立清晰模块边界，只有数据所有权、发布节奏、可靠性隔离或安全边界明确时拆服务。

### 5. 使用技术栈自带边界

Go 的 `internal`、Kratos layout、Protobuf API、sqlc repository adapter、Vite feature folders、OpenAI prompt builder in code 都是已有边界机制。规范优先组合这些机制，不另造框架。

### 6. AI workflow 作为架构边界一等对象

AI prompt、tool、agent runtime、eval 和数据访问不能散落在全局工具包。AI workflow 必须有 owner、tool port、权限、成本、数据和审批边界。

## 取舍

- 增加少量架构工件，但避免长期代码耦合带来的高额改动成本。
- 不强制完整图形建模，降低维护成本。
- 不默认 monorepo 多 module 或微服务，避免早期复杂化。
- 简单 import 扫描可能漏掉动态依赖，但能低成本发现最常见边界破坏。
