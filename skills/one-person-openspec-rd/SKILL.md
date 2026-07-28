---
name: one-person-openspec-rd
description: "Gate R&D applicability, route applicable work through Explore or Deliver, then route Deliver through Quick, Standard, or High-risk; use OpenSpec and complex methods only where their triggers apply."
---

# Explore / Deliver Solo R&D Router

## Purpose

帮助一名产品/研发负责人先排除非研发任务，再以最小足够治理完成探索或交付。人的产品判断、风险接受、高影响副作用和最终问责不可外包。

## Applicability

在读取四分类十一项目、选择研发路径或创建研发工件前判断任务的主要结果。

进入 R&D 的条件至少满足一项：

- 改变、验证、发布、运行、恢复或处置产品/工程系统；
- 直接决定产品、体验、技术或验收边界；
- 研究直接支持一个已识别产品或工程决定。

普通写作、翻译、摘要、内容制作、行政、账目整理、一般查询、通用研究和未获实现授权的只读报告属于 Non-R&D。立即使用任务自身流程；不读取四分类十一项目，不创建 OpenSpec、研发状态或 Superpowers 工件。任务自身的删除、外发、敏感数据、法律或财务授权要求仍然有效。

混合请求按结果拆分；只有 R&D 部分进入本 router，其他部分只消费已验证事实。

### Applicable Repository Reading

把当前项目的仓库根记为 `<repo-root>`，路径始终相对该根解析：

1. 读取 `<repo-root>/README.md`。
2. 按主要决定只读取一个分类入口：
   - `docs/01-initiation/README.md`
   - `docs/02-product-design/README.md`
   - `docs/03-engineering-delivery/README.md`
   - `docs/04-operations-maintenance/README.md`
3. 再读取该分类中一个或少数直接相关项目原则，不默认扫描全部十一项。
4. 只有任务需要落地规则时，读取 `docs/execution-details.md`，再按其中的主题映射只加载一个或少数命中的执行细节文件；不得扫描整个第三级目录。

如果仓库没有自己的正式研发入口，读取 `references/workflow-map.md` 作为明确 fallback；不要把 fallback 当作项目事实。只有实现确实需要确认 Go、前端或数据默认时，才读取 `references/stack-defaults.md`。

## Work Mode

通过 applicability 后先选工作目的：

- **Explore**：关键未知仍主导，目标是用可证伪证据学习。
- **Deliver**：行为已经足够明确，目标是形成稳定、可维护、可验收的增量。

Quick、Standard、High-risk 只属于 Deliver。`Prototype` 是 Explore artifact；`Walking Skeleton` 是实施 tactic；两者都不是 route。

## Explore

按最高优先级未知选择一种类型：

- **Product Discovery**：用户、问题、价值、范围或成功标准未知；
- **UX Prototype**：关键任务流程、信息架构、交互或可理解性未知；
- **Technical Spike**：架构、集成、契约或技术可行性未知。

### Boundary and Record

轻量 Explore 必须保持：

- 本地或隔离 sandbox；
- 合成、可 reset/reseed 数据；
- 无生产、真实客户数据、真实凭据、未批准外部系统、付款、外部通信、公开承诺或不可逆动作；
- 不声明稳定 API、production migration、release candidate 或 production-ready。

任一边界被突破时停止轻量豁免并重新路由。只维护一份短记录：question、hypothesis、sandbox boundary、shortest slice、active tasks、showcase、evidence/limits、decision、next。

### Execution

- 同时最多 5 个 active tasks；其余放入 Next 或 Later。
- 第一轮优先用 Walking Skeleton 从实际产品入口经过必要组件形成一个可见业务结果。
- 每 120 分钟或每 5 次提交 showcase，以先到者为准。
- 连续 2 小时没有新增可见产品事实时，缩小 question/shortest slice 或停止。
- 使用 Alice、Bob、Admin 等可理解 fixture；API、DOM 或数据库行不能代替用户可见事实。
- 核心领域、授权、安全、数据一致性、公共契约、bugfix 和危险重构优先测试先行；抛弃式脚手架、生成代码、简单配置和探索代码可先实现，promote 前为 selected behavior 补齐相称回归证据。

合法 outcome 是 `validated | invalidated | revise | stopped | promote`。只有真实 showcase 后由人选择的最小稳定增量可以 promote；明确 excluded exploration，再重新判断 Deliver route。Explore 默认不需要 OpenSpec、formal visual UX、完整质量矩阵、Browser E2E 或独立终审，但任何实际命中的风险控制仍然有效。

## Deliver

### Quick

用于低风险、局部、可逆且不影响用户、生产、敏感数据、权限、付款、承诺或外部系统的明确工作。

- 不强制创建 OpenSpec 或流程文件。
- 交付 artifact/diff、相关检查和剩余风险。

### Standard

用于用户可见、跨文件/会话、AI 行为变化或需要独立验收的明确工作。

