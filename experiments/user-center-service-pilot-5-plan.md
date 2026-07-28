# 用户服务第五轮研发规范实验方案：Design-First Vertical Delivery

状态：`draft-awaiting-review`；本文获用户明确确认后只授权产品定义与 UX 设计，不授权立即写代码。
日期：2026-07-27
目标仓库：`D:\Workspace\user` 现有 Git 仓库；第五轮使用用户指定的新基线，不恢复历史实现。
权威边界：本文是第五轮实验方案和编码前状态记录；UX 设计由本文链接的唯一 `ux/` 目录承载；进入实现后由唯一 OpenSpec `tasks.md` 承载任务状态。三者不复制彼此内容。

## 1. 路由与本轮性质

- R&D applicability：适用。本轮直接决定并实现用户服务的产品、体验、技术和验收边界。
- Work mode：`Deliver`。前四轮已经给出足够清楚的目标用户、核心价值和最小行为，本轮不是先写代码寻找需求的 Prototype。
- Deliver route：`Standard`。本轮只使用本地合成数据、Mock provider 和可重建环境，无生产、真实用户、真实凭据或外部副作用；同时它跨多个应用并改变用户可见行为，需要 OpenSpec、可视 UX 和独立终审。
- `visual_ux: required`。本轮改变登录、第一方应用访问、管理员搜索/禁用和禁用反馈等关键任务。
- OpenSpec：产品定义和 UX 获得人工确认后、任何生产性代码前创建。
- 风险升级：一旦需要真实 provider、真实个人或财务数据、生产管理员、真实通知、外部系统、公开承诺或不可逆动作，立即停止并重新路由为 High-risk；不得沿用本方案的轻量本地授权。

第五轮只继承前四轮已经验证的产品需求和流程反例，不继承任何旧任务列表、代码进度、session 状态、OpenSpec、数据库、配置或治理结论。执行顺序、应用切分、门禁和任务图全部以本文重新开始。

## 2. 从前四轮继承什么

| 来源 | 继承的稳定事实 | 第五轮的处理 |
| --- | --- | --- |
| 第一轮 | 用户服务要提供稳定内部身份、可插拔 provider、第一方服务 API、独立管理边界和两个独立前端 | 保留为产品方向，但只选择一条可验收纵向增量 |
| 第一轮失败 | work brief 不能替代产品定义；模板、完整本地环境和浏览器证据缺失 | 产品定义、UX、模板路径和证据层级均设为显式门禁 |
| 第二轮 | 项目地图、统一本地入口、命令登记和最新失败否决旧结论有价值 | 使用单一项目地图和单一当前状态，不按治理文件数量判定成功 |
| 第二轮失败 | 人工浏览器检查曾被夸大为 Browser E2E；多轮 review 没阻止不可用页面 | 人工 showcase 与自动 Browser E2E 分开命名，验收使用真实页面业务动作 |
| 第三轮 | `services/user-center/`、`web/user/`、`web/admin/` 的多应用形状可用；Alice/Bob/Admin 是可理解 fixture | 固化应用根，继续用人类产品语言验收 |
| 第三轮失败 | 46.7 小时、102 次提交和 74 份流程文件仍只通过 1 条旅程；展示太晚 | 最多 5 个 active tasks；按纵切片展示；不为每个微步骤新增 plan/spec/review |
| 第四轮方案 | Alice 登录、Finance 记账、Admin 按姓名禁用、Alice 被拒绝且 Bob 不受影响，是合适的最小业务闭环 | 保留这条业务闭环，但改成设计先行的稳定交付，不使用单根 `internal/` 的临时形状 |
| 第四轮暴露的规范缺口 | 编码前没有 Product Definition / UX approval 硬门；服务内部目录未绑定具体应用根 | 增加两道人工门和仓库根—应用根目录合同 |

## 3. Product Definition 候选

本节是待用户审查的产品定义，不因本文落盘自动视为批准。

### 3.1 目标用户与结果

- **Alice / Bob：第一方应用用户。** 通过统一身份登录后能识别自己的账号，并在第一方 Finance Demo 中完成一项简单任务。
- **Admin：内部账号支持管理员。** 能以独立身份入口按人类可读信息找到目标用户，并以可审计理由禁用该用户。
- **第一方业务开发者：用户服务消费者。** 能依据用户服务签发的稳定内部身份和状态决定访问，不建立第二套用户账号。

