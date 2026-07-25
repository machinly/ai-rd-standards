# 提案：回灌用户中心第二轮试验复盘

## Why

用户中心第二轮生成了大量安全、数据、运维和审查工件，并经历五轮独立终审，但最新结论仍为 `changes_requested`，且没有证明用户能从真实页面完成最基本任务。复盘表明当前规范把注意力过多放在接口、事务、guard 产物和 review 轮数上，没有先关闭关键用户旅程、真实 Browser E2E 和单一完成状态。

用户要求把 `D:\Workspace\user\governance\user-center-service-pilot-2-review\` 的复盘继续回灌为正式规范。该来源只支持本地合成实验结论，不支持用户中心生产就绪或规范总体有效性结论。

## What Changes

- 用户可见 Standard/High-risk 工作先定义少量可执行关键旅程，并尽早关闭至少一条真实浏览器闭环。
- 严格区分 Browser E2E、manual browser check 和局部 DOM/可访问性证据；关键旅程缺少可重复浏览器自动化时不能 accepted。
- 建立单一当前状态；最新独立审查为 `changes_requested` 时，先前完成摘要自动失效。
- 独立终审必须同时包含工程/安全视角和陌生验收者执行关键用户旅程的产品视角。
- 所有 guard/流程工件统一写入 `governance/<registered-domain>/`；项目根 README 和机器可读地图说明顶层目录、权威入口、进程与常用命令。
- 多个 Go `cmd` 入口必须登记用途、环境、生命周期、权限、数据写入、恢复和停用方式。
- 高价值代码注释解释状态转换、权限拒绝、事务/并发、关键 SQL、前端按钮状态、异常恢复和临时限制背后的“为什么”。
- 实验先关闭产品输入、最小旅程、完整本地环境和一条浏览器闭环，再按命中风险增加治理工件；每个治理域登记触发原因和改变的决策/门禁。
- OpenSpec 已由单独的用户决策改为 Standard/High-risk 实现默认，本 change 不恢复“可选后复评”规则，只记录第二轮没有覆盖该变量。

## Non-goals

- 不修复、发布或继续评价用户中心实现。
- 不把本轮复盘写成用户中心完成记录。
- 不要求 Quick 创建用户旅程矩阵、governance 目录或 OpenSpec。
- 不以固定注释覆盖率、固定 E2E 百分比或 review 轮数作为质量指标。
- 不一次性重写所有历史 guard；核心 router 的 governance 路径覆盖规则优先，命中的 runtime skill 逐步同步。

## Human decision

用户已明确授权将第二轮复盘继续回灌到正式规范。独立最终审查仍必须由未参与本次整改的 reviewer 完成；生产者不能自行接受。

