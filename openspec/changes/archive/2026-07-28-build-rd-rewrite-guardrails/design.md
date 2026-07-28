## Context

唯一执行依据是 `docs/superpowers/specs/2026-07-15-rd-standards-content-rewrite-plan.md`。用户已批准 G0，但当前仓库没有 `rd-rebuild` 工具、治理域或 active OpenSpec change；工作区同时已有大量未提交和未跟踪内容，不能用 clean worktree 假设，也不能用 Git HEAD 代替实际来源。

Change A 属于 Standard 本地实现。用户负责 G1 语义审查和批准，Codex 只负责工具实现、生产者自检和证据；没有独立 reviewer 时不能声称独立终审通过。Change A 不涉及用户可见产品能力、生产、外部系统或真实客户数据，因此不建立 Browser E2E 或完整应用集成环境。

阶段 A 的第一批写入发生在工具可自我保护之前。启动时已通过只读命令取得 G0 证据：Git 状态 638 条、W0–W9 共 40 个文件、来源聚合 SHA-256 为 `ac382ac1d71fae8e012b543b173e2c6eba7c1dfaabd4701c8d3633d5af5f653c`，且所有计划目标路径此前不存在。OpenSpec change 创建后、生产代码写入前，将生成 tooling bootstrap manifest，记录除 Change A 白名单外的既有工作区路径、状态和内容摘要；后续范围检查同时验证该 manifest 和来源摘要。

## Goals / Non-Goals

**Goals:**

- 实现方案第 18–23 节规定的 CLI、模块、fixture、单元测试、治理状态与事实报告。
- 用明确、可重复的结构检查阻断来源变化、范围越界、记录缺口、重复归属、无支持原则、非法状态跳转和工具异常。
- 区分结构失败、人工语义审查和工具异常；任何非零结果停止状态推进。
- 保护 G0 时已经存在的未提交修改，并证明真实 W0–W9 dry-run 前后未变化。
- 让 `status` 和报告只呈现已有事实、最后可信 gate、阻塞项和下一步。

**Non-Goals:**

- 不实现语义自动化，不产生真实原子规则、原则或草稿。
- 不开始 Change B，不进入 `sources_frozen`，不生成 G1 人工批准。
- 不修改 W0–W9、正式入口、历史 OpenSpec 主规格或其他用户资产。
- 不使用第三方依赖、网络、生产服务、外部 provider 或真实用户数据。
- 不用 commit、push、stash、reset、checkout、删除或移动来完成或回滚。

## Decisions

### 1. 单一薄 CLI 与标准库内部模块

`tools/rd_rebuild.py` 只负责 `argparse`、根目录解析、统一输出与退出码；业务逻辑按方案固定拆到 `tools/rd_rebuild_core/`：

- `model.py`：结果、状态、错误和确定性序列化；
- `baseline.py`：文件枚举、SHA-256、bootstrap/content manifest、来源验证；
- `scope.py`：阶段白名单和既有工作区状态保护；
- `records.py`：CSV/JSONL 读取与 inventory、segment、rule、classification、rewrite 基础校验；
- `coverage.py`：处理状态、目标映射和覆盖聚合；
- `principles.py`：原则支持关系和仅提示型工具词检测；
- `drafts.py`：四分类、十一项、必需章节和权威引用结构；
- `gates.py`：状态机、前置 gate、审批需求和原子状态写入；
- `report.py`：只从检查结果与记录聚合事实报告。

替代方案是单文件脚本，启动更快但会把来源保护、CSV 语义、状态写入和报告混在一个不可审查边界中；不采用。也不新增框架或 schema 库，避免一次性工具依赖和隐式行为。

### 2. 一个结果模型决定输出与退出码

所有检查返回结构化 `CheckResult`，字段至少包括 `status`、`summary`、`findings` 和 `evidence`，序列化时补充固定 `exit_code`；`next_action` 由状态和报告证据明确给出。聚合优先级固定为 `TOOL_ERROR > BLOCKED > REVIEW_REQUIRED > WARN > PASS`，退出码固定：

- `0`：`PASS` 或仅 `WARN`；
- `1`：`BLOCKED`；
- `2`：`REVIEW_REQUIRED`；
- `3`：`TOOL_ERROR`。

未运行和跳过不会被计为 PASS。预期政策失败转换为 `BLOCKED` 或 `REVIEW_REQUIRED`；未预期异常由 CLI 顶层转为 `TOOL_ERROR` 并保留诊断，不能返回 0。

### 3. 政策先于检查，白名单使用精确前缀

`governance/rd-standards-rebuild/policy.json` 是机器政策入口，至少包含方案要求的字段，并把阶段 A 白名单限制为：

