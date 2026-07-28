# 用户服务第四轮研发规范实验方案：Walking Skeleton Explore

状态：`running`；已于 2026-07-27 在新的 session 启动。
日期：2026-07-26
实验授权：用户确认开启用户服务第四轮实验。
权威工件：本文既是第四轮方案，也是执行期间唯一的 Explore 短记录；它不是用户服务交付证明。

## 1. 路由与代码边界

本轮仍然验证用户服务，但不再重建完整 MVP，也不恢复前三轮的实现：

- R&D applicability：适用，因为任务将创建并验证用户服务的实际产品闭环；
- work mode：`Explore`；
- Explore type：`UX Prototype`，同时保留最低身份与授权正确性；
- Deliver route：promote 前不适用；
- OpenSpec：promote 前不创建；
- 目标仓库：继续使用 `D:\Workspace\user`；
- 用户已确认该仓库中的历史实现文件已经清空。第四轮以清空后的当前 Git revision 和 worktree 状态为新基线，不新建另一个仓库；
- 不从 Git 历史、备份或其他目录恢复前三轮代码、配置、数据库、OpenSpec tasks 和治理工件，也不续跑旧任务。

本仓库的 `governance/current-status.json` 只链接本文，不复制 active tasks、showcase 或 outcome。执行事实、偏差和最终决定只写入本文。

## 2. 前三轮事实与第四轮修正

| 轮次 | 可采信结果 | 第四轮的直接修正 |
| --- | --- | --- |
| 第一轮 | 服务被删除；缺少权威产品输入、批准模板、完整本地环境和真实浏览器证据；高风险问题到终审才暴露 | 不恢复旧代码；使用明确产品旅程和准确证据名称 |
| 第二轮 | 治理、模板和本地环境改善，但最终仍为 `changes_requested`；人工浏览器检查被夸大为 Browser E2E，旧完成状态没有被最新失败否决 | Showcase 只证明实际观察；当前失败立即否决旧结论 |
| 第三轮 | 46.7 小时、102 次提交、74 份流程文件后，11 条旅程仅 1 条通过；首条旅程约 22.2 小时才完成，停止于 G5 | 只做一个 Walking Skeleton；最多 5 个 active tasks；每 120 分钟或 5 次提交展示；promote 前不建 OpenSpec |

第四轮保留前三轮的用户服务产品方向，但改变验证顺序：先证明真实用户能看到并使用身份，再逐轮吸收异常、正确性、安全、并发和运行复杂度。本轮不以完整用户中心、完整家庭财务产品或生产架构为目标。

历史依据：

- [第一轮方案](user-center-service-pilot-plan.md)与[第一轮回灌](../reviews/2026-07-10-user-center-experiment-ingestion.md)；
- [第二轮方案](user-center-service-pilot-2-plan.md)与[第二轮回灌](../reviews/2026-07-11-user-center-pilot-2-ingestion.md)；
- [第三轮方案](user-center-service-pilot-3-plan.md)与[第三轮回灌](../reviews/2026-07-24-user-center-pilot-3-ingestion.md)。

## 3. Question 与 hypotheses

### 3.1 唯一产品问题

在一个完全本地、合成、可 reset 的环境中，用户服务能否通过一条人类可理解的实际旅程证明自己的核心价值：Alice 登录第一方 Demo、创建一笔支出，Admin 按姓名找到并禁用 Alice，随后 Alice 的 Demo 访问立即被服务端拒绝？

### 3.2 产品 hypothesis

如果登录身份、内部用户、第一方 Demo 和管理员状态控制的最小边界正确，观察者应能只通过页面完成以下判断：

1. 登录后看到的是 Alice，而不是内部 ID 或固定的 `User`；
2. Alice 可以创建并看到一笔金额为 42.50、分类为 Groceries 的支出；
3. Admin 可以按显示名 `Alice` 搜索并执行带理由的 Disable；
4. Alice 再次访问 Demo 时被明确拒绝，Bob 仍可正常访问；
5. Reset 后相同旅程可以重复。

### 3.3 流程 hypothesis

如果新的 Explore / Deliver 与 Superpowers complexity gate 有效，本轮应在不牺牲最低授权边界的前提下：

- 首次真实产品 showcase 不晚于 120 active minutes，且不晚于第 5 次提交；
- 完整 Walking Skeleton 不晚于 240 active minutes，且不晚于第 10 次提交；
- active tasks 峰值不超过 5；
- 先产生页面业务事实，再增加非必要治理、异常矩阵或长期架构；
- promote 前只维护本文，不创建 OpenSpec、平行 Superpowers spec/plan 或目标项目状态文件；
- Superpowers 只在具体复杂问题命中时使用，不因新 session、创作性、时长或文件数自动触发或串联；
- 准确记录失败、缺口和证据层级，不用测试数量或文档数量替代产品结果。

