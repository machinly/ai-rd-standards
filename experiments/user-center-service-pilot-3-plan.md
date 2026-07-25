# 用户中心与家庭财务 Demo：第三轮研发规范实验方案

状态：实验已停止于 G5；G9 决定为 `improve`；不是产品交付记录。  
设计方向批准：2026-07-22，用户在当前 Codex 任务中批准“一个实验总计划、两个顺序实施单元”的方案。  
最终评估：2026-07-24，见[第三轮正式回灌记录](../reviews/2026-07-24-user-center-pilot-3-ingestion.md)。

## 1. 文档身份与权威边界

本文是第三轮实验的唯一总计划，负责说明产品结果、实验假设、范围、关键旅程、风险、门禁、证据和退出方式。它不代表用户中心或家庭财务 Demo 已经创建、通过验证或可以发布。

- 本轮只创建这一份实验计划，不复制 work brief、OpenSpec tasks 或当前状态。
- 实施期间，目标项目仓库的 `governance/current-status.json` 是执行状态权威；用户终止实验后的 G9 决定以本文和正式回灌记录为准。
- 两个实施单元各自使用 OpenSpec，`tasks.md` 是对应单元的执行状态权威。
- 实验数据只在真实任务开始后写入目标项目的 `experiments/rd-standard-pilot.jsonl`；不得预填时间、成本、通过结果或审查结论。
- 本仓库的 [pilot schema](rd-pilot-record.schema.json) 约束记录格式，[pilot verifier](../tools/verify_pilot_records.py) 只验证记录一致性，不替代产品验收。

本轮按以下正式研发入口执行：

- [研发规范总入口](../README.md)
- [产品定义](../docs/02-product-design/03-definition.md)
- [体验设计](../docs/02-product-design/04-experience-design.md)
- [评估](../docs/04-operations-maintenance/11-evaluation.md)
- [唯一研发路由 skill](../skills/one-person-openspec-rd/SKILL.md)

## 2. 已批准决定与本轮默认值

### 2.1 用户已批准

- 建设完整的用户中心 MVP。
- 同时建设一个使用用户中心的 Demo；Demo 是简单的家庭财务记录工具。
- 不部署生产，只在本地 Docker 测试环境运行。
- 外部登录 provider 不做真实接入，使用可重复的 Mock。
- 家庭、成员和账本权限属于家庭财务 Demo；用户中心只负责身份、登录、会话和第一方服务身份。
- 用户中心 API 只服务第一方应用；家庭财务 Demo 是已登记的第一方客户端。

### 2.2 为避免继续打断而采用的明确默认值

- 所有用户、管理员、家庭和财务记录均为合成测试数据；禁止复制真实个人资料、真实账单、银行流水或凭据。
- 普通用户与管理员使用不同入口、token audience、session 和权限策略。
- 管理员使用独立测试账号并强制 TOTP MFA；本轮不实现 passkey。
- 用户中心和家庭财务后端分别拥有数据库边界；允许共用一个本地 MySQL 实例，但使用不同 database/schema 与凭据，禁止跨库直接查询。
- 一个家庭使用一种基础货币；记录 currency code，但不做汇率换算、多币种合并或金融建议。
- 所有产品组件都由同一个 Docker Compose 测试拓扑启动；浏览器测试可以使用一次性测试容器。
- 后端采用 Go、Kratos、Protobuf/gRPC、MySQL 与 sqlc；交互前端采用 Vite、React 与 TypeScript。实际模板版本和创建命令必须在实施时从批准来源读取并留下 provenance，本文不虚构版本号。

这些默认值可以在实施前由用户修改；任何改变真实数据、生产、外部 provider、管理员边界、数据删除或第一方 API 范围的决定都必须回到本节重新批准。

## 3. 实验目标与可证伪假设

### 3.1 产品结果

从干净环境启动一套完整本地系统，使合成用户能够：

1. 通过 Mock OIDC 登录用户中心并获得稳定内部用户身份；
2. 进入家庭财务 Demo，创建或加入家庭；
3. 记录收入和支出，按分类查看月度汇总；
4. 管理自己的会话、资料导出和账号退出/删除；
5. 由独立管理员入口执行受控的查询、禁用、恢复和 session 撤销；
6. 在所有路径中保持普通用户、管理员和不同家庭之间的权限隔离。

