# 一人公司研发规范

这是本仓库唯一的正式研发规范入口，但它只适用于会改变、验证、发布、运行或直接决定产品/工程系统的工作。普通写作、翻译、摘要、内容制作、行政、一般查询和与具体产品/工程决定无关的研究使用任务自身流程，不需要套用本规范。

适用的研发工作按立项、产品设计、工程交付、运行维护四个分类组织十一项活动。四个分类文件只承载分类原则，十一项文件只承载项目原则；需要落地时，再从执行细节总索引中读取一个或少数命中的主题文件，不扫描整套文档。

人始终拥有产品方向、用户价值、风险接受、高影响副作用和最终问责。AI 可以准备分析、方案、实现与证据，但不会因流程、角色或 skill 名称获得额外授权。

## 使用方式

1. **R&D applicability**：任务主要结果是否改变、验证、发布、运行、恢复或处置产品/工程系统，直接决定其产品/体验/技术/验收边界，或研究直接支持一个已识别产品/工程决定？否，则立即使用任务自身流程。
2. **Work mode**：存在关键未知且目标是学习时选 Explore；行为已经足够明确且目标是稳定交付时选 Deliver。
3. **Deliver route**：只有 Deliver 再按 Quick、Standard、High-risk 分流。
4. 进入研发后，从下方选择一个主要分类，先读分类原则，再读一个或少数直接相关的项目原则；需要执行规则时，从[执行细节总索引](docs/execution-details.md)按主题只加载命中的细节文件。
5. 实现中发现上游前提不成立时，返回拥有该决定的项目；不得在下游静默改写产品、风险或发布边界。
6. 结论必须带当前证据、剩余风险和下一步。失败、停止、回退和终止都是真实结果。

```text
Task → R&D applicability
       ├─ No  → use the task's own workflow
       └─ Yes → Explore | Deliver
                 Explore: Product Discovery | UX Prototype | Technical Spike
                 Deliver: Quick | Standard | High-risk
```

`Prototype` 是 Explore 中用于学习的 artifact，`Walking Skeleton` 是尽快贯通真实入口和可见结果的实施 tactic；两者都不是 route。混合请求按结果拆分，只有研发部分进入本规范。非研发部分不创建 OpenSpec、研发状态或 Superpowers 工件。

Explore 类型跟随最高优先级未知：用户、问题或价值未知选 Product Discovery；关键任务流程、信息架构、交互或可理解性未知选 UX Prototype；架构、集成、契约或技术可行性未知选 Technical Spike。

## Explore 与 Deliver

| 工作模式 | 适用情况 | 最小要求 |
| --- | --- | --- |
| Explore | Product Discovery、UX Prototype 或 Technical Spike；关键未知仍主导，目标是学习 | 本地或隔离 sandbox、一份短记录、最短可见事实、真实 showcase、明确 outcome 与 next |
| Deliver | 目标行为已经足够明确，准备形成稳定增量 | 再按下表选择 Quick、Standard 或 High-risk |

### Deliver 风险分流

| 路径 | 适用情况 | 最小要求 |
| --- | --- | --- |
| Quick | 低风险、可逆、无实质用户行为、生产或敏感数据影响 | 产物或 diff、相关检查、剩余风险 |
| Standard | 实质用户可见行为、跨文件或跨会话、AI 行为变化、需要独立验收 | 默认创建或继续 OpenSpec change，保留验收、验证与回滚，独立终审 |
| High-risk | 生产、客户数据、安全、权限、凭据、付款、公开承诺、外部通信或不可逆动作 | 副作用前记录影响、停止条件和回滚，由独立者预审并取得用户明确批准 |

代表性边界是：不改变含义的局部按钮文案属于 Deliver Quick；已经确认的用户资料编辑属于 Deliver Standard；生产管理员权限或真实账号删除属于 Deliver High-risk。轻量 Explore 一旦准备接触真实客户数据、真实凭据或生产副作用，就停止轻量豁免并重新路由。

具体路由和完成要求由唯一研发 skill [one-person-openspec-rd](skills/one-person-openspec-rd/SKILL.md) 承载。轻量 Explore 和 Deliver Quick 不强制创建 OpenSpec；Deliver Standard/High-risk 的实现性变更默认使用 OpenSpec，除非用户明确批准跳过并记录 owner、理由、范围和恢复方式。领域关键词不能单独决定风险路径：只使用本地合成数据和测试凭据的 gateway/OIDC/service identity 学习任务属于 Explore / Technical Spike，不因 `auth` 一词自动升级为 High-risk。Superpowers 只在存在具体复杂问题时选择一个或少数直接相关 skills；会话开始、AI 参与、创作性、时长和文件数都不能单独触发，也不能因调用一项而自动串联其他项。已有 OpenSpec `tasks.md` 足以执行时只更新它，不再创建 Superpowers plan。产品或架构存在多个高返工合理方案时可只用 `brainstorming`，并把结论写回产品定义、技术设计或 OpenSpec design；编译器已直接证明漏 import 时直接机械修复和验证，不调用 `systematic-debugging`，根因未知或首次修复失败时才调用；只有用户允许、任务独立、写域不重叠、没有顺序依赖且确有净收益时才使用 parallel agents。

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

第三级统一从[执行细节总索引](docs/execution-details.md)进入。该索引逐项说明“内容层—执行细节类型—文件”的对应关系；分类和项目原则文件不复制这些细节。

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

正式正文包含 2,337 个唯一稳定规则目标；5,956 条来源原子规则及其处理决定保留在治理账本中。账本负责历史来源追溯，不构成第二份正式规范。

## 验证

运行：

    python tools/verify_rd_standards.py .
    python tools/check_runtime_skill_sync.py .
    openspec validate --all --strict --no-interactive

验证器只证明结构、追溯、链接和运行时 skill 状态符合当前约束；它不能替代真实任务验收、独立审查或高风险批准。