本轮要改善的结果是：身份服务不只“返回一个 ID”，而是让第一方应用可靠识别用户，并让独立管理员的状态控制能准确、可理解地传递到该应用。

### 3.2 Selected increment

本轮只交付以下闭环：

1. Alice 通过 Mock OIDC 登录，用户端显示 `Alice` 和稳定内部身份所对应的可理解资料；
2. Alice 进入第一方 Finance Demo，通过页面创建 `42.50 / Groceries / Lunch` 支出并看到结果；
3. Admin 从独立入口登录，按显示名 `Alice` 搜索，输入理由 `pilot 5 review` 并确认 Disable；
4. Alice 再次进入 Finance Demo 时由服务端拒绝，并看到可理解的禁用状态与下一步；
5. Bob 仍能登录并访问自己的空账本，证明没有禁用错误对象；
6. reset/reseed 后整条旅程可以重复。

### 3.3 产品范围

本轮包含：

- 一个 Mock OIDC provider，提供 Alice、Bob 和 Admin 合成身份；
- provider subject 到稳定内部 `user_id` 的映射，内部 ID 不直接等于 provider subject；
- 用户基础资料和 `active | disabled` 最小状态；
- 用户 session，以及禁用后现有访问失效的明确语义；
- 固定登记的第一方 Finance Demo client、audience 与最小 scope；
- 用户服务只拥有身份、账号状态和粗粒度第一方 scope；
- Finance Demo 拥有支出记录及其资源权限，不读取用户服务数据库；
- Admin 独立入口、独立 session/token audience、按显示名搜索、带理由禁用和最小审计；
- 用户端、管理端和 Finance Demo 三个独立前端应用；
- 单一宿主端口的本地 gateway，以及可重复的 up/wait/reset/showcase/e2e/down 命令。

### 3.4 明确不做

- 真实微信、QQ、支付宝、Google、Firebase 或其他 provider；
- 真实用户、真实财务数据、真实凭据、生产部署、邮件、短信或外部通知；
- 多身份绑定/解绑、账号合并、找回、MFA/passkey、设备管理、导出和删除传播；
- 组织/租户、公开第三方 API、自助 client 注册、复杂 RBAC/ABAC；
- 完整家庭、成员、邀请、账户、分类体系、报表、多币种、银行同步、支付或金融建议；
- 完整安全、并发、恢复、监控和发布矩阵；只有当前闭环真实命中的最低控制进入本轮；
- 把本地合成结果描述为 provider sandbox、production-ready 或通用 IAM。

以上非范围保留为 `Later`，不是第五轮的隐含承诺。

### 3.5 产品成功与失败

产品成功必须由观察者从真实页面完成并理解整条 selected increment；内部 ID、日志、数据库行、API 200、单元测试数量或口头解释不能替代。

以下任一情况使产品验收失败：

- 页面只显示固定 `User`、opaque ID 或无法区分 Alice/Bob 的内容；
- Admin 只能按内部 ID 找人，或搜索 `Alice` 不能得到清楚结果；
- Disable 只影响前端按钮，不由服务端执行访问拒绝；
- Alice 被禁用时 Bob 也受影响；
- Finance 直接相信浏览器提交的 `user_id`，或跨库读取用户服务数据；
- reset 后旅程不能重放；
- 证据依赖手工改库、内部函数或日志才能成立。

### 3.6 Product Definition 人工门

用户必须明确确认以下整体决定：目标用户与结果、selected increment、范围、非范围、成功/失败标准，以及“本轮仅本地合成、第一方、无真实 provider/生产”的风险边界。

在确认前，执行者只可：

- 整理本节并提出最多 3 个真正影响产品方向的问题；
- 更新本文中的候选定义和 review 记录；
- 不得创建或修改 `go.mod`、`package.json`、`internal/`、`src/`、API、数据库、脚本或运行代码。

Product review：`pending`。Decision owner：用户。批准不得从沉默、一般授权或“开始实验”推断。

## 4. UX Design 人工门

Product Definition 明确批准后，才开始 UX Design。UX 必须先形成静态、无业务脚本、无真实 API 的可视工件，再请求用户单独确认。

唯一 UX 目录：`ux/build-user-service-vertical-slice-pilot-5/`，至少包含：

