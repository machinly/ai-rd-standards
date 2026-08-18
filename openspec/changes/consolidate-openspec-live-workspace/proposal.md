## Why

正式研发规范已经由根 `README.md` 与 `docs/` 唯一承载，但 OpenSpec 曾保存 56 份重复主题规格和 65 个不参与当前执行的 archive。第一轮收敛已删除 54 份无消费者 specs、全部 archive 和旧 archive 决策，只因 `tools/test_current_rd_standards.py` 直接读取而暂留两份 UX specs。

后续审计确认，UX 规则已经完整进入正式 `docs/`；让测试继续读取两份副本只会固化双份维护。`tools/build_review_snapshot.py` 也只服务 2026-07-10 历史快照，当前 `--check` 已因预期 403 个文件、实际 227 个文件而失败。用户现已授权处理工具目录，因此本 change 完成最后的依赖解除与删除。

## Routing

- path: Standard
- visual_ux: not-required
- reason: 本 change 精简规范验证工具和 OpenSpec 资产，不改变产品界面或用户任务。
- decision_owner: user
- deletion_authorization: 用户明确同意按工具审计建议处理；历史证据不再作为保留理由。
- recovery: 受 Git 管理内容只通过仓库历史恢复；不创建第二份备份。

## What Changes

- 将 `tools/test_current_rd_standards.py` 的 UX 回归检查限定为 canonical `docs/`，不再读取 OpenSpec specs。
- 删除已失效的 `tools/build_review_snapshot.py`。
- 删除最后两份重复 OpenSpec specs，使 `openspec/` 只保留配置、当前说明和真实 active changes。
- 保留 `verify_pilot_records.py` 与对应测试；是否放弃未来流程效果验证留给后续明确决定。
- 不修改其他目录中的历史引用或用户现有内容。

## Non-Goals

- 不修改正式 UX 规则、第五轮方案、pilot 数据或其他用户未提交工作。
- 不修改 `reviews/`、`governance/`、`knowledge/`、`experiments/`、`skills/` 或其他历史目录。
- 不替 `define-application-root-directory-contract` 作出独立终审结论。
- 不删除当前仍有效的正式规范、runtime、项目证据或 pilot 验证器。

## Capabilities

### New Capabilities

- `openspec-live-assets`

### Modified Capabilities

无。

## Acceptance

- `openspec/` 只保留配置、当前说明和真实 active changes，不再包含仓库级 `specs/` 或 `changes/archive/`。
- `test_current_rd_standards.py` 仍验证两种 viewport、两种主题和一轮 review，但只读取 canonical `docs/`。
- `build_review_snapshot.py` 不再存在；其历史引用不被改写。
- OpenSpec strict validation、正式规范验证、运行时同步、全量工具测试和 diff 检查通过。
- 本轮新增写入只位于 `tools/` 与 `openspec/`。
