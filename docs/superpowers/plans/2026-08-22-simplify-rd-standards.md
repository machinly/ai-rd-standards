# 研发规范整体精简实施计划

> **For agentic workers:** 本次由当前会话内联执行，不派生子 Agent。若后续跨会话恢复，先读取本计划和根 `WORKFLOW.md`，再从未完成复选框继续。

**Goal:** 用一个短小、显式启用的研发工作约定替换当前四分类十一项、2,337 条正式规则和硬编码追溯门禁，同时保留真实的授权、安全、恢复和证据边界。

**Architecture:** `WORKFLOW.md` 成为唯一正式规范，`README.md` 只负责范围和导航，`skills/opc-rd/SKILL.md` 是显式调用的薄适配器。OpenSpec 只承载确有长期契约价值的活动变更；一个新的结构检查器只检查入口、链接、内容预算、退出边界和活动状态，不检查固定措辞或历史规则数量。

**Tech Stack:** Markdown、Python 3 标准库、OpenSpec YAML 配置、Git 恢复。

**Spec:** 根 `WORKFLOW.md` 承载最终批准的十条精简内核；本计划保存实现边界和验证证据。旧重建设计只通过恢复基线中的 Git 历史追溯，不再作为活动文件。

## Global Constraints

- 恢复基线固定为 Git 提交 `be7703a2c0c2ea90a495bcbf65a954874eb5b11a`，执行前工作树必须干净。
- 不提交、不推送、不 stash、不 reset、不 checkout。
- 新规范仅在用户明确调用 `$opc-rd` 或明确要求使用本规范时启用。
- 默认不创建额外规格、计划、审查、Agent 或治理状态；只有真实长期契约或高影响风险需要时才增加。
- 生产、客户数据、凭据、权限、资金、外部通信、删除或不可逆副作用仍需当次明确授权和可行恢复路径。
- `README.md + WORKFLOW.md` 默认阅读不超过 200 个物理行；`README.md + WORKFLOW.md + skills/opc-rd/SKILL.md` 不超过 350 个物理行。
- Go、Kratos、MySQL、sqlc、Vite、React 和目录布局仅作为可选个人技术偏好，不进入正式工作流。
- 旧正文、账本、历史审查和失效 change 从活动工作树退出，由 Git 历史恢复。

---

### Task 1: 建立唯一正式入口与行为场景

**Files:**
- Create: `WORKFLOW.md`
- Rewrite: `README.md`
- Rewrite: `openspec/README.md`
- Modify: `openspec/config.yaml`
- Test: `tools/test_check_workflow.py`

**Interfaces:**
- Consumes: 用户批准的十条精简内核。
- Produces: 唯一正式入口 `WORKFLOW.md`，以及场景验收所依赖的稳定路由语义。

- [x] **Step 1: 写出行为测试**

  测试必须覆盖：必要入口、内容预算、README 链接、旧正式目录拒绝、无重复状态、活动 OpenSpec change 最小文件、以及不硬编码规则数量。

- [x] **Step 2: 运行测试并确认旧仓库失败**

  Run: `python tools/test_check_workflow.py -v`

  Expected: 因 `WORKFLOW.md` 不存在、旧正式目录仍存在而失败。

- [x] **Step 3: 写入新入口**

  `WORKFLOW.md` 只包含：显式适用、默认直接执行、OpenSpec 触发条件、人类决定、高影响授权、保护范围、按风险验证、按风险审查、单一事实源、技术栈分离和完成报告。

- [x] **Step 4: 更新 README 和 OpenSpec 边界**

  `README.md` 只解释用途、三问路由、文件地图和一个验证命令；OpenSpec 不再使用 Standard/High-risk 术语。

- [x] **Step 5: 运行行为测试**

  Run: `python tools/test_check_workflow.py -v`

  Expected: 在旧目录尚未删除时，只剩退出边界相关失败。

### Task 2: 用轻量检查器替换规则数量门禁

**Files:**
- Create: `tools/check_workflow.py`
- Test: `tools/test_check_workflow.py`
- Delete: `tools/verify_rd_standards.py`
- Delete: `tools/test_current_rd_standards.py`
- Delete: 其余旧治理、pilot、runtime 同步检查器及测试。

**Interfaces:**
- Consumes: Task 1 的入口和内容预算。
- Produces: `validate_repository(root: Path) -> dict[str, object]` 与 CLI 退出码 0/1。

