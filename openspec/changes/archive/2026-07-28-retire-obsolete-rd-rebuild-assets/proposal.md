## Why

正式四分类十一项规范已经完成替换，但两项重建 change 仍留在 active 区，旧重建工具链、失去入口的角色文档和重复执行计划也仍处于当前工作树。这让历史证据和当前执行面混在一起，并增加误读、误运行和误提交风险。

## Routing

- path: Standard
- visual_ux: not-required
- decision_owner: user
- approval: 用户于 2026-07-28 确认按全仓清理审计建议执行
- recovery: 所有受 Git 管理的删除均可由本 change 的提交或 Git 历史恢复；本地缓存可由测试重新生成

## What Changes

- 删除三个 Python `__pycache__`、空 `.agents/`，并忽略 `.agents/` 与 `.superpowers/` 本地运行态目录；不读取或删除现有 `.superpowers/` 内容。
- 删除两份已经有 OpenSpec archive 承接、且没有当前引用的 Superpowers 执行计划。
- 删除八份没有 live navigation、现行导航已明确退役的角色视角文档。
- 为 `build-rd-rewrite-guardrails` 与 `rewrite-rd-standards-content` 记录被正式替换结果覆盖的结论，并使用 `--skip-specs` 归档。
- 删除只服务于已完成重建的 `rd_rebuild` CLI、核心模块、fixtures 与专项测试。
- 保留 `governance/rd-standards-rebuild/`、`governance/rd-standards/review/`、历史 reviews、sources、experiments、56 份历史主题 specs 和现有 OpenSpec archives。
- 更新历史重建治理与知识映射，使其指向 archive 而不是已不存在的 active change，并将保留的旧执行方案明确标为历史记录。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `rd-standards-navigation`: 增加正式替换完成后，历史执行资产必须退出当前执行面、历史证据必须保留的生命周期要求。

## Impact

- 删除 33 个受 Git 管理的旧计划、角色和重建工具文件，其中包含 6 个重建 fixture；实际数量以提交 diff 为准。
- 两个旧 change 从 `openspec/changes/` 移至 `openspec/changes/archive/2026-07-28-*`。
- 当前 `define-application-root-directory-contract` change、pilot 4/5、三级规范正文、正式校验器和运行时 skill 不在清理范围。
