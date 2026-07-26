# 第四轮研发规范实验方案：本地库存 CSV 导入 UX Prototype

状态：`approved`；待新的 session 启动，尚未开始计时或实现。
日期：2026-07-26
实验授权：用户在当前 Codex 任务中提出“开启第四轮实验，写一个实验方案”。
方案批准：2026-07-26，用户说明将回到新的 session 开启实验，并在结束后返回复盘。
权威工件：本文既是实验方案，也是执行期间唯一的 Explore 短记录；它不是产品交付记录。

## 1. 实验选择与路由

第三轮已经证明，重跑完整用户中心会继续受到旧范围和既有实现的干扰；只做文字路由题又无法证明新流程能更快产生真实产品事实。本轮选择一个全新、独立、可丢弃的本地产品切片：**库存 CSV 导入预览**。

本轮路由为：

- R&D applicability：适用，因为任务将创建并验证一个本地产品交互；
- work mode：`Explore`；
- Explore type：`UX Prototype`；
- Deliver route：不适用，除非真实 showcase 后用户选择 `promote`；
- OpenSpec：promote 前不创建；
- 正式 visual UX gate、模板 provenance、完整质量矩阵和独立终审：本轮轻量 Explore 不要求；
- 安全、真实副作用和证据不得夸大的底线继续有效。

目标实现目录预定为 `D:\Workspace\inventory-csv-pilot-4`。不得复制或继续 `D:\Workspace\user` 的用户中心代码、OpenSpec、治理工件或未完成任务。

本仓库的 `governance/current-status.json` 只登记本轮为 `planned` 并链接本文，不复制 active tasks、showcase 或 outcome；执行事实仍只写在本文。

为排除框架选择造成的混杂，技术默认固定为无后端、无第三方依赖的静态 Web Prototype：HTML、CSS、ES modules 与浏览器 File API，通过本机已有的静态文件服务器运行。不得先安装框架或建设脚手架；若该默认值被实际环境证明不可行，记录证据后才能换成同等规模的替代方案，且计时不重置。

## 2. Question 与 hypotheses

### 2.1 唯一产品问题

第一次使用的仓库操作员 Alice，能否通过“先预览、明确指出错误、排除错误行、再确认导入”的单页流程，理解一份有一行错误的库存 CSV，并得到可信的导入结果，而不需要阅读外部说明或查看内部 ID？

### 2.2 产品 hypothesis

若预览表直接使用商品名称和行号表达错误，并在确认前显示将导入与将排除的数量，Alice 应能在不接受口头解释的情况下完成导入，并正确说出：成功导入 4 行、排除 1 行、库存总量为 45。

### 2.3 流程 hypothesis

若新的 Explore / Deliver 路由与 Superpowers complexity gate 有效，则本轮应同时满足：

1. 从首个实现动作起 120 分钟内，或第 5 次提交前，以先到者为准，出现一次使用实际应用入口的 showcase；
2. 在扩展横向治理或加固前先贯通一条 Walking Skeleton；
3. active tasks 峰值不超过 5；
4. promote 前只维护本文这一份执行记录，不创建 OpenSpec、平行 Superpowers spec/plan 或目标项目状态文件；
5. Superpowers 只有在出现具体复杂问题时才调用，每次调用都能说明所解决的问题，且不会自动串联下一项；
6. 保持本地、合成、可 reset、无外部副作用的 sandbox 边界。

任一关键条件不成立，都必须留下 `invalidated`、`revise` 或 `stopped` 的真实结论，不能通过增加文档、门禁或工期把失败解释成成功。

## 3. Sandbox boundary

允许：

- 全新的本地目录和本机浏览器；
- 仓库随附的合成 CSV fixture；
- 可删除、可重新生成的浏览器状态或本地临时状态；
- 为形成最短可见结果所需的单个 Web 应用及少量测试。

禁止：

- 生产环境、真实库存、真实客户或个人数据；
- 真实凭据、外部登录、外部 API、网络发送、付款或公开发布；
- 从用户电脑任意读取未明确选择的文件；
- 把 Prototype 声明为稳定 API、生产 migration、release candidate 或 production-ready；
- 为“看起来完整”而增加账号、权限、后台任务、数据同步、监控或部署系统。

若实现需要突破任一边界，立即停止轻量 Explore 并重新路由，不默认扩大授权。

## 4. Shortest slice 与确定性 fixture

应用只提供一个本地 URL。Alice 通过真实页面完成以下路径：

