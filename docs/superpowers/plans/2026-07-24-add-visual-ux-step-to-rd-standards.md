# Add Visual UX Step to R&D Standards Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有四分类、十一项目研发规范中，把开发前静态可视 UX 与人工“可开发”批准加入“体验设计”，并让计划、实现、验证和运行时路由消费该结果；本轮不建设通用 UX Kit。

**Architecture:** “体验设计”是可视 UX 语义的唯一 owner；“计划”只检查输入是否 ready，“实现”只检查批准并在偏离时回退，“验证”只用浏览器证据核对已批准方案。OpenSpec 记录本次 Standard 增量，现有治理覆盖矩阵继续承担正式 rule-id 追溯，运行时 skill 只保留薄路由。

**Tech Stack:** Markdown、静态 HTML/SVG 规范约定、OpenSpec CLI、Python 3 标准库 `unittest`、CSV/JSON 治理账本、PowerShell。

## Global Constraints

- 唯一设计依据是 `docs/superpowers/specs/2026-07-24-rd-visual-ux-step-design.md`；旧的通用 UX Kit 方向不再是实施依据。
- 只增加现有“体验设计”的子步骤，不新增第十二项目，不新增 `verify_ux_*`、schema、renderer、catalog、通用模板生成器、可交互原型或外部设计工具依赖。
- 必须在当前工作区执行。`docs/02-product-design/`、`docs/03-engineering-delivery/`、`governance/`、`tools/test_current_rd_standards.py` 和 `tools/verify_rd_standards.py` 含有尚未进入 `HEAD` 的权威基线；从 `HEAD` 新建 worktree 会丢失这些输入。
- 不得执行 `stash`、`reset`、`checkout --`、清理未跟踪文件或批量回滚。每次写入只使用精确路径和锚点，保留所有无关修改。
- 不把当前未跟踪或已修改的正式规范、治理文件、工具文件整体加入提交，因为那会吸收用户既有基线。只有全新且路径独立的 OpenSpec change 可以在精确核对 staged paths 后单独提交；若用户没有要求提交，保持未提交并在交付中说明。
- `governance/rd-standards/replacement-manifest.json` 是 2026-07-20 正式替换事件的历史证据，继续保留其中的 2313/5956 历史数字；当前 2321 数字写入根 `README.md`、verifier、测试和 `governance/current-status.json`，不得重写历史事件。
- `atomic-rules.csv` 和 `coverage-matrix.csv` 保持 5956 行；新增的 8 个正式目标是既有来源规则的细化映射，不伪造新的 W0–W9 原子来源。
- 每个任务完成后运行该任务列出的检查。任何非预期失败先调查，不通过放宽校验、删除证据或改写历史数字来“修绿”。

---

### Task 1: 固化批准状态并创建 Standard OpenSpec change

**Files:**

- Modify: `docs/superpowers/specs/2026-07-24-rd-visual-ux-step-design.md`
- Create: `openspec/changes/add-visual-ux-step-to-rd-standards/proposal.md`
- Create: `openspec/changes/add-visual-ux-step-to-rd-standards/design.md`
- Create: `openspec/changes/add-visual-ux-step-to-rd-standards/tasks.md`
- Create: `openspec/changes/add-visual-ux-step-to-rd-standards/specs/accessibility-ai-ux-standard/spec.md`
- Create: `openspec/changes/add-visual-ux-step-to-rd-standards/specs/ai-coding-workflow-standard/spec.md`
- Create: `openspec/changes/add-visual-ux-step-to-rd-standards/specs/testing-quality-standard/spec.md`

- [ ] **Step 1: 确认 change 尚不存在并证明缺失会失败**

Run:

```powershell
openspec validate add-visual-ux-step-to-rd-standards --strict --no-interactive
```

Expected: 非零退出，明确说明 change 不存在；若 change 已存在，先完整读取并核对，不能覆盖未知内容。

- [ ] **Step 2: 更新已批准设计的状态**

把：

```markdown
状态：已按用户反馈收窄范围，待用户审阅
```

替换为：

```markdown
状态：已获用户认可，待实施
```

并在“## 15. 决策记录”末尾追加：

```markdown
- 2026-07-24：用户认可收窄后的设计，可进入实施计划与 Standard change。
```

- [ ] **Step 3: 创建 `proposal.md`**

写入：

```markdown
## Why

当前正式研发规范已经定义关键任务、surface、基本状态、可访问性和浏览器证据，但没有把“开发前看见静态界面方案并由人确认可开发”设为清晰门禁。结果是实现者可能只凭文字推断页面结构、高风险交互和状态反馈，直到开发后才发现体验分歧。

本 change 落实已获认可的 `docs/superpowers/specs/2026-07-24-rd-visual-ux-step-design.md`，只调整现有研发规范和薄路由，不建设通用 UX Kit。

## Routing

- path: Standard
- visual_ux: not-required
- reason: 本 change 修改研发规范文档与路由，不新增或改变产品用户界面。

## What Changes

- 在“体验设计”中加入条件触发的静态低保真 UX、最小仓库产物、高保真条件升级和人工 `approved` 门禁。
- 在“计划”中加入 `visual_ux` 判定、工件链接和 production implementation readiness 检查。
- 在“实现”中加入批准检查，以及任务路径、状态、权限含义或高风险确认偏离时返回体验设计的规则。
- 在“验证”中加入 Browser E2E、desktop/mobile 条件截图、四类基本状态、keyboard/focus 与已批准线框的一致性检查。
- 更新 `one-person-openspec-rd` 的路由和 review rubric，不复制正式体验设计正文。
- 更新正式 rule-id 测试、既有来源映射和当前治理状态。

## Non-Goals

- 不新增研发分类或项目。
- 不建设通用 UX Kit、跨项目组件 catalog、pattern ID、schema、renderer 或专用 verifier。
- 不制作可交互原型，不强制 Figma、Penpot 或其他外部设计工具。
- 不建立像素级视觉回归平台。
- 不自动迁移历史项目，不修改产品方向、发布授权或高风险责任边界。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `accessibility-ai-ux-standard`：在适用界面变更中加入开发前静态可视 UX 与明确人类批准。
- `ai-coding-workflow-standard`：禁止实现者在 required UX 未批准时开始生产性实现，禁止在代码中静默改设计。
- `testing-quality-standard`：要求用 Browser E2E 和条件截图对照已批准 UX，截图不替代业务旅程。

## Impact

- 正式规范继续保持四分类、十一项目，体验设计拥有可视 UX 语义。
- 新增 8 个正式 rule-id，总数由 2313 变为 2321；原子来源规则仍为 5956。
- 运行时只同步 `one-person-openspec-rd` 的三个路由/review 文件。
- 回滚通过后续 Standard change 收窄触发范围或移除计划/实现门禁；已有线框和 review 保留为历史证据。
```

