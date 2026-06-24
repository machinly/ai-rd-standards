# admin-ops-action-standard 规格

## Purpose

定义一人公司生产后台运营、人工操作、高风险动作、审计、break-glass 和 AI operator 的安全边界，确保生产数据、计费、权限、配置、AI workflow 和外部副作用的人工变更可授权、可 dry-run、可审计、可回滚或可补偿。

## Requirements

### Requirement: 生产 target 必须定义 admin ops artifacts

任何包含后台操作、生产脚本、support/admin console、manual data fix、AI operator 或高风险人工动作的 target MUST 在发布前具备 admin ops artifacts。

#### Scenario: 新增生产后台动作

- GIVEN 一个 target 新增或修改后台动作、生产脚本、support/admin console、manual data fix 或 AI operator tool
- WHEN 创建或更新 OpenSpec change
- THEN 创建 `admin-ops/action-registry/<target>.json`
- AND 创建 `admin-ops/operator-playbook/<target>.md`
- AND 创建 `admin-ops/audit-log-schema/<target>.json`
- AND 创建 `admin-ops/break-glass/<target>.md`
- AND 创建 `admin-ops/ops-review/<target>.md`

### Requirement: Action registry 必须登记动作、风险、权限、dry-run、回滚和审计

Action registry MUST 记录 target、owner、actions、risk levels、permission model、approval policy、dry-run policy、rollback policy、rate limits、observability、AI autonomy、人审点和复审节奏。

#### Scenario: 登记一个后台写动作

- GIVEN 后台动作会改变用户、租户、数据、计费、权益、配置、AI workflow 或外部副作用
- WHEN 写入 `admin-ops/action-registry/<target>.json`
- THEN action 包含 id、name、category、scope、risk_level、actor、authorization、input_schema、prechecks、dry_run、execution_path、rollback、audit_event 和 status
- AND R2/R3/R4 动作必须有 human checkpoint、dry-run 或等价预检查、rollback/compensate 和 audit event

### Requirement: Operator playbook 必须指导安全执行和中止

Operator playbook MUST 记录 scope、when to use、preconditions、dry run、execute、verify、rollback/compensate、abort/escalation、communication 和 linked artifacts。

#### Scenario: 执行生产人工动作

- GIVEN founder 或 operator 准备执行后台动作
- WHEN 使用 `admin-ops/operator-playbook/<target>.md`
- THEN playbook 指导确认 action registry、权限、linked artifact、dry-run 结果和影响范围
- AND 指导执行后验证用户影响、数据一致性、审计事件、告警和回滚点

### Requirement: Audit log schema 必须覆盖高风险动作证据

Audit log schema MUST 记录 event name、required fields、sensitive fields、retention、storage、integrity、alerts、query examples 和 human checkpoint。

#### Scenario: 记录一次高风险后台动作

- GIVEN R1/R2/R3/R4 后台动作执行或 dry-run
- WHEN 写入 audit event
- THEN 审计事件包含 event_id、timestamp、actor_id、actor_type、tenant_id、action_id、action_version、reason、linked_artifact、request_id、dry_run、approval_id、target_resource、before_ref、after_ref、status 和 error_class
- AND 审计记录使用 append-only 或等价完整性控制
- AND 不保存 secret、完整 raw prompt、完整 raw response 或不必要个人数据

### Requirement: Break-glass 必须限时、记录、撤销和复盘

Break-glass policy MUST 记录 scope、triggers、access grant、time limit、allowed actions、forbidden actions、logging、communication、revoke 和 review。

#### Scenario: 常规权限无法恢复生产影响

- GIVEN SEV、数据恢复、安全事件、账号锁定、供应商故障或无法通过常规权限恢复用户
- WHEN 使用 break-glass
- THEN 访问被限时授予
- AND 允许动作和禁止动作被记录
- AND 所有动作进入审计日志
- AND 结束后撤销访问并完成 review

### Requirement: Ops review 必须减少危险手工动作和权限漂移

Ops review MUST 记录 recent actions、high risk actions、failed/aborted actions、audit gaps、permission drift、toil to automate、AI autonomy review 和 next one change。

#### Scenario: 周期性复盘后台运营动作

- GIVEN 到达每周或双周 ops review 节奏
- WHEN 更新 `admin-ops/ops-review/<target>.md`
- THEN 记录高风险动作、失败或中止动作、审计缺口、权限漂移和重复 toil
- AND 只选择一个最高影响改进作为 next one change

### Requirement: AI operator 不得默认自动执行高风险写动作

AI operator、support assistant 或 admin agent MUST NOT autonomously execute R2/R3/R4 actions unless explicit OpenSpec approval, structured action schema, server-side prechecks, audit events, rollback/compensate path, and human checkpoint are present.

#### Scenario: AI 建议生产后台动作

- GIVEN AI 从支持消息、事故上下文、日志或产品反馈中提出后台动作
- WHEN 动作涉及写生产、钱、权限、删除、隐私、安全、外部通知、跨租户或 break-glass
- THEN AI 只能生成结构化 plan 或 dry-run request
- AND 服务端执行权限、precheck、approval、audit 和 rollback 校验
- AND 人工批准后才可执行

### Requirement: Admin ops artifacts 不得保存敏感内容

Admin ops artifacts MUST NOT 保存真实 secret、生产 DSN、供应商 token、私钥、完整 raw prompt、完整 raw response、完整用户数据、银行卡数据或不必要个人联系方式。

#### Scenario: 记录动作、审计字段或操作证据

- GIVEN 需要保存后台动作定义、审计字段、dry-run 结果或复盘证据
- WHEN 写入 `admin-ops/` artifacts
- THEN 使用引用、摘要、hash、redacted diff、request id 和 linked artifact
- AND 不保存真实 secret、生产 DSN、供应商 token、私钥、完整 raw prompt、完整 raw response、完整用户数据、银行卡数据或不必要个人联系方式
