## Why

第三轮实验在 46.7 小时和 102 次提交后仍只有一条完整关键旅程，说明现行入口把本地合成学习任务过早产品化，并让可选复杂方法自动膨胀为全流程。与此同时，非研发任务缺少直接退出条件。

本 change 落实已确认设计 `docs/superpowers/specs/2026-07-26-rd-explore-deliver-superpowers-scope-design.md`；设计文档保留论证，本 change 只描述正式增量。

## Routing

- path: Standard
- visual_ux: not-required
- reason: 本 change 修改研发规范、治理和运行时路由，不新增或改变产品用户界面。

## What Changes

- 在任何研发读取和风险路由前增加 R&D applicability。
- 把研发一级工作模式改为 Explore / Deliver；Explore 使用 Product Discovery、UX Prototype、Technical Spike，Deliver 保留 Quick、Standard、High-risk。
- 为轻量 Explore 增加 sandbox、Walking Skeleton、5 个 active tasks、120 分钟或 5 次提交 showcase、2 小时无可见事实即缩小或停止、选择性 TDD 和 promote 边界。
- 把 Superpowers 改为复杂度触发、最小 skill 集、禁止自动串联的可选工具箱。
- 更新正式规范、运行时 skill、用户级 Codex instruction、治理映射、知识入口与回归测试。

## Non-Goals

- 不把 Prototype 增加为第四个风险路径。
- 不让非研发任务创建 OpenSpec 或研发治理工件。
- 不降低真实生产、数据、凭据、付款、外部通信和不可逆副作用门禁。
- 不修改 Superpowers 插件缓存，不建设 routing engine、新 schema 或流程平台。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `one-person-rd-governance`
- `rd-standards-navigation`
- `ai-coding-workflow-standard`
- `testing-quality-standard`

## Impact

- 正式规范仍为四分类十一项目；新增 16 个正式 rule-id，总数从 2,321 调整为 2,337。
- 两份来源账本仍各保留 5,956 条历史原子规则，只细化既有来源到新目标的映射。
- `one-person-openspec-rd` 继续作为薄路由，用户级 `AGENTS.md` 部署跨任务 Superpowers 作用域。
- 结构实现完成后仍需独立终审；流程效果保持 pending，直到新的本地合成 Explore 试点产生真实证据。
