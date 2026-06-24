# 一人公司 AI 研发操作系统规范

## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 `docs/W2-openspec-risk/main.md` 已经判断需要更细地定义 OpenSpec change、AI 研发操作系统、双重 review 或工作单元治理时，才读取本文件。

如果当前只是判断 W2 应该先读哪个文件，或只需要定义变更的基本意图、行为、边界、风险和退出条件，先回到 `docs/W2-openspec-risk/main.md`。

## 场景触发规范

- 架构边界、模块职责、数据所有权或依赖方向变化：进入 `docs/W2-openspec-risk/architecture-boundary-standard.md`。
- API、Protobuf、错误语义、事件、webhook、AI tool schema 或兼容性变化：进入 `docs/W2-openspec-risk/api-contract-compatibility-standard.md`。
- 威胁模型、数据处理、依赖供应链、secret、构建来源或安全隐私门禁：进入 `docs/W2-openspec-risk/security-privacy-supply-chain-standard.md`。
- 认证、授权、租户隔离、support/admin 访问或 AI 代用户操作：进入 `docs/W2-openspec-risk/auth-tenant-boundary-standard.md`。
- 成本预算、容量、限流、供应商依赖、超支或降级：进入 `docs/W2-openspec-risk/cost-capacity-vendor-boundary-standard.md`。
- 隐私页、条款、AI disclosure、退款、安全、合规或用户承诺：进入 `docs/W2-openspec-risk/trust-policy-compliance-standard.md`。
- 客户数据导入、导出、同步、删除、备份、向量库或 AI 记忆数据流：进入 `docs/W2-openspec-risk/customer-data-portability-lifecycle-standard.md`。
- 新供应商、DPA、子处理方、数据出境、供应商训练/保留条款：进入 `docs/W2-openspec-risk/processor-transfer-vendor-standard.md`。
- 开源许可证、第三方素材、AI 生成内容、客户内容复用、NOTICE/attribution：进入 `docs/W2-openspec-risk/ip-license-provenance-standard.md`。
- 用户可见 AI 行为：下一步进入 `docs/W3-ai-behavior/prompt-eval-agent-workflow-standard.md`。

## 最小产出

```text
openspec/changes/<change-id>/
  proposal.md
  design.md
  tasks.md
  specs/*/spec.md
```

必要时补充：

- `architecture/decisions/<yyyymmdd>-<decision>.md`
- `architecture/boundaries/<target>.json`
- `contracts/surface-map/<target>.json`
- security / privacy / supply-chain review artifact

## 目标

把“一个人 + AI 工具”的研发过程变成可恢复、可审查、可迭代的系统。它不追求团队级流程完整度，只追求让一个人持续交付时不被上下文、返工、线上风险和 AI 不确定性拖垮。

## 本规范只解决什么

- 如何把任何研发请求变成一个 OpenSpec change。
- 如何限制人的注意力消耗。
- 如何在每个阶段做两次落地 review。
- 如何让后续 Go/Kratos/sqlc/gRPC/Vite/运维规范都能接到同一条流水线上。

不在本规范展开的内容：具体 Go 项目结构、Kratos 服务模板、sqlc 查询规范、Vite UI 工程规范、SRE 告警细则。这些进入后续 W 步骤或触发型专项。

## 依据转译

- 《人月神话》提醒：不要把 AI 当作“银弹”。一人公司缺的不是更多并发，而是更低协调成本和更少误判。
- 小型项目管理的核心裁剪：只保留能避免返工、遗漏和失控的工件，砍掉仪式感。
- OpenSpec 的核心适配：每个变更有 proposal/spec/design/tasks，规格进入代码库，不留在聊天记录里。
- Anthropic agent 建议：优先 workflow，只有开放、动态、需要模型自主决策的任务才升级为 agent。
- OpenAI 文档建议：生产 prompt 进入代码、走测试与部署；AI 变化用 eval 管住，不靠感觉。
- Google ML 与 SRE 建议：先有指标和 pipeline，再谈复杂模型；上线后用 SLO/error budget 判断可靠性投入。

## 规则 1：工作单元只能是 OpenSpec change

任何超过 30 分钟的研发工作，必须先创建一个 change：

