# AI 研发工作流入口

## 目标

这份文档只回答一个问题：**当前工作处在 AI 研发工作流的哪一步？**

默认不要按“技术主题”或“阶段编号”读规范。先定位工作流 step，再读该 step、上一步输入、下一步门禁。人的注意力只用于高影响判断，细节由 OpenSpec、skill 和 verifier 承接。

## 工作流总览

```text
W0 Intake
  -> W1 Discovery
  -> W2 OpenSpec / Risk Frame
  -> W3 AI Behavior Design
  -> W4 Product / System Build
  -> W5 Verification / Safety Gates
  -> W6 Release / Launch
  -> W7 Operate / Observe
  -> W8 Learn / Improve
  -> W9 Maintain / Recover Context
```

## W0：工作入口与当前焦点

**问题**：这件事现在该不该做？

只读：

- `docs/W0-intake/main.md`

最小产出：

- `planning/work-intake/<work-id>.json`
- `planning/decision-board/<period>.json`

需要你判断：

- 是否进入 `now` / `expedite`。
- 是否停车、杀掉或超过本周期 appetite。

## W1：问题发现、用户证据与成功指标

**问题**：我们要解决的是真问题，还是只是想做一个功能？

只读：

- `docs/W1-discovery/main.md`
- 需要事件、指标或实验时读 `docs/W1-discovery/product-analytics-experiment-standard.md`
- 支持反馈成为证据时读 `docs/W8-learn/customer-support-trust-ops-standard.md`

最小产出：

- product bet
- metrics map 或 learning decision
- feedback / evidence reference

需要你判断：

- 目标用户、问题定义、成功指标和不做什么。
- 是否接受证据不足但仍继续。

## W2：OpenSpec、边界与风险框定

**问题**：这次变更的行为、边界、风险和退出条件是什么？

只读：

- `docs/W2-openspec-risk/main.md`
- 必要时读架构、契约、安全隐私、auth、成本、客户数据、供应商、IP 或信任承诺专项。

最小产出：

```text
openspec/changes/<change-id>/
  proposal.md
  design.md
  tasks.md
  specs/*/spec.md
```

需要你判断：

- 产品方向、数据边界、安全隐私例外、长期架构锁定、显著成本。

## W3：AI 行为设计、eval 与安全样本

**问题**：AI 能力在什么输入下算好、算坏、必须拒绝或降级？

只读：

- `docs/W3-ai-behavior/main.md`
- 需要 prompt/eval、数据集、红队、内容安全、记忆、模型路由、工具、RAG、模型优化或本地化时，再读对应触发专项。

最小产出：

- prompt / model / route / tool 设计
- eval fixtures
- red-team / abuse cases
- rollback 或 fallback 规则

需要你判断：

- 是否接受无 eval 的 AI 行为变更。
- 是否允许模型供应商、工具权限、RAG 来源或记忆策略变化。

## W4：产品与系统实现

**问题**：如何把已定义的行为落到 Go、Vite、数据、配置和任务系统里？

只读：

- `docs/W4-build/main.md`
- 需要后端、前端、数据、配置、本地开发、AI 协作编码、计费、异步任务、事件/Webhook、通知或开发者体验时，再读对应 W4 触发专项。

最小产出：

- 可 review 的实现批次
- migration / config / feature flag / worker / integration 工件
- 本地验证结果与 AI coding batch log
- 交给 W5 的测试、风险和残余缺口

需要你判断：

- 不可逆数据迁移。
- 生产配置默认值。
- 会改变用户可见承诺的 UI、API、权限、计费、通知或外部副作用。

## W5：验证、安全门禁与质量回归

**问题**：上线前有什么证据说明它不会明显伤害用户、成本、可靠性或信任？

只读：

- `docs/W5-verify/main.md`
- 需要测试质量、可访问性/AI UX、性能回归或韧性演练时，再读对应 W5 触发专项。
- AI 输出变更时读 `docs/W8-learn/ai-quality-regression-incident-standard.md`

最小产出：

- test run / eval run
- accessibility / UX review
- performance / resilience result
- accepted risk 或 rollback plan

需要你判断：

