# rd-standards How-To

## 1. R&D Applicability

先读根 `README.md` 的 applicability。任务主要结果只有在以下任一条件成立时进入研发：改变、验证、发布、运行、恢复或处置产品/工程系统；直接决定产品/体验/技术/验收边界；研究直接支持一个已识别产品或工程决定。

### Non-R&D

- 普通写作、翻译、摘要、内容制作、行政、账目整理、一般查询、通用研究和未获实现授权的只读报告使用自身流程。
- 不继续读取四分类十一项目，不创建 OpenSpec、研发状态或 Superpowers 工件。
- 混合请求按结果拆分；非研发部分只消费已验证事实。
- 退出研发规范不取消删除、外发、敏感数据、法律、财务等任务自身授权边界。

## 2. Explore or Deliver

进入研发后先选择工作目的：

- Explore：关键未知仍主导，目标是用可证伪证据学习。
- Deliver：行为已经足够明确，目标是稳定、可维护、可验收的增量。

Prototype 是 Explore artifact；Walking Skeleton 是 tactic；两者都不是 route。

### Explore

1. 按最高优先级未知选择 Product Discovery、UX Prototype 或 Technical Spike。
2. 只维护一份短记录：question、hypothesis、sandbox boundary、shortest slice、active tasks、showcase、evidence/limits、decision、next。
3. 保持本地/隔离、合成、可 reset/reseed；不接触生产、真实客户数据、真实凭据、未批准外部系统、付款、外部通信、公开承诺或不可逆动作。
4. 同时最多 5 个 active tasks；先从实际产品入口关闭一条 Walking Skeleton。
5. 每 120 分钟或每 5 次提交 showcase，以先到者为准；连续 2 小时无新增可见事实时 shrink 或 stop。
6. 使用 Alice、Bob、Admin 等可理解 fixture，准确区分 showcase、Browser E2E 和 Deliver acceptance。
7. 结束时只选 `validated | invalidated | revise | stopped | promote`。只有人选择的最小稳定增量可以 promote，并重新判断 Deliver route。

轻量 Explore 默认不创建 OpenSpec、formal visual UX、完整质量矩阵或独立终审；实际命中的安全、授权、数据和副作用控制仍然适用。

### Deliver / Quick

- 写清一个明确结果和 non-goals。
- 做最小可逆变更，运行相关检查并报告剩余风险。
- 不强制创建 OpenSpec。

### Deliver / Standard

- 实现前创建或继续一个 OpenSpec change。
- 记录 outcome、non-goals、acceptance、scope、risks、verification、rollback 和 next；`tasks.md` 是执行状态来源。
- 用户可见工作先确认产品行为、体验、`visual_ux` 判定与关键旅程；OpenSpec 只链接这些输入。
- 需要未参与产出的 independent final review。

### Deliver / High-risk

- 记录 decision owner、影响范围、停止条件和回滚。
- 将准备与真实副作用分开。
- 在生产、删除、付款、外部通信、权限或凭据动作前取得用户明确批准。
- auth、数据迁移、管理员权限和难回退设计先由未参与产出的审查者预审；缺少批准、权限或回滚证据时停止。

Deliver Standard/High-risk 的代码、配置、schema、API、AI 行为、数据、基础设施或发布设计变更默认使用 OpenSpec。只有用户明确批准并记录 owner、理由、范围和恢复方式时，具体实现才可跳过。

## 3. Superpowers Complexity Gate

只为具体复杂问题选择最小直接相关 skill：重大产品/UX 歧义或多方案架构可用 brainstorming；现有状态不足的复杂跨会话计划可用 writing-plans；根因未知或首次修复失败的故障可用 systematic-debugging；重大完成、merge 或 release 结论可用 verification-before-completion；Deliver Standard/High-risk 终审按授权使用 review skill。

会话开始、AI 参与、创作性、任务时长和文件数都不能单独触发。调用一个 skill 不授权另一个；已有产品文档、技术设计、Explore record 或 OpenSpec 足够时，不创建平行 Superpowers spec/plan/work brief。默认单 Agent；只有用户允许、任务独立、写域不重叠且有净收益时才有限并行。

## 4. 验证

运行：

    python tools/verify_rd_standards.py .
    python tools/check_runtime_skill_sync.py .
    openspec validate --all --strict --no-interactive

分别解释结果：formal verifier 只证明四分类十一项目、2,337 个 rule-id、追溯和链接；runtime checker 只证明 canonical/installed router 与用户级 scoped block 一致；OpenSpec validation 只证明规格结构。它们不能替代真实 Explore 效果、Deliver acceptance、独立审查或高风险批准。

## 5. 更新知识

结构变化后：

1. 更新根入口、受影响分类和项目正文。
2. 更新 `knowledge/docs-map/rd-standards.json`、context pack、how-to 与 glossary。
3. 向 `knowledge/freshness/rd-standards.jsonl` 追加事实记录。
4. 更新 decision、approval 和 `governance/current-status.json`。
5. 不改写历史 replacement manifest，不在多个入口复制动态状态。
