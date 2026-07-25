# 研发适用性、Explore / Deliver 路由与 Superpowers 作用域调整设计

状态：设计已获用户确认，实施计划已形成，待执行独立的 Standard change
日期：2026-07-26
适用对象：一名产品/研发负责人 + Codex
依据：

- [用户中心与家庭财务 Demo 第三轮研发规范实验方案](../../../experiments/user-center-service-pilot-3-plan.md)
- [第三轮正式回灌记录](../../../reviews/2026-07-24-user-center-pilot-3-ingestion.md)
- [现行研发规范入口](../../../README.md)
- [现行计划规范](../../03-engineering-delivery/06-planning.md)
- [现行唯一研发路由 skill](../../../skills/one-person-openspec-rd/SKILL.md)

## 1. 背景与问题

第三轮实验在 G5 停止。46.7 小时和 102 次提交后，11 条关键旅程只有 1 条通过、1 条失败且不完整、9 条未实现；62 个 OpenSpec tasks 完成 32 个，家庭财务 Demo 尚未开始。第一条真实纵向旅程约在 22.2 小时和第 61 次提交后才完成，而 `docs/superpowers`、`governance` 和 `openspec` 已累计 74 个文件、11,643 行。

这些事实不证明 OpenSpec、设计、TDD、审查或安全控制没有价值。它们证明：

1. 现行路由过早把“本地、合成、可重建的学习任务”整体当作产品化 High-risk 交付；
2. 风险判断过度依赖 `auth`、`admin`、`payment` 等领域词，没有先看真实后果、暴露范围和可恢复性；
3. 产品化、加固、恢复和证据整理先于最短可见产品闭环；
4. Superpowers 的全会话和全创作触发规则会自动串联设计文档、详细计划、TDD、工作树、子 Agent 和多轮 review，与“按需使用复杂方法”的目标冲突；
5. 非研发任务缺少明确退出条件，容易被研发规范和 Superpowers 一并吸入。

本次调整必须同时解决适用范围、探索与交付分离、Superpowers 作用域以及单一事实来源四个问题。只增加一个名为 `Prototype` 的第四等级不能解决概念混用，也不能阻止流程继续膨胀。

## 2. 已确认决定

用户已确认：

- 研发规范不适用于所有任务；非研发任务必须能够直接退出，不创建研发流程工件；
- 不把 `Prototype` 与 Quick、Standard、High-risk 并列；
- 第一层使用 `Explore / Deliver`；
- Explore 可按实际问题标记为 Product Discovery、UX Prototype 或 Technical Spike；
- Deliver 继续使用 Quick、Standard、High-risk；
- Superpowers 是复杂问题的按需工具箱，不是所有阶段的默认总流程；
- 使用某个 Superpowers skill 不自动授权或触发其余 skills；
- 英文术语作为正式名称，中文只用于解释，不制造另一套中文路由名。

## 3. 目标

调整后的研发入口应使执行者能够依次回答：

1. 这是不是研发任务？
2. 如果是，当前主要目的是 Explore 还是 Deliver？
3. 如果是 Deliver，属于 Quick、Standard 还是 High-risk？
4. 当前是否真的存在需要 Superpowers 专门方法处理的复杂问题？
5. 当前最短的可见产品事实或可验收结果是什么？

预期结果：

- 非研发任务不读取研发规范、不创建 OpenSpec、不更新研发 current status；
- Explore 在受控边界内优先学习，先形成一条真实可见闭环；
- Deliver 只稳定已经确认的行为，不把全部探索历史重新包装成规格；
- High-risk 继续保护真实生产、数据、权限、凭据、付款、外部通信和不可逆副作用；
- Superpowers 只在复杂度门命中时调用一个或少数直接相关 skills；
- 同一事实只有一个权威位置，不再平行维护 Superpowers spec/plan、OpenSpec 和 work brief。

## 4. 非目标

- 不新增第五个分类或第十二个研发项目；
- 不建设覆盖研发、行政、销售、内容、财务和个人事务的通用任务规范；
- 不要求每个非研发任务记录“不适用”证明；
- 不把 Explore 变成逃避安全、权限或外部副作用审批的标签；
- 不删除 Quick、Standard、High-risk；
- 不默认放宽生产、真实数据、真实凭据、付款、删数或外部通信控制；
- 不为本调整建设新的流程平台、dashboard、schema 或专用 renderer；
- 不直接修改已安装插件的缓存目录；
- 不在本设计阶段修改正式规范或运行时 skill。

