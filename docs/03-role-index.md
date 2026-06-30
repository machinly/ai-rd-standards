# 角色泳道入口

## 目标

这份入口只回答一个问题：**当前 W0-W9 已经定位后，哪些角色需要参与、各自读什么、交付什么？**

W0-W9 仍然是主线。角色不是新的瀑布流程，也不按“产品 -> 设计 -> 后端 -> 前端 -> 测试 -> 运维”顺序推进。角色只是泳道：同一个 OpenSpec change 可以同时调度产品、Tech Lead、后端、前端、测试、运维、运营、安全合规，但所有角色都服务当前主导 W 和相邻门禁。

## 默认使用顺序

1. 总控 Agent 先读取 `README.md`、`docs/00-start-here.md`、`docs/02-standard-index.md` 和当前 OpenSpec change。
2. 总控 Agent 判断主导 W，并列出本次必须参与和可选参与的角色。
3. 角色 Agent 只读取自己的角色入口、当前 W 的 `00-main.md`，以及 `docs/02-standard-index.md` 中命中的触发专项。
4. 角色 Agent 输出判断、artifact、风险、缺口和人审点。
5. 总控 Agent 汇总冲突，更新 OpenSpec、tasks、索引或知识工件。

## 角色入口

| 角色 | 入口 | 主责 W | 典型参与 |
| --- | --- | --- | --- |
| 产品 | `docs/roles/product.md` | W0/W1/W8 | W2/W5/W6 |
| Tech Lead | `docs/roles/tech-lead.md` | W2 | W0-W9 |
| 后端 | `docs/roles/backend.md` | W4 | W2/W5/W6/W7 |
| 前端 | `docs/roles/frontend.md` | W4/W5 | W1/W2/W6 |
| 测试 | `docs/roles/qa.md` | W5 | W2/W3/W4/W6/W8 |
| 运维 | `docs/roles/ops.md` | W6/W7 | W4/W5/W8/W9 |
| 运营 | `docs/roles/support-ops.md` | W6/W8 | W0/W1/W9 |
| 安全合规 | `docs/roles/security-compliance.md` | W2/W5/W7 | W3/W4/W6/W9 |

## 总控 Agent 输出契约

总控 Agent 每次调度角色时输出：

- 当前主导 W，以及是否有 W3-W7 并行支线。
- 参与角色：`required` 和 `optional` 分开。
- 本次读取清单：当前 W 主规范、必要触发专项、角色入口。
- OpenSpec 更新点：proposal、spec、design、tasks 中哪几项会被更新。
- 冲突、人审点和下一步。

## 角色 Agent 输出契约

每个角色 Agent 输出：

- 角色判断：本角色是否应参与、是否阻塞。
- 已读取规范：角色入口、当前 W 主规范、触发专项。
- 产出或检查结果：只列本角色负责的 artifact。
- 风险和缺口：按 `must-fix`、`accepted-risk`、`handoff` 分类。
- 需要总控 Agent 汇总的事项。
- 需要问人的高影响判断。

## 专项精简规则

角色泳道也用于判断专项是否还值得独立存在。每个触发型专项必须能回答：

- 服务哪个角色消费者？
- 服务哪个 W？
- 什么触发条件才读？
- 最小产出是什么？
- 为什么不能由父级 `00-main.md` 覆盖？

答不清的专项默认合并、降级或删除。保留专项优先服务高频角色工作或高风险门禁；低频治理主题只在父级入口保留触发提醒和人审点。

## 人审点

默认不问：角色选择、读取清单、低风险索引更新、任务勾选、链接修正。

必须问：

- 是否改变 W0-W9 主线或 canonical 入口。
- 是否删除、归档、降级战略性文档。
- 是否接受数据、安全、隐私、合规、合同、发布、生产恢复或公开承诺风险。
- 是否让角色 Agent 执行真实生产副作用、真实客户触达、真实付款、真实数据删除或凭据操作。

