---
decision_id: introduce-explore-deliver-and-scope-superpowers-2026-07-26
decision: gate-rd-applicability-route-explore-deliver-and-scope-superpowers
approved_by: user
approved_at: 2026-07-26
archive_decision: publish-structure-with-pilot-pending
archive_decided_at: 2026-07-26
partially_supersedes:
  - default-enable-openspec-2026-07-11:lightweight-explore
conditions:
  - non-rd-exits-before-reading-rd-standards
  - explore-remains-local-synthetic-resettable-and-non-production
  - deliver-standard-and-high-risk-still-default-to-openspec
  - real-high-risk-controls-remain
  - superpowers-requires-a-concrete-complexity-trigger
revisit_on: after-first-new-explore-pilot-or-2026-08-26
---

# R&D Applicability、Explore / Deliver 与 Scoped Superpowers 决策记录

日期：2026-07-26
状态：structural implementation accepted；pilot pending
决策人：用户
执行范围：当前研发规范、`one-person-openspec-rd`、用户级 Codex Superpowers 作用域与后续本地合成试点

## 用户确认

- 研发规范不适用于所有任务；非研发任务在读取研发正文前退出。
- 研发一级工作模式使用 Explore / Deliver。
- Explore 使用 Product Discovery、UX Prototype 或 Technical Spike；Deliver 才使用 Quick、Standard 或 High-risk。
- Superpowers 只在产品设计、UX、架构、复杂计划、未知调试、重大验证或审查等具体复杂问题中按需使用，不在所有步骤自动调用。

## 对 2026-07-11 OpenSpec 决策的部分取代

`decisions/2026-07-11-default-enable-openspec.md` 继续适用于 **Deliver Standard/High-risk implementation**：代码、配置、schema、API、AI 行为、数据、基础设施和发布设计变更默认在实现前创建或继续一个 OpenSpec change。

该默认值不再适用于轻量 Explore。Explore 只维护一份短记录，并在本地/隔离、合成、可重建、无真实副作用的 sandbox 中形成最短可见事实。只有人选择的稳定增量 promote 后，才重新判断 Deliver route；Standard/High-risk OpenSpec 只描述 selected increment 并链接探索证据。

Deliver Quick 继续保持无 OpenSpec 默认路径；Deliver Standard/High-risk 跳过 OpenSpec 仍需用户明确批准并记录 owner、理由、范围和恢复方式。

## 术语边界

- `Prototype` 是 Explore 中用于学习的 artifact，不是第四个风险或交付路径。
- `Walking Skeleton` 是从实际产品入口贯通必要组件并形成可见结果的 tactic，不是 route。
- Explore outcome 是 `validated | invalidated | revise | stopped | promote`，任何一项都不自动表示产品完成或生产就绪。

## Superpowers 作用域

会话开始、AI 参与、创作性、任务时长、文件数量或工作模式都不能单独触发 Superpowers。只有实质产品歧义、多种高返工方案、跨组件或难回退架构、复杂跨会话依赖、未知或首次修复失败的故障，以及重大合并、发布或完成结论，才选择一个或少数直接相关 skills。

调用一个 skill 不授权或自动串联其他 skills。已有产品文档、技术设计、Explore record 或 OpenSpec 拥有事实和状态时，不创建平行 Superpowers spec、plan、work brief 或状态文件。

## 依据

第三轮用户中心实验在 46.7 小时和 102 次提交后仍只有一条完整关键旅程；产品化、横向治理和证据工件先于最短可见闭环。该负面结果说明本地合成学习任务被过早路由为产品化交付，且 blanket Superpowers 触发会放大流程。用户随后确认 `docs/superpowers/specs/2026-07-26-rd-explore-deliver-superpowers-scope-design.md`。

## 不代表

- 不授权生产、真实客户数据、真实凭据、付款、外部通信或不可逆副作用。
- 不降低真实 High-risk 的批准、回滚、验证和独立审查要求。
- 不授权修改 Superpowers 插件缓存或自动启动子 Agent。
- 不把结构校验 PASS 解释为 Explore 流程效果已验证。

## Pilot pending 归档决定

2026-07-26，用户明确选择“以 pilot pending 状态归档”。本次结构实施已经通过完整验证和未参与产出的 independent final review，可以合并到 OpenSpec base specs 并关闭 active change；由于没有执行新的本地合成 Explore 任务，流程效果继续记录为 `pending`，不得写成 `pass`、`validated` 或已证明能够缩短反馈时间。

归档后若自然出现符合 sandbox boundary 的本地产品任务，可以另行记录真实 pilot 证据；若证据显示路由或 complexity gate 需要调整，使用新的 Standard change 修正规范，不改写本次归档的历史状态。

## 回滚

若新的本地合成 pilot 显示 Explore 或 complexity gate 增加歧义、降低风险识别或没有缩短可见反馈，通过后续 Standard change 收窄或移除相关规则。回滚保留 R&D applicability、真实 High-risk 控制、历史负面证据和单一状态边界；用户级 instruction 只删除 managed markers 之间的 block，不覆盖其他用户内容。
