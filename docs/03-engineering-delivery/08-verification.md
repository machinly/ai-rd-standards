# 验证

> 本项目把实现结果转化为可定位、可复现、与风险相称的证据。本文只规定验证判断与证据；产品范围、技术方案、实现修复、发布动作和运行处置分别由其权威项目承接。

## 项目目的与边界

验证回答“用什么证据证明产品行为、技术约束和风险控制确实成立”。它适用于用户可见功能、服务、前端、数据变更、AI workflow、异步任务、外部集成及其发布前质量判断，也承接运行或评估阶段暴露出的补证据需求。

本项目不重写产品目标，不临时改变契约、安全、成本或信任边界，不在证据不足时以格式通过代替语义验收。验证推翻上游输入时，应返回相应权威项目；只有验证结论明确后，发布项目才接管真实环境变更。

## 根本原则

- **ITEM-VERIFICATION-001**：验证应使用最少、最快、最可信的测试保护最重要行为。

## 核心判断

执行验证时依次回答：

1. 目标行为与风险是什么，哪些旅程或边界不可破坏？
2. 所需证据属于 unit/component、host integration、dependency-container、complete local integration、Browser E2E、provider sandbox 还是生产观察？
3. 实际启动了什么、执行了什么、覆盖了什么，哪些内容仍未覆盖？
4. 失败、跳过、flaky、例外和证据过期如何影响结论，谁决定修复、降级、回滚、延期或接受风险？
5. 结果是否推翻定义、技术设计、AI 行为或实现输入，是否具备进入发布的真实证据？

## 重新组织后的规范要求

### 入口、路由与通用门禁

<!-- rule-id: VERIFY-PLANNING-GOVERNANCE-ROUTING-FP-W3-003-L009 -->
- 条件“选择 AI 行为专项时”成立时，应围绕“主入口回退”形成可核对结论：普通 AI 行为工作须先返回[技术设计](05-technical-design.md)，用户可见行为尚未定义时先返回[定义](../02-product-design/03-definition.md)。

<!-- rule-id: VERIFY-PLANNING-GOVERNANCE-ROUTING-FP-W4-001-L085 -->
- 条件“选择实现出口时”成立时，应围绕“发布路由”形成可核对结论：发布、上线、公开承诺或 rollback 计划须在“验证”通过后转交[发布](09-release.md)。

<!-- rule-id: VERIFY-PLANNING-GOVERNANCE-ROUTING-FP-W4-006-L023 -->
- 条件“迁移现有项目时”成立时，应围绕“模板基线迁移”形成可核对结论：现有手工项目只能通过明确重建或迁移计划转交模板基线。

<!-- rule-id: VERIFY-AUTH-TENANT-PERMISSION -->
- 条件“enqueue job 时”成立时，应围绕“tenant 校验”形成可核对结论：入队前须校验 tenant。

<!-- rule-id: VERIFY-LIVE-INCIDENT-RESPONSE-FP-W5-001-L105 -->
- 条件“选择验证出口时”成立时，应围绕“进入评估条件”形成可核对结论：线上质量、反馈或事故学习转交[评估](../04-operations-maintenance/11-evaluation.md)。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L003 -->
- 运行风险验证专项是可选 playbook，不是默认流程。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L007 -->
- 运行风险专项仅在当前验证命中至少一类范围时读取：性能预算；负载画像；benchmark；Web Vitals；DB 或 AI latency；容量；依赖失败；429、5xx 或 timeout；重试；dead letter；fallback；降级 UI。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L025 -->
- 条件“选择最小工件时”成立时，应围绕“工件按需边界”形成可核对结论：执行风险工件须按触发选择而非默认全量创建。

<!-- rule-id: VERIFY-PLANNING-GOVERNANCE-ROUTING-FP-W5-004-L056 -->
- 调整预算上限须由人决定，适用对象包括饱和度、quota、SLO、timeout、token、bundle、Core Web Vitals 以及 p95/p99。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L058 -->
- 接受性能回归、未知基线、跳过降级验证、扩大 blast radius 或带 gap 发布，必须由人决定。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L059 -->
- 计划显著增加云资源、数据库索引/缓存/CDN/队列、供应商优先级或模型成本，必须由人决定。

<!-- rule-id: VERIFY-PLANNING-GOVERNANCE-ROUTING-FP-W5-004-L060 -->
- 如要停用或降低下列防护，须交由人作出决定：timeout、rate limit、retry budget、circuit breaker、fallback、dead letter、人工审批。

<!-- rule-id: VERIFY-LIVE-INCIDENT-RESPONSE-FP-W7-004-L216 -->
- 条件“执行 `security-incidents/vulnerability-disclosure/<target>.md` 相关工作时”成立时，应围绕“运行触发专项：安全/隐私事故、漏洞披露与应急响应治理规范”形成可核对结论：早期一人公司允许先通过 GitHub Security Advisory、供应商平台或 CNA 协调。

### 测试组合、记录与证据层级

<!-- rule-id: VERIFY-EXPLORE-HUMAN-READABLE-FIXTURES -->
- 用户可见 Explore 使用 Alice、Bob、Admin 等人类可识别 fixture 和可理解业务结果；opaque ID、API success、DOM 存在或数据库行本身不能证明用户理解和完成任务。

<!-- rule-id: VERIFY-EXPLORE-SHOWCASE-BOUNDARY -->
- Showcase 必须复用实际产品入口和真实页面动作，不另建掩盖当前状态的静态展示站。它记录 observed behavior、visible fact、limits 和 next decision；只有满足完整 Browser E2E 契约时才可命名为 Browser E2E，也不得作为 Deliver accepted、release-ready 或 production-ready 证据。

<!-- rule-id: VERIFY-EVIDENCE-W0-001-L026 -->
- 条件“任务仅包含所列局部修复时”成立时，应围绕“intake 排除条件”形成可核对结论：纯链接、拼写、格式或局部测试修复通常不用 “选题”。

<!-- rule-id: VERIFY-EVIDENCE-W0-001-L065 -->
- 条件“高影响赌注缺乏充分证据时”成立时，应围绕“风险接受”形成可核对结论：接受证据不足的高影响赌注须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W1-001-L054 -->
- 条件“缺乏产品证据但决定继续时”成立时，应围绕“证据例外”形成可核对结论：无证据继续须显式留存风险。

<!-- rule-id: VERIFY-EVIDENCE-W1-001-L056 -->
- Explore 形成结果后，产品决策应基于证据选择 `validated`、`invalidated`、`revise`、`stopped` 或 `promote`；这些结论都不表示 Deliver accepted，结果可用后不得继续凭感觉推进。

<!-- rule-id: VERIFY-EVIDENCE-W1-001-L086 -->
- 条件“只需最小实现验证假设时”成立时，应围绕“调研出口”形成可核对结论：最小核验实现转交[实现](07-implementation.md)，且 scope 受 experiment 与 appetite 限制。

<!-- rule-id: VERIFY-EVIDENCE-W1-001-L087 -->
- 条件“需要上述验证证据时”成立时，应围绕“调研出口”形成可核对结论：需证明不伤害质量、成本、可靠性或信任时转交本验证项目。

<!-- rule-id: VERIFY-EVIDENCE-W1-002-L106 -->
- 条件“指标准备支持发布判断时”成立时，应围绕“指标门禁”形成可核对结论：没有事件依赖的指标禁止用于发布判断。

<!-- rule-id: VERIFY-EVIDENCE-W1-002-L205 -->
- 条件“准备开启自动采集时”成立时，应围绕“隐私门禁”形成可核对结论：开启自动采集前须通过 privacy review。

<!-- rule-id: VERIFY-EVIDENCE-W2-001-L017 -->
- 条件“编写技术设计规格时”成立时，应围绕“风险分层”形成可核对结论：区分实现前风险与后续验证或发布风险。

<!-- rule-id: VERIFY-EVIDENCE-W2-001-L018 -->
- 条件“编写技术设计规格时”成立时，应围绕“责任边界”形成可核对结论：区分由人决定与 Codex、skill、verifier、测试责任。

<!-- rule-id: VERIFY-EVIDENCE-W2-002-L209 -->
- 条件“执行低风险架构工件工作时”成立时，应围绕“执行责任”形成可核对结论：Codex 按默认值创建结构工件并由脚本核查。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L231 -->
- 检查契约工件时，字段完整性、路径存在性、章节、CI gate、AI schema 链接、敏感内容和 contract test 结构均交由 Codex 与 verifier 核查。

<!-- rule-id: VERIFY-EVIDENCE-W2-005-L015 -->
- 条件“使用供应商处理数据时”成立时，应围绕“供应商原则”形成可核对结论：供应商处理须有证据。

<!-- rule-id: VERIFY-QUALITY-GATE-W2-005-L068 -->
- 条件“license gate 失败时”成立时，应围绕“license gate”形成可核对结论：禁止通过删除 license 文件解决 license gate 失败。

<!-- rule-id: VERIFY-EVIDENCE-W3-001-L009 -->
- 条件“界定技术设计中的 AI 职责时”成立时，应围绕“技术设计与调研边界”形成可核对结论：技术设计中的 AI 行为方案禁止替代调研产品证据。

<!-- rule-id: VERIFY-EVIDENCE-W3-003-L066 -->
- 分项条件与结论：条件“改变失败样本时”下，删除现有失败样本须由人决定；条件“改变失败样本时”下，retire 现有失败样本须由人决定；条件“改变失败样本时”下，降权现有失败样本须由人决定；条件“改变安全评测定义时”下，改变 grader 须由人决定；条件“改变安全评测定义时”下，改变 threshold 须由人决定；条件“改变安全评测定义时”下，改变 safety boundary 须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W3-003-L068 -->
- 适用条件是“改变内容安全策略时”。须逐项满足：改变 moderation threshold 须由人决定；改变 enforcement action 须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W4-001-L053 -->
- 适用条件是“决定实现出口时”。须逐项满足：接受没有本地核验的实现转交下一步须由人决定；接受没有验证门禁证据的实现转交下一步须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W4-001-L084 -->
- 条件“选择实现出口时”成立时，应围绕“验证路由”形成可核对结论：证据不足、测试缺口或未核验风险须转交本验证项目。

<!-- rule-id: VERIFY-EVIDENCE-W4-001-L095 -->
- 条件“实施实现工作时”成立时，应围绕“验证失败处置”形成可核对结论：核验失败但方向仍正确时留在[实现](07-implementation.md)修复，或转交本验证项目判断。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L160 -->
- 条件“选择前端栈时”成立时，应围绕“框架例外门禁”形成可核对结论：不采用 React 和 TypeScript 须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L161 -->
- 条件“扩大前端架构时”成立时，应围绕“SSR 门禁”形成可核对结论：引入 SSR、强 SEO 或服务端渲染须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L164 -->
- 条件“改变产品视觉时”成立时，应围绕“品牌视觉门禁”形成可核对结论：公开新品牌视觉须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W4-005-L178 -->
- 条件“实现前端 flag 时”成立时，应围绕“后端重新授权”形成可核对结论：权限、计费和租户隔离须由后端再次核查。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L072 -->
- 适用条件是“处理失败测试时”。须逐项满足：无法解释的失败测试禁止删除或 skip；无法解释的失败测试须标记 needs-human 或 needs-more-tests。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L082 -->
- 条件“处理测试缺口时”成立时，应围绕“测试缺口门禁”形成可核对结论：接受删除失败测试、未解释 flaky 或高风险缺口须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W4-007-L055 -->
- 适用条件是“发送通知前”。须逐项满足：通知须核查 preference；通知须核查 consent；通知须核查 suppression；通知须核查 quiet hours；通知须核查 rate limit；通知须核查 idempotency。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-001-L007 -->
- 进入验证时，必须先以本规范确定范围，再由真实触发条件决定后续专项路由。

<!-- rule-id: VERIFY-EVIDENCE-PRINCIPLE-W5-001-L009 -->
- 实现准备进入发布或生产运行前，验证须判断实现是否具备足够的不伤害证据。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L025 -->
- 条件“验证暴露产品发现问题时”成立时，应围绕“调研路由”形成可核对结论：用户问题、指标或产品证据须回[调研](../01-initiation/02-research.md)。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L041 -->
- 分项条件与结论：条件“裁剪验证范围时”下，最小验证产出不要求无差别跑满全部门禁；条件“存在真实风险时”下，每个真实风险须有证据、解释或明确人工接受三者之一。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L053 -->
- 条件“使用真实 provider 或生产信号时”成立时，应围绕“真实环境证据边界”形成可核对结论：真实 provider sandbox 或生产观测须单独批准并留存边界。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L061 -->
- 普通测试文件命名、低风险 fixture、局部断言写法、无失败的 build/test 记录及低风险文案可访问性微调，默认不需要人作出决定。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L068 -->
- 条件“计划真实边界验证时”成立时，应围绕“真实环境验证门禁”形成可核对结论：在真实生产或付费边界做执行风险核验须由人决定。

<!-- rule-id: VERIFY-QUALITY-GATE-W5-001-L089 -->
- 条件“准备从验证进入发布时”成立时，应围绕“验证出口 gate”形成可核对结论：仅当满足验证出口条件方可能转交[发布](09-release.md)。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L092 -->
- 条件“存在较新负面证据时”成立时，应围绕“旧证据失效”形成可核对结论：较新的 changes_requested 或失败旅程须使旧完成摘要失效。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L094 -->
- 条件“验证结果影响前序输入时”成立时，应围绕“前序输入有效性”形成可核对结论：“技术设计”/“技术设计”的 AI 行为部分/“实现” 输入须未被推翻，否则先回退。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L100 -->
- 条件“选择验证出口时”成立时，应围绕“进入发布条件”形成可核对结论：核验通过且发布风险可解释时转交[发布](09-release.md)。





<!-- rule-id: VERIFY-TEST-QUALITY-GENERAL-W5-002-L003 -->
- 测试质量专项或运行风险验证专项与本规范的正式分类及项目原则冲突时，必须以正式规范为准。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L003 -->
- 条件“判断是否读取测试质量专项时”成立时，应围绕“专项流程定位”形成可核对结论：本专项须保持为按需选择 playbook 而非默认流程。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L007 -->
- 测试质量专项的读取前提是当前验证至少命中一类范围：测试策略；`test matrix`；`test run`；flaky；Go、Vite、sqlc 或 gRPC 门禁；AI eval；发布前质量证据。未命中时不得读取该专项。

<!-- rule-id: VERIFY-EVIDENCE-PRINCIPLE-W5-002-L013 -->
- 条件“设计测试策略时”成立时，应围绕“风险驱动测试原则”形成可核对结论：测试组合应以最少及最快、最可信方式保护最重要行为。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L040 -->
- 条件“判断临时代码验证时”成立时，应围绕“临时代码排除”形成可核对结论：一行以内及可人工确认且不进生产的临时代码不适用本专项。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L041 -->
- 条件“处理事故紧急缓解时”成立时，应围绕“事故例外与补证据”形成可核对结论：事故紧急缓解可不适用本专项，但事后须补回归测试或显式留存不补原因。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L042 -->
- 只更新文案或注释且不影响产品、权限、隐私、成本或发布时，不适用本专项。

<!-- rule-id: VERIFY-TEST-QUALITY-EVIDENCE-GATE-W5-002-L046 -->
- 条件“创建质量工件时”成立时，应围绕“target 命名一致性”形成可核对结论：同一 target 的质量工件须采用一致文件名。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L124 -->
- 适用条件是“处理 flaky 测试时”。须逐项满足：默认禁止长期依赖 retry；retry 只能作为短期隔离信号且禁止替代修复。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L140 -->
- 条件“运行 small tests 时”成立时，应围绕“small test 网络约束”形成可核对结论：small tests 禁止访问外部网络。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L142 -->
- 条件“运行 small tests 时”成立时，应围绕“small test 确定性”形成可核对结论：small tests 禁止采用 sleep。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L143 -->
- 条件“运行 small tests 时”成立时，应围绕“small test 敏感边界”形成可核对结论：small tests 禁止读取生产配置或 secret。

<!-- rule-id: VERIFY-EVIDENCE-PRINCIPLE-W5-002-L147 -->
- 条件“设计 medium tests 时”成立时，应围绕“medium test 目标”形成可核对结论：medium tests 须核验组件间真实交互。

<!-- rule-id: VERIFY-EVIDENCE-PRINCIPLE-W5-002-L159 -->
- 条件“设计 large tests 时”成立时，应围绕“large test 目标”形成可核对结论：large tests 须核验关键用户路径和发布配置。

<!-- rule-id: VERIFY-EVIDENCE-PRINCIPLE-W5-002-L169 -->
- 条件“设计 large tests 时”成立时，应围绕“large test 数量”形成可核对结论：large tests 数量须保持少量。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L185 -->
- 输入解析、URL、JSON、SQL filter、权限表达式或 prompt 模板变量发生变化时，须补 Go fuzz test，或留存不补的原因。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L203 -->
- 条件“发生视觉或响应式变化时”成立时，应围绕“视觉缺陷检查”形成可核对结论：视觉核验须核查文字重叠、按钮溢出和焦点丢失。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L205 -->
- 条件“记录局部浏览器检查时”成立时，应围绕“局部证据边界”形成可核对结论：DOM、焦点和错误提示核查只能标记为局部证据。

<!-- rule-id: VERIFY-EVIDENCE-PRINCIPLE-W5-002-L221 -->
- 条件“测试失败时”成立时，应围绕“失败默认处理”形成可核对结论：测试失败默认按真实问题处理并先复现定位。

<!-- rule-id: VERIFY-TEST-QUALITY-EVIDENCE-GATE-W5-002-L228 -->
- 条件“使用覆盖率时”成立时，应围绕“覆盖率边界”形成可核对结论：覆盖率只能作为风险提示且禁止作为唯一质量目标。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L233 -->
- 条件“提升覆盖率时”成立时，应围绕“无断言测试禁令”形成可核对结论：禁止为达到覆盖率百分比编写无断言测试。

<!-- rule-id: VERIFY-EVIDENCE-PRINCIPLE-W5-002-L234 -->
- 关键路径、权限、数据写入、成本限制或 AI 工具副作用的测试，优先级须高于整体代码行覆盖率。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L244 -->
- 条件“测试层级结论冲突时”成立时，应围绕“E2E 冲突人审”形成可核对结论：large E2E 失败但 small tests 通过时继续发布须由人判断。


<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-003-L223 -->
- 适用条件是“验证响应式界面时”。须逐项满足：移动端和桌面端都禁止出现文本溢出；移动端和桌面端都禁止出现按钮文字截断；移动端和桌面端都禁止出现控件重叠；移动端和桌面端都禁止出现不可点击目标。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L019 -->
- 形成运行风险结论时，QA 负责判断现有执行风险证据是否足以转交“发布”。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L043 -->
- 条件“执行验证或演练时”成立时，应围绕“stop conditions”形成可核对结论：stop conditions 须明确一人何时停止核验或演练。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L049 -->
- 生产压测、真实供应商压测、真实付费 AI 调用、使用真实客户数据或共享环境进行验证，都须经过人审。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L057 -->
- 在真实或共享边界执行 load/stress/fault injection 前须由人决定；这些边界包括 production、共享环境、客户流量、客户数据、供应商及付费 AI provider。

<!-- rule-id: VERIFY-EVIDENCE-W6-001-L029 -->
- 条件“出现验证问题时”成立时，应围绕“验证路由”形成可核对结论：上线前核验证据须回本验证项目。

<!-- rule-id: VERIFY-EVIDENCE-W6-001-L089 -->
- 条件“选择发布出口时”成立时，应围绕“回退验证”形成可核对结论：门禁失败或证据不足时回本验证项目。





<!-- rule-id: VERIFY-EVIDENCE-W6-003-L196 -->
- 条件“维护 customer acceptance gate 时”成立时，应围绕“customer acceptance 替代”形成可核对结论：customer_acceptance 须留存验收证据，或明确尚未验收且不可转生产/付费/公开引用。

<!-- rule-id: VERIFY-EVIDENCE-W7-001-L011 -->
- 条件“当前运行工作形成需要交由技术设计、实现、验证或发布处理的事项时”成立时，应围绕“运行核心入口”形成可核对结论：核验证据须返回本验证项目。

<!-- rule-id: VERIFY-EVIDENCE-W7-001-L055 -->
- 条件“决定是否接受未验证备份时”成立时，应围绕“未验证备份门禁”形成可核对结论：接受未核验备份须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W7-001-L081 -->
- 条件“执行进入评估或长期维护的出口工作时”成立时，应围绕“运行出口”形成可核对结论：需要补核验时返回本验证项目。