- [x] **Step 1: 实现最小检查器**

  检查：UTF-8 入口、Markdown 本地链接、内容预算、退役路径不存在、`openspec/config.yaml` 非空、每个 active change 包含 `proposal.md` 与 `tasks.md`、不存在 `governance/current-status.json` 竞争状态。

- [x] **Step 2: 运行单元测试**

  Run: `python tools/test_check_workflow.py -v`

  Expected: 全部通过。

- [x] **Step 3: 运行真实仓库检查**

  Run: `python tools/check_workflow.py .`

  Expected: 删除旧路径前准确列出退出项；不得因规则数量或固定中文句子失败。

### Task 3: 退出旧正文、账本、历史状态和失效 change

**Files:**
- Delete: `docs/01-initiation/`
- Delete: `docs/02-product-design/`
- Delete: `docs/03-engineering-delivery/`
- Delete: `docs/04-operations-maintenance/`
- Delete: `docs/execution-details.md`
- Delete: `docs/roles/`
- Delete: `docs/sources/`
- Delete: `docs/superpowers/specs/`
- Delete: `decisions/`, `experiments/`, `governance/`, `knowledge/`, `reviews/`
- Delete: `openspec/changes/`
- Delete: `skills/opc-rd/references/workflow-map.md`
- Delete: `skills/opc-rd/references/review-rubric.md`
- Delete: `skills/opc-rd/references/superpowers-scope.md`
- Keep: `skills/opc-rd/references/stack-defaults.md`，明确为可选个人偏好。
- Modify: `skills/opc-rd/agents/openai.yaml`，加入 `allow_implicit_invocation: false`。

**Interfaces:**
- Consumes: Git 恢复基线与 Task 1/2 的新入口。
- Produces: 无第二套正式正文、无历史状态竞争、无旧 runtime 路由引用的活动工作树。

- [x] **Step 1: 再次解析并核对所有删除目标**

  每个递归目标的绝对路径必须位于 `D:\Workspace\研发规范`，且不得包含仓库根、`.git`、`.superpowers` 或未列出的用户目录。

- [x] **Step 2: 执行可由 Git 恢复的批量退出**

  只删除本任务明确列出的 tracked 路径；不触碰忽略的 `.superpowers/` 本地状态。

- [x] **Step 3: 校验技能包**

  Run: `python C:\Users\machinly\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\opc-rd`

  Expected: skill frontmatter、名称和 UI 元数据有效；引用目录中只保留真实需要的技术偏好。

### Task 4: 完整验证与交付盘点

**Files:**
- Modify only if verification exposes a defect: `README.md`, `WORKFLOW.md`, `openspec/README.md`, `openspec/config.yaml`, `tools/check_workflow.py`, `tools/test_check_workflow.py`, `skills/opc-rd/agents/openai.yaml`。

**Interfaces:**
- Consumes: Task 1–3 的完整候选。
- Produces: 可复现检查结果、变更清单、恢复方式和剩余风险。

- [x] **Step 1: 运行所有新测试**

  Run: `python tools/test_check_workflow.py -v`

  Expected: PASS。

- [x] **Step 2: 运行真实仓库检查**

  Run: `python tools/check_workflow.py .`

  Expected: `WORKFLOW_CHECK=PASS`。

- [x] **Step 3: 验证 OpenSpec 结构**

  Run: `openspec validate --all --strict --no-interactive`

  Expected: 没有活动 change 时正常报告 0 个失败；若 CLI 不接受空工作区，则准确记录工具边界而不恢复旧 change。

- [x] **Step 4: 检查 Markdown 链接、diff 和工作树范围**

  Run: `git diff --check`

  Expected: 退出码 0；所有变更都位于本计划列出的路径。

- [x] **Step 5: 记录规模变化和恢复说明**

  报告整改前后的活动规范文件数、行数、规则 ID 数，注明所有删除均可从 `be7703a2c0c2ea90a495bcbf65a954874eb5b11a` 恢复，并明确未 commit、未 push。

## Self-Review

- Spec coverage：唯一入口、显式启用、直接执行、OpenSpec 边界、高影响授权、技术栈分离、历史退出、轻量检查、恢复和验证均有任务覆盖。
- Placeholder scan：无 TBD、TODO 或未定义实现项。
- Interface consistency：检查器入口统一为 `validate_repository(root)`，CLI 统一为 `python tools/check_workflow.py .`。
- Commit boundary：按用户边界省略所有 commit 步骤；Git 仅作为读取和恢复来源。
