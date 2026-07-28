## Context

`governance/current-status.json` 已声明 `formal_replacement_complete`，历史重建 run state 也已通过 G9；然而两个重建 change 仍显示 active，且其一次性 CLI、fixtures 和测试仍可被误认为当前维护入口。与此同时，角色文档已经失去 live navigation，两份 Superpowers 计划的决定、设计和任务已由 OpenSpec archive 承接。

本 change 只缩减当前执行面，不重写历史事实。Git 历史和保留的治理账本继续提供内容恢复与审计证据。

## Goals / Non-Goals

**Goals:**

- 让 `openspec list` 只显示真实进行中的 change。
- 删除没有当前消费者的一次性重建执行代码和重复计划。
- 让本地运行态目录不再污染 Git 状态。
- 保留正式规则追溯、批准、来源基线和历史审查证据。

**Non-Goals:**

- 不删除或改写 `governance/rd-standards-rebuild/` 的历史证据。
- 不压缩 56 份历史主题 specs 或 270 个既有 archive 文件。
- 不处理旧快照审查工具包；它属于后续低优先级清理。
- 不修改当前应用根目录合同、pilot 4/5 或用户服务仓库。

## Decisions

### 1. 分开“历史证据”和“可执行工具”

历史治理目录和规则追溯账本继续保留。只删除根入口、当前 skill 和现有验证命令均不再调用的 `rd_rebuild` CLI、核心模块、fixtures 与专项测试。这样可以消除旧执行面，而不丢失当时的输入摘要、批准、状态迁移和报告。

### 2. 旧 change 使用 archive，不直接删除

两个 change 都保留 `archive-outcome.md`，说明未勾选任务已经被后续 G9 与正式替换事实覆盖。归档使用 `--skip-specs`，因为 base specs 已作为历史主题规格保留，清理不得重新合并旧 delta 或改变当前正式规则。

### 3. 只删除可证明失去 live consumer 的文档

两份 Superpowers plans 没有入站引用，对应设计、proposal、tasks 和 review 已在 archive 中。八份角色文档只有历史 manifest/archive 引用，现行导航明确禁止把角色文档恢复为操作入口。历史引用可以继续指向当时存在过的路径，内容可从 Git 历史恢复。仍需保留的 2026-07-15 重写方案在文首明确标记为历史记录，并注明旧命令已经退役，避免被误认为当前执行入口。

### 4. 本地运行态只忽略，不处置已有 `.superpowers/`

三个 Python cache 和空 `.agents/` 可直接删除。`.agents/` 与 `.superpowers/` 加入 `.gitignore`；现有 `.superpowers/` 曾被前序计划明确保护，因此本 change 不读取 token、不删除内容、不停止进程。

### 5. 恢复以 Git 为准

受 Git 管理的删除通过 revert 本 change 提交恢复。Python cache 通过重新运行测试恢复。归档 change 可从 `openspec/changes/archive/2026-07-28-*` 移回 active，但只有新的明确决定才允许恢复旧重建工具为当前入口。

## Risks / Trade-offs

- [历史文档链接指向已删除角色文件] → 这些链接只存在于 manifest 或 archive，保留原路径作为历史事实，不把它们当 live navigation；Git 历史仍可恢复内容。
- [删除工具后无法重跑旧 G0-G9] → 历史运行结果、输入摘要、工具 manifest 和报告继续保留；当前正式规范由 `verify_rd_standards.py` 验证。
- [归档未全勾选 change 掩盖未完成事实] → `archive-outcome.md` 明确记录 superseded/terminated 原因，不把未勾选任务改写成完成。
- [清理混入用户当前工作] → 使用显式 allowlist，不使用 `git clean -fd` 或 `git add -A`，并在删除前后核对 pilot、当前 change 和 `.superpowers/`。

## Migration Plan

1. 记录 change 和精确删除 allowlist，先做 strict validation。
2. 删除缓存与空目录，更新 `.gitignore`。
3. 删除孤立计划和角色文档。
4. 为两个旧 change 增加 archive outcome，再以 `--skip-specs` 归档。
5. 更新历史治理映射并删除旧重建工具链。
6. 运行正式 verifier、剩余单元测试、runtime sync、pilot record、OpenSpec strict validation、链接与 diff 检查。
7. 完成 producer self-check，保留 independent final review 为最终接受边界。

## Open Questions

无。旧快照工具包和更激进的历史 specs/archive 压缩明确留给后续决定。