- `flow.md`：目标、入口、Alice/Admin/Bob 正常路径、retry/cancel/exit、non-goals 和线框索引；
- `surface-map.md`：`oidc`、`user`、`finance`、`admin`、`disabled` 五个 surface 的关系；
- `wireframes/<surface>--<state>.html|svg`：按适用范围覆盖 `success`、`loading`、`empty`、`error` 和 `disabled`；
- `review.md`：Decision owner、Reviewed at、Artifacts reviewed、Decision 与 Notes。

UX 必须让用户能判断：

1. Alice 从哪里登录、如何知道登录的是自己、如何进入 Finance；
2. 空账本如何引导创建第一笔支出，提交中、成功和失败如何表达；
3. Admin 如何按姓名搜索、区分结果、理解 Disable 的对象与后果、填写理由并确认；
4. Alice 被禁用后看到什么、能做什么、不会看到什么；
5. Bob 的正常状态如何与 Alice 的禁用状态形成清楚对照；
6. 键盘顺序、可见焦点、WCAG 2.2 AA 对比度和状态不只依赖颜色的基线。

UX review 必须由用户写出或明确给出 `approved`。在 `review.md` 为 `approved` 前，禁止进行 Technical Design、OpenSpec 或任何应用代码生成。批准后若任务路径、信息架构、状态、权限含义或确认方式发生实质变化，必须更新 UX 并重新审批。

UX review：`not-started`。

## 5. Technical Design 与目录合同门

Product Definition 和 UX 都批准后，才允许形成技术设计。技术设计写入本轮唯一 OpenSpec `design.md`，不得另建 Superpowers spec 或平行架构文档。

### 5.1 仓库模式

第五轮固定为 `multi-application`。`governance/project-map.json` 必须在模板生成前登记每个应用的 `id`、`kind`、`path` 与 `manifest`。

目标目录为：

```text
D:\Workspace\user\
├─ README.md
├─ go.work                         # 只有确需协调两个 Go module 时使用；不是业务 module
├─ services\
│  ├─ user-center\
│  │  ├─ go.mod
│  │  ├─ api\
│  │  ├─ cmd\user-center\
│  │  ├─ configs\
│  │  ├─ internal\server\
│  │  ├─ internal\service\
│  │  ├─ internal\biz\
│  │  ├─ internal\data\
│  │  ├─ internal\conf\
│  │  ├─ migrations\
│  │  ├─ queries\
│  │  └─ sqlc.yaml
│  └─ finance-demo\
│     ├─ go.mod
│     ├─ api\
│     ├─ cmd\finance-demo\
│     ├─ configs\
│     ├─ internal\...
│     ├─ migrations\
│     ├─ queries\
│     └─ sqlc.yaml
├─ web\
│  ├─ user\
│  ├─ admin\
│  └─ finance\
├─ ux\build-user-service-vertical-slice-pilot-5\
├─ e2e\pilot-5\
├─ deploy\
├─ scripts\
├─ governance\
└─ openspec\
```

以下路径禁止出现在聚合仓库根：

- `internal/`、`cmd/`、`api/`、`configs/`、`migrations/`、`queries/`、`src/`、`sqlc.yaml`；
- 属于某个业务应用的根级 `go.mod` 或 `package.json`。

仓库级 `go.work`、`pnpm-workspace.yaml` 或仅负责编排的 workspace manifest 可以位于根，但必须在项目地图中说明用途，不能承载某个应用的业务代码。

模板命令必须显式生成到已声明的空应用根。禁止先在仓库根生成再移动，禁止手工搭目录后声称来自模板。每次生成后立即运行：

```powershell
python D:\Workspace\研发规范\tools\verify_project_evidence.py D:\Workspace\user --application-layout-only --json
```

目录门失败时停止，不通过“稍后整理目录”继续写业务代码。

### 5.2 系统边界

- Gateway 只暴露一个宿主端口，并按 `oidc.localhost`、`user.localhost`、`finance.localhost`、`admin.localhost` 和 `api.localhost` 路由；若实际平台不支持，替代方案必须在技术设计中说明隔离损失并获用户确认。
- User Center 拥有外部身份映射、内部用户、账号状态、session、第一方 client/scope 和管理员审计。
- Finance Demo 拥有支出数据及资源授权，只消费用户服务的稳定身份/状态合同，不读其数据库。
- 普通用户、Admin 和服务调用使用不同 audience/session 边界；不得用普通用户表的 `is_admin` 作为管理权限模型。
- 两个后端缺省使用 Go、Kratos、Protobuf/gRPC、MySQL 与 sqlc；前端使用 Vite、React 与 TypeScript。
- 两个服务可以共用本地 MySQL 实例，但使用不同 database/schema 与凭据；默认无 foreign key，完整性由约束、事务、幂等和应用逻辑承担。
- 本轮只设计 selected increment 所需合同，不提前设计通用 IAM、完整 Finance、所有错误 taxonomy 或生产平台。

