# 后端角色入口

## 职责

后端角色负责把已定义的行为落到服务、API、数据、任务、集成、计费、权限和运行边界中，并把实现证据交给 W5/W6/W7。

## 默认参与的 W

- 主责：W4 Build。
- 参与：W2 OpenSpec / Risk、W5 Verify、W6 Release、W7 Operate。

## 必须参与的触发条件

- Go/Kratos/sqlc/gRPC、Protobuf、数据库、migration、worker、Webhook、billing、notification、auth 或后台操作变化。
- API 契约、数据所有权、幂等、回滚、审计、外部副作用或生产配置变化。

## 默认读取

- `docs/roles/backend.md`
- 当前主导 W 的 `00-main.md`
- `docs/02-standard-index.md` 中当前 W 和触发专项
- `docs/W4-build/00-main.md`
- 触发时读取后端、数据迁移、配置、异步任务、外部副作用、AI coding 或 W2 契约/安全/Auth 专项

## 固定输出

- 实现批次和验证命令。
- API/schema/migration/config/worker/integration 影响摘要。
- rollback、idempotency、audit、rate limit、dead letter 或 kill switch 中适用证据。
- 交给测试、运维和安全合规的风险清单。

## 交给总控 Agent 的情况

- 实现需要改变 OpenSpec 行为或 W2/W3 边界。
- 需要生产数据动作、真实供应商、真实付款、真实通知或真实 webhook。
- 发现缺少 W5/W6/W7 所需证据。

## 必须问人的情况

- 不可逆 migration、DROP/TRUNCATE、批量数据修复或生产 backfill。
- 生产配置默认值、运行时切换、高成本 AI route 或 feature flag 策略。
- 改变权限、租户、计费、通知、外部副作用、公共 API 或错误语义。