- [ ] **Step 4: 创建 `design.md`**

写入：

```markdown
## Context

唯一产品与流程设计依据是 `docs/superpowers/specs/2026-07-24-rd-visual-ux-step-design.md`。本 change 不重复该文档的完整论证，只锁定正式规范、OpenSpec delta、运行时路由和治理追溯的实施边界。

## Goals / Non-Goals

**Goals**

- 形成“产品行为已定义 → 静态低保真 UX → 人工 approved → 直接开发 → 浏览器验证”的可执行链路。
- 让小文案、局部 token/间距和不改变任务/结构/状态/控制的低风险样式修复跳过可视 UX。
- 保留项目内组件复用，避免为一次变更提前抽象跨项目组件体系。

**Non-Goals**

- 通用 UX Kit、catalog、schema、renderer、交互原型、像素级回归平台。
- 新增正式项目、复制体验规则到计划/实现/验证、重写历史替换证据。

## Decisions

### 1. 体验设计是唯一语义 owner

触发条件、静态产物、人工批准、高保真升级和组件复用只在 `04-experience-design.md` 定义。下游仅检查输入、偏离或证据。

### 2. 静态仓库产物是默认

required change 使用一个权威 `ux/<change-id>/` 或项目既有等价目录，包含 `flow.md`、`wireframes/<surface>--<state>.html|svg` 和 `review.md`，其中 `<state>` 至少按适用范围覆盖 `success`、`loading`、`empty`、`error`。HTML/SVG 不含业务脚本、真实 API、数据写入或仓库外资源。

### 3. 人工 approved 阻断生产性实现

只有明确的人类决定可以产生 `approved`。沉默、一般授权、OpenSpec validation、AI 自检或已经写出代码都不能推断批准。批准后实质改变任务路径、结构、状态、权限含义或高风险确认时重新 review。

### 4. 组件复用停留在项目内

优先项目既有组件、设计 token、原生或成熟可访问组件；重复交互组合复用，一次性业务结构不提前晋升为共享系统。

### 5. 历史来源账本只细化映射

8 个新 rule-id 分别细化既有 UX 触发、工件身份、人工判断、计划输入、实现回退和视觉证据来源。更新 `atomic-rules.csv` 与 `coverage-matrix.csv` 的 `target_rule_id`，不增加或伪造 W0–W9 原子行。

## Risks / Trade-offs

- 小改动被流程放大：用窄触发和 `not-required` 理由控制。
- 线框沦为事后附件：把人类批准放在生产性实现前。
- 下游复制产品定义：每个下游文件只保留一条门禁/一致性规则。
- 通用组件建设失控：明确至少两个真实项目出现重复证据后另立 change。
- 截图冒充功能验收：Browser E2E 仍是关键旅程证据，截图只核对视觉结构。

## Migration / Rollback

1. 先 strict validate 本 change。
2. 用失败测试固定 8 个新 rule-id 和 2321 总数。
3. 更新正式规范，再更新既有来源映射和 verifier。
4. 更新并同步运行时 skill。
5. 执行四个路由场景、完整测试、strict validation 和独立 final review。
6. 若成本过高，后续 Standard change 可把触发范围收窄到高风险交互并移除通用门禁，不删除已有历史证据。
```

- [ ] **Step 5: 创建 `tasks.md`**

写入：

```markdown
# Tasks

- [x] 用户认可收窄后的可视 UX 步骤设计。
- [x] 创建本 Standard change 和三个 capability delta，并通过 change strict validation。
- [ ] 先增加 8 个正式 rule-id 与 2321 总数的失败测试。
- [ ] 更新产品设计、体验设计、计划、实现和验证正式规范。
- [ ] 更新原子规则目标映射、覆盖矩阵、verifier 和当前治理状态。
- [ ] 更新并同步 `one-person-openspec-rd` 薄路由与 review rubric。
- [ ] 验收 copy、关键页面、高风险删除和品牌营销页四个路由场景。
- [ ] 运行完整单测、正式规范 verifier、运行时 skill sync 和 OpenSpec strict validation。
- [ ] 完成 producer self-check 和独立 final review。
```

- [ ] **Step 6: 创建三个 delta spec**

`specs/accessibility-ai-ux-standard/spec.md`：

```markdown
## ADDED Requirements

### Requirement: 可视 UX 适用性必须在生产性实现前判定

Standard/High-risk change MUST 在 proposal 中记录 `visual_ux: required | not-required` 和理由。新增或实质改变关键用户任务、页面结构、信息架构、导航、关键 surface 关系、高影响交互、会影响下一步的基本状态，或 desktop/mobile 实质布局差异时 MUST 为 `required`；不改变含义的文案、局部 token/间距/单控件外观和不改变任务、结构、状态或用户控制的低风险修复 MAY 为 `not-required`。

#### Scenario: 新关键页面流程

- **WHEN** change 新增或实质改变关键用户任务与页面结构
- **THEN** proposal 记录 `visual_ux: required`
- **AND** 在生产性实现前完成静态可视 UX

#### Scenario: 不改变含义的文案修正

- **WHEN** change 只修正文案且不改变任务、结构、状态或用户控制
- **THEN** proposal 可以记录 `visual_ux: not-required`
- **AND** 记录不触发理由

### Requirement: Required 可视 UX 必须形成最小静态仓库产物

`visual_ux: required` change MUST 在一个权威目录维护 `flow.md`、`wireframes/<surface>--<state>.html|svg` 和 `review.md`。Wireframes MUST 覆盖关键路径与适用的 loading、empty、error、success；desktop 为默认，只有布局实质不同才增加 mobile；不适用状态 MUST 在 `flow.md` 说明理由。

#### Scenario: 准备关键 surface 的开发前 review

- **WHEN** change 的 `visual_ux` 为 `required`
- **THEN** `flow.md` 记录目标、入口、正常步骤、error/retry/cancel/exit、non-goals 和 wireframe 索引
- **AND** 静态 wireframes 不包含业务脚本、真实 API、数据写入或仓库外资源
- **AND** 重复区域使用项目内稳定语义名称

### Requirement: 生产性实现必须取得明确的人类 UX 批准

`visual_ux: required` change MUST 在生产性实现前由人类明确给出 `approved`。`review.md` MUST 记录 decision owner、reviewed at、artifacts reviewed、decision 和 notes；沉默、一般授权、AI 推断、OpenSpec validation 或后续实现状态 MUST NOT 产生批准。批准后任务路径、结构、状态、权限含义或高风险确认发生实质变化时 MUST 重新 review。

#### Scenario: Required UX 尚未批准

- **WHEN** `review.md` 缺失或 decision 不是 `approved`
- **THEN** 可以继续技术调查或记录开放问题
- **AND** 不得开始或标记 production implementation ready

#### Scenario: 品牌营销页需要更高视觉判断

- **WHEN** 新品牌/营销页、新视觉语言、信息密度或视觉层级使低保真不足
- **THEN** 由人决定是否增加高保真静态设计
- **AND** 不因此增加可交互原型阶段
```