### 5.3 实现前定向审查

虽然整体路线为 Standard，下列高返工边界仍须在代码前由未参与设计的人审查：

- user-center 与 finance-demo 的数据所有权；
- subject、内部 `user_id`、audience、scope 与 session 的关系；
- Admin 身份隔离、按姓名搜索、Disable 状态转换与审计；
- 禁用后现有访问如何失效，Bob 如何不受影响；
- gateway/cookie/origin 边界；
- 目录模式、应用根和模板目标路径。

结论只能是 `accepted | changes_requested`。`changes_requested` 时返回本节或 UX，不得写实现。

## 6. OpenSpec 门

计划使用 change id：`build-user-service-vertical-slice-pilot-5`。

创建顺序：

1. Product review 为 `approved`；
2. UX `review.md` 为 `approved`；
3. 创建 proposal/specs/design/tasks，只描述 selected increment；
4. proposal 记录 `visual_ux: required` 并链接已批准 UX；
5. design 写入第 5 节全部技术决定和目录合同；
6. tasks 最多保留 5 个 active tasks，其余只放 Next/Later；
7. 运行 `openspec validate build-user-service-vertical-slice-pilot-5 --strict --no-interactive`；
8. 完成第 5.3 节定向独立审查；
9. 只有 strict validation 通过且 review 为 `accepted`，才能把首个代码任务改为 `in_progress`。

OpenSpec `tasks.md` 一旦创建即成为实现状态权威。本文只记录 gate、showcase、度量和最终实验判断，不复制任务勾选状态。

## 7. 全新实施顺序

本轮按用户可见纵切片推进，不按“先把所有后端层写完、再补前端”推进。

### Slice 0：应用根与模板基线

- 建立根 README、项目地图和声明的空应用根；
- 在各自应用根使用批准模板生成两个 Go 服务和三个 Vite 前端，保留版本、命令、目标路径和初始 build/test provenance；
- 建立最小 gateway、统一命令骨架和合成 reset 入口；
- 运行应用目录验证，证明根目录无应用私有 `internal/` 或 `src/`。

Exit：全部应用位于声明路径、模板证据可复查、目录验证通过。此 Slice 不因目录齐全而声称产品可用。

### Slice 1：可见身份

- 从真实 OIDC 页面选择 Alice；
- User Web 显示 Alice 的可理解资料；
- 重复登录映射到同一内部用户；
- 从单一 gateway 入口完成第一次人工 showcase。

Exit：观察者无需日志或内部 ID 就能确认 Alice 登录成功。核心身份映射测试先行；页面样式按已批准 wireframe 实现。

### Slice 2：第一方消费

- Alice 从 User Web 进入 Finance Web；
- Finance API 验证用户服务签发的身份，不接受浏览器提交的 `user_id` 作为授权事实；
- Alice 创建并看到 `42.50 / Groceries / Lunch`；
- Bob 看到自己的空状态。

Exit：真实页面动作与服务端业务状态一致，用户服务数据库和 Finance 数据库保持隔离。

### Slice 3：Admin Disable 闭环

- Admin 从独立入口登录；
- 按 `Alice` 搜索并看到可区分的结果；
- 输入理由、查看对象与影响、确认 Disable；
- Alice 现有访问失效并看到可行动的 disabled 页面；
- Bob 继续正常访问；
- reset 后重放整条旅程。

Exit：完整 selected increment 通过人工 showcase 和自动 Browser E2E。

### Slice 4：收口

- 只修复 selected increment 暴露的 P0/P1 或阻断性 UX 问题；
- 完成分层验证、干净环境重建和陌生验收者独立终审；
- 记录真实完成、`changes_requested`、stopped 或 terminated，不保留旧成功摘要抵消最新失败。

每个 Slice 同时最多 5 个 active tasks。每完成一个用户可见 Slice 就展示；若连续 2 小时没有新增可见产品事实，缩小当前 Slice 或停止，不能用新增文档、测试数量或基础设施延长投入。