<!-- rule-id: VERIFY-EVIDENCE-W7-002-L019 -->
- 条件“执行‘本专项只解决什么’相关工作时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1”形成可核对结论：一人公司发布前后的安全核查。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L024 -->
- 条件“执行‘本专项只解决什么’相关工作时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1”形成可核对结论：SRE-lite skill 与本地核查脚本。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L216 -->
- 每周或每两周执行 SRE-lite review 时，须核查最近一次发布是否造成回滚、hotfix 或用户影响。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L217 -->
- 条件“执行 Toil 与每周运维复盘相关工作时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / Toil 与每周运维复盘”形成可核对结论：每周或每两周的 SRE-lite review 须核查哪个 page 是误报或不可行动。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L218 -->
- 条件“创建或维护 Toil 与每周运维复盘工件时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / Toil 与每周运维复盘”形成可核对结论：每周或每两周的 SRE-lite review 须核查哪个手动动作重复两次以上并应脚本化或写入 runbook。

<!-- rule-id: VERIFY-EVIDENCE-W7-003-L244 -->
- 绕过正常发布、权限、feature flag、审计、rate limit 或安全门禁的请求必须升级给人决定，不得由工具自行放行。

<!-- rule-id: VERIFY-EVIDENCE-W7-004-L253 -->
- 条件“执行 `security-incidents/post-incident-review/<target>.md` 相关工作时”成立时，应围绕“运行触发专项：安全/隐私事故、漏洞披露与应急响应治理规范”形成可核对结论：Action Items 最多 3 个，每个有 owner、due、核验方法。

<!-- rule-id: VERIFY-EVIDENCE-W8-001-L070 -->
- 条件“执行触发型评估专项时”成立时，应围绕“评估触发型专项”形成可核对结论：信号暴露核验缺口时返回本验证项目。





### 契约、数据与迁移

<!-- rule-id: VERIFY-DATA-QUALITY -->
- 只有当[调研](../01-initiation/02-research.md)明确需要产品事件、指标地图、实验分流、第三方 analytics、隐私 review 或数据质量复盘时，才读取本专项。事件名、属性、来源、destination、主指标、分流逻辑或隐私策略每次发生变化后，须复查数据质量。

<!-- rule-id: VERIFY-EVIDENCE-W1-002-L188 -->
- 分项条件与结论：条件“存在付费用户或真实实验时”下，有付费用户或真实实验时每周核查数据质量；条件“分析仅用于内测时”下，仅当内测时每两周核查数据质量。

<!-- rule-id: VERIFY-EVIDENCE-W1-002-L190 -->
- dashboard 支撑扩大实验范围、提高 AI 自主性、加大触达、关闭功能、定价或发布决策之前，须确认 data quality review 尚未过期。

<!-- rule-id: VERIFY-EVIDENCE-W1-002-L215 -->
- 条件“决定发布、定价、自主性、触达、默认模型或删功能时”成立时，应围绕“人工决策门禁”形成可核对结论：高影响产品决策须由人查看数据质量 review。

<!-- rule-id: VERIFY-AI-SIDE-EFFECT-AUTHORIZATION -->
- 条件“AI 输出将进入高影响副作用时”成立时，应围绕“输出校验”形成可核对结论：高影响输出执行前须经过 schema 校验。

<!-- rule-id: VERIFY-AI-EVAL-CHANGE-TRIGGERS -->
- 分项条件与结论：条件“改变 prompt 时”下，prompt 变化须执行对应 eval；条件“改变 model 时”下，model 变化须执行对应 eval；条件“改变 schema 时”下，schema 变化须执行对应 eval；条件“改变 tool 时”下，tool 变化须执行对应 eval。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L007 -->
- 条件“决定是否使用 AI safety 专项时”成立时，应围绕“专项进入条件”形成可核对结论：仅当 “技术设计”的 AI 行为部分 主入口触发 eval 数据、安全或 moderation 时方可采用本专项。

<!-- rule-id: VERIFY-EVIDENCE-W3-003-L065 -->
- 条件“选择 AI 数据时”成立时，应围绕“高风险数据门禁”形成可核对结论：采用真实、敏感或高影响数据须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L165 -->
- 条件“改变前端协议时”成立时，应围绕“gRPC-Web 门禁”形成可核对结论：接入 gRPC-Web 或 Connect 须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-CHECK-DATA-MIGRATION -->
- 条件“设计跨表关系时”成立时，应围绕“关系生命周期校验”形成可核对结论：无 foreign key 的跨表关系须有创建、更新和删除校验。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-004-L243 -->
- 条件“选择 AI 数据时”成立时，应围绕“真实用户数据 AI 门禁”形成可核对结论：AI 训练或 eval 采用真实用户数据须由人决定。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-006-L063 -->
- 条件“建立测试数据时”成立时，应围绕“真实用户数据禁令”形成可核对结论：seed 和 fixtures 禁止采用真实用户数据。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L026 -->
- 验证暴露契约、安全、权限、成本、供应商或信任边界问题时，须返回[技术设计](05-technical-design.md)。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L083 -->
- 条件“列举风险门禁失败时”成立时，应围绕“技术设计风险回退”形成可核对结论：安全、权限、隐私、供应链或契约门禁失败须回[技术设计](05-technical-design.md)。

<!-- rule-id: VERIFY-API-CONTRACT-ERROR-MODEL-FP-W5-001-L103 -->
- 条件“选择验证出口时”成立时，应围绕“回退技术设计条件”形成可核对结论：契约或风险边界需改变时回[技术设计](05-technical-design.md)。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L141 -->
- 条件“运行 small tests 时”成立时，应围绕“small test 数据库约束”形成可核对结论：small tests 禁止依赖真实数据库。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L151 -->
- 适用条件是“测试无外键数据模型时”。须逐项满足：无 foreign key 时 medium tests 默认涵盖引用校验；无 foreign key 数据访问 medium tests 默认涵盖并发写入；无 foreign key 数据访问 medium tests 默认涵盖删除；无 foreign key 数据访问 medium tests 默认涵盖孤儿数据检测。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L153 -->
- 适用条件是“测试 gRPC handler 时”。须逐项满足：gRPC medium tests 默认核验适用的 status code；gRPC medium tests 默认核验适用的 metadata；gRPC medium tests 默认核验适用的 deadline；gRPC medium tests 默认核验适用的 auth context。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L155 -->
- 适用条件是“测试 AI tool workflow 时”。须逐项满足：AI tool workflow medium tests 默认涵盖 dry-run；AI tool workflow medium tests 默认涵盖 schema；AI tool workflow medium tests 默认涵盖权限；AI tool workflow medium tests 默认涵盖错误路径。

<!-- rule-id: VERIFY-TEST-QUALITY-SCHEMA-DATA-W5-002-L186 -->
- 条件“生产 schema 兼容风险高时”成立时，应围绕“sqlc verify 替代关系”形成可核对结论：生产 schema 兼容风险高时须执行 sqlc verify 或留存跳过原因二者之一。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L187 -->
- 适用条件是“gRPC API 变化且该场景适用时”。须逐项满足：gRPC API 测试须涵盖适用的 成功；gRPC API 测试须涵盖适用的 权限失败；gRPC API 测试须涵盖适用的 validation 失败；gRPC API 测试须涵盖适用的 not found；gRPC API 测试须涵盖适用的 deadline/cancel。

<!-- rule-id: VERIFY-EVIDENCE-W6-002-L156 -->
- 条件“构建 production image 时”成立时，应围绕“runtime 测试数据”形成可核对结论：runtime image 禁止具备 测试数据。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-003-L304 -->
- 条件“启用客户数据进入 AI 前”成立时，应围绕“AI safety gate”形成可核对结论：客户数据转交 AI 前须有 eval、refusal 或 safety gate 中的适用控制。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-003-L305 -->
- 适用条件是“复用客户样例时”。须逐项满足：客户试点样例转交长期 eval/dataset 前须确认授权；客户试点样例转交长期 eval/dataset 前须确认脱敏；客户试点样例转交长期 eval/dataset 前须确认用途。

<!-- rule-id: VERIFY-API-CONTRACT-ERROR-MODEL-FP-W7-001-L011 -->
- 条件“当前运行工作形成需要交由技术设计、实现、验证或发布处理的事项时”成立时，应围绕“运行核心入口”形成可核对结论：契约、安全、成本、供应商或信任边界须返回[技术设计](05-technical-design.md)。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L259 -->
- 条件“执行发布检查时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / 风险边界：产品 / 工程 / 运维”形成可核对结论：发布核查的最低门禁须具备 migration 核查。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W7-004-L290 -->
- AI 相关事故分流必须显式判断是否存在 agent 工具越权、RAG/记忆泄露、训练或 eval 数据泄露、模型供应商数据事件以及安全 policy 绕过。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-003-L036 -->
- 条件“评估当前工作是否属于本文件的适用或排除范围时”成立时，应围绕“评估触发专项：AI 质量回归、线上质量事故与回滚规范 / 范围”形成可核对结论：用户反馈及 support ticket、产品指标、人工抽样、eval run、trace、schema parse failure、tool failure、fallback rate 触发的质量事故。

<!-- rule-id: VERIFY-AI-QUALITY-EVAL-FOLLOWUP -->
- 条件“执行 `ai-quality/regression-triage/<capability>.md` 相关工作时”成立时，应围绕“评估触发专项：AI 质量回归、线上质量事故与回滚规范”形成可核对结论：第 5 步再补 eval，把事故样例加入技术设计中的 AI eval 或 dataset，避免同类问题回归。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-003-L274 -->
- 事故样例是否沉淀进长期 eval/dataset，必须由人决定；样例包含客户内容、敏感数据或授权不清材料时，尤其需要明确批准。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W9-003-L112 -->
- 适用条件是“创建或维护“maintenance/update-policy/<target>.md”工件时”。须逐项满足：AI SDK、model route 或 eval dataset 维护须跑最小 eval；AI SDK、model route 或 eval dataset 维护须留存成本；AI SDK、model route 或 eval dataset 维护须留存质量；AI SDK、model route 或 eval dataset 维护须留存回退。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W9-003-L202 -->
- API、protobuf、schema、prompt 或 eval contract 的 breaking change 必须升级给人作引入决定。

### 用户旅程、前端与可访问性

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L162 -->
- 条件“扩大前端平台时”成立时，应围绕“前端平台门禁”形成可核对结论：引入大型 UI 库、复杂状态库或组件平台须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L163 -->
- 条件“引入前端第三方 SDK 时”成立时，应围绕“第三方 SDK 门禁”形成可核对结论：前端直接接入带成本或隐私风险的第三方 SDK 须由人决定。

<!-- rule-id: VERIFY-API-CONTRACT-ERROR-MODEL-FP-W5-001-L051 -->
- 条件“声称 Browser E2E 时”成立时，应围绕“Browser E2E 业务动作”形成可核对结论：Browser E2E 禁止用 API 替代场景业务动作。

<!-- rule-id: VERIFY-GOVERNANCE -->
- 条件“声称 Browser E2E 时”成立时，应围绕“Browser E2E 页面入口”形成可核对结论：Browser E2E 须从页面入口执行真实业务交互。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L051 -->
- Browser E2E 必须断言页面结果和必要最终业务状态。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L052 -->
- 条件“命名人工或局部浏览器证据时”成立时，应围绕“Browser E2E 命名边界”形成可核对结论：人工浏览器或局部 DOM/焦点/错误提示核查禁止称为 Browser E2E。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L055 -->
- 分项条件与结论：条件“命名集成证据时”下，仅在 Docker 中执行测试禁止自动命名为完整本地集成；条件“命名浏览器证据时”下，HTTP/gRPC integration 或人工浏览器核查禁止自动命名为 Browser E2E；条件“产品验收指定证据层级时”下，验收要求的证据层级须提供，否则明确标记未完成。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L091 -->
- 条件“关键旅程缺少 Browser E2E 时”成立时，应围绕“关键旅程验收边界”形成可核对结论：缺少关键旅程 Browser E2E 时禁止以人工接受风险标记 accepted。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L163 -->
- 适用条件是“验证完整集成时”。须逐项满足：large tests 默认从干净状态启动完整本地集成环境；完整本地集成须实际具备全部后端、前端、MySQL 和必要 mock/provider。

<!-- rule-id: VERIFY-API-CONTRACT-ERROR-MODEL-FP-W5-002-L164 -->
- 条件“执行 Playwright 关键路径时”成立时，应围绕“Playwright 业务动作”形成可核对结论：Playwright 关键路径须从页面入口执行真实动作且禁止用 API 替代业务动作。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L201 -->
- 条件“发生前端纯逻辑或状态变化时”成立时，应围绕“Vitest 触发”形成可核对结论：纯逻辑或组件状态变化须用 Vitest 核验。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L202 -->
- 用户关键路径、可访问性风险、导航、表单提交、支付前确认或文件上传下载发生变化时，须用 Playwright 验证。

<!-- rule-id: VERIFY-TEST-QUALITY-CONFIG-FLAG-W5-002-L205 -->
- Browser E2E 必须能从干净完整本地环境统一运行。

<!-- rule-id: VERIFY-TEST-QUALITY-GENERAL-W5-002-L205 -->
- 条件“声称 Browser E2E 时”成立时，应围绕“E2E 可重复性”形成可核对结论：Browser E2E 须是可重复浏览器自动化。

<!-- rule-id: VERIFY-TEST-QUALITY-RELEASE-ROLLBACK-W5-002-L205 -->
- 条件“关键旅程 Browser E2E 缺失时”成立时，应围绕“完成状态阻断”形成可核对结论：关键旅程缺少或跳过 Browser E2E 时禁止标记 accepted 或 release-ready。

<!-- rule-id: VERIFY-TEST-QUALITY-UX-FRONTEND-W5-002-L240 -->
- 条件“定义核心行为时”成立时，应围绕“核心行为人审”形成可核对结论：不可破坏的核心用户行为须由人判断。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L241 -->
- 条件“选择人工验收时”成立时，应围绕“人工验收边界”形成可核对结论：人只能决定哪些非关键风险接受手工验收，阻断完成的关键旅程禁止以人工核查替代 Browser E2E。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L007 -->
- UX 专项仅在当前验证至少涉及一类范围时读取：用户界面；关键交互；键盘或焦点；WCAG；AI disclosure；反馈纠错；降级状态；界面信任。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-003-L161 -->
- 条件“验证可访问性时”成立时，应围绕“自动化证据边界”形成可核对结论：自动化工具只能作为底线且禁止替代 keyboard-only 与人工 screen reader smoke。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-003-L162 -->
- 条件“裁剪可访问性验证时”成立时，应围绕“screen reader 最小化”形成可核对结论：早期一人公司不要求全屏幕阅读器矩阵。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L227 -->
- 呈现 AI workflow 时，界面必须明确区分 `user input`、`AI output`、`retrieved context`、`tool result` 与 `human-reviewed result`。

<!-- rule-id: VERIFY-ADMIN-ACTION-CONTROL -->
- 分项条件与结论：条件“执行“Vite 前端默认规则”相关工作时”下，服务端须重复校验；条件“执行 AI 写操作的服务端 precheck 时”下，AI 触发写操作须通过服务端 precheck；条件“执行 AI 写操作的 policy check 时”下，AI 触发写操作须通过 policy check；条件“批准 AI 触发的生产写操作时”下，AI 触发写操作须通过 human checkpoint。

### AI 行为、评测与安全

<!-- rule-id: VERIFY-WORKFLOW-GATE-W0-001-L080 -->
- 条件“验收 planning 扩展时”成立时，应围绕“验收边界”形成可核对结论：目录结构禁止作为 planning 验收条件。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W1-001-L009 -->
- 条件“使用调研时”成立时，应围绕“调研职责边界”形成可核对结论：[调研](../01-initiation/02-research.md)不可替代 AI eval。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W1-001-L033 -->
- 已明确复现和验收且不改变用户体验、成本、安全、权限或数据处理的小 bug fix，不适用“调研”。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W1-001-L085 -->
- 条件“用户可见 AI 行为发生变化时”成立时，应围绕“调研出口”形成可核对结论：先回[定义](../02-product-design/03-definition.md)明确用户可见行为，再由[技术设计](05-technical-design.md)补齐 eval、失败样例、安全边界和 fallback 方案。

<!-- rule-id: VERIFY-EVIDENCE-W1-002-L142 -->
- 条件“实验存在所列可信度问题时”成立时，应围绕“实验发布门禁”形成可核对结论：SRM、关键 guardrail 失败、埋点缺失或分配漂移时实验结果禁止用于发布判断。

<!-- rule-id: VERIFY-PRODUCT-ANALYTICS-EXPERIMENT-W1-002-L215 -->
- 条件“使用 AI 生成分析结论时”成立时，应围绕“AI 分析边界”形成可核对结论：AI 自动生成的分析结论只能作为 draft。

<!-- rule-id: VERIFY-EVIDENCE-W1-002-L228 -->
- 条件“检查分析工件的 expected-fail 行为时”成立时，应围绕“expected-fail 自动检查”形成可核对结论：expected-fail 行为的结构与一致性核查交给 Codex 与 verifier。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W2-001-L093 -->
- 条件“变更涉及用户可见 AI 行为时”成立时，应围绕“技术设计出口”形成可核对结论：用户可见 AI 行为边界变化时先回[定义](../02-product-design/03-definition.md)，再由[技术设计](05-technical-design.md)定义 eval、失败、红队与 fallback。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-001-L021 -->
- 适用条件是“推进用户可见 AI 能力时”。须逐项满足：没有最小 eval 禁止转交实现或发布；没有失败样例禁止转交实现或发布。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-001-L072 -->
- 分项条件与结论：条件“决定是否接受 AI 质量风险时”下，接受 eval 失败须由人决定；条件“决定是否接受 AI 数据风险时”下，接受 train/eval 泄漏风险须由人决定。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-001-L087 -->
- 条件“选择 AI 技术设计出口时”成立时，应围绕“实现进入条件”形成可核对结论：AI 行为、eval、失败样例、安全边界和 fallback 可执行后转交[实现](07-implementation.md)。

<!-- rule-id: VERIFY-AI-EVAL-PLAYBOOK-ROUTING -->
- 条件“决定是否采用该专项时”成立时，应围绕“专项可选性”形成可核对结论：prompt/eval 专项是按需选择 playbook，不是默认流程。

<!-- rule-id: VERIFY-AI-EVAL-BEFORE-IMPLEMENTATION -->
- 条件“实现用户可见 AI 能力前”成立时，应围绕“AI eval 先于实现”形成可核对结论：用户可见 AI 行为须先定义 eval 再实现模型调用、工具、结构化输出、trace 和安全边界。

<!-- rule-id: VERIFY-AI-EVAL-BEFORE-CHANGE -->
- 条件“改变 prompt 或 model 时”成立时，应围绕“eval fixture 前置”形成可核对结论：eval fixtures 须先于 prompt 或 model 改动落地。

<!-- rule-id: VERIFY-AI-EVAL-PLATFORM-DEPENDENCY -->
- 条件“选择 eval 存储和平台时”成立时，应围绕“旧平台依赖边界”形成可核对结论：旧 OpenAI Evals platform 禁止作为长期唯一依赖。

<!-- rule-id: VERIFY-AI-EVAL-MINIMUM-CASE-COUNT -->
- 条件“编写最小 eval cases 时”成立时，应围绕“case 数量下限”形成可核对结论：cases.jsonl 至少具备三条 case。

<!-- rule-id: VERIFY-AI-EVAL-FAILURE-DISCIPLINE -->
- 条件“处理 eval 失败时”成立时，应围绕“失败忽略禁令”形成可核对结论：禁止以模型偶然波动为由直接忽略 eval 失败。

<!-- rule-id: VERIFY-AI-EVAL-FAILURE-DISPOSITION -->
- 处理 eval 失败时，须分别留存接受或不接受、回滚或不回滚的决定。

<!-- rule-id: VERIFY-AI-EVALUATOR-OPTIMIZER-USE-CASE -->
- 条件“选择 AI workflow 层级时”成立时，应围绕“evaluator-optimizer 条件”形成可核对结论：需迭代优化且有明确评价标准时采用 evaluator-optimizer。

<!-- rule-id: VERIFY-AI-SAFETY-EVIDENCE-GATE -->
- 条件“评估 AI 风险控制时”成立时，应围绕“风险证据边界”形成可核对结论：禁止仅凭设计说明认定 AI 工具、隐私和注入风险已受控。

<!-- rule-id: VERIFY-AI-EVAL-EXPERIMENT-WAIVER -->
- 仅当用户明确说明该能力是内部一次性实验时，方可豁免本地 eval fixtures 与三样例前置要求。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L003 -->
- AI eval safety 专项与本规范的正式分类及项目原则冲突时，必须以正式规范为准。

<!-- rule-id: VERIFY-AI-EVAL-PLAYBOOK-OPTIONAL-W3-003-L003 -->
- AI eval safety 专项是可选 playbook，不是默认流程。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L015 -->
- 适用条件是“验证 AI 行为变化时”。须逐项满足：没有 rubric 禁止把 AI 行为变化视为已核验；没有失败样例禁止把 AI 行为变化视为已核验；没有安全样例禁止把 AI 行为变化视为已核验。