## 5. 总体模型

```text
收到任务
  ↓
R&D applicability
  ├─ No  → 退出研发规范，使用任务自身的工作方式
  └─ Yes
       ↓
Work mode
  ├─ Explore
  │    ├─ Product Discovery
  │    ├─ UX Prototype
  │    └─ Technical Spike
  └─ Deliver
       ├─ Quick
       ├─ Standard
       └─ High-risk

Superpowers complexity gate 横向覆盖上述过程，但不自动触发。
```

`Explore` 与 `Deliver` 描述工作目的：

- Explore 的结果是减少关键未知并作出继续、修改或停止决定；
- Deliver 的结果是形成稳定、可维护、可验收的变更。

Quick、Standard、High-risk 只描述 Deliver 的治理路径。`Prototype` 是 Explore 中可能产生的一类工件，不是第四个风险或交付等级。`Walking Skeleton` 是形成端到端可见闭环的实施方法，也不是路线。

## 6. R&D applicability

### 6.1 进入研发规范

任务的主要结果满足以下任一条件时进入：

- 改变软件、产品、配置、schema、API、AI 行为、数据处理、基础设施或发布状态；
- 验证、发布、运行、恢复或处置一个产品或工程系统；
- 直接决定某项产品或工程变更的产品定义、体验设计、技术设计或验收边界；
- 研究结果将直接支持一个已识别的产品或工程决定。

### 6.2 退出研发规范

下列任务在不改变产品或工程系统时默认退出：

- 普通写作、翻译、摘要和资料整理；
- 图像、视频、演示材料等内容制作；
- 行政、日程、账目整理和一般信息查询；
- 与具体产品或工程决定无关的通用研究；
- 只读报告，且没有被授权产生后续实现变更。

退出后：

- 不读取四分类十一项目；
- 不创建 OpenSpec、研发计划、治理域或 current status；
- 不调用 `one-person-openspec-rd`；
- 不因“AI 参与”或“开始了一次会话”调用 Superpowers。

退出研发规范不取消任务自身的安全约束。外部发送、删除、敏感数据、法律、财务或其他高影响动作仍按对应任务的授权要求处理。

### 6.3 混合任务

混合请求按结果拆分边界，不让任一部分污染全部任务：

- “修复 bug 并撰写说明”中的代码变更进入研发；说明只消费已验证事实；
- “分析市场并决定是否建设功能”只有直接支持产品决定的部分进入 Product Discovery；
- “生成营销图并部署网站”中的图像制作不是研发，网站变更和部署是研发；
- 非研发部分不会因为与研发部分出现在同一请求中而创建独立 OpenSpec。

## 7. Explore

### 7.1 目的与类型

Explore 用于结果尚不确定、需要通过证据减少未知的研发工作：

- **Product Discovery**：验证目标用户、问题、价值、范围或成功标准；
- **UX Prototype**：验证任务流程、信息架构、交互和可理解性；
- **Technical Spike**：验证技术可行性、架构选择、集成边界或关键性能假设。

同一 Explore 可以包含多个观察视角，但只能有一个本轮最高优先级问题和一个最短验证切片。

### 7.2 轻量 Explore 的边界

只有同时满足以下条件，Explore 才获得轻量豁免：

- 在本地或隔离 sandbox 运行；
- 只使用合成、可丢弃、可重新生成的数据；
- 不访问生产、真实客户、真实凭据或未批准的外部系统；
- 不执行付款、外部通信、公开承诺或不可逆操作；
- 状态可以确定性 reset/reseed；
- 不把输出声明为稳定 API、生产 migration、发布候选或生产就绪。

`auth`、`admin`、`payment` 等词本身不取消轻量 Explore；真实后果、暴露范围和可恢复性才是判断依据。

一旦边界被突破，执行者必须停止轻量豁免并重新路由。涉及生产、真实数据、真实凭据、真实权限、付款、外部通信或不可逆副作用时，至少采用 High-risk 控制，不得继续以 Explore 为由降低门禁。

### 7.3 执行合同

轻量 Explore 默认：