## 8. 验证与证据名称

- `unit`：subject 映射、状态转换、audience/scope、Finance 归属与 Bob 不受影响；
- `component`：单个服务或前端在受控依赖下的行为；
- `host integration`：gateway、服务、数据库或 Mock OIDC 的局部真实集成；
- `complete local integration`：两个后端、三个前端、gateway、MySQL 和 Mock OIDC 由统一入口启动并贯通；
- `manual showcase`：用户或观察者在真实页面完成当前 Slice；
- `browser E2E`：自动浏览器通过真实页面执行业务动作，断言 UI 和最终业务状态，并保存失败 trace/screenshot/video；
- `independent review`：未参与产出的人从干净环境验收。

人工 showcase 不能标为 Browser E2E；接口、DOM 存在或页面打开不能标为产品旅程通过；Mock OIDC 不能标为 provider sandbox；本轮没有 production observation。

最低命令合同：

```powershell
pwsh ./scripts/dev.ps1 up
pwsh ./scripts/dev.ps1 wait
pwsh ./scripts/dev.ps1 reset
pwsh ./scripts/dev.ps1 showcase
pwsh ./scripts/dev.ps1 e2e
pwsh ./scripts/dev.ps1 logs
pwsh ./scripts/dev.ps1 down
```

`showcase` 可以准备确定性 fixture，但关键业务动作必须从页面完成；`e2e` 必须从干净完整环境运行。

## 9. Superpowers 使用范围

默认调用数为 0。会话开始、创作性、文件数量、任务时长、进入产品设计、进入 UX 或开始编码都不能单独触发 Superpowers。

只有下列具体问题允许重新判断：

| 问题 | 可选 skill | 允许条件 | 本轮默认 |
| --- | --- | --- | --- |
| Product/UX | `brainstorming` | 至少两个合理方案会实质改变用户任务、信息架构或范围，错误选择会造成明显返工 | 当前已有单一 selected increment，不调用 |
| Architecture | `brainstorming` | user-center/finance 数据所有权、session/audience 或 gateway 隔离存在多个高成本、难回退方案 | 先按第 5 节执行；只有新证据制造真实分叉时调用一次 |
| Debugging | `systematic-debugging` | 根因未知、跨组件、flaky，或第一种修复已经失败 | 编译器、测试或请求 trace 已直接证明原因时机械修复，不调用 |
| Completion | `verification-before-completion` | 准备对完整 selected increment、merge 或最终实验结论作重大完成声明 | 只在最终收口时允许，不用于每个小步骤 |

以下 skills 不预授权：`writing-plans`、`executing-plans`、`using-git-worktrees`、`subagent-driven-development`、`dispatching-parallel-agents`、`requesting-code-review`、`finishing-a-development-branch`。本文和 OpenSpec tasks 已拥有计划状态；独立审查是研发门禁，不等于必须调用 Superpowers review skill。

核心身份、权限、状态转换和跨服务合同必须测试先行，但这是一条实现要求，不自动触发完整 `superpowers:test-driven-development` 流程。

每次实际调用必须在本文 Run log 记录：具体 trigger、skill、开始/结束时间、解决的问题、改变的决定和净收益。调用一项不授权下一项；没有净收益必须如实记录。

## 10. 实验度量与判定

第五轮重点验证设计前置和目录合同是否真正改变执行，而不是再次统计文件数量。

必须记录：

- 产品定义首次提交到人工决定的 active minutes 与往返次数；
- UX 首个可审查线框、批准时间和返工原因；
- 首个代码产出的时间，证明它晚于两项人工批准；
- 模板生成目标路径及目录 verifier 结果；
- implementation started_at 到 Slice 1、2、3 首次可见事实的 active minutes 与 commit；
- active-task peak；
- 产品代码、测试、UX、OpenSpec 和其他治理工件数量；
- rework 次数与原因，尤其是产品/UX/目录返工是否在代码前被吸收；
- 各证据层级、最新结果、未覆盖项和剩余风险；
- Superpowers 调用及净收益；不可得的 token、成本或 tool-call 指标写 `unknown` 和原因，不填 0。

研发规范实验判为 `supported` 必须同时满足：

