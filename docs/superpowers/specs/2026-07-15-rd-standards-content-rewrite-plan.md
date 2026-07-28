# 研发规范内容重写执行方案

状态：历史执行记录（2026-07-28 退役，不得再作为执行入口）
日期：2026-07-15  
适用范围：`docs/W0-*` 至 `docs/W9-*` 现有内容  
目标使用者：用户本人 + Codex

> 归档说明：本方案对应的重写工作已被当前正式三层规范取代；相关 OpenSpec 变更已归档至 `openspec/changes/archive/2026-07-28-build-rd-rewrite-guardrails/` 与 `openspec/changes/archive/2026-07-28-rewrite-rd-standards-content/`。`tools/rd_rebuild.py` 及其命令已经退役，本文中的命令仅保留为历史审计证据。当前入口以根 `README.md` 和 `tools/verify_rd_standards.py` 为准。

## 1. 方案定位

本方案用于指导研发规范的内容重写，不是最终目录迁移方案。

它授权的工作只有：

1. 先创建并验证本方案定义的约束工具；
2. 完整 review W0–W9；
3. 把原内容拆成可追溯的原子规则；
4. 将规则重新归入四个分类下的十一项；
5. 在规则组织过程中提炼项目原则和分类原则；
6. 形成并审查一套与旧规范并存的新草稿。

它不授权：

- 删除、移动或覆盖任何现有规范；
- 用新草稿替换当前入口；
- 改造 OpenSpec 目录；
- 提交、推送、stash、reset 或 checkout；
- 根据文件数或总行数强行压缩内容；
- 执行最终重建迁移。

最终迁移必须在草稿、覆盖矩阵和退出清单全部经用户批准后，另行制定实施计划。

本方案取代此前以大范围删除为核心的 `docs/superpowers/specs/2026-07-15-rd-standards-rebuild-design.md`。旧设计仅作为失败记录保留，不能再作为执行依据。此前在讨论中提前写出的原则草案同样不构成来源或约束。

## 2. 固定目标结构

四个分类与十一项的关系固定如下：

```text
立项
├─ 选题
└─ 调研

持续演进
├─ 产品设计
│  ├─ 定义
│  └─ 体验设计
├─ 工程交付
│  ├─ 技术设计
│  ├─ 计划
│  ├─ 实现
│  ├─ 验证
│  └─ 发布
└─ 运行维护
   ├─ 运行
   └─ 评估
```

这里共有四个分类：

1. 立项；
2. 产品设计；
3. 工程交付；
4. 运行维护。

“持续演进”不是第五个分类，而是产品立项后的循环关系：产品设计 → 工程交付 → 运行维护 → 下一轮产品设计或工程交付。

“产品计划”属于定义，回答本轮做什么；十一项中的“计划”是工程计划，回答如何完成交付。

## 3. 核心重写原则

### 3.1 原则必须自下而上形成

不能先编写原则，再把旧内容套入原则。

正确顺序是：

```text
完整原文
  ↓
原子规则
  ↓
按意图形成规则簇
  ↓
归入十一项
  ↓
形成项目原则候选
  ↓
形成分类原则候选
```

每条项目原则必须能够反向追溯到支持它的原子规则集合。每条分类原则必须能够追溯到分类下的项目原则和规则簇。

### 3.2 不直接搬运或复制旧内容

最终草稿不能整段复制旧文件，也不能用“把 W 目录改名”的方式完成迁移。

旧内容只作为来源。重写时需要：

- 识别规则真正解决的问题；
- 拆开混在同一段中的不同要求；
- 合并意图相同但表述不同的规则；
- 重新确定规则在研发流程中的位置；
- 用新上下文重新表达；
- 保留仍然有效的具体技术决定和风险边界。

### 3.3 原则与执行细节分层

每个分类和每一项都必须有“根本性原则”列表，但原则不能包含框架、数据库、目录、命令或具体工具。

内容分为四层：

1. **根本原则**：长期稳定、能够指导判断、不依赖具体工具；
2. **规范要求**：在明确条件下必须满足的行为或边界；
3. **执行细则**：框架、数据库、技术栈、目录、工具和命令；
4. **依据与参考**：来源、案例、外部标准和历史背景。

具体内容不能因为不属于原则层就被删除。MySQL、sqlc、Go/Kratos、Vite/React、前后端组织方式、安全门禁和验证命令等应保留在相应项目的规范要求或执行细则中。

### 3.4 一个规则只有一个权威位置

每条重写后的规则只有一个主要归属。其他项目需要使用时，只建立引用，不复制正文。

跨阶段原文如果包含多个独立意图，应拆成多条原子规则分别归属，而不是把同一句话复制到多个项目。

### 3.5 精简来自重组和去重

不设置总文件数或总行数削减指标。精简通过以下方式获得：

- 删除重复解释；
- 合并同义规则；
- 移除无决策价值的流程外壳；
- 让默认入口只提供导航；
- 让具体内容按十一项和真实触发条件加载。

任何内容退出都必须有逐条理由，不能按目录、文件名、历史状态或篇幅批量判定。

## 4. 执行产物

规范内容重写只在独立草稿区工作，不修改 W0–W9。约束工具、运行状态和 OpenSpec change 分别进入本节后文规定的工具区、治理区和 OpenSpec 工作区。

