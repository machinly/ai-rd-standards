## Why

当前 W0–W9 研发规范按历史工作流和专项文件累积，存在跨阶段重复、同一判断分散、工具细节与稳定原则混杂、默认阅读路径较长等问题。用户已批准唯一执行方案 `docs/superpowers/specs/2026-07-15-rd-standards-content-rewrite-plan.md`，Change A 门禁工具已通过 G1；现在需要在不修改旧规范和正式入口的前提下，完整 review W0–W9，重组为四分类十一项的新草稿。

## What Changes

- 冻结经过 G1 验收的工具版本、W0–W9 实际来源和当前工作区状态。
- 逐文件完整读取 W0–W9，建立来源清单、逐行连续分段账本和可追溯原子规则表。
- 将全部规则归入立项、产品设计、工程交付、运行维护四分类下的十一项，记录次要影响、冲突和处理决定。
- 在保留语义边界的前提下重新表达规范要求，阻止长段直接搬运，并为合并、拆分、替代和退出保留逐条追溯。
- 从稳定规则簇形成十一项原则和四分类原则，建立原则—规则追溯。
- 生成并行的 `rebuild-draft/` 草稿、覆盖矩阵、冲突清单、退出候选和事实审查报告。
- 在 `awaiting_user_review` 停止，等待用户逐项审查；即使用户批准，最多进入迁移方案设计许可，不执行正式迁移。

## Non-Goals

- 不删除、移动、覆盖或修改 `docs/W0-*` 至 `docs/W9-*`。
- 不修改 `README.md`、`docs/00-start-here.md` 或任何正式入口。
- 不把 OpenSpec、Superpowers、工具政策或既有原则草案当作研发内容来源。
- 不自动决定语义归属、冲突取舍、原则正确性或退出可接受性。
- 不执行最终迁移，不 archive change，不 commit、push、stash、reset 或 checkout。

## Capabilities

### New Capabilities

- `rd-standards-content-rewrite`: 将完整 W0–W9 来源重组为四分类十一项的可追溯并行草稿，并通过人工批准门控制语义决定。

### Modified Capabilities

无。

## Impact

- 写入仅限 `rebuild-draft/`、本 change 和 `governance/rd-standards-rebuild/` 中方案允许的基线、状态、批准与报告文件。
- 旧规范和正式入口持续有效；`rebuild-draft/` 仅供审查。
- 来源为 G2 冻结的 W0–W9 共 40 个文件；任何来源变化、工具变化或越界写入都阻断推进。
- 用户负责 G4 冲突/归属决定、G6 原则确认和 G9 最终审查许可；Codex 负责读取、提取、重写、追溯和生产者自检。
