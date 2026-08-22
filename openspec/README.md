# OpenSpec 活动工作区

OpenSpec 只用于确有长期契约价值的活动变更。正式工作方式以根 [WORKFLOW.md](../WORKFLOW.md) 为准，这里不复制流程正文。

## 何时使用

满足以下任一条件时，可以创建或继续一个 change：

- 改变需要长期维护的产品、API、数据、AI、基础设施或发布契约；
- 工作必须跨会话恢复；
- 存在多个重要验收条件或关键技术取舍；
- 失败影响较大，需要明确停止条件和恢复方式。

跨文件、用户可见、使用 AI 或任务耗时本身不要求 OpenSpec。只读调查、普通修复、文档修改和局部可逆工作默认直接执行。

## 状态边界

- `changes/<change-id>/proposal.md` 记录意图、范围、非目标和验收。
- `changes/<change-id>/tasks.md` 是该变更唯一的执行状态。
- 不再维护重复的 `current-status.json`、work brief 或平行计划。
- 格式校验不替代真实验收，也不授权生产或其他高影响副作用。

没有真实活动 change 时，`changes/` 可以不存在。