建议草稿结构：

```text
rebuild-draft/
  README.md
  01-initiation/
    README.md
    01-topic-selection.md
    02-research.md
  02-product-design/
    README.md
    03-definition.md
    04-experience-design.md
  03-engineering-delivery/
    README.md
    05-technical-design.md
    06-planning.md
    07-implementation.md
    08-verification.md
    09-release.md
  04-operations-maintenance/
    README.md
    10-operation.md
    11-evaluation.md
  review/
    source-inventory.csv
    source-segments.csv
    atomic-rules.csv
    coverage-matrix.csv
    principle-traceability.csv
    conflicts.md
    retirement-candidates.md
```

`rebuild-draft/` 是并行草稿，不是新正式入口。用户批准最终迁移前，任何现有文件仍然有效。

## 5. 阶段一：冻结范围并建立来源清单

### 5.1 固定来源范围

本轮主要来源只包括：

```text
docs/W0-intake/
docs/W1-discovery/
docs/W2-openspec-risk/
docs/W3-ai-behavior/
docs/W4-build/
docs/W5-verify/
docs/W6-release/
docs/W7-operate/
docs/W8-learn/
docs/W9-maintain/
```

其他 README、knowledge、OpenSpec 主规格、历史 change、review 和 skill 不在本轮直接重写范围内。它们只能在 W0–W9 草稿形成后用于查漏、识别冲突或确认来源，不能代替对 W0–W9 的完整 review。若要扩展来源范围，必须先获得用户确认。

### 5.2 完整读取

逐文件完整读取，不能只读取标题、目录、摘要、规则关键词或索引。

建议分四批执行：

1. W0–W2；
2. W3–W4；
3. W5–W6；
4. W7–W9。

每批结束只更新来源清单和原子规则，不提前定稿分类原则。

### 5.3 来源清单字段

`review/source-inventory.csv` 至少包含：

```text
source_id
path
title
original_purpose
applicability
major_topics
referenced_sources
known_overlaps
known_conflicts
review_status
reviewed_at
```

完成条件：W0–W9 的每个文件恰好出现一次，且 `review_status=reviewed`。

### 5.4 来源分段账本

完整读取不能只靠“文件已读”的声明证明。`review/source-segments.csv` 将每个来源文件划成连续、可追溯的语义段，至少包含：

```text
segment_id
source_id
source_start_line
source_end_line
segment_kind
atomic_rule_ids
disposition
notes
```

`segment_kind` 允许值：

- `rule-bearing`
- `context`
- `example`
- `navigation`
- `duplicate`
- `empty`

除空白行外，每一行必须恰好被一个来源分段覆盖。`rule-bearing` 分段必须关联至少一条原子规则；其他分段必须说明为什么不形成规则。这个账本证明内容被逐段处理，但不能证明语义判断一定正确，语义正确性仍由后续审查确认。

## 6. 阶段二：拆分原子规则

### 6.1 原子规则定义

一条原子规则只表达一个可以独立保留、重写、合并、拆分或退出的判断。

遇到以下情况必须拆分：

- 一句话同时包含产品、技术和发布要求；
- 一条规则同时包含原则和具体工具；
- 一个段落同时包含适用条件、执行动作和验证证据；
- 一个列表项包含多个能够独立变化的约束。

### 6.2 原子规则记录

`review/atomic-rules.csv` 至少包含：

```text
rule_id
source_id
source_path
source_start_line
source_end_line
source_text
intent
applies_when
subject
rule_layer
candidate_category
candidate_item
secondary_impacts
cluster_id
treatment
target_rule_id
notes
```

`source_text` 只用于内部追溯，不能直接进入最终规范。

`rule_layer` 允许值：

- `principle-input`
- `normative-requirement`
- `risk-or-approval-boundary`
- `artifact-or-evidence`
- `implementation-detail`
- `reference-or-rationale`

`treatment` 初始为 `unreviewed`。

### 6.3 原子性检查

每条记录必须能单独回答：

- 它要求什么或保护什么？
- 在什么情况下适用？
- 如果删除它，会失去什么约束？
- 它是否能在不依赖相邻规则的情况下被归类？

不能回答时继续拆分或补充上下文。

## 7. 阶段三：归入四分类和十一项

### 7.1 主归属判断

根据规则“首次应该影响哪个研发决策”确定主要归属：

| 分类 | 项目 | 主要判断 |
| --- | --- | --- |
| 立项 | 选题 | 是否值得投入、优先级和取舍 |
| 立项 | 调研 | 如何理解问题、证据和不确定性 |
| 产品设计 | 定义 | 本轮交付什么、范围、规则和验收 |
| 产品设计 | 体验设计 | 用户如何完成任务以及如何感知结果 |
| 工程交付 | 技术设计 | 系统如何实现以及如何控制长期技术风险 |
| 工程交付 | 计划 | 如何拆分、排序、跟踪和恢复交付工作 |
| 工程交付 | 实现 | 如何产生代码、配置、迁移和技术产物 |
| 工程交付 | 验证 | 用什么证据证明产品和技术结果 |
| 工程交付 | 发布 | 如何安全进入真实环境并确认结果 |
| 运行维护 | 运行 | 如何持续服务、观测、支持和处理事件 |
| 运行维护 | 评估 | 如何判断效果并决定下一轮变化 |

