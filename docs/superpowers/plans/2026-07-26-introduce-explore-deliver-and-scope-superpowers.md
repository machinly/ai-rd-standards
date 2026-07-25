# Introduce Explore / Deliver and Scope Superpowers Implementation Plan

> **For implementers:** This plan exists because the change crosses formal standards, OpenSpec capabilities, governance ledgers, runtime routing, and user-level Codex instructions. It is a fixed implementation recipe, not a second status source. After Task 2 creates the OpenSpec change, update only that change's `tasks.md` for live status. Do not automatically invoke `executing-plans`, worktrees, subagents, or review skills; apply the approved Superpowers complexity gate first. Independent review requires a genuinely separate reviewer and must not be self-declared.

**Goal:** 让研发规范先排除非研发任务，再把研发工作分为 `Explore / Deliver`；仅在 Deliver 中使用 `Quick / Standard / High-risk`，并把 Superpowers 收窄为复杂问题的按需工具箱。

**Architecture:** 根入口拥有 R&D applicability 与一级路由；调研、定义、体验设计、技术设计、计划、实现、验证和评估分别拥有 Explore 的局部语义；Deliver 继续消费现有 OpenSpec、visual UX、验证和审查门禁。`one-person-openspec-rd` 是薄运行时路由，用户级 `~/.codex/AGENTS.md` 部署跨任务生效的 Superpowers 作用域。已确认设计是决策依据，新 OpenSpec change 是本次增量合同和执行状态，正式正文是运行规则，治理账本只做历史追溯。

**Tech Stack:** Markdown、OpenSpec CLI 1.2.0、Python 3 标准库 `unittest`、CSV/JSON 治理账本、PowerShell、Codex user-level `AGENTS.md`。

## Baseline and non-negotiable constraints