### 3.2 研发规范实验目标

第三轮不再重复验证已经退役的流程，而是验证当前四分类、十一项目与唯一研发 skill 能否在一个真实 High-risk 项目中：

- 先形成产品行为、体验和验收，再进入实现；
- 在实现前发现身份、管理员、数据生命周期和难回退契约风险；
- 从批准模板生成全部新应用并保留 provenance；
- 尽早关闭一条真实浏览器旅程，而不是先扩张治理工件；
- 用一个完整本地环境覆盖用户中心、两个用户中心前端、家庭财务后端和前端、MySQL 与 Mock provider；
- 准确区分 unit、component、host integration、dependency container、complete local integration、browser E2E 与 manual evidence；
- 让最新失败或 `changes_requested` 自动否决旧的完成摘要；
- 产生可比较、可恢复且不过度包装的实验记录。

### 3.3 假设

如果当前研发规范有效，则第三轮应在不遗漏 High-risk 边界的前提下完成产品闭环，并留下可复现证据；OpenSpec、审查与治理工件应能够减少歧义或返工，而不是只增加文件数量。

如果关键旅程仍在最终审查才暴露基础不可用、证据层级再次被夸大、当前状态再次漂移，或流程工件无法帮助恢复和决策，则本轮假设不成立，即使结构验证和大部分测试通过也不能判定成功。

## 4. 产品范围

### 4.1 用户中心 MVP

本轮包含：

- Mock OIDC 登录、首次登录建号和稳定内部 `user_id`；
- 多个 Mock 外部身份与一个内部用户的绑定、解绑和冲突拒绝；
- 用户基础资料、账号状态、session 列表、单 session 撤销、全部退出；
- 固定的第一方客户端登记、scope、token audience 和调用审计；
- 用户资料导出、账号删除预览、二次确认、session 撤销和删除传播事件；
- 独立管理员登录与 TOTP MFA；
- 管理员查询用户、查看身份绑定、禁用/恢复用户、撤销 session；
- 所有管理员动作的 actor、target、reason、request id、结果与时间审计；
- 健康检查、关键错误指标、登录/权限拒绝指标和可定位的 request id。

“完整 MVP”只表示上述闭环全部可用并可验收，不表示已经覆盖通用 IAM、所有登录厂商或生产合规能力。

### 4.2 家庭财务 Demo

本轮包含：

- 使用用户中心登录，不维护第二套密码、session 或管理员身份；
- 创建家庭、生成一次性邀请、由另一个合成用户接受邀请；
- `owner` 与 `member` 两个家庭角色；
- 创建账户、收入/支出记录和分类；
- 编辑与删除自己的可操作记录，删除动作有明确对象和确认；
- 按月份和分类展示收入、支出与净额汇总；
- 家庭成员只能访问所属家庭的数据；
- 用户被禁用时不能继续访问；用户删除事件到达后撤销成员访问并按既定策略匿名化历史作者引用；
- 可从干净 seed 数据重复执行核心旅程。

### 4.3 明确不做

- 生产部署、真实用户、真实财务数据或真实凭据；
- Google、微信、QQ、支付宝等外部 provider 的真实 sandbox 或生产接入；
- 银行同步、支付、转账、信用卡连接、自动对账、税务或投资功能；
- 金融建议、预测、AI 分类或任何能直接触发金钱动作的自动化；
- 第三方开发者平台、公开客户端注册、开放 API key 自助管理；
- 把家庭或账本权限放入用户中心；
- 用户中心组织/企业租户、复杂 ABAC、通用 IAM 或多服务拆分；
- 原生移动应用、短信、真实邮件、passkey 和完整品牌系统；
- 多币种换算、正式会计报表或法定合规结论；
- 把本地测试证据描述为 provider sandbox、production observation 或生产就绪。

## 5. 系统边界与本地拓扑

### 5.1 组件

完整本地环境至少包含：

