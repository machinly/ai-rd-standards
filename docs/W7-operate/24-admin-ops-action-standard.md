# 阶段 24：后台运营、人工操作与高风险动作规范

## 目标

一人公司最危险的生产操作，常常不是正式发布，而是“我临时进后台改一下”“跑个 SQL 修一下”“让 AI agent 帮我处理一下”。这些动作绕过 release pipeline、测试、权限和审计，会直接影响钱、权限、数据、隐私、用户信任和恢复能力。第 24 阶段定义后台运营、人工操作与高风险动作规范，让每个生产 target 都能回答：哪些动作允许人做，谁能做，何时需要批准，怎么 dry-run，怎么回滚，怎么审计，AI 能帮到哪一步。

默认原则：后台操作也是产品代码的一部分。能写成受控动作的，不靠临场 SQL；能 dry-run 的，不直接执行；能由 AI 建议的，不等于 AI 可以自动写生产。

## 核心依据

- 《人月神话》：后台操作复杂度来自隐式状态和概念不一致；临时脚本不是银弹，反而会制造不可见耦合。
- 小型项目管理：一人公司只保留能防止高损失误操作、恢复上下文和降低重复劳动的最小工件。
- Twelve-Factor App Admin Processes：管理任务应作为 one-off processes 运行在与应用相同 release、codebase 和 config 中，避免同步漂移。
- Google SRE Automation / Eliminating Toil：自动化能降低重复劳动，但拥有 admin 权限的自动化必须防御性校验、预先评估风险，并在不安全时退回人工。
- Google SRE Emergency Response：rollback 和应急流程必须提前测试，否则事故中会放大影响。
- Google SRE Reliable Product Launches：checklist 能让发布和运营动作可重复、可审查，但必须按本系统裁剪。
- OWASP Authorization Cheat Sheet：后台操作也要 least privilege、deny by default、每次请求校验权限和记录日志。
- OWASP Logging / Top 10 A09：高价值事务和安全事件需要审计轨迹；日志不足会让攻击和误操作无法检测。
- NIST SP 800-53 Rev. 5：访问控制、审计与问责、事件响应等控制家族可裁剪为一人公司的最小风险管理。
- OpenAI Agent Builder Safety：涉及敏感工具或特权上下文时，应避免把不可信输入放入高优先级指令，用结构化输出约束数据流。
- Google SRE AI Engineering Reliable Operations：AI 运维自动化应按监控、调查、批准、执行和自主管理逐级推进，高风险执行默认需要人批准。

## 范围

适用对象：

- 内部 admin console、support console、运营脚本、one-off command、后台 job、数据修复工具。
- 会改变用户数据、权限、租户、计费权益、退款/credit、feature flag、配置、AI workflow、生产依赖或外部通知的动作。
- Go/Kratos/gRPC admin API、sqlc 数据修正、Vite 后台页面、AI operator / support assistant / admin agent。

不适用对象：

- 已完全由 migration/backfill 规范覆盖的正式数据迁移；但触发 migration 的人工审批仍属于本阶段。
- 只读 dashboard、公开帮助页、无生产数据访问的本地实验。
- 企业级 PAM、SIEM、SOAR、ITSM 审批流和多人职责分离体系；需要时单独开合规或企业客户 change。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
admin-ops/
  action-registry/<target>.json
  operator-playbook/<target>.md
  audit-log-schema/<target>.json
  break-glass/<target>.md
  ops-review/<target>.md
