# OpenSpec archive decision — 2026-07-10

Decision source：decisions/2026-07-10-rd-standards-reset.md。
Reason：58 个 change 已全部完成但仍处于 active，导致工作状态失真。

## Delta coverage audit

- Delta specs：58；
- 已存在对应主 spec：57；
- Requirement 名称已被主 spec 覆盖：56；
- 未进入主 spec 的两个 change：
  - add-operating-model-and-agent-orchestration / agent-operating-model；
  - add-role-swimlanes-and-simplify-standards / rd-standards-navigation 的旧角色路由修改。

这两个 delta 已被当前“最小内核 + 三档风险路径 + 可选角色视角”方向取代，不应同步为现行主规格。

## Action

全部 completed changes 使用 --skip-specs 归档：

- 其余 56 个 change 的 requirement 已在主 specs 中；
- 两个未覆盖 delta 被明确 supersede；
- archive 保留 proposal、design、tasks 和 delta specs 作为历史证据。

归档后，openspec/changes 根目录不应保留 completed active change。

## Result

- attempted：58；
- archived：58；
- failed：0；
- active after archive：0；
- archived directory count：58；
- main specs validation：56 passed，0 failed。
