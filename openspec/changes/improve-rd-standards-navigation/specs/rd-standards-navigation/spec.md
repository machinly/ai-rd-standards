# rd-standards-navigation 的变更规格

## ADDED Requirements

### Requirement: 根入口必须指向 AI 研发工作流而不是平铺全部规范

研发规范仓库的 README MUST 作为短入口，指向 AI 研发工作流入口、workflow-to-standard 索引、上下文包、来源索引和常用验证命令，而不是展开全部阶段清单。

#### Scenario: 打开仓库根入口

- GIVEN 用户打开 `README.md`
- WHEN 用户需要决定下一步读什么
- THEN README 指向 `docs/00-start-here.md`
- AND README 说明先定位当前 W0-W9 workflow step
- AND README 不要求用户通读所有阶段

### Requirement: 工作流入口必须覆盖从想法到维护的 AI 研发生命周期

工作流入口 MUST 定义 W0-W9，并覆盖 intake、discovery、OpenSpec/risk、AI behavior、build、verify、release、operate、learn、maintain。

#### Scenario: 定位当前 AI 研发步骤

- GIVEN 用户有一个研发请求、AI 行为变更、事故、客户反馈或文档维护任务
- WHEN 查看 `docs/00-start-here.md`
- THEN 文档帮助用户定位 W0-W9 中的当前步骤
- AND 每个步骤列出问题、只读规范、最小产出和人审点

### Requirement: 完整索引必须把所有规范挂到 workflow step

完整索引 MUST 保留所有阶段入口，但必须以 W0-W9 为主组织方式，并为每个阶段给出主归属 workflow step。

#### Scenario: 查找阶段规范

- GIVEN 用户需要查找某个阶段规范
- WHEN 查看 `docs/00-standard-index.md`
- THEN 文档显示该阶段的主归属 workflow step
- AND 文档显示该 workflow step 的主规范、触发专项、人审点和常用 skill

### Requirement: Workflow 规范文件必须按 workflow step 目录存放

每个 workflow step 目录 MUST 有且只有一个 `main.md` 作为核心入口。触发型专项 MUST 使用语义化文件名，且不得以数字开头。目录中的 W step MUST 等于该规范在索引中的主归属。

#### Scenario: 查看规范文件物理结构

- GIVEN 仓库包含编号规范文件
- WHEN 查看 `docs/` 目录
- THEN `01` 到 `55` 等编号规范不直接平铺在 `docs/` 根目录
- AND 每个编号规范位于对应的 `docs/Wx-*` 目录
- AND `docs/00-start-here.md` 与 `docs/00-standard-index.md` 保留为入口文件

### Requirement: 新增规范必须声明 workflow 归属

任何新增规范 MUST 说明它服务 W0-W9 哪一步、补哪个缺口、最小 artifact 是什么，以及如何由 skill 或 verifier 承接。

#### Scenario: 准备新增规范

- GIVEN Codex 或用户想添加新规范
- WHEN 更新索引或 OpenSpec proposal
- THEN 变更说明该规范的主 workflow step
- AND 说明它不是另起一摊的主题清单

### Requirement: Workflow 索引必须可自动校验

导航层 MUST 提供本地校验命令，检查 README 短入口、W0-W9 完整性、规范到 workflow step 的唯一映射、物理目录归属和索引路径存在性。

#### Scenario: 新增或重命名规范后校验索引

- GIVEN 新增、删除或重命名 `docs/Wx-*/*.md` 规范文件
- WHEN 运行 `python tools\verify_workflow_index.py .`
- THEN 每个规范恰好映射到一个 W0-W9 step，并且每个 W 只有一个 `main.md`
- AND 每个编号规范位于对应 W0-W9 目录
- AND 索引引用的规范路径存在
- AND README 未退化为平铺阶段清单

### Requirement: 核心 R&D skill 必须先路由 workflow step

`one-person-openspec-rd` MUST 在创建 OpenSpec 或实现前先判断请求处于 W0-W9 哪一步，并只读取当前 step、上一步输入和下一步门禁对应的规范。

#### Scenario: 使用核心 skill 开始研发请求

- GIVEN 用户请求规划、实现、验证、发布、运维、学习或维护 AI 产品研发工作
- WHEN 使用 `one-person-openspec-rd`
- THEN skill 先说明当前 W0-W9 workflow step
- AND skill 根据 step 决定是否创建 planning、product discovery、OpenSpec、AI eval、build、release、ops、learning 或 knowledge artifacts
- AND skill 只升级高影响人工判断

### Requirement: 导航层必须具备知识恢复工件

导航层 MUST 具备 docs map、context pack、glossary、how-to 和 freshness log，使 Codex 和人可以按工作流恢复上下文。

#### Scenario: Codex 接手规范仓库

- GIVEN Codex 需要继续整理或使用研发规范
- WHEN 读取 `knowledge/docs-map/rd-standards.json`
- THEN docs map 指向 README、工作流入口、workflow-to-standard 索引和 context pack
- AND context pack 要求先定位 W0-W9

### Requirement: 导航层必须避免制造新的注意力负担

导航层 MUST 将完整清单作为 reference，把第一入口保持为 workflow step 选择，并明确哪些决策需要人工判断。

#### Scenario: 用户只想开始当前工作

- GIVEN 用户打开仓库准备开始一个具体任务
- WHEN 阅读 README 和 `docs/00-start-here.md`
- THEN 用户能在不通读完整索引的情况下定位当前 workflow step
- AND 高影响人工判断被集中列出