<!-- rule-id: VERIFY-EVIDENCE-W3-003-L015 -->
- 适用条件是“验证 AI 行为变化时”。须逐项满足：没有 provenance 禁止把 AI 行为变化视为已核验；没有 release decision 禁止把 AI 行为变化视为已核验。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L050 -->
- 条件“运行 AI release gate 时”成立时，应围绕“样本集合门禁”形成可核对结论：release gate 样本须属于 eval、canary 或 red_team。

<!-- rule-id: VERIFY-AI-MODEL-ROUTING-FP-W3-003-L057 -->
- 适用条件是“使用模型参与标注时”。须逐项满足：模型只能辅助初标；模型初标禁止直接成为 ground truth。

<!-- rule-id: VERIFY-SAFETY-REDTEAM-FP-W3-003-L059 -->
- 适用条件是“记录红队发现时”。须逐项满足：禁止保存完整可直接滥用 payload；优先保存脱敏或合成 proxy；红队留存须保留 finding id。

<!-- rule-id: VERIFY-AI-EVAL-SAFETY-W3-003-L061 -->
- 条件“评估 AI 安全结果时”成立时，应围绕“安全失败显性化”形成可核对结论：安全失败禁止被平均分掩盖。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L065 -->
- 条件“改变 eval 数据用途时”成立时，应围绕“eval 转训练门禁”形成可核对结论：将 eval case 移入训练、微调或蒸馏须由人决定。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L066 -->
- 条件“改变安全评测定义时”成立时，应围绕“rubric 变更门禁”形成可核对结论：改变 rubric 须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W3-003-L069 -->
- 适用条件是“决定安全材料披露时”。须逐项满足：保存或公开真实攻击 payload 须由人决定；保存或公开高危内容须由人决定；保存或公开红队结果须由人决定；保存或公开系统提示细节须由人决定；保存或公开供应商弱点须由人决定。

<!-- rule-id: VERIFY-AI-RAG-MEMORY -->
- 条件“决定是否使用 AI context 专项时”成立时，应围绕“专项进入条件”形成可核对结论：仅当 “技术设计”的 AI 行为部分 主入口触发 memory、RAG、引用或 grounding 时方可采用本专项。

<!-- rule-id: VERIFY-AI-CONTEXT-MEMORY-RETRIEVAL-W3-004-L052 -->
- 适用条件是“生成引用时”。须逐项满足：引用须可追溯到 source id；引用须可追溯到 version 或 date；引用须可追溯到可点击来源；禁止伪造 citation。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L017 -->
- 条件“改变生产模型、工具或数据边界时”成立时，应围绕“eval gate”形成可核对结论：生产 AI runtime 默认变化须有 eval gate。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L030 -->
- 条件“处理 prompt/eval 细节时”成立时，应围绕“AI eval 设计边界”形成可核对结论：本专项禁止替代[技术设计](05-technical-design.md)中的 AI prompt/eval 方案。

<!-- rule-id: VERIFY-EVIDENCE-W3-005-L240 -->
- 条件“接受 runtime 控制缺口时”成立时，应围绕“无测试门禁”形成可核对结论：接受没有测试的用户可见 AI 能力须由人决定。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-001-L027 -->
- 条件“判断实现适用范围时”成立时，应围绕“AI 技术设计回退”形成可核对结论：AI 行为、eval、红队、路由、权限、RAG 或记忆须返回[技术设计](05-technical-design.md)的 AI 行为部分。

<!-- rule-id: VERIFY-EVIDENCE-W4-001-L052 -->
- 条件“授权 AI coding 时”成立时，应围绕“失败测试门禁”形成可核对结论：允许 AI agent 删除或跳过失败测试须由人决定。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-001-L094 -->
- 条件“实施实现工作时”成立时，应围绕“AI 行为变化回退”形成可核对结论：prompt、eval、模型、工具、RAG、记忆或 AI 安全变化时返回[技术设计](05-technical-design.md)的 AI 行为部分。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-004-L204 -->
- 条件“构建 AI eval fixtures 时”成立时，应围绕“真实隐私样本禁令与例外”形成可核对结论：AI eval fixtures 禁止采用真实用户隐私样本，除非经过脱敏并留存依据。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-005-L187 -->
- 条件“登记 AI route flag 时”成立时，应围绕“AI eval linkage”形成可核对结论：AI model route flag 须转交 AI eval。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-005-L193 -->
- 条件“管理 AI 配置时”成立时，应围绕“AI 配置范围”形成可核对结论：model、temperature、max tokens、tool iteration、provider、prompt version、retrieval index 和 safety threshold 都须作为生产行为配置治理。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L055 -->
- 条件“裁剪 AI coding 工件时”成立时，应围绕“完整证据触发”形成可核对结论：若 AI coding 变更触及生产、数据、安全、AI 行为或发布流水线，必须保留完整证据。

<!-- rule-id: VERIFY-DEV-WORKSPACE-AI-CODING-W4-006-L065 -->
- 条件“执行 AI coding 批次时”成立时，应围绕“批次单一问题”形成可核对结论：batch log 每批只能回答一个 review 问题。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L003 -->
- 验证专项是可选 playbook，不是默认流程。

<!-- rule-id: VERIFY-MINIMAL-KERNEL-PRIORITY-W5-001-L003 -->
- 验证专项规则若与本规范的正式分类及项目原则不一致，正式规范具有优先效力。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L007 -->
- 条件“从验证核心入口选择专项时”成立时，应围绕“验证专项触发”形成可核对结论：专项只能按触发条件读取。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L011 -->
- 分项条件与结论：条件“验证推翻规格或风险边界时”下，规格或风险边界需改变时须回退 “技术设计” 而非在 “核验” 补写；条件“验证推翻 AI 行为时”下，AI 行为需改变时须按首次受影响决策回退：用户可见行为或输入回[定义](../02-product-design/03-definition.md)，交互与感知回[体验设计](../02-product-design/04-experience-design.md)，prompt、eval、模型、路由、RAG、工具或记忆方案回[技术设计](05-technical-design.md)，而非在 “核验” 重定义；条件“验证过程中出现发布承诺问题时”下，“核验” 禁止临时决定发布承诺。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L027 -->
- 条件“验证暴露 AI 定义问题时”成立时，应围绕“AI 定义路由”形成可核对结论：用户可见 AI 行为及其输入须回[定义](../02-product-design/03-definition.md)，模型、工具或 eval 方案缺口须回[技术设计](05-technical-design.md)。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L074 -->
- 条件“选择验证专项时”成立时，应围绕“专项按需读取”形成可核对结论：验证专项只能在触发条件出现时读取。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-001-L082 -->
- 条件“发现列举 AI 验证问题时”成立时，应围绕“AI 问题路由”形成可核对结论：AI 质量、安全拒绝或 eval 失败须回 “技术设计”的 AI 行为部分，必要时再转交 “评估”。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L096 -->
- 条件“准备进入发布时”成立时，应围绕“发布风险承接”形成可核对结论：发布风险须能由 release checklist、rollback path 和客户沟通承接。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-001-L102 -->
- 条件“选择验证出口时”成立时，应围绕“回退 AI 设计条件”形成可核对结论：用户可见 AI 行为需改变时回[定义](../02-product-design/03-definition.md)，eval 方案需改变时回[技术设计](05-technical-design.md)。



<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L215 -->
- 条件“使用自动 grader 时”成立时，应围绕“模型自评边界”形成可核对结论：AI eval 禁止仅依赖模型自评。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L217 -->
- 适用条件是“验证工具调用型 agent 时”。须逐项满足：工具调用型 agent 须测试错误工具；工具调用型 agent 须测试拒绝越权；工具调用型 agent 须测试超时；工具调用型 agent 须测试空结果；工具调用型 agent 须测试部分失败；工具调用型 agent 须测试人工审批路径。

<!-- rule-id: VERIFY-EVIDENCE-PRINCIPLE-W5-003-L013 -->
- 条件“设计或验证用户可见 surface 时”成立时，应围绕“surface 可回答性”形成可核对结论：每个用户可见 surface 须明确用户环境、关键任务、键盘、焦点、AI、纠错反馈和发布前核验。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L042 -->
- 设计 failure mode 验证时，必须覆盖最高影响的 1 至 3 个依赖；应按场景选择故障，包括 AI schema/tool/RAG failure、queue backlog、malformed response、429、5xx、timeout 和 latency。

<!-- rule-id: VERIFY-EVIDENCE-W6-001-L011 -->
- 分项条件与结论：条件“发布发现证据不足时”下，核验证据不足须回本验证项目而非在发布补测试；AI 行为证据不足也先回本验证项目，若同时暴露行为或 eval 方案缺口，再分别回[定义](../02-product-design/03-definition.md)或[技术设计](05-technical-design.md)。

<!-- rule-id: VERIFY-EVIDENCE-W6-001-L027 -->
- 出现 AI 行为、eval、红队、模型路由、工具权限或 RAG 证据问题时，须先由本验证项目区分证据缺口与设计缺口；证据缺口留在验证，设计缺口返回[技术设计](05-technical-design.md)，用户可见行为缺口返回[定义](../02-product-design/03-definition.md)。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-001-L092 -->
- 条件“选择发布出口时”成立时，应围绕“回退 AI 设计”形成可核对结论：需调整用户可见 AI 行为时回[定义](../02-product-design/03-definition.md)，需调整 eval 或模型路径时回[技术设计](05-technical-design.md)。



<!-- rule-id: VERIFY-WORKFLOW-GATE-W7-001-L011 -->
- 条件“当前运行工作形成需要交由技术设计、实现、验证或发布处理的事项时”成立时，应围绕“运行核心入口”形成可核对结论：发布决策须返回[发布](09-release.md)。







<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W7-002-L120 -->
- 条件“定义生产 AI 能力的 eval 或人工抽检质量信号时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / 监控与观测”形成可核对结论：eval pass rate 或人工抽检通过率。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-001-L045 -->
- 条件“判断该条列举的低风险事项是否需要升级给人时”成立时，应围绕“评估规范 / 人工判断点”形成可核对结论：普通反馈分类及低风险模板文案、Q-SEV3 eval case、无敏感内容的脱敏样本、低风险文档修正。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-001-L054 -->
- 是否将客户内容用于长期 eval、demo、训练、文档或公开材料，须由人决定。







<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-003-L015 -->
- 条件“定义 AI 产品质量可靠性原则时”成立时，应围绕“评估触发专项：AI 质量回归、线上质量事故与回滚规范 / 目标”形成可核对结论：默认原则：**AI 质量不是主观感觉，而是由用户任务成功率、eval 结果、生产信号与人工抽检共同定义的产品可靠性。**

<!-- rule-id: VERIFY-AI-QUALITY-REGRESSION-CASE -->
- 条件“处置已判定为 Q-SEV3 的质量问题时”成立时，应围绕“评估触发专项：AI 质量回归、线上质量事故与回滚规范 / `ai-quality/regression-triage/<capability>.md`”形成可核对结论：Q-SEV3 质量问题须补 regression case。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-003-L272 -->
- eval 失败、人工抽检失败或用户投诉持续存在时，是否仍然发布须由人决定。

<!-- rule-id: VERIFY-LIVE-INCIDENT-RESPONSE-FP-W8-003-L273 -->
- 为提升通过率而降低 safety/refusal/guardrail 阈值，须由人决定。











### 异步任务、管理动作与凭据

<!-- rule-id: VERIFY-ASYNC-JOB-WORKER-FP-W4-008-L173 -->
- 适用条件是“enqueue job 时”。须逐项满足：入队前须校验 actor；入队前须校验 job type；入队前须校验 payload schema；入队前须校验 dedupe key；入队前须校验 budget；入队前须校验 rate limit；入队前须校验用户可见状态。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W4-008-L273 -->
- 条件“接受 worker 控制缺口时”成立时，应围绕“worker 缺口门禁”形成可核对结论：缺少幂等、lease、max attempts、dead letter、graceful shutdown 或 stuck recovery 中任一项时，接受该 worker 控制缺口须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-002-L184 -->
- 并发、cache、goroutine、stream、worker、共享 map 或异步 agent loop 发生改动时，必须运行 `go test -race ./...`。

<!-- rule-id: VERIFY-EVIDENCE-W7-005-L171 -->
- 条件“执行 `credentials/rotation-plan/<target>.md` 相关工作时”成立时，应围绕“运行触发专项：凭据、密钥与服务账号生命周期规范”形成可核对结论：能双 key 或版本化的供应商，优先先创建新 key、部署新引用、核验流量、再撤旧 key。

<!-- rule-id: VERIFY-EVIDENCE-W7-005-L172 -->
- 条件“执行 `credentials/rotation-plan/<target>.md` 相关工作时”成立时，应围绕“运行触发专项：凭据、密钥与服务账号生命周期规范”形成可核对结论：不可双 key 的凭据须有健康核查。

<!-- rule-id: VERIFY-CREDENTIAL-ROTATION-VALIDATION-STEPS -->
- 分项条件与结论：条件“执行“credentials/rotation-plan/<target>.md”相关工作时”下，数据库密码须有明确核验步骤；条件“执行“credentials/rotation-plan/<target>.md”相关工作时”下，JWT signing key 须有明确核验步骤；条件“执行“credentials/rotation-plan/<target>.md”相关工作时”下，webhook signing secret 须有明确核验步骤；条件“执行“credentials/rotation-plan/<target>.md”相关工作时”下，TLS/private key 须有明确核验步骤；条件“实现或维护“credentials/rotation-plan/<target>.md”时”下，OpenAI key 须有明确核验步骤；条件“实现或维护“credentials/rotation-plan/<target>.md”时”下，CI deploy identity 须有明确核验步骤。

<!-- rule-id: VERIFY-CREDENTIAL-ROTATION-VALIDATION-EXCEPTION -->
- 条件“决定跳过 credential 轮换验证时”成立时，应围绕“轮换验证例外 checkpoint”形成可核对结论：跳过 credential 轮换核验须人工 checkpoint。

### 性能、韧性与恢复证据

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-001-L059 -->
- 分项条件与结论：条件“建立最小 eval 时”下，最小 eval 至少具备三条样例；条件“建立最小 eval 时”下，最小 eval 须有 happy path 样例；条件“建立最小 eval 时”下，最小 eval 须有边界或失败样例；条件“建立最小 eval 时”下，最小 eval 须有对抗或注入样例；条件“评测高风险 AI 能力时”下，高风险能力 eval 须具备安全样例；条件“评测高风险 AI 能力时”下，高风险能力 eval 须具备隐私样例；条件“评测高风险 AI 能力时”下，高风险能力 eval 须具备拒绝样例；条件“评测高风险 AI 能力时”下，高风险能力 eval 须具备降级样例；条件“评测高风险 AI 能力时”下，高风险能力 eval 须具备人工复核样例。

<!-- rule-id: VERIFY-EVIDENCE-W3-001-L088 -->
- 条件“选择技术设计出口时”成立时，应围绕“验证路由”形成可核对结论：需证明质量、安全、可访问性、性能或韧性时转交本验证项目。

<!-- rule-id: VERIFY-AI-CONTEXT-MEMORY-RETRIEVAL-W3-004-L051 -->
- 条件“上下文不可靠时”成立时，应围绕“上下文失败响应替代项”形成可核对结论：上下文低置信、过期、冲突、缺 citation 或来源不可信时，AI 可按情况选择降级、询问、说明不确定或拒答。

<!-- rule-id: VERIFY-EVIDENCE-W4-001-L028 -->
- 条件“判断实现适用范围时”成立时，应围绕“验证路由”形成可核对结论：上线前验收、性能、可访问性、韧性和安全门禁须转交本验证项目。

<!-- rule-id: VERIFY-BACKUP-RESTORE-RECOVERY-FP-W4-004-L214 -->
- 条件“评估备份时”成立时，应围绕“备份可用性 gate”形成可核对结论：没有恢复演练的备份禁止视为可用。

<!-- rule-id: VERIFY-EVIDENCE-W4-004-L242 -->
- 条件“选择备份能力时”成立时，应围绕“恢复成本门禁”形成可核对结论：用更高成本换数据恢复能力须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-NORM-W5-001-L050 -->
- 条件“声称 complete local integration 时”成立时，应围绕“完整本地集成”形成可核对结论：complete local integration 须由同一可重复入口启动、等待、smoke 和清理全部产品组件。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L067 -->
- 下列任一接受决定都必须由人作出：性能回归；未知基线；放宽 p95/p99；放宽 Core Web Vitals；放宽 bundle、AI token/latency 或容量预算。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-001-L069 -->
- 下列任一接受决定都必须由人作出：降级路径未验证；blast radius 扩大；自动 failover；自动供应商切换；弱化 timeout、retry 或 fallback。

<!-- rule-id: VERIFY-EVIDENCE-RISK-W5-002-L103 -->
- 条件“验收用户可见 target 时”成立时，应围绕“旅程不可替代边界”形成可核对结论：功能/API 清单或接口 smoke 禁止替代关键旅程矩阵。

<!-- rule-id: VERIFY-RETRY-FALLBACK-RESILIENCE-FP-W5-002-L222 -->
- 分项条件与结论：条件“处理 flaky 时”下，retry 只能用于降低临时噪音；条件“使用 retry 时”下，采用 retry 时须设置 Fix By。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L243 -->
- 条件“AI eval 失败时”成立时，应围绕“AI 失败处置选择”形成可核对结论：AI eval 失败后的修复、降级、回滚或人工兜底选择须由人判断。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L013 -->
- 适用条件是“准备上线时”。须逐项满足：执行风险门禁须判断预算、降级、停止和恢复；执行风险门禁须把 blast radius 控制在一人可处理范围。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L039 -->
- 适用条件是“验证 latency 时”。须逐项满足：latency 须至少留存 p95 或 p99 二者之一；latency 核验禁止只看平均值。

<!-- rule-id: VERIFY-PERFORMANCE-RESILIENCE-W5-004-L048 -->
- 缺少性能或韧性基线时，结论只能取 `pass_with_notes`、`needs_fix`、`needs-more-tests`；此时不得给出 `pass`。

<!-- rule-id: VERIFY-BACKUP-RESTORE-RECOVERY-FP-W5-004-L051 -->
- 条件“设计失败恢复时”成立时，应围绕“无限自救禁令”形成可核对结论：禁止出现无限 spinner、无限队列或无限 agent 自救。

<!-- rule-id: VERIFY-PERFORMANCE-RESILIENCE-W5-004-L052 -->
- 形成 `accepted_risk`、`defer-release`、`rollback` 中任一结论，或计划带性能/降级缺口发布时，必须经过人审。

<!-- rule-id: VERIFY-RESTORE-DRILL-EXECUTABLE-EVIDENCE -->
- 需要证明恢复路径可执行时，restore drill 必须产出足以证明该恢复路径可执行的证据；验证项目核对证据与结论，SRE-lite 演练和运行准备仍通过“运行”接口承接。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L126 -->
- 条件“执行恢复与基础设施提醒相关工作时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / 恢复与基础设施提醒”形成可核对结论：出现真实合同、付费关键数据、生产 IaC apply、跨区域恢复、客户证据或高风险资源销毁的计划性实现变更时，须保留核验证据。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L136 -->
- 每条告警须回答用户是否正在受影响。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L137 -->
- 每条告警须回答是否正在消耗 error budget。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L139 -->
- 每条告警须回答是否有指向处置第一步的 runbook。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L144 -->
- 条件“执行告警规范相关工作时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / 告警规范”形成可核对结论：低流量服务优先用黑盒探测和端到端 smoke test；避免少量样本造成误报。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L215 -->
- 条件“执行 Toil 与每周运维复盘相关工作时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / Toil 与每周运维复盘”形成可核对结论：每周或每两周的 SRE-lite review 须核查哪个 SLO 最近最接近预算耗尽。

### 对外声明与证据门禁

<!-- rule-id: VERIFY-EVIDENCE-W2-005-L061 -->
- 条件“强承诺缺乏证据时”成立时，应围绕“对外声明”形成可核对结论：没有证据的强承诺只能是 draft。

<!-- rule-id: VERIFY-EVIDENCE-W2-005-L069 -->
- 条件“编写 AI disclosure 时”成立时，应围绕“AI 声明”形成可核对结论：AI disclosure 禁止将供应商能力表述为产品已核验能力。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W5-001-L085 -->
- 条件“处理发布类事项时”成立时，应围绕“发布前置”形成可核对结论：发布窗口、回滚、客户上线或公开声明须在验证结论明确后转交[发布](09-release.md)。



