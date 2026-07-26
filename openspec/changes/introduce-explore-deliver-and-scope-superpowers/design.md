## Context

唯一决策依据是 `docs/superpowers/specs/2026-07-26-rd-explore-deliver-superpowers-scope-design.md`。本 change 不复制该设计的完整论证，只锁定正式规范、OpenSpec capability、运行时路由、用户级 instruction 与治理追溯之间的责任边界。

## Goals / Non-Goals

**Goals**

- 在读取研发正文前排除非研发任务，并只把混合请求中的研发结果纳入规范。
- 将研发一级工作模式明确为 Explore / Deliver，只在 Deliver 下使用 Quick / Standard / High-risk。
- 让 Product Discovery、UX Prototype 和 Technical Spike 通过轻量 sandbox、最短可见事实和明确 promote 边界降低不确定性。
- 将 Superpowers 收窄为复杂问题的按需工具箱，选择最小 skill 集且禁止自动串联。

**Non-Goals**

- 不增加第五分类、第十二项目、第四个风险路径或新的流程平台。
- 不让 Explore 绕过真实生产、客户数据、凭据、付款、外部通信或不可逆副作用门禁。
- 不把 Prototype 或 Walking Skeleton 定义为 route。
- 不修改 Superpowers 插件缓存，不把结构校验冒充流程效果验证。

## Decisions

### 1. 根入口拥有 applicability 与一级路由

根 README 和选题拥有 R&D applicability、混合任务边界、Explore / Deliver 以及 Superpowers complexity gate。非研发结果在读取四分类十一项前退出；Quick / Standard / High-risk 只属于 Deliver。

### 2. Explore 语义由既有项目分别拥有

调研拥有 Product Discovery 与 Explore sandbox；定义拥有 promote 决定；体验设计区分 Explore 的 UX Prototype 与 Deliver 的 formal visual UX；技术设计拥有 Technical Spike 和 Walking Skeleton；计划拥有 active-task 与 showcase cadence；实现拥有选择性 TDD；验证拥有可理解 fixture 与 showcase 证据命名；评估拥有 Explore outcome 与 process net benefit。不会新增分类、项目或第二套规范。

### 3. Deliver 保留现有门禁

Deliver 继续按 Quick / Standard / High-risk 分流。Standard/High-risk implementation 默认使用 OpenSpec；真实生产、数据、权限、凭据、付款、外部通信和不可逆动作继续应用现有风险、批准、验证与独立审查要求。Explore promote 时只把人选中的最小稳定增量转换为 Deliver。

### 4. 权威状态只存在一处

本 change 的 `tasks.md` 是执行状态权威，已确认设计记录理由，正式正文记录运行规则，治理账本只记录历史来源映射。已有 OpenSpec tasks 足够时，不并行维护 Superpowers plan 或 work brief。

### 5. 运行时分为 repo router 与个人默认作用域

`one-person-openspec-rd` 是薄 R&D 路由；用户级 `~/.codex/AGENTS.md` 部署跨仓库默认的 Superpowers scope。更靠近工作目录的 repo/nested `AGENTS.md` 仍可覆盖个人默认值，因此试点必须检查实际 instruction chain。只维护带 markers 的 bounded block，不覆盖其他用户内容。

### 6. Superpowers 由具体复杂度触发

实质产品歧义、多种高返工方案、跨组件或难回退架构、复杂跨会话依赖、未知或首次修复失败的故障，以及重大合并、发布或完成结论，才允许选择一个或少数直接相关 skills。会话开始、AI 参与、创作性、时长和文件数不能单独触发；调用一个 skill 不授权另一个。

## Risks / Trade-offs

- Applicability 过窄可能漏掉直接支持产品决定的研究：用“是否直接支持已识别产品/工程决定”作为边界。
- Explore 被用来逃避交付门禁：promote 时重新路由，任何 sandbox 越界立即停止轻量豁免。
- 时间/WIP 规则变成新的仪式：只维护单一短记录，文件数和提交数不作为效果指标。
- Global instruction 与项目 instruction 冲突：以更近的适用 `AGENTS.md` 为准，并在试点前显式检查。
- Scope validator 只能证明部署一致：真实选择行为必须由代表场景和新 Explore pilot 验证。

## Migration / Rollback

1. 先归档已接受的 visual UX change，再创建并严格校验本 change。
2. 先用失败测试锁定 16 个 rule-id、2,337 总数和运行时 managed block，再更新正式正文、账本、router 与知识入口。
3. 机械同步 canonical router，bounded 更新用户级 `AGENTS.md`，完成代表场景、完整验证和真正独立终审。
4. 新的本地合成 Explore pilot 单独验证流程效果；没有真实证据时保持 pending。
5. 若需回滚，通过后续 Standard change 收窄 Explore 或 Superpowers 规则；只移除 managed markers 内文本，保留 applicability、真实 High-risk 控制和历史证据。
