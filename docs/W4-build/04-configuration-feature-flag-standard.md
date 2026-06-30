# W4 Build 触发专项：配置、环境、Feature Flag 与运行时变更规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及配置注册表、环境差异、Feature Flag、kill switch、运行时变更、前端公开 env 或 AI route/runtime 参数时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/00-main.md`，由主入口判断是否触发本专项。

## 目标

一人公司常见事故不一定来自代码错误，而是来自配置漂移、环境差异、开关长期遗留、运行时改动无人记录、前端误暴露密钥或 AI 模型参数悄悄变化。本专项定义最小配置与运行时变更规范，让配置、环境、Feature Flag、kill switch 和运行时变更可审查、可回滚、可清理。

默认原则：代码决定能力边界，配置决定部署差异，Feature Flag 决定运行时行为；三者必须分开记录，不把配置当秘密仓库，不把 flag 当永久产品策略。

## 核心依据

- 《人月神话》：复杂度会从代码转移到配置。配置不是银弹，必须保持概念完整性。
- 小型项目管理：只记录会影响生产行为、成本、安全或用户体验的配置，不维护重型 CMDB。
- Twelve-Factor App Config / Dev-Prod Parity：配置应和代码分离，环境差异应最小化且明确。
- Google SRE Configuration Design：好的配置接口应能快速、可信、可测试地修改；配置复杂度会增加人的认知负担和生产风险。
- Google SRE Configuration Specifics / Progressive Rollouts：配置变更也有风险，应有位置、验证、回滚、分阶段 rollout 和 toil 控制。
- Martin Fowler Feature Toggles：Feature Toggle 能不改代码改变行为，但会增加复杂度；必须按 toggle 类型管理生命周期。
- OpenFeature：Feature Flag evaluation、evaluation context、provider 边界应 vendor-neutral，默认值和错误行为必须明确。
- Kratos Config：微服务配置应与代码分离，运行时从文件、环境或配置中心加载。
- Vite Env and Modes：Vite 只向客户端暴露带指定前缀的 env；这些值会被静态替换进前端 bundle。
- gRPC Service Config：超时、重试、hedging、负载均衡等运行时行为属于高风险配置，需要明确默认值和回滚。

## 范围

适用对象：

- Go/Kratos 服务配置、gRPC client/service config、sqlc 数据库连接参数。
- Vite 前端环境变量、public runtime config、feature exposure。
- AI model、prompt variant、tool limit、token limit、provider、temperature、routing。
- Feature Flag、kill switch、experiment toggle、ops toggle、permission toggle。
- 生产、preview/staging、本地环境差异。

不适用对象：

- 纯代码常量且不会因环境变化。
- 不进入生产的一次性脚本参数。
- secret 值本身。secret 只记录引用、来源、权限和轮换，不记录真实值。

## 最小工件

每个生产服务、前端应用或 AI workflow 使用同一个 `<target>` 文件名：

```text
config/
  registry/<target>.json
  environments/<target>.md
  flags/<target>.json
  runtime-changes/<target>.jsonl
  runbooks/<target>.md
```

### `config/registry/<target>.json`

配置注册表用于记录配置项事实，不存真实 secret 值。必须包含：

- `target`、`owner`、`stack`
- `environments`
- `config_items`
- `secrets_policy`
- `validation`
- `startup_checks`
- `reload_policy`
- `drift_detection`
- `human_checkpoint`
- `review_cadence`

每个 `config_items` 条目必须包含：

- `key`
- `type`
- `owner`
- `source`：env、config_file、secret_manager、config_center、build_time、feature_flag。
- `environments`
- `required`
- `default`
- `validation`
- `sensitive`
- `client_exposed`
- `restart_required`
- `rollout`
- `rollback`

默认：生产配置必须有 validation 和 rollback；敏感配置不得记录真实值；前端 client exposed 配置不得敏感。

### `config/environments/<target>.md`

环境矩阵给人读，必须包含：

- `Scope`
- `Environments`
- `Config Sources`
- `Secrets Sources`
- `Differences`
- `Promotion Path`
- `Validation`
- `Rollback`
- `Human Checkpoints`

默认至少记录 local、preview/staging、production 三类，除非产品还未进入生产。

### `config/flags/<target>.json`

Feature Flag 清单必须包含：

- `target`、`owner`
- `flags`
- `evaluation_context`
- `provider`
- `defaults`
- `cleanup_policy`
- `observability`
- `human_checkpoint`
- `review_cadence`

每个 flag 必须包含：

- `key`
- `type`
- `category`：release、experiment、ops、permission、kill_switch、migration、ai_model_route。
- `owner`
- `created_on`
- `expires_on` 或 `review_on`
- `default`
- `fail_behavior`
- `targeting`
- `rollout_plan`
- `observability`
- `cleanup_plan`

默认：release 和 experiment flag 必须有 `expires_on`；ops、permission、kill_switch 至少有 `review_on`；所有 flag 必须有 cleanup plan。