1. 选择随项目提供的 `inventory-one-error.csv`；
2. 在页面预览 5 行商品，不查看 API、日志或数据库；
3. 清楚看到第 4 行 `USB Cable` 的数量 `abc` 无效；
4. 选择排除该错误行；
5. 确认导入；
6. 在结果区域看到“已导入 4 行、已排除 1 行、库存总量 45”；
7. 执行 Reset 后回到可重复的初始状态。

固定 fixture 为：

```csv
sku,name,quantity
A-100,Notebook,12
A-101,Pen,20
A-102,Mug,5
A-103,USB Cable,abc
A-104,Laptop Stand,8
```

Showcase 必须复用实际应用入口。另做静态展示页、直接调用内部函数、只证明 DOM 存在或由 API 代替上传与确认，都不算通过。

## 5. 范围

本轮包含：

- 文件选择；
- 固定三列 CSV 的解析；
- 人类可理解的预览表；
- 一条数量校验错误；
- 排除错误行、确认导入、结果汇总和 Reset；
- 最低限度的 keyboard smoke、解析规则检查和真实浏览器 showcase。

本轮不包含：

- 列映射、批量编辑、撤销历史、复杂错误 taxonomy；
- 后端、数据库、账号、角色、多人协作或长期持久化；
- 任意 CSV 方言、超大文件、性能优化、国际化或正式无障碍审计；
- 完整 Browser E2E 套件、发布流水线、监控、恢复演练或生产安全结论；
- 为 legacy pilot JSONL schema 强行把 `Explore` 改写成路线 `B` 或某个 Deliver risk path。

页面标题、帮助文案或结果摘要属于伴随的普通内容工作，直接在产品切片中完成；不得为这些 Non-R&D 子任务单独创建研发工件或触发 Superpowers。

## 6. Active tasks、Next 与 Later

执行开始时只允许以下 5 个 active tasks：

1. 建立可启动的单页应用和唯一实际入口；
2. 加入固定 CSV fixture 与最小解析；
3. 实现预览表和第 4 行错误表达；
4. 实现排除、确认、结果汇总与 Reset；
5. 执行真实 showcase、最低检查并把事实写回本文。

`Next` 只保留 showcase 暴露出的一个最高影响修正。其他想法全部进入 `Later`，本轮不实施。active task 完成或明确停止后才能从 `Next` 补入，峰值始终不得超过 5。

## 7. 时间盒与执行节奏

1. 用户批准本文后记录 `started_at`、工具版本、实际初始读取文件和 byte 数；从首个实现动作开始计算 active time。
2. 优先让页面启动并显示 fixture，再补齐解析和确认路径；不得先建设治理目录、错误矩阵或测试平台。
3. 每 120 分钟或每 5 次提交进行一次真实 showcase，以先到者为准。
4. 连续 2 小时没有新增可见产品事实时，停止并缩小 question 或 shortest slice；不得追溯性延长时限。
5. 本轮 active time 硬上限为 4 小时，提交上限为 10 次。到达任一上限时必须展示当前事实并选择 outcome。
6. 等待用户观察的时间与实际实施 active time 分开记录；墙钟跨度不能冒充工作时长。

第一次 showcase 只回答产品 hypothesis，不借机评审生产架构。若第一次观察暴露歧义，只选择一个最高影响修正并在剩余时间盒内再展示一次。

## 8. Superpowers complexity gate

本方案设计阶段因“复跑旧项目、只做文字模拟、新建实际切片”三种方法会产生明显不同的混杂因素，使用了一次 `brainstorming` 来选择实验方法；该调用只影响本文，不授权后续 skills，也不计入实施时间。

实施阶段不预先要求任何 Superpowers。只有出现具体复杂问题时，才在本文 Run log 记录：

- 时间与当时 active task；
- 具体复杂度触发器；
- 选择的唯一或最小 skill 集；
- 它改变了哪个决定或证据；
- 实际耗时、减少的返工或“无净收益”结论。

没有命中触发器而零调用是合法结果。调用一项后不得自动进入详细计划、worktree、子 Agent、多轮 review、verification 或 branch finishing。实现已明确的简单页面、fixture、配置和机械错误修正直接完成并做相称检查。

## 9. Showcase 与证据

Showcase 由用户或另一位未查看实现细节的人从应用首页开始，使用固定 fixture 完成 shortest slice。观察者不得接受口头步骤解释；可以询问页面文字含义。至少记录：

- 首次可见页面时间与首次完整 showcase 时间；
- 观察者是否独立完成上传、识别错误、排除和确认；
- 观察者说出的导入数、排除数和库存总量；
- 一张结果截图，必要时附失败截图；
- Reset 后是否能重复；
- keyboard-only smoke 的实际范围；
- 自动检查的准确层级及其未覆盖项。

