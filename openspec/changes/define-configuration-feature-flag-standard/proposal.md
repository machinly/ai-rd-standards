# 提案：定义配置、环境、Feature Flag 与运行时变更规范

## 意图

为一人公司建立可检查的配置与运行时变更基线，让生产配置、环境差异、Feature Flag、kill switch、AI model route 和运行时变更都有 owner、验证、回滚、清理和人审点，降低配置漂移、前端泄密、过期 flag、无记录生产改动和 AI 行为悄悄变化的风险。

## 范围

- 定义 `config/registry`、`config/environments`、`config/flags`、`config/runtime-changes`、`config/runbooks` artifacts。
- 定义 Go/Kratos、Vite、gRPC、AI workflow 的配置边界和默认规则。
- 定义 Feature Flag 类型、生命周期、evaluation context、fail behavior、cleanup 和 observability。
- 定义生产配置变更、敏感配置、前端暴露、AI route、长期 flag、kill switch 的人工 checkpoint。
- 创建配置和 flag 落地 skill 与检查脚本。

## 不做

- 不采购或绑定商业 feature management 平台。
- 不把 secret 值写入仓库。
- 不建立重型 CMDB。
- 不替代阶段 6 发布流水线、阶段 8 auth、阶段 9 成本、阶段 10 安全、阶段 11 产品实验和阶段 12 测试规范。

## 依据

- 《人月神话》：配置复杂度也是复杂度，必须保持概念完整性。
- 小型项目管理：只记录高影响配置和可恢复上下文。
- Twelve-Factor App Config / Dev-Prod Parity。
- Google SRE Configuration Design、Configuration Specifics、Progressive Rollouts。
- Martin Fowler Feature Toggles。
- OpenFeature specification。
- Kratos Config、Vite Env and Modes、gRPC Service Config。

## 需要人的判断

建议默认：任何生产配置变更、敏感配置新增/迁移、前端 client-exposed env、新 Feature Flag、AI model/provider route、kill switch 或长期 flag 例外，都必须有人审记录和 rollback。
