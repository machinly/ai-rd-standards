# agent-operating-model 规格

## ADDED Requirements

### Requirement: 规范体系必须有与技术栈无关的操作模型抽象层

规范体系 MUST 提供一份操作模型文档，只描述系统模型、第一性原则和自主性等级，不包含具体语言、框架、供应商或产品的实现细节。该文档 MUST 位于 W0-W9 工作流之上，并说明各层的稳定度与变更频率差异。

#### Scenario: 新 Agent 或新人理解体系

- GIVEN 一个从未接触本仓库的 Agent 或人
- WHEN 阅读 `docs/04-operating-model.md`
- THEN 能在不读任何 W0-W9 细节的情况下说出系统的五个平面、核心原则和当前自主性等级
- AND 文档中不出现绑定具体技术栈的强制条文

### Requirement: 多 Agent 协作必须遵循显式任务契约

总控 Agent 派发给工人 Agent 的每个任务 MUST 包含目标、输出契约、上下文来源指引和边界四要素，且 MUST 附带机器可判定的完成判据或明确声明该任务需要人工验收。缺少完成判据的任务 MUST NOT 进入无人值守执行通道。

#### Scenario: 派发一个实现任务

- GIVEN 一个 OpenSpec change 已拆出可并行的实现批次
- WHEN 总控 Agent 派发某个批次给工人 Agent
- THEN 任务契约中包含目标、输出契约、上下文引用（指向 spec 原文而非转述摘要）和不做什么
- AND 包含验证命令或验收标准
- AND 包含预算与停止条件

### Requirement: 并发执行必须遵守读写分离纪律

编排规范 MUST 规定：读类任务（检索、研究、审查）允许并行扇出；写类任务（代码、配置、文档的修改）在同一文件域内同一时刻 MUST 只有一个执行者。构建、测试等重资源操作 MUST 串行化或限流。

#### Scenario: 两个批次涉及同一模块

- GIVEN 两个实现批次都要修改同一目录下的文件
- WHEN 总控 Agent 调度
- THEN 两个批次被串行执行，或重新切分为互不相交的文件域
- AND 不允许两个工人 Agent 同时写同一文件域

### Requirement: 执行循环必须有防停滞与升级机制

总控 Agent MUST 维护任务账本与进度账本，每轮检查是否完成、是否循环、是否前进；停滞计数 MUST 有上限，超限触发重规划或升级。工人 Agent 的自纠错循环 MUST 有迭代上限，超限后 MUST 升级而不是继续重试。升级 MUST 按阶梯进行：调整方式重试、更换模型或分解方式、挂起进入升级队列等待人工。

#### Scenario: 工人 Agent 反复修不过测试

- GIVEN 一个批次的验证连续多次失败且无新进展
- WHEN 达到迭代上限
- THEN 工人 Agent 停止重试，产出失败报告（已尝试路径、失败证据、建议）
- AND 总控 Agent 按升级阶梯处理，最终可挂起该任务进入人工升级队列
- AND 其他不依赖该任务的工作继续推进

### Requirement: 生产与不可逆副作用在无人值守时必须默认拒绝

生产发布、生产数据迁移、生产配置变更、真实付款、对外通信、生产数据删除、合同承诺等生产、不可逆或对外动作 MUST 经过确定性策略门检查。无人值守运行时这些动作 MUST 默认拒绝并进入升级队列；当前规范 MUST NOT 把 A3/A4 解释为生产自动发布授权。权限判定 MUST NOT 因 Agent 之间的转述而放宽。

#### Scenario: 无人值守夜间运行遇到发布动作

- GIVEN 系统在无人值守窗口运行
- WHEN 某任务到达"发布到生产"步骤
- THEN 策略门拒绝生产执行，只允许保留发布候选、预检与回滚证据，并把该任务挂入升级队列
- AND 系统继续处理其他任务，不阻塞、不硬闯、不重试绕过

### Requirement: 自主性必须按等级渐进放权