`specs/ai-coding-workflow-standard/spec.md`：

```markdown
## ADDED Requirements

### Requirement: AI 实现必须消费已批准的可视 UX 输入

AI-assisted Standard/High-risk implementation MUST 读取 proposal 的 `visual_ux` 判定。值为 `required` 时，生产性实现前 MUST 链接当前 `flow.md`、关键 wireframes 和人类 `approved` review；AI MUST NOT 用 OpenSpec、文字 brief、一般授权或已生成代码代替该批准。

#### Scenario: Required UX 未批准

- **WHEN** AI 准备开始用户可见生产性实现
- **AND** `visual_ux` 为 `required` 但没有当前人类 `approved`
- **THEN** AI 停止该生产性实现路径
- **AND** 返回体验设计或请求明确决定

#### Scenario: 实现发现已批准方案不成立

- **WHEN** 实现发现任务路径、状态、权限含义或高风险确认需要实质改变
- **THEN** 先更新体验设计并重新取得人类批准
- **AND** 不在代码中静默改变后把 wireframe 标为过期附件
```

`specs/testing-quality-standard/spec.md`：

```markdown
## ADDED Requirements

### Requirement: Required 可视 UX 必须以浏览器证据核对已批准方案

`visual_ux: required` change MUST 用可重复 Browser E2E 证明关键旅程，并用 desktop screenshot 核对已批准 wireframes；只有布局实质不同时才要求 mobile screenshot。验证 MUST 覆盖适用的 loading、empty、error、success、keyboard-only、visible focus 和 focus order，并记录实质差异及重新 review 证据。Screenshot MUST NOT 替代 Browser E2E。

#### Scenario: 实现与已批准 UX 一致

- **WHEN** 在干净完整本地环境验证 required 可视 UX change
- **THEN** Browser E2E 从页面入口完成真实用户动作并断言最终状态
- **AND** desktop screenshot 可与当前批准 wireframe 核对
- **AND** 布局实质不同时有 mobile screenshot

#### Scenario: 浏览器实现存在实质偏差

- **WHEN** 任务路径、结构、状态、权限含义或高风险确认与批准 UX 不一致
- **THEN** 验证不得把该路径标为 accepted
- **AND** 返回体验设计更新并重新 review
```

- [ ] **Step 7: 验证新 change**

Run:

```powershell
openspec validate add-visual-ux-step-to-rd-standards --strict --no-interactive
```

Expected:

```text
Change 'add-visual-ux-step-to-rd-standards' is valid
```

如果 CLI 使用逐项输出，至少应出现该 change 的 `✓` 且退出码为 0。

- [ ] **Step 8: 提交边界**

当前正式规范基线不可安全提交。若本次执行明确需要提交，只允许此时精确 stage 全新的 change 目录和设计状态这一已知单行更新；先运行：

```powershell
git status --short -- docs/superpowers/specs/2026-07-24-rd-visual-ux-step-design.md openspec/changes/add-visual-ux-step-to-rd-standards
git diff --cached --name-only
```

若 staged 列表包含其他路径，停止并清空本次 staging，不提交。用户未要求提交时跳过 commit。

---

### Task 2: 先写正式规则契约测试

**Files:**

- Modify: `tools/test_current_rd_standards.py`

- [ ] **Step 1: 扩展 import 和期望规则表**

把：

```python
from verify_rd_standards import parse_target_ids, validate_repository
```

替换为：

```python
from verify_rd_standards import RULE_ID_RE, parse_target_ids, validate_repository
```

在 `ROOT = Path(__file__).resolve().parents[1]` 后加入：

```python
VISUAL_UX_RULE_IDS_BY_FILE = {
    "docs/02-product-design/04-experience-design.md": {
        "EXPERIENCE-VISUAL-UX-APPLICABILITY",
        "EXPERIENCE-VISUAL-UX-ARTIFACTS",
        "EXPERIENCE-VISUAL-UX-APPROVAL",
        "EXPERIENCE-VISUAL-UX-HIGH-FIDELITY",
    },
    "docs/03-engineering-delivery/06-planning.md": {
        "PLAN-VISUAL-UX-READINESS",
    },
    "docs/03-engineering-delivery/07-implementation.md": {
        "IMPL-VISUAL-UX-GATE",
        "IMPL-VISUAL-UX-DEVIATION",
    },
    "docs/03-engineering-delivery/08-verification.md": {
        "VERIFY-VISUAL-UX-CONFORMANCE",
    },
}
```

- [ ] **Step 2: 更新总数期望并加入新测试**

把：

```python
self.assertEqual(2313, result["rule_id_count"])
```

替换为：

```python
self.assertEqual(2321, result["rule_id_count"])
```

在 `test_repository_uses_only_the_formal_four_category_structure` 后加入：