- 只维护一份短迭代记录；
- 同时最多 5 个 active tasks，其余放入 `Next` 或 `Later`；
- 第一轮优先形成一条 Walking Skeleton；
- 对用户可见问题，使用真实产品入口、真实页面动作和最终业务结果；
- 使用 Alice、Bob、Admin 等人类可识别 fixture，不以 opaque ID、API 成功或 DOM 存在性替代可理解性；
- 每 120 分钟或每 5 次提交进行一次真实 showcase，以先到者为准；
- 连续 2 小时没有新增可见产品事实时停止并缩小范围；
- Showcase 复用实际产品入口，不另建掩盖当前状态的静态展示站；
- UI 和交互探索允许先实现后补关键自动化；
- 核心领域规则、安全边界、数据一致性和 bugfix 继续优先测试先行；
- 保留服务端授权、参数化 SQL、基本 Cookie/CSRF 防护以及日志不泄露 secret 的底线；
- 对纯合成、可丢弃状态优先 reset/reseed，不执行产品化前向恢复和长期证据固化。

### 7.4 工件与状态

短迭代记录只包含：

- question；
- hypothesis；
- sandbox boundary；
- shortest slice；
- active tasks；
- showcase result；
- evidence and limits；
- decision；
- next。

Explore 的合法结果为：

- `validated`；
- `invalidated`；
- `revise`；
- `stopped`；
- `promote`。

这些状态都不表示产品完成或生产就绪。轻量 Explore 默认不创建 OpenSpec、完整质量矩阵、模板 provenance、恢复演练或独立终审；实际命中的高风险控制除外。

## 8. Deliver

Deliver 用于目标行为已经足够明确，准备形成稳定结果的工作。

### 8.1 Quick

适用于结果已知、局部、低影响、容易撤回，且不触及用户关键行为、生产、敏感数据、权限或外部承诺的变更。

最小结果：

- diff 或产物；
- 相关检查；
- 剩余风险。

Quick 不因跨一个小时、修改多个相邻文件或 AI 参与而自动升级。

### 8.2 Standard

适用于需要稳定维护、用户可见行为发生实质变化、跨会话恢复、稳定契约或独立验收的变更。

Standard：

- 默认创建或继续一个 OpenSpec change；
- 只记录从 Explore 中选中并准备稳定的增量；
- 使用 `tasks.md` 作为执行状态权威；
- 保留验收、验证、回滚和独立终审；
- 按现行规则判断 visual UX、完整集成环境、模板 provenance 和关键旅程。

### 8.3 High-risk

适用于真实生产、客户数据、安全或权限边界、凭据、付款、公开承诺、外部通信、删数、难回退契约或不可逆操作。

High-risk：

- 在真实副作用前取得明确人类批准；
- 记录 impact、stop conditions、rollback、decision owner 和 evidence；
- auth、数据迁移、管理员权限和难回退契约在生产性实现前独立预审；
- 权限、批准或回滚证据不足时停止。

领域名不是单独触发器。本地合成身份实验可以 Explore；修改生产身份或管理员权限必须 High-risk。

## 9. Explore 到 Deliver 的转换

只有经过展示和选择的行为进入 Deliver。

转换发生在以下任一时点：

- 核心假设已验证，用户决定稳定该行为；
- 输出开始承担稳定 API、schema、migration 或兼容性责任；
- 需要正式维护、发布或独立验收；
- Explore sandbox 边界将被突破；
- 继续探索的成本高于形成稳定增量。

转换时：

1. 选择准备稳定的最小行为；
2. 明确不进入本次 Deliver 的探索结果；
3. 重新判断 Quick、Standard 或 High-risk；
4. Standard/High-risk 创建 OpenSpec 时只描述稳定增量并链接 Explore 证据；
5. 不把聊天、失败尝试和全部探索记录复制进 proposal、design 和 tasks；
6. 正式门禁从转换点开始，不追溯性伪造探索阶段已完成的产品化证据。

## 10. Superpowers 复杂度覆盖层

### 10.1 定位

Superpowers 是解决复杂问题的方法集合，不是研发路径、权限系统、状态权威或所有任务的默认编排器。

以下事项都不能单独触发 Superpowers：

- 开始了一次会话；
- AI 参与任务；
- 工作具有创作性；
- 文件数量多；
- 任务持续时间长；
- 任务被分为 Explore、Quick、Standard 或 High-risk。

调用一个 skill 不自动触发后续 skills。禁止默认串联：

```text
brainstorming
  → design doc
  → writing-plans
  → worktree
  → subagents
  → per-task review
  → branch finishing
```

### 10.2 复杂度门

满足以下至少一项时，才选择一个或少数直接相关 skills：

