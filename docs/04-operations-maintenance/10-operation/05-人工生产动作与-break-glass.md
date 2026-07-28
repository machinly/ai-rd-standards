# 运行：人工生产动作与 break-glass

## 执行细则

<!-- rule-id: OPERATION-ADMIN-001 -->
后台操作视为产品代码管理。内部 admin/support console、运营脚本、one-off command、后台 job 与数据修复工具，只要会改变用户数据、权限、租户、计费权益、退款/credit、feature flag、配置、AI workflow、生产依赖或外部通知，就必须使用同一 `<target>` 维护 `admin-ops/action-registry/<target>.json`、`operator-playbook/<target>.md` 与 `ops-review/<target>.md`，覆盖 dry-run、approval、audit、rollback/compensate。正式 migration/backfill 的执行规范另管，但其人工审批仍在本项目内。

<!-- rule-id: OPERATION-ADMIN-002 -->
任何未注册动作不得进入生产 admin UI、support tool、agent tool 或运营脚本；执行前必须确认该动作已在 action registry 登记。

<!-- rule-id: OPERATION-ADMIN-003 -->
动作风险使用闭集：`R0-readonly` 为不涉及敏感数据和跨租户的只读；`R1-low` 为单用户低风险状态变更；`R2-sensitive` 涉及付费、权益、个人数据、AI 输出补救或生产配置；`R3-destructive` 涉及删除、批量修复、跨租户、退款/credit、权限、外部通知或直接写生产数据；`R4-break-glass` 为绕过常规权限或紧急生产访问。

<!-- rule-id: OPERATION-ADMIN-004 -->
`R1-low` 可自动化但必须审计；`R2-sensitive` 必须 human checkpoint；`R3-destructive` 必须先 dry-run、获批准并具备回滚或补偿计划；`R4-break-glass` 只授予限时访问并全量审计。

<!-- rule-id: OPERATION-ADMIN-005 -->
`admin-ops/operator-playbook/<target>.md` 必须包含 Scope、When To Use、Preconditions、Dry Run、Execute、Verify、Rollback / Compensate、Abort / Escalation、Communication 与 Linked Artifacts。

<!-- rule-id: OPERATION-ADMIN-006 -->
执行任何 admin action 前必须确认当前 actor 对目标、租户与动作均有权限。

<!-- rule-id: OPERATION-ADMIN-007 -->
能够 dry-run 的后台动作不得直接执行；dry-run 或 precheck 必须列出影响对象、数量、受影响租户、金额、权限影响与外部副作用。

<!-- rule-id: OPERATION-ADMIN-008 -->
实际执行必须从最小范围开始：单租户、单用户、单批次，并保持可停止。

<!-- rule-id: OPERATION-ADMIN-009 -->
执行后必须验证用户影响、数据一致性、审计事件、告警与回滚点。

<!-- rule-id: OPERATION-ADMIN-010 -->
关闭或补偿动作时，必须记录结果、失败、回滚、credit、用户沟通及后续 action。

<!-- rule-id: OPERATION-ADMIN-011 -->
批量生产数据修复、真实生产 backfill、生产数据或跨租户访问、impersonation、break-glass、R2/R3/R4 动作、生产 SQL/脚本/REPL/一次性 job，以及让 AI 或 agent 获得生产写权限，均必须人工判断。

<!-- rule-id: OPERATION-ADMIN-012 -->
AI 可以协助调查、归类、生成 dry-run plan、解释风险和草拟记录，但不得自主退款、删除、改权限、跨租户访问、发外部通知、改生产配置或执行 break-glass；AI 触发的任何写操作必须产生 audit event。

<!-- rule-id: OPERATION-ADMIN-013 -->
租户上线涉及 admin action 时，必须经过本运行项目中后台运营专项的审批、dry-run、rollback 与 audit log 控制。