### 7.2 归属规则

- 每条原子规则必须有且只有一个 `candidate_item` 作为主要归属；
- `secondary_impacts` 只用于建立引用；
- 规则本身含有多个独立决策时先拆分，再分别归属；
- 不根据原 W 编号直接映射；
- 不因为一个文件名包含 build、verify、release 或 operate 就整文件归入对应项目。

完成条件：不存在未归属规则，不存在同一原子规则的多个主要归属。

## 8. 阶段四：聚类、去重和冲突处理

### 8.1 按意图聚类

在每个项目内部，根据规则保护的共同目标形成规则簇，例如：

- 用户价值与优先级；
- 产品行为与范围；
- 架构边界与依赖方向；
- 数据完整性与生命周期；
- 契约兼容性；
- 安全、权限与信任；
- 验证证据；
- 发布风险和恢复；
- 运行可靠性；
- 反馈和效果判断。

聚类名称只是工作标签，不能直接当成原则。

### 8.2 处理状态

每条原子规则最终必须标记为以下之一：

- `rewrite`：保留意图并重新表达；
- `merge`：与其他规则合并为一条新规则；
- `split`：拆分到多个新规则；
- `supersede`：由更清楚或更新的规则替代；
- `retire`：确认无效、重复或无净收益；
- `conflict`：与其他规则冲突，需要用户决定。

`retire` 必须记录理由和失去它不会造成的风险。`conflict` 不能由 Codex 静默解决。

### 8.3 重写规则

重写后的规则必须：

- 保留原规则的有效约束；
- 清楚写明适用条件；
- 避免同时承担多个意图；
- 与所在项目的上下文一致；
- 不重复其他项目的权威规则；
- 不因追求简短而删除具体技术边界。

## 9. 阶段五：边组织边形成根本原则

### 9.1 项目原则

只有当一个项目内的规则簇已经稳定后，才能形成该项目的原则候选。

每条候选原则记录在 `review/principle-traceability.csv`：

```text
principle_id
level
category
item
statement
supporting_cluster_ids
supporting_rule_ids
decision_guidance
stability_check
conflicting_rule_ids
status
```

项目原则候选必须通过：

1. 更换框架、数据库或工具后仍然成立；
2. 能指导一个真实研发判断；
3. 不包含命令、目录、字段或具体执行步骤；
4. 不只是“保证质量”“重视安全”一类空泛口号；
5. 有明确的规则簇和原子规则支持；
6. 不与已接受规则冲突。

### 9.2 分类原则

分类原则只能在分类下所有项目原则形成后归纳。

它必须覆盖多个项目的共同长期约束，并记录支持它的项目原则 ID。不能从分类名称直接推导原则。

### 9.3 原则审查

每个分类和每个项目都必须有原则列表，但不预设数量。原则数量由实际规则簇决定；宁可少而有依据，也不能为满足格式制造原则。

## 10. 阶段六：编写新规范草稿

### 10.1 分类说明结构

四个分类的 `README.md` 使用统一结构：

```text
分类目的与边界
根本原则
包含的项目
项目之间的关系
进入条件
结束或循环条件
与其他分类的接口
```

### 10.2 项目规范结构

十一项规范使用统一结构：

```text
项目目的与边界
根本原则
核心判断
重新组织后的规范要求
按主题整理的执行细则
输入与产物
完成、停止或退出条件
相关项目引用
```

具体框架、数据库、前后端组织、AI runtime、工具、命令和文件结构进入“执行细则”或适用的规范要求，不进入根本原则。

### 10.3 草稿编写顺序

按以下顺序编写，避免上层原则过早锁定：

1. 十一项的规范要求和执行细则；
2. 十一项的项目原则；
3. 四个分类说明；
4. 四个分类原则；
5. 总入口和持续演进关系。

## 11. 阶段七：覆盖、冲突和质量审查

### 11.1 覆盖矩阵

`review/coverage-matrix.csv` 必须证明：

- 每个 W0–W9 文件都已完整 review；
- 每条原子规则都有处理状态；
- 每条保留规则都有新的目标规则；
- 每条原则都有支持它的规则；
- 每条退出规则都有理由；
- 没有未归属、未处理或来源不明的规则。

### 11.2 内容审查

检查以下问题：

- 是否把整段旧内容换个标题后继续保留；
- 是否遗漏技术栈、数据库、前端、后端、AI、安全、测试、发布或运行要求；
- 是否把执行细节错误提升为根本原则；
- 是否把原则写成没有决策意义的口号；
- 是否在多个项目重复同一规则；
- 是否静默解决了需要用户决定的冲突；
- 是否为了减少篇幅而损失约束；
- 是否仍然需要先理解 W0–W9 才能使用新草稿。

### 11.3 可用性审查

用代表性工作检查能否从四个分类进入正确项目，例如：

- 新产品是否进入立项；
- 新用户功能是否进入定义和体验设计；
- 架构或数据库变更是否进入技术设计；
- Bug 是否进入实现和验证，并在改变产品行为时返回定义；
- 生产发布是否进入发布；
- 事故是否进入运行；
- 用户反馈和指标结果是否进入评估并形成下一轮输入。