规范 MUST 定义自主性等级，并把放权条件绑定到可度量证据（验证覆盖、历史通过率、失败率）而不是主观判断。默认等级 MUST 保留人审门禁；提升等级 MUST 是显式的人工决策。

#### Scenario: 提升某类任务的自主等级

- GIVEN 某类任务在过去若干次运行中验证通过率达到规定阈值
- WHEN 用户决定放权
- THEN 该类任务的自主等级提升被记录（等级、依据、日期）
- AND 出现质量回归时等级可以降回并留下记录

### Requirement: W0-W9 主入口必须逐阶段承接操作模型和编排协议

每个 W0-W9 主入口 MUST 明确说明本阶段如何执行 L0 操作模型、L1 多 Agent 编排协议和小型项目管理原则。该说明 MUST 是阶段特定的执行条款，而不是复制 `docs/04-operating-model.md` 或 `docs/05-agent-orchestration.md` 的长原则。任何跨会话、多 Agent 或无人窗口的工作 MUST 能从当前 W 主入口找到下一步应进入的契约、账本、验证或升级路径。

#### Scenario: 下一个 Codex 从某个 W 主入口接手

- GIVEN 一个 Codex 只读取当前 W 的 `00-main.md`
- WHEN 它需要判断本阶段如何处理操作模型、Agent 编排和小型项目管理
- THEN 该文件说明本阶段应写入哪些目标、边界、验收、证据、责任或维护工件
- AND 指向需要回到 L0/L1、OpenSpec、验证门禁或人审升级的条件
- AND 不要求把 L0/L1 全文复制到该 W 文件

### Requirement: W0-W9 触发专项必须逐文件承接操作模型和编排协议

每个 W0-W9 目录下除 `00-main.md` 外的触发专项 MUST 明确说明本专项如何执行 L0 操作模型、L1 多 Agent 编排协议、小型项目管理原则和 T2/T3 安全口径。该说明 MUST 是专项特定的执行条款，覆盖本专项的工件如何成为任务契约、验收证据、写域边界、DoD、升级队列、失败分类账、发布/运行收尾或 handoff 中适用的一项。

#### Scenario: 下一个 Codex 命中某个触发专项

- GIVEN 一个 Codex 已通过当前 W 主入口命中某个 `docs/W*/0N-*.md` 触发专项
- WHEN 它读取该专项准备拆任务或执行
- THEN 该文件说明本专项哪些活动可以只读并行，哪些写入或决策必须串行
- AND 说明哪些生产、不可逆、对外、凭据、真实客户数据或高影响 AI 动作必须升级人审
- AND 不要求把 `docs/04-operating-model.md` 或 `docs/05-agent-orchestration.md` 的长原则复制进专项正文

### Requirement: 小型项目管理资料必须被正式吸收而非孤立引用

规范 MUST 把小型项目管理资料转译进 W0-W9 的阶段行为和触发专项：W0/W1 覆盖项目取舍、范围控制、成功标准和 non-goals；W2 覆盖风险、边界和计划粒度；W4/W5 覆盖小批量交付、验证闭环和返工控制；W6/W7 覆盖发布、运维和责任边界；W8/W9 覆盖复盘、知识回写和维护节奏；各专项覆盖其具体工件如何服务交付物、验收、暂停恢复和 closeout。source map MUST 记录 `docs/sources/2026-07-08-small-project-management-operating-guide.md` 与这些规范条款的关系。

#### Scenario: 小型项目资料被用于一次研发 change

- GIVEN 一个超过半天、跨多个 W 或暂停后需要恢复上下文的研发工作
- WHEN 它按 W0-W9 推进
- THEN W0/W1 要求写清 goal、deliverables、acceptance criteria、non-goals、appetite 和停止条件
- AND W2 把交付物视图与 OpenSpec tasks 区分开
- AND W4-W9 分别留下批次证据、验证结论、发布/运行责任、学习结论和维护 handoff