- 唯一设计依据是 `docs/superpowers/specs/2026-07-26-rd-explore-deliver-superpowers-scope-design.md`。
- 当前基线已经通过：102 个单测、2,321 个正式 rule-id、5,956 条原子来源、59 个 OpenSpec items。
- `add-visual-ux-step-to-rd-standards` 已完成并独立接受，但尚未归档；新 change 创建前必须先归档。
- `build-rd-rewrite-guardrails` 与 `rewrite-rd-standards-content` 仍是历史 active changes，但各自只拥有 `rd-rewrite-guardrails`、`rd-standards-content-rewrite` capability，不与本次四个 capability 重叠；本轮不修改或替它们补状态。
- `.superpowers/` 是任务开始前已有的未跟踪目录。本计划和后续实施都不得读取后改写、删除、清理或 stage 它。
- 不新增第五分类或第十二项目，不新增通用流程平台、dashboard、routing engine 或 pilot schema。
- `governance/rd-standards/replacement-manifest.json` 是 2026-07-20 替换事件的历史证据，其中 2,313/5,956 保持不变；当前数字写入 README、verifier 和 `governance/current-status.json`。
- `atomic-rules.csv` 与 `coverage-matrix.csv` 都保持 5,956 行；只细化既有来源到新正式目标的映射。
- 不直接修改 `C:\Users\machinly\.codex\plugins\cache\...` 下的 Superpowers 插件。
- 用户级 `C:\Users\machinly\.codex\AGENTS.md` 当前为空，但写入前仍须重新读取；只维护带起止标记的本规则块，保留未来出现的其他用户内容。
- 官方 Codex manual 确认 `~/.codex/AGENTS.md` 是跨仓库个人默认值，但更靠近当前目录的 repo/nested `AGENTS.md` 优先。因此 global block 是默认部署，不是对冲突项目文件的机械覆盖；Task 11 必须检查目标仓库的适用指令链。参考：[AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。
- 当前工作没有并行写域，也不需要隔离长期分支；默认在现有 checkout 原地实施，不调用 worktree 或多 Agent。
- 每个提交前使用 `git diff --check`、精确 `git status --short -- <paths>` 和 `git diff --cached --name-only`。任何 staged path 超出该任务清单时停止。

---

### Task 1: 归档已完成的 visual UX change

**Files:**

- Move via OpenSpec: `openspec/changes/add-visual-ux-step-to-rd-standards/`
- Create via OpenSpec: `openspec/changes/archive/2026-07-26-add-visual-ux-step-to-rd-standards/`
- Modify via OpenSpec:
  - `openspec/specs/accessibility-ai-ux-standard/spec.md`
  - `openspec/specs/ai-coding-workflow-standard/spec.md`
  - `openspec/specs/testing-quality-standard/spec.md`

- [ ] **Step 1: 重新证明归档前置条件**

Run:

```powershell
git status --short
openspec list
openspec status --change add-visual-ux-step-to-rd-standards --json
openspec validate add-visual-ux-step-to-rd-standards --strict --no-interactive
Get-Content -Raw openspec/changes/add-visual-ux-step-to-rd-standards/review.md
rg -n "visual_ux|静态可视|wireframes" openspec/specs/accessibility-ai-ux-standard/spec.md openspec/specs/ai-coding-workflow-standard/spec.md openspec/specs/testing-quality-standard/spec.md
```

Expected:

- status 为 `isComplete: true`；
- strict validation 通过；
- review decision 为 `accept`；
- 三个 base spec 尚未包含本 change 的五项 requirement；
- 另外两个 active historical changes 不包含本次四个 modified capability；
- workspace 只有任务开始前的 `?? .superpowers/`。

若 base spec 已出现相同 requirement，先逐项比较 active delta 与 base；只有完全等价且能解释来源时才考虑 `--skip-specs`。当前基线预期使用普通归档，不使用 `--skip-specs`。

- [ ] **Step 2: 执行普通归档**

Run:

```powershell
openspec archive add-visual-ux-step-to-rd-standards -y
```

Expected: active change 被移动到日期化 archive，五项 delta 合并进三个 base spec。

- [ ] **Step 3: 验证归档结果**

Run:

```powershell
openspec list
openspec validate --all --strict --no-interactive
rg -n "可视 UX 适用性必须在生产性实现前判定|AI 实现必须消费已批准的可视 UX 输入|Required 可视 UX 必须以浏览器证据核对已批准方案" openspec/specs
git diff --check
```

Expected: visual UX change 不再 active；三个 requirement 均在对应 base spec；OpenSpec 总数暂时从 59 变为 58，全部通过。

- [ ] **Step 4: 提交归档**

```powershell
git add -A -- openspec/changes/add-visual-ux-step-to-rd-standards openspec/changes/archive/2026-07-26-add-visual-ux-step-to-rd-standards openspec/specs/accessibility-ai-ux-standard/spec.md openspec/specs/ai-coding-workflow-standard/spec.md openspec/specs/testing-quality-standard/spec.md
git diff --cached --name-only
git commit -m "openspec: archive completed visual UX change"
```

Expected staged paths 只包含本任务列出的 archive 和三个 base spec；不得包含 `.superpowers/`。

---

### Task 2: 创建 Explore / Deliver Standard change

**Files:**

- Create: `openspec/changes/introduce-explore-deliver-and-scope-superpowers/proposal.md`
- Create: `openspec/changes/introduce-explore-deliver-and-scope-superpowers/design.md`
- Create: `openspec/changes/introduce-explore-deliver-and-scope-superpowers/tasks.md`
- Create:
  - `openspec/changes/introduce-explore-deliver-and-scope-superpowers/specs/one-person-rd-governance/spec.md`
  - `openspec/changes/introduce-explore-deliver-and-scope-superpowers/specs/rd-standards-navigation/spec.md`
  - `openspec/changes/introduce-explore-deliver-and-scope-superpowers/specs/ai-coding-workflow-standard/spec.md`
  - `openspec/changes/introduce-explore-deliver-and-scope-superpowers/specs/testing-quality-standard/spec.md`

- [ ] **Step 1: 使用 CLI 创建 change**

```powershell
openspec new change introduce-explore-deliver-and-scope-superpowers --description "Add R&D applicability, Explore/Deliver routing, and a complexity-gated Superpowers scope."
openspec status --change introduce-explore-deliver-and-scope-superpowers --json
```

- [ ] **Step 2: 写 proposal，明确范围而不复制设计**

`proposal.md` 至少包含：

```markdown
## Why

第三轮实验在 46.7 小时和 102 次提交后仍只有一条完整关键旅程，说明现行入口把本地合成学习任务过早产品化，并让可选复杂方法自动膨胀为全流程。与此同时，非研发任务缺少直接退出条件。

本 change 落实已确认设计 `docs/superpowers/specs/2026-07-26-rd-explore-deliver-superpowers-scope-design.md`；设计文档保留论证，本 change 只描述正式增量。

## Routing

- path: Standard
- visual_ux: not-required
- reason: 本 change 修改研发规范、治理和运行时路由，不新增或改变产品用户界面。

## What Changes

- 在任何研发读取和风险路由前增加 R&D applicability。
- 把研发一级工作模式改为 Explore / Deliver；Explore 使用 Product Discovery、UX Prototype、Technical Spike，Deliver 保留 Quick、Standard、High-risk。
- 为轻量 Explore 增加 sandbox、Walking Skeleton、5 个 active tasks、120 分钟或 5 次提交 showcase、2 小时无可见事实即缩小或停止、选择性 TDD 和 promote 边界。
- 把 Superpowers 改为复杂度触发、最小 skill 集、禁止自动串联的可选工具箱。
- 更新正式规范、运行时 skill、用户级 Codex instruction、治理映射、知识入口与回归测试。

## Non-Goals

- 不把 Prototype 增加为第四个风险路径。
- 不让非研发任务创建 OpenSpec 或研发治理工件。
- 不降低真实生产、数据、凭据、付款、外部通信和不可逆副作用门禁。
- 不修改 Superpowers 插件缓存，不建设 routing engine、新 schema 或流程平台。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `one-person-rd-governance`
- `rd-standards-navigation`
- `ai-coding-workflow-standard`
- `testing-quality-standard`
```

- [ ] **Step 3: 写 change design**

`design.md` 只锁定实现责任：

- 根 README/选题拥有 R&D applicability、Explore/Deliver 和 Superpowers complexity gate；
- 调研拥有 Product Discovery 与 Explore sandbox，定义拥有 promote 决定；
- 体验设计区分 Explore 的 UX Prototype 与 Deliver 的 formal visual UX；
- 技术设计拥有 Technical Spike/Walking Skeleton，计划拥有 WIP 与 showcase cadence；
- 实现拥有选择性 TDD，验证拥有人类可识别 fixture 与 showcase 证据命名；
- 评估拥有 Explore outcome 与 process net benefit；
- `tasks.md` 是 change 状态权威，设计文档和本计划不得复制 live status；
- 用户级 `AGENTS.md` 是 Superpowers 跨任务运行时部署，repo skill 是 R&D 路由；
- 回滚通过后续 Standard change 完成，不删除历史证据。

- [ ] **Step 4: 写四个 capability delta**

使用下列 requirement 标题和边界。`MODIFIED` 标题必须与归档后的 base spec 完全相同，并包含完整更新后的 requirement 与全部仍有效 scenario。

`one-person-rd-governance`：

```text
ADDED     研发规范必须先判定适用性
ADDED     研发工作必须区分 Explore 与 Deliver
ADDED     轻量 Explore 必须保持在可恢复 sandbox
ADDED     Explore 必须以最短可见事实约束投入
ADDED     Explore 只有选中的稳定增量可以进入 Deliver
ADDED     Superpowers 必须通过复杂度门按需选择
RENAMED   默认流程必须按影响、可逆性和问责性分流
       →  Deliver 必须按影响、可逆性和问责性分流
RENAMED   Standard 和 High-risk 实现性变更必须默认使用 OpenSpec
       →  Deliver Standard 和 High-risk 实现性变更必须默认使用 OpenSpec
MODIFIED  Deliver 必须按影响、可逆性和问责性分流
MODIFIED  Deliver Standard 和 High-risk 实现性变更必须默认使用 OpenSpec
MODIFIED  治理工件必须有预算和可观察用途
```

必须覆盖的 scenario：

- 摘要非技术材料、生成营销插图和通用研究直接退出研发规范；
- 产品问题判断进入 Product Discovery；
- 本地合成 auth spike 不因领域词自动 High-risk；
- Explore 接触真实客户数据时停止轻量豁免并重新路由；
- Deliver Standard 默认 OpenSpec，Explore 默认不创建；
- 已有 OpenSpec tasks 足够时不再创建 Superpowers plan；
- 调用一个 Superpowers skill 不触发其他 skills。

`rd-standards-navigation`：

```text
RENAMED   根入口必须指向最小三档路径
       →  根入口必须先判适用性和 Explore / Deliver
RENAMED   W0-W9 和角色文档必须是可选 playbook
       →  退役导航不得返回默认入口
RENAMED   核心 skill 必须使用三档风险路由
       →  核心 skill 必须先判适用性并使用 Explore / Deliver
MODIFIED  根入口必须先判适用性和 Explore / Deliver
MODIFIED  默认读取集合必须保持小
MODIFIED  退役导航不得返回默认入口
MODIFIED  核心 skill 必须先判适用性并使用 Explore / Deliver
MODIFIED  知识地图必须反映真实默认入口
ADDED     非研发任务必须在读取研发正文前退出
ADDED     Superpowers 运行时必须遵守复杂度作用域
```

`## RENAMED Requirements` 使用 OpenSpec 的 `FROM:` / `TO:` 格式；同一 requirement 的完整新正文放在 `## MODIFIED Requirements` 的新标题下。正文把三档明确收窄为 Deliver 子路由，并删除已退役 `docs/00-start-here.md`、`docs/01-minimal-rd-kernel.md` 的操作性引用。

`ai-coding-workflow-standard`：

```text
MODIFIED  AI 参与不得自动增加流程工件
RENAMED   Standard 工作只维护一份可恢复状态
       →  Deliver Standard 工作只维护一份可恢复状态
MODIFIED  Deliver Standard 工作只维护一份可恢复状态
ADDED     Explore AI 实现必须优先最短可见切片
ADDED     测试先行必须按行为风险选择
ADDED     Superpowers 调用不得自动串联或复制权威工件
```

`testing-quality-standard`：

```text
MODIFIED  生产目标必须定义测试质量工件
ADDED     Explore showcase 必须使用真实产品入口和可理解 fixture
ADDED     Explore 证据不得冒充 Deliver 验收
ADDED     测试先行范围必须与行为风险匹配
```

其中“生产目标”只约束 Deliver Standard/High-risk；轻量 Explore 不默认创建完整质量矩阵、Browser E2E 或独立终审，但任何实际命中的风险控制仍保留。

- [ ] **Step 5: 创建粗粒度 authoritative tasks**

`tasks.md` 使用：

```markdown
# Tasks

- [x] 用户确认 Explore / Deliver 与 Superpowers 作用域设计。
- [x] 归档已完成的 visual UX change。
- [x] 创建本 Standard change 和四个 capability delta，并通过 strict validation。
- [ ] 先增加正式路由与运行时作用域的失败测试。
- [ ] 更新四分类十一项目中的适用入口和 Explore / Deliver 边界。
- [ ] 更新 16 个新 rule-id、既有来源映射、verifier、decision、knowledge 与 current status。
- [ ] 更新并部署 one-person-openspec-rd 和用户级 Superpowers scope instruction。
- [ ] 完成代表场景、完整结构验证、producer self-check 和独立 final review。
- [ ] 在新的本地合成任务上完成 Explore 试点，或明确保持 pilot pending。
```

- [ ] **Step 6: strict validate 并提交 change 合同**

```powershell
openspec validate introduce-explore-deliver-and-scope-superpowers --strict --no-interactive
openspec show introduce-explore-deliver-and-scope-superpowers --json --deltas-only
git add -- openspec/changes/introduce-explore-deliver-and-scope-superpowers
git diff --cached --name-only
git commit -m "openspec: specify Explore Deliver routing"
```

Expected: change valid；只 stage 新 change 目录。

---

### Task 3: 先写正式规则和运行时作用域契约测试

**Files:**

- Modify: `tools/test_current_rd_standards.py`
- Later modify in Task 7: `tools/check_runtime_skill_sync.py`

- [ ] **Step 1: 增加 16 个新正式目标的文件所有权表**

在 `VISUAL_UX_RULE_IDS_BY_FILE` 后增加：

```python
EXPLORE_DELIVER_RULE_IDS_BY_FILE = {
    "docs/01-initiation/01-topic-selection.md": {
        "TOPIC-RD-APPLICABILITY",
        "TOPIC-MIXED-TASK-BOUNDARY",
        "TOPIC-WORK-MODE-ROUTING",
        "TOPIC-SUPERPOWERS-COMPLEXITY-GATE",
    },
    "docs/01-initiation/02-research.md": {
        "RESEARCH-EXPLORE-SANDBOX-BOUNDARY",
    },
    "docs/02-product-design/03-definition.md": {
        "DEFINITION-EXPLORE-PROMOTION",
    },
    "docs/02-product-design/04-experience-design.md": {
        "EXPERIENCE-UX-PROTOTYPE-BOUNDARY",
    },
    "docs/03-engineering-delivery/05-technical-design.md": {
        "TECH-EXPLORE-WALKING-SKELETON",
    },
    "docs/03-engineering-delivery/06-planning.md": {
        "PLAN-EXPLORE-WIP-LIMIT",
        "PLAN-EXPLORE-SHOWCASE-CADENCE",
        "PLAN-EXPLORE-DELIVER-HANDOFF",
    },
    "docs/03-engineering-delivery/07-implementation.md": {
        "IMPL-SELECTIVE-TEST-FIRST",
    },
    "docs/03-engineering-delivery/08-verification.md": {
        "VERIFY-EXPLORE-HUMAN-READABLE-FIXTURES",
        "VERIFY-EXPLORE-SHOWCASE-BOUNDARY",
    },
    "docs/04-operations-maintenance/11-evaluation.md": {
        "EVALUATION-EXPLORE-OUTCOME",
        "EVALUATION-PROCESS-NET-BENEFIT",
    },
}
```

- [ ] **Step 2: 更新当前总数测试并新增 owner 测试**

把 repository 期望从 `2321` 改为 `2337`，并增加：

```python
    def test_explore_deliver_rules_have_explicit_owners(self) -> None:
        expected_all: set[str] = set()

        for rel, expected in EXPLORE_DELIVER_RULE_IDS_BY_FILE.items():
            text = (ROOT / rel).read_text(encoding="utf-8")
            actual = set(RULE_ID_RE.findall(text))
            self.assertTrue(expected <= actual, f"{rel} missing {sorted(expected - actual)}")
            self.assertTrue(expected_all.isdisjoint(expected))
            expected_all.update(expected)

        self.assertEqual(16, len(expected_all))
```

- [ ] **Step 3: 增加正式入口的代表语义测试**

新增一个测试，只读取 README 与 topic selection；runtime router 和未来的 `references/superpowers-scope.md` 留到 Task 7 再测，避免提交一个依赖尚不存在 runtime 文件的红色中间状态。锁定：

```python
self.assertLess(root_readme.index("R&D applicability"), root_readme.index("Quick"))
self.assertIn("Explore", root_readme)
self.assertIn("Deliver", root_readme)
self.assertIn("Product Discovery", topic_selection)
self.assertIn("UX Prototype", topic_selection)
self.assertIn("Technical Spike", topic_selection)
self.assertNotIn("Prototype | Quick | Standard | High-risk", root_readme)
```

测试名称：

```python
def test_applicability_precedes_explore_deliver_and_deliver_risk_routes(...)
```

- [ ] **Step 4: 运行测试并确认只按预期失败**

```powershell
python -m unittest discover -s tools -p "test_current_rd_standards.py" -v
```

Expected: 新 rule-id 与 2,337 总数缺失导致失败；现有 visual UX、component reuse 和 runtime legacy tests 继续通过。不要提交红色状态。

---

### Task 4: 更新根入口、立项和产品设计

**Files:**

- Modify: `README.md`
- Modify:
  - `docs/01-initiation/README.md`
  - `docs/01-initiation/01-topic-selection.md`
  - `docs/01-initiation/02-research.md`
- Modify:
  - `docs/02-product-design/README.md`
  - `docs/02-product-design/03-definition.md`
  - `docs/02-product-design/04-experience-design.md`

- [ ] **Step 1: 把根入口改为三步顺序**

README 的“使用方式”必须先出现：

```text
1. R&D applicability：任务主要结果是否改变、验证、发布、运行或直接决定产品/工程系统？
2. Work mode：存在关键未知且目标是学习时选 Explore；行为已经明确且目标是稳定交付时选 Deliver。
3. Deliver route：只有 Deliver 再按 Quick、Standard、High-risk 分流。
```

紧接其后增加最小图：

```text
Task → R&D applicability
       ├─ No  → use the task's own workflow
       └─ Yes → Explore | Deliver
                 Explore: Product Discovery | UX Prototype | Technical Spike
                 Deliver: Quick | Standard | High-risk
```

明确 `Prototype` 是 Explore artifact，`Walking Skeleton` 是实施方法，不是 route；非研发退出不创建 OpenSpec、研发状态或 Superpowers 工件。

- [ ] **Step 2: 在选题中增加四个 owner rule**

在现有 `TOPIC-SELECTION-TRIGGER` 前增加：

```markdown
<!-- rule-id: TOPIC-RD-APPLICABILITY -->
- 只有任务主要结果会改变、验证、发布、运行、恢复或处置产品/工程系统，直接决定其产品/体验/技术/验收边界，或研究将直接支持一个已识别产品/工程决定时，才进入本研发规范。普通写作、翻译、摘要、内容制作、行政、账目整理、一般查询、通用研究和未获实现授权的只读报告默认退出。

<!-- rule-id: TOPIC-MIXED-TASK-BOUNDARY -->
- 混合请求按结果拆分；只有研发部分进入本规范，非研发部分只消费已验证事实，不因与代码、部署或设计出现在同一请求中而创建独立 OpenSpec 或研发工件。

<!-- rule-id: TOPIC-WORK-MODE-ROUTING -->
- 进入研发后先选 Explore 或 Deliver。Explore 用于以可证伪证据减少关键未知，并按最高优先级问题标记为 Product Discovery、UX Prototype 或 Technical Spike；Deliver 用于稳定已经足够明确的行为。只有 Deliver 再选择 Quick、Standard 或 High-risk。

<!-- rule-id: TOPIC-SUPERPOWERS-COMPLEXITY-GATE -->
- Superpowers 只在存在实质产品歧义、多种高返工方案、跨组件/长期/难回退设计、未知复杂故障、复杂跨会话计划或重大完成结论时，选择一个或少数直接相关 skills；会话开始、AI 参与、创作性、时长或文件数均不能单独触发，调用一个 skill 不授权或串联其他 skills。
```

同时保留 `TOPIC-SELECTION-TRIGGER` 作为“已经进入研发后的显式候选取舍”规则，不让它重新吸入非研发任务。

- [ ] **Step 3: 把调研收窄为 Product Discovery 与轻量 Explore**

修改现有规则：

- `RESEARCH-FOCUSED-OUTCOME`：一轮只有一个最高优先级 question、一个可证伪 hypothesis 和一个 shortest slice；
- `RESEARCH-DISCOVERY-APPLICABILITY`：只覆盖直接支持已识别产品/工程决定的 Product Discovery；
- `RESEARCH-EVIDENCE-BASED-DECISION`：合法结果为 `validated | invalidated | revise | stopped | promote`；
- `RESEARCH-PROPORTIONAL-ARTIFACTS`：Explore 只维护一份短记录，字段为 question、hypothesis、sandbox boundary、shortest slice、active tasks、showcase、evidence/limits、decision、next；
- `RESEARCH-INTERNAL-WORK-EXCLUSION`：与具体产品/工程决定无关的通用研究直接退出研发，而不是转入另一个研发项目。

新增：

```markdown
<!-- rule-id: RESEARCH-EXPLORE-SANDBOX-BOUNDARY -->
- 轻量 Explore 只在本地或隔离 sandbox、合成且可 reset/reseed 的数据、无生产/真实客户/真实凭据/未批准外部系统、无付款/外部通信/公开承诺/不可逆操作，且不声明稳定 API、production migration、release candidate 或 production-ready 时成立。任一边界被突破即停止轻量豁免并重新路由。
```

- [ ] **Step 4: 让定义拥有 promote 决定**

新增：

```markdown
<!-- rule-id: DEFINITION-EXPLORE-PROMOTION -->
- Explore 只有经过真实 showcase 且由人选择的最小行为可以 promote。转换时明确 selected increment 与 excluded exploration，重新判断 Deliver 的 Quick、Standard 或 High-risk；Standard/High-risk OpenSpec 只描述稳定增量并链接 Explore 证据，不复制聊天、失败尝试或全部探索历史。
```

同时：

- `DEFINITION-IMPLEMENTATION-READINESS` 明确只约束 Deliver Standard/High-risk；
- `DEFINITION-PRODUCT-ROUTING` 增加“未知仍主导时回 Explore，结果已知时不得借 Explore 逃避交付”；
- `DEFINITION-OPENSPEC-CONTROL` 明确轻量 Explore 默认不创建 OpenSpec；
- `DEFINITION-AI-ARTIFACT-CHOICE` 增加 Superpowers/AI playbook 只按复杂问题选用。

- [ ] **Step 5: 区分 UX Prototype 与 formal visual UX**

新增：

```markdown
<!-- rule-id: EXPERIENCE-UX-PROTOTYPE-BOUNDARY -->
- UX Prototype 属于 Explore，用于比较关键任务流程、信息架构、交互和可理解性；可以是静态或可运行工件，并应尽快从实际产品入口向人展示。它不自动要求 Deliver 的 `flow.md`、完整 state wireframes、`review.md` 或 production implementation approval，也不能冒充已批准的 formal visual UX。
```

修改 `EXPERIENCE-VISUAL-UX-APPLICABILITY`，明确现有 `visual_ux: required | not-required` 是 Deliver Standard/High-risk 的正式门禁；Explore promote 后，从转换点开始判断，不追溯伪造探索期批准。

- [ ] **Step 6: 更新分类入口但不增加分类**

`docs/01-initiation/README.md` 说明 Product Discovery 是 Explore 类型；`docs/02-product-design/README.md` 说明 UX Prototype 与 Deliver visual UX 的边界。根 README 的四分类十一项列表保持原样。

---

### Task 5: 更新技术设计、计划、实现、验证和评估

**Files:**

- Modify:
  - `docs/03-engineering-delivery/README.md`
  - `docs/03-engineering-delivery/05-technical-design.md`
  - `docs/03-engineering-delivery/06-planning.md`
  - `docs/03-engineering-delivery/07-implementation.md`
  - `docs/03-engineering-delivery/08-verification.md`
- Modify:
  - `docs/04-operations-maintenance/README.md`
  - `docs/04-operations-maintenance/11-evaluation.md`

- [ ] **Step 1: 技术设计加入 Technical Spike 和 Walking Skeleton**

保留并收窄 `TECH-201-ARCHITECTURE-EXPERIMENT-EXCLUSION`：一次性 Technical Spike 只有在 sandbox boundary 成立、有删除/过期边界且不进入生产时，才不展开完整架构专项。

新增：

```markdown
<!-- rule-id: TECH-EXPLORE-WALKING-SKELETON -->
- Technical Spike 的第一轮优先形成一条 Walking Skeleton：从一个真实产品入口经过实际所需组件到达一个可见业务结果。多服务 Explore 仍提供一个用户入口，不以分别证明 API、数据库或服务启动代替端到端产品事实；横向加固、平台化和所有异常覆盖延后到该事实出现之后。
```

在复杂架构触发处说明：跨服务、数据所有权、权限模型、稳定 API、重大选型或难回退设计可以使用 `brainstorming`；沿用已批准模式的单组件变更默认跳过。

- [ ] **Step 2: 计划拥有 WIP、showcase cadence 与 handoff**

新增：

```markdown
<!-- rule-id: PLAN-EXPLORE-WIP-LIMIT -->
- 轻量 Explore 同时最多 5 个 active tasks；其余进入 `Next` 或 `Later`。新任务进入 active 前必须完成、移出或让位一个现有任务。

<!-- rule-id: PLAN-EXPLORE-SHOWCASE-CADENCE -->
- 轻量 Explore 每 120 分钟或每 5 次提交进行一次真实 showcase，以先到者为准；连续 2 小时没有新增可见产品事实时停止并缩小 question 或 shortest slice，不得用补文档、横向治理或追溯延长期限掩盖停滞。

<!-- rule-id: PLAN-EXPLORE-DELIVER-HANDOFF -->
- promote 时只把 selected increment 转成 Deliver tasks；Explore 的短记录保留证据链接，Deliver Standard/High-risk 使用 OpenSpec `tasks.md` 作为状态权威，不并行维护 Superpowers plan 或 work brief。
```

修改：

- `PLAN-TRACKED-BATCH-APPLICABILITY`：Explore 使用短记录；Deliver 才按跨会话/验收需要显式展开；
- `PLAN-RISK-ROUTE-NOT-DURATION`：Quick/Standard/High-risk 只属于 Deliver；
- `PLAN-SINGLE-RECORD-DEFAULT`：现有 OpenSpec tasks 足够时跳过 `writing-plans`；
- `PLAN-VISUAL-UX-READINESS`：只在 promote 后的 Deliver 适用。

- [ ] **Step 3: 实现采用纵切片和选择性 TDD**

修改现有 `IMPL-DISCOVERY-AND-SPEC-BOUNDARY` 与 `IMPL-USER-VISIBLE-LONG-WORK-ENTRY`，明确 Explore 可以做不可发布的最小实现，先关闭 Walking Skeleton，再扩展横向框架、恢复、质量矩阵或平台化。

新增：

```markdown
<!-- rule-id: IMPL-SELECTIVE-TEST-FIRST -->
- 核心领域规则、服务端授权、安全边界、数据一致性、公共契约、bugfix 和危险重构优先测试先行；抛弃式 UI 脚手架、生成代码、简单配置和 UX/Technical Explore 可以先实现后补对 selected behavior 有价值的自动化。Explore promote 前必须为准备稳定的行为补齐与风险相称的回归证据，不追溯要求所有失败探索都采用 TDD。
```

- [ ] **Step 4: 验证区分 showcase 与 formal acceptance**

新增：

```markdown
<!-- rule-id: VERIFY-EXPLORE-HUMAN-READABLE-FIXTURES -->
- 用户可见 Explore 使用 Alice、Bob、Admin 等人类可识别 fixture 和可理解业务结果；opaque ID、API success、DOM 存在或数据库行本身不能证明用户理解和完成任务。

<!-- rule-id: VERIFY-EXPLORE-SHOWCASE-BOUNDARY -->
- Showcase 必须复用实际产品入口和真实页面动作，不另建掩盖当前状态的静态展示站。它记录 observed behavior、visible fact、limits 和 next decision；只有满足完整 Browser E2E 契约时才可命名为 Browser E2E，也不得作为 Deliver accepted、release-ready 或 production-ready 证据。
```

在输入/完成段明确：Explore 可合法以 `invalidated`、`revise` 或 `stopped` 结束；证据准确命名比通过数量更重要。

- [ ] **Step 5: 评估记录结果与流程净收益**

新增：

```markdown
<!-- rule-id: EVALUATION-EXPLORE-OUTCOME -->
- Explore 结束时记录 `validated | invalidated | revise | stopped | promote`、showcase 观察、证据限制和一个 next；这些结果都不表示产品完成或生产就绪。

<!-- rule-id: EVALUATION-PROCESS-NET-BENEFIT -->
- 评估 Explore 与可选方法时记录 time to first visible fact、process minutes、showcase 次数、active-task 峰值、Superpowers 实际使用及其解决的问题、OpenSpec promote 边界、rework/恢复成本和未覆盖证据。文件数与提交数只作上下文，不能单独证明成功或浪费。
```

调整 Operations README，使“评估”可以消费受控 Explore 结果和流程证据，但不把调研的产品 hypothesis 结论复制成第二权威。

---

### Task 6: 同步 16 个来源映射、正式计数和 verifier

**Files:**

- Modify: `governance/rd-standards/review/atomic-rules.csv`
- Modify: `governance/rd-standards/review/coverage-matrix.csv`
- Modify: `tools/verify_rd_standards.py`
- Modify: `README.md`
- Verify unchanged: `governance/rd-standards/replacement-manifest.json`

- [ ] **Step 1: 在两份 5,956 行账本中做相同映射**

对下列 `rule_id` 的现有 `target_rule_id` 末尾追加新目标；用分号分隔，不改其他列：

| source rule | append target |
| --- | --- |
| `RULE-W0-003` | `TOPIC-RD-APPLICABILITY` |
| `RULE-W1-022` | `TOPIC-MIXED-TASK-BOUNDARY` |
| `RULE-W1-045` | `TOPIC-WORK-MODE-ROUTING;TECH-EXPLORE-WALKING-SKELETON` |
| `RULE-W5-003-001` | `TOPIC-SUPERPOWERS-COMPLEXITY-GATE` |
| `RULE-W2-061` | `RESEARCH-EXPLORE-SANDBOX-BOUNDARY` |
| `RULE-W1-043` | `DEFINITION-EXPLORE-PROMOTION;PLAN-EXPLORE-DELIVER-HANDOFF` |
| `RULE-W1-124` | `EXPERIENCE-UX-PROTOTYPE-BOUNDARY` |
| `RULE-W0-024` | `PLAN-EXPLORE-WIP-LIMIT` |
| `RULE-W1-012` | `PLAN-EXPLORE-SHOWCASE-CADENCE` |
| `RULE-W5-002-170` | `IMPL-SELECTIVE-TEST-FIRST` |
| `RULE-W4-006-034` | `VERIFY-EXPLORE-HUMAN-READABLE-FIXTURES` |
| `RULE-W5-001-038` | `VERIFY-EXPLORE-SHOWCASE-BOUNDARY` |
| `RULE-W1-039` | `EVALUATION-EXPLORE-OUTCOME` |
| `RULE-W0-041` | `EVALUATION-PROCESS-NET-BENEFIT` |

这 14 条来源覆盖 16 个新目标。相同 `rule_id` 在 `atomic-rules.csv` 与 `coverage-matrix.csv` 的最终 `target_rule_id` 必须完全一致。

- [ ] **Step 2: 更新 current count**

在 `tools/verify_rd_standards.py`：

```python
EXPECTED_FORMAL_RULE_IDS = 2337
```

根 README 改为：

```markdown
正式正文包含 2,337 个唯一稳定规则目标；5,956 条来源原子规则及其处理决定保留在治理账本中。
```

- [ ] **Step 3: 运行账本与正式规则测试**

```powershell
python -m unittest discover -s tools -p "test_current_rd_standards.py" -v
python tools/verify_rd_standards.py .
```

Expected: Task 3 新增的两个测试和所有既有测试均通过；正式 verifier 输出：

```text
RD_STANDARDS=PASS categories=4 items=11 rule_ids=2337 review_files=7
```

Task 7 的三个 runtime/global tests 尚未写入，因此不存在允许保留的预期失败。

- [ ] **Step 4: 确认历史 replacement 未被改写**

```powershell
$replacement = Get-Content -Raw governance/rd-standards/replacement-manifest.json | ConvertFrom-Json
$replacement.formal_targets.rule_target_count
$replacement.formal_targets.atomic_rule_count
```

Expected:

```text
2313
5956
```

- [ ] **Step 5: 提交正式规则、测试和映射**

精确 stage Tasks 3–6 的 repo 文件，确认不含 OpenSpec tasks 的虚假完成状态、`.superpowers/` 或 runtime installed copy，然后：

```powershell
git add -- README.md docs/01-initiation/README.md docs/01-initiation/01-topic-selection.md docs/01-initiation/02-research.md docs/02-product-design/README.md docs/02-product-design/03-definition.md docs/02-product-design/04-experience-design.md docs/03-engineering-delivery/README.md docs/03-engineering-delivery/05-technical-design.md docs/03-engineering-delivery/06-planning.md docs/03-engineering-delivery/07-implementation.md docs/03-engineering-delivery/08-verification.md docs/04-operations-maintenance/README.md docs/04-operations-maintenance/11-evaluation.md governance/rd-standards/review/atomic-rules.csv governance/rd-standards/review/coverage-matrix.csv tools/test_current_rd_standards.py tools/verify_rd_standards.py
git diff --cached --name-only
git diff --check
git commit -m "docs: introduce Explore Deliver routing"
```

---

### Task 7: 更新 R&D router 并部署用户级 Superpowers scope

**Skills for this task only:**

- 使用 `skill-creator`，因为这是对既有 Codex skill 的行为更新；
- 该 skill 变更本身跨前置门、fallback、review 和 runtime sync，满足复杂度门，因此可以只使用 `superpowers:writing-skills` 辅助验证；
- 不因使用这两个 skills 自动调用 brainstorming、worktree、subagents、review 或 branch-finishing。

**Files:**

- Modify:
  - `skills/one-person-openspec-rd/SKILL.md`
  - `skills/one-person-openspec-rd/agents/openai.yaml`
  - `skills/one-person-openspec-rd/references/workflow-map.md`
  - `skills/one-person-openspec-rd/references/review-rubric.md`
  - `skills/one-person-openspec-rd/references/stack-defaults.md`
- Create: `skills/one-person-openspec-rd/references/superpowers-scope.md`
- Modify: `tools/check_runtime_skill_sync.py`
- Modify: `tools/test_current_rd_standards.py`
- Mechanically sync: `C:\Users\machinly\.codex\skills\one-person-openspec-rd\...`
- Bounded user-level modify: `C:\Users\machinly\.codex\AGENTS.md`

- [ ] **Step 1: 先写 global-instruction validator tests**

在 `test_current_rd_standards.py` 增加三个测试：

```python
def test_runtime_router_exposes_explore_types_and_scoped_superpowers(...)
def test_global_superpowers_scope_rejects_missing_managed_block(...)
def test_global_superpowers_scope_accepts_exact_managed_block(...)
```

第一个测试读取 canonical `SKILL.md` 和 `references/superpowers-scope.md`，断言 Product Discovery、UX Prototype、Technical Spike、`does not authorize another` 和 `Do not automatically chain` 存在，并断言 OpenSpec 默认值只位于 Deliver Standard/High-risk。

从 `check_runtime_skill_sync` 导入未来的 `validate_global_agents`。用 temp files 验证：

- 空 global AGENTS 返回 invalid；
- 含其他用户文字但缺少 managed block 返回 invalid；
- 含其他用户文字并包含 canonical managed block 返回 valid；
- checker 不要求 global AGENTS 与 canonical 整文件相等，只要求 exact block 存在。

运行该文件并确认 import 或 missing-function 失败。

- [ ] **Step 2: 创建 canonical managed block**

`references/superpowers-scope.md` 写入：

```markdown
<!-- rd-standards:superpowers-scope:start -->
## Scoped Superpowers

This instruction overrides plugin-level blanket triggers that would invoke Superpowers at every conversation start or for all creative work.

Do not invoke Superpowers merely because a conversation started, AI is involved, work is creative, many files are involved, or the task is long.

Apply the R&D applicability gate first. Non-R&D work does not invoke `one-person-openspec-rd` and does not invoke Superpowers unless that task has a concrete complex problem directly served by one specific skill.

For R&D work, choose Explore or Deliver before any Deliver risk route. Invoke a Superpowers skill only for a concrete complexity trigger: material product ambiguity, multiple costly alternatives, cross-component or hard-to-reverse architecture, complex cross-session dependencies, an unknown or failed-first-fix bug, or a major merge/release/completion conclusion.

Use only the smallest directly relevant skill set. Invoking one skill does not authorize another. Do not automatically chain brainstorming, design documents, writing plans, worktrees, subagents, code review, verification, or branch finishing.

Write facts and status only to the current canonical artifact. Do not create duplicate Superpowers specs, plans, work briefs, or status files when product documents, technical design, an Explore iteration record, or OpenSpec already owns that information.
<!-- rd-standards:superpowers-scope:end -->
```

- [ ] **Step 3: 重写 router 的读取与路由顺序**

`SKILL.md` front matter description 改为：

```yaml
description: "Gate R&D applicability, route applicable work through Explore or Deliver, then route Deliver through Quick, Standard, or High-risk; use OpenSpec and complex methods only where their triggers apply."
```

正文顺序必须是：

1. `Applicability`：非研发立即退出，不读取四分类十一项；
2. `Work Mode`：Explore / Deliver；
3. `Explore`：Product Discovery / UX Prototype / Technical Spike、sandbox、single record、Walking Skeleton、5 tasks、showcase、selective TDD、outcomes；
4. `Deliver`：Quick / Standard / High-risk；
5. `OpenSpec`：只默认用于 Deliver Standard/High-risk implementation；
6. `Superpowers Complexity Gate`：链接 `references/superpowers-scope.md`，按设计矩阵选择最小 skill 集；
7. `Review` 与 `Completion`：Explore 不默认独立终审，Deliver Standard/High-risk 保持现有门禁。

`workflow-map.md` 使用相同 fallback 顺序；`review-rubric.md` 增加 Explore self-check，检查 sandbox、actual entry、fixture、showcase、active-task peak、outcome 和 Superpowers trigger；`stack-defaults.md` 明确技术栈不是 applicability 或 work-mode 前置条件。

`agents/openai.yaml` 更新为：

```yaml
interface:
  display_name: "Explore / Deliver R&D"
  short_description: "先判定研发适用性，再区分探索与交付，并按复杂度选择方法"
  default_prompt: "Use $one-person-openspec-rd only after the R&D applicability gate. Route applicable work through Explore or Deliver, use Quick/Standard/High-risk only for Deliver, and invoke Superpowers only for a concrete complexity trigger without automatic chaining."
```

- [ ] **Step 4: 扩展 runtime sync checker**

在 `ROUTER_FILES` 加入：

```python
"references/superpowers-scope.md",
```

新增：

```python
def validate_global_agents(canonical_scope: Path, global_agents: Path) -> dict[str, object]:
    # valid only when both files exist and the normalized canonical managed block
    # is present verbatim in global_agents; unrelated surrounding user text is allowed
```

CLI 新增可选 `--global-agents`；默认使用：

```python
codex_home / "AGENTS.md"
```

非 JSON 输出在原有字段后增加：

```text
global_superpowers_scope=synced
```

缺失或 drift 必须使命令非零退出。

- [ ] **Step 5: 让 repo tests 变绿**

```powershell
python -m unittest discover -s tools -p "test_current_rd_standards.py" -v
```

Expected: 比基线新增 5 个测试，此文件总数相应增加，所有测试通过。

- [ ] **Step 6: 部署 installed skill**

只机械复制 `ROUTER_FILES` 中的六个 canonical 文件到：

```text
C:\Users\machinly\.codex\skills\one-person-openspec-rd\
```

不得修改其他 installed skills 或插件 cache。

- [ ] **Step 7: 有界写入 user-level AGENTS**

重新读取：

```powershell
Get-Content -Raw C:\Users\machinly\.codex\AGENTS.md
```

如果 markers 不存在，用 `apply_patch` 追加 canonical block；如果已存在，只替换 markers 之间的内容；如果出现不成对 markers，停止并人工检查。不得覆盖 marker 外内容。

- [ ] **Step 8: 验证、提交 repo source，并记录外部部署**

```powershell
python tools/check_runtime_skill_sync.py .
git diff --check
git status --short -- skills/one-person-openspec-rd tools/check_runtime_skill_sync.py tools/test_current_rd_standards.py
git add -- skills/one-person-openspec-rd/SKILL.md skills/one-person-openspec-rd/agents/openai.yaml skills/one-person-openspec-rd/references/workflow-map.md skills/one-person-openspec-rd/references/review-rubric.md skills/one-person-openspec-rd/references/stack-defaults.md skills/one-person-openspec-rd/references/superpowers-scope.md tools/check_runtime_skill_sync.py tools/test_current_rd_standards.py
git diff --cached --name-only
git commit -m "runtime: scope Superpowers to complex work"
```

Expected:

```text
RUNTIME_SKILL_SYNC=PASS status=synced legacy_present=0 preserved_missing=0 global_superpowers_scope=synced
```

该 PASS 只证明文件已部署；Codex 在新会话中的真实选择行为由 Task 9 的代表场景和 Task 11 的新 Explore pilot 验证。提交只包含 repository canonical source/checker/tests；用户级 AGENTS 与 installed skill 不在 Git 中，最终交付必须单独披露。

---

### Task 8: 更新 decision、knowledge 和 current governance

**Files:**

- Create: `decisions/2026-07-26-introduce-explore-deliver-and-scope-superpowers.md`
- Modify:
  - `governance/rd-standards/approvals.jsonl`
  - `governance/current-status.json`
  - `knowledge/docs-map/rd-standards.json`
  - `knowledge/context-packs/rd-standards.md`
  - `knowledge/how-to/rd-standards.md`
  - `knowledge/glossary/rd-standards.md`
  - `knowledge/freshness/rd-standards.jsonl`
- Verify unchanged: `governance/rd-standards/replacement-manifest.json`

- [ ] **Step 1: 记录部分取代关系**

新 decision 必须说明：

- 2026-07-11 的 OpenSpec 默认决定仍适用于 **Deliver Standard/High-risk implementation**；
- 该决定不再适用于轻量 Explore；
- Prototype 是 Explore artifact，Walking Skeleton 是 tactic；
- 非研发不进入规范；
- Superpowers 使用复杂度门，禁止自动串联；
- 依据是用户确认和第三轮负面实验；
- 回滚时保留 applicability 与真实 High-risk 控制。

- [ ] **Step 2: 追加 approval 与 freshness**

`approvals.jsonl` 追加用户确认记录，scope 精确引用本设计，不把确认扩张为生产、外部系统或插件缓存授权。

`freshness` 追加一行，记录：

```text
change=introduced-rd-applicability-explore-deliver-and-scoped-superpowers
result=formal-routing-updated-pilot-pending
review_on=after-first-new-explore-pilot-or-2026-08-26
```

- [ ] **Step 3: 更新知识入口**

- docs map status 改为能表达 Explore/Deliver；
- linked OpenSpec changes 增加 visual UX archive 和当前 active change；
- context pack/handoff prompt 先做 applicability，再 Explore/Deliver；
- how-to 分成 Non-R&D、Explore、Deliver/Quick/Standard/High-risk；
- glossary 增加 `R&D applicability`、`Explore`、`Product Discovery`、`UX Prototype`、`Technical Spike`、`Deliver`、`Prototype`、`Walking Skeleton`、`Superpowers complexity gate`；
- 删除任何把 Quick/Standard/High-risk 描述成所有任务第一步的文字。

- [ ] **Step 4: 更新 current status，但不预填最终 PASS**

`latest_evidence` 更新：

```json
"formal_rule_target_count": 2337,
"atomic_rule_count": 5956,
"latest_change": {
  "id": "introduce-explore-deliver-and-scope-superpowers",
  "design": "docs/superpowers/specs/2026-07-26-rd-explore-deliver-superpowers-scope-design.md",
  "decision": "approved",
  "formal_rule_target_count_before": 2321,
  "formal_rule_target_count_after": 2337,
  "atomic_rule_count": 5956,
  "previous_change_archive": "openspec/changes/archive/2026-07-26-add-visual-ux-step-to-rd-standards"
},
"pilot": {
  "status": "pending",
  "reason": "Structural implementation is complete only after final review; effect requires a new local synthetic Explore task."
}
```

`final_verification` 只在 Task 10 命令真实通过后写实际结果。`status` 可继续表示 formal corpus 可用，但 `pilot.status` 不得提前改为 pass。

- [ ] **Step 5: 提交知识与治理**

```powershell
git diff --check
git add -- decisions/2026-07-26-introduce-explore-deliver-and-scope-superpowers.md governance/rd-standards/approvals.jsonl governance/current-status.json knowledge/docs-map/rd-standards.json knowledge/context-packs/rd-standards.md knowledge/how-to/rd-standards.md knowledge/glossary/rd-standards.md knowledge/freshness/rd-standards.jsonl
git diff --cached --name-only
git commit -m "docs: publish Explore Deliver governance"
```

---

### Task 9: 验收代表路由，不建设 routing engine

**Files:**

- Modify live status only: `openspec/changes/introduce-explore-deliver-and-scope-superpowers/tasks.md`
- No new schema or router program

- [ ] **Step 1: 逐项用正式 rule-id 和 OpenSpec scenario 核对**

| Scenario | Expected |
| --- | --- |
| 摘要非技术材料 | Non-R&D；不读研发正文，不调用 one-person router/Superpowers |
| 生成营销插图 | Non-R&D；走图像任务自身流程 |
| 与产品决定无关的行业研究 | Non-R&D |
| 判断已识别用户问题是否值得建设 | Explore / Product Discovery |
| 比较两个关键任务流程 | Explore / UX Prototype；只有多方案且返工显著时用 brainstorming |
| 本地合成 gateway/OIDC/service identity | Explore / Technical Spike；不因 auth 关键词自动 High-risk |
| 不改变含义的按钮文案 | Deliver / Quick；不调用 brainstorming |
| 已确认的用户资料编辑 | Deliver / Standard；默认 OpenSpec |
| 生产管理员权限或真实账号删除 | Deliver / High-risk |
| Explore 接入真实客户数据 | 停止轻量 Explore，重新路由并应用 High-risk 控制 |
| 已有 OpenSpec tasks 足够 | 不创建 Superpowers plan |
| 跨服务数据所有权有三个合理方案 | brainstorming；结论写技术设计/OpenSpec design |
| 编译器明确指出漏 import | 机械修复，不调用 systematic-debugging |
| 跨服务偶发失败且首次修复无效 | systematic-debugging |
| 三项任务共享写域或顺序依赖 | 不使用 parallel agents |

每项必须能够从 README、formal rule 和 capability scenario 得到相同结论。若需要通过 skill 中新增独立语义才能解释，返回对应 formal owner 修正；skill 只能做薄路由。

- [ ] **Step 2: 搜索错误的旧路由**

```powershell
rg -n "先.*Quick.*Standard.*High-risk|route the task as Quick|Prototype.*Quick.*Standard.*High-risk" README.md docs skills knowledge
rg -n "every conversation|all creative work|自动串联|automatically chain" skills/one-person-openspec-rd C:\Users\machinly\.codex\AGENTS.md
```

Expected: 第一组不再把三档风险作为所有任务第一步；第二组只出现禁止 blanket trigger/automatic chain 的作用域语义。

- [ ] **Step 3: 更新 OpenSpec tasks 的真实状态**

只在相应工作和命令完成后勾选；不得把 Task 10 review 或 Task 11 pilot 预先标为完成。

---

### Task 10: 完整结构验证和独立终审

**Skill scope for this task:** 本任务准备作出重大规范与运行时完成结论，明确命中复杂度门，因此只使用 `superpowers:verification-before-completion` 来约束证据检查；这不自动触发其他 Superpowers skills。只有用户明确授权独立 Agent reviewer 时，才可额外使用 `requesting-code-review`；否则由用户指定的人类或独立上下文完成正式终审。

**Files:**

- Create after genuine review: `openspec/changes/introduce-explore-deliver-and-scope-superpowers/review.md`
- Modify after real commands:
  - `openspec/changes/introduce-explore-deliver-and-scope-superpowers/tasks.md`
  - `governance/current-status.json`

- [ ] **Step 1: 运行完整本地测试**

```powershell
python -m unittest discover -s tools -p "test_*.py" -v
```

Expected after the five new tests:

```text
Ran 107 tests
OK
```

若实际 discovery 数变化，以真实输出为准并解释原因，不修改摘要来伪造 107。

- [ ] **Step 2: 运行所有正式门禁**

```powershell
python tools/verify_rd_standards.py .
python tools/check_runtime_skill_sync.py .
python tools/verify_pilot_records.py .
openspec validate --all --strict --no-interactive
```

Expected:

```text
RD_STANDARDS=PASS categories=4 items=11 rule_ids=2337 review_files=7
RUNTIME_SKILL_SYNC=PASS ... global_superpowers_scope=synced
PILOT_RECORD_FORMAT=PASS
PILOT_EFFECT_VERIFIED=PENDING
Totals: 59 passed, 0 failed (59 items)
```

当前单条第二轮负面记录还会产生 “Standard/High-risk without OpenSpec ... ineligible” warning；这是保留的历史负面证据。`PENDING` 是正确结果，直到 Task 11 的新 Explore pilot 提供真实证据；不得把结构 PASS 改写为流程效果已验证。

- [ ] **Step 3: Producer self-check**

检查：

- 非研发退出发生在任何研发正文读取前；
- Explore/Deliver 与 Quick/Standard/High-risk 没有并列混用；
- Prototype/Walking Skeleton 没有成为 route；
- Explore sandbox 不能覆盖真实生产/数据/凭据/付款/外部通信/不可逆动作；
- formal visual UX、完整质量矩阵、OpenSpec 与独立终审只从 Deliver/promote 点生效；
- 16 个新 rule-id 唯一且都有历史来源映射；
- 账本仍为 5,956/5,956 行，replacement manifest 仍为 2,313/5,956；
- global AGENTS marker 外内容未变化；
- plugin cache 未修改；
- `.superpowers/` 未 stage；
- 没有平行 live status。

- [ ] **Step 4: 获取真正独立 final review**

本 change 是 Deliver / Standard，必须由未参与产出的 reviewer 检查设计、OpenSpec delta、formal diff、ledger mapping、runtime/global instruction、测试与代表场景。

不要自动启动子 Agent。执行到此若用户尚未明确允许独立 Agent，应停止在 `self-check-complete`，请求用户指定人类 reviewer 或明确授权一个独立上下文。Reviewer 记录：

```markdown
# Independent Final Review

Reviewer:
Reviewed at:
Target revision:
Scope:
Evidence checked:
Findings:
Decision: accept | changes-requested | reject
Residual risks:
```

只有 `accept` 才能把结构实施标为完成。`changes-requested` 时修正并重跑受影响检查。

- [ ] **Step 5: 写入真实 final verification**

用实际日期、单测数、2,337 rule-id、runtime/global scope、OpenSpec 数和 review decision 更新 `current-status.json`。`pilot.status` 继续为 `pending`。

- [ ] **Step 6: 提交 review 与最终状态**

```powershell
git diff --check
git add -- openspec/changes/introduce-explore-deliver-and-scope-superpowers/review.md openspec/changes/introduce-explore-deliver-and-scope-superpowers/tasks.md governance/current-status.json
git diff --cached --name-only
git commit -m "docs: accept Explore Deliver standards change"
```

change 暂时保持 active，直到 Task 11 pilot 结束或用户明确决定以 pending 状态归档。

---

### Task 11: 在新的本地合成任务上验证 Explore

**External prerequisite:** 用户指定或批准一个新的本地合成产品任务/仓库。不得自动恢复第三轮已停止 scope，也不得在没有明确目标时新建产品仓库。

**Canonical artifact:** 目标项目只维护一份 Explore iteration record；本仓库只链接最终证据，不复制其 live status。不新增 pilot schema。

- [ ] **Step 1: 选择合格任务**

任务必须：

- 有一个真实用户可见问题和可证伪 hypothesis；
- 能在本地/隔离 sandbox 使用合成可重建数据；
- 无生产、真实客户、真实凭据、付款、外部通信和不可逆副作用；
- 可从实际产品入口形成一个 Walking Skeleton；
- 预期首个 showcase 能在 120 分钟内发生。

在目标仓库先运行 `rg --files -g AGENTS.md`，从仓库根到工作目录读取适用文件。若更近的 repo/nested instruction 要求 blanket Superpowers 或与本设计冲突，停止并由用户决定是更新项目指令还是换试点；不得假设 global AGENTS 会覆盖更近文件。

- [ ] **Step 2: 建立唯一短记录**

只记录：

```text
question
hypothesis
sandbox boundary
shortest slice
active tasks (max 5)
showcase result
evidence and limits
decision
next
```

计量字段放在同一记录末尾：time to first visible fact、process minutes、showcase count、active-task peak、Superpowers skills/trigger/problem solved、OpenSpec before/after promote、rework/recovery、uncovered evidence。

- [ ] **Step 3: 执行时间与提交门**

- 首次 showcase 不晚于 120 分钟；
- 每 120 分钟或 5 commits showcase，以先到者为准；
- 连续 2 小时没有新 visible fact 时实际执行 shrink 或 stop；
- 使用 Alice/Bob/Admin 等 fixture 和实际产品入口；
- 不另建静态展示站；
- Superpowers 每次调用写明一个 complexity trigger，禁止 chain；
- promote 前不创建完整 OpenSpec 或平行 Superpowers spec/plan。

- [ ] **Step 4: 结束并选择 outcome**

只选 `validated | invalidated | revise | stopped | promote`。若 `promote`：

- 选择最小 stable increment；
- 重新判断 Deliver Quick/Standard/High-risk；
- Standard/High-risk 创建 OpenSpec，只链接 Explore 证据；
- 从转换点开始补 formal visual UX、稳定契约、质量和 review，不追溯伪造。

- [ ] **Step 5: 回灌结论**

在本仓库创建一份简短 review，链接目标项目的 canonical record，更新 `governance/current-status.json.latest_evidence.pilot`。只有十项设计验收均有真实证据时标记 `pass`；否则记录 `negative-evidence`、`revise` 或 `stopped`。

- [ ] **Step 6: 归档本 change**

Pilot 结论和独立 review 已记录后：

```powershell
openspec validate introduce-explore-deliver-and-scope-superpowers --strict --no-interactive
openspec archive introduce-explore-deliver-and-scope-superpowers -y
openspec validate --all --strict --no-interactive
```

归档前确认四个 capability delta 尚未以其他方式进入 base specs。归档后更新 knowledge link 和 current status，再提交 archive。若用户选择在 pilot pending 时归档，必须在 decision/current status 中明确“结构已发布、效果待验证”，不能写成 pilot passed。

---

## Final handoff checklist

- 交付说明必须分别报告：
  - formal standards structure；
  - runtime skill sync；
  - user-level AGENTS managed block；
  - OpenSpec validation/archive state；
  - independent review；
  - pilot `pending | pass | negative-evidence`；
  - 未覆盖证据和剩余风险。
- 不把 unit/format/strict validation 冒充真实 Explore 效果。
- 不把用户确认本设计解释为生产、外部系统、真实数据、插件缓存或自动子 Agent授权。
- 回滚 user-level instruction 时只删除 `rd-standards:superpowers-scope` markers 之间的 managed block；不覆盖其他用户内容。
