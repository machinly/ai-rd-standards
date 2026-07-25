---
decision_id: default-enable-openspec-2026-07-11
decision: default-openspec-for-standard-and-high-risk-implementation
approved_by: user
approved_at: 2026-07-11
supersedes:
  - rd-standards-reset-2026-07-10:openspec-optional
conditions:
  - quick-remains-without-openspec
  - product-input-and-ux-remain-authoritative
  - openspec-does-not-replace-real-verification-or-independent-review
  - skip-requires-explicit-user-approval-and-recorded-boundary
revisit_on: after-10-eligible-pilot-records-or-two-default-openspec-retrospectives
---

# 默认启用 OpenSpec 决策记录

日期：2026-07-11
状态：accepted for implementation
决策人：用户
执行范围：当前研发规范、核心 router 和相关 Go/Vite 运行时技能

## 用户指令

默认启用 OpenSpec。

## 解释

- Quick 保持轻量，不创建 OpenSpec。
- Standard/High-risk 的代码、配置、schema、API、AI 行为、数据、基础设施和发布设计变更，在实现前创建或继续一个 OpenSpec change。
- 产品澄清、只读 review、报告和事故止血不因自身自动创建；它们产生后续实现变更时再创建。
- 具体实现要跳过默认规则，必须由用户明确批准并记录 decision owner、理由、适用范围和恢复方式。
- OpenSpec 只记录 change 增量并链接权威产品输入、体验设计、review 和验证；不能替代它们。
- `tasks.md` 作为执行状态来源，默认不再并行维护内容重复的 work brief。

## 依据

用户中心第二轮在模板批次作出一次不使用 OpenSpec 的决定，后续即使契约复杂度、返工和独立审查轮数显著上升，也没有重新评估。本轮因此无法提供 OpenSpec 成本或收益证据。新的默认规则让该变量真正进入后续 Standard/High-risk 实验，同时用 Quick 豁免和单一事实来源限制流程成本。

## 不代表

- OpenSpec 格式 PASS 不代表产品完成；
- 创建 change 不代表真实用户旅程或 Browser E2E 已通过；
- 生产者归档 change 不代表独立 reviewer 已接受；
- 默认启用不代表必须扫描全部历史 specs 或恢复 W0-W9 默认路由。

## 回退

若真实 pilot 显示 OpenSpec 维护时间超过实现收益、重复事实增加、恢复/返工没有改善，用户可将特定任务或全局规则降级。降级必须保留实验数据和明确的新决策，不由执行者静默跳过。