<!-- rule-id: VERIFY-TEST-QUALITY-UX-FRONTEND-W5-002-L015 -->
- 分项条件与结论：条件“选择质量工件时”下，质量工件须按用户影响而非工作时长决定；条件“实现用户可见 Standard/High-risk 变更前”下，用户可见 Standard/High-risk 变更在实现前须说明关键旅程；条件“实现用户可见 Standard/High-risk 变更前”下，用户可见 Standard/High-risk 变更在实现前须说明保护行为。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L015 -->
- 缺少预算、基线、失败模式、降级证据或 go/no-go 决策时，不得声称性能或韧性可控。

<!-- rule-id: VERIFY-EVIDENCE-W6-001-L070 -->
- 形成审计证据包时，由本验证项目的长期证据主题判断是否需要证据索引或单独 change；知识入口和后续维护决定另由[评估](../04-operations-maintenance/11-evaluation.md)承接。

<!-- rule-id: VERIFY-EVIDENCE-W6-001-L071 -->
- 条件“发现 claim 边界证据不足时”成立时，应围绕“技术设计 claim 回退”形成可核对结论：信任、数据或供应商 claim 证据不足须回[技术设计](05-technical-design.md)。



<!-- rule-id: VERIFY-EVIDENCE-W6-003-L239 -->
- 条件“计划扩张或转付费时”成立时，应围绕“claim boundary link”形成可核对结论：Expansion / Conversion 须受 “发布” 对外声明证据专项约束。

<!-- rule-id: VERIFY-EVIDENCE-W6-003-L275 -->
- 条件“客户提出自定义功能、SLA、数据处理、公开背书或 roadmap 承诺时”成立时，应围绕“claim escalation”形成可核对结论：客户提出列举定制或承诺时须链接 “发布” 对外声明证据专项。

<!-- rule-id: VERIFY-EVIDENCE-W6-003-L307 -->
- 条件“AI 输出将对外使用时”成立时，应围绕“AI external claim gate”形成可核对结论：AI 输出用于客户公开材料、案例、承诺或建议时须走 “发布” 对外声明证据专项。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L015 -->
- 执行 claim gate 时，本专项不得替代技术设计中的信任政策、客户数据生命周期与供应商处理，验证中的证据保全，发布中的商业义务，或实现中的开发者文档。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-EVIDENCE-GATE -->
- 分项条件与结论：条件“claim 缺少证据时”下，无证据强声明只能保持 draft；条件“claim 证据过期时”下，证据过期的 claim 须选择降级、隐藏、改写或由人决定之一。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-GOVERNANCE-BOUNDARY -->
- 条件“执行 claim gate 时”成立时，应围绕“底层工件责任边界”形成可核对结论：底层工件本身不由本专项治理；本专项只做跨 surface 一致性与证据门禁。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L166 -->
- 条件“治理高风险 claim 时”成立时，应围绕“high-risk claim checkpoint”形成可核对结论：high risk 或涉及列举高风险 claim_type 时须人工 checkpoint。

<!-- rule-id: VERIFY-CLAIM-EVIDENCE-SOURCE-SAFETY -->
- 适用条件是“记录 claim evidence 时”。须逐项满足：claim 证据须优先引用事实源；claim evidence map 禁止复制敏感证据内容。

<!-- rule-id: VERIFY-CLAIM-CORRECTION-TRIGGER -->
- 条件“claim 失效时”成立时，应围绕“claim correction 顺序”形成可核对结论：发现 claim 错误、过期、证据失效、供应商政策变化或能力退化时，须先降级、隐藏或更正，再评估通知。

<!-- rule-id: VERIFY-CLAIM-EVIDENCE-PRESERVATION -->
- 适用条件是“保全 claim correction 证据时”。须逐项满足：证据保全只能保存链接及版本、hash、截图摘要或 release id 中的适用项；claim correction 证据禁止复制客户内容；claim correction 证据禁止复制 raw prompt 或 response。

<!-- rule-id: VERIFY-AI-CLAIM-EVIDENCE-GATE -->
- 发布 AI 能力 claim 时，必须至少连接一项适用证据；可选来源包括供应商官方边界、human review、RAG eval、tool/runtime guard、prompt version、model route、red-team/safety finding 与 eval。发布绝对化强 claim 时，除非证据、范围和例外均明确存在，否则禁止承诺绝对 AI、数据、合规或 SLA 说法。AI 扫描发现 claim 与证据冲突时，默认输出阻断结论与最低风险改写建议。

<!-- rule-id: VERIFY-CLAIM-EVIDENCE-GAP-CHECKPOINT -->
- 是否接受 claim 存在以下任一缺口，必须由人决定：证据不足；证据过期；供应商政策不清；系统能力不一致；无法复现。

### 跨项目工作流结构检查

<!-- rule-id: VERIFY-WORKFLOW-SINGLE-MAIN-ENTRY -->
- [验证](08-verification.md)、[发布](09-release.md)、[运行](../04-operations-maintenance/10-operation.md)和[评估](../04-operations-maintenance/11-evaluation.md)各自只能有一个 canonical 项目文档作为权威入口，检查时须确认不存在并列的第二入口；维护决定归评估、长期证明归验证，不得另立第十二项。

<!-- rule-id: VERIFY-WORKFLOW-SPECIALTY-TRIGGERED -->
- 上述项目中的专项主题只能按真实触发条件加载；若另有细化 playbook，必须声明其非主入口身份并回链 canonical 项目文档。

<!-- rule-id: VERIFY-WORKFLOW-NAVIGATION-CONSISTENCY -->
- 总入口、分类入口、相关项目引用和适用索引须共同指向同一个 canonical 项目文档；source map 只承担来源追溯，不能形成竞争导航。

<!-- rule-id: VERIFY-WORKFLOW-LEGACY-WRAPPER-ABSENCE -->
- 完成目录结构核验时，须确认没有未编号专项、`core-*` wrapper，也没有仅以旧阶段编号作为主身份的正文。

## 按主题整理的执行细则

### 工作流检查命令

<!-- rule-id: VERIFY-WORKFLOW-INDEX-COMMAND -->
- 四分类十一项正式目录的完整性必须由 `python tools/verify_rd_standards.py .` 提供机器证据；任何历史目录或历史索引校验都不得作为正式结构或新增第十二项的完成证据。

### 入口、路由与通用门禁

<!-- rule-id: VERIFY-EXPERIMENT-TRUSTWORTHINESS-CHECKS -->
- 条件“验证实验可信度时”成立时，应围绕“missing event check”形成可核对结论：trustworthiness checks 须具备 missing event check。

<!-- rule-id: VERIFY-PLANNING-GOVERNANCE-ROUTING-FP-W4-003-L152 -->
- 适用条件是“验收前端 change 时”。须逐项满足：关键页面须留存 LCP 目标或采集计划；关键页面须留存 INP 目标或采集计划；关键页面须留存 CLS 目标或采集计划。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L029 -->
- 条件“对应运行风险被触发时”成立时，应围绕“budget 工件”形成可核对结论：可按触发选择 budget 工件。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L032 -->
- 条件“对应运行风险被触发时”成立时，应围绕“verification plan 工件”形成可核对结论：可按触发选择 verification plan 工件。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L033 -->
- 条件“对应运行风险被触发时”成立时，应围绕“run report 工件”形成可核对结论：可按触发选择 run report 工件。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L034 -->
- 条件“对应运行风险被触发时”成立时，应围绕“degradation check 工件”形成可核对结论：可按触发选择 degradation check 工件。

<!-- rule-id: VERIFY-SRE-LITE-OPERATIONS-W7-002-L160 -->
- 条件“执行发布规范相关工作时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / 发布规范”形成可核对结论：高风险发布默认拆小。

### 测试组合、记录与证据层级

<!-- rule-id: VERIFY-EVIDENCE-W0-001-L037 -->
- 条件“创建 intake 最小记录时”成立时，应围绕“evidence”形成可核对结论：最小 intake 留存须具备证据。

<!-- rule-id: VERIFY-EVIDENCE-W2-001-L052 -->
- 条件“创建 OpenSpec change 时”成立时，应围绕“delta spec”形成可核对结论：delta spec 留存可核验 requirement 和 scenario 并采用 SHALL 或 MUST。

<!-- rule-id: VERIFY-EVIDENCE-W2-001-L054 -->
- 条件“创建 OpenSpec change 时”成立时，应围绕“tasks”形成可核对结论：tasks.md 提供可逐项完成和核验的 checklist。

<!-- rule-id: VERIFY-EVIDENCE-W2-001-L061 -->
- 条件“变更触发 Auth 专项时”成立时，应围绕“Auth 工件”形成可核对结论：Auth 触发时补充身份及策略、授权测试和审计工件。

<!-- rule-id: VERIFY-EVIDENCE-W2-002-L074 -->
- 条件“创建架构 boundary 时”成立时，应围绕“boundary purpose”形成可核对结论：boundary JSON 用于机器核查。

<!-- rule-id: VERIFY-EVIDENCE-W2-002-L118 -->
- 条件“创建依赖规则工件时”成立时，应围绕“dependency rules purpose”形成可核对结论：dependency rules 工件用于核查依赖方向。

<!-- rule-id: VERIFY-EVIDENCE-W4-001-L036 -->
- 条件“执行实现工作时”成立时，应围绕“最小验证结果”形成可核对结论：每个[实现](07-implementation.md)工作须留下最小核验结果。

<!-- rule-id: VERIFY-EVIDENCE-W4-001-L037 -->
- 条件“移交验证时”成立时，应围绕“测试输出证据”形成可核对结论：[实现](07-implementation.md)须为本验证项目留下测试输出。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L090 -->
- 条件“不使用 foreign key 时”成立时，应围绕“并发测试”形成可核对结论：无 foreign key 时须实现并发测试。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L109 -->
- 适用条件是“推进服务端 change 时”。须逐项满足：服务端 change 须补 usecase 单元测试；服务端 change 须补 repository 集成测试或可替代核验；服务端 change 须补 service 适配测试。

<!-- rule-id: VERIFY-SERVICE-QUALITY-GATE -->
- 条件“推进服务端 change 时”成立时，应围绕“质量门禁步骤”形成可核对结论：服务端 change 最后须跑质量门禁并更新 tasks。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L120 -->
- 条件“验证服务端 change 时”成立时，应围绕“go mod tidy 命令”形成可核对结论：合并或交付前须执行 go mod tidy。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L121 -->
- 条件“验证服务端 change 时”成立时，应围绕“gofmt 命令”形成可核对结论：合并或交付前须执行 gofmt -w .。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L122 -->
- 条件“验证服务端 change 时”成立时，应围绕“go test 命令”形成可核对结论：合并或交付前须执行 go test ./...。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L130 -->
- 条件“验证服务端 change 时”成立时，应围绕“make all 命令”形成可核对结论：采用 Kratos layout 或 Makefile 时须执行 make all。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L131 -->
- 条件“验证服务端 change 时”成立时，应围绕“make api 命令”形成可核对结论：采用 Kratos layout 或 Makefile 时须执行 make api。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L136 -->
- 适用条件是“验证服务端 change 时”。须逐项满足：Standard/High-risk 项目须执行项目证据 verifier；存在多个 cmd 时须启用 command registry 门禁。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L118 -->
- 适用条件是“实现深色主题时”。须逐项满足：深色主题须核查边框；深色主题须核查 hover 状态；深色主题须核查 focus 状态；深色主题须核查 disabled 状态；深色主题须核查 empty 状态；深色主题须核查 error 状态。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L144 -->
- 条件“验证前端 change 时”成立时，应围绕“包管理器替代命令”形成可核对结论：非 pnpm 项目须采用已有包管理器等价命令。

<!-- rule-id: VERIFY-EVIDENCE-W4-005-L209 -->
- 条件“创建配置工件时”成立时，应围绕“字段自动检查”形成可核对结论：配置工件字段须由 Codex 按模板创建并由脚本核查。

<!-- rule-id: VERIFY-EVIDENCE-W4-007-L038 -->
- 触发 integration test plan 工件时，计划默认存放于 `integrations/integration-test-plan/<target>.json`。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-001-L017 -->
- 发布前验证若涉及开发者接口、通知、计费、外部集成、后台任务、配置、数据迁移、公共 API、生产代码或用户可见功能，适用本项目。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-001-L018 -->
- 以下对象的测试与证据整理适用本项目：migration、webhook、worker、prompt/tool/model/RAG、AI workflow、Vite 前端及 Go/Kratos/sqlc/gRPC。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-001-L019 -->
- 本项目覆盖降级验证、韧性演练、性能回归、负载画像、性能预算、界面信任、AI UX 与可访问性。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-001-L020 -->
- 下列发布前记录属于本项目证据：fault-injection、benchmark、smoke、manual exploratory、flaky、accepted risk 及 test/eval run。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-001-L035 -->
- 条件“执行验证时”成立时，应围绕“验证范围”形成可核对结论：每个验证工作须留存本次变更的核验范围。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-001-L036 -->
- 条件“执行验证时”成立时，应围绕“实际运行证据”形成可核对结论：每个验证工作须留存适用的实际执行证据。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-001-L037 -->
- 条件“存在无法运行、暂不适用或待补验证时”成立时，应围绕“跳过项证据”形成可核对结论：每个跳过或不适用项须同时留存状态和原因。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-001-L039 -->
- 条件“验证需要下游承接时”成立时，应围绕“下游证据链接”形成可核对结论：每个验证工作须留下适用的发布、运行或评估证据链接。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-001-L045 -->
- 适用条件是“记录验证证据时”。须逐项满足：核验留存须写清命令；核验留存须写清执行环境；核验留存须写清实际启动组件；核验留存须写清涵盖路径；核验留存须写清结果；核验留存须写清未涵盖项。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-001-L047 -->
- 条件“命名 unit/component 证据时”成立时，应围绕“unit/component 层级”形成可核对结论：unit/component 证据须限定为单进程或局部模块。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-001-L048 -->
- 条件“命名 host integration 证据时”成立时，应围绕“host integration 层级”形成可核对结论：host integration 须表示宿主机应用进程连接真实或模拟依赖。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-001-L076 -->
- 出现通用测试策略、test matrix、test run、flaky，或 Go/Vite/sqlc/gRPC/AI eval 门禁事项时，必须进入测试质量专项。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-001-L091 -->
- 条件“准备进入发布时”成立时，应围绕“关键风险证据”形成可核对结论：转交[发布](09-release.md)前，关键用户路径、数据写入、权限、AI 行为、外部副作用和发布门禁六类风险须已有证据。



<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-002-L033 -->
- 条件“为后端设计验证时”成立时，应围绕“后端适用范围”形成可核对结论：后端服务适用本测试质量专项。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-002-L036 -->
- 数据迁移、权限、成本、安全或发布相关的高风险变更，适用本专项。

<!-- rule-id: VERIFY-FLAKY-TEST-RECORD -->
- 分项条件与结论：存在 quarantine、retry 或已知 flaky 时必须创建 flaky-tests 记录，没有 flaky 时可省略；记录必须包含 `Known Flakes`、`Impact`、`Quarantine Rule`、`Owner`、`Fix By` 和 `Release Risk`；创建记录时必须使用精确路径 `governance/quality/flaky-tests/<target>.md`。

<!-- rule-id: VERIFY-TEST-COMMAND-ENTRY-W5-002-L091 -->
- 适用条件是“维护 test matrix commands 条目时”。须逐项满足：commands 条目 须具备 name；commands 条目 须具备 command；commands 条目 须具备 tier；commands 条目 须具备 when。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-002-L130 -->
- 条件“设计 small tests 时”成立时，应围绕“small test 目标”形成可核对结论：small tests 的目标是最快发现逻辑回归。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-002-L134 -->
- 设计 Go small tests 时，默认范围完整覆盖 domain/usecase 函数、权限判断、错误映射与 config 解析。

<!-- rule-id: VERIFY-TEST-COMMAND-ENTRY-W5-002-L176 -->
- 条件“验证 Go 服务时”成立时，应围绕“Go test 命令”形成可核对结论：后端默认门禁具备 go test ./...。

<!-- rule-id: VERIFY-TEST-COMMAND-ENTRY-W5-002-L177 -->
- 条件“验证 Go 服务时”成立时，应围绕“Go race 命令”形成可核对结论：后端默认门禁具备 go test -race ./...。

<!-- rule-id: VERIFY-TEST-QUALITY-GENERAL-W5-002-L215 -->
- 条件“使用自动 grader 时”成立时，应围绕“grader 校准”形成可核对结论：自动 grader 须保留人类校准记录。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L142 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“standard geist_design_md”形成可核对结论：默认 standards 须至少具备 geist_design_md。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L146 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“check semantic_structure”形成可核对结论：默认 checks 须至少涵盖 semantic_structure。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L150 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“check contrast_light_dark”形成可核对结论：默认 checks 须至少涵盖 contrast_light_dark。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L151 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“check form_labels_errors”形成可核对结论：默认 checks 须至少涵盖 form_labels_errors。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L153 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“check reduced_motion”形成可核对结论：默认 checks 须至少涵盖 reduced_motion。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L154 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“check responsive_reflow”形成可核对结论：默认 checks 须至少涵盖 responsive_reflow。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L155 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“check touch_target_size”形成可核对结论：默认 checks 须至少涵盖 touch_target_size。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L156 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“check status_not_color_only”形成可核对结论：默认 checks 须至少涵盖 status_not_color_only。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L218 -->
- 适用条件是“实现 light/dark theme 时”。须逐项满足：Geist light/dark token 须分别核查 contrast；Geist light/dark token 须分别核查 focus；Geist light/dark token 须分别核查 hover；Geist light/dark token 须分别核查 disabled；Geist light/dark token 须分别核查 empty；Geist light/dark token 须分别核查 error。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L050 -->
- 条件“验证 provider 故障时”成立时，应围绕“provider 演练替代”形成可核对结论：真实 provider 故障演练默认采用 mock、recorded response、sandbox 或 staging 之一。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L064 -->
- 条件“最小化运行风险验证时”成立时，应围绕“最小安全验证”形成可核对结论：一人允许先为一个核心路径建立预算和一个失败模式核验，不必先搭完整平台。

<!-- rule-id: VERIFY-EVIDENCE-W6-001-L082 -->
- 条件“商业承诺进入运行前”成立时，应围绕“义务证据”形成可核对结论：商业承诺须有证据链接。



<!-- rule-id: VERIFY-QUALITY-GATE-W6-002-L125 -->
- 条件“维护 pipeline gates 时”成立时，应围绕“gate build”形成可核对结论：pipeline gates 须具备 build 类动作。

<!-- rule-id: VERIFY-EVIDENCE-W6-002-L138 -->
- 条件“存在相应供应链风险时”成立时，应围绕“dependency scan”形成可核对结论：依赖扫描或漏洞核查须按风险加入。

<!-- rule-id: VERIFY-EVIDENCE-W6-002-L168 -->
- 适用条件是“Vite production promote 后”。须逐项满足：production promote 后须核验 关键页面；production promote 后须核验 登录/支付/核心表单；production promote 后须核验 错误页；production promote 后须核验 静态资源。

<!-- rule-id: VERIFY-EVIDENCE-W6-002-L233 -->
- 条件“建设首条真实流水线时”成立时，应围绕“流水线辅助验证”形成可核对结论：首条真实流水线必须把 build、test、artifact、promote 与 rollback 约束写成可执行门禁，并由仓库核验命令检查。

<!-- rule-id: VERIFY-EVIDENCE-W6-003-L141 -->
- 条件“维护 integrations[] 时”成立时，应围绕“integrations[].test_plan”形成可核对结论：integrations[] 须具备 test_plan。

<!-- rule-id: VERIFY-EVIDENCE-W6-003-L299 -->
- 执行生产启用、数据导入、SSO、计费或 AI on customer data 时，须显示证据链接。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L251 -->
- 在第一个真实服务落地轻量运行保障时，应按照[运行](../04-operations-maintenance/10-operation.md)生成适用的 `ops/` 工件，并由仓库核验命令检查这些工件。

<!-- rule-id: VERIFY-EVIDENCE-W7-003-L241 -->
- 高风险管理动作若缺少 dry-run、rollback/compensate、审计字段或测试，任何继续执行的风险接受都必须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W7-004-L097 -->
- 条件“执行 `security-incidents/response-plan/<target>.md` 相关工作时”成立时，应围绕“运行触发专项：安全/隐私事故、漏洞披露与应急响应治理规范”形成可核对结论：保存稳定引用及 hash、trace id、request id、audit event id、时间线和最小且已脱敏（redacted）的证据。

<!-- rule-id: VERIFY-EVIDENCE-W7-004-L255 -->
- 条件“执行 `security-incidents/post-incident-review/<target>.md` 相关工作时”成立时，应围绕“运行触发专项：安全/隐私事故、漏洞披露与应急响应治理规范”形成可核对结论：复盘证据链接到本验证项目审计证据专项的 audit evidence，不复制敏感原文。

