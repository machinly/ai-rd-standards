# W2 OpenSpec / Risk 核心入口

## W2 定位

本文件是 W2 OpenSpec / Risk 的核心入口，也是进入 `docs/W2-openspec-risk/` 后默认先读的唯一主规范。W2 只回答一个问题：**这次变更的行为、边界、风险和退出条件是什么？**

W2 不负责实现，不负责替代产品发现，也不负责上线证明。W0/W1 已经说明这件事值得做、要解决什么问题；W2 负责把它压成一个可审查的 OpenSpec change，并在实现前确认架构、契约、数据、安全、权限、成本、供应商、IP 和用户承诺边界。

## 核心问题

任何超过 30 分钟，或影响用户、生产、数据、安全、成本、AI 行为、公开承诺、客户数据、供应商或知识产权的工作，都先进入 W2。W2 必须回答：

- 这次具体改变什么行为，不改变什么？
- 哪些用户、系统、数据、权限、供应商、契约或承诺会受到影响？
- 哪些风险必须在实现前写清，哪些可以留到验证或发布门禁？
- 哪些判断必须由人做，哪些交给 Codex、skill、verifier 和测试承接？
- 什么条件下可以进入 W3/W4/W5/W6，什么条件下回到 W0/W1 停车或补证据？

默认原则：没有 OpenSpec change、风险边界和退出条件的高影响工作，不进入实现。

## 适用范围

适用：

- 用户可见功能、AI workflow、生产系统、API、数据流、权限、配置、供应商、合规声明或公开承诺的变更。
- 会改变架构边界、模块职责、数据所有权、Protobuf/API、错误语义、AI tool schema、身份权限、租户隔离、成本容量、客户数据生命周期、供应商处理方、IP 来源或信任政策的工作。
- 超过 30 分钟且需要中断后可恢复上下文的研发批次。

不适用：

- 小于 30 分钟、低风险、可轻易回滚、无用户/生产/数据/安全/成本影响的修复；完成后补一句 change log 即可。
- 目标用户、痛点、证据和成功指标尚不清楚的工作；回到 W1。
- 事故止血、发布执行、线上观测、学习复盘和文档维护；分别进入 W7、W6、W7/W8、W9。

## 最小产出

每个 W2 工作单元必须落到一个 OpenSpec change：

```text
openspec/changes/<change-id>/
  proposal.md
  design.md
  tasks.md
  specs/*/spec.md
```

最小要求：

- `proposal.md`：意图、范围、不做什么、依据、需要人的判断。
- `specs/*/spec.md`：可验证 requirement，包含 scenario，并使用 OpenSpec 可识别的 `SHALL` 或 `MUST`。
- `design.md`：只记录实现前必须锁定的技术、数据、安全、成本或供应商决策。
- `tasks.md`：能逐项完成和验证的 checklist。

必要时补充专项工件：

- 架构：ADR、boundary JSON、module map、dependency rules。
- 契约：surface map、compatibility policy、protobuf evolution、error model、contract tests、AI tool schema。
- 安全隐私：threat model、privacy record、supply-chain record、secrets record。
- Auth：identity boundary、policy matrix、authorization tests、audit notes。
- 成本容量：budget、vendor boundary、cost/capacity runbook。
- 客户数据：data map、transfer contract、sync runbook、rights/deletion policy。
- 供应商：processor register、DPA checklist、subprocessor watch、transfer impact。
- IP：source register、license policy、AI output policy、notice/attribution。
- 信任承诺：commitment register、policy surfaces、AI disclosure、data rights runbook。

## 人工判断点

默认不问人的事项：文件落点、模板初稿、低风险字段补齐、普通章节命名、可回滚局部实现、已由仓库默认栈明确的技术细节。

必须人工判断：

- 是否改变产品方向、目标用户、定价、公开承诺或客户合同边界。
- 是否改变数据边界、隐私用途、安全例外、认证授权、租户隔离或高风险 AI 副作用。
- 是否接受 breaking API/protobuf/schema/AI tool contract 变化。
- 是否引入长期架构锁定、关键供应商、数据出境、DPA 缺口、供应商训练/保留或显著成本。
- 是否处理敏感数据、高影响领域、客户数据删除例外、不可逆数据动作或无法履行的用户权利请求。
- 是否引入高风险许可证、无授权素材、客户内容复用或对 AI 输出做强权利声明。

