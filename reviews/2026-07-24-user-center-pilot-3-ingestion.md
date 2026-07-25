# 用户中心与家庭财务 Demo 第三轮实验：正式回灌记录

状态：negative experiment evidence；G9 决定为 `improve`；不是产品交付记录。  
日期：2026-07-24  
来源项目：`D:\Workspace\user`  
实验方案：[第三轮研发规范实验方案](../experiments/user-center-service-pilot-3-plan.md)  
评估范围：从首个 Pilot 3 产出 `d43503a` 到实验收尾与 showcase 设计 `cdc6265`。

## 评估决定

本轮只选择一个出口：`improve`。

第三轮证明现行流程能够产生局部正确的实现、审查和治理证据，但没有证明它能以合理成本及时交付可用产品。实验在 G5 停止：G0 至 G4 通过，用户中心只通过 UC-01，ADM-01 为失败且不完整，其余九条旅程未实现，家庭财务 Demo 未开始。结构校验、测试数量、审查轮数和治理工件不能抵消这个产品结果。

唯一最高影响下一步：回到[计划](../docs/03-engineering-delivery/06-planning.md)，单独发起一次研发规范精简变更，先建立“Prototype / 薄纵切片 / 定时 showcase”路径；在该变更前不继续源项目 Task 11.2，也不把第三轮描述为完成。

源项目冻结的 `current-status.json` 仍保留 `in-progress` 与 “No automatic continuation”；用户随后明确终止实现并要求复盘。本 G9 记录关闭该实验状态，不把源项目的遗留字段解释为继续授权。

## 来源与指纹

来源工作区在评估时为 clean。下列指纹冻结本次判断所用的关键事实；源项目保留完整实现与运行证据，本仓库不复制代码、容器或测试 artifacts。

| 来源 | SHA-256 |
| --- | --- |
| `governance/current-status.json` | `57BBAE3717922DD0E478C0EADB0AB4948BC837F7910A787F9E6BCB0A9163AEC2` |
| `governance/quality/user-journeys.json` | `5871D65640BBAAD47D9D38499631634CCDABD7B1CF6FFF2EF810308E77C6FE5D` |
| `openspec/changes/build-user-center-mvp-pilot-3/tasks.md` | `1E0DF047BE131AF3A2C84183C94BD246CF03B7FA73BE4483F3523027747450A7` |
| `experiments/rd-standard-pilot.jsonl` | `8141358282A08B4084E37E679D808D77E2507894926ED4EC74332ACD703C1405` |
| `governance/evidence/user-center/adm-01-unaccepted-execution-incident.json` | `1A72C029D24CDFC6B63DF9F76CBAC788FE5CBB4327C3C931C20C54B80207A9A7` |
| `governance/evidence/user-center/adm-02-forward-recovery.json` | `7245EDCEFCCD2040C4C919F7695B6CDC04B0B2AC54BFC985F5B0748F03CC5185` |
| `services/user-center/internal/biz/auth.go` | `D2ED14D44C79DEAA331DA4040BCB3C9E29D165D5E2C2F2D726198A1C8862F3FE` |
| `web/admin/src/app/App.tsx` | `FC3F3D734CFF298F5C1F87675DCB0CC604179E6E61E4E26C96E1752642EE68EB` |
| `e2e/user-center/tests/support/adm01Journey.ts` | `F09AE83D630EB23CCB26B18081BDB0AC4142D320532FD6ED0C3A7C649A0E643B` |
| `scripts/dev.ps1` | `6B83A5DB3D19F89AA5DCDF97B28563104005EB1FCD135535E67764DAA926E696` |
| `deploy/compose.yaml` | `7412330DAA7CAD0854EE0C590AB95FD3E4678C87B1BE9B87801C6FED7FF033BA` |

## 可采信事实

| 信号 | 观察结果 |
| --- | --- |
| 时间与提交 | 首个 Pilot 3 产出到收尾共 46.7 小时、102 次提交，其中 61 次为 `docs:` |
| 首条真实纵向旅程 | 第 61 次提交、约 22.2 小时后才完成 UC-01 |
| Admin Web | 第 70 次提交、约 27 小时后完成首版；最终 `App.tsx` 为 2,212 行，配套 `App.test.tsx` 为 1,526 行 |
| 实验门禁 | G0-G4 通过；停止于 G5；G6-G8 未开始 |
| OpenSpec 执行 | 62 个任务只完成 32 个 |
| 用户旅程 | 11 条中 1 条通过、1 条失败且不完整、9 条未实现 |
| 产品价值 | 用户中心只有局部能力；家庭财务 API/Web 均未实现 |
| 流程工件 | `docs/superpowers`、`governance`、`openspec` 共 74 个文件、11,643 行；含 8 份 specs、12 份 plans、17 份 reviews、13 份 evidence、4 份 provenance |
| 事故恢复 | ADM-01 失败到完成前向恢复约 5.8 小时；恢复不构成 ADM-01/ADM-02 旅程通过证据 |
| Showcase | 第 102 次提交才开始设计；源项目没有 `showcase/` 实现目录 |

46.7 小时是可复查的墙钟跨度，不冒充纯工作时长；文件数和行数也不单独证明浪费。它们与“仅一条旅程通过、用户价值未闭环”的结果共同构成流程失焦证据。

## 关键产品反例

人工验收暴露了自动化没有阻止的基础可用性问题：