1. Product Definition 和 UX 均在首个代码文件前获得明确人工批准；
2. 多应用目录验证始终通过，仓库根没有应用私有 `internal/` 或 `src/`；
3. Slice 1 在实现开始后 120 active minutes 或第 5 次实现提交前出现，以先到者为准；
4. 完整 Slice 3 在 8 active hours 或第 15 次实现提交内出现，以先到者为准；
5. active-task peak 不超过 5；
6. 人工 showcase 与 Browser E2E 准确命名，最新失败能否决旧完成结论；
7. OpenSpec 和治理工件只服务明确决定、审查或验收，没有平行 Superpowers plan/spec；
8. 每次 Superpowers 调用都有具体 trigger 和可说明的净收益；0 次同样合格。

任一产品闭环成功都不自动证明流程 `supported`；流程符合但产品 hypothesis 失败，也可以得到有价值的 `not-supported` 或 `inconclusive` 证据。

## 11. Stop conditions

出现以下任一情况立即停止当前门或回退：

- Product Definition 或 UX 未批准却准备创建应用代码；
- 准备从沉默、一般授权或上一轮决定推断本轮 UX approval；
- 多应用仓库根出现 `go.mod` + `internal/` 的服务形状，或前端代码落入根 `src/`；
- 模板目标路径未声明、应用根非空、准备覆盖或先根生成再搬运；
- 需要恢复、复制或继续旧实现和旧任务；
- 需要真实数据、真实 provider、生产、外部通信或不可逆副作用；
- active tasks 超过 5，或出现第二份实施计划/状态文件；
- 连续 2 小时没有新增可见产品事实；
- Admin 只能按内部 ID 找人、服务端没有真正拒绝 Alice，或 Bob 受到错误影响；
- 准备把人工检查、API 成功或结构验证描述成 Browser E2E/产品完成。

停止是合法结果，不以补文档、扩大范围或改写旧状态强行继续。

## 12. 最终状态与出口

交付状态使用 `accepted | changes_requested | stopped | terminated`。实验评估使用 `supported | not-supported | inconclusive`，两者分别记录，不互相冒充。

只有 selected increment 的当前 Browser E2E、人工验收、目录验证和独立终审均通过，才能写 `accepted`。任何更新的失败或 `changes_requested` 立即否决旧完成摘要。

本轮结束后只选择一个最高影响 next：继续稳定 selected increment、返回产品/UX revise、修正规范，或终止。Later 中的多 provider、绑定、MFA、删除、完整 Finance 和生产加固不自动进入第六轮。

## 13. 新 session 启动指令

新 session 必须逐字遵守以下顺序：

1. 读取本文、研发规范根 README、产品定义、体验设计、实现条文中“应用根”规则；
2. 记录第五轮的用户指定 baseline、branch、初始 worktree、工具版本和读取 byte 数；若基线含未获用户指定的文件，只报告冲突并停止，不删除、不覆盖、不复用；
3. 复述 `Deliver / Standard`、`visual_ux: required`、Product Definition gate、UX gate、目录 gate 和“未批准前零代码”；
4. 只向用户提交第 3 节 Product Definition 候选供审查，等待明确决定；
5. Product approved 后只创建静态 UX 工件并请求第二次明确决定；
6. UX approved 后创建 OpenSpec、技术设计和项目地图，完成 strict validation 与定向独立审查；
7. 只有上述门全部通过后，才在声明的应用根生成模板和代码；
8. 每个 Slice 展示真实页面事实，并把实验 gate/showcase/度量写回本文，把实施任务状态只写入 OpenSpec `tasks.md`。

启动阶段明确禁止：创建根 `go.mod`、根 `internal/`、任何应用 `package.json`/`src/`、业务测试或实现代码；禁止因新 session 自动调用 Superpowers；禁止重新生成另一份产品方案或实施计划。

## 14. 当前决定与下一步

- Plan review：`pending`；Decision owner：用户。
- Product review：`pending`。
- UX review：`not-started`。
- Technical/OpenSpec review：`not-started`。
- Implementation：`not-authorized`。
- Superpowers：本方案编写阶段 0 次；没有具体复杂问题需要额外方法。
- Multi-Agent：0 次；本方案未获用户要求或授权并行 Agent。

唯一下一步：用户审查并明确确认本文。该确认只开放 Product Definition review，不开放代码实施。

## 15. Run log

尚未开始。任何时间、提交、通过结果、成本或审查结论都必须在真实发生后记录，不预填、不从前四轮补造。
