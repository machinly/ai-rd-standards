# 实现：配置、Feature Flag 与前端 env

## 规范要求

<!-- rule-id: IMPL-CODE-CONFIG-FLAG-SEPARATION -->
- 代码、配置与 Feature Flag 须分开记录：配置只决定部署差异，Feature Flag 只决定运行时行为。

<!-- rule-id: IMPL-CONFIG-ARTIFACT-PATHS -->
- 配置工件缺省位于 `config/environments/<target>.md`、`config/flags/<target>.json` 与 `config/runtime-changes/<target>.jsonl`。

<!-- rule-id: IMPL-CONFIG-ENVIRONMENT-FIELDS -->
- 配置注册表及每个 config item 都须记录适用的 `environments`。

<!-- rule-id: IMPL-ENVIRONMENT-MATRIX-SECTIONS -->
- 环境矩阵须包含 `Scope`、`Environments`、`Config Sources`、`Secrets Sources`、`Differences`、`Promotion Path`、`Validation`、`Rollback` 与 `Human Checkpoints`。

<!-- rule-id: IMPL-PRODUCTION-ENVIRONMENT-SET -->
- 系统进入生产后，环境矩阵至少记录 `local`、`preview` 或 `staging` 二者之一，以及 `production`。

<!-- rule-id: IMPL-FLAG-CATALOG-SCHEMA -->
- Feature Flag 清单须包含 `target`、`flags`、`provider`、`defaults`、`cleanup_policy`、`human_checkpoint` 与 `review_cadence`。

<!-- rule-id: IMPL-FLAG-ITEM-SCHEMA -->
- 每个 flag 须记录 `key`、`type`、`category`、`created_on`、`expires_on` 或 `review_on` 二者之一、`default`、`fail_behavior`、`targeting` 与 `cleanup_plan`。

<!-- rule-id: IMPL-SHORT-LIVED-FLAG-EXPIRY -->
- release 和 experiment flag 须有 `expires_on`。

<!-- rule-id: IMPL-LONG-LIVED-FLAG-REVIEW -->
- ops、permission 与 kill_switch flag 至少须有 `review_on`。

<!-- rule-id: IMPL-ALL-FLAGS-CLEANUP-PLAN -->
- 所有 flag 都须有 cleanup plan。

<!-- rule-id: IMPL-RUNTIME-CHANGE-LOG-SCHEMA -->
- runtime change 日志须包含 `date`、`target`、`environment`、`change_type`、`key`、`actor`、`reason`、`result` 与 `rollback`。

<!-- rule-id: IMPL-GO-TYPED-CONFIG -->
- Go 配置须使用类型化 struct，禁止在业务代码中散落 `os.Getenv`。

<!-- rule-id: IMPL-LOOKUPENV-WHEN-EMPTY-DIFFERS -->
- 需要区分“未设置”和“空值”时，使用 `os.LookupEnv`。

<!-- rule-id: IMPL-KRATOS-CONFIG-BOUNDARY -->
- Kratos config 负责加载、watch 与 decode；业务层只接收已校验的配置对象。

<!-- rule-id: IMPL-CONFIG-FAIL-FAST-EXCEPTION -->
- 关键配置或未明确可降级的配置加载失败时须 fail fast；只有明确可降级的非关键配置例外。

<!-- rule-id: IMPL-RELOADABLE-CONFIG-CONTRACT -->
- reloadable 配置须说明 reload 范围、验证方式与失败回退。

<!-- rule-id: IMPL-VITE-ENV-NONSENSITIVE -->
- 进入浏览器 bundle 的 env 必须是非敏感信息。

<!-- rule-id: IMPL-VITE-ENV-PREFIX -->
- 客户端变量须使用 `VITE_` 前缀，或项目明确配置的 `envPrefix`。

<!-- rule-id: IMPL-RUNTIME-PUBLIC-CONFIG-ENDPOINT -->
- 前端需要运行时动态配置时，须使用后端只读 public config endpoint，并记录缓存和回滚。

<!-- rule-id: IMPL-FRONTEND-FLAG-UI-ONLY -->
- 前端 flag 只能控制 UI exposure，不能作为服务端权限或权益裁决。

<!-- rule-id: IMPL-RELEASE-FLAG-EXPIRY -->
- release toggle 只用于短期隐藏能力，并须有 `expires_on`。

<!-- rule-id: IMPL-EXPERIMENT-FLAG-CRITERIA -->
- experiment toggle 须有 success criteria、stop criteria 与 cleanup。

<!-- rule-id: IMPL-MIGRATION-FLAG-ROUTE -->
- migration toggle 须进入数据迁移规范处理。

<!-- rule-id: IMPL-EXPIRED-FLAG-REMOVAL -->
- 过期 flag 须删除代码路径与配置，禁止以“以后可能用”为由保留。

<!-- rule-id: IMPL-AI-CONFIG-COST-ROLLBACK -->
- AI 配置变更须链接成本 guardrail 与 rollback。

<!-- rule-id: IMPL-AI-ROUTE-FLAG-FIELDS -->
- AI route flag 须记录 `default`、`fallback` 与 `fail behavior`。

<!-- rule-id: IMPL-PRODUCTION-CONFIG-HUMAN-GATE -->
- 生产配置或 Feature Flag 变更须交由人工判断。

<!-- rule-id: IMPL-SENSITIVE-CONFIG-HUMAN-GATE -->
- 敏感配置的新增、迁移或轮换窗口须交由人工判断。

<!-- rule-id: IMPL-LONG-LIVED-FLAG-HUMAN-GATE -->
- 长期保留某个 flag 须交由人工判断。

<!-- rule-id: IMPL-FRONTEND-ENV-HUMAN-GATE -->
- 向前端暴露环境变量须交由人工判断。

<!-- rule-id: IMPL-AI-RUNTIME-SWITCH-HUMAN-GATE -->
- 在运行时切换 AI model、provider 或 prompt route 须交由人工判断。