- 产品目标、用户问题、成功标准或非目标存在实质歧义；
- 存在多个合理方案，错误选择会造成明显返工；
- 涉及跨组件架构、长期契约、数据所有权或权限边界；
- 决定难回退，或涉及真实生产、数据、安全和外部承诺；
- 工作需要跨会话、复杂依赖排序或明确交接；
- 故障根因未知、跨组件、偶发，或第一次修复已经失败；
- 准备作出重大功能完成、可合并或可发布结论。

调用时必须简要说明命中的复杂度和选用 skill 的原因，不记录未调用清单。

### 10.3 阶段映射

| 问题 | 可选 skill | 使用条件 | 默认跳过 |
| --- | --- | --- | --- |
| Product Discovery | `brainstorming` | 用户、问题、价值、范围或成功标准有重大未知和多个方案 | 已有明确问题和单一验证假设 |
| UX / Product Design | `brainstorming`；必要时 visual companion | 新关键旅程、信息架构或高影响交互需要比较 | 文案、样式和已有方案的直接实现 |
| Architecture Design | `brainstorming` | 跨服务、数据所有权、权限模型、稳定 API、重大选型或难回退设计 | 沿用已批准模式的单组件修改 |
| Implementation Planning | `writing-plans` | 多组件、跨会话、复杂依赖或需要交接，且现有任务记录不足 | Quick、Explore 微切片、OpenSpec tasks 已足够 |
| Implementation | `test-driven-development` | 核心领域规则、权限、安全、数据一致性、公共契约、bugfix 或危险重构 | 抛弃式 UI 脚手架、生成代码、简单配置和探索代码 |
| Debugging | `systematic-debugging` | 根因未知、跨组件、flaky、性能问题或第一次修复失败 | 错误信息已直接证明根因的机械修正 |
| Completion | `verification-before-completion` | 重大功能、bug 修复、merge 或 release 结论 | 普通资料编辑只运行对应轻量检查 |
| Review | `requesting-code-review` / `receiving-code-review` | Standard/High-risk 终审、重大里程碑、复杂或有争议反馈 | Explore 微切片和机械修改 |
| Isolation | `using-git-worktrees` | 长期分支、并行变更或需要保护现有用户改动 | 只读、Quick、已有隔离环境 |
| Plan Execution | `executing-plans` | 已批准的复杂计划需要在独立会话执行 | 当前会话可完成的小型任务 |
| Multi-Agent | `subagent-driven-development` / `dispatching-parallel-agents` | 用户允许，任务独立、写域不重叠且有净收益 | 默认单 Agent、探索阶段和顺序依赖任务 |
| Branch Integration | `finishing-a-development-branch` | 功能分支或 worktree 已验证，确实需要集成决定 | 无分支、只读和普通原地修改 |

### 10.4 单一工件所有权

Superpowers 提供方法，不自动获得文档所有权：

- 产品事实写入产品定义或体验设计；
- 架构事实写入技术设计或 OpenSpec `design.md`；
- Standard/High-risk 执行状态写入 OpenSpec `tasks.md`；
- Explore 只使用一份短迭代记录；
- 非研发任务使用自身产物；
- 已有权威工件足够时，不再创建 `docs/superpowers/specs` 或 `docs/superpowers/plans` 的平行副本。

若选用的原始 Superpowers skill 强制创建平行工件或自动串联后续 skill，本规范的用户决定优先：保留其解决问题的方法，改写为当前权威工件，不执行无关串联。

### 10.5 运行时约束

当前安装版 `using-superpowers` 要求每次会话开始即检查并在存在极低可能性时强制调用；`brainstorming` 还要求所有创作任务进入设计文档、提交和详细实施计划。这与本设计直接冲突。

实施不能只修改研发正文，还必须增加高优先级、可持久化的 Codex 指令：

> Do not invoke Superpowers merely because a conversation started, AI is involved, or work is creative. Apply the R&D applicability gate and the Superpowers complexity gate first. When the gate is met, invoke only the smallest set of skills that directly addresses the complex problem. Do not chain skills automatically or create duplicate authority artifacts.

该指令优先覆盖 `using-superpowers` 的全会话默认规则，并应对非研发任务同样生效。项目内研发 skill 同步保留同一语义。不得直接编辑插件 cache；如果实际试点证明高优先级指令无法稳定约束运行时，再单独决定是否维护 scoped personal plugin，不能把 fork 作为本轮默认范围。