```python
    def test_visual_ux_step_has_one_owner_and_delivery_gates(self) -> None:
        expected_all: set[str] = set()

        for rel, expected in VISUAL_UX_RULE_IDS_BY_FILE.items():
            text = (ROOT / rel).read_text(encoding="utf-8")
            actual = set(RULE_ID_RE.findall(text))
            self.assertTrue(expected <= actual, f"{rel} missing {sorted(expected - actual)}")
            self.assertTrue(expected_all.isdisjoint(expected))
            expected_all.update(expected)

        self.assertEqual(8, len(expected_all))
```

- [ ] **Step 3: 运行测试并确认按预期失败**

Run:

```powershell
python -m unittest discover -s tools -p "test_current_rd_standards.py" -v
```

Expected: 非零退出；新测试报告 8 个新 rule-id 缺失，repository 测试仍看到 2313 而不是 2321。任何导入错误或无关测试失败都不是预期失败，须先修正测试本身。

---

### Task 3: 让体验设计成为可视 UX 的唯一语义 owner

**Files:**

- Modify: `docs/02-product-design/README.md`
- Modify: `docs/02-product-design/04-experience-design.md`

- [ ] **Step 1: 更新产品设计分类入口**

在 `README.md` 做以下精确替换：

```markdown
- [体验设计](04-experience-design.md)：把已定义行为组织为完整、可访问、可信且可纠正的任务路径；适用时先形成可见的静态 UX 并取得开发前人工确认。
```

```markdown
定义先说明本轮改变与不改变什么，并确定必须由人承担的高影响决定。体验设计消费这些边界，补齐正常、异常、纠正和退出状态；触发可视 UX 时，还要在生产性实现前形成静态方案并取得人工“可开发”确认。若交互推演暴露范围、承诺或风险缺口，则回到定义更新，而不是在界面中静默改变产品含义。
```

```markdown
当用户行为、非范围、验收与退出条件明确，关键任务路径及其异常、可访问和高影响控制边界完整，且适用的可视 UX 已由人确认时，可交给工程交付。任何后续证据推翻目标、用户场景、承诺或体验前提时，返回定义或体验设计重新判断。
```

```markdown
从立项接收已选择的问题、证据和投入边界；向工程交付提供稳定的产品行为、体验契约、适用的已批准可视 UX、验收和风险边界。工程验证或运行评估发现行为不成立、用户无法完成任务或信任边界被破坏时，把证据退回对应项目，而不是由下游自行重写产品决定。
```

- [ ] **Step 2: 在体验设计“重新组织后的规范要求”下新增唯一语义段**

在 `## 重新组织后的规范要求` 与 `### 交互契约、组件与错误` 之间插入：

```markdown
### 开发前可视 UX

<!-- rule-id: EXPERIENCE-VISUAL-UX-APPLICABILITY -->
- 新增或实质改变关键用户任务、页面结构、信息架构、导航、关键 surface 关系、高影响交互、会显著影响用户下一步的 loading/empty/error/success，或 desktop/mobile 存在实质布局差异时，须在生产性实现前执行可视 UX。Standard/High-risk change 在 proposal 中记录 `visual_ux: required | not-required` 与理由；是否触发存在合理疑问时按 `required` 处理。不改变含义的文案、局部 token/间距/单控件外观，以及不改变任务、结构、状态和用户控制的低风险样式修复默认不触发。

<!-- rule-id: EXPERIENCE-VISUAL-UX-ARTIFACTS -->
- `visual_ux: required` 的 change 在 `ux/<change-id>/` 或项目既有的一个权威设计目录维护 `flow.md`、`wireframes/<surface>--<state>.html|svg` 与 `review.md`，其中 `<state>` 按适用范围覆盖 `success`、`loading`、`empty`、`error`。`flow.md` 记录用户目标、入口、正常步骤、error/retry/cancel/exit、non-goals 和线框索引；线框只表达布局、信息层级、内容与操作位置，不含业务脚本、真实 API、数据写入或仓库外资源。desktop 为默认，只有布局实质变化时才补 mobile；不适用状态须在 `flow.md` 说明理由。

<!-- rule-id: EXPERIENCE-VISUAL-UX-APPROVAL -->
- `review.md` 至少记录 Decision owner、Reviewed at、Artifacts reviewed、Decision 与 Notes。只有明确的人类决定可以产生 `approved`；AI 不得根据沉默、一般授权、OpenSpec validation 或后续实现状态推断批准。`approved` 是进入生产性实现的门禁；批准后任务路径、结构、状态、权限含义或高风险确认发生实质变化时，须更新可视 UX 并重新 review。

<!-- rule-id: EXPERIENCE-VISUAL-UX-HIGH-FIDELITY -->
- 低保真静态 UX 是默认。新品牌/营销页面、新视觉语言、信息密度或视觉层级本身构成主要风险，或低保真不足以支持真实取舍时，由人决定是否增加高保真静态设计；该升级不增加可交互原型阶段，确认后仍直接进入开发。
```

- [ ] **Step 3: 收紧组件复用与 playbook 边界**

把 `EXPERIENCE-COMPONENT-CHOICE` 的正文替换为：

```markdown
- 可视 UX 与实现默认优先当前项目已有组件、设计 token、原生控件或成熟可访问组件；在线框中用 `AppShell`、`FormField`、`StatePanel`、`ConfirmAction` 等稳定语义名称标出重复区域，同一项目的重复交互只实现一次并通过组合复用，一次性业务结构留在当前 change。采用自定义复杂 widget 必须由人判断；跨项目 catalog、通用 UX Kit 和共享 renderer 另立 change。
```

把 `EXPERIENCE-PLAYBOOK-BOUNDARY` 的正文替换为：

```markdown
- 轻量静态 wireframes 与开发前人工 review 属于条件触发的体验设计步骤，并服从本规范的正式分类及项目原则。完整品牌系统、通用 UX Kit、设计稿协作流程、大型组件库、视觉回归平台或全面用户研究计划不属于此轻量流程；法律级无障碍审计或正式 VPAT 转交专业审阅或单独 change。
```

- [ ] **Step 4: 更新输入、产物和完成条件**

把三个段落分别替换为：