不设总行数通过门槛。记录默认阅读量、重复规则数量、未解决冲突和查找路径，作为用户判断精简是否有效的证据。

## 12. 用户审查门

完成草稿后，提交一份审查包：

1. 四分类和十一项草稿；
2. 十五份原则列表；
3. W0–W9 来源清单；
4. 来源分段账本；
5. 原子规则表；
6. 覆盖矩阵；
7. 原则追溯表；
8. 冲突清单；
9. 退出候选清单；
10. 旧结构与新结构的导航对照；
11. 默认阅读量和重复减少情况。

用户需要分别确认：

- 研发流程分类是否正确；
- 有效规则是否完整保留；
- 原则是否真实来自内容；
- 冲突如何处理；
- 哪些旧内容可以退出；
- 是否允许进入最终迁移设计。

任一项未确认，都不能开始最终迁移。

## 13. 完成条件

本内容重写阶段只有同时满足以下条件才算完成：

1. W0–W9 全部文件完成逐文件 review；
2. 来源分段账本覆盖所有非空白来源内容；
3. 所有规则性内容已拆成可追溯原子规则；
4. 所有原子规则已有且只有一个主要归属；
5. 所有规则都有明确处理状态；
6. 十一项草稿完整；
7. 四个分类说明完整；
8. 每项和每个分类的原则都可追溯到规则；
9. 具体技术决定和风险边界没有因为原则化而丢失；
10. 所有冲突均已披露；
11. 所有退出候选均有逐条理由；
12. 当前 W0–W9 未被删除、移动或覆盖；
13. 用户已审阅草稿包。

达到这些条件只代表“新规范草稿可供迁移决策”，不代表最终重建已经完成。

## 14. 执行体系方案选择

本次重建同时包含“约束工具建设”和“规范内容重写”两个可以独立验收的子系统。执行前比较三种方式：

| 方案 | 做法 | 优点 | 主要问题 | 结论 |
| --- | --- | --- | --- | --- |
| 纯文档约束 | 只靠本方案和提示词约束 Codex | 启动最快 | 无法稳定发现漏读、越界写入、重复归属和门禁跳过 | 不采用 |
| 单一 change | 在一个 OpenSpec change 中边造工具边重写内容 | 状态集中 | 未经验证的工具会直接约束真实内容，失败时难以区分工具问题和内容问题 | 不采用 |
| 双 change 工具化 | 先完成门禁工具，再启动内容重写 | 工具和内容可分别测试、审查、停止和恢复 | 多一个明确阶段 | 采用 |

采用以下顺序：

```text
设计获批
  ↓
OpenSpec A：build-rd-rewrite-guardrails
  ↓
工具通过测试、fixture 验证和用户审查
  ↓
冻结工具版本与 W0–W9 基线
  ↓
OpenSpec B：rewrite-rd-standards-content
  ↓
四批 review、重写、原则形成和覆盖审查
  ↓
用户审查
  ↓
只进入“可设计最终迁移”状态
```

工具建设和内容重写不能并行。内容重写阶段发现工具缺陷时，必须停止内容阶段，回到工具 change 修复并重新验收，不能现场修改工具后继续跑。

## 15. 执行约束的根本原则

本节原则约束的是“如何执行这次重建”，不是未来四分类和十一项中的研发根本原则。前者可以现在确定；后者仍然必须从 W0–W9 的规则组织中自下而上形成。

1. **人负责语义与问责，工具负责可判定事实。** 工具可以判断文件、字段、范围、状态和引用是否一致，不能判断一条研发原则是否正确，也不能代替用户批准冲突和退出。
2. **先定义政策，再执行自动化。** 所有允许写入的路径、状态转换、字段规则和人工批准点先进入机器可读政策；执行中不得临时放宽。
3. **默认保护来源。** W0–W9 以执行开始时的实际工作区内容为基线，不以 Git HEAD 代替；任何删除、移动或内容变化都阻断执行。
4. **工具本身先被验证。** 没有通过反例 fixture、单元测试和真实只读演练的工具，不能作为内容重写门禁。
5. **没有证据就不能推进状态。** “已经读过”“已经覆盖”“已经形成原则”等声明必须有可追溯记录支持。
6. **自动检查不得冒充语义审查。** 格式 PASS、OpenSpec validation 和脚本 PASS 只证明各自检查范围，不证明规范内容正确。
7. **不自动制造批准。** 工具只能报告 `REVIEW_REQUIRED`；冲突裁决、退出决定、原则接受和迁移许可只能来自用户的明确决定。
8. **一个事实只有一个权威状态。** OpenSpec `tasks.md` 记录 change 执行状态，机器运行状态记录在治理文件中，规则内容记录在草稿账本中；三者不能复制同一事实形成竞争入口。
9. **任何阶段都可安全停止和恢复。** 每个状态转换都保存输入摘要、工具版本、检查结果和下一步；失败不得通过删文件或重置工作区恢复。
10. **门禁复杂度必须有净收益。** 每个检查都要对应一种真实失败模式；只有产生噪声、不能改变决定的检查应删除或降级为提示。

## 16. Superpowers、OpenSpec、工具与人的分工

四者承担不同职责，不能互相替代：

