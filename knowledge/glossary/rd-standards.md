# rd-standards Glossary

## Domain Terms

- Minimal kernel：默认加载的不超过 15 条硬规则。
- Quick：低风险、可逆、无需持久治理工件的路径。
- Standard：默认使用一个 OpenSpec change，并需要验证证据和独立审查的路径。
- High-risk：副作用前需要明确人类批准、风险和回滚记录的路径。
- Work brief：仅用于非实现性记录或经用户批准跳过 OpenSpec 的例外；不得与 active change 重复维护同一事实。
- Playbook：只在命中具体问题时读取的可选指导，不是默认规则。
- Independent reviewer：未参与产出、基于目标和证据做最终审查的人或独立执行上下文。
- Human decision owner：对高影响决定有真实权限并承担责任的人。

## Bounded Context Language

- W0-W9：历史形成的十个主题/生命周期坐标；当前仅用于检索旧 playbook。
- OpenSpec change：Standard/High-risk 实现性变更的默认规格与状态工件；由风险路径触发，不由任务时长单独触发。
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
- 不把两个自检视角描述为两次独立 review。
- 不把格式 PASS 描述为行为已验证。
- 不把人的角色缩减为目标输入和异常审批。
- 不用“角色 Agent”暗示真实岗位、权限或独立性。