- 实现前创建或继续一个 OpenSpec change。
- 新用户能力、新服务或重大体验变化先确认权威产品输入和体验设计。
- 用户可见 change 在 proposal 记录 `visual_ux: required | not-required`；required 时链接当前 static UX 和明确的人类 `approved` review。
- 定义少量关键旅程，按风险提供完整本地集成、Browser E2E 和其他准确命名的证据。
- 最终 reviewer 不能是生产者。

### High-risk

用于真实生产、客户数据、安全、权限、凭据、付款、公开承诺、外部通信或不可逆操作。

- 在真实副作用前记录 impact、stop conditions、rollback、decision owner 和 evidence，并取得明确人类批准。
- auth、数据迁移、管理员权限和难回退契约在生产性实现前由未参与设计的人审查风险与回滚。
- 权限、批准或恢复证据不足时停止，不绕过。

## OpenSpec

OpenSpec 只默认用于 **Deliver Standard/High-risk implementation** 的代码、配置、schema、API、AI 行为、数据、基础设施或发布设计变更。轻量 Explore 和 Deliver Quick 不默认创建。

proposal/specs/design/tasks 只记录本 change 的稳定增量；`tasks.md` 是执行状态权威，并链接产品、体验、review 与验证证据。不要复制 Explore 全部历史或创建平行 work brief。只有用户明确批准并记录 decision owner、理由、范围和恢复方式时，Deliver Standard/High-risk 才可跳过 OpenSpec。

所有 guard/流程工件默认写入 `governance/<registered-domain>/`；项目只使用 `governance/current-status.json` 作为当前完成状态。OpenSpec validation 不替代真实验收、独立审查或发布批准。

## Superpowers Complexity Gate

使用任何 Superpowers 前读取 `references/superpowers-scope.md`。会话开始、AI 参与、创作性、任务时长、文件数量或路由名称都不能单独触发。只在具体复杂问题命中时选择最小直接相关 skill 集，并说明触发器和要解决的问题。

| Problem | Optional skill | Use only when | Skip when |
| --- | --- | --- | --- |
| Product/UX ambiguity | `brainstorming` | 重大未知且存在多个高返工方案 | 已有单一 hypothesis、文案/样式或直接实现 |
| Architecture | `brainstorming` | 跨服务、数据所有权、权限模型、稳定 API、重大选型或难回退设计 | 沿用已批准模式的单组件修改 |
| Planning | `writing-plans` | 多组件、跨会话、依赖复杂且现有记录不足 | Quick、Explore 微切片或 OpenSpec tasks 已足够 |
| Implementation | `test-driven-development` | 核心领域、权限、安全、数据一致性、公共契约、bugfix 或危险重构 | 抛弃式脚手架、生成代码、简单配置或探索代码 |
| Debugging | `systematic-debugging` | 根因未知、跨组件、flaky、性能问题或首次修复失败 | 错误已直接证明根因的机械修正 |
| Completion | `verification-before-completion` | 重大功能、bugfix、merge 或 release 结论 | 普通资料编辑的轻量检查 |
| Review | `requesting-code-review` / `receiving-code-review` | Deliver Standard/High-risk 终审、重大里程碑或复杂争议反馈 | Explore 微切片和机械修改 |
| Isolation/execution | `using-git-worktrees` / `executing-plans` | 长期隔离或已批准复杂计划需独立会话执行 | 已有隔离环境或当前会话小任务 |
| Multi-Agent | `subagent-driven-development` / `dispatching-parallel-agents` | 用户允许、任务独立、写域不重叠且有净收益 | 默认单 Agent、Explore 或顺序依赖 |
| Branch integration | `finishing-a-development-branch` | 已验证功能分支确实需要集成决定 | 无分支、只读或普通原地修改 |

调用一个 skill 不自动授权下一项。产品事实写入产品定义/体验设计，架构事实写入技术设计或 OpenSpec design，Explore 状态写入唯一短记录，Deliver Standard/High-risk 状态写入 OpenSpec tasks。原始 skill 若要求平行工件或无关串联，以本作用域和当前权威工件为准。

## Review

- 所有 R&D 路径做 producer self-check；使用 `references/review-rubric.md`。
- Explore self-check 核对 sandbox、actual entry、fixture、showcase、active-task peak、outcome、证据限制和每次 Superpowers trigger；默认不要求独立终审。
- Deliver Standard/High-risk 需要未参与产出的 independent final review。
- High-risk 的 auth/data/admin/irreversible 设计还需要 pre-implementation independent review。
- unit、integration、依赖容器、完整本地集成、Browser E2E、provider sandbox 和生产观察必须分开命名；同一执行者的两个视角不是两次独立审查。

## Completion

最终总结包含：

- applicability、Explore/Deliver 与 Deliver route；
- artifact/change、验证证据层级、未覆盖项和剩余风险；
- Explore outcome、showcase 与 next，或 Deliver 的 done/stopped/terminated；
- OpenSpec change id、validation、review/archive 状态，或明确的不适用/批准跳过记录；
- 用户可见 Deliver Standard/High-risk 的 `visual_ux` 判定与批准状态；
- 外部部署、需要人的决定，以及任何 Superpowers 或 Multi-Agent 的实际净收益；
- 新应用的 template provenance，或明确说明不适用。