| 机制 | 本次职责 | 不负责 |
| --- | --- | --- |
| 用户 | 确认目标结构、裁决语义冲突、批准原则和退出、决定是否进入迁移设计 | 逐文件机械检查和重复校验 |
| Codex | 完整读取、拆分规则、重写内容、提出原则候选、修复工具发现的问题 | 替用户批准高影响决定 |
| Superpowers | 在开始实现前完成设计和计划；执行时按小任务推进、自检并在完成前验证 | 保存 change 状态、定义研发内容或自动授予批准 |
| OpenSpec | 保存两次实现性 change 的 outcome、non-goals、acceptance、risks、rollback、tasks 和 next | 替代产品判断、W0–W9 来源、真实内容审查和工具测试 |
| `rd-rebuild` 工具 | 保护范围、验证账本、控制状态转换、生成覆盖与审查报告 | 自动归类、自动写原则、自动退出规则或自动迁移 |

Superpowers、OpenSpec、工具政策和本节执行原则都不是未来研发原则的内容来源。未来四分类和十一项的原则来源仍然只有完整 review 后形成的 W0–W9 规则簇。

Superpowers 的一般提交习惯不能扩大本方案授权。整个重建期间默认不 commit、不 push；只有用户单独明确授权时才执行 Git 写操作。

用户本人是 Codex 产物的最终人工审查者。Codex 的不同自检视角仍然只是生产者自检，不能写成独立审查。

## 17. OpenSpec 执行模型

两个子系统都属于 Standard：它们跨文件、跨会话、需要独立验收，但写入仅限本地工具、治理记录和并行草稿，且可以停止和回滚。最终迁移、删除旧规范或切换正式入口不包含在这个风险判断中，届时必须重新分流。

### 17.1 Change A：建设约束工具

固定 change id：

```text
build-rd-rewrite-guardrails
```

范围：

- 创建本方案规定的 CLI、内部模块、fixture 和单元测试；
- 创建机器可读政策、运行状态和审批记录结构；
- 用合成 fixture 验证通过、失败、越界、缺失、冲突和恢复路径；
- 对真实 W0–W9 只做只读 baseline 和 dry-run；
- 不创建真实原子规则，不重写规范内容。

完成门：工具测试通过、真实来源未变化、OpenSpec strict validation 通过、用户确认工具可以进入实际运行。

### 17.2 Change B：重写规范内容

固定 change id：

```text
rewrite-rd-standards-content
```

范围：

- 使用冻结后的工具版本执行本方案第 5–13 节；
- `tasks.md` 是内容重写执行进度的唯一权威来源；
- change 中只写本次重写增量、风险、验收、回滚和任务状态，并链接本方案和 `rebuild-draft/`；
- 不把全部原子规则或草稿正文复制进 OpenSpec。

完成门：审查包形成、工具门禁全部通过、OpenSpec strict validation 通过、用户完成审查。完成后仍然不 archive、不迁移，除非用户另行批准。

### 17.3 OpenSpec 使用命令

Change A 和 Change B 分别在其阶段开始时创建：

```powershell
openspec new change build-rd-rewrite-guardrails
openspec new change rewrite-rd-standards-content
```

每次进入实现前和每个阶段结束后，按当前 change 运行对应命令：

```powershell
openspec validate build-rd-rewrite-guardrails --strict --no-interactive
openspec status --change build-rd-rewrite-guardrails

openspec validate rewrite-rd-standards-content --strict --no-interactive
openspec status --change rewrite-rd-standards-content
```

`openspec archive` 不属于本方案自动步骤。即使任务全部完成，也必须等用户审查和单独授权。

## 18. 约束工具设计

### 18.1 文件结构

工具阶段计划创建：

```text
tools/
  rd_rebuild.py
  rd_rebuild_core/
    __init__.py
    model.py
    baseline.py
    scope.py
    records.py
    coverage.py
    principles.py
    drafts.py
    gates.py
    report.py
  fixtures/rd_rebuild/
    valid/
    source_changed/
    line_gap/
    duplicate_owner/
    unsupported_principle/
    unauthorized_write/
  test_rd_rebuild_baseline.py
  test_rd_rebuild_records.py
  test_rd_rebuild_gates.py
  test_rd_rebuild_report.py

governance/
  project-map.json
  current-status.json
  rd-standards-rebuild/
    policy.json
    run-state.json
    baseline-manifest.json
    tool-manifest.json
    approvals.jsonl
    reports/
```

`rebuild-draft/review/` 保存内容语义账本；`governance/rd-standards-rebuild/` 保存工具政策、运行状态和机器证据。治理域必须登记进 `governance/project-map.json`。

工具只使用 Python 标准库，避免为一次重建引入运行时依赖。入口沿用当前仓库 `argparse`、明确退出码和 `unittest` fixture 的风格。

### 18.2 写入范围政策

`policy.json` 至少声明：

```text
schema_version
plan_path
source_roots
protected_roots
allowed_write_roots_by_phase
required_files_by_gate
allowed_enums
principle_review_patterns
copy_detection_thresholds
approval_gates
tool_manifest_sha256
```

Change A 允许写入的范围只包括工具、测试、该 change 和治理域。Change B 允许写入的范围只包括 `rebuild-draft/`、Change B 和治理运行报告；冻结后的工具文件不得修改。