### 契约、数据与迁移

<!-- rule-id: VERIFY-EVIDENCE-W1-002-L171 -->
- data quality review 用于定期核查数据是否仍可信。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L058 -->
- 条件“change 触发契约专项时”成立时，应围绕“contract tests path”形成可核对结论：最小契约工件必须以 `contract-tests/<target>.json` 承载 contract test 计划。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L092 -->
- 条件“surface 稳定或有外部消费者时”成立时，应围绕“契约门禁”形成可核对结论：stable 或外部采用的 surface 须有 contract tests。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L153 -->
- 条件“创建 contract test plan 时”成立时，应围绕“contract target”形成可核对结论：contract test plan 须留存 target。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L154 -->
- 条件“创建 contract test plan 时”成立时，应围绕“contract owner”形成可核对结论：contract test plan 须留存 owner。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L155 -->
- 创建 contract test plan 时，必须保留机器字段 `compatibility_baseline`。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L156 -->
- 创建 contract test plan 时，必须保留机器字段 `test_suites`。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W2-003-L157 -->
- 创建 contract test plan 时，必须保留机器字段 `consumer_fixtures`。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L158 -->
- 创建 contract test plan 时，必须保留机器字段 `generated_clients`。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L159 -->
- 创建 contract test plan 时，必须保留机器字段 `ci_gates`。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L160 -->
- 创建 contract test plan 时，必须保留机器字段 `release_gates`。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W2-003-L161 -->
- 创建 contract test plan 时，必须保留机器字段 `ai_eval_links`。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L162 -->
- 创建 contract test plan 时，必须保留机器字段 `human_checkpoint`。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L166 -->
- 变更 Protobuf 时，必须运行 `buf breaking` 或等价检查。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L167 -->
- 条件“变更 gRPC handler 时”成立时，应围绕“contract gate”形成可核对结论：gRPC handler contract tests 涵盖成功和关键失败类型。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W2-003-L169 -->
- 条件“变更 AI tool schema 时”成立时，应围绕“contract gate”形成可核对结论：AI tool schema 变化须执行 eval 和 tool-call fixtures。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W2-003-L178 -->
- 定义 AI tool 或 structured output 契约时，必须保留机器字段 `eval_links`。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L210 -->
- 条件“这些类别影响用户路径时”成立时，应围绕“契约测试”形成可核对结论：错误及权限和空状态类别应纳入 contract tests。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W2-003-L215 -->
- 条件“prompt 演进影响所列行为时”成立时，应围绕“AI 契约验证”形成可核对结论：prompt 改变工具调用、输出、错误或 fallback 时须执行 eval。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-001-L017 -->
- 分项条件与结论：条件“改变 prompt 时”下，prompt 变化须由 eval 证明；条件“改变 schema 时”下，schema 变化须由 eval 证明；条件“改变 AI 工具时”下，工具变化须由 eval 证明；条件“改变模型时”下，模型变化须由 eval 证明；条件“改变 RAG 时”下，RAG 变化须由 eval 证明；条件“改变 AI 记忆时”下，记忆变化须由 eval 证明；条件“改变内容安全行为时”下，内容安全变化须由 eval 证明；条件“改变模型或工具路由时”下，路由变化须由 eval 证明。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-001-L052 -->
- 触发 eval 数据场景时，补充 `ai-data/` 工件。

<!-- rule-id: VERIFY-AI-EVAL-PLATFORM-SYNC -->
- 条件“需要平台评测时”成立时，应围绕“平台同步边界”形成可核对结论：仓库内 fixtures 按需选择同步到平台 datasets 或 traces。

<!-- rule-id: VERIFY-AI-EVAL-CASE-CONTRACT -->
- 分项条件与结论：每条 eval case 必须有稳定 `id` 和输入；eval set 至少包含一个枚举标签：`boundary`、`failure`、`adversarial` 或 `injection`。

<!-- rule-id: VERIFY-AI-SAFETY-TEST-COVERAGE -->
- 适用条件是“验证 AI 工具安全时”。须逐项满足：安全测试至少涵盖 prompt injection；安全测试至少涵盖越权工具调用；安全测试至少涵盖私密数据泄露；安全测试至少涵盖拒绝策略。

<!-- rule-id: VERIFY-AI-PROMPT-METADATA-SCRIPT-CHECK -->
- 条件“维护最小 AI 工件时”成立时，应围绕“prompt 元数据脚本检查”形成可核对结论：脚本须核查 prompt 元数据。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L029 -->
- 触发 eval 数据工件时，dataset card 的默认位置必须采用精确路径 `ai-data/dataset-card/<dataset>.md`。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L030 -->
- 触发 eval 数据工件时，eval set 的精确默认路径是 `ai-data/eval-set/<dataset>.jsonl`。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L031 -->
- 触发 eval 数据工件时，labeling guide 的精确默认路径是 `ai-data/labeling-guide/<dataset>.md`。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L032 -->
- 触发 eval 数据工件时，quality report 的精确默认路径是 `ai-data/quality-report/<dataset>.json`。

<!-- rule-id: VERIFY-AI-EVAL-SAFETY-W3-003-L051 -->
- 适用条件是“使用真实或外部数据作样本时”。须逐项满足：真实用户数据、raw AI 数据、客户内容或公开数据须留存 license 或 consent；真实用户数据、raw AI 数据、客户内容或公开数据须留存隐私分类；真实用户数据、raw AI 数据、客户内容或公开数据须留存用途。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L165 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval datasets 字段”形成可核对结论：eval gate 须具备 datasets。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L179 -->
- 适用条件是“改变 runtime route 时”。须逐项满足：默认模型变化前须跑对应 eval；供应商变化前须跑对应 eval；reasoning effort 变化前须跑对应 eval；工具能力变化前须跑对应 eval；structured output schema 变化前须跑对应 eval；fallback chain 变化前须跑对应 eval；context window 变化前须跑对应 eval；connector scope 变化前须跑对应 eval。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L226 -->
- 条件“评估不同模型时”成立时，应围绕“schema adherence 证据”形成可核对结论：不同模型的 schema adherence 须在 eval gate 单独留存。

<!-- rule-id: VERIFY-EVIDENCE-W3-005-L243 -->
- 适用条件是“验证 runtime 工件时”。须逐项满足：字段完整性交由 Codex 与 verifier 核对；章节完整性交由 Codex 与 verifier 核对；JSON 枚举交由 Codex 与 verifier 核对；schema 引用交由 Codex 与 verifier 核对；route 引用交由 Codex 与 verifier 核对；human checkpoint 涵盖交由 Codex 与 verifier 核对；敏感内容扫描由 Codex 与 verifier 执行；OpenSpec linkage 交由 Codex 与 verifier 核对。

<!-- rule-id: VERIFY-PLANNING-GOVERNANCE-ROUTING-FP-W4-002-L096 -->
- 条件“sqlc vet 暂不适用时”成立时，应围绕“sqlc vet 例外记录”形成可核对结论：暂不可配置 sqlc vet 时须在 tasks 留存原因和后续项。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L096 -->
- 条件“运行服务质量门禁时”成立时，应围绕“sqlc vet gate”形成可核对结论：配置 sqlc vet 后变更须通过 vet。

<!-- rule-id: VERIFY-API-CONTRACT-ERROR-MODEL-FP-W4-002-L103 -->
- 条件“推进服务端 change 时”成立时，应围绕“proto 定义步骤”形成可核对结论：服务端 change 须先定义 proto 请求、响应、service、错误和校验。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L123 -->
- 条件“验证服务端 change 时”成立时，应围绕“sqlc generate 命令”形成可核对结论：合并或交付前须执行 sqlc generate。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L124 -->
- 条件“验证服务端 change 时”成立时，应围绕“sqlc vet 命令”形成可核对结论：合并或交付前须执行 sqlc vet。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L134 -->
- 适用条件是“验证服务端 change 时”。须逐项满足：采用 Buf 或 protoc 时须执行对应生成命令；不可执行的命令须在 final summary 留存原因；不可执行的命令须在 tasks.md 留存原因。

<!-- rule-id: VERIFY-EVIDENCE-W4-002-L185 -->
- 条件“偏离已确认的服务数据默认时”成立时，应围绕“数据默认例外验证方式”形成可核对结论：偏离已确认的 MySQL、sqlc、无 ORM、通用 SQL 或无 foreign key 默认时须留存核验方式。

<!-- rule-id: VERIFY-API-CONTRACT-ERROR-MODEL-FP-W4-003-L043 -->
- 条件“实现前端 API 通信时”成立时，应围绕“HTTP BFF 默认”形成可核对结论：浏览器默认通过 HTTP 或 BFF 层访问后端。

<!-- rule-id: VERIFY-EVIDENCE-W4-004-L013 -->
- 条件“实施数据变更时”成立时，应围绕“发布前数据检查”形成可核对结论：全部数据变更须能在发布前被核查。

<!-- rule-id: VERIFY-EVIDENCE-W4-004-L076 -->
- 条件“实施生产数据变更时”成立时，应围绕“data change 事实源”形成可核对结论：data/changes JSON 须作为机器可核查的数据变更事实源。

<!-- rule-id: VERIFY-DATA-MIGRATION-W4-004-L106 -->
- 条件“记录数据变更时”成立时，应围绕“verification 字段”形成可核对结论：data change JSON 须具备 verification 配置块。

<!-- rule-id: VERIFY-BUILD-TYPECHECK-FP-W4-004-L136 -->
- 条件“同步 schema/query/code 时”成立时，应围绕“sqlc vet 步骤”形成可核对结论：sqlc generate 后须执行 sqlc vet。

<!-- rule-id: VERIFY-EVIDENCE-W4-004-L147 -->
- 条件“使用动态 SQL 时”成立时，应围绕“动态 SQL 测试”形成可核对结论：动态 SQL 须留存测试策略。

<!-- rule-id: VERIFY-EVIDENCE-W4-004-L148 -->
- 适用条件是“删除或重命名字段时”。须逐项满足：删除或重命名字段前须核查全部 query 消费者；删除或重命名字段前须核查全部 API 消费者；删除或重命名字段前须核查全部后台任务消费者；删除或重命名字段前须核查全部 AI prompt 或 schema 消费者；删除或重命名字段前须核查全部报表消费者；删除或重命名字段前须核查全部外部导出消费者。

<!-- rule-id: VERIFY-MIGRATION-BACKFILL-DATA-FIX-FP-W4-004-L189 -->
- 条件“执行生产数据修复时”成立时，应围绕“data fix Verification 字段”形成可核对结论：data fix 留存须具备 Verification。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-004-L201 -->
- 新增个人数据字段时，须说明该字段是否会进入日志、备份或 AI eval。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-006-L065 -->
- 条件“执行 AI coding 批次时”成立时，应围绕“产物分批”形成可核对结论：generated code、schema/proto、业务逻辑、UI、migration 和 eval fixture 应尽量分批。

<!-- rule-id: VERIFY-EVIDENCE-DETAIL-W5-002-L151 -->
- 条件“测试 sqlc 数据访问时”成立时，应围绕“sqlc 真实 schema”形成可核对结论：medium tests 默认核验 sqlc 对真实 MySQL schema 的读写。

<!-- rule-id: VERIFY-TEST-COMMAND-ENTRY-W5-002-L178 -->
- 条件“验证 sqlc 服务时”成立时，应围绕“sqlc generate 命令”形成可核对结论：后端默认门禁具备 sqlc generate。

<!-- rule-id: VERIFY-TEST-COMMAND-ENTRY-W5-002-L179 -->
- 条件“验证 sqlc 服务时”成立时，应围绕“sqlc vet 命令”形成可核对结论：后端默认门禁具备 sqlc vet。

<!-- rule-id: VERIFY-MIGRATION-BACKFILL-DATA-FIX-FP-W5-002-L186 -->
- 适用条件是“发生 migration 或 schema 变化时”。须逐项满足：migration 或 schema 变化须执行 sqlc generate；migration 或 schema 变化须执行 sqlc vet。

<!-- rule-id: VERIFY-GRPC-TEST-COVERAGE -->
- 条件“gRPC API 变化时”成立时，应围绕“gRPC 测试替代”形成可核对结论：gRPC API 变化须补 handler 或 bufconn 测试之一。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L214 -->
- 条件“验证 AI 变更时”成立时，应围绕“eval 数据证据”形成可核对结论：AI 变更须留存 eval dataset 或本地 fixtures 之一。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L224 -->
- 条件“测试存在列举不稳定依赖时”成立时，应围绕“可控 fixture 建议”形成可核对结论：依赖时间及随机数、网络、外部服务、共享数据库或全局状态的测试应优先改成可控 fixture。

<!-- rule-id: VERIFY-EVIDENCE-W6-002-L134 -->
- 适用条件是“执行发布静态检查时”。须逐项满足：静态核查须涵盖 格式；静态核查须涵盖 lint；静态核查须涵盖 sqlc vet；静态核查须涵盖 proto 生成一致性。

<!-- rule-id: VERIFY-EVIDENCE-W6-002-L136 -->
- 分项条件与结论：条件“存在并发或关键路径风险时”下，并发或关键路径风险测试默认执行 go test -race；条件“存在 schema migration 时”下，schema migration 风险测试须执行 dry-run。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-003-L106 -->
- 定义试点 AI Boundary 时，须说明客户数据是否用于 eval。

<!-- rule-id: VERIFY-EVIDENCE-W7-001-L038 -->
- 条件“执行运行最小产出相关工作时”成立时，应围绕“运行核心规范 / 最小产出”形成可核对结论：可定位证据包括 trace/log/metric/request id/audit event/rotation run/recovery drill 的引用，禁止保存 secret、完整个人数据或 raw prompt/response。

<!-- rule-id: VERIFY-EVIDENCE-W7-003-L217 -->
- 条件“执行 Go / Kratos / sqlc / gRPC 默认规则相关工作时”成立时，应围绕“运行触发专项：后台运营、人工操作与高风险动作规范”形成可核对结论：R2/R3/R4 需集成或回放测试。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-003-L035 -->
- 条件“执行范围相关工作时”成立时，应围绕“评估触发专项：AI 质量回归、线上质量事故与回滚规范 / 范围”形成可核对结论：prompt 及 model、route、schema、retrieval、reranker、tool、guardrail、memory、dataset、eval、feature flag 或供应商变化后的质量回归。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-003-L041 -->
- 适用条件是“执行“范围”相关工作时”。须逐项满足：prompt或eval fixture 的基础创建；prompt/eval fixture 的基础创建须转交 “技术设计”的 AI 行为部分 prompt/eval 和数据集专项。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-003-L256 -->
- 适用条件是“执行“AI workflow 默认规则”相关工作时”。须逐项满足：每次 prompt/model/route/retrieval/tool/schema 变化前后须比较基线样例；每次 prompt/model/route/retrieval/tool/schema 变化前后须比较事故样例；每次 prompt/model/route/retrieval/tool/schema 变化前后须比较现有线上高频任务样例。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W9-003-L041 -->
- 条件“执行范围相关工作时”成立时，应围绕“评估中的维护触发专项：依赖升级、技术债与弃用治理规范 / 范围”形成可核对结论：技术债及弃用接口、旧配置、旧 feature flag、旧 prompt/eval dataset。

<!-- rule-id: VERIFY-EVIDENCE-W9-003-L164 -->
- 条件“实现或维护 Go / Kratos / sqlc / gRPC 默认规则时”成立时，应围绕“评估中的维护触发专项：依赖升级、技术债与弃用治理规范”形成可核对结论：CI 须采用 go mod tidy 核查漂移。

### 用户旅程、前端与可访问性

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W2-003-L168 -->
- 条件“变更前端 client 或 BFF 时”成立时，应围绕“contract gate”形成可核对结论：前端 client 或 BFF 执行生成客户端或 schema fixture tests。

<!-- rule-id: VERIFY-EVIDENCE-W2-003-L209 -->
- 条件“升级前端 client schema 后”成立时，应围绕“前端契约验证”形成可核对结论：Vite client schema 升级后执行 build、typecheck、Vitest 和关键 Playwright smoke。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L137 -->
- 条件“验证前端 change 时”成立时，应围绕“install 命令”形成可核对结论：前端 change 默认执行 pnpm install。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L138 -->
- 条件“验证前端 change 时”成立时，应围绕“build 命令”形成可核对结论：前端 change 默认执行 pnpm build。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L139 -->
- 条件“验证前端 change 时”成立时，应围绕“test 命令”形成可核对结论：前端 change 默认执行 pnpm test。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L140 -->
- 条件“验证前端 change 时”成立时，应围绕“lint 命令”形成可核对结论：前端 change 默认执行 pnpm lint。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L141 -->
- 条件“验证前端 change 时”成立时，应围绕“preview 命令”形成可核对结论：前端 change 默认执行 pnpm preview。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L148 -->
- 条件“验收前端 change 时”成立时，应围绕“preview 验收”形成可核对结论：须用本地 vite preview 打开关键页面核验构建产物。

<!-- rule-id: VERIFY-VITE-VERCEL-FRONTEND-W4-003-L149 -->
- 条件“验收前端 change 时”成立时，应围绕“首屏视觉验收”形成可核对结论：首屏禁止有明显布局跳动、空白或不可读文字。

<!-- rule-id: VERIFY-EVIDENCE-W4-003-L150 -->
- 条件“验收前端 change 时”成立时，应围绕“关键路径证据”形成可核对结论：关键用户路径至少有一个 Vitest 测试或人工验收留存。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L028 -->
- 条件“建立本地集成环境时”成立时，应围绕“前端 dev server 边界”形成可核对结论：前端日常开发测试可采用宿主机 dev server。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L029 -->
- 条件“运行完整集成测试时”成立时，应围绕“双前端可访问”形成可核对结论：完整集成测试时两个前端须实际存在且可访问。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L070 -->
- 分项条件与结论：条件“验证 Go 项目时”下，Go 工作区 verify 须执行 go test ./...；条件“验证 Vite 项目时”下，Vite 工作区 verify 须执行 build。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-001-L051 -->
- Browser E2E 失败时必须保留 trace、截图或视频。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-002-L034 -->
- 条件“为前端设计验证时”成立时，应围绕“前端适用范围”形成可核对结论：Vite 前端和关键旅程适用本专项。

<!-- rule-id: VERIFY-TEST-STRATEGY -->
- 分项条件与结论：条件“适用质量专项时”下，生产服务、前端或用户可见 AI workflow 须维护 test strategy；条件“维护 test strategy 时”下，test strategy 须具备 Scope；条件“维护 test strategy 时”下，test strategy 须具备 Risk；条件“维护 test strategy 时”下，test strategy 须具备 Test Portfolio；条件“维护 test strategy 时”下，test strategy 须具备 Small Tests；条件“维护 test strategy 时”下，test strategy 须具备 Medium Tests；条件“维护 test strategy 时”下，test strategy 须具备 Large Tests；条件“维护 test strategy 时”下，test strategy 须具备 Flaky Policy；条件“维护 test strategy 时”下，test strategy 须具备 Commands；条件“维护 test strategy 时”下，test strategy 须具备 Human Checkpoints；条件“维护覆盖率策略时”下，测试策略须留存 coverage_focus。

<!-- rule-id: VERIFY-TEST-MATRIX -->
- 分项条件与结论：条件“适用质量专项时”下，生产服务、前端或用户可见 AI workflow 须维护 test matrix；条件“维护 test matrix 时”下，test matrix 须具备 target；条件“维护 test matrix 时”下，test matrix 须具备 owner；条件“维护 test matrix 时”下，test matrix 须具备 risk_level；条件“维护 test matrix 时”下，test matrix 须具备 stack；条件“维护 test matrix 时”下，test matrix 须具备 change_types；条件“维护 test matrix 时”下，test matrix 须具备 small_tests；条件“维护 test matrix 时”下，test matrix 须具备 medium_tests；条件“维护 test matrix 时”下，test matrix 须具备 large_tests；条件“维护 test matrix 时”下，test matrix 须具备 contract_tests；条件“维护 test matrix 时”下，test matrix 须具备 smoke_tests；条件“维护 test matrix 时”下，test matrix 须具备 commands；条件“维护 test matrix 时”下，test matrix 须具备 coverage_focus；条件“维护 test matrix 时”下，test matrix 须具备 flaky_policy；条件“维护 test matrix 时”下，test matrix 须具备 human_checkpoint；条件“维护 test matrix 时”下，test matrix 须具备 review_cadence。

<!-- rule-id: VERIFY-TEST-QUALITY-UX-FRONTEND-W5-002-L052 -->
- 条件“适用用户可见质量专项时”成立时，应围绕“user journeys 工件”形成可核对结论：用户可见 target 须维护关键用户旅程工件。