| 组件 | 责任 |
| --- | --- |
| Mock OIDC | 提供普通用户与管理员的可重复身份 fixture，不模拟真实厂商已通过认证 |
| User Center API | 身份映射、用户、session、第一方客户端、scope、审计与数据生命周期 |
| User Web | 普通用户登录、资料、身份绑定、session、导出与删除 |
| Admin Web | 独立管理员登录、TOTP、用户状态和 session 管理 |
| Finance API | 家庭、成员、账户、分类、收支、汇总和资源级授权 |
| Finance Web | 家庭财务关键旅程及 loading、empty、error、success 状态 |
| MySQL | 为两个后端提供相互隔离的本地 database/schema 与账号 |
| Browser E2E runner | 从真实页面执行关键旅程并保存失败截图、trace 或 video |

### 5.2 信任与数据流

1. Mock OIDC 只提供外部身份声明；User Center API 负责映射稳定内部用户并建立本地 session/token。
2. Finance API 只接受用户中心签发且 audience、issuer、expiry 和 scope 正确的身份，不接受前端传入的 `user_id` 作为授权事实。
3. Finance API 使用 token subject 查找家庭成员关系；家庭角色与资源授权完全由 Finance API 决定。
4. 管理员 token 不能访问普通用户或 Finance API 的用户路径；普通用户 token 不能调用管理员路径。
5. User Center API 与 Finance API 不读取对方数据库。禁用、恢复和删除通过版本化事件或明确 API 契约传播，并验证重复投递、乱序和失败恢复。
6. 日志、截图和测试 artifacts 不保存 token、TOTP secret、完整个人资料或财务明细；测试值也按敏感数据方式处理。

### 5.3 统一命令合同

目标项目必须提供一套可发现的命令入口，至少支持：

    pwsh ./scripts/dev.ps1 up
    pwsh ./scripts/dev.ps1 wait
    pwsh ./scripts/dev.ps1 smoke
    pwsh ./scripts/dev.ps1 e2e
    pwsh ./scripts/dev.ps1 logs
    pwsh ./scripts/dev.ps1 down

`up` 必须从声明的镜像、migration 和 seed 启动全部组件；`wait` 检查真实 readiness；`smoke` 覆盖跨组件最短路径；`e2e` 在干净完整环境运行浏览器套件；`down` 默认保留可诊断信息，清除 volume 的独立危险参数只允许用于确认没有真实数据的测试环境。

## 6. 关键用户旅程与验收

以下旅程在产品输入阶段写入目标项目的 `governance/quality/user-journeys.json`，并映射到可重复测试。每个界面必须覆盖 loading、empty、error 和 success；关键路径还要通过 keyboard-only smoke 与 WCAG 2.2 AA 基线检查。

| ID | 关键旅程 | 最终业务断言 | 最低证据 |
| --- | --- | --- | --- |
| UC-01 | 新用户经 Mock OIDC 首次登录 | 只创建一个稳定内部用户，重复登录不重复建号 | browser E2E + API/DB assertion |
| UC-02 | 用户绑定第二个 Mock 身份 | 正确绑定同一用户；已被占用身份被拒绝且不改写原关系 | browser E2E + concurrency/contract test |
| UC-03 | 用户查看并撤销 session | 被撤销 session 立即失效，其他未选 session 按设计保留 | browser E2E + integration |
| ADM-01 | 独立管理员完成 TOTP 登录并禁用用户 | 普通用户 token 不能调用管理 API；禁用后现有访问失效并留下审计 | browser E2E + auth negative tests |
| ADM-02 | 管理员恢复用户并撤销指定 session | 只影响目标用户与目标 session，审计 actor/target/reason 完整 | browser E2E + audit assertion |
| FIN-01 | 用户登录 Demo、创建家庭和第一笔支出 | Finance 只使用 token subject，记录与月度汇总一致 | browser E2E + integration |
| FIN-02 | 第二用户接受一次性邀请并记录收入 | 成员关系只属于目标家庭，邀请不可重复使用 | browser E2E + replay test |
| FIN-03 | 用户编辑和删除可操作记录 | 金额、分类、汇总与审计/历史策略一致，错误状态可行动 | browser E2E + integration |
| SEC-01 | 非成员枚举或直接请求其他家庭资源 | 列表、详情、修改和删除全部拒绝，响应不泄露资源是否存在 | browser E2E + authorization matrix |
| LIFE-01 | 用户导出并删除账号 | 导出范围明确；删除需二次确认；session 失效；Finance 成员访问被撤销 | browser E2E + event/idempotency test |
| REC-01 | 全部组件停止后从空 volume 重建 | migration、seed、readiness、smoke 与核心 E2E 可重新运行 | complete local integration |