```markdown
输入包括已批准的产品行为和范围、目标用户与关键任务、AI 行为/风险定义、权限与数据边界、错误合同，以及运行和支持场景。进入可视 UX 前还须已有本轮改变/不改变的行为、验收与退出条件、已知错误和降级场景；上游输入不成立时返回定义。
```

```markdown
产物按适用范围包括 surface map、interaction contract、component contract、状态与错误映射、accessibility test plan、AI disclosure、授权/确认设计、敏感输入提示和支持入口。触发可视 UX 时还包括一个权威目录中的 `flow.md`、关键静态 wireframes 和人类 review；单纯内部低风险界面或不触发条件的局部修正不要求机械创建全部工件。
```

```markdown
体验设计在关键任务、组件与输入方式、基本/AI 状态、错误与下一步、键盘/焦点、可访问性、AI disclosure/纠错/降级、敏感输入和高风险确认均已覆盖，且适用的可视 UX 已取得人类 `approved` 时完成。缺少可视 UX 批准、例外批准、敏感数据收集决定、高影响 AI、异步控制或通知变化时停止；需要改变产品行为或范围时返回定义。
```

- [ ] **Step 5: 局部检查**

Run:

```powershell
rg -n "EXPERIENCE-VISUAL-UX-|通用 UX Kit|可交互原型|approved" docs/02-product-design/README.md docs/02-product-design/04-experience-design.md
```

Expected: 4 个新 rule-id 只出现在 `04-experience-design.md`；入口只做概述；通用 UX Kit 和可交互原型只出现在明确排除边界中。

---

### Task 4: 加入计划、实现和验证的消费门禁

**Files:**

- Modify: `docs/03-engineering-delivery/06-planning.md`
- Modify: `docs/03-engineering-delivery/07-implementation.md`
- Modify: `docs/03-engineering-delivery/08-verification.md`

- [ ] **Step 1: 在计划中加入 readiness**

在 `PLAN-SERVICE-CHANGE-START` 后插入：

```markdown
<!-- rule-id: PLAN-VISUAL-UX-READINESS -->
- Standard/High-risk change 的计划须读取 proposal 中的 `visual_ux` 判定。值为 `required` 时，计划链接当前 `flow.md`、关键 wireframes 和 `review.md`；尚未取得人类 `approved` 时可以记录技术调查或开放问题，但不得把生产性实现任务标记为 ready。值为 `not-required` 时保留理由，不补造 UX 工件。
```

把计划的“输入与产物”和“完成、停止或退出条件”替换为：

```markdown
输入包括已经确认的产品与体验设计、OpenSpec change、适用的 `visual_ux` 判定及其当前 review、风险和人工判断边界、现有任务状态，以及专项要求的工件入口。产物包括唯一执行清单、排序后的批次、所需前置工件、恢复上下文、开放决策和下一步；计划只引用其他项目的证据或动作，不复制其权威规则。
```

```markdown
当工作已拆成有序批次、每个批次有权威状态、前置输入与专项路由明确，适用的可视 UX 已取得人类批准，且接手者可从记录恢复上下文时，计划可交给实现。产品或体验输入未确认、`visual_ux: required` 尚未批准、风险路径不清、需要人工判断而尚未决定，或 OpenSpec 与实际工作不一致时停止；实现中发现范围或边界变化时返回相应产品或技术设计项目重新计划。
```

- [ ] **Step 2: 在实现中加入批准与偏离回退**

在 `IMPL-SPEC-TO-TASKS-HANDOFF` 后插入：

```markdown
<!-- rule-id: IMPL-VISUAL-UX-GATE -->
- 用户可见 Standard/High-risk 实现开始前须读取 proposal 的 `visual_ux` 判定；值为 `required` 时，只有计划引用当前 `flow.md`、关键 wireframes 和人类 `approved` review，且项目内组件复用选择已说明，才可开始相关生产性编码。缺失任一输入时返回体验设计或计划，不得用 OpenSpec、文字 brief 或已生成代码代替批准。
```

在 `IMPL-W4-AUTHORITY-BOUNDARY` 后插入：

```markdown
<!-- rule-id: IMPL-VISUAL-UX-DEVIATION -->
- 实现发现已批准方案中的任务路径、页面结构、状态、权限含义或高风险确认无法成立，或需要产生实质偏差时，须停止受影响路径，先更新可视 UX 并重新取得人类批准；不得只在代码中改变界面，再把线框当作过期附件。
```

把实现的“输入与产物”和“完成、停止或退出条件”替换为：

```markdown
输入包括已经批准的产品和体验要求、适用的 `visual_ux` 判定与当前人类 review、技术设计、OpenSpec change 与 `tasks.md`、现有仓库模式、数据与权限边界、实际触发的专项工件和人工判断结果。产物包括可 review 的代码批次、配置与 flag、schema/migration/query、生成代码、前端与后端实现、AI runtime 与 job、可复现工作区命令、残余风险和交接引用。
```

```markdown
当实际触发表面均有对应实现、上游输入和已批准可视 UX 未被暗改、生成物来自权威源、本地能够构建或已有具体阻塞说明、高风险控制与人工 checkpoint 清楚、残余风险已移交时，实现可以进入验证。出现产品方向或契约边界变化、required UX 缺少批准或发生未复审的实质偏差、生产副作用即将发生、数据或权限边界不清，或无法保持可回滚与可审查批次时停止；不得用下游验证或发布阶段掩盖实现缺口。
```

- [ ] **Step 3: 在验证中加入已批准 UX 对照**

把 `VERIFY-VISUAL-REGRESSION-EVIDENCE` 正文替换为：

```markdown
- 条件“发生视觉或响应式变化时”成立时，至少保存 desktop screenshot；只有 mobile 布局实质不同时才要求 mobile screenshot。可以增加 Playwright 视觉断言，但截图或视觉断言都不能替代从页面入口执行真实业务动作的 Browser E2E。
```

紧接该规则后插入：

```markdown
<!-- rule-id: VERIFY-VISUAL-UX-CONFORMANCE -->
- `visual_ux: required` 的 change 须在干净完整本地环境用 Browser E2E 证明关键旅程，并对照当前人类批准的 `flow.md` 与 wireframes 核对 desktop、适用的 mobile、loading、empty、error、success、keyboard-only、visible focus 和 focus order。任务路径、结构、状态、权限含义或高风险确认存在实质差异时，记录差异并返回体验设计重新 review；未完成前不得把该路径标为 accepted。
```

