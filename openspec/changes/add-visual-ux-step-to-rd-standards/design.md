## Context

唯一产品与流程设计依据是 `docs/superpowers/specs/2026-07-24-rd-visual-ux-step-design.md`。本 change 不重复该文档的完整论证，只锁定正式规范、OpenSpec delta、运行时路由和治理追溯的实施边界。

## Goals / Non-Goals

**Goals**

- 形成“产品行为已定义 → 静态低保真 UX → 人工 approved → 直接开发 → 浏览器验证”的可执行链路。
- 让小文案、局部 token/间距和不改变任务/结构/状态/控制的低风险样式修复跳过可视 UX。
- 保留项目内组件复用，避免为一次变更提前抽象跨项目组件体系。

**Non-Goals**

- 通用 UX Kit、catalog、schema、renderer、交互原型、像素级回归平台。
- 新增正式项目、复制体验规则到计划/实现/验证、重写历史替换证据。

## Decisions

### 1. 体验设计是唯一语义 owner

触发条件、静态产物、人工批准、高保真升级以及组件选择与复用原则只在 `04-experience-design.md` 定义。下游仅检查输入、偏离或证据；`07-implementation.md` 的既有组件抽象规则只约束实现组织方式与 shared component 晋升阈值，不重新决定重复交互是否复用。

### 2. 静态仓库产物是默认

required change 使用一个权威 `ux/<change-id>/` 或项目既有等价目录，包含 `flow.md`、`wireframes/<surface>--<state>.html|svg` 和 `review.md`，其中 `<state>` 至少按适用范围覆盖 `success`、`loading`、`empty`、`error`。HTML/SVG 不含业务脚本、真实 API、数据写入或仓库外资源。

### 3. 人工 approved 阻断生产性实现

只有明确的人类决定可以产生 `approved`。沉默、一般授权、OpenSpec validation、AI 自检或已经写出代码都不能推断批准。批准后实质改变任务路径、结构、状态、权限含义或高风险确认时重新 review。

### 4. 组件复用停留在项目内

优先项目既有组件、设计 token、原生或成熟可访问组件；重复交互从第二个调用点起组合复用，feature-local 复用不受 shared component 晋升阈值阻止。只有同一项目至少 3 个真实调用点且语义稳定时才晋升跨 feature shared component，一次性业务结构不提前进入共享系统，也不得为达到阈值复制实现。

### 5. 历史来源账本只细化映射

8 个新 rule-id 分别细化既有 UX 触发、工件身份、人工判断、计划输入、实现回退和视觉证据来源。更新 `atomic-rules.csv` 与 `coverage-matrix.csv` 的 `target_rule_id`，不增加或伪造 W0–W9 原子行。

## Risks / Trade-offs

- 小改动被流程放大：用窄触发和 `not-required` 理由控制。
- 线框沦为事后附件：把人类批准放在生产性实现前。
- 下游复制产品定义：每个下游文件只保留一条门禁/一致性规则。
- 通用组件建设失控：明确至少两个真实项目出现重复证据后另立 change。
- 截图冒充功能验收：Browser E2E 仍是关键旅程证据，截图只核对视觉结构。

## Migration / Rollback

1. 先 strict validate 本 change。
2. 用失败测试固定 8 个新 rule-id 和 2321 总数。
3. 更新正式规范，再更新既有来源映射和 verifier。
4. 更新并同步运行时 skill。
5. 执行四个路由场景、完整测试、strict validation 和独立 final review。
6. 若成本过高，后续 Standard change 可把触发范围收窄到高风险交互并移除通用门禁，不删除已有历史证据。
