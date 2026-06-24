# Proposal: define admin ops action standard

## 意图

建立一人公司后台运营、人工操作与高风险动作规范，覆盖 admin action 登记、dry-run、approval、rollback/compensate、audit log、break-glass、AI operator 自治级别和运营复盘，避免临场 SQL、隐藏后台按钮或 agent 写工具绕过研发与运维门禁。

## 范围

- 新增 `admin-ops-action-standard` spec。
- 新增阶段 24 规范文档。
- 创建 `admin-ops-action-guard` skill 和 verifier。
- 补充来源索引与 README。

## 不做什么

- 不引入企业级 PAM、SIEM、SOAR、ITSM 审批平台或多人职责分离体系。
- 不替代 data migration、billing reconciliation、security/privacy、incident response 或 release pipeline；本阶段定义人工生产动作的共同控制面。
- 不连接真实生产数据库、云账号、后台系统或用户数据。
- 不允许 AI agent 自动执行高风险生产写操作；默认只读/建议。

## 依据

- 《人月神话》和小型项目管理。
- Twelve-Factor App Admin Processes。
- Google SRE Automation / Eliminating Toil、Emergency Response、Reliable Product Launches。
- OWASP Authorization、Logging、Top 10 A09 Security Logging and Monitoring Failures。
- NIST SP 800-53 Rev. 5。
- OpenAI Agent Builder Safety。
- Google SRE AI Engineering Reliable Operations。

## 需要人的判断

只有这些需要人工 checkpoint：生产数据访问、跨租户访问、用户 impersonation、break-glass、删除/批量修改、退款/credit、权益覆盖、权限变更、外部通知、无 dry-run/rollback/audit 的高风险动作、AI 自动写工具、生产 SQL/REPL/脚本、绕过发布/权限/审计/安全检查。