Browser E2E 必须通过真实页面动作完成业务操作，并断言最终业务状态；直接调用 API 准备目标动作、只检查页面能打开或人工点击都不能替代该证据。允许 API 仅用于创建不属于被测行为的隔离 fixture，并须在测试中显式标注。

## 7. 风险路径、OpenSpec 与门禁

### 7.1 风险路径

整体按 High-risk 管理，触发原因是身份、权限、管理员动作、数据删除和家庭级资源隔离。虽然只使用合成数据和本地环境，也不能降低 auth 与授权设计的审查等级。

本次仅创建实验设计文档，尚未开始实现，因此现在不伪造 OpenSpec change。实施时按依赖顺序创建：

1. `build-user-center-mvp-pilot-3`；
2. `build-family-finance-demo-pilot-3`。

两个 change 都必须在实施前运行：

    openspec validate <change-id> --strict --no-interactive

第二个 change 必须引用第一个 change 已稳定并验证的身份契约，不得复制或静默改变 token、scope、禁用和删除语义。

### 7.2 顺序门禁

| Gate | 进入条件 | 通过证据 | 不通过时 |
| --- | --- | --- | --- |
| G0 书面方案 | 本文已落盘 | 用户复审并明确批准本文 | 修改本文，不创建项目 |
| G1 产品与体验 | G0 通过 | product bet、范围/非范围、surface、状态和旅程映射获用户确认 | 返回产品定义 |
| G2 OpenSpec | G1 通过 | 用户中心 change 完整且 strict validation 通过 | 修复 change，不写实现 |
| G3 实施前独立审查 | G2 通过 | 非生产者审查身份、管理员、删除、事件和回滚；结论 accepted | `changes_requested` 并停止实现 |
| G4 项目基线 | G3 通过 | 模板 provenance、首次 build/test、完整 Compose 拓扑和统一命令通过 | 修复基线，不扩展功能 |
| G5 用户中心闭环 | G4 通过 | UC/ADM 旅程、负向权限测试和浏览器证据通过 | 修复用户中心，不开始 Demo |
| G6 Demo OpenSpec 与闭环 | G5 通过 | 第二 change strict validation、家庭授权与数据生命周期的独立实施前审查 accepted、FIN/SEC 旅程通过 | 修复契约或 Demo |
| G7 全系统验收 | G6 通过 | LIFE/REC、完整 E2E、可访问性、恢复演练与证据包通过 | 最新状态置为失败或 changes_requested |
| G8 独立终审 | G7 通过 | 陌生验收者从干净环境执行关键旅程并给出 accepted | 不得保留旧完成摘要 |
| G9 实验评估 | G8 通过或实验停止 | 单一评估决定、一个最高影响下一步和去敏证据 | 保持 stopped/terminated 的真实状态 |

生产者自检不算独立审查。同一执行者换一个提示词或做第二遍检查也不算独立 reviewer。

## 8. 验证与证据合同

### 8.1 分层证据

- unit：纯函数、领域规则、金额计算、token/claim 解析和权限判断。
- component：单个服务或前端组件在受控依赖下的行为。
- host integration：宿主进程与一个或少数依赖的集成；若全部运行在容器中，可明确记为不适用。
- dependency container：MySQL 或 Mock OIDC 等依赖容器证据。
- complete local integration：全部产品组件在统一 Docker 拓扑中的跨服务证据。
- browser E2E：真实浏览器、真实页面动作、业务状态断言和失败 artifacts。
- manual：视觉、文案或探索性检查，只支持它实际观察到的结论。

Mock OIDC 证据不得标记为 provider sandbox；本轮没有 production observation。

### 8.2 必须覆盖的负向与恢复测试