- `tools/rd_rebuild.py`；
- `tools/rd_rebuild_core/`；
- `tools/fixtures/rd_rebuild/`；
- `tools/test_rd_rebuild_*.py`；
- `openspec/changes/build-rd-rewrite-guardrails/`；
- `governance/project-map.json`；
- `governance/current-status.json`；
- `governance/rd-standards-rebuild/`。

通配只允许测试文件名模式，不把整个 `tools/`、`openspec/changes/` 或 `governance/` 视为可写。W0–W9 同时列为 source roots 和 protected roots。内容阶段白名单仅在政策中声明供 fixture/未来 Change B 使用，G1 前不会激活。

替代方案是只看 `git status` 是否干净；它会把用户既有 638 条状态误报为本 change，也无法保护未跟踪文件内容，因此不采用。

### 4. bootstrap manifest 与 G2 内容基线分离

`baseline-manifest.json` 在阶段 A 使用 `kind=tooling-bootstrap`：记录 G0 既有脏路径/状态/内容 SHA-256、W0–W9 文件清单和哈希、目标路径初始不存在证据、方案路径和捕获时间。它只支持 tooling scope 与来源不变性检查，不代表 `sources_frozen`，也不能作为 G2 通过证据。

`baseline-create --dry-run` 对真实仓库只展示计划读取、计划写入和摘要，不改写 manifest。未来 G1 获批后，Change B 才能通过非 dry-run 创建 `kind=content-frozen` 的独立内容基线，并记录冻结工具 manifest；本 change 不执行该动作。

为防止“重建 baseline 让失败变绿”，已有 manifest 默认不可覆盖；只有与政策声明的合法下一阶段一致并经过 gate 的新 kind 才能创建。Change A 测试覆盖拒绝任意覆盖和 dry-run 零写入。

### 5. 记录检查只判定机器事实

CSV 使用 Python `csv` 标准库并要求精确必填字段。检查器只判定：

- inventory 的来源唯一性、完整性和 review 状态；
- segment 的行号、连续覆盖、空洞/重叠/越界及 rule-bearing 引用；
- rule 的字段、ID、来源、行号、枚举和初始/最终 treatment；
- classification 的唯一主归属和合法 secondary 引用；
- rewrite 的目标映射、retire 逐条理由及复制阈值事实；
- principle 的支持关系、分类覆盖和工具词风险；
- draft 的目录、章节、四分类、十一项和权威引用结构。

归属是否正确、规则是否同义、原则是否根本、技术细节是否有效、退出是否可接受只返回 `REVIEW_REQUIRED` 或 `WARN`，不自动修改记录。

### 6. gate 是唯一状态写入者

`run-state.json` 仅允许方案规定的十个状态；Change A 实际最多从 `planned` 进入 `tooling_ready`。`gate` 在一次运行中先验证当前状态、所需检查、manifest、审批要求和证据新鲜度，再通过临时文件同目录替换原子写入状态。异常发生在替换前不得提升状态。

G1 的自动部分通过后，工具只能报告 `REVIEW_REQUIRED` 和 pending 用户审查；它不得把状态写成 `tooling_ready`。只有从 `approvals.jsonl` 读取到与当前 scope SHA-256 匹配、由用户明确决定并由 Codex忠实记录的 G1 `approved` 事件后，gate 才能转换。Change A 交付时不会伪造该事件，因而停在 `planned` 加“G1 自动证据就绪/等待用户”。

替代方案是让单元测试通过即自动进入 `tooling_ready`；这违反人工批准门，不采用。

### 7. 报告只聚合可追溯事实

`report-build` 读取 manifest、run-state、审批事件、检查结果和账本；每个计数同时给出来源文件/记录类型和可复算过滤条件。缺少输入时报告 `BLOCKED`，语义未决时列为 `REVIEW_REQUIRED`，不生成“原则正确”“内容完整”等结论。

dry-run 不写报告。非 dry-run 的 G1 事实报告写入固定类型文件，内容阶段报告同时写入 `rebuild-draft/review/` 和 `governance/rd-standards-rebuild/reports/`；报告正文记录输入摘要且不写入时间戳，重复运行同一输入应得到相同内容。

### 8. TDD、fixture 与证据层级

每项行为先写一个失败测试并运行观察预期失败，再写最小实现。合成 fixture 覆盖：valid、source changed、line gap、duplicate owner、unsupported principle、unauthorized write；测试内再构造缺字段、越界、复制、无目标、非法 gate、缺批准、异常和中止恢复。

