# 一人公司研发规范

这是本仓库唯一的正式研发规范入口。规范按立项、产品设计、工程交付、运行维护四个分类组织十一项研发活动；每项工作只读取一个相关分类和一个或少数相关项目，不扫描整套文档。

人始终拥有产品方向、用户价值、风险接受、高影响副作用和最终问责。AI 可以准备分析、方案、实现与证据，但不会因流程、角色或 skill 名称获得额外授权。

## 使用方式

1. 先说明要改变的结果、明确不做什么，并判断工作属于 Quick、Standard 还是 High-risk。
2. 从下方选择一个主要分类，先读分类入口，再读直接相关的项目正文。
3. 实现中发现上游前提不成立时，返回拥有该决定的项目；不得在下游静默改写产品、风险或发布边界。
4. 结论必须带当前证据、剩余风险和下一步。失败、停止、回退和终止都是真实结果。

## 风险分流

| 路径 | 适用情况 | 最小要求 |
| --- | --- | --- |
| Quick | 低风险、可逆、无用户、生产或敏感数据影响 | 产物或 diff、相关检查、剩余风险 |
| Standard | 用户可见、跨文件或跨会话、AI 行为变化、需要独立验收 | 默认创建或继续 OpenSpec change，保留验收、验证与回滚，独立终审 |
| High-risk | 生产、客户数据、安全、权限、凭据、付款、公开承诺、外部通信或不可逆动作 | 副作用前记录影响、停止条件和回滚，由独立者预审并取得用户明确批准 |

具体路由和完成要求由唯一研发 skill [one-person-openspec-rd](skills/one-person-openspec-rd/SKILL.md) 承载。Quick 不强制创建 OpenSpec；Standard/High-risk 的实现性变更默认使用 OpenSpec，除非用户明确批准跳过并记录 owner、理由、范围和恢复方式。

## 四分类与十一项

- [立项](docs/01-initiation/README.md)
  - [选题](docs/01-initiation/01-topic-selection.md)
  - [调研](docs/01-initiation/02-research.md)
- [产品设计](docs/02-product-design/README.md)
  - [定义](docs/02-product-design/03-definition.md)
  - [体验设计](docs/02-product-design/04-experience-design.md)
- [工程交付](docs/03-engineering-delivery/README.md)
  - [技术设计](docs/03-engineering-delivery/05-technical-design.md)
  - [计划](docs/03-engineering-delivery/06-planning.md)
  - [实现](docs/03-engineering-delivery/07-implementation.md)
  - [验证](docs/03-engineering-delivery/08-verification.md)
  - [发布](docs/03-engineering-delivery/09-release.md)
- [运行维护](docs/04-operations-maintenance/README.md)
  - [运行](docs/04-operations-maintenance/10-operation.md)
  - [评估](docs/04-operations-maintenance/11-evaluation.md)

这四类不是只能前进一次的流水线。评估形成的新事实必须回到拥有相应决定的项目：价值或优先级变化回到选题，证据不足回到调研，行为或体验变化回到产品设计，技术、质量或发布缺口回到工程交付。

## 治理与追溯

- [治理说明](governance/README.md)
- [项目映射](governance/project-map.json)
- [当前状态](governance/current-status.json)
- [人工批准记录](governance/rd-standards/approvals.jsonl)
- [规则覆盖矩阵](governance/rd-standards/review/coverage-matrix.csv)
- [原子规则账本](governance/rd-standards/review/atomic-rules.csv)
- [原则追溯表](governance/rd-standards/review/principle-traceability.csv)
- [完全覆盖证据](governance/rd-standards/replacement-manifest.json)

正式正文包含 2,321 个唯一稳定规则目标；5,956 条来源原子规则及其处理决定保留在治理账本中。账本负责历史来源追溯，不构成第二份正式规范。

## 验证

运行：

    python tools/verify_rd_standards.py .
    python tools/check_runtime_skill_sync.py .
    openspec validate --all --strict --no-interactive

验证器只证明结构、追溯、链接和运行时 skill 状态符合当前约束；它不能替代真实任务验收、独立审查或高风险批准。