- 普通用户调用管理员 API；
- 管理员 token 调用普通用户或 Finance 用户路径；
- 非家庭成员访问、枚举、修改或删除其他家庭资源；
- 过期、错误 audience、错误 issuer、撤销和禁用后的 token；
- 身份绑定冲突、并发绑定和重复 callback；
- 邀请重复使用、过期、错误家庭和并发接受；
- 金额边界、重复提交、幂等、事务失败和汇总一致性；
- 用户禁用、恢复、删除事件的重复投递、乱序和消费者失败；
- migration up/down 或等价恢复证明，以及空环境重建。

### 8.3 状态与过强结论防护

- 每次验证记录 command、environment、result、covered 和 not_covered。
- 更新的 `changes_requested`、失败旅程或失效 manifest 必须立刻把单一当前状态改为未完成。
- “接口测试通过”“容器启动”“页面可访问”和“人工点过”均不得写成完整 E2E 或产品完成。
- 只有 G8 accepted 后才能写“第三轮产品验收完成”；本地验收永远不能写成生产就绪。

## 9. 实验记录与度量

### 9.1 记录单位

至少为以下真实任务分别写一条记录，不把多个阶段压成无法解释的总数：

1. 产品与体验定义；
2. 用户中心 OpenSpec 与实施前审查；
3. 用户中心 MVP 实现与验收；
4. 家庭财务 Demo OpenSpec、实现与验收；
5. 全系统恢复演练与独立终审；
6. 第三轮实验评估。

记录沿用 schema 中的 `route = B` 仅为历史数据兼容；它表示当前 Quick/Standard/High-risk 路由，不恢复任何旧流程。实施任务使用 `risk_path = High-risk`。

### 9.2 开始时即采集

每个任务在首个有效动作前记录：

- `started_at`；
- 模型、runtime skill、OpenSpec、CLI、模板、Docker、Go、Node 和数据库版本指纹；
- 实际初始读取文件清单及 byte 数，`context_unit = bytes`；
- 到首个有效产出或命令的 `startup_minutes`；
- 人工打断的次数、原因与等待分钟；
- OpenSpec、审查、治理和证据整理的 `process_minutes`；
- 总耗时、返工、失败重试、工具调用和新增治理工件数量；
- 实际验证层级、覆盖和未覆盖项。

运行环境无法提供 token、成本或工具调用总数时写 `null`，并在 `metrics_gaps` 说明原因；未知值不得写成 0。

### 9.3 OpenSpec 净收益

每个 change 结束时回答：

- 哪个歧义、风险或返工被 proposal/spec/design/tasks 提前消除；
- 哪些内容与产品、体验或治理文档重复；
- 维护 OpenSpec 实际花费多少分钟；
- change 是否减少恢复时间或审查往返；
- 下轮应保留、合并还是删除哪些字段。

只统计文件数量不能证明流程有效。

### 9.4 恢复演练

G7 前安排一次至少间隔一天的新会话恢复演练。恢复者不得依赖原聊天，按根 README、治理入口、当前状态、两个 OpenSpec change 和必要代码入口恢复；记录读取 byte 数、恢复分钟、是否找对当前 gate、是否能给出下一条可执行命令。目标是在 15 分钟内正确恢复，超过时必须记录造成延迟的具体入口或冲突。

## 10. 成功、失败与最终决定

### 10.1 本轮成功条件

必须同时满足：

- G0 至 G8 全部以当前证据通过；
- 表中所有关键旅程在干净完整环境通过，且 SEC-01、ADM-01、LIFE-01 无权限或数据生命周期错误；
- 全部新应用具有可复查模板 provenance 和首次 build/test 证据；
- 两个 OpenSpec change 均 strict validation 通过，并记录实际维护成本；
- 实施前独立审查发生在相应高风险代码之前，独立终审由非生产者完成；
- 所有实际实施任务均有 schema 合法的记录；可获得指标已采集，不可获得指标有真实缺口原因；
- 最新 current status、旅程结果和 reviewer decision 一致；
- 恢复演练能在 15 分钟内找到正确状态和下一步；
- 没有把 Mock、局部测试或 manual evidence 描述为更高证据层级。

前两轮缺少可信的可比较时间基线，因此第三轮不能单独声称流程时间下降 30% 或总交付时间改善。它能产生一组新的合格证据，并验证前两轮暴露的具体缺口是否复发。