<!-- rule-id: VERIFY-TEST-RUN-RECORD -->
- 分项条件与结论：条件“适用质量专项时”下，生产服务、前端或用户可见 AI workflow 须维护 test runs；条件“运行关键测试时”下，test runs 须留存关键 test run。

<!-- rule-id: VERIFY-KEY-JOURNEY-EVIDENCE -->
- 分项条件与结论：条件“验证用户可见 Standard/High-risk target 时”下，用户可见 Standard/High-risk target 须定义少量阻断完成的关键旅程；条件“维护 用户旅程 时”下，用户旅程 须具备 evidence_level；条件“维护 用户旅程 时”下，用户旅程 须具备 evidence。

<!-- rule-id: VERIFY-TEST-QUALITY-UX-FRONTEND-W5-002-L097 -->
- 适用条件是“维护 用户旅程 时”。须逐项满足：用户旅程 须具备 id；用户旅程 须具备 role；用户旅程 须具备 goal。

<!-- rule-id: VERIFY-TEST-QUALITY-UX-FRONTEND-W5-002-L098 -->
- 适用条件是“维护 用户旅程 时”。须逐项满足：用户旅程 须具备 preconditions；用户旅程 须具备 真实页面 steps。

<!-- rule-id: VERIFY-TEST-QUALITY-UX-FRONTEND-W5-002-L099 -->
- 适用条件是“维护 用户旅程 时”。须逐项满足：用户旅程 须具备 success；用户旅程 须具备 failure。

<!-- rule-id: VERIFY-TEST-QUALITY-UX-FRONTEND-W5-002-L100 -->
- 条件“维护 用户旅程 时”成立时，应围绕“用户旅程.command”形成可核对结论：用户旅程 须具备 command。

<!-- rule-id: VERIFY-TEST-QUALITY-UX-FRONTEND-W5-002-L101 -->
- 适用条件是“维护 用户旅程 时”。须逐项满足：用户旅程 须具备 status；用户旅程 须具备 last_run_at。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-002-L136 -->
- 设计前端 small tests 时，默认范围完整覆盖纯函数、状态 reducer、格式化与表单校验。

<!-- rule-id: VERIFY-EVIDENCE-DETAIL-W5-002-L154 -->
- 条件“测试 Vite 组件时”成立时，应围绕“Vite 组件环境”形成可核对结论：Vite 组件交互默认在 Vitest browser mode 或等价环境核验。

<!-- rule-id: VERIFY-TEST-COMMAND-ENTRY-W5-002-L194 -->
- 条件“验证 Vite 前端时”成立时，应围绕“Vitest 命令”形成可核对结论：前端默认门禁须包含精确命令 `npm run test -- --run`。

<!-- rule-id: VERIFY-TEST-COMMAND-ENTRY-W5-002-L195 -->
- 条件“验证 Vite 前端时”成立时，应围绕“Vite build 命令”形成可核对结论：前端默认门禁须包含精确命令 `npm run build`。

<!-- rule-id: VERIFY-TEST-COMMAND-ENTRY-W5-002-L196 -->
- 条件“验证关键前端路径时”成立时，应围绕“Playwright 命令”形成可核对结论：前端默认门禁须包含精确命令 `npx playwright test`。

<!-- rule-id: VERIFY-VISUAL-REGRESSION-EVIDENCE -->
- 条件“发生视觉或响应式变化时”成立时，至少保存 desktop screenshot；只有 mobile 布局实质不同时才要求 mobile screenshot。可以增加 Playwright 视觉断言，但截图或视觉断言都不能替代从页面入口执行真实业务动作的 Browser E2E。

<!-- rule-id: VERIFY-VISUAL-UX-CONFORMANCE -->
- `visual_ux: required` 的 change 须在干净完整本地环境用 Browser E2E 证明关键旅程，并对照当前人类批准的 `flow.md` 与 wireframes 核对 desktop、适用的 mobile、loading、empty、error、success、keyboard-only、visible focus 和 focus order。任务路径、结构、状态、权限含义或高风险确认存在实质差异时，记录差异并返回体验设计重新 review；未完成前不得把该路径标为 accepted。

<!-- rule-id: VERIFY-BROWSER-E2E-EVIDENCE -->
- 由人工操控浏览器取得的证据，其类型必须记录为 `manual-browser-check`。


<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L015 -->
- 分项条件与结论：条件“验证关键用户路径时”下，关键用户路径须有可执行交互契约；条件“验证关键用户路径时”下，关键用户路径须有可访问性测试计划；条件“验证 AI 用户路径时”下，关键用户路径中的 AI 须有透明说明；条件“验证关键用户路径时”下，关键用户路径须有复盘留存。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-003-L034 -->
- 本专项覆盖 Vite / React / TypeScript 前端 surface，包括 AI 自动化确认页、AI 推荐、AI copilot、AI chat、命令面板、表格、菜单、弹层、工作台、设置页、仪表盘、表单和页面。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-003-L036 -->
- 验证前后端 UX contract 时，范围必须覆盖 Go/Kratos/gRPC 后端暴露给前端的 loading、error、empty、success 状态，以及错误码、权限状态、异步任务状态、AI 降级和用户反馈 API。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L054 -->
- 条件“适用本专项时”成立时，应围绕“UX review 工件”形成可核对结论：每个关键 surface 须维护 UX review。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L075 -->
- 维护 surface map 时，须记录 screen reader smoke 是否适用。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L125 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.surface”形成可核对结论：accessibility test plan 须具备 surface。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L126 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.owner”形成可核对结论：accessibility test plan 须具备 owner。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L127 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.standards”形成可核对结论：accessibility test plan 须具备 standards。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L128 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.tools”形成可核对结论：accessibility test plan 须具备 tools。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L129 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.checks”形成可核对结论：accessibility test plan 须具备 checks。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L130 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.viewports”形成可核对结论：accessibility test plan 须具备 viewports。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L131 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.assistive_tech”形成可核对结论：accessibility test plan 须具备 assistive_tech。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L132 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.gates”形成可核对结论：accessibility test plan 须具备 gates。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L133 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.exceptions”形成可核对结论：accessibility test plan 须具备 exceptions。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L134 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.evidence_refs”形成可核对结论：accessibility test plan 须具备 evidence_refs。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L135 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.human_checkpoint”形成可核对结论：accessibility test plan 须具备 human_checkpoint。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L136 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“accessibility test plan.status”形成可核对结论：accessibility test plan 须具备 status。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L162 -->
- 适用条件是“验证关键 surface 时”。须逐项满足：至少须保留一个桌面浏览器 keyboard pass 留存；至少须保留一个移动 viewport pass 留存；至少须保留一个 screen reader smoke 留存。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L185 -->
- 处理 AI 用户反馈时，反馈必须连接至少一个适用入口：[运行](../04-operations-maintenance/10-operation.md)中的支持路径、[评估](../04-operations-maintenance/11-evaluation.md)中的反馈学习、[技术设计](05-technical-design.md)中的 eval 或红队方案，或本验证项目的 UX review。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L191 -->
- 条件“维护 UX review 时”成立时，应围绕“UX review.Recent Changes”形成可核对结论：UX review 须具备 Recent Changes。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L192 -->
- 条件“维护 UX review 时”成立时，应围绕“UX review.Usability Findings”形成可核对结论：UX review 须具备 Usability Findings。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L194 -->
- 条件“维护 UX review 时”成立时，应围绕“UX review.AI Expectation Risks”形成可核对结论：UX review 须具备 AI Expectation Risks。

<!-- rule-id: VERIFY-OBSERVABILITY-SLO-ALERT -->
- 条件“维护 UX review 时”成立时，应围绕“UX review.Metrics / Feedback”形成可核对结论：UX review 须具备 Metrics / Feedback。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L196 -->
- 条件“维护 UX review 时”成立时，应围绕“UX review.Exceptions”形成可核对结论：UX review 须具备 Exceptions。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L197 -->
- 条件“维护 UX review 时”成立时，应围绕“UX review.Open Risks”形成可核对结论：UX review 须具备 Open Risks。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L198 -->
- 条件“维护 UX review 时”成立时，应围绕“UX review.Next One Change”形成可核对结论：UX review 须具备 Next One Change。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L202 -->
- 条件“pre-revenue 阶段”成立时，应围绕“pre-revenue review cadence”形成可核对结论：pre-revenue UX review 默认每月一次或关键 surface或AI interaction 发布前执行。

<!-- rule-id: VERIFY-ACCESSIBILITY-AI-UX-W5-003-L203 -->
- 有活跃用户时，UX review 默认每两周一次，或在每次改变关键任务、AI 输出呈现、用户控制、表单、导航、权限或计费路径前执行。

<!-- rule-id: VERIFY-AI-MODEL-ROUTING-FP-W5-004-L040 -->
- 条件“该前端指标适用时”成立时，应围绕“frontend route transition”形成可核对结论：前端在适用时须留存 route transition。

<!-- rule-id: VERIFY-API-CONTRACT-ERROR-MODEL-FP-W5-004-L040 -->
- 条件“该前端指标适用时”成立时，应围绕“frontend 关键 API 延迟”形成可核对结论：前端在适用时须留存 关键 API 延迟。

<!-- rule-id: VERIFY-OPERATIONAL-RISK-VERIFICATION-W5-004-L040 -->
- 适用条件是“该前端指标适用时”。须逐项满足：前端在适用时须留存 LCP；前端在适用时须留存 INP；前端在适用时须留存 CLS；前端在适用时须留存 bundle。

<!-- rule-id: VERIFY-BUILD-TYPECHECK-FP-W6-002-L137 -->
- 分项条件与结论：条件“构建 Go release 时”下，Go service build 默认产出容器镜像；条件“构建 Vite release 时”下，Vite build 默认产出 dist。

<!-- rule-id: VERIFY-QUALITY-GATE-W6-002-L164 -->
- 条件“构建 Vite release 时”成立时，应围绕“Vite build gate”形成可核对结论：Vite 前端 gate 须执行 npm run build。

<!-- rule-id: VERIFY-EVIDENCE-W6-002-L165 -->
- 条件“验证 Vite release 时”成立时，应围绕“frontend tests by risk”形成可核对结论：Vitest、component 或 accessibility smoke 须按项目风险执行适用项。

<!-- rule-id: VERIFY-EVIDENCE-W7-004-L268 -->
- 条件“执行 Vite 前端默认规则相关工作时”成立时，应围绕“运行触发专项：安全/隐私事故、漏洞披露与应急响应治理规范 / Vite 前端默认规则”形成可核对结论：详细证据留在后端和 audit evidence。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W7-005-L288 -->
- 凭据暴露审查必须涵盖 Vite/browser/mobile、公开 docs、support transcript、logs、prompt、eval 与 RAG source；任何把值送入这些表面的决定都需人工处置。

<!-- rule-id: VERIFY-BUILD-TYPECHECK-FP-W9-003-L176 -->
- 适用条件是“实现或维护“Vite / npm 默认规则”时”。须逐项满足：前端依赖升级后至少执行 typecheck；前端依赖升级后至少执行 build。

<!-- rule-id: VERIFY-EVIDENCE-W9-003-L176 -->
- 适用条件是“实现或维护“Vite / npm 默认规则”时”。须逐项满足：前端依赖升级后至少执行 unit tests；前端依赖升级后至少执行关键 Playwright smoke；前端依赖升级后至少执行视觉核查；前端依赖升级后至少执行可访问性核查。

### AI 行为、评测与安全

<!-- rule-id: VERIFY-EVIDENCE-W1-002-L140 -->
- 适用条件是“验证实验可信度时”。须逐项满足：trustworthiness checks 须具备 instrumentation check；trustworthiness checks 须具备 sample ratio mismatch check；trustworthiness checks 须具备 guardrail check；trustworthiness checks 须具备 bot/internal traffic exclusion。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W1-002-L214 -->
- 不能只依据 token 用量或用户点击判断 AI 质量；质量指标必须同时连接 eval 版本与产品事件。

<!-- rule-id: VERIFY-AI-PROMPT-ARTIFACT-FP-W2-002-L216 -->
- 条件“组织 prompt 时”成立时，应围绕“默认取舍”形成可核对结论：prompt builder 默认靠近 feature 且不转交全局 prompt 仓库。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-001-L016 -->
- 适用条件是“定义 AI capability 样本时”。须逐项满足：eval 样本须涵盖 happy path；eval 样本须涵盖边界场景；eval 样本须涵盖失败场景；eval 样本须涵盖对抗场景；eval 样本须涵盖隐私场景；eval 样本须涵盖安全场景；eval 样本须涵盖低置信场景；eval 样本须涵盖多语言场景。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-001-L045 -->
- 条件“定义最小 AI 工件时”成立时，应围绕“eval cases 路径”形成可核对结论：每个用户可见 AI capability 须有 cases.jsonl。

<!-- rule-id: VERIFY-AI-RUNBOOK-EVIDENCE -->
- 条件“定义最小 AI 工件时”成立时，应围绕“eval runbook 路径”形成可核对结论：每个用户可见 AI capability 须有 runbook.md。

<!-- rule-id: VERIFY-SAFETY-REDTEAM-FP-W3-001-L052 -->
- 触发红队或发布安全场景时，补充 `ai-safety/` 工件。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-001-L080 -->
- 条件“规划模型优化时”成立时，应围绕“模型优化 baseline eval”形成可核对结论：模型优化前先确认 baseline eval。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-LOCATION -->
- 分项条件与结论：选择 eval 事实源时默认采用仓库内 fixtures；建立 AI artifact 时，eval cases、rubric、runbook 分别落在 `ai/evals/<capability>/cases.jsonl`、`ai/evals/<capability>/rubric.md`、`ai/evals/<capability>/runbook.md`。

<!-- rule-id: VERIFY-AI-EVAL-CASE-COVERAGE -->
- 适用条件是“编写最小 eval cases 时”。须逐项满足：cases.jsonl 须具备 happy path；cases.jsonl 须具备边界或失败 case；cases.jsonl 须具备对抗或 prompt injection case。

<!-- rule-id: VERIFY-AI-EVAL-RUNBOOK -->
- 适用条件是“编写 eval runbook 时”。须逐项满足：runbook.md 须说明如何执行 eval；runbook.md 须说明如何留存结果；runbook.md 须说明失败时如何回滚。

<!-- rule-id: VERIFY-AI-CHANGE-HUMAN-SAMPLE-REVIEW -->
- 条件“实现 AI change 后”成立时，应围绕“人工抽样 review”形成可核对结论：AI change 须进行人工抽样 review。

<!-- rule-id: VERIFY-AI-EVAL-EXECUTION-GATE -->
- 分项条件与结论：条件“实现 AI change 后”下，AI change 须执行本地 eval；条件“决定是否升级 agent 时”下，仅当 eval 证明收益时方可升级 agent；条件“升级 AI workflow 时”下，升级 workflow 层级须有 eval 或 trace 证明不足；条件“AI 能力上线时”下，上线 AI 能力须有 eval pass rate 或人工抽检通过率。

<!-- rule-id: VERIFY-AI-PROMPT-ARTIFACT-FP-W3-002-L090 -->
- 条件“编写 prompt 示例时”成立时，应围绕“边界示例”形成可核对结论：prompt 示例须涵盖边界情况。

<!-- rule-id: VERIFY-AI-PROMPT-CHANGE-EVAL-LINK -->
- 条件“改变 prompt 时”成立时，应围绕“prompt eval 链接”形成可核对结论：prompt 改动须说明关联 eval case。

<!-- rule-id: VERIFY-AI-EVAL-CASE-OPTIONAL-FIELDS -->
- 适用条件是“设计 eval case schema 时”。须逐项满足：cases.jsonl 推荐具备 id 字段；cases.jsonl 推荐具备 input 字段；cases.jsonl 推荐具备 criteria 字段；cases.jsonl 推荐具备 tags 字段；cases.jsonl 推荐具备 expected_shape 字段。

<!-- rule-id: VERIFY-AI-EVAL-FAILURE-RECORD -->
- 条件“处理 eval 失败时”成立时，应围绕“失败原因记录”形成可核对结论：eval 失败须留存原因。

<!-- rule-id: VERIFY-AI-EVAL-HISTORY-RECORD -->
- 适用条件是“维护重要 AI 能力时”。须逐项满足：重要能力历史结果须留存日期；重要能力历史结果须留存 commit；重要能力历史结果须留存 prompt version；重要能力历史结果须留存 model；重要能力历史结果须留存通过率；重要能力历史结果须留存人工备注。

<!-- rule-id: VERIFY-AI-EVAL-TAG-NAMING -->
- 条件“实施低风险 AI change 时”成立时，应围绕“eval tags 自主权”形成可核对结论：局部 eval tags 默认无需由人决定。

<!-- rule-id: VERIFY-AI-EVAL-SCRIPT-CHECK -->
- 适用条件是“维护最小 AI 工件时”。须逐项满足：脚本须核查最低 eval 样例数；脚本须核查边界样例。

<!-- rule-id: VERIFY-AI-ABUSE-CASE-RELEASE-MITIGATION -->
- 分项条件与结论：触发 AI safety 工件时，滥用用例登记默认位于 `ai-safety/abuse-case-register/<capability>.json`；记录 high/critical abuse case 时，必须同时给出 mitigation、owner 和 release decision。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L036 -->
- 触发 AI safety 工件时，adversarial cases 的精确默认路径是 `ai-safety/adversarial-cases/<capability>.jsonl`。

<!-- rule-id: VERIFY-AI-EVAL-SAFETY-W3-003-L037 -->
- 触发 AI safety 工件时，mitigation map 的精确默认路径是 `ai-safety/mitigation-map/<capability>.md`。

<!-- rule-id: VERIFY-AI-EVAL-SAFETY-W3-003-L038 -->
- 触发 AI safety 工件时，safety release review 的精确默认路径是 `ai-safety/safety-release-review/<capability>.md`。

<!-- rule-id: VERIFY-AI-EVAL-SAFETY-W3-003-L042 -->
- 触发内容安全工件时，moderation rules 的精确默认路径是 `content-safety/moderation-rules/<surface>.json`。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L049 -->
- 适用条件是“建立 eval set 时”。须逐项满足：eval set 至少具备 happy path；eval set 至少具备边界或失败样例；eval set 至少具备对抗或注入样例。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L052 -->
- 条件“记录 high/critical abuse case 时”成立时，应围绕“abuse eval ref 字段”形成可核对结论：high/critical abuse case 须有 eval ref。

<!-- rule-id: VERIFY-AI-EVAL-SAFETY-W3-003-L053 -->
- 条件“实施自动化 enforcement 时”成立时，应围绕“enforcement audit”形成可核对结论：自动化 enforcement 超过标注或复核时须有 audit。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L058 -->
- 条件“发现具有回归价值时”成立时，应围绕“红队样本回流”形成可核对结论：高价值红队发现须转成稳定 eval case。

<!-- rule-id: VERIFY-SAFETY-REDTEAM-FP-W3-003-L058 -->
- 处理红队发现时，须先将发现登记到 `ai-safety/`。

<!-- rule-id: VERIFY-AI-EVAL-SAFETY-W3-003-L060 -->
- 适用条件是“设计内容审核时”。须逐项满足：内容审核须有 policy；内容审核须有 rules；内容审核须有 review。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-003-L077 -->
- 条件“执行最小安全下一步时”成立时，应围绕“eval version 链接”形成可核对结论：每个 AI 行为 change 须链接 eval version。

<!-- rule-id: VERIFY-AI-EVAL-SAFETY-W3-003-L077 -->
- 条件“执行最小安全下一步时”成立时，应围绕“safety decision 链接”形成可核对结论：每个 AI 行为 change 须链接 safety release decision。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-004-L033 -->
- 触发上下文治理工件时，retrieval policy 的精确默认路径是 `ai-context/retrieval-policy/<capability>.json`。

<!-- rule-id: VERIFY-AI-CONTEXT-MEMORY-RETRIEVAL-W3-004-L034 -->
- 触发上下文治理工件时，citation grounding 的精确默认路径是 `ai-context/citation-grounding/<capability>.md`。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-004-L042 -->
- 适用条件是“定义检索策略时”。须逐项满足：retrieval policy 须留存 tenant scope filter；retrieval policy 须留存 user scope filter；retrieval policy 须留存 source allowlist；retrieval policy 须留存 max results；retrieval policy 须留存 max tokens；retrieval policy 须留存 score threshold；retrieval policy 须留存 citation policy；retrieval policy 须留存 fallback。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L045 -->
- 为生产 AI capability 建立 runtime 工件时，eval gate 的精确默认路径是 `ai-runtime/eval-gate/<capability>.json`。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L070 -->
- 条件“定义生产 route 时”成立时，应围绕“eval date 字段”形成可核对结论：生产 route 须留存 eval 日期。