## 4. Sandbox boundary

允许：

- `D:\Workspace\user` 中历史文件清空后的当前本地基线；
- Alice、Bob、Admin、Mock OIDC 和合成支出 fixture；
- 内存或可确定性 reset/reseed 的临时状态；
- 本机浏览器和只服务于本轮的本地端口；
- 为 identity mapping、服务端禁用和 Demo 授权边界提供的少量自动检查。

禁止：

- 生产、真实用户、真实个人或财务数据、真实 provider 和真实凭据；
- 外部 API、邮件、短信、付款、公开发布或不可逆操作；
- 复用前三轮数据库、secret、镜像、实现文件或未完成任务；
- 把 Prototype 声明为稳定 API、production migration、release candidate 或 production-ready；
- 为“完整”而扩展到多 provider、身份绑定、账号删除、MFA 平台、完整财务、观测平台或发布流水线。

若需要突破任一边界，立即停止轻量 Explore 并重新路由，不默认扩大授权。

## 5. Shortest slice

所有页面从一个宿主端口进入。默认使用以下 host 区分产品表面：

- `oidc.localhost:18080`：Mock 登录；
- `demo.localhost:18080`：第一方家庭财务 Demo；
- `admin.localhost:18080`：管理员入口。

一次完整 showcase 按以下顺序执行：

1. Reset 到 Alice、Bob、Admin 均为 active、没有支出记录的确定性状态；
2. Alice 通过 Mock OIDC 登录，在 Demo 首页看到自己的名字；
3. Alice 通过页面创建 `42.50 / Groceries / Lunch`，结果页显示记录与合计；
4. Admin 从独立入口登录，使用 `Alice` 搜索，而不是内部 user ID；
5. Admin 输入理由 `pilot showcase` 并 Disable Alice；
6. Alice 刷新或重新进入 Demo，服务端拒绝访问并显示可理解状态；
7. Bob 登录后仍可访问，证明操作没有影响错误对象；
8. 再次 Reset 后重复关键路径。

直接修改内存、调用内部函数、从日志读取结果、仅检查页面能打开或只证明 API 返回 200，都不能替代该 showcase。

## 6. Prototype 技术边界

为避免第四轮再次被框架和基础设施吞没，默认技术形状固定为：

- 一个新的 Go module、一个 `net/http` 进程、一个宿主端口；
- 按 Host 路由 Mock OIDC、Demo 和 Admin 三个表面；
- 模块内分离 identity/user、finance demo 与 admin，但本轮不拆网络服务；
- 使用内存 store 和显式 Reset，不引入 MySQL、migration、Kratos、gRPC、React、容器或第三方 provider；
- 使用 host-only session cookie，状态改变使用最低限度 CSRF 防护；
- 服务端根据 session 对应的内部 user status 决定 Demo 访问，不能相信页面提交的 `user_id`；
- 日志和错误不得输出 session、secret 或完整财务 fixture。

这是可丢弃的 UX Prototype 技术形状，不代表否定前三轮确认的 Go/Kratos/MySQL/sqlc/Vite 交付方向。若真实 showcase 后选择 promote，再以 selected increment 重新做 Technical Design 和 Deliver 路由；不得把本轮内部接口直接宣布为稳定契约。

若 `*.localhost` 在实际浏览器中不可用，可以改为同一端口的 `/oidc`、`/demo`、`/admin` 路径，但必须记录证据和由此未验证的 origin/cookie 隔离限制，计时不得重置。

## 7. Active tasks、Next 与 Later

执行开始时只有以下 5 个 active tasks：

1. 建立单进程、单端口、三表面入口与 Reset；
2. 实现 Alice/Bob Mock 登录、稳定内部身份和可见显示名；
3. 实现 Alice 创建并查看一笔 Demo 支出；
4. 实现 Admin 按姓名搜索、Disable 与服务端访问拒绝；
5. 执行两个 showcase、最低检查并把事实写回本文。

`Next` 只允许保存 showcase 暴露出的一个最高影响修正。其他事项进入 `Later`，本轮不实施。active task 完成、移出或停止后才能补入新任务，峰值始终不得超过 5。

`Later` 包含完整异常状态、身份绑定、session 管理、TOTP、完整审计、MySQL/sqlc、Kratos/gRPC、Vite/React、完整 Browser E2E、并发矩阵、删除传播、恢复、监控与发布。它们不是隐含承诺。

## 8. 时间盒与 showcase cadence

