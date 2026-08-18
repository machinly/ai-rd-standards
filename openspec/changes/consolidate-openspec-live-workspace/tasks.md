# Tasks

- [x] 确认用户删除历史 OpenSpec 资产和失效工具的决定与 Git 恢复边界。
- [x] 验证无 base specs/archive 时既有 active change 仍可 strict validate。
- [x] 删除 54 份无 live consumer 的 specs、65 个 archive（288 个文件）和旧 archive 决策。
- [x] 确认两份 UX specs 的当前变化已由 canonical `docs/` 承接。
- [x] 实际运行 `build_review_snapshot.py --check`，确认固定快照已失效（403 expected / 227 actual）。
- [x] 从当前规范测试中移除两份 OpenSpec spec 读取，同时保留最新 UX 断言。
- [x] 删除 `build_review_snapshot.py` 和最后两份 OpenSpec specs。
- [x] 更新 `openspec/README.md`，只列配置与 active changes。
- [x] 运行 OpenSpec strict、正式规范、runtime sync、全量工具测试、范围扫描和 diff 检查。
- [x] 完成 producer self-check。
- [ ] 由未参与产出的 reviewer 完成 independent final review；未接受前保留本 change。

## Current evidence

- 2026-08-06 isolated probe：仅保留 config 与 `define-application-root-directory-contract` 时，OpenSpec strict validation 为 1 passed / 0 failed。
- 两份 canonical docs 与两份 specs 当前都包含 `mobile-portrait`、`1080p-landscape`、`light`、`dark`、四种组合与一轮页面 review；验证条文同时保留“不按四种组合重复完整 Browser E2E”的边界。
- pilot verifier 当前格式有效但 0 eligible；本次保留，未冒充流程效果已验证。
- `visual_ux: not-required`：只改变工具依赖与规范资产集合。

## Producer self-check（2026-08-06）

- 路由：R&D / Deliver / Standard；`visual_ux: not-required`。
- 结果：`tools/build_review_snapshot.py` 已删除；当前规范测试只读取 canonical docs；仓库级 `openspec/specs/`、archive 和旧 archive 决策均不存在。`tools/` 现有 7 个文件，`openspec/` 现有 14 个文件。
- 用户工作：保留了 `test_current_rd_standards.py` 中用户新增的两种 viewport、两种主题、四种组合、一轮 review 和 Browser E2E 边界断言，只删除两次 spec 读取；正式 UX 条文、第五轮方案和 `docs/roles/` 未修改。
- OpenSpec：`openspec list` 显示 2 个真实 active changes；strict validation 为 2 passed / 0 failed。
- 验证：27 项全量工具单元测试通过；正式规范验证通过（4 类、11 项、99 份细则、2,337 个 rule-id、7 份 review 文件）；runtime skill sync 通过；pilot record 格式有效且诚实报告 0 eligible / effect not verified；`git diff --check` 无错误。
- 范围：本轮新增写入只位于 `tools/` 与 `openspec/`；两份正式 UX 条文和第五轮方案是进入本轮前已有的 tracked changes，8 份 `docs/roles/` 是已有 untracked files。
- 剩余限制：历史 reviews/manifests 仍提到已删除的 snapshot 工具与 OpenSpec specs；pilot verifier 尚无 eligible 数据；本 change 与应用根 change 都仍待独立终审。
- Superpowers：0，未命中具体复杂度触发器。Multi-Agent：0，未获授权且无必要。模板 provenance：不适用。
