# 研发工作审查契约

这份文件区分“生产者自检”和“独立最终审查”。两者不能互相冒充。

## Producer Self-Check

执行者在交付前回答：

- 结果是否满足 outcome 和 acceptance？
- 实现所依据的产品输入和体验设计是否真实存在并经人确认，而不是由 OpenSpec 代替？
- 用户可见 Standard/High-risk 是否记录 `visual_ux` 判定；required 时，当前静态 UX 是否由人明确 `approved`，批准后实质偏差是否重新 review？
- Standard/High-risk 实现是否有 active OpenSpec change、strict validation 和真实 tasks 状态；若跳过，是否有用户批准记录？
- 是否修改了范围外内容？
- 是否保留用户已有工作？
- 验证命令是否真实运行并记录结果？
- 证据是否准确标为 unit、integration、依赖容器、完整本地集成、浏览器 E2E、provider sandbox 或生产观察？
- 多组件项目是否实际启动全部后端、前端、数据库和必要 mock/provider，而不是零散拼接测试？
- 用户可见范围是否有关键旅程矩阵；Browser E2E 是否为可重复自动化而非人工局部检查？
- `governance/current-status.json` 是否与最新独立 review 和关键旅程结果一致？
- 是否存在未披露的失败、跳过或假设？
- 是否有更小、更可逆的方案？
- 是否触发 High-risk 人工批准？

Self-check 可以使用两个视角：

- A：一人可执行性和流程成本；
- B：产品、工程、运行和安全风险。

A/B 是一次自检的两个镜头，不是独立 review。

## High-risk Pre-Implementation Review

auth、数据迁移、管理员权限、身份绑定、跨租户和难回退契约在生产性实现前，由未参与设计的人检查：权威产品输入、状态/并发语义、权限边界、数据保留、回滚/前向恢复、测试矩阵和禁止结论。发现缺口时先改设计，不把问题推迟到最终终审。

## Independent Final Review

Standard 和 High-risk 的最终 reviewer 必须：

- 未参与产出；
- 使用干净上下文；
- 读取目标、acceptance、产物/diff 和验证证据；
- 对新用户能力读取权威产品输入、体验设计和验收映射；缺失时不得只按技术 brief 接受；
- 对 `visual_ux: required` 的 change，读取当前 `flow.md`、关键 wireframes、人工批准和偏差记录；缺少批准或存在未复审实质偏差时不得接受；
- 以陌生验收者身份从干净完整本地环境执行关键用户/管理员旅程；不能只审 API、事务和安全工件；
- 不以生产者的完成声明作为证据；
- 只报告影响正确性、风险、数据、安全或明确需求的问题；
- 记录 reviewer、日期、目标版本和结论。
- 核对完成声明与证据层级一致；局部测试不得支持系统/E2E 结论。
- 最新 review 为 changes-requested 或关键旅程失败时，确认旧完成摘要已经失效。

最小记录：

    Reviewer:
    Reviewed at:
    Target revision:
    Scope:
    Evidence checked:
    Findings:
    Decision: accept | changes-requested | reject
    Residual risks:

## 通过条件

Quick：

- 相关验证通过；
- 没有隐藏 High-risk 副作用。

Standard：

- self-check 完成；
- 独立 reviewer 接受；
- acceptance 有证据。
- `visual_ux: required` 时有当前人类批准，且实现实质偏差已经重新 review；
- 用户可见范围的阻断旅程具有最新 Browser E2E pass；人工检查或 skip_e2e 不能支持 accepted。

High-risk：

- Standard 条件全部满足；
- decision owner 已明确批准；
- rollback 和 stop conditions 可执行；
- 副作用后的观察或通知路径明确。

## 不能作为通过证据

- “文档很完整”；
- “格式校验通过”；
- “执行者认为已经完成”；
- 用 AI 推断、一般授权、OpenSpec validation 或已经完成的实现代替可视 UX 人类批准；
- 用 OpenSpec 代替产品文档、体验设计或未确认决策；
- 只有 OpenSpec 格式 PASS，没有对应 acceptance 和真实运行证据；
- 用依赖容器或宿主 integration 冒充完整本地集成/浏览器 E2E；
- 用 manual browser check、DOM/焦点检查或 API 代替页面业务动作冒充 Browser E2E；
- 最新 review 为 changes-requested，却仍引用较早 pass 摘要宣称完成；
- 同一执行者生成的第二段 review；
- 没有对应 acceptance 的大量测试；
- 没有真实任务数据的自主等级声明。