现有工作区可能已经有未提交修改，因此范围校验不能简单要求 `git status` 为空。baseline 必须记录执行开始时实际存在的文件、SHA-256 和状态；后续只比较增量，既保护用户已有修改，也阻止本次执行悄悄扩大写入范围。

### 18.3 CLI 合同

计划实现一个入口：

```powershell
python tools/rd_rebuild.py <command> --root .
```

子命令及职责：

| 子命令 | 作用 | 能否修改语义内容 |
| --- | --- | --- |
| `baseline-create` | 记录来源、现有工作区状态和工具版本摘要 | 否 |
| `baseline-verify` | 检查 W0–W9 是否被删除、移动或修改 | 否 |
| `scope-check` | 检查本阶段新增写入是否只在允许路径 | 否 |
| `inventory-check` | 检查 W0–W9 文件清单、唯一性和 review 状态 | 否 |
| `segment-check` | 检查非空白来源行是否被分段账本连续覆盖 | 否 |
| `rule-check` | 检查原子规则字段、行号、枚举、来源和处理状态 | 否 |
| `classification-check` | 检查每条规则只有一个主要归属及引用是否合法 | 否 |
| `rewrite-check` | 检查保留规则的目标映射、正文重复和退出理由 | 否 |
| `principle-check` | 检查原则追溯、分类覆盖和具体工具词风险 | 否 |
| `draft-check` | 检查四分类、十一项、必需章节和权威规则引用 | 否 |
| `gate` | 聚合当前阶段所需检查并决定能否转换状态 | 只更新运行状态 |
| `report-build` | 生成覆盖、冲突、退出和审查摘要 | 只写报告 |
| `verify-all` | 重跑所有已适用检查 | 否 |
| `status` | 显示当前状态、阻塞项、证据和下一动作 | 否 |

工具不得提供 `auto-classify`、`auto-principles`、`auto-retire`、`approve`、`migrate` 或 `delete` 子命令。

`baseline-create`、`gate` 和 `report-build` 必须支持 `--dry-run`。dry-run 只显示计划读取、计划写入和预计状态变化，不写文件，也不能生成可供后续 gate 使用的通过证据。

### 18.4 检查结果和退出码

所有命令输出统一状态：

- `PASS`：结构检查通过；
- `WARN`：不阻断，但必须进入审查报告；
- `REVIEW_REQUIRED`：需要用户语义决定，不能推进 gate；
- `BLOCKED`：确定性规则失败，不能推进 gate；
- `TOOL_ERROR`：工具自身异常，停止当前阶段。

退出码固定为：

```text
0 = PASS 或仅有 WARN
1 = BLOCKED
2 = REVIEW_REQUIRED
3 = TOOL_ERROR
```

工具不得捕获异常后仍返回 0，也不得把跳过项统计为 PASS。

### 18.5 硬检查与人工检查边界

以下问题可以硬阻断：

- 来源文件缺失、哈希变化或未登记新增文件；
- 来源分段存在空洞、越界或重叠；
- 原子规则缺字段、行号无效、ID 重复或来源不存在；
- 一条规则有多个主要归属或没有主要归属；
- `rewrite`、`merge`、`split`、`supersede` 没有目标规则；
- `retire` 没有逐条理由；
- 原则没有支持规则，或分类原则没有覆盖多个项目；
- 四分类、十一项或必需章节缺失；
- 当前阶段出现未授权写入；
- 试图跳过前置 gate。

以下问题只能产生 `REVIEW_REQUIRED` 或 `WARN`：

- 两条规则是否真的同义；
- 一项规则最适合归入哪个项目；
- 冲突应保留哪一方；
- 原则是否足够根本、稳定且有决策价值；
- 技术细节是否仍然有效；
- 退出一条规则是否可接受；
- 草稿是否真的更清晰、精简和可用。

复制检测只作为防误搬运门禁：规范化后长度不少于 40 个字符的原文被完整复制进草稿时 `BLOCKED`；高相似但非完全相同的段落产生 `REVIEW_REQUIRED`。技术名称、不可改写的标准术语、短语和代码片段不单独触发复制阻断。

原则中的数据库、框架、命令、目录和工具词由政策中的模式表检测，默认产生 `REVIEW_REQUIRED`，不能仅凭关键词自动删除原则。

## 19. 状态机与人工批准门

`run-state.json` 只允许以下顺序状态：

```text
planned
  → tooling_ready
  → sources_frozen
  → sources_reviewed
  → rules_classified
  → rules_rewritten
  → principles_derived
  → audit_ready
  → awaiting_user_review
  → approved_for_migration_design
```

不存在 `migrated`、`completed_rebuild` 或 `old_content_deleted` 状态，因为这些动作不在本方案范围内。