## 11. 保留、提前与延后的控制

### 11.1 始终保留

- 人拥有产品方向、风险接受、外部副作用和最终问责；
- 真实生产、数据、权限、凭据、付款、外部通信和不可逆动作需要明确批准；
- 服务端授权、参数化 SQL、secret 不落日志等最低安全底线；
- 证据层级不得互相冒充；
- 失败、stopped 和 terminated 是合法结果。

### 11.2 Explore 优先

- 一个最高优先级问题；
- 一条最短 Walking Skeleton；
- 人类可识别 fixture；
- 真实产品入口和定时 showcase；
- 最多 5 个 active tasks；
- 真实结果和证据边界。

### 11.3 转入 Deliver 后补齐

- 完整 OpenSpec；
- 稳定 API、schema 和 migration 责任；
- visual UX 正式门禁；
- 模板 provenance；
- 完整质量矩阵和系统性异常覆盖；
- 恢复演练、发布门禁和长期证据；
- Standard/High-risk 独立终审。

实际风险已提前命中时，对应控制不得延后。

## 12. 正式规范改动范围

实施不得新增分类或项目，只修改拥有相应决定的入口：

- `README.md`：在风险分流前增加 R&D applicability 和 Explore / Deliver；
- `docs/01-initiation/`：区分通用研究与直接支持产品/工程决定的 Product Discovery；
- `docs/02-product-design/03-definition.md`：定义 Explore 问题、假设、范围和 promote 决定；
- `docs/02-product-design/04-experience-design.md`：区分 UX Prototype 的快速真实展示与 Deliver 的正式 visual UX；
- `docs/03-engineering-delivery/05-technical-design.md`：加入 Technical Spike、Walking Skeleton 和多服务 Explore 的单一用户入口判断；
- `docs/03-engineering-delivery/06-planning.md`：维护 5 个 active tasks、showcase 时限、Explore 到 Deliver 转换；
- `docs/03-engineering-delivery/07-implementation.md`：加入选择性 TDD 和先纵切片后横向加固；
- `docs/03-engineering-delivery/08-verification.md`：加入人类可识别 fixture、showcase、Explore 证据与正式验收边界；
- `docs/04-operations-maintenance/11-evaluation.md`：记录 Explore 结果和流程净收益，不把文件数当价值；
- `skills/one-person-openspec-rd/`：更新 applicability、Explore / Deliver 路由、Superpowers 复杂度门、fallback map 和 review rubric；
- 用户级或项目级 Codex instruction：覆盖 `using-superpowers` 的全会话强制规则；
- OpenSpec capability specs：更新 one-person governance、navigation、AI coding workflow 和 testing quality 的增量要求；
- knowledge、governance ledger、verifier tests 和 runtime sync：同步新入口和代表场景；
- `decisions/`：新增一份决策记录，部分取代“所有 Standard/High-risk 实现前默认完整展开”的解释，但保留 Deliver 的 OpenSpec 默认值。

当前 `add-visual-ux-step-to-rd-standards` change 已完成 tasks 且独立 review 为 accept，但仍为 active。实施新 change 前先按当前事实完成其归档或明确并存边界，避免两个 active changes 同时修改 visual UX、planning、implementation 和 testing specs。

## 13. 路由验收场景

| 场景 | 预期 |
| --- | --- |
| 摘要一份非技术材料 | 非研发；不读取研发规范，不调用 Superpowers |
| 生成一张营销插图 | 非研发；使用图像任务自身流程 |
| 调研一个与具体产品决定无关的行业问题 | 非研发 |
| 判断某个已识别用户问题是否值得建设 | Explore / Product Discovery |
| 用静态或可运行界面比较两个关键任务流程 | Explore / UX Prototype；复杂时可用 brainstorming |
| 在本地合成环境验证 gateway、OIDC 和服务间身份 | Explore / Technical Spike |
| 修改一个不改变含义的按钮文案 | Deliver / Quick；不调用 brainstorming |
| 实现已经确认的用户资料编辑能力 | Deliver / Standard；默认 OpenSpec |
| 修改生产管理员权限或真实账号删除 | Deliver / High-risk |
| 本地合成 auth 原型 | 不因 `auth` 关键词自动 High-risk |
| Explore 准备接入真实客户数据 | 停止轻量 Explore，重新路由并采用 High-risk 控制 |
| 已有 OpenSpec tasks 足以执行 | 不再创建 Superpowers plan |
| 跨服务数据所有权存在三个合理方案 | 使用 brainstorming，并把决定写入技术设计或 OpenSpec design |
| 编译器明确指出漏掉一个 import | 直接修复和验证，不调用 systematic-debugging |
| 跨服务偶发失败且首次修复无效 | 使用 systematic-debugging |
| 三个任务共享写域或顺序依赖 | 不使用 parallel agents |