证据只声明为 Python unit/fixture、CLI dry-run、仓库静态验证和 OpenSpec strict validation。没有独立 reviewer、Browser E2E、完整应用集成或生产观察，不能扩张声明。

### 9. G2 后工具恢复使用跨平台启动器与追加式换版链

G8 dry-run 暴露的 `openspec-strict: TOOL_ERROR` 是 Windows 进程启动缺陷：交互式 PowerShell 可以解析 `openspec.ps1`，Python `shutil.which("openspec")` 则解析 npm 的 `openspec.CMD`，而 `subprocess.run(["openspec", ...], shell=False)` 无法直接启动该 wrapper。恢复实现必须先用 `shutil.which` 解析实际入口；普通可执行文件和 POSIX 入口使用参数列表直接启动。Windows `.cmd`/`.bat` 使用 `executable=COMSPEC`、`shell=False` 和完全固定的 `cmd.exe /d /s /v:off /c` 命令文本；wrapper 路径及经严格标识符校验的 change 名只通过子进程专用环境变量进入双引号参数位置，从而让含空格或 `&` 等元字符的合法 wrapper 路径仍保持单一参数边界，且不能形成额外命令。

原 G2 content-frozen baseline 及其工具摘要保持不可变且不可通过“同时重写 baseline 与工具 manifest”重新绑定。content scope 无条件核对原 baseline 文件 SHA-256、原工具摘要、来源摘要和实施前 bootstrap SHA-256 四个代码内固定锚点，并要求调用者传入的 baseline 与磁盘原件完全一致。替换工具只能通过固定文件 `governance/rd-standards-rebuild/reports/2026-07-19-tool-recovery-manifest.json` 建立追加式换版链。该记录必须包含恢复 ID、失败报告、旧/新工具 manifest 摘要、来源摘要、bootstrap 报告摘要、保护聚合的路径与 Git 状态计数/摘要、G8 后冻结工作区摘要、精确允许路径、实际变更文件、全部验证结果、生产者自检、独立审查结论和用户重新 G1 验收事件。

恢复范围不能由恢复记录自行扩张：检查器只接受本设计固定的两个生产文件、两个测试文件、Change A 目录、工具 manifest、审批日志及两份固定恢复报告。它必须重算 whitelist 之外的全部路径内容摘要和 Git 状态摘要，并与批准实施前的 bootstrap 报告完全一致。来源摘要必须仍为 `ac382ac1d71fae8e012b543b173e2c6eba7c1dfaabd4701c8d3633d5af5f653c`。在 `audit_ready/G7` 仍核对实施前完整保护快照；恢复记录另冻结“除恢复白名单与 `run-state.json` 外的完整工作区”，并在 `audit_ready/G7`、`awaiting_user_review/G8`、`approved_for_migration_design/G9` 三个合法状态持续核对，因此 G8/G9 的状态或审批变化不会掩盖 `rebuild-draft` 等语义内容漂移。每次 gate 转换先验证当前状态与 `last_passed_gate` 成对；G9 的实时检查集合必须再次调用 content scope，因此调用者不能凭一条用户审批绕过状态配对或 G8 后冻结工作区核验。

恢复有两个不同人工事件：当前 `G1R` 事件只授权实现和验证；替换工具完成全量验证与独立只读审查后，仍须用户明确重新接受 G1。恢复记录中的实施授权对象和预先固定的 renewed-G1 `approval_id` 都纳入 canonical 审批范围摘要；renewed-G1 的审批 ID 必须不同于固定实施授权 ID，改绑 ID 必须改变摘要。审批日志的每条记录至少包含方案规定的八个字段；基础日志允许历史 G0 的 `decided_at: null`，但真正用于推进 gate 的事件必须有非空字符串决定时间。无效 JSON、非对象行、缺字段、字段类型错误、重复 ID 或同 gate/scope 多事件都是确定性治理数据失败，统一返回 `BLOCKED` 且不能回退选择较早的 approved 事件；只有实际文件 I/O 或运行时异常才返回 `TOOL_ERROR`。生产者自检和独立审查都必须用非空 JSON 字符串声明身份，不能把 `null`、对象、数组或其他类型强制转换成伪身份；去除首尾空白并忽略大小写后仍必须是不同主体。独立审查的 critical/important/minor 只有精确的整数 `0` 才表示零发现，布尔值和浮点零均无效。只有第二个、与恢复记录及候选工具摘要绑定的人工事件存在时，才能把恢复记录标为 `approved`、更新工具 manifest，并让内容范围检查接受“旧基线摘要 → 新工具摘要”的精确替换。任何缺失、未批准、摘要不符、范围聚合变化或来源变化都返回 `BLOCKED`；启动器本身无法运行则返回 `TOOL_ERROR`。在重新验收与最终换版完成前不得推进 G8 状态。