- `proposal.md`：为什么做、做什么、不做什么。
- `specs/*/spec.md`：用户可感知或系统可验证的行为变化。
- `design.md`：最少必要技术决策。
- `tasks.md`：能逐项完成和验证的 checklist。

少于 30 分钟且低风险的修复，可以直接做，但完成后要补一句 change log 到最近的相关 change 或规范文档。

## 规则 2：人的判断点要被压缩

默认不问人的问题：

- 文件命名、目录落点、局部实现方式。
- 已由技术偏好明确的选型：Go、Kratos、sqlc、gRPC、Vite、OpenSpec。
- 可轻易回滚、可测试验证、成本很低的实现细节。

必须问人的问题：

- 会影响产品方向、定价、目标用户或数据边界。
- 会引入长期架构锁定，例如云厂商、数据库、认证体系、计费平台。
- 会花费显著金钱或连续占用数天。
- 会触及隐私、安全、合规、不可逆数据迁移。
- 两种方案都合理，但代表完全不同的业务取舍。

提问格式必须短：最多 3 个选项，并给出推荐默认值。

## 规则 3：每个内容必须双重 review

每完成一个阶段性内容，先给两轮 review，再进入下一段。

Review A：一人公司可落地性

- 是否能被一个人独立执行？
- 是否减少认知负担，而不是增加流程负担？
- 是否有明确退出条件？
- 是否能在中断后恢复？
- 是否有自动化或 skill 能承接重复劳动？

Review B：产品/工程/运维风险

- 是否避免过早复杂化？
- 是否有测试、eval 或人工验收点？
- 是否有上线后观测信号？
- 是否保护用户数据和业务连续性？
- 是否能在失败时回滚或降级？

## 规则 4：AI 功能先定义 eval，再改 prompt 或模型

任何用户可见的 AI 能力都要先写最小 eval：

- 3-10 条代表性输入。
- 每条输入的可接受输出标准。
- 至少 1 条失败/攻击/边界样例。
- 记录当前模型、prompt 版本、测试日期。

prompt 必须作为代码或配置进入版本控制。不能把生产 prompt 只保存在聊天记录、控制台草稿或个人笔记中。

## 规则 5：后续技术规范的默认落点

- 服务端规范：Kratos service + Protobuf API + gRPC first；HTTP 只作为外部兼容层。
- 数据访问：SQL schema 和 query 先写清楚，再用 sqlc 生成类型安全 Go 代码。
- 前端规范：Vite 项目；界面参考 Vercel Geist 的浅色/深色 token，但不盲目复制品牌。
- 运维规范：先定义最小 SLO 和错误预算政策，再做告警和仪表盘。
- 文档规范：每个规范变更都必须能映射到一个 OpenSpec change。

## Review A：一人公司可落地性

结论：可落地，但必须保持“一个 change 一个目标”。

- 工件数量控制在 4 个核心文件，能防止 AI 上下文丢失，又不会变成重流程。
- 人只需要判断高成本、高风险、不可逆的事项，低风险细节交给默认规则。
- 双重 review 是轻量的，因为它只回答固定问题，不要求写长报告。
- 最大风险是把 OpenSpec 当成文档负担；应把 tasks 直接变成执行清单。
- 下一步应做一个能自动提醒这些规则的 Codex skill，减少每次手动复述。

## Review B：产品/工程/运维风险

结论：作为总入口足够稳，但还缺技术模板和验证脚本。

- 它避免了“先写代码再补解释”的 AI 研发常见失败模式。
- 它把 AI prompt/eval 纳入版本控制，为后续真实 AI 产品留出质量闸门。
- 它只定义原则，尚不能直接生成 Kratos/sqlc/Vite 项目；这些要在后续阶段分开完成。
- SLO 只作为后续接口出现，避免一开始就背上完整 SRE 体系。
- 风险最大的默认值是“gRPC first”：对外部 Web/API 集成时需要明确 HTTP gateway 策略，后续必须单独规范。

## 当前只需要你判断的事项

我建议默认接受这两个决策，除非你明确反对：

1. 每次只推进一个 active OpenSpec change，避免一人公司上下文分裂。
2. 双重 review 固定为“可落地性”和“产品/工程/运维风险”，后续每个阶段都沿用。