- 是否接受失败门禁、性能回归、AI 质量回归或安全/隐私例外。

## W6：发布、客户上线与对外承诺

**问题**：这次变更能不能发布、如何发布、对谁承诺什么？

只读：

- `docs/W6-release/main.md`
- 需要发布流水线、客户上线、对外声明证据或合同/SLA 时，再读对应 W6 触发专项。

最小产出：

- release checklist
- launch readiness
- smoke test / rollback path
- claim evidence map

需要你判断：

- 生产发布、回滚、公开声明、客户定制、合同/SLA 承诺。

## W7：线上运行、观测与事故处理

**问题**：上线后如何知道它活得好不好，坏了怎么恢复？

只读：

- `docs/W7-operate/main.md`
- 需要 SRE-lite、观测性、备份恢复、后台运营、基础设施、事故响应或凭据生命周期时，再读对应 W7 触发专项。

最小产出：

- SLO / dashboard / alert
- incident record
- restore or rotation run
- ops review

需要你判断：

- 是否升级事故、通知客户/监管、执行生产恢复或凭据轮换。

## W8：反馈、学习与下一轮改进

**问题**：我们从用户、指标、支持、eval 和事故里学到了什么？

只读：

- `docs/W8-learn/main.md`
- 需要支持反馈、信任运营或 AI 质量回归时，再读对应 W8 触发专项。
- 如果学习结果改变问题定义或优先级，再回到 `docs/W1-discovery/main.md` 或 `docs/W0-intake/main.md`。

最小产出：

- learning decision
- quality regression record
- support-to-R&D feedback
- updated work intake / decision board

需要你判断：

- 是否继续、停车、杀掉、扩大、回滚或重新定义产品方向。

## W9：维护、依赖、文档与上下文恢复

**问题**：这套系统下次还能被你和 Codex 接起来吗？

只读：

- `docs/W9-maintain/main.md`
- 需要知识恢复、维护债务、审计证据或开源维护时，再读对应 W9 触发专项。

最小产出：

- docs map / context pack / freshness log
- debt / dependency review
- evidence package

需要你判断：

- canonical 文档入口、术语变化、删除/归档文档、接受过期文档。

## 使用规则

- 新需求从 W0 开始，不能直接跳到实现。
- AI 行为变化必须经过 W3，再进入 W4。
- 代码完成不等于完成；至少走到 W5。
- 用户可见或生产变更必须走到 W6/W7。
- 学习和回归进入 W8，再决定是否回到 W0。
- 文档和索引问题进入 W9，不要伪装成新功能。
- 新增或重命名规范后必须运行 `python tools\verify_workflow_index.py .`，确认它挂到了 W0-W9。

## 给 Codex 的接手提示

```text
先读取 README.md、docs/00-start-here.md、knowledge/context-packs/rd-standards.md。
先判断当前任务处在 W0-W9 哪一步。
只读取该 step、上一步输入和下一步门禁对应的规范。
如果需要实现，创建或更新一个 OpenSpec change。
只把高影响决策交给用户，其余按对应 skill、verifier 和两轮 review 落地。
```

## Review 1：一人公司注意力审查

- 保留：每一步只回答一个研发问题，避免按主题散读。
- 保留：人只判断 now/expedite、方向、风险、发布、事故和 canonical 入口。
- 调整：索引从“场景选择器”改为 W0-W9 工作流，新增规范必须挂靠某一步。
- 风险：工作流看起来比场景表更长。缓解：实际使用只读当前一步和相邻一步。

结论：可落地。它把规范变成一条 AI 研发流水线，而不是阶段仓库。

## Review 2：产品、工程、运维、安全、成本审查

- 产品角度：W0/W1/W8 防止一开始就写代码。
- 工程角度：W2/W4/W5 把规格、实现和验证分清。
- 运维角度：W6/W7 明确发布后才算进入真实运行。
- 安全隐私角度：W2/W3/W5 把数据、模型和安全门禁提前。
- 成本角度：工作流减少全库阅读和重复上下文恢复。

结论：可落地。新增规范以后必须服务某个 workflow step，否则就不该加入主索引。