<!-- rule-id: VERIFY-EVIDENCE-W3-005-L086 -->
- 条件“编写 model registry 时”成立时，应围绕“model quality gate 字段”形成可核对结论：model registry 须具备 quality_gate。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L092 -->
- 条件“登记 model route 时”成立时，应围绕“route eval refs 字段”形成可核对结论：每条 route 至少留存 eval refs。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L096 -->
- 条件“登记 route 证据时”成立时，应围绕“route evidence 或不适用说明”形成可核对结论：route 的 eval_refs 和 safety_refs 须指向 “技术设计”的 AI 行为部分 prompt/eval、安全样本或内容安全工件，或说明暂不适用的原因。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L161 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval capability 字段”形成可核对结论：eval gate 须具备 capability。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L162 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval owner 字段”形成可核对结论：eval gate 须具备 owner。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L163 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval baseline route 字段”形成可核对结论：eval gate 须具备 baseline_route。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L164 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval candidate route 字段”形成可核对结论：eval gate 须具备 candidate_route。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L166 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval metrics 字段”形成可核对结论：eval gate 须具备 metrics。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L167 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval thresholds 字段”形成可核对结论：eval gate 须具备 thresholds。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L168 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval tool checks 字段”形成可核对结论：eval gate 须具备 tool_checks。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L170 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval safety checks 字段”形成可核对结论：eval gate 须具备 safety_checks。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L171 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval rollout 字段”形成可核对结论：eval gate 须具备 rollout。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L172 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval rollback 字段”形成可核对结论：eval gate 须具备 rollback。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L173 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval evidence refs 字段”形成可核对结论：eval gate 须具备 evidence_refs。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L174 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval human checkpoint 字段”形成可核对结论：eval gate 须具备 human_checkpoint。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L175 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval status 字段”形成可核对结论：eval gate 须具备 status。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L229 -->
- 适用条件是“扩大 AI 工具能力时”。须逐项满足：新增工具前须执行对应 eval 或对抗样本；新增 connector 前须执行对应 eval 或对抗样本；新增写权限前须执行对应 eval 或对抗样本；新增代码执行能力前须执行对应 eval 或对抗样本；提升工具自治等级前须执行对应 eval 或对抗样本。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L243 -->
- 条件“验证 runtime 工件时”成立时，应围绕“eval 基础验证”形成可核对结论：eval fixture 和基础核验交由 Codex 与 verifier 核对。

<!-- rule-id: VERIFY-EVIDENCE-W4-001-L079 -->
- 条件“决定实现出口时”成立时，应围绕“AI 验证结果”形成可核对结论：AI coding 变更须有核验命令结果。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-005-L114 -->
- 条件“编写 flag 清单时”成立时，应围绕“flag evaluation context 字段”形成可核对结论：Feature Flag 清单须具备 evaluation_context。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W4-005-L194 -->
- 条件“改变 AI 配置时”成立时，应围绕“AI eval linkage”形成可核对结论：AI 配置变更须链接 eval run。

<!-- rule-id: VERIFY-DEV-WORKSPACE-AI-CODING-W4-006-L020 -->
- 条件“创建 Go 服务时”成立时，应围绕“首次构建结果”形成可核对结论：Go 服务模板 provenance 须保存首次构建结果。

<!-- rule-id: VERIFY-DEV-WORKSPACE-AI-CODING-W4-006-L046 -->
- 工作区验证工件默认存放于 `dev-workspace/verification/<target>.json`。

<!-- rule-id: VERIFY-DEV-WORKSPACE-AI-CODING-W4-006-L051 -->
- AI coding review 工件默认存放于 `ai-coding/review/<change-id>.md`。

<!-- rule-id: VERIFY-DEV-WORKSPACE-AI-CODING-W4-006-L052 -->
- AI coding verification 工件默认存放于 `ai-coding/verification/<change-id>.json`。

<!-- rule-id: VERIFY-DEV-WORKSPACE-AI-CODING-W4-006-L060 -->
- 条件“创建应用时”成立时，应围绕“模板首次构建结果”形成可核对结论：须留存应用模板首次构建结果。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L066 -->
- 适用条件是“执行 AI coding review 时”。须逐项满足：review 须核查意图；review 须核查架构；review 须核查 AI 常见错误；review 须核查依赖；review 须核查安全；review 须核查核验结果。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L090 -->
- 适用条件是“执行最小安全下一步时”。须逐项满足：每个 OpenSpec change 须说清本地核验命令；每个 OpenSpec change 须说清 AI 批次证据。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L038 -->
- 验证风险决策应给出含义明确的结论；可采用 `defer-release`、`rollback`、`accepted-risk`、`needs-more-tests`、`needs-fix`、`pass`，也可使用等价表述。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-001-L049 -->
- 条件“命名 dependency-container 证据时”成立时，应围绕“dependency-container 层级”形成可核对结论：dependency-container 只表示数据库、mock、工具或 test runner 在容器中，应用本身不在容器中。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L050 -->
- 条件“设计完整本地集成环境时”成立时，应围绕“集成运行方式”形成可核对结论：完整本地集成允许混用容器与宿主机进程。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L078 -->
- 核心路径涉及以下任一风险时必须进入 operational risk 专项：性能、负载、Web Vitals、bundle、DB query、AI latency/token、容量、依赖失败、429/5xx/timeout、重试、降级 UI、fault injection、dead letter、blast radius。

<!-- rule-id: VERIFY-WORKFLOW-GATE-W5-001-L092 -->
- 向[发布](09-release.md)转交之前，须确认最新冻结输入的独立 review 结论与 `governance/current-status.json` 所示状态相符。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-002-L035 -->
- 条件“验证 AI 变更时”成立时，应围绕“AI 适用范围”形成可核对结论：AI 行为与 workflow 适用本专项。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L069 -->
- 条件“维护 test strategy 时”成立时，应围绕“test strategy.AI Evals”形成可核对结论：test strategy 须具备 AI Evals。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L070 -->
- 条件“维护 test strategy 时”成立时，应围绕“test strategy.Fixtures”形成可核对结论：test strategy 须具备 Fixtures。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L082 -->
- 条件“维护 test matrix 时”成立时，应围绕“test matrix.ai_evals”形成可核对结论：test matrix 须具备 ai_evals。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L085 -->
- 条件“维护 test matrix 时”成立时，应围绕“test matrix.fixtures”形成可核对结论：test matrix 须具备 fixtures。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-002-L135 -->
- 设计 AI small tests 时，默认范围完整覆盖 prompt builder、schema validator 与 tool permission resolver。

<!-- rule-id: VERIFY-EVIDENCE-DETAIL-W5-002-L152 -->
- 条件“测试 Kratos 服务时”成立时，应围绕“Kratos 集成”形成可核对结论：medium tests 默认涵盖 Kratos usecase/repo/service 集成。

<!-- rule-id: VERIFY-TEST-FAILURE-DISPOSITION -->
- 适用条件是“large test 失败时”。须逐项满足：large test 失败须能定位 owner；large test 失败须能定位下一步。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-002-L209 -->
- 判断 AI 门禁适用性时，以下任一对象变化都属于 AI 变更：prompt；model；temperature；tool schema；retrieval；agent route；guardrail；output schema。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L213 -->
- 适用条件是“验证 AI 变更时”。须逐项满足：AI 变更 eval 须至少具备代表样例；AI 变更 eval 须至少具备边界样例；AI 变更 eval 须至少具备失败样例。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W5-002-L216 -->
- 条件“生产 prompt 变化时”成立时，应围绕“prompt eval 结果”形成可核对结论：生产 prompt 变化须链接 eval 结果。

<!-- rule-id: VERIFY-AI-PROMPT-ARTIFACT-FP-W5-002-L216 -->
- 适用条件是“生产 prompt 变化时”。须逐项满足：生产 prompt 变化须链接OpenSpec；生产 prompt 变化须链接回滚方式。

<!-- rule-id: VERIFY-EVIDENCE-DETAIL-W5-002-L246 -->
- 条件“执行本专项其余工作时”成立时，应围绕“自动化执行边界”形成可核对结论：非人工质量判断内容应由 Codex 按模板创建并由脚本核查。

<!-- rule-id: VERIFY-EVIDENCE-REFERENCE-W5-003-L035 -->
- 条件“验证用户可见 AI 时”成立时，应围绕“AI 适用范围”形成可核对结论：任何用户可见 AI 能力适用本专项。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L141 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“standard wai_aria_apg”形成可核对结论：默认 standards 须至少具备 wai_aria_apg。

<!-- rule-id: VERIFY-EVIDENCE-DETAIL-W5-003-L245 -->
- 条件“执行本专项其余验证时”成立时，应围绕“自动化执行边界”形成可核对结论：非由人决定的结构与机器核查由 Codex 和 verifier 处理。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-002-L135 -->
- 条件“发布 AI 变更时”成立时，应围绕“AI local eval”形成可核对结论：AI 单元门禁默认执行本地 eval fixtures。

<!-- rule-id: VERIFY-BUILD-TYPECHECK-FP-W6-002-L156 -->
- 条件“构建 production image 时”成立时，应围绕“multi-stage build”形成可核对结论：生产 container build 须采用 multi-stage。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-003-L143 -->
- 条件“维护 ai_settings 时”成立时，应围绕“ai_settings.eval gate”形成可核对结论：ai_settings 须具备 eval gate。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-003-L195 -->
- 维护 `ai_eval` gate 时，至少须链接一项工件；来源可为评估中的 quality rollback、技术设计中的 model route、red-team 或 eval。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-003-L306 -->
- 条件“启用客户专属 AI 配置时”成立时，应围绕“AI linkage prompt/eval”形成可核对结论：客户专属 AI 配置须链接相应的 prompt/eval 工件。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-003-L325 -->
- 条件“执行本专项其余验证时”成立时，应围绕“自动化执行边界”形成可核对结论：非由人决定的结构、敏感扫描与 fixture 由 Codex 和 verifier 处理。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-004-L317 -->
- 条件“执行本专项其余验证时”成立时，应围绕“自动化执行边界”形成可核对结论：非由人决定的结构、敏感扫描、链接、时效与 fixture 由 Codex 和 verifier 处理。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W7-004-L277 -->
- 条件“实现或维护 AI workflow 默认规则时”成立时，应围绕“运行触发专项：安全/隐私事故、漏洞披露与应急响应治理规范 / AI workflow 默认规则”形成可核对结论：修复后须补 eval/red-team case，避免同类 prompt injection、RAG poisoning、tool misuse 再次通过。

<!-- rule-id: VERIFY-EVIDENCE-W8-001-L036 -->
- 条件“执行评估最小产出相关工作时”成立时，应围绕“评估核心规范 / 最小产出”形成可核对结论：脱敏事实应说明受影响对象及其任务、发生频率和严重度，并提供证据引用及对应的 release/prompt/model/route/request id。

<!-- rule-id: VERIFY-EVIDENCE-W8-001-L083 -->
- 条件“完成评估学习并记录 continue、improve、rollback、stop 或 maintain 出口时”成立时，应围绕“评估核心规范 / 出口”形成可核对结论：`maintain` 表示在[评估](../04-operations-maintenance/11-evaluation.md)中沉淀维护决策、文档、依赖或上下文；需要形成长期证明时转交本验证项目保存证据，产生代码变更时转交[实现](07-implementation.md)。

<!-- rule-id: VERIFY-EVIDENCE-W8-003-L040 -->
- 适用条件是“执行“范围”相关工作时”。须逐项满足：安全/隐私/漏洞事故的通知及证据保全和法律边界；安全、隐私或漏洞事故的通知、证据保全和法律边界须转交 “执行” 安全/隐私事故专项。

<!-- rule-id: VERIFY-RAG-QUALITY-REGRESSION-CHECKS -->
- 适用条件是“实现或维护“AI workflow 默认规则”时”。须逐项满足：RAG 质量回归须核查索引版本；RAG 质量回归须核查 chunking；RAG 质量回归须核查 embedding/reranker；RAG 质量回归须核查 source freshness；RAG 质量回归须核查 tenant filter；RAG 质量回归须核查 citation accuracy。

<!-- rule-id: VERIFY-AGENT-QUALITY-REGRESSION-CHECKS -->
- 分项条件与结论：条件“实现或维护“AI workflow 默认规则”时”下，工具型 agent 质量回归须核查工具选择；条件“实现或维护“AI workflow 默认规则”时”下，工具型 agent 质量回归须核查参数；条件“实现或维护“AI workflow 默认规则”时”下，工具型 agent 质量回归须核查权限拒绝；条件“实现或维护“AI workflow 默认规则”时”下，工具型 agent 质量回归须核查重试；条件“实现或维护“AI workflow 默认规则”时”下，工具型 agent 质量回归须核查部分失败；条件“检查工具型 agent 回归中的审批行为时”下，工具型 agent 质量回归须核查人工审批；条件“创建或维护“AI workflow 默认规则”工件时”下，工具型 agent 质量回归须核查审计日志。

<!-- rule-id: VERIFY-LIVE-INCIDENT-RESPONSE-FP-W8-003-L259 -->
- 条件“执行 AI workflow 默认规则相关工作时”成立时，应围绕“评估触发专项：AI 质量回归、线上质量事故与回滚规范 / AI workflow 默认规则”形成可核对结论：若质量异常归因于安全、abuse 或 content policy，应先转入适用的安全或内容规范；不得以“提高通过率”为由削弱 guardrail。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W8-003-L265 -->
- 条件“创建或维护需要人判断的关键点工件时”成立时，应围绕“评估触发专项：AI 质量回归、线上质量事故与回滚规范 / 需要人判断的关键点”形成可核对结论：signal 字段命名及普通 Q-SEV3 triage、低风险 eval case 添加、复盘文案、非核心能力的小阈值调整。

<!-- rule-id: VERIFY-EVIDENCE-W9-001-L051 -->
- 继续延期过期文档、证据缺口、audit log 缺口、freshness 缺口、context pack 缺口或维护债，必须由人显式接受风险。

<!-- rule-id: VERIFY-EVIDENCE-W9-001-L072 -->
- 条件“执行维护触发型专项时”成立时，应围绕“评估中的维护规范 / 触发型专项”形成可核对结论：证据缺口暴露安全、隐私、合同或供应商边界问题时，返回[技术设计](05-technical-design.md)。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W9-003-L123 -->
- 条件“创建或维护 `maintenance/upgrade-plans/<target>.md` 工件时”成立时，应围绕“评估中的维护触发专项：依赖升级、技术债与弃用治理规范”形成可核对结论：`maintenance/upgrade-plans/<target>.md` 须具备字段 Test / Eval Matrix。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W9-003-L182 -->
- 条件“创建或维护 AI workflow 默认规则工件时”成立时，应围绕“评估中的维护触发专项：依赖升级、技术债与弃用治理规范 / AI workflow 默认规则”形成可核对结论：AI workflow 升级前须留存现有 eval baseline。

<!-- rule-id: VERIFY-AI-UPGRADE-COMPARISON -->
- 分项条件与结论：条件“创建或维护“AI workflow 默认规则”工件时”下，AI workflow 升级后须执行代表样例；条件“实现或维护“AI workflow 默认规则”时”下，AI workflow 升级后须执行边界样例；条件“实现或维护“AI workflow 默认规则”时”下，AI workflow 升级后须执行失败样例；条件“实现或维护“AI workflow 默认规则”时”下，AI workflow 升级后须对比质量；条件“实现或维护“AI workflow 默认规则”时”下，AI workflow 升级后须对比成本；条件“实现或维护“AI workflow 默认规则”时”下，AI workflow 升级后须对比错误类型。

<!-- rule-id: VERIFY-AI-DEPRECATION-DEPENDENCY-CHECK -->
- 适用条件是“删除旧 prompt 或 model route 前”。须逐项满足：删除旧 prompt 或 model route 前须确认没有 production trace 依赖旧版本；删除旧 prompt 或 model route 前须确认没有 eval 依赖旧版本；删除旧 prompt 或 model route 前须确认没有用户路径依赖旧版本。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W9-003-L191 -->
- 条件“配置自动依赖 PR 的验证 gate 时”成立时，应围绕“评估中的维护触发专项：依赖升级、技术债与弃用治理规范 / Dependabot / 自动化默认规则”形成可核对结论：自动依赖 PR 须触发对应 eval。

<!-- rule-id: VERIFY-AUTOMATED-DEPENDENCY-PR-GATE -->
- 条件“实现或维护 Dependabot / 自动化默认规则时”成立时，应围绕“评估中的维护触发专项：依赖升级、技术债与弃用治理规范 / Dependabot / 自动化默认规则”形成可核对结论：自动依赖 PR 禁止只凭版本号合并。

<!-- rule-id: VERIFY-EVIDENCE-W9-003-L191 -->
- 适用条件是“配置自动依赖 PR 的验证 gate 时”。须逐项满足：自动依赖 PR 须触发测试；自动依赖 PR 须触发构建；自动依赖 PR 须触发安全扫描。

### 异步任务、管理动作与凭据

<!-- rule-id: VERIFY-EVIDENCE-W3-005-L181 -->
- 分项条件与结论：条件“验证副作用工具时”下，有副作用工具测试须涵盖 dry-run；条件“验证副作用工具时”下，有副作用工具测试须涵盖 approval；条件“验证副作用工具时”下，有副作用工具测试须涵盖幂等；条件“验证有副作用工具时”下，有副作用工具测试须涵盖 rollback 或 compensation；条件“验证副作用工具时”下，有副作用工具测试须涵盖重复提交；条件“验证副作用工具时”下，有副作用工具测试须涵盖权限拒绝；条件“验证副作用工具时”下，有副作用工具测试须涵盖租户拒绝；条件“验证副作用工具时”下，有副作用工具测试须涵盖审计断言。

<!-- rule-id: VERIFY-JOB-TEST-PLAN-SCHEMA -->
- 分项条件与结论：建立异步工件时，job test plan 默认位于 `async-jobs/job-test-plan/<target>.json`；该计划必须包含 `target`、`owner`、`environments`、`cases`、`required_checks`、`evidence_refs`、`human_checkpoint` 和 `status`。

<!-- rule-id: VERIFY-JOB-REQUIRED-CHECKS -->
- 适用条件是“验证 job 时”。须逐项满足：required_checks 须涵盖 enqueue_schema；required_checks 须涵盖 idempotency_duplicate；required_checks 须涵盖 dequeue_lock_or_lease；required_checks 须涵盖 graceful_shutdown；required_checks 须涵盖 retry_backoff；required_checks 须涵盖 max_attempts；required_checks 须涵盖 dead_letter；required_checks 须涵盖 replay_guard；required_checks 须涵盖 cancellation；required_checks 须涵盖 timeout；required_checks 须涵盖 rate_limit_concurrency；required_checks 须涵盖 stuck_job_recovery；required_checks 须涵盖 status_polling；required_checks 须涵盖 telemetry；required_checks 须涵盖 sensitive_payload_redaction；required_checks 须涵盖 ai_cost_limit。

<!-- rule-id: VERIFY-JOB-SCENARIO-COVERAGE -->
- 分项条件与结论：条件“验证 job type 时”下，每个 job type 至少涵盖成功场景；条件“验证副作用 job 时”下，有副作用 job 须涵盖幂等；条件“验证 job type 时”下，每个 job type 至少涵盖重复提交场景；条件“验证 job type 时”下，每个 job type 至少涵盖 worker 崩溃或 lease 过期场景；条件“验证 job type 时”下，每个 job type 至少涵盖超时场景；条件“验证 job type 时”下，每个 job type 至少涵盖取消场景；条件“验证 job type 时”下，每个 job type 至少涵盖可重试错误场景；条件“验证 job type 时”下，每个 job type 至少涵盖不可重试错误场景；条件“验证 job type 时”下，每个 job type 至少涵盖死信场景；条件“验证 job type 时”下，每个 job type 至少涵盖回放保护场景；条件“验证 AI job 时”下，AI job 须涵盖 fallback 或用户可见失败状态之一；条件“验证副作用 job 时”下，有副作用 job 须涵盖重复尝试；条件“验证副作用 job 时”下，有副作用 job 须涵盖补偿或回滚路径；条件“验证副作用 job 时”下，有副作用 job 须涵盖审计；条件“验证副作用 job 时”下，有副作用 job 须涵盖外部调用失败。

<!-- rule-id: VERIFY-AI-JOB-LIMIT-AND-STATUS-COVERAGE -->
- 分项条件与结论：条件“验证 AI job 时”下，AI job 须涵盖 cost limit；条件“验证 AI job 时”下，AI job 须涵盖 token limit；条件“验证 AI job 时”下，AI job 须涵盖 model timeout；条件“验证 AI job 时”下，AI job 须涵盖 provider timeout；条件“验证对应 AI job 时”下，AI job 须涵盖 background 或 batch status polling。

<!-- rule-id: VERIFY-AI-JOB-EVAL-REFERENCES -->
- 条件“实现 AI job 时”成立时，应围绕“eval refs”形成可核对结论：AI job 须有 eval refs。