把验证的“输入与产物”、完成段首句和第一条相关项目引用调整为：

```markdown
输入至少包括已确认的产品行为与验收、技术与风险边界、实现差异、适用的 `visual_ux` 判定与已批准 UX、测试/eval 数据、环境与依赖说明。产物由上文各 canonical rule 定义，按触发条件形成 test strategy、matrix、journey、run record、eval gate、浏览器/截图对照、专项检查、失败证据及人工 checkpoint；相同事实只保留一个权威记录，其他项目引用其 target 或工件链接。
```

```markdown
完成意味着适用目标均有当前证据，命令、环境、启动组件、覆盖路径、结果与未覆盖项可定位，关键旅程达到要求的证据层级，required 可视 UX 与实现的一致性已核对，失败与例外已有真实处置。
```

```markdown
- “定义”与“体验设计”提供产品行为、关键旅程、适用的已批准可视 UX 和验收口径；验证只证明，不重定义。
```

- [ ] **Step 4: 证明下游没有复制体验定义**

Run:

```powershell
rg -n "PLAN-VISUAL-UX-READINESS|IMPL-VISUAL-UX-GATE|IMPL-VISUAL-UX-DEVIATION|VERIFY-VISUAL-UX-CONFORMANCE" docs/03-engineering-delivery
rg -n "visual_ux: required|flow.md|wireframes|approved" docs/03-engineering-delivery/06-planning.md docs/03-engineering-delivery/07-implementation.md docs/03-engineering-delivery/08-verification.md
```

Expected: 计划 1 个新 rule-id、实现 2 个、验证 1 个；下游文本只说明输入、门禁、偏离和证据，不重新定义触发矩阵或高保真升级。

---

### Task 5: 同步来源映射、rule 数和当前治理状态

**Files:**

- Modify: `README.md`
- Modify: `governance/rd-standards/review/atomic-rules.csv`
- Modify: `governance/rd-standards/review/coverage-matrix.csv`
- Modify: `tools/verify_rd_standards.py`
- Modify: `governance/rd-standards/approvals.jsonl`
- Modify: `governance/current-status.json`
- Verify unchanged: `governance/rd-standards/replacement-manifest.json`

- [ ] **Step 1: 在 verifier 中建立当前总数常量**

在 `EXPECTED_LEDGER_ROWS` 后加入：

```python
EXPECTED_FORMAL_RULE_IDS = 2321
```

把：

```python
    if len(markers) != 2313:
        errors.append(f"Expected 2313 rule IDs, found {len(markers)}")
```

替换为：

```python
    if len(markers) != EXPECTED_FORMAL_RULE_IDS:
        errors.append(
            f"Expected {EXPECTED_FORMAL_RULE_IDS} rule IDs, found {len(markers)}"
        )
```

并把：

```python
        errors.append("Coverage target IDs do not match the 2313 formal rule markers")
```

替换为：

```python
        errors.append("Coverage target IDs do not match the current formal rule markers")
```

- [ ] **Step 2: 同步正式入口的当前计数**

在根 `README.md` 中把：

```markdown
正式正文包含 2,313 个唯一稳定规则目标；5,956 条来源原子规则及其处理决定保留在治理账本中。账本负责历史来源追溯，不构成第二份正式规范。
```

替换为：

```markdown
正式正文包含 2,321 个唯一稳定规则目标；5,956 条来源原子规则及其处理决定保留在治理账本中。账本负责历史来源追溯，不构成第二份正式规范。
```

- [ ] **Step 3: 精确扩展 8 条既有原子来源的目标映射**

在 `atomic-rules.csv` 和 `coverage-matrix.csv` 中，对相同 `rule_id` 做相同的 `target_rule_id` 替换；不得改变其他列或行数：

| rule_id | 原 target_rule_id | 新 target_rule_id |
| --- | --- | --- |
| `RULE-W5-001-057` | `EXPERIENCE-UX-APPLICABILITY` | `EXPERIENCE-UX-APPLICABILITY;EXPERIENCE-VISUAL-UX-APPLICABILITY` |
| `RULE-W5-003-016` | `EXPERIENCE-UX-ARTIFACT-IDENTITY` | `EXPERIENCE-UX-ARTIFACT-IDENTITY;EXPERIENCE-VISUAL-UX-ARTIFACTS` |
| `RULE-W5-003-021` | `VERIFY-ACCESSIBILITY-AI-UX-W5-003-L054` | `VERIFY-ACCESSIBILITY-AI-UX-W5-003-L054;EXPERIENCE-VISUAL-UX-APPROVAL` |
| `RULE-W5-003-231` | `EXPERIENCE-TRUSTWORTHY-INTERACTION` | `EXPERIENCE-TRUSTWORTHY-INTERACTION;EXPERIENCE-VISUAL-UX-HIGH-FIDELITY` |
| `RULE-W4-002-112` | `PLAN-SERVICE-CHANGE-START` | `PLAN-SERVICE-CHANGE-START;PLAN-VISUAL-UX-READINESS` |
| `RULE-W2-047` | `IMPL-SPEC-TO-TASKS-HANDOFF` | `IMPL-SPEC-TO-TASKS-HANDOFF;IMPL-VISUAL-UX-GATE` |
| `RULE-W4-001-005` | `IMPL-W4-AUTHORITY-BOUNDARY` | `IMPL-W4-AUTHORITY-BOUNDARY;IMPL-VISUAL-UX-DEVIATION` |
| `RULE-W5-002-136` | `VERIFY-VISUAL-REGRESSION-EVIDENCE` | `VERIFY-VISUAL-REGRESSION-EVIDENCE;VERIFY-VISUAL-UX-CONFORMANCE` |

用 PowerShell 只读核对：

```powershell
$ids = @(
  'RULE-W5-001-057',
  'RULE-W5-003-016',
  'RULE-W5-003-021',
  'RULE-W5-003-231',
  'RULE-W4-002-112',
  'RULE-W2-047',
  'RULE-W4-001-005',
  'RULE-W5-002-136'
)
$atomic = Import-Csv -LiteralPath 'governance/rd-standards/review/atomic-rules.csv'
$coverage = Import-Csv -LiteralPath 'governance/rd-standards/review/coverage-matrix.csv'
$atomic | Where-Object { $ids -contains $_.rule_id } | Select-Object rule_id,target_rule_id
$coverage | Where-Object { $ids -contains $_.rule_id } | Select-Object rule_id,target_rule_id
```

