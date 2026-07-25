# 设计：从产品闭环开始的规范门禁

## 优先级顺序

用户可见 Standard/High-risk 项目按以下顺序建立信心：

1. 经人确认的产品输入和体验设计；
2. 少量关键用户/管理员旅程矩阵；
3. 批准模板和完整本地环境；
4. 尽早跑通一条真实 Browser E2E 闭环；
5. 按实际命中风险增加 auth、data、ops、credential 等治理域；
6. 在最新冻结输入上完成工程/安全和产品旅程独立终审。

这不是把安全放到最后；High-risk 实现前审查仍在第 1 至 3 步发生。该顺序只防止大量外围工件掩盖“用户根本无法完成任务”。

## 关键旅程与 Browser E2E

`governance/quality/user-journeys.json` 作为最小场景矩阵。每条旅程记录角色/目标、前置数据和权限、真实页面步骤、成功与失败结果、自动化层级、命令、证据、状态和最后执行时间。

只有同时满足以下条件才标为 `browser-e2e`：可重复浏览器自动化、从页面入口执行真实点击/输入/导航/确认、业务动作不被 API 替代、断言页面和必要最终业务状态、失败保留 trace/截图/视频，并能从干净完整本地环境统一运行。人工浏览器控制只能标为 `manual-browser-check`。

## 单一状态与证据失效

`governance/current-status.json` 是项目范围的单一当前状态，允许 `in_progress`、`independent_review`、`changes_requested`、`accepted`、`stopped`、`terminated`。它绑定目标 revision、最新 review 和更新时间。

任何较新的 `changes_requested`、失败旅程或失效 manifest 都使较早的完成摘要失效。历史 test run 可以保留为当时事实，但不能继续支撑当前 accepted 状态。

## 治理根目录与导航

项目过程证据统一进入：

```text
governance/
  README.md
  project-map.json
  current-status.json
  product/
  architecture/
  security/
  data/
  operations/
  quality/
  reviews/
  work/
  knowledge/
```

`project-map.json` 同时登记项目顶层目录和 governance domains。每个治理域说明 owner、触发原因、权威入口、改变的决策或门禁和保留策略。若 legacy skill 给出根目录相对路径，核心 router 将其重映射到 `governance/<domain>/`。

## Go 运行拓扑与设计意图

存在多个 `cmd` 时维护 `governance/architecture/command-registry.json`。每个入口登记 path、purpose、kind、environment、lifecycle、starter、dependencies、privileges、data_writes、failure_recovery、retirement。

设计意图注释只要求高价值位置，不设覆盖率：状态转换、权限拒绝、事务/并发、关键 SQL、前端按钮/禁用状态、异常恢复和临时限制。注释解释“为什么”和失败风险，不复述代码语法。

## 确定性验证边界

新增项目证据 verifier 只检查 artifact 结构、状态一致性、路径映射、cmd 覆盖和 Browser E2E 声明契约。它不能证明浏览器命令真实运行、用户体验正确或 reviewer 独立；这些仍需原始运行证据和独立验收。