## 触发型专项

- OpenSpec change、AI 研发操作系统、双重 review 和工作单元治理细则：读 `docs/W2-openspec-risk/01-one-person-ai-rd-operating-model.md`。
- 架构边界、模块职责、数据所有权、依赖方向、ADR 或服务拆分：读 `docs/W2-openspec-risk/02-architecture-boundary-standard.md`。
- API、Protobuf、错误语义、事件、webhook、AI tool schema 或兼容性变化：读 `docs/W2-openspec-risk/03-api-contract-compatibility-standard.md`。
- 威胁模型、数据处理、依赖供应链、secret、构建来源或安全隐私门禁：读 `docs/W2-openspec-risk/04-security-privacy-supply-chain-standard.md`。
- 认证、授权、租户隔离、support/admin 访问或 AI 代用户操作：读 `docs/W2-openspec-risk/05-auth-tenant-boundary-standard.md`。
- 成本预算、容量、限流、供应商依赖、超支或降级：读 `docs/W2-openspec-risk/06-cost-capacity-vendor-boundary-standard.md`。
- 客户数据导入、导出、同步、删除、备份、向量库或 AI 记忆数据流：读 `docs/W2-openspec-risk/07-customer-data-portability-lifecycle-standard.md`。
- 新供应商、DPA、子处理方、数据出境、供应商训练或保留条款：读 `docs/W2-openspec-risk/08-processor-transfer-vendor-standard.md`。
- 开源许可证、第三方素材、AI 生成内容、客户内容复用、NOTICE 或 attribution：读 `docs/W2-openspec-risk/09-ip-license-provenance-standard.md`。
- 隐私页、条款、AI disclosure、退款、安全、合规或用户承诺：读 `docs/W2-openspec-risk/10-trust-policy-compliance-standard.md`。

## 出口

- 产品问题、目标用户、证据或成功指标不清：回到 W1。
- 工作不值得进入 now/expedite，或 appetite 不成立：回到 W0 停车、杀掉或补证据。
- 用户可见 AI 行为、prompt、工具、模型、RAG、记忆或安全边界变化：进入 W3，先定义 eval、失败样例、红队样例和 fallback。
- 行为、边界和风险已写清，可以实现：进入 W4，并让 tasks.md 成为执行清单。
- 实现后需要证据证明质量、安全、性能、可访问性或韧性：进入 W5。
- 准备发布、客户上线或对外承诺：进入 W6。
- 风险无法关闭：回到 W0/W1 调整范围、停车或拆成更小 change。

## Review 1：一人公司注意力审查

- 保留：W2 只做实现前边界，不把所有专项都变成默认必读。
- 保留：人的判断集中在方向、数据、安全、成本、供应商、不可逆动作和承诺。
- 调整：旧的多个 W2 主规范统一降级为触发型专项，避免进入目录后不知道先读谁。
- 风险：W2 容易变成填表。缓解：只有触发条件命中的专项才读，OpenSpec tasks 必须直接服务后续实现和验证。

结论：可落地。W2 主入口把“先写代码”改成“先锁定行为、边界和退出条件”，但不强迫一次读完所有风险规范。

## Review 2：产品、工程、运维、安全、成本审查

- 产品角度：W2 保护 W1 的证据和 scope 不在实现中漂移。
- 工程角度：OpenSpec、契约、架构和 tasks 让 Go/Vite/AI 实现可以分批落地。
- 运维角度：成本、容量、供应商、降级和事故前置，减少上线后才发现无 runbook。
- 安全隐私角度：数据、auth、tenant、供应链、客户数据和供应商处理方在实现前进入边界。
- 成本角度：预算、硬限制、供应商退出计划和 appetite 防止一人公司被长期锁定或账单击穿。

结论：可落地。W2 完成后，下一步应该是一个小而明确的 W3/W4/W5/W6 出口，而不是继续扩写风险文档。