Expected: 两组各 8 行，映射完全相同。

- [ ] **Step 4: 追加设计批准记录**

向 `governance/rd-standards/approvals.jsonl` 追加一行合法 JSON：

```json
{"approval_id":"VISUAL-UX-STEP-2026-07-24-DESIGN-APPROVED","decision":"approved","decided_by":"user","decided_on":"2026-07-24","decision_source":"current-codex-task:user-message:可以","scope":"Approve the narrowed design that adds a conditional static visual UX sub-step and explicit human development approval to the existing R&D standards; exclude a generic UX Kit, catalog, schema, renderer, interactive prototype, and dedicated UX verifier.","git_actions":"not-authorized"}
```

- [ ] **Step 5: 先运行绿色结构测试**

Run:

```powershell
python -m unittest discover -s tools -p "test_current_rd_standards.py" -v
python tools/verify_rd_standards.py .
```

Expected:

```text
Ran 5 tests
OK
RD_STANDARDS=PASS categories=4 items=11 rule_ids=2321 review_files=7
```

- [ ] **Step 6: 更新当前状态，不改历史 replacement manifest**

在 `governance/current-status.json` 中：

- 把 `latest_evidence.formal_rule_target_count` 从 `2313` 改为 `2321`；
- 保留 `atomic_rule_count: 5956`；
- 在 `latest_evidence` 下增加：

```json
"latest_change": {
  "id": "add-visual-ux-step-to-rd-standards",
  "design": "docs/superpowers/specs/2026-07-24-rd-visual-ux-step-design.md",
  "decision": "approved",
  "formal_rule_target_count_before": 2313,
  "formal_rule_target_count_after": 2321,
  "atomic_rule_count": 5956
},
```

- 最终验证完成后，把 `latest_evidence.final_verification` 更新为本次真实日期与结果；预期为 101 个完整单测、2321 个正式 rule-id、59 个 OpenSpec 项，但必须以实际输出为准，不能在命令未运行时先写 PASS。

确认历史数字未被改写：

```powershell
$replacement = Get-Content -Raw -LiteralPath 'governance/rd-standards/replacement-manifest.json' | ConvertFrom-Json
$replacement.formal_targets.rule_target_count
$replacement.formal_targets.atomic_rule_count
```

Expected:

```text
2313
5956
```

---

### Task 6: 更新薄运行时路由，不复制体验正文

**Files:**

- Modify: `skills/one-person-openspec-rd/SKILL.md`
- Modify: `skills/one-person-openspec-rd/references/workflow-map.md`
- Modify: `skills/one-person-openspec-rd/references/review-rubric.md`
- Mechanically sync: installed `one-person-openspec-rd` copies of the same three files
- Do not modify: `skills/one-person-openspec-rd/agents/openai.yaml`
- Do not modify: `skills/one-person-openspec-rd/references/stack-defaults.md`

- [ ] **Step 1: 更新 Standard 路由**

在 `SKILL.md` 的 Standard 段，把现有“新用户能力……”一条替换为：

```markdown
- 新用户能力、新服务或重大体验变化在生产性实现前，确认产品输入和体验设计；OpenSpec 只链接它们，不能替代。用户可见 Standard/High-risk change 还要在 proposal 记录 `visual_ux: required | not-required` 与理由；required 时须链接当前静态 UX 和明确的人类 `approved` review 后再开始相关生产性实现。
```

在 Review 段把现有“reviewer 对照……”一条替换为：

```markdown
- reviewer 对照权威产品输入、体验设计和验收映射，不以 OpenSpec 代替需求；`visual_ux: required` 时还核对当前人类批准、实现偏差和重新 review 证据。
```

在 Completion 清单中的“OpenSpec change id、validation 和 archive/review 状态，或经用户批准的跳过记录”后加入：

```markdown
- 用户可见 Standard/High-risk 的 `visual_ux` 判定；required 时包含批准状态与当前工件入口；
```

- [ ] **Step 2: 更新 fallback map**

把 `workflow-map.md` 第 34 行对应段落替换为：

```markdown
For user-visible Standard/High-risk work, record `visual_ux: required | not-required` and the reason in the proposal. When required, link the current static UX artifacts and explicit human `approved` review before production implementation. Also define critical journeys in `governance/quality/user-journeys.json` and close one real Browser E2E early. Put guard artifacts under `governance/<registered-domain>/`; use `governance/current-status.json` as the only current completion state.
```

- [ ] **Step 3: 更新 review rubric**

在 Producer Self-Check 的产品输入检查后加入：

```markdown
- 用户可见 Standard/High-risk 是否记录 `visual_ux` 判定；required 时，当前静态 UX 是否由人明确 `approved`，批准后实质偏差是否重新 review？
```

在 Independent Final Review 的产品输入检查后加入：

```markdown
- 对 `visual_ux: required` 的 change，读取当前 `flow.md`、关键 wireframes、人工批准和偏差记录；缺少批准或存在未复审实质偏差时不得接受；
```

在 Standard 通过条件中加入：

```markdown
- `visual_ux: required` 时有当前人类批准，且实现实质偏差已经重新 review；
```

在“不能作为通过证据”中加入：

```markdown
- 用 AI 推断、一般授权、OpenSpec validation 或已经完成的实现代替可视 UX 人类批准；
```

- [ ] **Step 4: 确认 canonical 只改三个文件**

Run:

```powershell
git status --short -- skills/one-person-openspec-rd
```

Expected: 本任务相对开始状态只额外改变 `SKILL.md`、`references/workflow-map.md`、`references/review-rubric.md`；`agents/openai.yaml` 与 `stack-defaults.md` 的既有状态不被本任务改写。

- [ ] **Step 5: 机械同步运行时副本**

先运行 checker；预期 canonical 修改后出现三个 mismatch。然后执行：