<!-- rule-id: VERIFY-ASYNC-ARTIFACT-FIXTURES -->
- 适用条件是“验证异步工件时”。须逐项满足：异步工件 positive fixture 交由 Codex 与 verifier 核对；异步工件 negative fixture 交由 Codex 与 verifier 核对。

<!-- rule-id: VERIFY-JOB-ARTIFACT-VERIFIER-279 -->
- 适用条件是“验证异步工件时”。须逐项满足：异步工件字段完整性交由 Codex 与 verifier 核对；异步工件状态机交由 Codex 与 verifier 核对；异步工件 JSON 枚举交由 Codex 与 verifier 核对；异步工件测试涵盖交由 Codex 与 verifier 核对；异步工件敏感内容扫描交由 Codex 与 verifier 核对；异步工件 OpenSpec linkage 交由 Codex 与 verifier 核对；异步工件基础核验交由 Codex 与 verifier 核对。

<!-- rule-id: VERIFY-ASYNC-JOB-WORKER-FP-W5-004-L041 -->
- 适用条件是“该运行指标适用时”。须逐项满足：DB/worker/AI 在适用时须留存 慢查询；DB/worker/AI 在适用时须留存 queue depth；DB/worker/AI 在适用时须留存 provider quota；DB/worker/AI 在适用时须留存 token；DB/worker/AI 在适用时须留存 tool iteration；DB/worker/AI 在适用时须留存 cost。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W7-003-L217 -->
- 条件“实现或维护 Go / Kratos / sqlc / gRPC 默认规则时”成立时，应围绕“运行触发专项：后台运营、人工操作与高风险动作规范”形成可核对结论：全部 admin action 须有 Go 测试或至少 dry-run fixture。

<!-- rule-id: VERIFY-EVIDENCE-W7-005-L015 -->
- 条件“执行凭据生命周期目标相关工作时”成立时，应围绕“运行触发专项：凭据、密钥与服务账号生命周期规范 / 目标”形成可核对结论：仓库只保存引用及用途、scope、owner、轮换证据和风险判断。

<!-- rule-id: VERIFY-API-CONTRACT-ERROR-MODEL-FP-W7-005-L258 -->
- 服务启动时，须校验必需 secret 是否存在，并校验其格式是否合理。

<!-- rule-id: VERIFY-EVIDENCE-W7-005-L261 -->
- 条件“执行 Go / Kratos / sqlc / gRPC 默认规则相关工作时”成立时，应围绕“运行触发专项：凭据、密钥与服务账号生命周期规范”形成可核对结论：JWT signing key、webhook signing secret 和 encryption key 轮换须定义核验方法。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W7-005-L281 -->
- 条件“创建或维护需要人判断的关键点工件时”成立时，应围绕“运行触发专项：凭据、密钥与服务账号生命周期规范 / 需要人判断的关键点”形成可核对结论：普通字段顺序及 Markdown 小节文案、低风险开发 key 命名、无生产访问的测试 fixture。

### 性能、韧性与恢复证据

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W3-005-L169 -->
- 条件“编写 runtime eval gate 时”成立时，应围绕“eval cost latency 字段”形成可核对结论：eval gate 须具备 cost_latency_limits。

<!-- rule-id: VERIFY-AI-MODEL-ROUTING-FP-W3-005-L180 -->
- 适用条件是“评估 candidate route 时”。须逐项满足：baseline 与 candidate 至少比较质量；baseline 与 candidate 至少比较拒答与安全；baseline 与 candidate 至少比较 schema 成功率；baseline 与 candidate 至少比较 tool call 成功率；baseline 与 candidate 至少比较 p95 latency；baseline 与 candidate 至少比较 token；baseline 与 candidate 至少比较 cost；baseline 与 candidate 至少比较超时率。

<!-- rule-id: VERIFY-RETRY-FALLBACK-RESILIENCE-FP-W3-005-L180 -->
- 条件“评估 candidate route 时”成立时，应围绕“fallback 触发率比较”形成可核对结论：baseline 与 candidate 至少比较 fallback 触发率。

<!-- rule-id: VERIFY-RETRY-FALLBACK-RESILIENCE-FP-W3-005-L189 -->
- 条件“编写 fallback runbook 时”成立时，应围绕“fallback Failure Modes 字段”形成可核对结论：fallback runbook 须具备 Failure Modes。

<!-- rule-id: VERIFY-EVIDENCE-W3-005-L203 -->
- 条件“处理 AI runtime 故障时”成立时，应围绕“可验证来源降级”形成可核对结论：降级模式可只返回可核验来源。

<!-- rule-id: VERIFY-EVIDENCE-W4-004-L160 -->
- 适用条件是“执行生产迁移时”。须逐项满足：生产迁移须核验行数；生产迁移须核验约束；生产迁移须核验采样结果；生产迁移须核验关键 query；生产迁移须核验 SLO 信号。

<!-- rule-id: VERIFY-BACKUP-RESTORE-RECOVERY-FP-W4-004-L227 -->
- 条件“编写 restore 文档时”成立时，应围绕“RPO RTO 章节”形成可核对结论：restore 文档须具备 RPO/RTO。

<!-- rule-id: VERIFY-EVIDENCE-W4-005-L170 -->
- 条件“改变 gRPC runtime 配置时”成立时，应围绕“gRPC 配置验证”形成可核对结论：gRPC 高风险配置生产变更须 test run 或 smoke。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L027 -->
- 适用条件是“建立本地集成环境时”。须逐项满足：完整本地环境须完成 readiness；完整本地环境须完成 smoke。

<!-- rule-id: VERIFY-EVIDENCE-W4-006-L061 -->
- 适用条件是“建立本地集成环境时”。须逐项满足：完整本地集成环境须留存 smoke 命令；完整本地集成环境须留存实际执行证据。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-001-L093 -->
- 适用条件是“存在验证缺口时”。须逐项满足：失败项、跳过项、flaky、性能退化、可访问性例外和韧性缺口须写清影响；核验缺口须留存 owner；核验缺口须留存修复或缓解方案。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-001-L095 -->
- 条件“验证产生运行或学习后续时”成立时，应围绕“运行学习交接”形成可核对结论：上线后观测、告警、runbook、incident 或 quality review 须交给 “运行”/“评估”。

<!-- rule-id: VERIFY-INTEGRATION-SMOKE-COVERAGE -->
- 分项条件与结论：条件“验证完整集成时”下，完整本地集成启动后须执行 readiness 与 smoke；条件“存在 preview 环境时”下，large tests 默认涵盖 preview 环境 smoke；条件“验证第三方依赖时”下，large tests 默认用第三方 sandbox 或真实供应商之一做最小兼容性核查；条件“生产发布后”下，large tests 默认涵盖生产发布后的只读 smoke。

<!-- rule-id: VERIFY-EVIDENCE-ARTIFACT-W5-003-L152 -->
- 条件“维护 accessibility test plan 时”成立时，应围绕“check screen_reader_smoke”形成可核对结论：默认 checks 须至少涵盖 screen_reader_smoke。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L020 -->
- 条件“运行风险验证形成运维后续时”成立时，应围绕“运维承接责任”形成可核对结论：运维负责接收 “执行” runbook、SLO 与 watch 需求。

<!-- rule-id: VERIFY-PERFORMANCE-RESILIENCE-W5-004-L030 -->
- 条件“对应运行风险被触发时”成立时，应围绕“load profile 工件”形成可核对结论：可按触发选择 load profile 工件。

<!-- rule-id: VERIFY-PERFORMANCE-RESILIENCE-W5-004-L031 -->
- 条件“对应运行风险被触发时”成立时，应围绕“failure mode map 工件”形成可核对结论：可按触发选择 failure mode map 工件。

<!-- rule-id: VERIFY-RETRY-FALLBACK-RESILIENCE-FP-W5-004-L041 -->
- 条件“该运行指标适用时”成立时，应围绕“runtime timeout”形成可核对结论：DB/worker/AI 在适用时须留存 timeout。

<!-- rule-id: VERIFY-EVIDENCE-W5-004-L044 -->
- 适用条件是“验证降级路径时”。须逐项满足：降级核验须说明用户仍能做什么；降级核验须说明用户不可做什么；降级核验须说明可稍后重试或转人工中的适用路径。

<!-- rule-id: VERIFY-EVIDENCE-W6-002-L062 -->
- 条件“组织 release 工件时”成立时，应围绕“smoke 推荐落点”形成可核对结论：推荐采用 release/smoke/<service>.md 作为 smoke 工件落点。

<!-- rule-id: VERIFY-EVIDENCE-W6-002-L237 -->
- 条件“评价发布风险时”成立时，应围绕“风险证据责任”形成可核对结论：发布风险降低须由 smoke、rollback 和 post-deploy 证据证明。

<!-- rule-id: VERIFY-EVIDENCE-W7-001-L030 -->
- 条件“执行运行适用范围相关工作时”成立时，应围绕“运行核心规范 / 适用范围”形成可核对结论：测试、性能、可访问性和韧性门禁返回本验证项目。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L068 -->
- 条件“执行运维 artifact 目录规范相关工作时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / 运维 artifact 目录规范”形成可核对结论：`ops/slo/<service>.json` 是机器可核查的 SLO 事实来源。

<!-- rule-id: VERIFY-EVIDENCE-W7-002-L102 -->
- 条件“创建或维护运维 artifact 目录规范工件时”成立时，应围绕“运行触发专项：SRE-lite 运维规范 v0.1 / 运维 artifact 目录规范”形成可核对结论：`slo_target` 须能从现有日志、指标或外部 uptime 核查计算。

<!-- rule-id: VERIFY-EVIDENCE-W7-005-L211 -->
- 条件“创建或维护 `credentials/rotation-run/<target>.json` 工件时”成立时，应围绕“运行触发专项：凭据、密钥与服务账号生命周期规范”形成可核对结论：`validation` 留存 smoke、health、synthetic call、provider usage、logs/metrics、failed auth rate 或 gRPC/API request 成功证据。

<!-- rule-id: VERIFY-EVIDENCE-W7-005-L258 -->
- 分项条件与结论：条件“服务启动时必需 secret 的存在性、格式或最小 smoke 权限校验失败时”下，必需 secret 的启动校验失败时默认 fail fast；条件“服务启动并验证必需 secret 的实际权限时”下，服务启动时须校验必需 secret 的权限能否完成最小 smoke。

<!-- rule-id: VERIFY-EVIDENCE-W8-001-L073 -->
- 条件“根据当前学习信号选择评估专项或跨项目回流路径时”成立时，应围绕“评估核心规范 / 触发型专项”形成可核对结论：学到的知识需长期保存、归档或用于上下文恢复时转交[评估](../04-operations-maintenance/11-evaluation.md)的维护主题；需要形成审计证明时转交本验证项目。

<!-- rule-id: VERIFY-EVIDENCE-W9-001-L050 -->
- 删除、归档、降级、改名或公开文档、证据、开源仓库，须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W9-001-L076 -->
- 条件“执行维护触发型专项时”成立时，应围绕“评估中的维护规范 / 触发型专项”形成可核对结论：证据来自事故、凭据、恢复或生产操作时，返回[运行](../04-operations-maintenance/10-operation.md)核对事实。

<!-- rule-id: VERIFY-CONTEXT-PACK-HANDOFF-READINESS -->
- Context pack 是否足以供人或 Codex 接手，须由人判断。

### 对外声明与证据门禁

<!-- rule-id: VERIFY-EVIDENCE-W2-005-L085 -->
- 条件“工作涉及所列表面时”成立时，应围绕“证据边界”形成可核对结论：对外 claim、供应商数据流或高成本 AI workflow 须有证据链接。

<!-- rule-id: VERIFY-JOB-CLAIM-CONCURRENCY-EVIDENCE -->
- 条件“使用数据库专有 claim SQL 时”成立时，应围绕“claim SQL 并发证据”形成可核对结论：采用专有 claim SQL 时须留存并发证据。

<!-- rule-id: VERIFY-EVIDENCE-LEVEL-GATE -->
- 适用条件是“实现用户可见 Standard/High-risk 变更前”。须逐项满足：用户可见 Standard/High-risk 变更在实现前须说明证据层级；用户可见 Standard/High-risk 变更在实现前须说明阻断完成的门禁。

<!-- rule-id: VERIFY-EVIDENCE-W6-001-L081 -->
- 条件“对外 claim 进入运行前”成立时，应围绕“claim 证据”形成可核对结论：对外 claim 须有证据。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-TRACEABILITY -->
- 适用条件是“发布对外 claim 时”。须逐项满足：每条对外 claim 须能追溯 证据；每条对外 claim 须能追溯 最后核验时间。

<!-- rule-id: VERIFY-CLAIM-EVIDENCE-MAP-REQUIREMENT -->
- 条件“治理外部 claim 时”成立时，应围绕“claim evidence map 工件”形成可核对结论：每个 production target 须维护 claim evidence map。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-EVIDENCE-RELEASE-GATE-W6-004-L082 -->
- 条件“维护 surface 时”成立时，应围绕“surface.source_of_truth”形成可核对结论：surface 须具备 source_of_truth。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L104 -->
- 维护 surface 时，`source_of_truth` 必须链接适用的事实源；允许来源完整限定为技术设计、评估维护、发布、实现，或代码、配置、eval、观测中的事实源。

<!-- rule-id: VERIFY-CLAIM-EVIDENCE-MAP-SCHEMA -->
- 适用条件是“维护 claim evidence map 时”。须逐项满足：claim evidence map 须具备 target；claim evidence map 须具备 owner；claim evidence map 须具备 claims；claim evidence map 须具备 evidence_sources；claim evidence map 须具备 substantiation_policy；claim evidence map 须具备 expiry_policy；claim evidence map 须具备 human_checkpoint；claim evidence map 须具备 status。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L122 -->
- 条件“维护 claim 时”成立时，应围绕“claim.id”形成可核对结论：claim 须具备 id。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L123 -->
- 条件“维护 claim 时”成立时，应围绕“claim.claim_text”形成可核对结论：claim 须具备 claim_text。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L124 -->
- 条件“维护 claim 时”成立时，应围绕“claim.claim_type”形成可核对结论：claim 须具备 claim_type。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L125 -->
- 条件“维护 claim 时”成立时，应围绕“claim.surface_refs”形成可核对结论：claim 须具备 surface_refs。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L126 -->
- 条件“维护 claim 时”成立时，应围绕“claim.risk_level”形成可核对结论：claim 须具备 risk_level。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L127 -->
- 条件“维护 claim 时”成立时，应围绕“claim.scope”形成可核对结论：claim 须具备 scope。

<!-- rule-id: VERIFY-CLAIM-ENTRY-EVIDENCE-REF -->
- 条件“维护 claim 时”成立时，应围绕“claim.evidence_refs”形成可核对结论：claim 须具备 evidence_refs。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L129 -->
- 条件“维护 claim 时”成立时，应围绕“claim.substantiation_level”形成可核对结论：claim 须具备 substantiation_level。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L130 -->
- 条件“维护 claim 时”成立时，应围绕“claim.last_verified”形成可核对结论：claim 须具备 last_verified。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L131 -->
- 条件“维护 claim 时”成立时，应围绕“claim.expires_at”形成可核对结论：claim 须具备 expires_at。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L132 -->
- 条件“维护 claim 时”成立时，应围绕“claim.owner”形成可核对结论：claim 须具备 owner。

<!-- rule-id: VERIFY-EXTERNAL-CLAIM-COMMITMENT-FP-W6-004-L133 -->
- 条件“维护 claim 时”成立时，应围绕“claim.status”形成可核对结论：claim 须具备 status。

<!-- rule-id: VERIFY-CLAIM-TYPE-ENUM -->
- 条件“维护 claim evidence map 时”成立时，应围绕“claim type enum”形成可核对结论：claim_type 须采用 ai_capability、ai_limitation、accuracy_or_quality、latency_or_performance、availability_sla、security、privacy_data_use、data_retention、no_training、data_residency、human_review、compliance、billing_refund、support_response、api_stability 或 ip_license 之一。

<!-- rule-id: VERIFY-AI-EVAL-FIXTURE-W6-004-L156 -->
- 条件“记录 claim substantiation 时”成立时，应围绕“substantiation enum”形成可核对结论：substantiation_level 须采用 source_link、config_verified、test_or_eval、slo_measurement、contract_or_dpa、manual_attestation 或 unsupported 之一。

<!-- rule-id: VERIFY-CLAIM-CORRECTION-SURFACE-CHECKS -->
- 适用条件是“更正对外 claim 时”。须逐项满足：claim 更正须核查 docs；claim 更正须核查 SDK；claim 更正须核查 support macro；claim 更正须核查 contract/order；claim 更正须核查 AI disclosure；claim 更正须核查 privacy；claim 更正须核查 security page；claim 更正须核查 developer changelog；claim 更正须核查 sales material。

<!-- rule-id: VERIFY-CLAIM-GATE-LOG -->
- 条件“记录 claim gate 事件时”成立时，应围绕“claim log evidence ref”形成可核对结论：claim gate 日志须保存 evidence ref。

<!-- rule-id: VERIFY-CLAIM-SURFACE-EVIDENCE-PRESENTATION -->
- 条件“设计 claim surface 时”成立时，应围绕“Geist claim presentation”形成可核对结论：Geist claim surface 应优先清晰排版及状态徽标、表格、时间戳和证据链接。

<!-- rule-id: VERIFY-EVIDENCE-W7-001-L071 -->
- 审计证据包、长期证据保全或 trust center 证据必须进入本验证项目的审计证据主题；是否需要单独 evidence change 由本规范的触发条件决定。

<!-- rule-id: VERIFY-EVIDENCE-W9-001-L052 -->
- 向客户、审计方、监管方、律师、供应商或公众导出证据包，须由人决定。

<!-- rule-id: VERIFY-EVIDENCE-W9-001-L065 -->
- 条件“执行审计证据触发型专项时”成立时，应围绕“验证中的长期证据规范 / 触发型专项”形成可核对结论：审计证据、证据包、audit log、retention、customer/security evidence 或 SOC 2 readiness，先在本验证项目最小产出的证据索引中登记。

<!-- rule-id: VERIFY-EVIDENCE-W9-001-L075 -->
- 条件“执行审计证据触发型专项时”成立时，应围绕“验证中的长期证据规范 / 触发型专项”形成可核对结论：对外证据包或开源 release 变成公开承诺时，返回[发布](09-release.md)。

## 输入与产物

Deliver 验证输入至少包括已确认的产品行为与验收、技术与风险边界、实现差异、适用的 `visual_ux` 判定与已批准 UX、测试/eval 数据、环境与依赖说明。Explore 验证只消费 question、hypothesis、sandbox boundary、shortest slice 与当前 showcase，并使用可理解 fixture 记录 observed behavior、visible fact、limits 和 next decision。产物由上文各 canonical rule 定义；相同事实只保留一个权威记录，其他项目引用其 target 或工件链接。

证据记录必须如实标明层级。unit/component、宿主机 integration、仅依赖容器、完整本地集成、Browser E2E、provider sandbox 与生产观察互不冒充；格式校验、构建成功或 OpenSpec validation 也不等同于产品与语义验收。

## 完成、停止或退出条件

Deliver 完成意味着适用目标均有当前证据，命令、环境、启动组件、覆盖路径、结果与未覆盖项可定位，关键旅程达到要求的证据层级，required 可视 UX 与实现的一致性已核对，失败与例外已有真实处置。Explore 可以合法以 `invalidated`、`revise` 或 `stopped` 结束；证据准确命名比通过数量更重要，showcase 不会自动产生 Deliver 完成结论。出现不可解释失败、关键证据缺失、需要改动上游定义、真实环境验证越界或需人接受的风险时停止推进，并按上文 target 返回相应项目或人工 checkpoint。

验证通过且发布风险可解释时，转交“发布”；实现方向仍成立但测试失败时，退回“实现”修复；产品、契约、AI 行为或风险边界被推翻时，分别退回“定义/体验设计”“技术设计”或相关权威项目；运行观察和学习后续交给“运行”与“评估”。

## 相关项目引用

- “定义”与“体验设计”提供产品行为、关键旅程、适用的已批准可视 UX 和验收口径；验证只证明，不重定义。
- “技术设计”提供契约、安全、权限、成本、数据、AI runtime 与恢复边界；验证发现边界不成立时退回。
- “计划”记录需要跟踪的验证工作、例外 owner 和后续项。
- “实现”提供可构建产物、本地运行入口与修复；验证不在此复制实现规范。
- “发布”消费通过结论、rollback、smoke 和未决风险；真实环境变更仍由发布项目授权。
- “运行”提供生产信号、事故、凭据轮换与恢复演练引用；“评估”把反馈和质量回归转成下一轮验证输入。