### `config/runtime-changes/<target>.jsonl`

记录生产或准生产运行时配置变更：

```json
{"date":"2026-06-24","target":"ai-assistant","environment":"production","change_type":"feature_flag","key":"brief_export_enabled","actor":"solo-founder","reason":"enable 10 percent beta rollout","result":"success","rollback":"set flag false"}
```

禁止记录真实 secret、token、password、connection string、用户邮箱或手机号。

### `config/runbooks/<target>.md`

运行手册必须包含：

- `Scope`
- `Change Procedure`
- `Validation`
- `Rollback`
- `Kill Switch`
- `Drift Detection`
- `Human Checkpoints`

默认所有生产配置变更都要有 rollback。高风险开关要有 kill switch 或明确说明不适用。

## Go / Kratos 默认规则

- 配置 struct 必须类型化，避免在业务代码中散落 `os.Getenv`。
- `os.LookupEnv` 比 `os.Getenv` 更适合区分“未设置”和“空值”。
- Kratos config 负责加载、watch 和 decode；业务层只接收已校验的配置对象。
- 配置加载失败应 fail fast，除非是明确可降级的非关键配置。
- reloadable 配置必须说明 reload 范围、验证方式和失败回退。
- gRPC timeout、retry、hedging、load balancing、circuit breaker 属于高风险配置，生产变更需要 test run 或 smoke。

## Vite 前端默认规则

- 所有会进入浏览器 bundle 的 env 必须是非敏感信息。
- Vite 暴露到客户端的变量必须遵守 `VITE_` 前缀或项目明确配置的 `envPrefix`。
- 不把 API key、service token、数据库 URL、OpenAI key、JWT secret 放进 Vite env。
- `import.meta.env` 是 build-time 替换；需要运行时动态配置时，使用后端提供的只读 public config endpoint，并记录缓存和回滚。
- 前端 flag 只控制 UI exposure；权限、计费、租户隔离必须由后端再次检查。

## Feature Flag 默认规则

- Release toggle：短期隐藏未完成或高风险能力，必须有 expires_on。
- Experiment toggle：连接 W1 Discovery 产品实验，有 success/stop criteria 和 cleanup。
- Ops toggle / kill switch：用于降级、关闭高成本或高风险路径，必须有 runbook。
- Permission toggle：表达套餐、授权或租户能力，必须进入 auth boundary。
- Migration toggle：配合数据迁移双写/双读，必须进入数据迁移规范。
- AI model route：切换模型、provider、prompt variant 或 tool route，必须进入 AI eval、成本和安全边界。

默认：flag 数量越少越好。过期 flag 必须删除代码路径和配置，不允许“先留着”。

## AI 配置默认规则

- model、temperature、max tokens、tool iteration、provider、prompt version、retrieval index、safety threshold 都是生产行为配置。
- AI 配置变更必须链接 eval run、成本 guardrail 和 rollback。
- AI provider/model route flag 需要记录 default、fallback、fail behavior 和 observability。
- 不允许运行时把用户输入拼成未校验的 prompt/config key。

## 需要人判断的关键点

只把这些配置判断交给人：

- 是否允许生产配置或 Feature Flag 变更。
- 是否允许敏感配置新增、迁移或轮换窗口。
- 是否允许长期保留某个 flag。
- 是否允许前端暴露某个环境变量。
- 是否允许 AI model/provider/prompt route 运行时切换。
- 是否触发 kill switch、降级、回滚或继续 rollout。

其他字段由 Codex 先按模板创建，并由脚本检查。

## Review 1：一人公司注意力审查

- 保留：配置注册表、环境矩阵、flag 清单、runtime change log、runbook 五类工件足够恢复上下文。
- 保留：只把生产变更、敏感配置、前端暴露、AI route、flag 过期例外交给人。
- 调整：不引入商业 feature management 平台作为默认，早期 JSON + runbook 足够。
- 调整：不要求所有本地开发变量都登记，只登记影响生产或用户行为的配置。
- 风险：flag 清理容易被拖延。缓解：release/experiment flag 强制 expires_on，脚本报错。

结论：可落地。该阶段把配置变更从“记在脑子里”转为“可测试、可回滚、可清理”的最小流程。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：experiment flag 必须连接 W1 Discovery 实验，不让开关替代产品决策。
- 工程角度：Go/Kratos/Vite/gRPC 都有明确配置边界，避免配置散落。
- 运维角度：配置变更也走 rollout、smoke、runtime log 和 rollback，符合 SRE 风险控制。
- 安全隐私角度：secret 不进仓库，Vite client env 不得敏感，evaluation context 不记录不必要个人数据。
- 成本角度：AI model route、tool limit 和高成本功能必须可关闭、可观测、可回滚。

结论：可落地。本专项补上了运行时行为控制层，和发布、安全、成本、AI eval 规范互相衔接。