| Gate | 进入状态 | 必须满足 |
| --- | --- | --- |
| G0 | `planned` | 用户批准本方案并明确开始执行 |
| G1 | `tooling_ready` | Change A 工具测试、fixture、dry-run、strict validation 和用户审查通过 |
| G2 | `sources_frozen` | 工具版本与 W0–W9 实际基线已记录，允许写入范围已锁定 |
| G3 | `sources_reviewed` | 四批来源均有清单、连续分段和原子规则；无漏读 |
| G4 | `rules_classified` | 全部规则有唯一主要归属；冲突已披露并获得所需决定 |
| G5 | `rules_rewritten` | 所有处理状态完整；保留规则有目标；退出有理由；无直接搬运 |
| G6 | `principles_derived` | 十一项和四分类原则均有追溯；人工确认语义成立 |
| G7 | `audit_ready` | 草稿、覆盖矩阵、冲突、退出和审查报告齐全 |
| G8 | `awaiting_user_review` | 完整审查包和全套检查结果已经生成；停止写入并等待用户 |
| G9 | `approved_for_migration_design` | 用户完成逐项审查，并明确批准只进入最终迁移方案设计 |

`approvals.jsonl` 只记录已经发生的人工决定，至少包含：

```text
approval_id
gate
decision
decided_by
decided_at
scope_sha256
decision_source
notes
```

Codex 可以在等待时生成 `pending` 请求，但不能自行把它改成 `approved`。只有用户在任务中明确表达决定后，Codex 才能按原意记录批准；记录本身是追溯信息，不是假装能够密码学证明用户身份。

## 20. 具体执行方案

### 20.1 阶段 A：建设并验证工具

1. 用户确认本增强方案后，创建 `build-rd-rewrite-guardrails`。
2. 在 proposal/spec/design 中锁定本节 CLI 合同、允许写入范围、退出码、fixture 和验收条件。
3. 先为 baseline 与 scope 写失败测试，再实现最小功能。
4. 先为来源分段、原子规则、归类和原则追溯的错误样例写失败测试，再实现检查器。
5. 先为非法状态跳转、缺少批准和工具异常写失败测试，再实现 gate。
6. 实现报告生成器；报告只聚合已有事实，不生成语义结论。
7. 对全部合成 fixture 运行测试。
8. 对真实 W0–W9 运行只读 dry-run，确认不会写入来源。
9. 运行仓库既有验证和 OpenSpec strict validation。
10. 交付工具设计、命令、测试证据和剩余限制给用户审查，然后停止。

工具阶段最低验证命令：

```powershell
python -m unittest discover -s tools -p "test_rd_rebuild_*.py" -v
python tools/rd_rebuild.py baseline-create --root . --dry-run
python tools/rd_rebuild.py scope-check --root . --phase tooling
python tools/verify_rd_standards.py .
python tools/verify_workflow_index.py .
openspec validate build-rd-rewrite-guardrails --strict --no-interactive
openspec status --change build-rd-rewrite-guardrails
```

在工具尚未实现前，上述 `rd_rebuild.py` 命令只是接口契约，不能伪造运行结果。

### 20.2 阶段 B：启动内容重写

只有 G1 获批后执行：

1. 创建 `rewrite-rd-standards-content`，链接本方案和已验收工具证据。
2. 创建真实 baseline，冻结工具 manifest、W0–W9 文件哈希和工作区已有状态。
3. 运行 `python tools/rd_rebuild.py gate --root . --target sources_frozen` 完成 G2，确认来源保护与写入范围。
4. 创建 `rebuild-draft/` 的空结构和机器可读账本表头。
5. 严格按 W0–W2、W3–W4、W5–W6、W7–W9 四批执行完整读取。
6. 每批只允许新增来源清单、分段和原子规则；每批结束运行 baseline、scope、inventory、segment 和 rule 检查。
7. 四批全部通过后运行 `python tools/rd_rebuild.py gate --root . --target sources_reviewed` 完成 G3；未通过时不能开始全局归类。
8. 执行十一项主归属、规则簇、去重和冲突识别；运行 classification 检查。
9. 将需要人决定的归属和冲突一次性形成审查包；用户决定后才运行 `python tools/rd_rebuild.py gate --root . --target rules_classified` 完成 G4。
10. 逐项重写规范要求和执行细则，填充处理状态和目标映射；运行 rewrite 检查。
11. 处理复制、高相似、丢失技术边界和退出理由问题；运行 `python tools/rd_rebuild.py gate --root . --target rules_rewritten` 完成 G5。
12. 从稳定规则簇形成十一项原则，再形成四分类原则；运行 principle 检查并由用户审查语义。
13. 编写分类说明、总入口和持续演进关系；运行 draft 检查，再运行 `python tools/rd_rebuild.py gate --root . --target principles_derived` 完成 G6。
14. 生成覆盖矩阵、冲突清单、退出候选和审查报告；运行 `python tools/rd_rebuild.py gate --root . --target audit_ready` 完成 G7。
15. 重跑全套验证，运行 `python tools/rd_rebuild.py gate --root . --target awaiting_user_review` 完成 G8，然后停止所有写入。
16. 用户审查后，最多运行 `python tools/rd_rebuild.py gate --root . --target approved_for_migration_design` 完成 G9；不执行最终迁移。

每个内容批次结束运行。`--batch` 依次使用 `w0-w2`、`w3-w4`、`w5-w6`、`w7-w9`；例如第一批运行：

```powershell
python tools/rd_rebuild.py baseline-verify --root .
python tools/rd_rebuild.py scope-check --root . --phase content
python tools/rd_rebuild.py inventory-check --root .
python tools/rd_rebuild.py segment-check --root . --batch w0-w2
python tools/rd_rebuild.py rule-check --root . --batch w0-w2
openspec validate rewrite-rd-standards-content --strict --no-interactive
```