1. 用户批准本文后，新的 session 记录 `started_at`、工具版本、目标仓库 baseline commit、初始 worktree 状态和实际读取上下文 byte 数；首个实现动作前不预填结果。
2. Showcase 1 在 120 active minutes 或第 5 次提交前进行，以先到者为准；最低可见事实是 Alice 从实际登录入口进入 Demo，并通过页面创建和看到 42.50 支出。
3. Showcase 2 在 240 active minutes 或第 10 次提交前进行；目标是完成 Admin 搜索/Disable、Alice 被拒绝、Bob 不受影响和 Reset。
4. 连续 2 小时没有新增可见产品事实时，立即缩小 question/shortest slice 或停止；补文档和补测试数量不算可见事实。
5. 本轮 active time 硬上限为 6 小时、提交上限为 15 次。到达任一上限时必须展示当前状态并选择真实 outcome，不能追溯性延长。
6. 等待用户观察的时间与实施 active time 分开记录；墙钟跨度不能冒充工作时长。

Showcase 必须复用实际产品入口，不另建静态展示站。第一次展示后只修一个最高影响问题，再继续下一可见事实。

## 9. Superpowers complexity gate

本方案设计阶段需要在“复用旧实现、在同一仓库的清空基线上重启、另建仓库”三种会显著改变混杂因素和返工成本的方案中作出选择，因此使用了一次 `brainstorming` 选择同仓库清空基线。该调用只影响本文，不授权后续 skills，也不计入第四轮实施时间。

第四轮实施不预先要求任何 Superpowers。只有出现具体复杂问题时，才在本文记录：触发器、选择的最小 skill、解决的问题、耗时、改变的决定和实际净收益。没有 trigger 而零调用是合法结果。

本轮的产品问题、Prototype 架构、active tasks 和测试边界已经明确；会话开始、AI 参与、代码文件增加或任务持续一段时间都不能重新触发完整 brainstorming、writing-plans、worktree、子 Agent、多轮 review、verification 或 branch finishing 链。明确错误直接修复并做相称检查；根因未知或首次修复失败时再重新判断 complexity gate。

## 10. 最低检查与证据边界

Showcase 前至少保留以下准确命名的证据：

- unit：外部 subject 到稳定内部 user 的映射、display name、status transition；
- component/host integration：服务端对 active/disabled 用户的 Demo 访问控制，Bob 不受 Alice 状态变化影响；
- manual showcase：真实浏览器中的 Alice 登录、支出创建、Admin 搜索/Disable、Alice 被拒绝和 Reset；
- security baseline：服务端授权、host-only cookie、状态改变的最低 CSRF 检查，以及日志不泄露 session/secret。

核心身份映射和授权拒绝优先测试先行；页面布局、文案和抛弃式脚手架可以先实现，再在 showcase 前补相称检查。这里的测试先行要求不自动触发完整 Superpowers TDD 流程。

除非真正使用自动化浏览器执行页面动作并断言最终业务状态，否则证据不得标为 Browser E2E。人工观察只能记为 manual showcase；本轮没有 provider sandbox、complete local integration 或 production observation 证据。

## 11. 度量与 Run log

执行期间只在本文追加 Run log，不预填成功数字：

- `started_at`、`finished_at`、active minutes 与墙钟跨度；
- time to first visible fact、Showcase 1 和 Showcase 2 时间；
- 每次 showcase 的目标提交、观察、失败与一个最高影响修正；
- active-task peak；
- product files、测试文件和 process/governance artifacts 数量；
- process minutes、实现分钟、返工次数和返工分钟；
- tool calls、token 和成本等运行时可得指标；不可得时写明缺口，不填 0；
- 每次 Superpowers 使用及其净收益；
- OpenSpec 是否保持在 promote 边界之外；
- evidence level、未覆盖项、剩余风险和来源提交指纹。

现有历史 pilot JSONL schema 不能准确表达 `Explore`。本轮不把 Explore 强行写成路线 `B` 或某个 Deliver risk path；实验结束后若需要机器聚合，再把 schema 扩展作为单独稳定增量评估。

## 12. Outcome 与 pilot assessment

结束时记录两个独立判断：

1. 产品 Explore outcome：`validated | invalidated | revise | stopped | promote` 中选择一个；
2. 研发规范 pilot assessment：`supported | not-supported | inconclusive` 中选择一个。它不是第六种 Explore outcome，也不自动触发 promote。

产品 hypothesis 只有在实际浏览器中完整观察 Alice 支出、Admin 按姓名 Disable、Alice 被拒绝、Bob 不受影响和 Reset 后，才可记为 `validated`。一个明确交互调整仍可能改变结论时选择 `revise`；核心边界或可理解性不成立时选择 `invalidated`；边界、时间盒或继续价值消失时选择 `stopped`。

pilot assessment 只有在以下条件全部满足时才可记为 `supported`：

