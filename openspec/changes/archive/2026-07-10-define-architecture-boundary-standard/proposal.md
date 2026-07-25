# 提案：定义架构决策、代码组织与模块边界规范

## 意图

为一人公司建立轻量架构边界基线，让生产服务、前端应用和用户可见 AI workflow 能记录重要架构决策、模块职责、依赖方向、API/data/AI 边界和例外人审点，避免代码组织随时间滑向大泥球。

## 范围

- 定义 `architecture/decisions`、`architecture/boundaries`、`architecture/module-maps`、`architecture/dependency-rules` artifacts。
- 定义 ADR、bounded context、module map、dependency rules 的字段和默认模板。
- 定义 Go/Kratos/sqlc/gRPC 后端结构、Vite 前端结构和 AI workflow 边界默认值。
- 定义新增服务、shared package、数据所有权、API contract、agent runtime 和 dependency exception 的人工 checkpoint。
- 创建架构边界落地 skill 和检查脚本。

## 不做

- 不引入大型企业架构流程。
- 不强制完整 C4/UML 图。
- 不默认微服务拆分。
- 不替代 W4 后端/前端、W3 AI、W2 auth/security、W5 testing 规范。

## 依据

- 《人月神话》：概念完整性和系统一致性优先。
- 小型项目管理：只记录高影响决策和可恢复上下文。
- D. L. Parnas, On the Criteria To Be Used in Decomposing Systems into Modules。
- Michael Nygard, Documenting Architecture Decisions；Thoughtworks Lightweight ADR。
- C4 Model。
- Domain-Driven Design / Bounded Context。
- Alistair Cockburn, Hexagonal Architecture / Ports and Adapters。
- Go module layout、Go `internal` packages、Kratos layout。
- Vite / React file structure guidance。
- OpenAI prompt engineering / Agents docs。
- Google SRE Simplicity。

## 需要人的判断

建议默认：任何影响依赖方向、数据所有权、API contract、AI tool boundary、shared package、服务拆分或新框架/供应商的变更，必须有 architecture boundary artifacts。接受 dependency exception 或架构锁定时必须有人审记录。
