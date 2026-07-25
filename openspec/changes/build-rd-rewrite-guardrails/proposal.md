## Why

研发规范内容重写需要先有可验证的范围保护、来源基线、记录校验和状态门禁，否则 Codex 无法可靠发现来源变化、未授权写入、账本缺口或人工批准被跳过。用户已批准 `docs/superpowers/specs/2026-07-15-rd-standards-content-rewrite-plan.md` 的 G0，因此现在只建设并验收该方案定义的阶段 A 工具。

## What Changes

- 新增仅使用 Python 标准库的 `rd-rebuild` CLI、内部模块、合成 fixture 与 `unittest` 测试。
- 新增机器可读政策、治理当前状态、运行状态、来源与工具 manifest、人工批准记录结构和事实聚合报告。
- 新增来源保护、增量写入范围、语义账本结构、唯一归属、目标映射、原则追溯、草稿结构、状态转换和报告一致性检查。
- 为 `PASS`、`WARN`、`REVIEW_REQUIRED`、`BLOCKED`、`TOOL_ERROR` 固定输出语义和退出码，并确保 dry-run 不产生后续 gate 可复用的通过证据。
- 使用合成正反 fixture、单元测试、确定性/恢复测试和真实 W0–W9 只读 dry-run 验收工具。
- 支持一次受用户明确授权、范围固定且可追溯的 G2 后工具恢复：修复 Windows npm `.cmd`/`.bat` OpenSpec 启动器，并以追加式恢复记录连接不可重绑定的原 G2 baseline、原冻结工具摘要和经重新验收的替换摘要；恢复后的 G8/G9 只允许状态与审批变化，不允许语义工作区漂移。
- 在用户完成 G1 审查前停止，不创建或继续 `rewrite-rd-standards-content`。

## Non-Goals

- 不读取 W0–W9 来提取、归类、重写原子规则或形成研发原则。
- 不创建 `rebuild-draft/`，不修改、删除、移动或覆盖 `docs/W0-*` 至 `docs/W9-*`。
- 不修改正式入口，不执行最终迁移，不创建 Change B，不 archive OpenSpec change。
- 不自动归类、生成原则、退出规则、批准 gate、迁移或删除内容。
- 不新增第三方运行时依赖，不执行 commit、push、stash、reset 或 checkout。
- 不把格式校验、脚本通过或 Codex 自检写成用户批准或独立审查。
- 工具恢复期间不修改内容语义、内容账本、重写草稿、正式入口或状态机状态；用户对恢复实施方案的批准不等于对替换工具的重新 G1 验收。

## Capabilities

### New Capabilities

- `rd-rewrite-guardrails`: 保护研发规范重写来源和写入范围，校验机器记录与状态转换，并生成可追溯的结构化审查证据。

### Modified Capabilities

无。

## Impact

- 新增范围限于 `tools/rd_rebuild.py`、`tools/rd_rebuild_core/`、`tools/fixtures/rd_rebuild/`、`tools/test_rd_rebuild_*.py`、本 change 与 `governance/rd-standards-rebuild/`，并按方案登记 `governance/project-map.json` 与 `governance/current-status.json`。
- 真实 W0–W9 在阶段 A 中只被读取、哈希和 dry-run；其 G0 聚合来源指纹为 `ac382ac1d71fae8e012b543b173e2c6eba7c1dfaabd4701c8d3633d5af5f653c`，共 40 个文件。
- 当前工作区在 G0 已有 638 个 Git 状态条目；工具必须保留这些既有修改，并只按 G0 状态与 Change A 精确白名单检查新增差异。
- 运行时仅依赖 Python 标准库和仓库已有 OpenSpec CLI；不调用生产、外部供应商、真实客户数据或网络服务。
- 本次窄范围恢复只允许修改 `tools/rd_rebuild_core/gates.py`、`tools/rd_rebuild_core/scope.py`、对应的两个测试文件、本 Change A、工具 manifest、审批日志和两份固定恢复报告；恢复快照之外的工作区必须保持摘要与 Git 状态一致，原 G2 baseline 文件及其工具/来源摘要必须匹配代码内固定锚点，生产者与独立审查者、实施授权与 renewed-G1 接受必须分别为不同主体和不同事件。
- 回滚仅指停止使用并保留阶段 A 新增文件供审查；未经用户另行授权不通过 Git 重置、删除或移动来回滚。
