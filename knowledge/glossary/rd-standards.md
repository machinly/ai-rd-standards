# rd-standards Glossary

## Domain Terms

- R&D applicability：在读取研发正文前判断任务主要结果是否改变、验证、发布、运行或直接决定产品/工程系统；不适用时直接使用任务自身流程。
- Explore：关键未知仍主导、目标是用可证伪证据学习的研发工作模式；合法 outcome 为 `validated | invalidated | revise | stopped | promote`。
- Product Discovery：围绕已识别产品/工程决定中的用户、问题、价值、范围或成功标准未知开展的 Explore 类型。
- UX Prototype：比较关键任务流程、信息架构、交互或可理解性的 Explore 类型；可以是静态或可运行工件。
- Technical Spike：降低架构、集成、契约或技术可行性未知的 Explore 类型。
- Deliver：行为已经足够明确、目标是形成稳定可维护增量的研发工作模式；其子路由为 Quick、Standard、High-risk。
- Quick：Deliver 中低风险、局部、可逆、无需持久治理工件的路径。
- Standard：Deliver 中默认使用一个 OpenSpec change，并需要验证证据和独立审查的路径。
- High-risk：Deliver 中在真实副作用前需要明确人类批准、风险和回滚记录的路径。
- Prototype：Explore 中用于学习的 artifact，不是 Quick/Standard/High-risk 的同级 route。
- Walking Skeleton：从实际产品入口贯通必要组件并形成一个可见业务结果的 tactic，不是 route。
- Superpowers complexity gate：只有具体复杂问题命中时才选择最小直接相关 skill 集的门；会话开始、AI 参与、创作性、时长和文件数不能单独触发。
- Work brief：仅用于没有其他权威记录的非实现性例外；不得与 Explore record 或 active OpenSpec change 重复维护同一事实。
- Playbook：只在命中具体问题时读取的可选指导，不是默认规则。
- Independent reviewer：未参与产出、基于目标和证据做最终审查的人或独立执行上下文。
- Human decision owner：对高影响决定有真实权限并承担责任的人。
- 分类原则：三级研发规范的第一层，只表达一个分类跨项目稳定成立的根本约束。
- 项目原则：三级研发规范的第二层，只表达一个项目稳定成立的根本约束。
- 执行细节总索引：`docs/execution-details.md`，是第三级主题文件的唯一总导航；它负责说明什么类型的细节位于哪个文件，不复制规则正文。

## Bounded Context Language

- W0-W9：历史来源的十个主题/生命周期标签；当前只存在于治理账本和 archive 追溯中，不是 live navigation 或可选操作入口。
- OpenSpec change：Deliver Standard/High-risk 实现性变更的默认规格与状态工件；轻量 Explore 和 Deliver Quick 默认不创建。
- Role lens：产品、工程、QA、运维或安全视角；不等于必须创建一个 Agent 岗位。
- Multi-Agent orchestration：尚未产品化的实验性协作方式。
- Canonical entrypoint：默认读取并决定当前行为的文件。
- Context pack：给人和 Codex 的短恢复入口。

## API Names

当前仓库没有运行时 API。未来若增加管理服务，API 名称必须来自真实产品对象，不从 W 编号或 Agent 角色派生。

## Data Names

- knowledge/docs-map/<target>.json：机器可读入口地图。
- knowledge/context-packs/<target>.md：上下文恢复摘要。
- knowledge/freshness/<target>.jsonl：结构变更和复审记录。
- docs/sources/evidence-registry.jsonl：关键声明与证据等级。
- experiments/<experiment>.md：真实任务对照试验。

## AI Terms

- Skill：可复用的 AI 工作说明，不自动获得权限。
- Eval：版本化的代表、边界和失败样例。
- Format valid：文件、schema 或语法有效。
- Governance complete：入口、审批、review 和生命周期相互一致。
- Pilot verified：真实任务数据支持流程净收益。
- Primary research：原始论文、数据或标准。
- First-party experience：厂商或项目自身的工程经验。
- Case study：有限实例研究。
- Secondary analysis：二手总结。
- Anecdote：未经独立验证的事件或观点。

## Avoided Terms

- 不把“虚拟公司操作系统”描述为当前已实现能力。
- 不把 W0-W9 描述为所有任务的自然或唯一流程。
- 不把 Quick/Standard/High-risk 描述为所有任务或全部研发的第一层路由。
- 不把 Prototype 或 Walking Skeleton 描述为路径。
- 不把一次 Superpowers 调用解释为后续 skills 的自动授权。
- 不把两个自检视角描述为两次独立 review。
- 不把格式 PASS 描述为行为已验证。
- 不把人的角色缩减为目标输入和异常审批。
- 不用“角色 Agent”暗示真实岗位、权限或独立性。
