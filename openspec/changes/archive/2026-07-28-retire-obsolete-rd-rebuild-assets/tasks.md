## 1. Change Boundary

- [x] 1.1 记录用户批准、Deliver Standard 路由、`visual_ux: not-required`、精确清理范围与 Git 恢复方式。
- [x] 1.2 Strict validate 本 change，并核对所有删除目标位于仓库内且没有未披露 live consumer。

## 2. Local And Document Cleanup

- [x] 2.1 删除三个 Python cache 和空 `.agents/`，将 `.agents/`、`.superpowers/` 加入 `.gitignore`，保留现有 `.superpowers/` 内容。
- [x] 2.2 删除两份无人引用的 Superpowers 执行计划和八份退役角色文档。

## 3. Historical Rebuild Retirement

- [x] 3.1 为 `build-rd-rewrite-guardrails` 与 `rewrite-rd-standards-content` 记录 superseded archive outcome。
- [x] 3.2 使用 `--skip-specs` 归档两个旧 change，并确认 `openspec list` 不再把它们标为 active。
- [x] 3.3 更新历史重建治理与知识映射，使其指向 archive；将保留的旧执行方案标为历史记录，并保留全部历史治理证据。
- [x] 3.4 删除 `rd_rebuild` CLI、核心模块、fixtures 和专项测试。

## 4. Verification And Review

- [x] 4.1 运行正式规范、剩余单元测试、runtime skill、pilot record、OpenSpec strict、链接和 diff 检查。
- [x] 4.2 完成 producer self-check，记录证据、未覆盖项和恢复方式。
- [x] 4.3 由未参与产出的 reviewer 完成 independent final review；接受后再归档本 cleanup change。

## Producer Self-check — 2026-07-28

- 路由与方法：Deliver / Standard；`visual_ux: not-required`；使用 `one-person-openspec-rd`，没有触发 Superpowers、模板或并行代理。
- 实施范围：删除 33 个受 Git 管理的退役文件（8 份角色文档、2 份重复计划、23 个旧重建工具链文件），清除 3 个 Python cache 和空 `.agents/`，归档 2 个被正式版本取代的旧 change。
- 保留核对：`.superpowers/` 内容、`governance/rd-standards-rebuild/` 的 13 份历史证据、pilot 4/5、应用根目录 change、正式三级规范及全部既有历史 archive 均存在。
- 引用核对：知识地图已经改指 2026-07-28 archive；排除明确标记的历史证据后，旧 active change 路径、`tools/rd_rebuild` 与 `docs/roles/` 没有 live reference。
- 验证证据：正式规范校验通过（4 类、11 项、99 份细则、2337 个规则 ID）；剩余 26 个单元测试通过；runtime skill 为 synced；OpenSpec strict 为 58/58；pilot record 格式通过，效果验证仍为既有 `PENDING`；`git diff --check` 通过。
- 未覆盖项：旧快照审查工具包按设计明确留给后续低优先级清理。
- 恢复方式：受 Git 管理的删除通过 revert 对应提交恢复；cache 可由测试重新生成；旧 change 只有在新的明确决定下才可从 archive 恢复为当前执行面。

## Independent Final Review — 2026-07-28

- reviewer: 用户（未参与文件产出）
- decision: accepted
- evidence: 用户在收到精确清理范围、保留项和全部验证结果后，明确指示“合并到 main”。
- residuals: pilot 效果验证的既有 `PENDING` 与仍处于 active 的应用根目录 change 不属于本 cleanup change 的接受阻塞项。
