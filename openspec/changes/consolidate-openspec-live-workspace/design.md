## Context

第一轮 OpenSpec 收敛后仅剩两份 base specs，因为当前测试直接读取它们。对照显示，两份 specs 的未提交 UX 变化已分别由正式体验设计和验证条文承接；测试只检查两种 viewport、两种主题、四种组合、一轮 review 与 Browser E2E 边界，不需要第二套规范正文。

工具审计还发现 `build_review_snapshot.py` 没有当前入口，只被历史 reviews 与 manifests 引用；它核对的固定快照已因仓库清理失效。其余验证器均有当前正式入口、active change、第五轮方案或可复用测试消费者。

## Decisions

### 1. 当前规范测试只读取 canonical docs

保留现有 UX 回归断言，但从循环中移除两份 OpenSpec specs。测试继续保护正式体验设计和验证条文，不再强迫历史副本同步。

### 2. 删除最后两份 base specs

解除测试依赖后，`openspec/specs/` 没有 live consumer，也不是 OpenSpec strict validation 的必要条件。删除整个目录；需要恢复时使用 Git 历史。

### 3. 删除固定历史快照工具

`build_review_snapshot.py` 的唯一职责是重建或核对 2026-07-10 固定 manifest。当前检查已经失败，且没有 live navigation。删除工具，不修改历史文档中的当时命令或结果。

### 4. 保留 pilot verifier

当前 pilot 数据没有 eligible 样本，但 verifier 仍能防止在证据不足时宣称流程效果通过。用户尚未决定放弃未来效果验证，因此 verifier 与测试继续保留。

## Risks / Trade-offs

- 删除 specs 后，OpenSpec 不再提供长期 base-spec 浏览；正式三级文档本来就是唯一正文，active change 的 strict validation 已在无 base specs 环境验证通过。
- 历史 reviews 仍提到已删除的 snapshot 工具与 specs；这些引用描述当时事实，本次不把历史文档重新变成 live navigation。
- `test_current_rd_standards.py` 是用户已修改文件；本次只删除两段 spec 读取和调整一个循环，不改动其最新 UX 断言。

## Rollback

如发现当前消费者仍需要删除项，从本次变更前的 Git revision 恢复精确文件；不得恢复整套历史资产后把它们当作正式规范。