全局归类后运行：

```powershell
python tools/rd_rebuild.py classification-check --root .
python tools/rd_rebuild.py rewrite-check --root .
python tools/rd_rebuild.py principle-check --root .
python tools/rd_rebuild.py draft-check --root .
python tools/rd_rebuild.py report-build --root .
python tools/rd_rebuild.py verify-all --root .
openspec validate rewrite-rd-standards-content --strict --no-interactive
openspec status --change rewrite-rd-standards-content
```

## 21. 工具如何约束 Codex 的行为

每个实际写入任务必须遵循同一协议：

```text
读取 OpenSpec tasks.md 当前任务
  ↓
运行 status 和当前 gate
  ↓
运行 baseline-verify 与 scope-check
  ↓
只修改任务声明的允许文件
  ↓
运行该任务对应的专用检查
  ↓
再次运行 baseline-verify 与 scope-check
  ↓
把命令、退出码和报告路径写回 tasks.md
  ↓
只有 gate 通过才进入下一任务
```

具体约束：

- Codex 在任何工具返回非零时必须停止状态推进，先报告问题；
- 不得通过修改 fixture、policy、baseline 或 tool manifest 让失败检查变绿；
- 内容阶段不得修改工具代码；
- 不得手工把 `run-state.json` 改到更后状态；状态只由 `gate` 在检查通过后更新；
- 不得把 WARN、跳过或未运行写成 PASS；
- 不得在一个批次未完成时提前编写最终原则；
- 不得把用户没有决定的冲突标记为 `supersede` 或 `retire`；
- 不得以 OpenSpec validation 通过代替来源覆盖、内容验证或用户审查；
- 每次恢复任务先运行 `status`、baseline 和 scope，不依赖对话记忆猜测进度；
- 如果工具结果与人工观察矛盾，以停止和调查为默认动作，不能绕过门禁。

## 22. 工具自身的验收标准

工具进入 G1 前必须证明：

1. 有效 fixture 全部通过；
2. 每类硬阻断至少有一个会失败的反例测试；
3. 非授权写入、来源变化、行覆盖空洞、重复主归属、无支持原则和非法 gate 跳转都能稳定失败；
4. `REVIEW_REQUIRED` 与 `BLOCKED` 的退出码不同；
5. 同一输入重复运行得到同一结果；
6. 中途中止后 `status` 能准确给出最后通过 gate、阻塞项和下一步；
7. baseline 能保护执行开始时已经存在的未提交修改；
8. 工具异常不会留下更高的虚假状态；
9. dry-run 不改动 W0–W9、草稿和治理状态；
10. 报告中的每个数字能回到原始记录；
11. 工具自身文件被修改后，内容阶段会因 manifest 不一致而停止；
12. 用户能够仅根据 `status` 和审查报告判断当前真实进度。

工具不需要证明它能理解研发规范语义。语义理解仍由 Codex 产出、用户审查，并由来源追溯支持。

## 23. 失败、停止与恢复

出现以下任一情况立即停止当前阶段：

- W0–W9 baseline 变化；
- 发生未授权路径写入；
- 工具 manifest 变化；
- OpenSpec strict validation 失败；
- gate 前置状态缺失；
- 来源账本存在未覆盖内容；
- 存在未裁决冲突却准备继续重写；
- 工具自身报错或结果不可复现；
- 用户要求暂停或改变方向。

停止时只允许：

1. 保存当前已证实状态和失败报告；
2. 标记 OpenSpec `tasks.md` 当前项为 blocked 或 stopped；
3. 报告最后可信 gate、受影响范围和恢复前置条件；
4. 等待用户决定。

禁止通过删除工作、重置 Git、重建 baseline、放宽 policy、跳过检查或静默改状态恢复。

恢复时先确认 OpenSpec change、工具 manifest、baseline、run-state 和实际文件相互一致；不一致时先调查，不继续内容工作。

## 24. 执行启动提示

后续新任务可以使用以下提示启动本方案：

```text
严格执行 docs/superpowers/specs/2026-07-15-rd-standards-content-rewrite-plan.md。

先读取方案并确认当前 gate。若约束工具尚未建设和验收，只执行 OpenSpec change `build-rd-rewrite-guardrails`，不要开始 W0–W9 内容重写。

工具通过用户审查后，再创建或继续 `rewrite-rd-standards-content`，按照 baseline、四批完整 review、原子规则拆分、十一项归类、规则重写、原则归纳、并行草稿和覆盖审查的顺序执行。

不要使用 docs/superpowers/specs/2026-07-15-rd-standards-rebuild-design.md；它已被新方案取代。
不要删除、移动或覆盖现有规范，不要修改正式入口，不要执行最终迁移，不要提交或推送。

执行任何写入前后运行当前阶段要求的 baseline、scope 和专用检查。工具非零退出时停止，不绕过、不放宽 policy、不重建 baseline。

研发原则必须在规则组织过程中形成，不能预写。最终交付四分类/十一项草稿、来源分段账本、原子规则覆盖矩阵、原则追溯表、冲突清单和退出候选清单，然后进入 `awaiting_user_review` 并停止，等待用户审查。
```