## Risks / Trade-offs

- [启动时工具尚不存在，无法自护第一次写入] → 在生产代码前保存 tooling bootstrap manifest；用 G0 Git 状态摘要、目标初始不存在证据和 W0–W9 来源摘要做交叉核对，并把这项 bootstrap 限制写入最终 G1 风险。
- [Git status 对未跟踪文件内容变化不敏感] → bootstrap manifest 对每个既有未跟踪/修改路径记录内容 SHA-256，而不是只记录 porcelain 状态。
- [工具试图做语义判断导致假确定性] → 将语义问题固定为 `REVIEW_REQUIRED/WARN`，CLI 不提供 auto/approve/migrate/delete 类命令。
- [报告或 gate 异常留下虚假较高状态] → 先算后写、同目录临时文件原子替换、异常测试验证状态不提升。
- [fixture 被修改来迎合实现] → fixture 目的、预期状态和失败码写入测试；最终审查同时核对 fixture 与 spec，不把测试通过单独视为正确。
- [对全工作区哈希成本较高] → tooling scope 只哈希 G0 脏/未跟踪路径和保护来源；内容基线再按政策枚举必要范围。规模当前为 40 个来源文件，可接受。
- [同一生产者无法提供独立最终审查] → 完成 producer self-check 后明确标记 independent review 未覆盖，由用户执行 G1 语义审查。
- [G2 后修复可能通过重写旧基线掩盖工具变化] → 旧 baseline 永不覆盖；只接受绑定旧/新摘要、保护聚合、独立审查和用户重新 G1 验收的追加式恢复记录。
- [恢复记录可以把任意路径加入 whitelist 自我授权] → 允许路径固定在本 design 与检查器中，记录只能逐项匹配，不能扩张；whitelist 外路径和 Git 状态必须重算并与实施前 bootstrap 摘要一致。
- [baseline 与候选 manifest 同时重写可跳过恢复] → 原 baseline 文件、原工具摘要、来源摘要与 bootstrap 摘要成为代码内固定锚点，content scope 无条件校验，不以可变 baseline 决定是否启动恢复。
- [G8 后合法状态变化掩盖语义漂移] → 单独冻结除恢复文件和 run-state 外的完整工作区，并强制 state/last gate 成对。
- [生产者冒充独立 reviewer 或复用实施授权] → 归一化后拒绝相同 reviewer 身份，并要求 renewed-G1 ID 与固定实施授权 ID 不同；两者均进入审批范围摘要。
- [审批 ID 可改绑、残缺或冲突事件可被选择] → canonical scope 纳入预定 renewed-G1 ID；统一校验八字段、ID 唯一性和同 gate/scope 单一事件，异常一律 BLOCKED。
- [非法 approval JSON 被误报为工具故障] → 语法错误和非对象记录按确定性 schema 失败返回 BLOCKED；仅真实 I/O/运行时异常使用 TOOL_ERROR。
- [JSON 布尔/浮点零冒充零审查发现] → finding count 必须是非布尔的精确整数零。

## Migration Plan

1. 生成并 strict validate 本 change 的 proposal、spec、design 和 tasks。
2. 写入 tooling bootstrap manifest、policy 和初始 `planned` 状态，不改变 W0–W9。
3. 按 TDD 小批次实现 baseline/scope、记录检查、gate 和报告。
4. 运行合成 fixture、全量单元测试、真实只读 dry-run、来源与范围验证、仓库既有验证和 OpenSpec strict validation。
5. 生成 G1 事实报告和 producer self-check，保持 G1 为 pending，停止写入等待用户。
6. 若 G2 后出现工具自身缺陷，只在用户批准的固定恢复范围内回到本 Change A：先记录失败与保护聚合，再按 TDD 修复、重跑全部 G1 验证、取得新的独立只读审查与用户重新 G1 验收，最后以追加式恢复记录换版；恢复前后均不覆盖旧基线。

无需部署或数据迁移。若工具失败，只停止使用并保留现有证据；未经用户另行授权不删除文件或执行 Git 恢复。修复必须在 Change A 内按失败测试继续，并重新运行全部 G1 验证。

## Open Questions

- G1 的语义审查与批准仍需用户在工具、命令、测试证据和剩余限制形成后明确给出。
- 独立 final review 当前没有未参与生产的 reviewer；本 change 只能完成 producer self-check 和用户 G1 审查，不能把二者写成独立 review。
- 本次 G2 后恢复的替换工具尚未完成实现、全量验证、独立审查或用户重新 G1 验收；当前用户批准仅授权执行恢复协议。