- Showcase 1 与 Showcase 2 分别满足 120/5 和 240/10 的双重上限；
- 实际入口、human-readable fixtures 和最终业务状态均可观察；
- active-task peak 不超过 5；
- promote 前只有本文这一份执行记录，没有 OpenSpec 或平行 Superpowers 工件；
- Superpowers 每次调用均有具体 trigger 和净收益记录，没有自动串联；零调用同样合格；
- sandbox、安全底线和无外部副作用边界没有突破；
- 证据准确命名，指标缺口没有补造。

产品 outcome 与 pilot assessment 不互相冒充：产品假设失败但反馈及时，流程仍可能得到 `supported`；产品交互成功但超时或流程膨胀，pilot assessment 必须是 `not-supported` 或 `inconclusive`。一次 `supported` 只是一条方向性正面证据，不能证明规范普遍有效。

只有真实 showcase 后，用户明确选择稳定“第一方 Demo 消费用户身份并响应禁用状态”这一最小行为时，才可选择 `promote`。随后重新判断 Deliver route；进入 Standard 时只为 selected increment 创建 OpenSpec，不复制本轮全部探索历史。

## 13. 停止与清理

出现以下任一情况立即停止或缩小：

- 需要生产、真实数据、真实 provider、真实凭据、外部通信或不可逆动作；
- 准备恢复或复制前三轮代码与未完成任务；
- 120 分钟内没有 Alice 从登录入口创建支出的可见事实；
- active tasks 超过 5，或出现第二份计划/状态/OpenSpec；
- 实现扩张到本轮 `Later` 项，而不是关闭当前 Walking Skeleton；
- Admin 只能按内部 ID 找用户，或 Alice/Bob 的状态影响错误对象；
- 观察结论依赖日志、API 或口头解释才能成立；
- 指标只能通过事后回忆补造。

实验目录只含合成、可重建状态。清理临时状态前确认目标路径和数据边界；保留本文、代码提交、去敏截图和命令结果，不保留真实 secret、浏览器 token 或真实财务数据。

## 14. 新 session 启动指令

新的 session 先读取本文，并明确复述：`Explore / UX Prototype`、目标仓库、5 个 active tasks、Showcase 1/2 时限、sandbox boundary 和“promote 前无 OpenSpec”。随后确认 `D:\Workspace\user` 仍处于用户所述的历史文件清空基线，记录 baseline commit、初始 worktree 状态、真实 `started_at` 和上下文量，再开始第一个实现动作。若发现未预期文件，只报告并停止，不自行删除或覆盖。

不得因为会话新开而重新生成产品方案、详细实施计划或调用整套 Superpowers。若本文与目标仓库事实冲突，先记录冲突并停止，不自行扩大范围。

## 15. 当前状态与下一步

当前状态为 `running`：目标仓库沿用 `D:\Workspace\user`，已在清空后基线上开始第四轮计时；尚无验证结果，也没有使用 OpenSpec。

下一步：完成单进程、单端口、三表面入口与 Reset，然后从实际登录入口形成首个可见产品事实。

## 16. Run log

### 2026-07-27 启动

- `started_at`：`2026-07-27T20:55:35+08:00`；`finished_at`、active minutes 与墙钟跨度待结束时记录；
- 路由复核：`Explore / UX Prototype`；Walking Skeleton；promote 前不适用 Deliver route 与 OpenSpec；
- 目标仓库：`D:\Workspace\user`；branch `main`；baseline commit `6b6fa577dc0c3423bc5dc004286be2d6be2111eb`（`clear all`）；
- 初始 worktree：clean，tracked files 为 0，目录中除 `.git` 外无文件；`main` 相对 `origin/main` 为 `+0/-0`，与方案中的清空基线一致；
- 工具版本：Go `1.26.1 windows/386`、Git `2.53.0.windows.1`、Node `24.13.1`、npm `11.8.0`；启动时未在 `PATH` 找到 `msedge`、`chrome` 或 `chromium`，浏览器实际路径待 showcase 前核验；
- 启动时主动读取的文件上下文：31,059 bytes。其中本文 16,853 bytes、`one-person-openspec-rd/SKILL.md` 10,132 bytes、因目标仓库无 README/研发入口而读取的 fallback `workflow-map.md` 4,074 bytes；对话系统上下文与工具返回值无法可靠计量，未补造；
- active tasks：5；当前 task 1 `in_progress`，tasks 2-5 `pending`；active-task peak 当前为 5；
- commits since baseline：0；showcase 尚未执行；time to first visible fact 尚未产生；
- Sandbox：仅本机端口、合成 Alice/Bob/Admin/支出与可 reset 内存状态；未接触生产、真实数据、真实 provider、真实凭据或外部副作用；
- Superpowers：0 次；当前没有命中具体复杂问题；Multi-Agent：0 次；
- OpenSpec：未创建，保持在 promote 边界之外；
- 运行时 tool calls、token 与成本：当前运行环境未提供完整、可靠的会话级计量，结束时记录可得部分并明确缺口。