`browser E2E` 只有在真实自动化浏览器执行页面动作并断言最终业务状态时才能这样命名。人工浏览器观察只记为 `manual showcase`；组件或函数测试不得冒充完整产品验收。

## 10. 度量与 Run log

执行期间只在本文追加 Run log，记录真实发生值，不预填成功数字：

- `started_at`、`finished_at`、active minutes 与墙钟跨度；
- time to first visible fact、time to first complete showcase；
- 每次 showcase 的提交号、观察和结果；
- active-task peak；
- product files 与 process/governance artifacts 数量；
- process minutes、实现分钟、返工次数和返工分钟；
- tool calls、token 或成本等运行时可得数据；不可得时写明缺口，不填 0；
- Superpowers 调用及净收益；
- OpenSpec 是否保持在 promote 边界之外；
- evidence level、未覆盖项和剩余风险。

现有 `rd-pilot-record.schema.json` 只能表示历史 `A/B + Quick/Standard/High-risk`，不能准确编码 `Explore`。本轮不篡改语义来满足旧 schema。实验完成后若确需进入机器聚合，再把“扩展 schema 以表达 Explore”作为独立稳定增量评估；在此之前，本文及其来源指纹是本轮权威证据。

## 11. Outcome 与判定

本轮结束记录两项彼此独立的判断：

1. 产品 Explore outcome 只能选择一个：`validated | invalidated | revise | stopped | promote`；
2. 研发规范 pilot assessment 只能选择一个：`supported | not-supported | inconclusive`。它是对流程证据的评估，不是第六种 Explore outcome，也不自动触发 promote。

pilot assessment 只有在以下条件全部满足时才可记为 `supported`：

- first complete showcase 不晚于 120 active minutes，且不晚于第 5 次提交；
- actual entry、5 行 fixture、错误排除、4/1/45 结果和 Reset 均可现场观察；
- active-task peak 不超过 5；
- promote 前只有本文这一份执行记录，没有 OpenSpec、平行 Superpowers 工件或目标项目状态文件；
- 每次 Superpowers 调用均有具体复杂度触发器、明确产出和净收益记录，且没有自动串联；零调用同样合格；
- sandbox 与无外部副作用边界没有突破；
- 证据名称准确，数据缺口没有补造。

产品 outcome 根据 Alice 的实际观察选择：能独立完成并正确说出 4/1/45 时可记为 `validated`；需要一个明确交互调整时选择 `revise`；核心产品 hypothesis 不成立时选择 `invalidated`；边界、时间盒或继续价值消失时选择 `stopped`。产品 outcome 与 pilot assessment 不互相冒充：产品假设失败但流程反馈及时，流程仍可能得到 `supported`；产品交互成功但流程超时或膨胀，pilot assessment 必须是 `not-supported` 或 `inconclusive`。

`supported` 只表示这一次受控实验支持流程 hypothesis，不证明规范普遍有效，也不表示产品已经完成。

只有真实 showcase 后，用户明确选择稳定“预览、排除错误行并确认导入”这一最小行为时，才可选择 `promote`。随后重新判断 Deliver route；若进入 Standard，只为选中的稳定增量创建 OpenSpec，不复制本轮全部探索历史。

## 12. 停止条件与清理

出现以下任一情况立即停止当前实施：

- 需要真实数据、凭据、外部服务、发布或不可逆动作；
- 120 分钟没有完整 showcase，且缩小一次后仍无新增可见事实；
- active tasks 超过 5，或出现为了流程而扩张的第二份状态/计划；
- 实现开始建设本轮明确排除的后端、账号、权限或平台能力；
- 观察结果依赖口头解释、内部 ID、日志或 API 才能成立；
- 指标只能靠事后回忆补造。

实验目录只含合成和可重建状态。清理时可以删除临时运行状态，但保留本文、源代码提交、去敏截图和命令结果；不得保留本地绝对 secret、浏览器 token 或用户机器上的真实 CSV。

## 13. 当前状态与下一步

当前状态为 `approved-not-started`：方案已经获得用户批准，但尚未创建目标项目、尚未开始计时、没有实现或验证结果，也没有使用 OpenSpec。

下一步只有一个：新的 session 先读取本文，从全新目录启动 Explore，并把所有真实进展、偏差、showcase 和最终 outcome 追加到本文；首个实现动作发生前不得预填 `started_at`。
