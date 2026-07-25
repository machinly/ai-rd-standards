# rd-standards Context Pack

## Mission

帮助一个人和 AI 用足够而不过量的控制可靠交付产品。人的产品判断、价值边界、高影响批准和最终问责不可外包。

## Canonical Shape

- 总入口：`README.md`
- 立项：`docs/01-initiation/README.md`，包含选题、调研
- 产品设计：`docs/02-product-design/README.md`，包含定义、体验设计
- 工程交付：`docs/03-engineering-delivery/README.md`，包含技术设计、计划、实现、验证、发布
- 运行维护：`docs/04-operations-maintenance/README.md`，包含运行、评估
- 唯一研发 skill：`skills/one-person-openspec-rd/`
- 治理入口：`governance/README.md`、`governance/project-map.json`、`governance/current-status.json`
- 追溯证据：`governance/rd-standards/review/`

## Default Reading

1. 读根 `README.md`。
2. 选择一个主要分类并读其 `README.md`。
3. 只读一个或少数直接相关的项目正文。

评估或验证推翻前提时，返回拥有该决定的项目，而不是在下游补写新的产品、风险或发布边界。

## Risk Routes

- Quick：低风险、可逆、无用户、生产或敏感数据影响；不强制流程文件或 OpenSpec。
- Standard：用户可见、跨文件或跨会话、AI 行为变化、需要独立验收；实现性变更默认创建或继续 OpenSpec，完成前独立终审。
- High-risk：生产、客户数据、安全、权限、凭据、付款、公开承诺、外部通信或不可逆动作；副作用前记录影响、停止与回滚，由独立者预审并取得用户明确批准。

## Human Ownership

人持续负责：

- 产品为谁服务以及为什么值得做；
- 产品行为、数据、价格、合同和公开承诺；
- 安全、隐私、法律、财务和不可逆风险接受；
- 生产发布、真实付款、外部通信、删除和凭据动作；
- 最终用户结果与公司行为。

AI 可以准备证据、方案、实现和验证，但不会因 skill、角色或流程名称获得额外权限。

## Evidence Boundaries

- unit、integration、dependency-container、complete local integration、Browser E2E、真实 provider 和人工验收必须分开命名。
- OpenSpec 记录 change 增量与执行状态，不替代产品输入、体验设计、真实验收或独立审查。
- `governance/current-status.json` 是单一当前状态；更新的失败、`changes_requested` 或失效证据否决旧完成摘要。
- 规则标记的历史来源与合并决定在治理账本中；账本不是第二份正式规范。

## Commands

    python tools/verify_rd_standards.py .
    python tools/check_runtime_skill_sync.py .
    openspec validate --all --strict --no-interactive

任何 PASS 都不自动证明真实项目效果，也不授权高风险副作用。

## Handoff Prompt

    Read README.md, then one relevant category README and one or a few directly relevant item documents.
    Route the work as Quick, Standard, or High-risk with one-person-openspec-rd.
    Return to the item that owns a decision when evidence invalidates an upstream assumption.
    Do not scan the full standards set by default.
    High-impact side effects require explicit human approval.