### 10.2 失败与停止条件

出现任一情况立即停止当前 gate：

- 需要真实用户、真实财务数据、真实 provider、生产部署或外部通信，但没有新的用户批准；
- 产品范围、管理员边界、删除语义或家庭权限被实现者静默改变；
- OpenSpec strict validation、实施前独立审查或当前 gate 失败；
- 任一普通用户获得管理员能力，或任一非成员访问其他家庭数据；
- 删除、禁用、恢复、session 撤销或事件重试影响错误对象；
- 模板 provenance 不可证明，或完整 Docker 环境缺少任一产品组件；
- Browser E2E 依赖 API 直接完成被测业务动作，或 manual 被标成自动化 E2E；
- 最新失败没有使旧完成状态失效；
- 度量在任务结束后才尝试回忆或补造；
- 测试工具发生未授权写入、非零退出或来源基线漂移。

停止是合法结果。不得为了得到“第三轮完成”而绕过门禁。

### 10.3 本地恢复与清理

本轮没有生产回滚。功能回退使用对应 OpenSpec 的代码/config/migration 恢复方案；环境恢复以从空 volume 重新执行 migration 和 seed 为准。删除本地 volume 前必须确认只含合成数据并使用明确危险参数。实验记录、失败 artifacts 和去敏审查证据应保留，secret、token、TOTP seed 和完整测试财务明细不得进入长期证据。

### 10.4 最终评估

G9 只能从 `continue`、`improve`、`rollback`、`stop`、`maintain` 中选择一个，并只保留一个最高影响下一步。其余发现保留为证据，不自动变成无限 backlog。

## 11. 实施顺序

1. 用户复审并批准本文，完成 G0。
2. 在全新目标项目中建立治理入口、单一当前状态和开始即采集的实验记录。
3. 完成产品/体验输入和关键旅程映射，取得 G1。
4. 创建用户中心 OpenSpec，strict validation 后进行实施前独立审查。
5. 从批准模板生成用户中心后端、User Web 与 Admin Web，建立完整 Docker 基线。
6. 先关闭 UC-01 与 ADM-01 两条浏览器纵向闭环，再扩展其余用户中心范围。
7. 用户中心 G5 通过后创建家庭财务 Demo OpenSpec，并冻结身份契约版本。
8. 从批准模板生成 Finance API 与 Finance Web，先关闭 FIN-01 与 SEC-01，再完成其余范围。
9. 执行全系统 LIFE-01、REC-01、可访问性、恢复演练和证据核对。
10. 由非生产者从干净环境完成独立终审。
11. 写入真实实验记录，形成单一 G9 决定和一个最高影响下一步。

不得并行实现两个后端的身份契约，也不得在用户中心 G5 之前开始家庭财务业务实现。

## 12. 与前两轮的关系

- [第一轮方案](user-center-service-pilot-plan.md) 和 [第一轮回灌](../reviews/2026-07-10-user-center-experiment-ingestion.md) 仅作为历史失败证据。
- [第二轮方案](user-center-service-pilot-2-plan.md) 和 [第二轮回灌](../reviews/2026-07-11-user-center-pilot-2-ingestion.md) 仅作为整改来源。
- 不恢复、复制、检查或评价已经删除的用户服务代码。
- 第三轮从全新目录和全新证据开始；历史未知指标保持未知。

## 13. 当前状态与下一步

当前真实状态是：G0 至 G4 已通过，实验停止于 G5。UC-01 通过，ADM-01 失败且不完整，其余九条关键旅程未实现；用户中心 OpenSpec 的 62 个任务完成 32 个；家庭财务 Demo、G6 至 G8 均未开始。源项目只完成局部用户中心能力，不构成完整本地产品、独立终审或生产就绪证据。

G9 的单一决定是 `improve`。证据、根因和后续规范调整约束见[第三轮正式回灌记录](../reviews/2026-07-24-user-center-pilot-3-ingestion.md)。

下一步只有一个：回到[计划](../docs/03-engineering-delivery/06-planning.md)，单独发起一次“Prototype / 薄纵切片 / 定时 showcase”研发规范精简变更；在此之前不继续源项目 Task 11.2，也不把本轮描述为完成。
