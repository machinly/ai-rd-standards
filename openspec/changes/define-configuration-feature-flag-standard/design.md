# 设计：配置、环境、Feature Flag 与运行时变更规范

## 设计决策

### 1. 配置注册表记录事实，不记录 secret 值

`config/registry` 记录 key、类型、来源、环境、验证、敏感性、是否暴露给客户端、是否需要重启和回滚方式。secret 只记录引用和管理方式，真实值必须留在 secret manager、环境或部署平台。

### 2. Feature Flag 独立于普通配置

普通配置多在部署或启动时生效，Feature Flag 是运行时行为开关。二者混在一起会导致生命周期、审计和回滚混乱，因此 `config/flags` 单独记录 category、targeting、fail behavior、observability 和 cleanup plan。

### 3. 运行时变更必须追加日志

一人公司常见问题是“我昨天改了什么”。`runtime-changes` 用 JSONL 记录生产或准生产变更事实，便于事故回溯和回滚，不替代发布流水线。

### 4. 前端配置默认不可信

Vite client env 会进入浏览器 bundle，不能放 secret。前端 flag 只控制展示，权限、计费、租户隔离必须由后端 enforcement。

### 5. AI route 是高风险配置

模型、provider、prompt variant、tool iteration、safety threshold 和 retrieval index 都会改变 AI 行为和成本。运行时切换必须连接 eval、成本 guardrail、fallback 和 rollback。

### 6. 人只判断高影响 runtime 变更

模板和脚本负责字段、过期、敏感值、Vite 前缀、flag 生命周期和运行时日志检查。人只判断生产变更、敏感配置、前端暴露、长期 flag、AI route 和 kill switch。

## 取舍

- JSON/Markdown 工件比配置平台轻，适合早期一人公司。
- 不默认动态配置中心，避免引入新运行时依赖。
- 不追求所有开发变量都登记，只登记会影响生产行为、用户体验、安全、成本或 AI 行为的配置。
- 简单脚本不能替代云平台审计，但能防止最常见的泄密、过期 flag 和无回滚配置。
