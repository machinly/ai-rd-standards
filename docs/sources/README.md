# 来源与证据政策

来源目录用于保存参考，不直接产生强制规则。核心规则只能引用与适用范围匹配的证据，并必须允许反证。

## 证据等级

| 类型 | 含义 | 默认权重 |
| --- | --- | --- |
| Primary research | 原始论文、数据、标准或官方规范 | 中到高，仍需检查方法与适用范围 |
| First-party experience | 厂商或项目自己的工程经验 | 中，限于相似系统和任务 |
| Case study | 一个或少量实例 | 低到中，只能提出假设 |
| Secondary analysis | 二手总结、媒体或个人分析 | 低，需要回到原始来源 |
| Anecdote | 无法独立验证的事件或观点 | 很低，不支撑强制规则 |

预印本不是自动无效，但必须标注未同行评审、样本、任务和结论边界。

## 核心声明记录

关键声明记录在 evidence-registry.jsonl。每条至少包含：

- claim_id
- claim
- source
- source_type
- evidence_level
- supports
- challenges
- applicability
- limitations
- reviewed_on
- status
- superseded_by

## 使用规则

- 来源存在不等于声明成立。
- 厂商产品经验不能直接推广到所有软件研发。
- 数值结论必须保留测量口径。
- 单实例案例不能证明普遍可靠性。
- 二手事故不得写成无保留事实。
- 核心规则需要至少一个反例或删除条件。
- 反证使用 `challenges` 指向它削弱的假设；不能把反证硬写成支持当前规则的材料。
- 来源或结论被更新时用 `superseded_by` 指向替代记录；`null` 表示尚无替代，不代表永远有效。
- 发现更强证据时更新 registry，不复制整篇来源。

## 现有资料

- 2026-06-23-source-map.md：历史来源目录，覆盖面广，但证据等级不统一。
- 2026-07-08-small-project-management-operating-guide.md：历史研究草案；旧 W 映射和“超过半天”门槛不具规范效力。
- evidence-registry.jsonl：最小内核和实验性操作模型使用的关键声明登记。

历史 source map 是检索目录，不是规范证明书。