```

### `admin-ops/action-registry/<target>.json`

动作注册表必须包含：

- `target`
- `owner`
- `actions`
- `risk_levels`
- `permission_model`
- `approval_policy`
- `dry_run_policy`
- `rollback_policy`
- `rate_limits`
- `observability`
- `ai_autonomy`
- `human_checkpoint`
- `review_cadence`

`actions` 每项至少包含：

- `id`
- `name`
- `category`
- `scope`
- `risk_level`
- `actor`
- `authorization`
- `input_schema`
- `prechecks`
- `dry_run`
- `execution_path`
- `rollback`
- `audit_event`
- `status`

默认风险级别：

- `R0-readonly`：只读、无敏感数据、无跨租户影响。
- `R1-low`：单用户低风险状态变更，可自动化，必须审计。
- `R2-sensitive`：涉及付费、权益、个人数据、AI 输出补救或生产配置，必须 human checkpoint。
- `R3-destructive`：删除、批量修复、跨租户、退款/credit、权限、外部通知、生产数据直接写入，必须 dry-run、批准、回滚或补偿计划。
- `R4-break-glass`：绕过常规权限或紧急生产访问，只能限时、全量审计、事后复盘。

默认：任何未注册动作不得进入生产 admin UI、support tool、agent tool 或运营脚本。

### `admin-ops/operator-playbook/<target>.md`

操作 playbook 必须包含：

- `Scope`
- `When To Use`
- `Preconditions`
- `Dry Run`
- `Execute`
- `Verify`
- `Rollback / Compensate`
- `Abort / Escalation`
- `Communication`
- `Linked Artifacts`

默认执行顺序：

1. 确认动作已在 action registry 登记，且当前 actor 有权限。
2. 链接原因：support case、incident、billing reconciliation、OpenSpec change、security/privacy request 或 data migration。
3. 先 dry-run 或预检查：影响对象、数量、租户、金额、权限、外部副作用。
4. 执行最小范围：单租户、单用户、单批次、可停止。
5. 验证用户影响、数据一致性、审计事件、告警和回滚点。
6. 关闭或补偿：记录结果、失败、回滚、credit、用户沟通和后续 action。

### `admin-ops/audit-log-schema/<target>.json`

审计日志 schema 必须包含：

- `target`
- `owner`
- `event_name`
- `required_fields`
- `sensitive_fields`
- `retention`
- `storage`
- `integrity`
- `alerts`
- `query_examples`
- `human_checkpoint`

`required_fields` 至少包含：

- `event_id`
- `timestamp`
- `actor_id`
- `actor_type`
- `tenant_id`
- `action_id`
- `action_version`
- `reason`
- `linked_artifact`
- `request_id`
- `dry_run`
- `approval_id`
- `target_resource`
- `before_ref`
- `after_ref`
- `status`
- `error_class`

默认：

- 高风险动作审计采用 append-only 或等价不可随意覆盖方式。
- 审计记录保存引用、摘要、hash 或 redacted diff，不保存完整 secret、完整 raw prompt、完整 raw response 或不必要个人数据。
- 审计日志本身是敏感资产，访问也要记录。

### `admin-ops/break-glass/<target>.md`

break-glass 策略必须包含：

- `Scope`
- `Triggers`
- `Access Grant`
- `Time Limit`
- `Allowed Actions`
- `Forbidden Actions`
- `Logging`
- `Communication`
- `Revoke`
- `Review`

默认：

- break-glass 只用于 SEV、数据恢复、安全事件、账号锁定、供应商故障或无法通过常规权限恢复用户的情况。
- 访问必须限时，结束后撤销。
- 不允许用 break-glass 常态化处理普通客服、产品试验、功能开关或批量数据修正。
- 每次 break-glass 后必须有 review，并补行动作注册表或 runbook 缺口。

### `admin-ops/ops-review/<target>.md`

运营复盘必须包含：

- `Recent Actions`
- `High Risk Actions`
- `Failed / Aborted Actions`
- `Audit Gaps`
- `Permission Drift`
- `Toil To Automate`
- `AI Autonomy Review`
- `Next One Change`

默认：

- 每周或每两周复盘一次近期 admin action。
- 只选一个最高影响改进：补 dry-run、补审计、收紧权限、移除危险脚本、写 runbook、自动化重复动作。
- 如果某个手工动作重复 2 次以上，必须决定：产品修复、文档修复、受控 admin action、自动化，或明确不处理。

## Go / Kratos / sqlc / gRPC 默认规则

- Admin API 必须是显式服务面，不靠隐藏 HTTP route 或 Vite 前端按钮保护。
- Go/Kratos middleware 必须执行身份、租户、权限、风险级别、approval 和 request id 校验。
- gRPC metadata 传播 actor、tenant、request id、approval id；不接受浏览器传入的“已批准”声明。
- sqlc 表默认包含：`admin_actions`、`admin_action_runs`、`admin_approvals`、`audit_events`、`break_glass_sessions`。
- 高风险写操作默认通过业务 usecase 执行，不直接手写生产 SQL；确需 SQL 时走 data migration / data fix 工件。
- 所有 admin action 必须有 Go 测试或至少 dry-run fixture；R2/R3/R4 需要集成或回放测试。

## Vite 前端默认规则

- 后台 UI 是工作台，不是营销页：信息密度高、状态清晰、按钮少而明确，符合 Vercel/Geist 的克制风格。
- 每个高风险按钮必须展示动作名、目标对象、影响数量、dry-run 结果、approval 状态和 rollback/compensate 说明。
- 隐藏路由、按钮禁用、前端角色判断不是安全边界；服务端必须重复校验。
- R2/R3/R4 操作必须二次确认；确认文本要包含目标和动作，不使用模糊“确定吗”。
- 后台页面不得显示不必要个人数据、secret、完整 prompt/response、支付敏感信息。

## AI workflow 默认规则

- AI 可以帮助调查、归类、生成 dry-run plan、解释风险和草拟操作记录。
- 默认自治级别是 L0/L1：AI 只读或建议，人执行。
- AI 触发写操作必须通过结构化 action schema、服务端 precheck、policy check、audit event 和 human checkpoint。
- 不允许把用户输入、客服消息、网页内容直接拼进高优先级 developer/system 指令后调用高权限工具。
- AI 不得自主执行退款、删除、权限变更、跨租户访问、外部通知、生产配置变更或 break-glass。

## 需要人判断的关键点

只把这些判断交给人：

- 是否允许生产数据访问、跨租户访问、用户 impersonation 或 break-glass。
- 是否执行 R2/R3/R4 动作，尤其是删除、批量修改、退款/credit、权益覆盖、权限变更、外部通知。
- 是否接受没有 dry-run、没有 rollback/compensate、没有审计字段或没有测试的高风险动作。
- 是否允许 AI 从建议升级到自动执行，或允许 agent 调用写工具。
- 是否手工运行生产 SQL、脚本、REPL、一次性 job 或数据修复。
- 是否绕过正常发布、权限、feature flag、审计、rate limit 或安全检查。

其他字段完整性、章节、动作登记、审计字段、敏感内容、review 节奏和基础风险分类由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“能做什么、怎么做、怎么记、紧急时怎么进、事后怎么改进”。
- 保留：人只判断生产数据、钱、权限、删除、跨租户、AI 自动写、break-glass 和绕过安全边界。
- 调整：不要求企业 PAM 或多人审批；一人公司先用显式 action registry、approval id、审计和复盘替代。
- 调整：不禁止脚本和后台工具；要求它们像产品代码一样 versioned、dry-run、testable、auditable。
- 风险：action registry 可能过度膨胀。缓解：只登记生产可执行动作；纯只读 dashboard 不强制进入 R2/R3 流程。

结论：可落地。一个人可以先为真实产品列出 5 到 10 个最常见 admin action，再逐步把危险脚本收敛到可审计、可回滚的后台动作。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：支持、计费、数据修复和用户沟通不再靠临场判断，降低误操作伤害用户信任。
- 工程角度：Go/Kratos/sqlc/gRPC 有服务端校验、结构化 action、测试和审计表路径。
- 运维角度：dry-run、rollback、abort、break-glass 和 review 连接阶段 5/21 的恢复能力。
- 安全隐私角度：least privilege、deny by default、审计、敏感字段最小化和生产数据访问 checkpoint 明确。
- 成本角度：重复手工动作通过 `Toil To Automate` 进入一个最高影响改进，不会无限建设内部平台。

结论：可落地。第 24 阶段补上了前面各阶段共同需要的“人操作生产”的安全面：不是不让人动，而是让每次动都有边界、证据和后悔药。