## 14. 试点与验收

正式变更实施并通过结构验证后，选择一个新的本地合成任务验证 Explore。试点至少证明：

1. 首个真实产品 showcase 不晚于实现开始后 120 分钟；
2. 同时 active tasks 不超过 5 个；
3. 在扩展横向治理前形成一条真实 Walking Skeleton；
4. Showcase 使用实际产品入口和人类可识别 fixture；
5. Explore 只维护一份短记录，没有默认创建完整 OpenSpec 或平行 Superpowers spec/plan；
6. 连续 2 小时无可见产品事实时实际执行缩小或停止；
7. promote 时只把选中的稳定增量带入 Deliver；
8. Superpowers 的每次调用都能指向一个明确复杂度触发器，没有默认串联；
9. 没有生产、真实数据、真实凭据、外部通信或不可逆副作用；
10. 结果准确标为 validated、invalidated、revise、stopped 或 promote。

同时记录：

- time to first visible fact；
- process minutes；
- showcase 次数和结果；
- active task 峰值；
- Superpowers skills 实际使用及解决的问题；
- OpenSpec 是否在 promote 前后正确分界；
- rework 和恢复成本；
- 未覆盖证据层级。

文件数和提交数只作为上下文，不单独证明成功或浪费。

## 15. 风险与控制

- **Explore 被当作无质量要求的借口**：保留 sandbox、最低安全底线、真实 showcase 和证据边界。
- **高风险工作伪装成探索**：以真实后果和数据边界判断；边界突破立即重新路由。
- **每项工作都被标成 Explore**：只有存在关键未知和可证伪假设时使用；结果已知的工作进入 Deliver。
- **Explore 永不结束**：每轮只有一个问题、一个最短切片和明确 decision；120 分钟 showcase 暴露漂移。
- **promote 时复制所有探索历史**：OpenSpec 只记录选中的稳定增量并链接证据。
- **Superpowers 仍然全局触发**：增加高优先级持久指令和代表场景测试，不依赖正文提醒。
- **Superpowers 完全不用导致复杂问题处理退化**：复杂度门明确产品、架构、调试、验证和审查触发器。
- **权威工件再次重复**：为 Product、Architecture、Explore 和 Deliver status 指定唯一 owner。
- **与现有 visual UX change 冲突**：在实施前归档或明确边界，再创建新 change。
- **120 分钟不适合特定任务**：该时限只约束轻量 Explore 的首次真实展示；无法展示时应缩小问题，而不是追溯性延长。

## 16. 回滚

本设计不涉及生产数据。若试点显示 Explore 或 Superpowers 复杂度门增加歧义、降低高风险识别或没有缩短可见反馈：

1. 保留试点记录为负面证据；
2. 停止新增 Explore 任务；
3. 新任务恢复 Quick / Standard / High-risk；
4. 保留 R&D applicability，继续排除非研发任务；
5. 保留真实高风险控制、证据分层和单一状态；
6. 通过后续 Standard change 收窄或移除 Explore 与 Superpowers 覆盖规则；
7. 不删除历史设计、失败和 reviewer 结论。

## 17. 决策记录

- 2026-07-25：第三轮正式回灌作为本次调整的主要负面实验依据。
- 2026-07-25：用户明确要求非研发任务不套用研发规范。
- 2026-07-25：提出受控探索、薄纵切片、定时 showcase 和最多 5 个 active tasks。
- 2026-07-25：用户要求限制 Superpowers，只在产品设计、架构设计等复杂问题中按需使用。
- 2026-07-26：不再把 Prototype 与 Quick、Standard、High-risk 并列。
- 2026-07-26：正式术语采用 Explore / Deliver；Explore 包含 Product Discovery、UX Prototype 和 Technical Spike，Deliver 包含 Quick、Standard 和 High-risk。
- 2026-07-26：用户确认 Explore / Deliver 与 Superpowers 复杂度覆盖层，可形成设计文档。