```powershell
$rdRuntimeSkillsRoot = if ($env:CODEX_HOME) {
  Join-Path $env:CODEX_HOME 'skills'
} else {
  Join-Path $env:USERPROFILE '.codex\skills'
}
$canonical = Resolve-Path -LiteralPath 'skills/one-person-openspec-rd'
$installed = Join-Path $rdRuntimeSkillsRoot 'one-person-openspec-rd'
$files = @(
  'SKILL.md',
  'references/workflow-map.md',
  'references/review-rubric.md'
)
foreach ($rel in $files) {
  $source = Join-Path $canonical $rel
  $target = Join-Path $installed $rel
  Copy-Item -LiteralPath $source -Destination $target -Force
}
python tools/check_runtime_skill_sync.py .
```

Expected:

```text
RUNTIME_SKILL_SYNC=PASS status=synced legacy_present=0 preserved_missing=0
```

---

### Task 7: 做四个路由场景和最终审查

**Files:**

- Modify: `openspec/changes/add-visual-ux-step-to-rd-standards/tasks.md`
- Create after review: `openspec/changes/add-visual-ux-step-to-rd-standards/review.md`
- Modify after verification: `governance/current-status.json`

- [ ] **Step 1: Producer 用四个场景逐项核对**

必须得到以下结论，且每项能引用正式 rule-id：

| 场景 | 预期 |
| --- | --- |
| 只修正不改变含义的文案 | `visual_ux: not-required`，记录理由，不补造工件 |
| 新增关键页面任务流 | `visual_ux: required`，低保真静态 UX + 人类批准后开发 |
| 新增高风险删除确认 | `visual_ux: required`，线框显示真实影响与退出/撤销边界 + 人类批准 |
| 新品牌营销页 | 先做 required 低保真，由人决定是否补高保真；不做交互原型 |

若任一场景需要依赖下游文件才能理解触发语义，返回 Task 3 收敛 owner；不得把触发矩阵复制到 skill。

- [ ] **Step 2: 运行 producer self-check**

至少检查：

- 8 个新 rule-id 的 owner 唯一且没有重复；
- 计划、实现、验证只消费体验输入；
- `UX Kit`、catalog、schema、renderer、interactive prototype 只出现在 non-goal/boundary；
- 没有新 `verify_ux_*` 文件；
- 5956 条原子规则与覆盖行未增减；
- `replacement-manifest.json` 的历史 2313/5956 未修改；
- required 人类批准不被一般授权、AI 或 validation 替代；
- screenshot 不被称为 Browser E2E。

- [ ] **Step 3: 请求未参与产出的 reviewer 做独立 final review**

Reviewer 必须读取：

- 已批准设计；
- 本 OpenSpec proposal/design/delta/tasks；
- 五份正式规范 diff；
- 三份 canonical skill diff；
- 8 条 atomic/coverage 映射；
- 测试与四场景结果。

`review.md` 使用以下结构并填写真实值：

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

只有真实 reviewer 给出 `accept` 才可完成。`changes-requested` 或 `reject` 时修正、重跑受影响检查并重新 review，不能预填接受结论。

- [ ] **Step 4: 更新 tasks 与当前状态**

Reviewer 接受且 Task 8 全部通过后：

- 将 `tasks.md` 中全部实现、验证和 review 项勾为 `[x]`；
- 用实际输出更新 `governance/current-status.json` 的 `latest_evidence.final_verification`；
- `status` 保持 `complete`，`atomic_rule_count` 保持 5956，`formal_rule_target_count` 为 2321；
- OpenSpec change 保持 active，不在本任务 archive；归档会修改当前已存在且带用户改动的主 specs，应另行决定。

---

### Task 8: 完整验证与安全交付

**Files:**

- Verify all changed paths

- [ ] **Step 1: 运行全部本地测试**

Run:

```powershell
python -m unittest discover -s tools -p "test_*.py" -v
```

Expected baseline after adding one test:

```text
Ran 101 tests
OK
```

如果实际总数不是 101，先解释测试发现范围变化；不得只修改治理摘要来匹配。

- [ ] **Step 2: 运行三项正式门禁**

Run:

```powershell
python tools/verify_rd_standards.py .
python tools/check_runtime_skill_sync.py .
openspec validate --all --strict --no-interactive
```

Expected:

```text
RD_STANDARDS=PASS categories=4 items=11 rule_ids=2321 review_files=7
RUNTIME_SKILL_SYNC=PASS status=synced legacy_present=0 preserved_missing=0
Totals: 59 passed, 0 failed (59 items)
```

- [ ] **Step 3: 检查禁建内容和路径范围**

Run:

```powershell
rg --files | rg "verify_ux_|ux-kit|ux_kit|catalog|renderer"
git status --short -- docs/02-product-design docs/03-engineering-delivery skills/one-person-openspec-rd governance/rd-standards governance/current-status.json tools/verify_rd_standards.py tools/test_current_rd_standards.py openspec/changes/add-visual-ux-step-to-rd-standards
```

Expected: 第一条不出现本 change 新增的专用工具或平台文件；第二条只显示计划内路径加任务开始前已经存在的基线状态。`.superpowers/` 和其他无关 dirty paths 不属于本任务，不清理。

- [ ] **Step 4: 最终一致性检查**

Run:

```powershell
$formal = python tools/verify_rd_standards.py . --json | ConvertFrom-Json
$status = Get-Content -Raw -LiteralPath 'governance/current-status.json' | ConvertFrom-Json
$replacement = Get-Content -Raw -LiteralPath 'governance/rd-standards/replacement-manifest.json' | ConvertFrom-Json
$formal.rule_id_count
$status.latest_evidence.formal_rule_target_count
$replacement.formal_targets.rule_target_count
```

Expected:

```text
2321
2321
2313
```

这三个数字分别代表当前正式规范、当前治理状态和历史替换事件，不能强行改成同一个数字。

- [ ] **Step 5: 交付**

最终说明：

- Standard change id 与设计依据；
- 正式规范新增的可视 UX 路径；
- 组件复用保留但通用 UX Kit 未建设；
- 101 tests、2321 rule-id、runtime sync、59 OpenSpec items 和 independent review 的实际结果；
- OpenSpec change 仍 active；
- 因权威目标文件在任务开始前已是 untracked/modified，本轮没有把这些既有基线整体提交；若用户需要 Git 整理，另行做精确范围决定。
