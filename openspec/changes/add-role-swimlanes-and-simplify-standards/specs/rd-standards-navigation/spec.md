# rd-standards-navigation 的角色泳道与精简变更规格

## ADDED Requirements

### Requirement: 导航层必须支持角色泳道入口

研发规范导航层 MUST 同时支持 workflow-first 和 role-first 两种入口。角色入口 MUST 把产品、Tech Lead、后端、前端、测试、运维、运营和安全合规映射到 W0-W9，而不是建立一条替代 W0-W9 的瀑布流程。

#### Scenario: 按角色进入规范

- GIVEN 用户或 Agent 想以产品、前端、后端、测试、运维、运营或安全合规角色参与工作
- WHEN 打开 `docs/03-role-index.md`
- THEN 文档说明 W0-W9 是主线、角色是泳道
- AND 文档指向对应 `docs/roles/*.md`
- AND 每个角色入口说明默认参与的 W、固定输出和升级条件

### Requirement: 多 Agent 执行必须由总控 Agent 先定位 W0-W9

当使用多个角色 Agent 执行研发工作时，总控 Agent MUST 先判断主导 W，再按角色泳道调度角色 Agent。角色 Agent MUST 只读取自己的角色入口和当前 W 相关规范。

#### Scenario: 调度多个角色 Agent

- GIVEN 一个研发请求需要多个角色参与
- WHEN 总控 Agent 开始执行
- THEN 总控 Agent 先说明当前主导 W
- AND 总控 Agent 列出参与角色和需要读取的规范
- AND 每个角色 Agent 输出自己的判断、artifact、风险、缺口和人审点
- AND 总控 Agent 汇总冲突并更新 OpenSpec 或 tasks

### Requirement: 专项规范必须有明确角色消费者

每个保留的触发型专项 MUST 能说明它服务哪个角色、哪个 W、什么触发条件、最小产出是什么，以及为什么不能由父级 `00-main.md` 覆盖。

#### Scenario: 评估一个专项是否保留

- GIVEN 仓库中存在一个触发型专项规范
- WHEN 执行专项精简 review
- THEN review 判断该专项的主要角色消费者
- AND 判断它是否承接高频工作或高风险门禁
- AND 判断它是否有独立最小工件或验证价值
- AND 如果答不清，则合并、降级或删除该专项

### Requirement: 低频专项必须优先降级而不是继续扩展

低频、未来可能才需要、或只有长清单但没有独立执行入口的专项 MUST 默认降级为父级 `00-main.md` 的触发提醒、附录或 OpenSpec change 记录，除非用户明确决定保留独立文档。

#### Scenario: 处理低频治理主题

- GIVEN 一个专项只服务低频场景，例如模型优化训练、复杂本地化、商业合同、审计证据或开源社区维护
- WHEN 执行精简
- THEN 默认把它降级为父级入口中的触发提醒
- AND 保留必须问人的高影响判断
- AND 不继续维护完整独立专项，除非用户明确接受其维护成本

### Requirement: 精简后的规范必须保持两种可恢复读法

精简完成后，仓库 MUST 保持两种可恢复读法：按 W0-W9 流程读，以及按角色泳道读。两种读法都 MUST 避免要求用户或 Agent 通读全部专项。

#### Scenario: 新 session 接手规范仓库

- GIVEN 新 Codex session 接手本仓库
- WHEN 读取 README
- THEN README 指向 `docs/00-start-here.md` 作为流程入口
- AND README 指向 `docs/03-role-index.md` 作为角色入口
- AND context pack 说明先定位 W0-W9，再选择角色泳道
- AND 索引和校验脚本能够发现死链或缺失角色入口