1. 新建用户的显示名被固定为 `"User"`：`services/user-center/internal/biz/auth.go:20` 和 `:731`。
2. ADM-01 E2E 用内部 `alice.userID` 搜索，并断言 `View User (<id>)`：`e2e/user-center/tests/support/adm01Journey.ts:453-470`。
3. 因此内部 ID 路径可以通过，而用户按产品语言搜索 “Alice” 得到 `No matching users`；搜索 “User” 也不能形成清楚、可识别的结果布局。
4. Admin 页面在一个 2,212 行组件中同时承载登录、TOTP、搜索、详情和动作状态，技术断言较多，但信息架构和视觉层级没有被及时人工验收。
5. `scripts/dev.ps1:402-426` 的 smoke 只检查 OIDC 页面文本和两个 callback 前端资源可访问，没有完成一次登录或业务 happy path。

结论：Browser E2E 必须使用人能识别的 fixture、文案和任务目标；“能按内部 ID 找到对象”不能替代“管理员能找到 Alice”。真实展示是验收入口，不是完成后的宣传附件。

## 根因判断

1. **风险分流只看领域词，没有充分看后果和可逆性。** 本地、合成、可重建实验因为 auth/admin 关键词整体进入 High-risk，原型阶段也承担接近产品化的全部门禁。
2. **把完整 MVP、产品化和加固放进同一张任务图。** 62 个任务同时覆盖协议、状态版本、锁顺序、审计、恢复、数据生命周期、可访问性和运维证据；首条纵向旅程前已经完成大量横向工作。
3. **流程工件领先于产品事实。** OpenSpec、plans、reviews 和 evidence 持续增长，但没有以“真实用户能否完成任务”作为最短反馈环。
4. **把可丢弃合成状态当成受保护生产状态。** 一次失败触发长时间的前向恢复、镜像证明和不可变证据处理，而不是预先批准的确定性 reset/reseed。
5. **自动化偏向内部正确性。** 测试验证 ID、状态版本、审计和协议，却没有足够早地验证名称、搜索、布局和可理解性。
6. **本地入口架构分散。** Compose 分别发布 5173、5174、8080、18000 四个端口，两个 Vite 应用各自维护代理规则；没有统一承载前后端入口的网关。
7. **Showcase 太晚。** 直到收尾才设计独立静态 showcase，没能在实现过程中反复暴露真实产品状态。

## 后续规范调整必须吸收的原则

以下是本次证据对后续规范变更的约束，不表示这些规则已经直接写入现行正文：

- 新增 **Prototype** 路径：面向本地、合成、可逆、无外部副作用的实验；风险判断以实际后果、可恢复性和暴露范围为主，不只按 auth、admin、payment 等关键词升级整个项目。
- Prototype 先交付一条薄纵切片：界面入口、后端、数据、真实浏览器动作和最终业务状态一次贯通；一轮最多维护 5 个 active tasks，其他内容只放 `Next/Later`。
- 每 90-120 分钟或每 5 次提交做一次真实 showcase；连续 2 小时没有可见产品进展时停止并缩小范围。
- Showcase 必须复用实际产品旅程和运行入口，不另做一个掩盖当前状态的静态网站。
- 异常处理先跑通一条通用、可行动、可重试的真实路径；完整错误 taxonomy、所有边界状态和恢复矩阵在 happy path 之后逐轮增加。
- UI 原型允许先实现再补关键测试；核心领域规则和 bugfix 继续采用测试先行。独立审查按里程碑执行，不在每个微切片重复。
- OpenSpec 用于已经展示、准备稳定的行为和契约；Prototype 默认只保留一份短迭代记录。完整 OpenSpec、provenance、恢复和发布门禁留给生产、真实数据、外部系统或不可逆副作用。
- 多服务本地 Demo 在技术设计时必须决定单一入口。对本项目，下一版应由一个 gateway/reverse proxy 只发布一个宿主端口，并按 `demo.localhost`、`user.localhost`、`admin.localhost`、`oidc.localhost`、`api.localhost` 路由；服务保持内部网络，host 分离继续保护用户端与管理端 origin/cookie 边界。
- 体验验收使用人类产品语言和确定性 fixture，例如 Alice、Bob、Admin；不得只用 opaque ID、API 成功或 DOM 存在性替代可理解性。
- 规范和 skill 应优先回答“现在最短的可见闭环是什么”，避免为同一微切片串联多份设计、计划、TDD、审查和完成仪式。

## 递进实现顺序

后续项目应按轮次吸收复杂度，而不是一次性展开：

1. **Walking skeleton**：单一网关、Alice/Bob/Admin fixtures、用户登录、一条 Finance 记录、管理员搜索 Alice 并禁用、Alice 访问被拒绝、一条真实浏览器 E2E 和人工视觉检查。
2. **异常与体验**：补一条通用异常路径、Admin 信息架构、关键 loading/empty/error 状态。
3. **正确性**：校验、幂等、状态版本和必要事务。
4. **安全与并发**：TOTP 限制/重放、CSRF、权限矩阵、竞态、锁和删除传播。
5. **性能与运行**：metrics、恢复演练、provenance、发布和长期证据。

即使在 Prototype，仍保留最小安全底线：只允许本地合成数据、不提交真实 secret、服务端授权、参数化 SQL、基础 Cookie/CSRF 防护，以及错误/日志不泄露 secret。其余加固必须由已出现的风险或下一轮目标触发。

## 证据边界

- 本记录不证明 OpenSpec、独立审查、安全或并发处理本身无价值；它证明这些活动在 happy path 之前无差别展开时，净收益为负。
- 本记录不支持恢复、继续或发布源项目，也不支持生产就绪结论。
- 源项目仅有两条阶段性 pilot JSONL 记录，缺少可信的全程 active time、token、成本和工具调用聚合；本仓库不补造一条“可比较完成记录”。本次结论以冻结的状态、提交、旅程和工件事实为依据。
- 后续修改 README、十一项目正文、唯一研发 skill 或 Superpowers 使用方式时，应引用本记录，并说明具体改动如何缩短首次可见闭环时间；不得只增加新的字段、模板或门禁。
